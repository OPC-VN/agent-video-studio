"""Locate the canonical effect resources in a checkout or an installed package."""
import os
from contextlib import ExitStack
from pathlib import Path

from video_studio.contract import ContractError


_CATALOG = Path("skills/video-theme-library/assets/effect-library/entries.json")
_MOTION = Path("skills/video-theme-library/assets/prompt-motion/index.json")
_INDEX_LIMIT = 16 * 1024 * 1024


def _windows_root(package, checkout, bundled):
    from . import _native_windows as native

    with native.open_root_chain_read(str(checkout)) as (checkout_handle, stack):
        parent = native._reader_open(checkout_handle, package.name, True)
        stack.callback(native.close, parent)
        try:
            root = native._reader_open(parent, "_bundled", True)
        except native.ReaderOpenError as exc:
            if exc.ntstatus != 0xC0000034:
                raise
            selected = checkout
            root = checkout_handle
        else:
            selected = bundled
            stack.callback(native.close, root)
        for relative in (_CATALOG, _MOTION):
            with ExitStack() as files:
                native._reader_relative(root, files, relative.as_posix(), _INDEX_LIMIT, None)
    return selected


def _posix_root(package, checkout, bundled):
    from . import _posix_fs as native

    with native.open_root_chain(str(checkout)) as (checkout_chain, stack):
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        checkout_fd = checkout_chain[-1][2]
        parent = os.open(package.name, flags, dir_fd=checkout_fd)
        stack.callback(os.close, parent)
        package_chain = [*checkout_chain, (checkout_fd, package.name, parent)]
        native._check_chain(package_chain)
        try:
            root = os.open("_bundled", flags, dir_fd=parent)
        except FileNotFoundError:
            selected = checkout
            selected_chain = checkout_chain
        else:
            selected = bundled
            stack.callback(os.close, root)
            selected_chain = [*package_chain, (parent, "_bundled", root)]
        for relative in (_CATALOG, _MOTION):
            with ExitStack() as files:
                native._read(selected_chain, files, relative.as_posix(), _INDEX_LIMIT, None)
        native._check_chain(package_chain)
        native._check_chain(selected_chain)
    return selected


def resource_root():
    """Use an installed bundle when present; otherwise use a complete checkout."""
    # abspath preserves links for the native chain reader to reject.
    package = Path(os.path.abspath(__file__)).parents[1]
    checkout = package.parent
    bundled = package / "_bundled"
    try:
        if os.name == "nt":
            return _windows_root(package, checkout, bundled)
        return _posix_root(package, checkout, bundled)
    except (OSError, ValueError, TypeError, ContractError) as exc:
        raise ContractError("Effect library resources are missing or incomplete or unsafe") from exc
