"""Resource selection verifies anchored checkout and bundle trees."""
import os
from pathlib import Path

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import resources


def make_root(root):
    for relative in (resources._CATALOG, resources._MOTION):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{}', encoding='utf-8')


def setup_module_path(monkeypatch, root):
    module = root / 'video_studio' / 'effect_library' / 'resources.py'
    module.parent.mkdir(parents=True)
    module.touch()
    monkeypatch.setattr(resources, '__file__', str(module))
    return module.parents[1] / '_bundled'


def test_checkout_selection_never_uses_unanchored_probes(monkeypatch, tmp_path):
    setup_module_path(monkeypatch, tmp_path)
    make_root(tmp_path)
    def forbidden(*args, **kwargs):
        pytest.fail('unanchored filesystem probe')
    monkeypatch.setattr(os.path, 'lexists', forbidden)
    monkeypatch.setattr(Path, 'is_file', forbidden)
    if os.name == 'nt':
        from video_studio.effect_library import _native_windows as native
        monkeypatch.setattr(native, 'open_root', forbidden)
        monkeypatch.setattr(native, 'open_directory', forbidden)
        monkeypatch.setattr(native, 'open_file', forbidden)
    assert resources.resource_root() == tmp_path


def test_incomplete_bundle_does_not_fall_back(monkeypatch, tmp_path):
    bundle = setup_module_path(monkeypatch, tmp_path)
    make_root(tmp_path)
    bundle.mkdir()
    with pytest.raises(ContractError):
        resources.resource_root()


def test_bundle_catalog_link_is_rejected(monkeypatch, tmp_path):
    bundle = setup_module_path(monkeypatch, tmp_path)
    make_root(tmp_path)
    make_root(bundle)
    index = bundle / resources._CATALOG
    index.unlink()
    try:
        index.symlink_to(tmp_path / resources._CATALOG)
    except OSError:
        pytest.skip('file symlinks unavailable')
    with pytest.raises(ContractError):
        resources.resource_root()


def test_bundle_hardlinked_index_is_rejected(monkeypatch, tmp_path):
    bundle = setup_module_path(monkeypatch, tmp_path)
    make_root(tmp_path)
    make_root(bundle)
    index = bundle / resources._CATALOG
    index.unlink()
    os.link(tmp_path / resources._CATALOG, index)
    with pytest.raises(ContractError):
        resources.resource_root()


@pytest.mark.skipif(os.name != 'nt', reason='Windows NT status')
def test_windows_only_missing_component_status_allows_fallback(monkeypatch, tmp_path):
    setup_module_path(monkeypatch, tmp_path)
    make_root(tmp_path)
    from video_studio.effect_library import _native_windows as native
    real_open = native._reader_open
    def denied(parent, name, directory):
        if name == '_bundled':
            raise native.ReaderOpenError(0xC0000022)
        return real_open(parent, name, directory)
    monkeypatch.setattr(native, '_reader_open', denied)
    with pytest.raises(ContractError):
        resources.resource_root()


def test_fallback_keeps_checkout_anchored_when_path_changes(monkeypatch, tmp_path):
    """A second pathname open could select a replacement checkout."""
    from contextlib import contextmanager
    setup_module_path(monkeypatch, tmp_path)
    make_root(tmp_path)
    if os.name == 'nt':
        from video_studio.effect_library import _native_windows as native
        original = native.open_root_chain_read
        attribute = 'open_root_chain_read'
    else:
        from video_studio.effect_library import _posix_fs as native
        original = native.open_root_chain
        attribute = 'open_root_chain'
    opened = []
    @contextmanager
    def once(path):
        opened.append(Path(path))
        if len(opened) > 1:
            raise OSError('checkout path was replaced before reopening')
        with original(path) as pinned:
            yield pinned
    monkeypatch.setattr(native, attribute, once)
    assert resources.resource_root() == tmp_path
    assert opened == [tmp_path]


def test_checkout_swap_during_absent_bundle_fails_closed(monkeypatch, tmp_path):
    checkout = tmp_path / 'checkout'
    checkout.mkdir()
    setup_module_path(monkeypatch, checkout)
    make_root(checkout)
    moved = tmp_path / 'original'
    attempted = []
    if os.name == 'nt':
        from video_studio.effect_library import _native_windows as native
        original_open = native._reader_open
        def race(parent, name, directory):
            try:
                return original_open(parent, name, directory)
            except native.ReaderOpenError as exc:
                if name == '_bundled' and exc.ntstatus == 0xC0000034:
                    attempted.append(True)
                    with pytest.raises(OSError):
                        checkout.rename(moved)
                raise
        monkeypatch.setattr(native, '_reader_open', race)
        assert resources.resource_root() == checkout
    else:
        original_open = os.open
        def race(path, flags, *args, **kwargs):
            try:
                return original_open(path, flags, *args, **kwargs)
            except FileNotFoundError:
                if path == '_bundled':
                    attempted.append(True)
                    checkout.rename(moved)
                    checkout.mkdir()
                    (checkout / 'video_studio' / '_bundled').mkdir(parents=True)
                raise
        monkeypatch.setattr(os, 'open', race)
        monkeypatch.setattr(os, 'supports_dir_fd', os.supports_dir_fd | {race})
        with pytest.raises(ContractError):
            resources.resource_root()
    assert attempted == [True]


def test_missing_posix_capability_is_reported_before_flags(monkeypatch, tmp_path):
    from video_studio.effect_library import _posix_fs as native
    def unavailable():
        raise ContractError('Secure POSIX filesystem access is unavailable')
    monkeypatch.setattr(native, '_capable', unavailable)
    monkeypatch.delattr(os, 'O_NOFOLLOW', raising=False)
    with pytest.raises(ContractError):
        resources._posix_root(tmp_path / 'video_studio', tmp_path,
                              tmp_path / 'video_studio' / '_bundled')
