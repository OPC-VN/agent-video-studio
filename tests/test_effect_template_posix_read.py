import hashlib
import os
import subprocess
import sys
from contextlib import ExitStack, contextmanager

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import _posix_fs as reader


native = pytest.mark.skipif(os.name != 'posix', reason='requires native POSIX filesystem')


def test_unsupported_platform_fails_closed(monkeypatch):
    monkeypatch.setattr(reader.os, 'supports_dir_fd', set())
    with pytest.raises(ContractError, match='unavailable'):
        reader.read_repo_file('.', 'file', limit=1)


def test_each_asset_closes_before_next_read(monkeypatch):
    closed = []
    @contextmanager
    def root(_):
        with ExitStack() as stack:
            yield [], stack
    def read(_chain, stack, path, _limit, _digest):
        if path == 'b':
            assert closed == ['a']
        stack.callback(closed.append, path)
        return b'x'
    monkeypatch.setattr(reader, 'open_root_chain', root)
    monkeypatch.setattr(reader, '_read', read)
    assets = [{'path': p, 'sha256': '0' * 64} for p in ('a', 'b')]
    assert reader.read_repo_files('.', assets) == {'a': b'x', 'b': b'x'}
    assert closed == ['a', 'b']


def test_bundle_close_failure_is_reported(monkeypatch):
    @contextmanager
    def root(_):
        with ExitStack() as stack:
            yield [], stack
    def fail_close():
        raise OSError('close failed')
    def read(_chain, stack, _path, _limit, _digest):
        stack.callback(fail_close)
        return b'x'
    monkeypatch.setattr(reader, 'open_root_chain', root)
    monkeypatch.setattr(reader, '_read', read)
    with pytest.raises(ContractError):
        reader.read_repo_files('.', [{'path': 'a', 'sha256': '0' * 64}])


@native
def test_exact_snapshot_hash_and_total_limit(tmp_path):
    (tmp_path / 'a').write_bytes(b'abc')
    (tmp_path / 'b').write_bytes(b'de')
    assets = [{'path': name, 'sha256': hashlib.sha256(data).hexdigest()}
              for name, data in [('a', b'abc'), ('b', b'de')]]
    result = reader.read_repo_files(tmp_path, assets, max_total=5)
    (tmp_path / 'a').write_bytes(b'new')
    assert result == {'a': b'abc', 'b': b'de'}
    (tmp_path / 'a').write_bytes(b'abc')
    with pytest.raises(ContractError):
        reader.read_repo_files(tmp_path, assets, max_total=4)
    with pytest.raises(ContractError):
        reader.read_repo_file(tmp_path, 'b', limit=2, expected_sha256='0' * 64)


@native
@pytest.mark.parametrize('relative', ['', '../file', '/file', 'a//b', 'a/./b', 'a\\b'])
def test_rejects_unsafe_relative_path(tmp_path, relative):
    with pytest.raises(ContractError):
        reader.read_repo_file(tmp_path, relative, limit=10)


@native
def test_rejects_root_and_ancestor_links(tmp_path):
    root = tmp_path / 'root'
    root.mkdir()
    (root / 'file').write_bytes(b'payload')
    (root / 'child').mkdir()
    (root / 'child' / 'file').write_bytes(b'payload')
    assert reader.read_repo_file(root / 'child', 'file', limit=100) == b'payload'
    (tmp_path / 'link').symlink_to(root, target_is_directory=True)
    for target, relative in [(tmp_path / 'link', 'file'),
                             (tmp_path / 'link' / 'child', 'file')]:
        with pytest.raises(ContractError):
            reader.read_repo_file(target, relative, limit=100)


@native
def test_rejects_subdir_and_leaf_links(tmp_path):
    (tmp_path / 'file').write_bytes(b'payload')
    (tmp_path / 'leaf').symlink_to('file')
    (tmp_path / 'subdir').mkdir()
    (tmp_path / 'subdir' / 'file').write_bytes(b'payload')
    (tmp_path / 'alias').symlink_to('subdir', target_is_directory=True)
    for relative in ('leaf', 'alias/file'):
        with pytest.raises(ContractError):
            reader.read_repo_file(tmp_path, relative, limit=100)


@native
def test_rejects_hard_link(tmp_path):
    (tmp_path / 'file').write_bytes(b'payload')
    os.link(tmp_path / 'file', tmp_path / 'hard')
    with pytest.raises(ContractError):
        reader.read_repo_file(tmp_path, 'file', limit=100)


@native
@pytest.mark.parametrize('target', ['parent', 'file'])
def test_rejects_source_swapped_during_read(tmp_path, monkeypatch, target):
    parent = tmp_path / 'parent'
    parent.mkdir()
    (parent / 'file').write_bytes(b'original')
    original_read = reader.os.read
    swapped = []
    def swap(fd, size):
        data = original_read(fd, size)
        if not swapped:
            swapped.append(True)
            if target == 'parent':
                parent.rename(tmp_path / 'old')
                parent.mkdir()
                (parent / 'file').write_bytes(b'replacement')
            else:
                (parent / 'file').rename(parent / 'old')
                (parent / 'file').write_bytes(b'replacement')
        return data
    monkeypatch.setattr(reader.os, 'read', swap)
    with pytest.raises(ContractError):
        reader.read_repo_file(tmp_path, 'parent/file', limit=32)


@native
def test_fifo_open_does_not_block(tmp_path):
    os.mkfifo(tmp_path / 'fifo')
    code = ("from video_studio.effect_library._posix_fs import read_repo_file; "
            "read_repo_file(__import__('sys').argv[1], 'fifo', limit=2)")
    result = subprocess.run([sys.executable, '-c', code, str(tmp_path)],
                            capture_output=True, timeout=5, check=False)
    assert result.returncode != 0
    assert b'ContractError' in result.stderr


@native
def test_detects_growth_and_closes_on_failure(tmp_path, monkeypatch):
    path = tmp_path / 'file'
    path.write_bytes(b'abc')
    original = reader.os.read
    calls = []
    def grow(fd, size):
        data = original(fd, size)
        if not calls:
            calls.append(True)
            with path.open('ab') as stream:
                stream.write(b'def')
        return data
    monkeypatch.setattr(reader.os, 'read', grow)
    with pytest.raises(ContractError):
        reader.read_repo_file(tmp_path, 'file', limit=3)


@native
def test_close_failure_is_not_silenced(tmp_path, monkeypatch):
    (tmp_path / 'file').write_bytes(b'a')
    original = reader.os.close
    calls = []
    def close(fd):
        original(fd)
        if not calls:
            calls.append(True)
            raise OSError('close failed')
    monkeypatch.setattr(reader.os, 'close', close)
    with pytest.raises(ContractError):
        reader.read_repo_file(tmp_path, 'file', limit=1)
