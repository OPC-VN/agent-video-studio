"""Descriptor-anchored, bounded read-only access to repository resources."""
import hashlib
import os
import re
import stat
from contextlib import ExitStack, contextmanager
from pathlib import PurePosixPath

from video_studio.contract import ContractError


def _capable():
    required = ('O_NOFOLLOW', 'O_DIRECTORY', 'O_NONBLOCK')
    if (os.name != 'posix' or any(not hasattr(os, name) for name in required)
            or os.open not in os.supports_dir_fd or os.stat not in os.supports_dir_fd
            or os.stat not in os.supports_follow_symlinks):
        raise ContractError('Secure POSIX filesystem access is unavailable')


def _identity(info):
    if not isinstance(info.st_ino, int) or info.st_ino <= 0 or not isinstance(info.st_dev, int) or info.st_dev < 0:
        raise ContractError('Filesystem identity is unavailable')
    return info.st_dev, info.st_ino


def _parts(relative):
    if (not isinstance(relative, str) or not relative or '\\' in relative
            or relative.startswith('/') or any(p in ('', '.', '..') for p in relative.split('/'))):
        raise ContractError('Unsafe relative path')
    from .catalog import _relative
    _relative(relative)
    return relative.split('/')


def _check_chain(chain):
    for parent, name, fd in chain:
        held = os.fstat(fd)
        if not stat.S_ISDIR(held.st_mode):
            raise ContractError('Directory changed during read')
        if parent is not None:
            current = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if not stat.S_ISDIR(current.st_mode) or _identity(current) != _identity(held):
                raise ContractError('Directory changed during read')
        _identity(held)


@contextmanager
def open_root_chain(path):
    """Open each absolute path component from / without following links."""
    _capable()
    raw = os.fspath(path)
    if not isinstance(raw, str) or '\x00' in raw or '..' in raw.split('/'):
        raise ContractError('Unsafe repository root')
    absolute = os.path.abspath(raw)
    parts = PurePosixPath(absolute).parts
    if not parts or parts[0] != '/':
        raise ContractError('Unsafe repository root')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    with ExitStack() as stack:
        root = os.open('/', flags)
        stack.callback(os.close, root)
        chain = [(None, '/', root)]
        for part in parts[1:]:
            parent = chain[-1][2]
            fd = os.open(part, flags, dir_fd=parent)
            stack.callback(os.close, fd)
            chain.append((parent, part, fd))
        _check_chain(chain)
        yield chain, stack
        _check_chain(chain)


def _read(chain, stack, relative, limit, expected_sha256):
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise ContractError('Invalid read limit')
    parts = _parts(relative)
    dirs = list(chain)
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    for part in parts[:-1]:
        parent = dirs[-1][2]
        fd = os.open(part, flags, dir_fd=parent)
        stack.callback(os.close, fd)
        dirs.append((parent, part, fd))
    parent = dirs[-1][2]
    fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    stack.callback(os.close, fd)
    before = os.fstat(fd)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ContractError('Source is not a single-link regular file')
    identity = _identity(before)
    chunks = []
    remaining = limit + 1
    while remaining:
        chunk = os.read(fd, min(remaining, 1024 * 1024))
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    raw = b''.join(chunks)
    if len(raw) > limit:
        raise ContractError('Source exceeds read limit')
    after = os.fstat(fd)
    current = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
    if (not stat.S_ISREG(after.st_mode) or after.st_nlink != 1
            or not stat.S_ISREG(current.st_mode) or current.st_nlink != 1
            or _identity(after) != identity or _identity(current) != identity
            or (before.st_size, before.st_mtime_ns, before.st_ctime_ns) !=
               (after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
        raise ContractError('Source changed during read')
    _check_chain(dirs)
    if expected_sha256 is not None and hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ContractError('Source hash mismatch')
    return raw


def read_repo_file(repo_root, relative: str, *, limit: int, expected_sha256: str | None = None) -> bytes:
    if expected_sha256 is not None and (not isinstance(expected_sha256, str) or not re.fullmatch(r'[0-9a-f]{64}', expected_sha256)):
        raise ContractError(f'Invalid digest for repository file {relative!r}')
    try:
        with open_root_chain(repo_root) as (chain, stack):
            return _read(chain, stack, relative, limit, expected_sha256)
    except ContractError as exc:
        raise ContractError(f'Cannot safely read repository file {relative!r}: {exc}') from exc
    except (OSError, ValueError, TypeError) as exc:
        raise ContractError(f'Cannot safely read repository file {relative!r}') from exc


def read_repo_files(repo_root, assets: list[dict], *, max_total: int = 67108864) -> dict[str, bytes]:
    if not isinstance(max_total, int) or isinstance(max_total, bool) or max_total < 0:
        raise ContractError('Invalid bundle limit')
    result = {}
    total = 0
    try:
        with open_root_chain(repo_root) as (chain, _root_stack):
            for asset in assets:
                path = asset['path']
                digest = asset['sha256']
                if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
                    raise ContractError(f'Invalid digest for repository file {path!r}')
                if path in result:
                    raise ContractError('Duplicate bundle path')
                try:
                    with ExitStack() as file_stack:
                        raw = _read(chain, file_stack, path, max_total - total, digest)
                except (ContractError, OSError) as exc:
                    raise ContractError(f'Cannot safely read repository file {path!r}: {exc}') from exc
                result[path] = raw
                total += len(raw)
        return result
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise ContractError('Cannot safely read repository bundle') from exc


def verify_repo_bundle(repo_root, record: dict) -> None:
    from .catalog import validate_entry
    validate_entry(record)
    if not record.get('assets'):
        raise ContractError('Repository bundle requires assets')
    read_repo_files(repo_root, record['assets'])


def write_tree(dirs: list[str], files: list[tuple[str, bytes]], dest) -> None:
    """Refuse before creating anything: atomic root ownership is unproven."""
    raise ContractError('Secure POSIX writer unavailable: atomic root ownership is not proven')
