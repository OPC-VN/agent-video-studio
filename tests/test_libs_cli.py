import base64
import hashlib
import io
import json
import os
import tarfile

import pytest

from video_studio import runtime_libs as libs, _netfetch
from video_studio.contract import ContractError, EngineError


@pytest.fixture
def package(tmp_path, monkeypatch):
    files = {'package/a.js': b'a', 'package/b.js': b'b'}
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w:gz') as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(name); info.size = len(data); tar.addfile(info, io.BytesIO(data))
    blob = stream.getvalue(); lock = libs.load_lock(); p = lock['packages']['gsap']
    p['tarball_sha256'] = hashlib.sha256(blob).hexdigest(); p['npm_integrity'] = 'sha512-' + base64.b64encode(hashlib.sha512(blob).digest()).decode()
    lock['libs']['gsap']['members'] = [{'member': name, 'dest': name.split('/')[-1], 'file_sha256': hashlib.sha256(data).hexdigest(), 'max_bytes': 50} for name,data in files.items()]
    monkeypatch.setattr(libs, 'load_lock', lambda path=None: lock)
    station = tmp_path / 'station'; station.mkdir()
    calls = []
    def fetcher(url, **kwargs): calls.append(url); return url, 'application/octet-stream', blob
    return station, lock, blob, calls, fetcher


def test_plan_no_network_and_confirmation(package):
    station, lock, blob, calls, fetcher = package
    assert set(libs.fetch_plan([], station)[0]['libs']) == set(lock['libs'])
    assert libs.fetch_plan(['gsap'], station)[0]['libs'] == ['gsap']
    with pytest.raises(ContractError): libs.fetch(['gsap'], False, station=station, fetcher=fetcher)
    assert not calls


def test_fetch_once_and_verify(package):
    station, lock, blob, calls, fetcher = package
    libs.fetch(['gsap'], True, station=station, fetcher=fetcher)
    assert len(calls) == 1
    assert libs.load(['gsap'], station) == {'a.js': b'a', 'b.js': b'b'}


def test_invalid_tarball_leaves_old_file(package):
    station, lock, blob, calls, fetcher = package
    dest = station / 'runtime-libs/gsap/3.15.0/a.js'; dest.parent.mkdir(parents=True); dest.write_bytes(b'old')
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, station=station, fetcher=lambda *a, **k: ('https://registry.npmjs.org/x', '', b'bad'))
    assert dest.read_bytes() == b'old'


def test_fetcher_categories(package):
    station, lock, blob, calls, fetcher = package
    def failed(kind):
        def f(*a, **k): raise _netfetch.FetchError('failure', kind=kind)
        return f
    with pytest.raises(EngineError): libs.fetch(['gsap'], True, station=station, fetcher=failed('network'))
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, station=station, fetcher=failed('policy'))


def test_overrides_are_copied():
    source = {'gsap': 'one'}
    libs.set_overrides(source); source['gsap'] = 'changed'
    result = libs.get_overrides(); result['gsap'] = 'changed'
    assert libs.get_overrides() == {'gsap': 'one'}
    libs.set_overrides({})


def test_fetch_rejects_redirect_and_integrity(package):
    station, lock, blob, calls, fetcher = package
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, station=station, fetcher=lambda *a, **k: ('https://evil.example/x', '', blob))
    lock['packages']['gsap']['npm_integrity'] = 'sha512-' + base64.b64encode(bytes(64)).decode()
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, station=station, fetcher=fetcher)
    assert not (station / 'runtime-libs').exists()


def test_from_file_offline_multimember(package, tmp_path):
    station, lock, blob, calls, fetcher = package
    a = tmp_path / 'a'; b = tmp_path / 'b'; a.write_bytes(b'a'); b.write_bytes(b'b')
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, from_file={'a.js': a}, station=station, fetcher=fetcher)
    libs.fetch(['gsap'], True, from_file={'a.js': a, 'b.js': b}, station=station, fetcher=fetcher)
    assert not calls and libs.load(['gsap'], station) == {'a.js': b'a', 'b.js': b'b'}


def test_symlink_tar_member_rejected(package):
    station, lock, blob, calls, fetcher = package
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w:gz') as tar:
        item = tarfile.TarInfo('package/a.js'); item.type = tarfile.SYMTYPE; item.linkname = '../outside'; tar.addfile(item)
    blob = stream.getvalue(); p = lock['packages']['gsap']; p['tarball_sha256'] = hashlib.sha256(blob).hexdigest(); p['npm_integrity'] = 'sha512-' + base64.b64encode(hashlib.sha512(blob).digest()).decode()
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, station=station, fetcher=lambda url, **kw: (url, '', blob))
    assert not (station / 'runtime-libs').exists()


def test_actual_netfetch_error_categories(package):
    station, lock, blob, calls, fetcher = package
    def network(url, **kwargs):
        return _netfetch.fetch_public(url, **kwargs, resolver=lambda *_: (_ for _ in ()).throw(OSError('dns unavailable')))
    with pytest.raises(EngineError): libs.fetch(['gsap'], True, station=station, fetcher=network)
    def policy(url, **kwargs):
        return _netfetch.fetch_public('https://evil.example/x', **kwargs)
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, station=station, fetcher=policy)


def test_cli_confirmation_and_plan(package, monkeypatch, capsys):
    station, lock, blob, calls, fetcher = package
    monkeypatch.setattr(libs._env, 'station_dir', lambda: str(station))
    assert libs.main(['fetch', 'gsap', '--json']) == 2
    out = json.loads(capsys.readouterr().out); assert out['error'] == 'needs_confirmation' and out['plan']
    assert libs.main(['plan', 'gsap', '--json']) == 0
    assert json.loads(capsys.readouterr().out)['ok'] is True


def test_fetch_does_not_overwrite_existing_conflict(package):
    station, lock, blob, calls, fetcher = package
    dest = station / 'runtime-libs/gsap/3.15.0/a.js'; dest.parent.mkdir(parents=True); dest.write_bytes(b'old')
    with pytest.raises(ContractError): libs.fetch(['gsap'], True, station=station, fetcher=fetcher)
    assert dest.read_bytes() == b'old' and not (dest.parent / 'b.js').exists()


def test_two_libs_one_package_downloaded_once(package):
    station, lock, blob, calls, fetcher = package
    ms = lock['libs']['gsap']['members']; lock['libs']['gsap']['members'] = ms[:1]
    lock['libs']['other'] = {'package': 'gsap', 'members': ms[1:], 'requires': ['gsap']}
    libs.fetch(['other'], True, station=station, fetcher=fetcher)
    assert len(calls) == 1 and libs.load(['other'], station) == {'a.js': b'a', 'b.js': b'b'}


def test_gnu_longname_recursion_is_contract_error(package):
    import gzip
    station, lock, _, _, _ = package
    long = tarfile.TarInfo('././@LongLink'); long.type = tarfile.GNUTYPE_LONGNAME; long.size = 2
    block = long.tobuf(format=tarfile.GNU_FORMAT) + b'x\0' + bytes(510)
    raw = block * 1500 + bytes(1024)
    blob = gzip.compress(raw)
    p = lock['packages']['gsap']
    p['tarball_sha256'] = hashlib.sha256(blob).hexdigest()
    p['npm_integrity'] = 'sha512-' + base64.b64encode(hashlib.sha512(blob).digest()).decode()
    with pytest.raises(ContractError):
        libs._extract_package(blob, 'gsap', ['gsap'], lock)


@pytest.mark.skipif(os.name == 'nt', reason='POSIX openat/link publication')
@pytest.mark.parametrize('race', [False, True])
def test_posix_partial_publication_reports_recovery(package, monkeypatch, race):
    station, lock, blob, calls, fetcher = package
    original = os.link; links = []
    def fail_second(src, dst, **kwargs):
        links.append(dst)
        if len(links) == 2:
            if race:
                path = station / 'runtime-libs/gsap/3.15.0' / dst
                path.write_bytes(b'other process')
            raise FileExistsError('simulated race') if race else OSError('simulated I/O')
        return original(src, dst, **kwargs)
    monkeypatch.setattr(os, 'link', fail_second)
    with pytest.raises(ContractError if race else EngineError, match=r'a\.js') as error:
        libs.fetch(['gsap'], True, station=station, fetcher=fetcher)
    assert 'libs fetch' in str(error.value)
    directory = station / 'runtime-libs/gsap/3.15.0'
    assert (directory / 'a.js').read_bytes() == b'a'
    if race: assert (directory / 'b.js').read_bytes() == b'other process'
    else: assert not (directory / 'b.js').exists()


@pytest.mark.skipif(os.name != 'nt', reason='Windows native publication')
@pytest.mark.parametrize('race', [False, True])
def test_windows_publication_failure_preserves_other_files(package, monkeypatch, race):
    from video_studio.effect_library import _native_windows as native
    station, lock, blob, calls, fetcher = package
    original = native.rename_no_replace; calls = []
    def fail_second(handle, root, dest):
        calls.append(dest)
        if len(calls) == 2:
            if race: (station / 'runtime-libs/gsap/3.15.0' / dest).write_bytes(b'other process')
            raise OSError('simulated failure')
        return original(handle, root, dest)
    monkeypatch.setattr(native, 'rename_no_replace', fail_second)
    with pytest.raises(OSError): libs.fetch(['gsap'], True, station=station, fetcher=fetcher)
    directory = station / 'runtime-libs/gsap/3.15.0'
    assert not (directory / 'a.js').exists()
    if race: assert (directory / 'b.js').read_bytes() == b'other process'
    else: assert not (directory / 'b.js').exists()


@pytest.mark.parametrize('race', [False, True])
def test_posix_publication_failure_reports_published_files_mock(monkeypatch, race):
    import posixpath
    import types
    import io
    calls = []; copied = {}; temps = {}; nextfd = [100]
    def open_fake(path, flags, *args, dir_fd=None):
        if path in ('a.js', 'b.js'): raise FileNotFoundError(path)
        nextfd[0] += 1
        if path.startswith('item-'): temps[nextfd[0]] = path
        return nextfd[0]
    class Writer(io.BytesIO):
        def __init__(self, fd): super().__init__(); self.fd = fd
        def fileno(self): return self.fd
        def close(self): copied[temps[self.fd]] = self.getvalue(); super().close()
    def link_fake(src, dest, **kwargs):
        calls.append(dest)
        if len(calls) == 2: raise FileExistsError('raced') if race else OSError('I/O failed')
        assert copied[src] == b'a'
    fake = types.SimpleNamespace(name='posix', path=types.SimpleNamespace(isdir=lambda _: True, abspath=lambda p: p),
        O_RDONLY=0, O_DIRECTORY=1, O_NOFOLLOW=2, O_NONBLOCK=4, O_WRONLY=8, O_CREAT=16, O_EXCL=32,
        open=open_fake, close=lambda fd: None, fdopen=lambda fd, mode: Writer(fd), fsync=lambda fd: None,
        mkdir=lambda *a, **kw: None, link=link_fake, unlink=lambda *a, **kw: None,
        fstat=lambda fd: types.SimpleNamespace(st_mode=0o40700, st_uid=42, st_dev=1, st_ino=2),
        stat=lambda *a, **kw: types.SimpleNamespace(st_dev=1, st_ino=2), geteuid=lambda: 42, rmdir=lambda *a, **kw: None)
    monkeypatch.setattr(libs, 'os', fake)
    with pytest.raises(ContractError if race else EngineError, match=r'a\.js') as error:
        libs._publish_files('/station', 'gsap', '3.15.0', {'a.js': b'a', 'b.js': b'b'})
    assert 'libs fetch' in str(error.value)


def test_posix_temp_entry_is_not_in_attacker_writable_target(monkeypatch):
    import io
    import types
    entries = {}; handles = {}; counter = [100]; target = {}
    def open_fake(name, flags, *args, dir_fd=None):
        if name == 'a.js': raise FileNotFoundError(name)
        counter[0] += 1; fd = counter[0]
        if flags & 16: handles[fd] = (dir_fd, name)
        return fd
    class Writer(io.BytesIO):
        def __init__(self, fd): super().__init__(); self.fd = fd
        def fileno(self): return self.fd
        def close(self): entries[handles[self.fd]] = self.getvalue(); super().close()
    def link_fake(src, dest, *, src_dir_fd, dst_dir_fd, follow_symlinks):
        # Attacker controls the destination directory, not a 0700 staging directory.
        if src_dir_fd == dst_dir_fd: entries[(src_dir_fd, src)] = b'attacker'
        target[dest] = entries[(src_dir_fd, src)]
    fake = types.SimpleNamespace(name='posix', path=types.SimpleNamespace(isdir=lambda _: True, abspath=lambda p: p),
        O_RDONLY=0, O_DIRECTORY=1, O_NOFOLLOW=2, O_NONBLOCK=4, O_WRONLY=8, O_CREAT=16, O_EXCL=32,
        open=open_fake, close=lambda fd: None, fdopen=lambda fd, mode: Writer(fd), fsync=lambda fd: None,
        mkdir=lambda *a, **kw: None, link=link_fake, unlink=lambda *a, **kw: None,
        rmdir=lambda *a, **kw: None, fchmod=lambda *a: None,
        fstat=lambda fd: types.SimpleNamespace(st_mode=0o40700, st_uid=42, st_dev=1, st_ino=2),
        stat=lambda *a, **kw: types.SimpleNamespace(st_dev=1, st_ino=2), geteuid=lambda: 42)
    monkeypatch.setattr(libs, 'os', fake)
    libs._publish_files('/station', 'gsap', '3.15.0', {'a.js': b'verified'})
    assert target['a.js'] == b'verified'


def test_posix_replaced_staging_owner_rejected_before_write(monkeypatch):
    import types
    calls=[]
    def open_fake(path, flags, *args, dir_fd=None):
        if path == 'a.js': raise FileNotFoundError(path)
        if path.startswith('item-'): pytest.fail('must not create file in untrusted staging directory')
        return 9
    fake = types.SimpleNamespace(name='posix', path=types.SimpleNamespace(isdir=lambda _: True, abspath=lambda p: p),
        O_RDONLY=0, O_DIRECTORY=1, O_NOFOLLOW=2, O_NONBLOCK=4, O_WRONLY=8, O_CREAT=16, O_EXCL=32,
        open=open_fake, close=lambda fd: None, mkdir=lambda *a, **kw: None,
        fstat=lambda fd: types.SimpleNamespace(st_mode=0o40700, st_uid=43, st_dev=1, st_ino=2),
        geteuid=lambda: 42, rmdir=lambda *a, **kw: calls.append('removed'))
    monkeypatch.setattr(libs, 'os', fake)
    with pytest.raises(ContractError): libs._publish_files('/station', 'gsap', '3.15.0', {'a.js': b'verified'})
    assert calls == []


def test_posix_cleanup_never_removes_stage_directory_by_name(monkeypatch):
    import io
    import types
    entries = {}; handles = {}; counter = [100]; removed = []
    def op(name, flags, *args, dir_fd=None):
        if name == 'a.js': raise FileNotFoundError(name)
        counter[0] += 1; fd=counter[0]
        if flags & 16: handles[fd] = (dir_fd, name)
        return fd
    class Writer(io.BytesIO):
        def __init__(self, fd): super().__init__(); self.fd=fd
        def fileno(self): return self.fd
        def close(self): entries[handles[self.fd]]=self.getvalue(); super().close()
    fake=types.SimpleNamespace(name='posix', path=types.SimpleNamespace(isdir=lambda _: True, abspath=lambda p:p),
      O_RDONLY=0,O_DIRECTORY=1,O_NOFOLLOW=2,O_NONBLOCK=4,O_WRONLY=8,O_CREAT=16,O_EXCL=32,
      open=op,close=lambda fd:None,fdopen=lambda fd,mode:Writer(fd),fsync=lambda fd:None,
      mkdir=lambda *a,**kw:None,link=lambda *a,**kw:None,unlink=lambda *a,**kw:None,
      fstat=lambda fd:types.SimpleNamespace(st_mode=0o40700,st_uid=42,st_dev=1,st_ino=2),
      stat=lambda *a,**kw:types.SimpleNamespace(st_dev=1,st_ino=2),geteuid=lambda:42,
      rmdir=lambda *a,**kw:removed.append(a))
    monkeypatch.setattr(libs,'os',fake)
    libs._publish_files('/station','gsap','3.15.0',{'a.js':b'verified'})
    assert not removed
