import hashlib
import importlib
import json
import os

import pytest

from video_studio.contract import ContractError

search_module = importlib.import_module('video_studio.effect_library.search')


def record():
    return {'id': 'VE-test', 'name': 'Test', 'kind': 'component', 'maturity': 'candidate',
            'rights': 'owned', 'source': 'synthetic', 'runtime': 'browser', 'tags': [],
            'roles': [], 'techniques': [], 'ratios': [],
            'assets': [{'path': p, 'sha256': hashlib.sha256(b'data').hexdigest(), 'rights': 'owned'}
                       for p in ('a.js', 'b.css')],
            'checks': dict.fromkeys(('static_check', 'preview', 'render', 'audio', 'ratio_test', 'reuse_evidence'), 'not_run')}


def test_dispatch_posix_reader(tmp_path, monkeypatch):
    root = tmp_path / 'resources'
    root.mkdir()
    catalog = tmp_path / 'catalog.json'
    catalog.write_text(json.dumps([record()]), encoding='utf-8')
    class Reader:
        def read_repo_file(self, base, relative, *, limit):
            assert base == catalog.parent and relative == catalog.name
            return catalog.read_bytes()
        def read_repo_files(self, base, assets, *, max_total):
            assert base == root
            return {asset['path']: b'data' for asset in assets}
    monkeypatch.setattr(search_module, '_IS_NT', False, raising=False)
    from video_studio.effect_library import _posix_fs
    monkeypatch.setattr(_posix_fs, 'read_repo_file', Reader().read_repo_file)
    monkeypatch.setattr(_posix_fs, 'read_repo_files', Reader().read_repo_files)
    monkeypatch.setattr(search_module, 'resource_root', lambda: root)
    assert search_module.search(repo_entries=catalog)[0]['id'] == 'VE-test'


@pytest.mark.skipif(os.name == 'nt', reason='requires native POSIX reader')
def test_real_posix_bundle_search(tmp_path, monkeypatch):
    root = tmp_path / 'resources'
    root.mkdir()
    for p in ('a.js', 'b.css'):
        (root / p).write_bytes(b'data')
    catalog = tmp_path / 'catalog.json'
    catalog.write_text(json.dumps([record()]), encoding='utf-8')
    monkeypatch.setattr(search_module, 'resource_root', lambda: root)
    assert search_module.search(repo_entries=catalog)[0]['id'] == 'VE-test'
    (root / 'b.css').write_bytes(b'bad')
    with pytest.raises(ContractError, match='VE-test.*b.css'):
        search_module.search(repo_entries=catalog)


def test_duplicate_id_not_selected_fails(tmp_path):
    a = record()
    a.update(kind='reference', rights='unknown', asset=None)
    a.pop('assets')
    b = dict(a)
    catalog = tmp_path / 'catalog.json'
    catalog.write_text(json.dumps([a, b]), encoding='utf-8')
    with pytest.raises(ContractError, match='Duplicate'):
        search_module.search('unmatched', repo_entries=catalog)


def test_override_catalog_does_not_redirect_assets(tmp_path, monkeypatch):
    root = tmp_path / 'resources'
    root.mkdir()
    external = tmp_path / 'external'
    external.mkdir()
    for p in ('a.js', 'b.css'):
        (external / p).write_bytes(b'data')
    catalog = external / 'catalog.json'
    catalog.write_text(json.dumps([record()]), encoding='utf-8')
    monkeypatch.setattr(search_module, 'resource_root', lambda: root)
    with pytest.raises(ContractError, match='VE-test.*a.js'):
        search_module.search(repo_entries=catalog)


def test_real_reader_checks_bundle_and_single_asset(tmp_path, monkeypatch):
    root = tmp_path / 'resources'
    root.mkdir()
    for p in ('a.js', 'b.css'):
        (root / p).write_bytes(b'data')
    single = record()
    single['id'] = 'VE-single'
    single['asset'] = single.pop('assets')[0]
    catalog = tmp_path / 'catalog.json'
    catalog.write_text(json.dumps([record(), single]), encoding='utf-8')
    monkeypatch.setattr(search_module, 'resource_root', lambda: root)
    assert {e['id'] for e in search_module.search(repo_entries=catalog)} == {'VE-test', 'VE-single'}
    (root / 'b.css').write_bytes(b'bad')
    with pytest.raises(ContractError, match='VE-test.*b.css'):
        search_module.search(repo_entries=catalog)


@pytest.mark.parametrize('depth', [8, 9])
def test_single_asset_preserves_legacy_path_depth(tmp_path, monkeypatch, depth):
    root = tmp_path / 'resources'
    root.mkdir()
    relative = '/'.join(['dir'] * (depth - 1) + ['effect.js'])
    asset = root.joinpath(*relative.split('/'))
    asset.parent.mkdir(parents=True)
    asset.write_bytes(b'data')
    single = record()
    single['asset'] = {'path': relative, 'sha256': hashlib.sha256(b'data').hexdigest()}
    single.pop('assets')
    catalog = tmp_path / 'catalog.json'
    catalog.write_text(json.dumps([single]), encoding='utf-8')
    monkeypatch.setattr(search_module, 'resource_root', lambda: root)
    assert search_module.search(repo_entries=catalog)[0]['id'] == 'VE-test'


@pytest.mark.parametrize('relative', ['../outside.js', '/absolute.js', 'dir/../outside.js', 'dir\\file.js'])
def test_single_asset_rejects_unsafe_paths(tmp_path, relative):
    single = record()
    single['asset'] = {'path': relative, 'sha256': hashlib.sha256(b'data').hexdigest()}
    single.pop('assets')
    catalog = tmp_path / 'catalog.json'
    catalog.write_text(json.dumps([single]), encoding='utf-8')
    with pytest.raises(ContractError):
        search_module.search(repo_entries=catalog)
