import json
import subprocess
import sys

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library.catalog import CHECKS, validate_entry
from video_studio.effect_library.search import search


def bundle():
    return {
        'id': 'VE-rights', 'name': 'Rights', 'kind': 'component',
        'maturity': 'candidate', 'rights': 'owned', 'source': 'synthetic',
        'runtime': 'browser', 'tags': [], 'roles': [], 'techniques': [], 'ratios': [],
        'checks': dict.fromkeys(CHECKS, 'not_run'),
        'assets': [{'path': p, 'sha256': '0' * 64, 'rights': 'owned'}
                   for p in ('a.js', 'b.css')],
    }


@pytest.mark.parametrize('value', [[], {}, 1, None, True])
@pytest.mark.parametrize('location', ['entry', 'asset'])
def test_invalid_rights_raise_contract_error(value, location):
    entry = bundle()
    target = entry if location == 'entry' else entry['assets'][0]
    target['rights'] = value
    with pytest.raises(ContractError):
        validate_entry(entry)


@pytest.mark.parametrize('value', [[], {}, 1])
def test_search_and_cli_reject_invalid_bundle_rights(tmp_path, value):
    entry = bundle()
    entry['assets'][0]['rights'] = value
    catalog = tmp_path / 'entries.json'
    catalog.write_text(json.dumps([entry]), encoding='utf-8')
    with pytest.raises(ContractError):
        search(repo_entries=catalog)
    pm = tmp_path / 'pm.json'
    pm.write_text('{"entries": []}', encoding='utf-8')
    result = subprocess.run(
        [sys.executable, '-m', 'video_studio.effect_library', '--repo-entries', str(catalog),
         '--pm-index', str(pm), '--no-distilled'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 2
    assert 'rights' in result.stderr
    assert 'Traceback' not in result.stderr


@pytest.mark.parametrize('rights', ['owned', 'licensed'])
def test_valid_bundle_asset_rights(rights):
    entry = bundle()
    entry['assets'][0]['rights'] = rights
    if rights == 'licensed':
        entry['assets'][0]['license'] = {'id': 'test', 'source': 'test', 'terms': 'test'}
    assert validate_entry(entry) is entry
