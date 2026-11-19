import os

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import _native_windows


@pytest.mark.skipif(os.name != 'nt', reason='Windows writer capability')
def test_unproven_windows_writer_refuses_before_creating_destination(tmp_path):
    dest = tmp_path / 'new-project'
    with pytest.raises(ContractError, match='Secure Windows writer unavailable'):
        _native_windows.write_tree([], [('index.html', b'example')], dest)
    assert not dest.exists()


@pytest.mark.skipif(os.name != 'nt', reason='Windows writer capability')
def test_unproven_windows_writer_preserves_existing_destination(tmp_path):
    dest = tmp_path / 'existing'
    dest.mkdir()
    marker = dest / 'marker'
    marker.write_bytes(b'unchanged')
    with pytest.raises(ContractError, match='Secure Windows writer unavailable'):
        _native_windows.write_tree([], [('index.html', b'example')], dest)
    assert marker.read_bytes() == b'unchanged'


@pytest.mark.skipif(os.name != 'nt', reason='Windows native capability')
def test_directory_create_supports_no_reparse_and_no_recall(tmp_path):
    import ctypes
    from ctypes import wintypes

    native = _native_windows
    parent = native.open_root(str(tmp_path))
    try:
        name = ctypes.create_unicode_buffer('probe')
        encoded_length = len('probe'.encode('utf-16-le'))
        text = native._UnicodeString(encoded_length, encoded_length, ctypes.cast(name, wintypes.LPWSTR))
        attrs = native._Attributes(ctypes.sizeof(native._Attributes), parent, ctypes.pointer(text), 0x1040, None, None)
        io = native._IoStatus()
        handle = wintypes.HANDLE()
        status = native._nt.NtCreateFile(ctypes.byref(handle), 0x00110083, ctypes.byref(attrs), ctypes.byref(io),
                                         None, 0x80, 3, 2, 0x00600021, None, 0)
        if status & 0xffffffff == 0xc000000d:
            pytest.skip('Directory FILE_CREATE with FILE_OPEN_NO_RECALL is unsupported')
        native._check(status)
        try:
            native._reader_info(handle, True)
        finally:
            native.close(handle)
    finally:
        native.close(parent)
