"""Security primitives for S4 input: local snapshot and pipe-only decoding."""
import hashlib
import sys

import pytest

from video_studio.contract import ContractError, EngineError
from video_studio.reference._scan_media import input_options, read_snapshot, run_bounded


def test_signature_and_digest_of_snapshot(tmp_path):
    path = tmp_path / 'source.mp4'
    content = b'\x00\x00\x00\x18ftypisom' + b'\x00' * 20
    path.write_bytes(content)
    raw, digest = read_snapshot(path)
    assert raw == content and digest == hashlib.sha256(content).hexdigest()
    assert input_options() == ['-protocol_whitelist', 'pipe', '-f', 'mov', '-enable_drefs', '0', '-use_absolute_path', '0', '-i', 'pipe:0']


def test_rejects_noncontainer_and_oversize(tmp_path):
    path = tmp_path / 'faked.mp4'
    path.write_text('ffconcat version 1.0\nfile /tmp/other\n', encoding='utf8')
    with pytest.raises(ContractError):
        read_snapshot(path)
    path.write_bytes(b'\x00\x00\x00\x18ftypisom' + b'x' * 50)
    with pytest.raises(ContractError):
        read_snapshot(path, limit=16)


def test_run_bounded_delivers_bytes_and_rejects_oversized_output():
    assert run_bounded([sys.executable, '-c', 'import sys;sys.stdout.buffer.write(sys.stdin.buffer.read())'], b'abc', timeout=5)[0] == b'abc'
    with pytest.raises(EngineError, match='trần'):
        run_bounded([sys.executable, '-c', 'import sys;sys.stdout.write("x"*10000)'], b'', timeout=5, stdout_limit=50)


def test_run_bounded_rejects_timeout():
    with pytest.raises(EngineError, match='thời hạn'):
        run_bounded([sys.executable, '-c', 'import time;time.sleep(5)'], b'', timeout=.1)
import json, shutil, subprocess
import pytest
from video_studio.contract import EngineError
from video_studio.reference._scan_media import input_options, read_snapshot, run_bounded


@pytest.mark.skipif(not shutil.which('ffmpeg') or not shutil.which('ffprobe'), reason='cần ffmpeg và ffprobe thật')
def test_faststart_decodes_but_tail_moov_fails_closed(tmp_path):
    ff, probe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    for name, flags in [('fast', ['-movflags', '+faststart']), ('tail', [])]:
        path = tmp_path / (name + '.mp4')
        generated = subprocess.run([ff, '-v', 'error', '-nostdin', '-f', 'lavfi', '-i',
                                    'testsrc2=size=160x90:rate=12:duration=2', '-c:v', 'mpeg4',
                                    *flags, str(path)], capture_output=True, timeout=30)
        assert generated.returncode == 0, generated.stderr.decode('utf8', 'replace')
        raw, _ = read_snapshot(path)
        output, _ = run_bounded([probe, '-v', 'error', *input_options(), '-show_entries',
                                 'format=duration', '-of', 'json'], raw, timeout=30)
        assert json.loads(output)['format']['duration']
        args = [ff, '-v', 'error', '-nostdin', *input_options(), '-map', '0:v:0', '-f', 'null', '-']
        if name == 'fast':
            run_bounded(args, raw, timeout=30)
        else:
            with pytest.raises(EngineError):
                run_bounded(args, raw, timeout=30)


def test_rejects_hardlink_source_without_opening_alias(tmp_path):
    import os
    path = tmp_path / 'source.mp4'
    path.write_bytes(b'\x00\x00\x00\x18ftypisom' + b'\x00' * 20)
    alias = tmp_path / 'alias.mp4'
    try:
        os.link(path, alias)
    except OSError:
        pytest.skip('filesystem does not support hardlinks')
    with pytest.raises(ContractError):
        read_snapshot(alias)


def test_bad_suffix_does_not_echo_source_path(tmp_path):
    path = tmp_path / 'private-name.txt'
    path.write_text('private', encoding='utf8')
    with pytest.raises(ContractError) as error:
        read_snapshot(path)
    assert 'private-name' not in str(error.value)


def test_thread_start_exception_reaps_launched_child(monkeypatch):
    import subprocess
    import threading
    from video_studio.reference import _scan_media
    created = []
    real_popen = subprocess.Popen
    def track(*args, **kwargs):
        child = real_popen(*args, **kwargs)
        created.append(child)
        return child
    monkeypatch.setattr(_scan_media.subprocess, 'Popen', track)
    monkeypatch.setattr(threading.Thread, 'start', lambda self: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        run_bounded([sys.executable, '-c', 'import time;time.sleep(10)'], b'', timeout=5)
    assert created and created[0].poll() is not None
    assert all(stream.closed for stream in (created[0].stdin, created[0].stdout, created[0].stderr))


def test_huge_timeout_is_contract_error():
    with pytest.raises(ContractError):
        run_bounded([sys.executable, '-c', 'pass'], b'', timeout=10 ** 1000)


def test_limit_options_work_with_real_tools_on_faststart(tmp_path):
    import json
    import shutil
    import subprocess
    from video_studio.reference._scan_media import constrained_input_options
    ff, probe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ff or not probe:
        pytest.skip('cần ffmpeg và ffprobe thật')
    path = tmp_path / 'fast.mp4'
    result = subprocess.run([ff, '-v', 'error', '-nostdin', '-f', 'lavfi', '-i',
                             'testsrc2=size=160x90:rate=12:duration=1', '-c:v', 'mpeg4',
                             '-movflags', '+faststart', str(path)], capture_output=True, timeout=30)
    assert result.returncode == 0
    data, _ = read_snapshot(path)
    args = constrained_input_options()
    assert args.index('-max_alloc') < args.index('-i')
    assert args.index('-max_pixels') < args.index('-i')
    assert args.index('-max_samples') < args.index('-i')
    assert args.index('-max_streams') < args.index('-i')
    assert args.index('-max_probe_packets') < args.index('-i')
    output, _ = run_bounded([probe, '-v', 'error', *args, '-show_entries', 'format=duration', '-of', 'json'], data, timeout=30)
    assert json.loads(output)['format']['duration']
    run_bounded([ff, '-v', 'error', '-nostdin', *args, '-map', '0:v:0', '-f', 'null', '-'], data, timeout=30)


def test_oversized_dimensions_fail_closed_on_real_ffmpeg(tmp_path):
    import shutil
    import subprocess
    from video_studio.reference._scan_media import constrained_input_options
    ff = shutil.which('ffmpeg')
    if not ff:
        pytest.skip('cần ffmpeg thật')
    path = tmp_path / 'large.mp4'
    result = subprocess.run([ff, '-v', 'error', '-nostdin', '-f', 'lavfi', '-i',
                             'color=size=2048x1088:rate=1:duration=1', '-c:v', 'mpeg4',
                             '-movflags', '+faststart', str(path)], capture_output=True, timeout=30)
    assert result.returncode == 0
    data, _ = read_snapshot(path)
    with pytest.raises(EngineError):
        run_bounded([ff, '-v', 'error', '-nostdin', *constrained_input_options(),
                     '-map', '0:v:0', '-f', 'null', '-'], data, timeout=30)
    assert sorted(p.name for p in tmp_path.iterdir() if p.name != 'home') == ['large.mp4']


def test_probe_nonempty_error_stderr_is_not_accepted():
    from video_studio.reference._scan_media import parse_probe_output
    with pytest.raises(EngineError):
        parse_probe_output(b'{"format":{},"streams":[]}', b'picture size exceeds limit')


def test_probe_malformed_and_duplicate_json_is_not_accepted():
    from video_studio.reference._scan_media import parse_probe_output
    for data in (b'{broken', b'{"streams":[],"streams":[]}'):
        with pytest.raises(EngineError):
            parse_probe_output(data, b'')


def test_probe_wrapper_enforces_limits_and_rejects_error_stderr(monkeypatch):
    from video_studio.reference import _scan_media
    called = []
    monkeypatch.setattr(_scan_media._ff, 'probe_exe', lambda: 'ffprobe')
    monkeypatch.setattr(_scan_media, 'require_capabilities', lambda _: None)
    def fake_run(argv, payload, **kwargs):
        called.append(argv)
        return b'{"format":{},"streams":[]}', b'error level warning'
    monkeypatch.setattr(_scan_media, 'run_bounded', fake_run)
    with pytest.raises(EngineError):
        _scan_media.probe_payload(b'bytes')
    argv = called[0]
    for flag in ('-max_alloc','-max_pixels','-max_samples','-max_streams','-max_probe_packets','-protocol_whitelist'):
        assert argv.index(flag) < argv.index('-i')
    assert argv[argv.index('-protocol_whitelist') + 1] == 'pipe'


def test_decode_wrapper_uses_xerror_and_no_stdin(monkeypatch):
    from video_studio.reference import _scan_media
    called = []
    monkeypatch.setattr(_scan_media._ff, 'exe', lambda: 'ffmpeg')
    monkeypatch.setattr(_scan_media, 'require_capabilities', lambda _: None)
    monkeypatch.setattr(_scan_media, 'run_bounded', lambda argv, payload, **kwargs: called.append(argv) or (b'frame=1\nprogress=end\n',b''))
    _scan_media.verify_video_decode(b'bytes')
    assert '-xerror' in called[0] and '-nostdin' in called[0]


def test_fixed_wrappers_on_real_faststart_and_tail_moov(tmp_path):
    import shutil
    import subprocess
    from video_studio.reference._scan_media import probe_payload, verify_video_decode
    ff, probe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ff or not probe:
        pytest.skip('cần ffmpeg và ffprobe thật')
    for name, flags in [('fast', ['-movflags', '+faststart']), ('tail', [])]:
        path = tmp_path / (name + '.mp4')
        result = subprocess.run([ff, '-v', 'error', '-nostdin', '-f', 'lavfi', '-i',
                                 'testsrc2=size=160x90:rate=12:duration=2', '-c:v', 'mpeg4',
                                 *flags, str(path)], capture_output=True, timeout=30)
        assert result.returncode == 0
        data, _ = read_snapshot(path)
        if name == 'fast':
            metadata = probe_payload(data)
            assert metadata['width'] == 160 and metadata['height'] == 90
            assert verify_video_decode(data) == 24
        else:
            with pytest.raises(EngineError):
                probe_payload(data)


def test_missing_tool_capabilities_are_reported_as_missing(monkeypatch):
    from video_studio.contract import StationMissing
    from video_studio.reference import _scan_media
    monkeypatch.setattr(_scan_media, 'run_bounded', lambda *a, **k: (b'-max_alloc', b''))
    with pytest.raises(StationMissing):
        _scan_media.require_capabilities('ffmpeg')


def test_capability_probe_rejects_superstring_only(monkeypatch):
    from video_studio.contract import StationMissing
    from video_studio.reference import _scan_media
    output = b'\n'.join(b'-' + name for name in [b'max_allocation', b'max_pixels', b'max_samples', b'max_streams', b'max_probe_packets'])
    monkeypatch.setattr(_scan_media, 'run_bounded', lambda *a, **k: (output,b''))
    with pytest.raises(StationMissing):
        _scan_media.require_capabilities('ffmpeg')


@pytest.mark.parametrize(('stdout','stderr'), [
    (b'frame=1\nprogress=end\n', b'error message'),
    (b'frame=1\n', b''),
    (b'frame=18001\nprogress=end\n', b''),
    (b'frame=999999999999999999999\nprogress=end\n', b''),
    (b'frame=0\nprogress=end\n', b''),
])
def test_decode_rejects_error_stderr_incomplete_or_over_budget(monkeypatch, stdout, stderr):
    from video_studio.reference import _scan_media
    monkeypatch.setattr(_scan_media._ff, 'exe', lambda: 'ffmpeg')
    monkeypatch.setattr(_scan_media, 'require_capabilities', lambda _: None)
    monkeypatch.setattr(_scan_media, 'run_bounded', lambda *a, **k: (stdout,stderr))
    with pytest.raises(EngineError):
        _scan_media.verify_video_decode(b'bytes')


def test_decode_does_not_accept_valid_old_frame_with_bad_final_frame(monkeypatch):
    from video_studio.reference import _scan_media
    monkeypatch.setattr(_scan_media._ff, 'exe', lambda: 'ffmpeg')
    monkeypatch.setattr(_scan_media, 'require_capabilities', lambda _: None)
    monkeypatch.setattr(_scan_media, 'run_bounded', lambda *a, **k: (b'frame=2\nprogress=continue\nframe=invalid\nprogress=end\n', b''))
    with pytest.raises(EngineError):
        _scan_media.verify_video_decode(b'bytes')
