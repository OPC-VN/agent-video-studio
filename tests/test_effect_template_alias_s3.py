import pytest

from video_studio.contract import ContractError
from video_studio.effect_library.catalog import CHECKS, validate_entry
from video_studio.effect_library.template import check_project_paths, plan_tree, validate_template_entry


def template_entry(paths):
    root = 'templates/effect-library/ve-demo/project'
    return {
        'id': 'VE-demo', 'name': 'Demo', 'kind': 'template', 'maturity': 'candidate',
        'rights': 'owned', 'source': 'local', 'runtime': 'hyperframes',
        'tags': [], 'roles': [], 'techniques': [], 'ratios': [],
        'checks': dict.fromkeys(CHECKS, 'not_run'),
        'template_root': root, 'contract_path': 'templates/effect-library/ve-demo/contract.md',
        'contract_sha256': 'a' * 64,
        'assets': [{'path': root + '/' + path, 'sha256': 'b' * 64, 'rights': 'owned'}
                   for path in paths],
    }


@pytest.mark.parametrize('left,right', [
    ('assets/Logo/a.css', 'assets/logo/b.css'),
    ('assets/é/a.css', 'assets/e\u0301/b.css'),
    ('assets/parent/Logo/a.css', 'assets/parent/logo/b.css'),
])
def test_directory_alias_rejected_at_every_validation_boundary(left, right):
    paths = ['index.html', left, right]
    entry = template_entry(paths)
    with pytest.raises(ContractError):
        check_project_paths(iter(paths))
    with pytest.raises(ContractError):
        validate_template_entry(entry)
    with pytest.raises(ContractError):
        validate_entry(entry)
    with pytest.raises(ContractError):
        plan_tree(dict.fromkeys(paths, b'data'))


def test_distinct_sibling_directories_and_bytes_are_preserved():
    files = {'index.html': b'\x00html', 'assets/Logo/a.css': b'\xff',
             'assets/logos/b.css': b'css'}
    check_project_paths(iter(files))
    assert validate_entry(template_entry(files))
    dirs, ordered = plan_tree(files)
    assert dirs == ['assets', 'assets/Logo', 'assets/logos']
    assert dict(ordered) == files
