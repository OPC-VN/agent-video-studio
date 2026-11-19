import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import template


def test_plan_deterministic_parent_first():
    files = {'assets/z/sub.js': b'2', 'index.html': b'a', 'assets/z/a.css': b'123'}
    dirs, ordered = template.plan_tree(files)
    assert dirs == ['assets', 'assets/z']
    assert ordered == sorted(files.items())


@pytest.mark.parametrize('files', [
    {}, {'index.html': 'not bytes'}, {'index.html': b'', 'assets/a.js': bytearray()},
    {'index.html': b'', 'assets/A/x.js': b'', 'assets/a/y.js': b''},
    {'index.html': b'', 'assets/\u00e9/x.js': b'', 'assets/e\u0301/y.js': b''},
    {'index.html': b'', 'assets/a.js': b'', 'assets/A.js': b''},
    {'assets/a.js': b''}, {'index.html': b'', '../x.js': b''},
    {'index.html': b'', 'assets/a.bin': b''},
])
def test_plan_rejects_bad_inputs(files):
    with pytest.raises(ContractError):
        template.plan_tree(files)


def test_plan_limit():
    with pytest.raises(ContractError):
        template.plan_tree({'index.html': b'x' * (64 * 1024 * 1024), 'assets/a.js': b'x'})
    with pytest.raises(ContractError):
        template.plan_tree({'index.html': b'', **{f'assets/{i}.js': b'' for i in range(64)}})


@pytest.mark.parametrize('device', ['CONIN$', 'CONOUT$', 'COM\u00b9', 'LPT\u00b2'])
@pytest.mark.parametrize('as_directory', [False, True])
def test_plan_rejects_windows_device_components(device, as_directory):
    path = f'assets/{device}/a.js' if as_directory else f'assets/{device}.js'
    with pytest.raises(ContractError):
        template.plan_tree({'index.html': b'', path: b''})


def test_dispatch_and_counts(monkeypatch, tmp_path):
    from video_studio.effect_library import _native_windows
    calls = []
    monkeypatch.setattr(template, '_IS_NT', True)
    monkeypatch.setattr(_native_windows, 'write_tree', lambda *args: calls.append(args), raising=False)
    files = {'index.html': b'abc', 'assets/a.js': b'd'}
    assert template.write_project(files, tmp_path / 'new') == {'files': 2, 'bytes': 4}
    assert calls == [(['assets'], sorted(files.items()), tmp_path / 'new')]


def test_posix_fails_before_touch(monkeypatch, tmp_path):
    from video_studio.effect_library import _posix_fs
    monkeypatch.setattr(template, '_IS_NT', False)
    def forbidden(*args, **kwargs):
        pytest.fail('writer touched filesystem')
    monkeypatch.setattr(_posix_fs.os, 'mkdir', forbidden)
    dest = tmp_path / 'new'
    with pytest.raises(ContractError, match='atomic'):
        template.write_project({'index.html': b'', 'assets/a.js': b''}, dest)
    assert not dest.exists()


def test_uncertain_retains_only_relative_names():
    exc = template.DestinationStateUncertain(('assets/a.js',))
    assert exc.remaining == ('assets/a.js',)
