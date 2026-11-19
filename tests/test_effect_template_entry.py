from copy import deepcopy

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library.catalog import CHECKS, validate_entry


def entry():
    root = 'templates/effect-library/ve-demo/project'
    return {
        'id': 'VE-demo', 'name': 'Demo', 'kind': 'template', 'maturity': 'candidate',
        'rights': 'owned', 'source': 'local', 'runtime': 'hyperframes',
        'tags': [], 'roles': [], 'techniques': [], 'ratios': [],
        'checks': dict.fromkeys(CHECKS, 'not_run'),
        'template_root': root, 'contract_path': 'templates/effect-library/ve-demo/contract.md',
        'contract_sha256': 'a' * 64,
        'assets': [{'path': root + '/' + p, 'sha256': 'b' * 64, 'rights': 'owned'}
                   for p in ('index.html', 'assets/style.css', 'map.json')],
    }


def test_valid_template_and_unchanged_non_template():
    value = entry()
    assert validate_entry(value) is value
    ordinary = deepcopy(value)
    ordinary['kind'] = 'component'
    for key in ('template_root', 'contract_path', 'contract_sha256'):
        del ordinary[key]
    assert validate_entry(ordinary) is ordinary


def test_template_single_asset_cannot_bypass():
    value = entry()
    value['asset'] = value.pop('assets')[0]
    with pytest.raises(ContractError):
        validate_entry(value)


@pytest.mark.parametrize('field', ['template_root', 'contract_path', 'contract_sha256'])
def test_template_bundle_validation_runs_before_return(field):
    value = entry()
    del value[field]
    with pytest.raises(ContractError):
        validate_entry(value)


@pytest.mark.parametrize('bad', ['', 'A' * 64, 'g' * 64, 'a' * 63, None])
def test_template_requires_contract_digest(bad):
    value = entry()
    value['contract_sha256'] = bad
    with pytest.raises(ContractError):
        validate_entry(value)


def test_template_root_component_containment():
    value = entry()
    value['assets'][0]['path'] = value['template_root'] + '-evil/index.html'
    with pytest.raises(ContractError):
        validate_entry(value)


@pytest.mark.parametrize('relative', ['.npmrc', 'package.json', 'scripts/a.js', 'file.glb',
    'file.gltf', 'file.geojson', 'file.wasm', 'file.pmtiles', 'file.pbf', 'file.hdr', 'file.bin',
    'assets/../x.js', 'assets//x.js', 'assets/CON.js', 'assets/x.js.', 'assets/x:foo.js'])
def test_unsafe_project_paths_rejected(relative):
    value = entry()
    value['assets'][1]['path'] = value['template_root'] + '/' + relative
    with pytest.raises(ContractError):
        validate_entry(value)


@pytest.mark.parametrize('left,right', [('assets/a.js', 'assets/A.js'),
    ('assets/é.js', 'assets/e\u0301.js'), ('assets/a.js', 'assets/a.js/b.js')])
def test_project_path_conflicts(left, right):
    value = entry()
    for asset, path in zip(value['assets'][1:], (left, right)):
        asset['path'] = value['template_root'] + '/' + path
    with pytest.raises(ContractError):
        validate_entry(value)


def test_contract_must_be_outside_project_and_not_an_asset():
    value = entry()
    value['contract_path'] = value['assets'][1]['path']
    with pytest.raises(ContractError):
        validate_entry(value)


def test_index_required_at_exact_root():
    value = entry()
    value['assets'][0]['path'] = value['template_root'] + '/Index.html'
    with pytest.raises(ContractError):
        validate_entry(value)


def test_maturity_render_gate():
    value = entry()
    value['maturity'] = 'implemented'
    with pytest.raises(ContractError):
        validate_entry(value)
    value['checks']['render'] = 'pass'
    value['evidence'] = {'render': 'render evidence'}
    assert validate_entry(value) is value


def test_project_path_checker_accepts_one_pass_iterable():
    from video_studio.effect_library.template import check_project_paths
    check_project_paths(iter(['index.html', 'assets/style.css']))


@pytest.mark.parametrize('field,bad', [
    ('template_root', 'templates//project'), ('template_root', 'C:/project'),
    ('contract_path', '../contract.md'), ('contract_path', 'templates/CON.md'),
    ('template_root', None), ('contract_path', ''),
])
def test_bad_template_metadata_paths(field, bad):
    value = entry()
    value[field] = bad
    with pytest.raises(ContractError):
        validate_entry(value)


def test_template_rights_require_owned_or_licensed_on_all_assets():
    value = entry()
    value['rights'] = 'unknown'
    with pytest.raises(ContractError):
        validate_entry(value)
    value['rights'] = 'owned'
    value['assets'][1]['rights'] = 'unknown'
    with pytest.raises(ContractError):
        validate_entry(value)


def test_template_licensed_asset_requires_license_terms():
    value = entry()
    value['assets'][1]['rights'] = 'licensed'
    with pytest.raises(ContractError):
        validate_entry(value)
