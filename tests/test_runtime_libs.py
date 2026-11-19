import copy
import hashlib
import json
import os

import pytest

from video_studio import runtime_libs as libs, render
from video_studio.contract import ContractError, StationMissing


def fixture_lock():
    lock = libs.load_lock()
    lib = copy.deepcopy(lock['libs']['gsap'])
    lib['members'] = [dict(lib['members'][0], dest='one.js', file_sha256=hashlib.sha256(b'one').hexdigest()), dict(lib['members'][0], member='package/two.js', dest='two.js', file_sha256=hashlib.sha256(b'two').hexdigest())]
    lock['libs']['three'] = lib
    lock['libs']['plugin'] = dict(copy.deepcopy(lock['libs']['gsap']), requires=['three'])
    return lock


def test_real_lock():
    assert libs.load_lock()['libs']['gsap']['members'][0]['file_sha256'] == render.PREVIEW_GSAP_SHA256


@pytest.mark.parametrize('change', ['member', 'absolute', 'dest', 'exe', 'url', 'host', 'integrity', 'package', 'cycle', 'collision', 'name', 'version', 'case'])
def test_invalid_lock(tmp_path, change):
    lock = fixture_lock(); m = lock['libs']['three']['members']; p = lock['packages']['gsap']
    actions = {'member': lambda: m[0].update(member='../x'), 'absolute': lambda: m[0].update(member='/x'), 'dest': lambda: m[0].update(dest='a/b.js'), 'exe': lambda: m[0].update(dest='x.exe'), 'url': lambda: p.update(tarball_url='http://registry.npmjs.org/x'), 'host': lambda: p.update(tarball_url='https://evil.example/x'), 'integrity': lambda: p.update(npm_integrity='sha512-bad'), 'package': lambda: lock['libs']['three'].update(package='missing'), 'cycle': lambda: lock['libs']['three'].update(requires=['plugin']), 'collision': lambda: m[1].update(dest='one.js'), 'name': lambda: lock['libs'].update({'../bad': lock['libs']['gsap']}), 'version': lambda: p.update(version='../bad'), 'case': lambda: m[1].update(dest='ONE.js')}
    actions[change](); path = tmp_path / 'lock.json'; path.write_text(json.dumps(lock))
    with pytest.raises(ContractError): libs.load_lock(path)


def test_resolve():
    assert libs.resolve(['plugin'], fixture_lock()) == ['three', 'plugin']
    with pytest.raises(ContractError): libs.resolve(['unknown'], fixture_lock())


def test_read_verified(tmp_path):
    p = tmp_path / 'f'; p.write_bytes(b'one'); sha = hashlib.sha256(b'one').hexdigest()
    assert libs.read_verified(p, sha, 3) == b'one'
    with pytest.raises(ContractError): libs.read_verified(p, '0' * 64, 3)
    with pytest.raises(ContractError): libs.read_verified(p, sha, 2)
    with pytest.raises(ContractError): libs.read_verified(tmp_path, sha, 3)


def test_symlink(tmp_path):
    p = tmp_path / 'f'; p.write_bytes(b'one'); link = tmp_path / 'link'
    try: link.symlink_to(p)
    except OSError: pytest.skip('symlink unavailable')
    with pytest.raises(ContractError): libs.read_verified(link, hashlib.sha256(b'one').hexdigest(), 3)


def test_status_and_load(tmp_path, monkeypatch):
    lock = fixture_lock(); monkeypatch.setattr(libs, 'load_lock', lambda path=None: lock)
    assert next(x for x in libs.status(tmp_path) if x['name'] == 'three')['state'] == 'missing'
    with pytest.raises(StationMissing): libs.load(['three'], station=tmp_path)
    d = tmp_path / 'runtime-libs' / 'gsap' / '3.15.0'; d.mkdir(parents=True)
    (d / 'one.js').write_bytes(b'one'); (d / 'two.js').write_bytes(b'bad')
    assert next(x for x in libs.status(tmp_path) if x['name'] == 'three')['state'] == 'mismatch'
    (d / 'two.js').write_bytes(b'two')
    assert libs.load(['three'], station=tmp_path) == {'one.js': b'one', 'two.js': b'two'}
    assert next(x for x in libs.status(tmp_path) if x['name'] == 'three')['state'] == 'ok'


def test_overrides_and_dependency(tmp_path, monkeypatch):
    lock = fixture_lock(); monkeypatch.setattr(libs, "load_lock", lambda path=None: lock)
    d = tmp_path / "runtime-libs" / "gsap" / "3.15.0"; d.mkdir(parents=True)
    (d / "one.js").write_bytes(b"one"); (d / "two.js").write_bytes(b"two")
    m = lock["libs"]["plugin"]["members"][0]
    m["file_sha256"] = hashlib.sha256(b"override").hexdigest()
    override = tmp_path / "override"; override.write_bytes(b"override")
    assert libs.load(["plugin"], station=tmp_path, overrides={"plugin": override}) == {"one.js": b"one", "two.js": b"two", "gsap.min.js": b"override"}
    (d / "two.js").unlink()
    assert next(x for x in libs.status(tmp_path) if x["name"] == "plugin")["state"] == "missing"


def test_posix_parent_component_cannot_be_followed(monkeypatch):
    import io
    import posixpath
    import types
    # Simulates POSIX openat: without O_NOFOLLOW on a parent, "link" resolves.
    calls = []
    def open_fake(path, flags, *, dir_fd=None):
        calls.append((path, flags, dir_fd))
        if path == 'link' and flags & 0x100:
            raise OSError('symlink refused')
        return 10 + len(calls)
    fake = types.SimpleNamespace(name='posix', path=posixpath, fsdecode=os.fsdecode, O_RDONLY=0, O_NOFOLLOW=0x100,
                                 O_DIRECTORY=0x200, O_NONBLOCK=0x400, open=open_fake,
                                 close=lambda fd: None, fstat=lambda fd: types.SimpleNamespace(st_mode=0o100644, st_size=3),
                                 fdopen=lambda fd, mode, closefd=False: io.BytesIO(b'one'))
    monkeypatch.setattr(libs, 'os', fake)
    sha = hashlib.sha256(b'one').hexdigest()
    with pytest.raises(ContractError):
        libs.read_verified('/safe/link/file.js', sha, 3)
    assert calls[-1][0] == 'link'
    assert calls[-1][1] & fake.O_NOFOLLOW


@pytest.mark.skipif(os.name == 'nt', reason='requires POSIX openat and symlinks')
def test_posix_parent_symlink_real(tmp_path):
    target = tmp_path / 'real'; target.mkdir(); (target / 'f').write_bytes(b'one')
    link = tmp_path / 'alias'; link.symlink_to(target, target_is_directory=True)
    sha = hashlib.sha256(b'one').hexdigest()
    assert libs.read_verified(target / 'f', sha, 3) == b'one'
    with pytest.raises(ContractError): libs.read_verified(link / 'f', sha, 3)


def test_public_signatures_have_annotations():
    import inspect
    for name in ('lock_path', 'load_lock', 'package_entry', 'lib_entry', 'resolve', 'members',
                 'station_dir', 'station_path', 'read_verified', 'status', 'load'):
        sig = inspect.signature(getattr(libs, name))
        assert sig.return_annotation is not inspect.Signature.empty, name
        assert all(p.annotation is not inspect.Parameter.empty for p in sig.parameters.values()), name


@pytest.mark.skipif(os.name != 'nt', reason='Windows native handle path')
def test_windows_norecall_refuses_parent_before_read(tmp_path, monkeypatch):
    from video_studio.effect_library import _native_windows as native
    called = []
    def refuse_parent(path):
        called.append(('root', path))
        raise OSError('reparse point rejected')
    monkeypatch.setattr(native, 'open_root', refuse_parent)
    monkeypatch.setattr(native, 'open_file', lambda *args: pytest.fail('must not open file'))
    monkeypatch.setattr(native, 'read_all', lambda *args: pytest.fail('must not read'))
    with pytest.raises(ContractError):
        libs.read_verified(tmp_path / 'junction' / 'file.js', '0' * 64, 100)
    assert called == [('root', str(tmp_path / 'junction'))]


def test_posix_safe_path_uses_openat_and_reads_verified_bytes(monkeypatch):
    import io
    import posixpath
    import types
    calls = []; closed = []
    def open_fake(path, flags, *, dir_fd=None):
        calls.append((path, flags, dir_fd))
        return 10 + len(calls)
    fake = types.SimpleNamespace(name='posix', path=posixpath, fsdecode=os.fsdecode,
                                 O_RDONLY=0, O_NOFOLLOW=0x100, O_DIRECTORY=0x200,
                                 O_NONBLOCK=0x400, open=open_fake, close=closed.append,
                                 fstat=lambda fd: types.SimpleNamespace(st_mode=0o100644, st_size=3),
                                 fdopen=lambda fd, mode, closefd=False: io.BytesIO(b'one'))
    monkeypatch.setattr(libs, 'os', fake)
    assert libs.read_verified('/safe/nested/file.js', hashlib.sha256(b'one').hexdigest(), 3) == b'one'
    assert [c[0] for c in calls] == ['/', 'safe', 'nested', 'file.js']
    assert all(c[1] & fake.O_NOFOLLOW for c in calls)
    assert [c[2] for c in calls] == [None, 11, 12, 13]
    assert set(closed) == {11, 12, 13, 14}
