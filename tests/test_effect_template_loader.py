import copy
import hashlib
import json
from unittest.mock import Mock

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import template
from video_studio.effect_library.catalog import CHECKS


def entry():
    return {
        'id': 'VE-demo', 'name': 'Demo', 'kind': 'template', 'maturity': 'candidate',
        'rights': 'owned', 'source': 'local', 'runtime': 'html',
        'tags': [], 'roles': [], 'techniques': [], 'ratios': [],
        'checks': dict.fromkeys(CHECKS, 'not_run'),
        'template_root': 'templates/demo', 'contract_path': 'contracts/demo.md',
        'contract_sha256': hashlib.sha256(b'contract snapshot').hexdigest(),
        'assets': [
            {'path': 'templates/demo/index.html', 'sha256': hashlib.sha256(b'html').hexdigest(), 'rights': 'owned'},
            {'path': 'templates/demo/assets/style.css', 'sha256': hashlib.sha256(b'css').hexdigest(), 'rights': 'owned'},
        ],
    }


@pytest.fixture
def boundary(monkeypatch):
    from video_studio.effect_library import _native_windows, _posix_fs
    native = _native_windows if template._IS_NT else _posix_fs
    record = entry()
    reads = Mock(side_effect=[json.dumps([record]).encode(), b'contract snapshot'])
    bundle = Mock(return_value={'templates/demo/index.html': b'html', 'templates/demo/assets/style.css': b'css'})
    parser = Mock()
    monkeypatch.setattr(native, 'read_repo_file', reads)
    monkeypatch.setattr(native, 'read_repo_files', bundle)
    monkeypatch.setattr(template, 'check_contract', parser)
    return record, reads, bundle, parser


def test_snapshot_passes_verified_contract_and_project_paths(boundary):
    record, reads, bundle, parser = boundary
    selected, files = template.load_template('VE-demo', repo_root='explicit')
    assert selected == record
    assert files == {'index.html': b'html', 'assets/style.css': b'css'}
    assert reads.call_args_list[0].args == ('explicit', 'skills/video-theme-library/assets/effect-library/entries.json')
    assert reads.call_args_list[0].kwargs == {'limit': 16 * 1024 * 1024}
    assert reads.call_args_list[1].args == ('explicit', record['contract_path'])
    assert reads.call_args_list[1].kwargs == {'limit': 1024 * 1024, 'expected_sha256': record['contract_sha256']}
    bundle.assert_called_once_with('explicit', record['assets'], max_total=64 * 1024 * 1024)
    parser.assert_called_once_with(b'contract snapshot', record, ['index.html', 'assets/style.css'])


def test_default_root_only_when_none(boundary, monkeypatch):
    from video_studio.effect_library import resources
    root = Mock(return_value='selected-root')
    monkeypatch.setattr(resources, 'resource_root', root)
    template.load_template('VE-demo')
    root.assert_called_once_with()
    assert boundary[1].call_args_list[0].args[0] == 'selected-root'


def test_explicit_root_does_not_call_selector(boundary, monkeypatch):
    from video_studio.effect_library import resources
    selector = Mock(side_effect=AssertionError('unexpected selection'))
    monkeypatch.setattr(resources, 'resource_root', selector)
    template.load_template('VE-demo', 'explicit')
    selector.assert_not_called()


@pytest.mark.parametrize('raw', [b'[{"id":"a","id":"b"}]', b'[NaN]', b'[Infinity]', b'[-Infinity]', b'[1e999]', b'{}', b'\xff'])
def test_rejects_invalid_catalog_before_source_reads(boundary, raw):
    _, reads, bundle, parser = boundary
    reads.side_effect = [raw]
    with pytest.raises(ContractError):
        template.load_template('VE-demo', 'root')
    assert reads.call_count == 1
    bundle.assert_not_called()
    parser.assert_not_called()


def test_duplicate_id_anywhere_before_selection(boundary):
    record, reads, bundle, _ = boundary
    other = copy.deepcopy(record)
    reads.side_effect = [json.dumps([record, other]).encode()]
    with pytest.raises(ContractError, match='[Dd]uplicate'):
        template.load_template('VE-demo', 'root')
    bundle.assert_not_called()


def test_invalid_unselected_record_rejected(boundary):
    record, reads, bundle, _ = boundary
    reads.side_effect = [json.dumps([record, {'id': 'VE-bad'}]).encode()]
    with pytest.raises(ContractError):
        template.load_template('VE-demo', 'root')
    bundle.assert_not_called()


def test_missing_id_is_rejected_before_asset_reads(boundary):
    _, reads, bundle, parser = boundary
    with pytest.raises(ContractError, match='not found'):
        template.load_template('VE-missing', 'root')
    assert reads.call_count == 1
    bundle.assert_not_called()
    parser.assert_not_called()


def test_contract_parser_error_propagates(boundary):
    _, _, _, parser = boundary
    parser.side_effect = ContractError('invalid contract')
    with pytest.raises(ContractError, match='invalid contract'):
        template.load_template('VE-demo', 'root')


@pytest.mark.parametrize('stage', ['catalog', 'contract', 'assets'])
def test_source_errors_abort_before_parser(boundary, stage):
    record, reads, bundle, parser = boundary
    if stage == 'catalog':
        reads.side_effect = OSError('catalog unavailable')
    elif stage == 'contract':
        reads.side_effect = [json.dumps([record]).encode(), OSError('contract mismatch')]
    else:
        bundle.side_effect = OSError('asset mismatch')
    with pytest.raises(ContractError):
        template.load_template('VE-demo', 'root')
    parser.assert_not_called()
