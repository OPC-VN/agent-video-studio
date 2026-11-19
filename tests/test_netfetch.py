"""Tải công khai có ghim địa chỉ (`video_studio._netfetch`) — RQ-033, TK1.

Test không ra mạng ngoài. Bộ phân giải và bộ kết nối được tiêm; hai ca dùng `127.0.0.1` thật (máy chủ
trong tiến trình test) để kiểm đường kết nối mặc định.
"""
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from video_studio import _netfetch as nf

PUBLIC = "93.184.216.34"


class FakeResp:
    def __init__(self, status=200, headers=None, body=b""):
        self.status = status
        self._headers = {k.lower(): v for k, v in (headers or {}).items()}
        self._body = body
        self.pos = 0

    def getheader(self, name, default=None):
        return self._headers.get(name.lower(), default)

    def read(self, amt=None):
        end = len(self._body) if amt is None else min(len(self._body), self.pos + amt)
        chunk = self._body[self.pos:end]
        self.pos = end
        return chunk


class FakeConn:
    def __init__(self, resp, log, call):
        self.resp, self.log, self.call = resp, log, call

    def request(self, method, path, headers=None):
        self.log.append({**self.call, "method": method, "path": path, "headers": dict(headers or {})})

    def getresponse(self):
        return self.resp

    def close(self):
        pass


def make(responses, resolver_ips=None):
    """-> (resolver, connector, log). `responses` là danh sách FakeResp trả lần lượt."""
    log, calls = [], {"resolve": 0}
    queue = list(responses)

    def resolver(host, port):
        calls["resolve"] += 1
        if resolver_ips is None:
            return [PUBLIC]
        value = resolver_ips(host) if callable(resolver_ips) else resolver_ips
        if value is None:
            raise OSError("không phân giải được")
        return value

    def connector(scheme, host, ip, port, timeout):
        return FakeConn(queue.pop(0), log, {"scheme": scheme, "host": host, "ip": ip, "port": port})

    return resolver, connector, log, calls


def get(url, resp=None, **kw):
    resolver, connector, log, calls = make([resp or FakeResp(200, {"Content-Type": "image/png"}, b"x" * 10)],
                                           kw.pop("ips", None))
    out = nf.fetch_public(url, max_bytes=kw.pop("max_bytes", 1000), resolver=resolver, connector=connector, **kw)
    return out, log, calls


def test_dns_rebinding_resolver_called_once():
    (_url, _ct, data), log, calls = get("https://img.example.com/a.png")
    assert data == b"x" * 10
    assert calls["resolve"] == 1                       # không phân giải lại giữa kiểm và kết nối
    assert log[0]["ip"] == PUBLIC and log[0]["host"] == "img.example.com"


@pytest.mark.parametrize("ip", [
    "127.0.0.1", "10.0.0.1", "169.254.169.254", "224.0.0.1", "100.64.0.1",
    "::1", "fe80::1", "fec0::1", "ff02::1", "::7f00:1",
    "64:ff9b::7f00:1", "2002:7f00:1::", "::ffff:10.0.0.1"])
def test_blocks_non_public(ip):
    resolver, connector, log, _ = make([FakeResp()], resolver_ips=[ip])
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://x.example.com/a.png", max_bytes=10, resolver=resolver, connector=connector)
    assert log == []                                   # chưa mở kết nối nào


def test_any_internal_address_blocks_even_with_public_siblings():
    resolver, connector, log, _ = make([FakeResp()], resolver_ips=[PUBLIC, "10.0.0.5"])
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://x.example.com/", max_bytes=10, resolver=resolver, connector=connector)
    assert log == []


def test_numeric_hosts_resolved_then_blocked():
    resolver, connector, log, _ = make([FakeResp()], resolver_ips=["127.0.0.1"])
    with pytest.raises(nf.FetchError):
        nf.fetch_public("http://2130706433/", max_bytes=10, resolver=resolver, connector=connector)
    assert log == []


@pytest.mark.parametrize("url", [
    "https://user@example.com/a.png", "https://user:pw@example.com/a.png", "https://example.com\\@evil/a.png",
    "https://exa\x00mple.com/a.png", "https://example.com:0/a.png", "https://example.com:99999/a.png",
    "https:///a.png", "file:///etc/passwd", "ftp://example.com/a.png", "", " "])
def test_url_sanitising(url):
    resolver, connector, log, _ = make([FakeResp()])
    with pytest.raises(nf.FetchError):
        nf.fetch_public(url, max_bytes=10, resolver=resolver, connector=connector)
    assert log == []


def test_host_header_is_normalised_hostname_and_port():
    _out, log, _ = get("http://Example.COM:8080/p?q=1")
    assert log[0]["headers"]["Host"] == "example.com:8080"
    assert log[0]["path"] == "/p?q=1"


def test_redirect_to_internal_blocked_before_connect():
    first = FakeResp(302, {"Location": "http://127.0.0.1/secret"})
    resolver, connector, log, _ = make([first, FakeResp(200, {}, b"hi")],
                                       resolver_ips=lambda h: ["127.0.0.1"] if h == "127.0.0.1" else [PUBLIC])
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://a.example.com/", max_bytes=10, resolver=resolver, connector=connector)
    assert [c["host"] for c in log] == ["a.example.com"]         # đích nội bộ không được kết nối


def test_relative_redirect_followed_and_missing_location_rejected():
    resolver, connector, log, _ = make([FakeResp(301, {"Location": "/b.png"}), FakeResp(200, {}, b"ok")])
    url, _ct, data = nf.fetch_public("https://a.example.com/x/a.png", max_bytes=10,
                                     resolver=resolver, connector=connector)
    assert url == "https://a.example.com/b.png" and data == b"ok"
    resolver, connector, log, _ = make([FakeResp(302, {})])
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://a.example.com/", max_bytes=10, resolver=resolver, connector=connector)


def test_redirect_to_other_scheme_rejected():
    resolver, connector, _log, _ = make([FakeResp(302, {"Location": "file:///etc/passwd"})])
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://a.example.com/", max_bytes=10, resolver=resolver, connector=connector)


def test_redirect_limit():
    loop = [FakeResp(302, {"Location": "https://a.example.com/n"}) for _ in range(10)]
    resolver, connector, log, _ = make(loop)
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://a.example.com/", max_bytes=10, resolver=resolver, connector=connector,
                        max_redirects=3)
    assert len(log) == 4                                         # 1 lần đầu + 3 chuyển hướng


def test_unresolvable_fails_closed():
    resolver, connector, log, _ = make([FakeResp()], resolver_ips=lambda h: None)
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://nope.example.com/", max_bytes=10, resolver=resolver, connector=connector)
    assert log == []


def test_cap_exact_ok_cap_plus_one_rejected():
    (_u, _c, data), _l, _ = get("https://a.example.com/", FakeResp(200, {}, b"y" * 100), max_bytes=100)
    assert len(data) == 100
    with pytest.raises(nf.FetchError):
        get("https://a.example.com/", FakeResp(200, {}, b"y" * 101), max_bytes=100)


def test_declared_content_length_over_cap_rejected_before_reading():
    resp = FakeResp(200, {"Content-Length": "5000"}, b"y" * 10)
    with pytest.raises(nf.FetchError):
        get("https://a.example.com/", resp, max_bytes=100)
    assert resp.pos == 0                                         # từ chối trước khi đọc thân


def test_total_deadline(monkeypatch):
    now = {"t": 0.0}
    monkeypatch.setattr(nf, "_now", lambda: now["t"])

    class Slow(FakeResp):
        def read(self, amt=None):
            now["t"] += 40.0                                    # mỗi lần đọc tốn 40 giây
            return super().read(min(amt or 4096, 4))

    with pytest.raises(nf.FetchError):
        get("https://a.example.com/", Slow(200, {}, b"y" * 1000), max_bytes=10000, total_deadline=60)


def test_http_error_status_rejected():
    with pytest.raises(nf.FetchError):
        get("https://a.example.com/", FakeResp(404, {}, b"no"))


def test_content_type_returned_lowercase():
    (_u, ct, _d), _l, _ = get("https://a.example.com/", FakeResp(200, {"Content-Type": "Image/PNG"}, b"x"))
    assert ct == "image/png"


@pytest.mark.parametrize("url", [
    "https://evilgithub.com/x", "https://x.github.com/x", "https://github.com.evil.com/x",
    "http://github.com/x"])
def test_allowed_hosts_exact_match(url):
    resolver, connector, log, _ = make([FakeResp(200, {}, b"ok")])
    with pytest.raises(nf.FetchError):
        nf.fetch_public(url, max_bytes=10, allowed_hosts=("github.com", "api.github.com"),
                        resolver=resolver, connector=connector)
    assert log == []


def test_allowed_hosts_accepts_listed_and_checks_redirects():
    resolver, connector, log, _ = make([FakeResp(200, {}, b"ok")])
    out = nf.fetch_public("https://GitHub.com./x", max_bytes=10, allowed_hosts=("github.com",),
                          resolver=resolver, connector=connector)
    assert out[2] == b"ok"
    resolver, connector, log, _ = make([FakeResp(302, {"Location": "https://cdn.example.com/x"}), FakeResp()])
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://github.com/x", max_bytes=10, allowed_hosts=("github.com",),
                        resolver=resolver, connector=connector)
    assert [c["host"] for c in log] == ["github.com"]


def test_gate_still_uses_shared_block_table():
    from video_studio.reference import gate
    assert gate._ip_is_internal is nf.ip_is_internal
    assert gate._BLOCKED_V4 is nf._BLOCKED_V4 and gate._BLOCKED_V6 is nf._BLOCKED_V6


# ── kết nối mặc định, THẬT trên loopback (RF4 của Cổng 1) ───────────────────────────────

def test_real_pinned_connection_sends_original_host(monkeypatch):
    seen = {}

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            seen["host"] = self.headers.get("Host")
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        port = srv.server_address[1]
        monkeypatch.setattr(nf, "ip_is_internal", lambda ip: False)   # chỉ cho test: đích là loopback
        calls = []

        def resolver(host, p):
            calls.append(host)
            return ["127.0.0.1"]

        _u, ct, data = nf.fetch_public(f"http://example.test:{port}/a.png", max_bytes=100, resolver=resolver)
    finally:
        srv.shutdown()
    assert data == b"ok" and ct == "image/png"
    assert seen["host"] == f"example.test:{port}"                    # Host là tên gốc, không phải IP
    assert calls == ["example.test"]                                  # chỉ phân giải một lần


def test_https_uses_server_hostname_and_verifies(monkeypatch):
    rec = {}

    class Ctx:
        check_hostname = True

        def wrap_socket(self, sock, server_hostname=None):
            rec["sni"] = server_hostname
            rec["check_hostname"] = self.check_hostname
            raise OSError("dừng ở đây")

    class Sock:
        def close(self):
            pass

    monkeypatch.setattr(nf.ssl, "create_default_context", lambda *a, **k: Ctx())
    monkeypatch.setattr(nf.socket, "create_connection", lambda addr, timeout=None, **k: rec.setdefault("addr", addr) and Sock())
    with pytest.raises(nf.FetchError):
        nf.fetch_public("https://img.example.com/a.png", max_bytes=10, resolver=lambda h, p: [PUBLIC])
    assert rec["sni"] == "img.example.com" and rec["check_hostname"] is True
    assert rec["addr"][0] == PUBLIC                                    # kết nối tới IP đã ghim


def test_structured_error_categories_are_stable():
    resolver, connector, _, _ = make([], resolver_ips=None)
    with pytest.raises(nf.FetchError) as denied:
        nf.fetch_public('https://evil.example/', max_bytes=3, allowed_hosts={'registry.npmjs.org'}, resolver=resolver, connector=connector)
    assert denied.value.kind == 'policy'
    resolver, connector, _, _ = make([], resolver_ips=lambda host: None)
    with pytest.raises(nf.FetchError) as network:
        nf.fetch_public('https://registry.npmjs.org/', max_bytes=3, allowed_hosts={'registry.npmjs.org'}, resolver=resolver, connector=connector)
    assert network.value.kind == 'network'
    resolver, connector, _, _ = make([FakeResp(200, {'Content-Length': '4'}, b'abcd')])
    with pytest.raises(nf.FetchError) as oversized:
        nf.fetch_public('https://registry.npmjs.org/', max_bytes=3, allowed_hosts={'registry.npmjs.org'}, resolver=resolver, connector=connector)
    assert oversized.value.kind == 'policy'
    resolver, connector, _, _ = make([FakeResp(302, {'Location': 'https://evil.example/'})])
    with pytest.raises(nf.FetchError) as redirect:
        nf.fetch_public('https://registry.npmjs.org/', max_bytes=3, allowed_hosts={'registry.npmjs.org'}, resolver=resolver, connector=connector)
    assert redirect.value.kind == 'policy'
    resolver, connector, _, _ = make([])
    with pytest.raises(nf.FetchError) as timeout:
        nf.fetch_public('https://registry.npmjs.org/', max_bytes=3, total_deadline=0, allowed_hosts={'registry.npmjs.org'}, resolver=resolver, connector=connector)
    assert timeout.value.kind == 'network'


@pytest.mark.parametrize("value, limit, expected", [
    ("0" * 5000, 0, 0),
    ("0" * 5000 + "1", 1, 1),
    ("0" * 5000 + "1000000000000", 1000000000000, 1000000000000),
])
def test_declared_length_normalizes_long_zero_prefix(value, limit, expected):
    assert nf._declared_length(value, limit) == expected


@pytest.mark.parametrize("value, limit", [
    ("0" * 5000 + "2", 1),
    ("0" * 5000 + "1000000000001", 1000000000000),
    ("9" * 5000, 1000000000000),
])
def test_declared_length_rejects_values_above_limit(value, limit):
    with pytest.raises(nf.FetchError):
        nf._declared_length(value, limit)


@pytest.mark.parametrize("header, body", [("0" * 5000, b""), ("0" * 5000 + "1", b"x")])
def test_fetch_accepts_zero_padded_declared_length(header, body):
    (url, _ct, data), _log, _ = get("https://a.example.com/", FakeResp(200, {"Content-Length": header}, body), max_bytes=1)
    assert url == "https://a.example.com/" and data == body


def test_fetch_rejects_zero_padded_length_before_reading():
    resp = FakeResp(200, {"Content-Length": "0" * 5000 + "2"}, b"xx")
    with pytest.raises(nf.FetchError):
        get("https://a.example.com/", resp, max_bytes=1)
    assert resp.pos == 0
