import hashlib
import os

import pytest

from video_studio.effect_library import _native_windows as native
from video_studio.contract import ContractError

pytestmark = pytest.mark.skipif(os.name != 'nt', reason='Windows native reader')


def test_snapshot_hash_and_bounds(tmp_path):
    (tmp_path / 'a.txt').write_bytes(b'abc')
    digest = hashlib.sha256(b'abc').hexdigest()
    assert native.read_repo_file(tmp_path, 'a.txt', limit=3, expected_sha256=digest) == b'abc'
    assert native.read_repo_files(tmp_path, [{'path': 'a.txt', 'sha256': digest}], max_total=3) == {'a.txt': b'abc'}
    with pytest.raises((OSError, ValueError)):
        native.read_repo_file(tmp_path, 'a.txt', limit=2)
    with pytest.raises((OSError, ValueError)):
        native.read_repo_file(tmp_path, 'a.txt', limit=3, expected_sha256='0' * 64)


def test_reject_hardlink_and_bad_paths(tmp_path):
    (tmp_path / 'a').write_bytes(b'a')
    os.link(tmp_path / 'a', tmp_path / 'b')
    with pytest.raises((OSError, ValueError)):
        native.read_repo_file(tmp_path, 'a', limit=10)
    with pytest.raises(ContractError):
        native.read_repo_file(tmp_path, '../a', limit=10)


def test_directory_open_no_recall_no_write_and_failure_is_closed(monkeypatch):
    calls = []
    def fail(*args):
        calls.append((args[1], args[8]))
        return -1073741811
    monkeypatch.setattr(native._nt, 'NtCreateFile', fail)
    with pytest.raises(OSError, match='0xc000000d'):
        native._reader_open(None, '\\??\\C:\\', True)
    access, options = calls[0]
    assert access & 0x20
    assert not access & 0x02
    assert options & 0x00400000
    assert options & 0x00200000


def test_directory_open_type_neutral_flags_and_api_failure(monkeypatch):
    calls = []
    def fail(*args):
        calls.append((args[1], args[8]))
        return -1073741811
    monkeypatch.setattr(native._nt, 'NtCreateFile', fail)
    with pytest.raises(OSError):
        native._reader_open(None, '\\??\\C:\\', True)
    access, options = calls[0]
    assert access & 0x20 and not access & 0x02
    assert options == 0x00600020


def test_file_cannot_be_used_as_directory(tmp_path):
    (tmp_path / 'file').write_bytes(b'data')
    with pytest.raises(OSError):
        with native.open_root_chain_read(tmp_path / 'file'):
            pass


def test_directory_symlink_rejected(tmp_path):
    target = tmp_path / 'target'
    target.mkdir()
    link = tmp_path / 'link'
    try:
        os.symlink(target, link, target_is_directory=True)
    except OSError as error:
        pytest.skip(f'directory symlink unavailable: {error.winerror}')
    with pytest.raises(OSError):
        with native.open_root_chain_read(link):
            pass


def test_remote_drive_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr(native, '_reader_local_drive', lambda drive: False)
    with pytest.raises(OSError, match='local'):
        with native.open_root_chain_read(tmp_path):
            pass


def test_directory_junction_rejected(tmp_path):
    import subprocess
    target = tmp_path / 'target'
    target.mkdir()
    link = tmp_path / 'junction'
    env = os.environ.copy()
    env.update(AVS_TEST_LINK=str(link), AVS_TEST_TARGET=str(target))
    result = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command',
                             'New-Item -ItemType Junction -Path $env:AVS_TEST_LINK -Target $env:AVS_TEST_TARGET | Out-Null'],
                            capture_output=True, timeout=10, env=env)
    if result.returncode:
        pytest.skip('junction creation unavailable')
    with pytest.raises(OSError):
        with native.open_root_chain_read(link):
            pass


def test_attribute_tag_api_failure_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr(native._kernel, 'GetFileInformationByHandleEx', lambda *args: 0)
    with pytest.raises(OSError):
        with native.open_root_chain_read(tmp_path):
            pass


def test_information_prototype_stable_across_calls(tmp_path):
    with native.open_root_chain_read(tmp_path) as (root, _):
        native._reader_info(root, True)
        first = native._kernel.GetFileInformationByHandle.argtypes[1]
        native._reader_info(root, True)
        assert native._kernel.GetFileInformationByHandle.argtypes[1] is first


def test_concurrent_reads(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    (tmp_path / 'a').write_bytes(b'abc')
    with ThreadPoolExecutor(max_workers=8) as pool:
        result = list(pool.map(lambda _: native.read_repo_file(tmp_path, 'a', limit=3), range(64)))
    assert result == [b'abc'] * 64


@pytest.mark.parametrize('status,length,device,characteristics', [
    (-1073741811, 8, 7, 0), (0, 4, 7, 0), (0, 8, 20, 0), (0, 8, 7, 0x10),
])
def test_volume_query_rejects_invalid_results(monkeypatch, tmp_path, status, length, device, characteristics):
    import ctypes
    def query(handle, io, buffer, size, cls):
        native_io = ctypes.cast(io, ctypes.POINTER(native._IoStatus)).contents
        native_io.information = length
        words = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint32))
        words[0], words[1] = device, characteristics
        return status
    monkeypatch.setattr(native._nt, 'NtQueryVolumeInformationFile', query)
    with pytest.raises(OSError):
        with native.open_root_chain_read(tmp_path):
            pass


def test_short_read_without_hash_is_rejected(monkeypatch, tmp_path):
    (tmp_path / 'a').write_bytes(b'abc')
    def early_eof(handle, buffer, length, count, overlapped):
        import ctypes
        ctypes.cast(count, ctypes.POINTER(native.wintypes.DWORD)).contents.value = 0
        return 1
    monkeypatch.setattr(native._kernel, 'ReadFile', early_eof)
    with pytest.raises(OSError, match='size'):
        native.read_repo_file(tmp_path, 'a', limit=3)


def test_reader_open_error_exposes_ntstatus_without_text_parsing(monkeypatch):
    monkeypatch.setattr(native._nt, 'NtCreateFile', lambda *args: -1073741772)
    with pytest.raises(native.ReaderOpenError) as caught:
        native._reader_open(None, '\\??\\C:\\', True)
    assert caught.value.ntstatus == 0xC0000034


def test_bundle_pins_all_files_before_first_read(monkeypatch, tmp_path):
    (tmp_path / 'a').write_bytes(b'a')
    (tmp_path / 'b').write_bytes(b'b')
    assets = [{'path': x, 'sha256': hashlib.sha256(x.encode()).hexdigest()} for x in ('a', 'b')]
    original = native._kernel.ReadFile
    attempted = []
    def read(handle, buffer, size, count, overlapped):
        if not attempted:
            try:
                with open(tmp_path / 'b', 'wb') as stream:
                    stream.write(b'x')
                attempted.append('write succeeded')
            except PermissionError:
                attempted.append('write denied')
        return original(handle, buffer, size, count, overlapped)
    monkeypatch.setattr(native._kernel, 'ReadFile', read)
    assert native.read_repo_files(tmp_path, assets) == {'a': b'a', 'b': b'b'}
    assert attempted == ['write denied']


def test_bundle_close_failure_reports_phase_and_closes_all(monkeypatch, tmp_path):
    for name in ('a', 'b'):
        (tmp_path / name).write_bytes(name.encode())
    assets = [{'path': x, 'sha256': hashlib.sha256(x.encode()).hexdigest()} for x in ('a', 'b')]
    original_open, original_close = native._reader_open, native.close
    opened, closed, named = [], [], {}
    def record_open(root, name, directory):
        handle = original_open(root, name, directory)
        opened.append(handle.value)
        named[handle.value] = name
        return handle
    def fail_close(handle):
        value = handle.value
        closed.append(value)
        original_close(handle)
        if named[value] == 'b':
            raise OSError('injected close error')
    monkeypatch.setattr(native, '_reader_open', record_open)
    monkeypatch.setattr(native, 'close', fail_close)
    with pytest.raises(ContractError, match='repo bundle.*close.*b'):
        native.read_repo_files(tmp_path, assets)
    assert sorted(opened) == sorted(closed)


def test_bundle_handle_count_and_depth_bounded(tmp_path):
    digest = '0' * 64
    with pytest.raises(ContractError, match='repo bundle'):
        native.read_repo_files(tmp_path, [{'path': str(i), 'sha256': digest} for i in range(65)])
    with pytest.raises(ContractError, match='repo bundle'):
        native.read_repo_files(tmp_path, [{'path': '/'.join(['x'] * 9), 'sha256': digest}])


def test_bundle_reports_failing_asset_and_phase(tmp_path):
    (tmp_path / 'a').write_bytes(b'a')
    (tmp_path / 'b').write_bytes(b'b')
    assets = [{'path': 'a', 'sha256': hashlib.sha256(b'a').hexdigest()},
              {'path': 'b', 'sha256': '0' * 64}]
    with pytest.raises(ContractError, match='repo bundle read failed for b'):
        native.read_repo_files(tmp_path, assets)
    assets[1]['path'] = 'missing'
    with pytest.raises(ContractError, match='repo bundle open failed for missing'):
        native.read_repo_files(tmp_path, assets)
