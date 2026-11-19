import hashlib
import json
import socket
import subprocess
import urllib.request
from pathlib import Path

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import __main__ as cli, template
from video_studio.effect_library.catalog import CHECKS
from video_studio.render import _scan_project


@pytest.fixture
def fixture_repo(tmp_path, monkeypatch):
    from video_studio.effect_library import _native_windows, _posix_fs, resources
    root = tmp_path / 'repo'
    data = {'index.html': b'<html></html>', 'assets/style.css': b'body{}',
            'assets/app.js': b'void 0;', 'data.json': b'{}'}
    table = '| chỗ thay | file | số lần xuất hiện | kiểu nội dung | giới hạn |\n| --- | --- | --- | --- | --- |\n| tiêu đề | index.html | 1 | chữ | ngắn |'
    contract = '\n\n'.join(f'## {i}. {h}\n' + (table if i == 3 else 'Nội dung.')
                            for i, h in enumerate(template.CONTRACT_HEADINGS, 1)).encode()
    digest = lambda raw: hashlib.sha256(raw).hexdigest()
    record = {'id': 'VE-demo', 'name': 'Demo', 'kind': 'template', 'maturity': 'candidate',
              'rights': 'owned', 'source': 'local', 'runtime': 'html', 'tags': [], 'roles': [],
              'techniques': [], 'ratios': [], 'checks': dict.fromkeys(CHECKS, 'not_run'),
              'template_root': 'templates/demo', 'contract_path': 'contracts/demo.md',
              'contract_sha256': digest(contract), 'assets': [
                  {'path': 'templates/demo/' + name, 'sha256': digest(raw), 'rights': 'owned'}
                  for name, raw in data.items()]}
    def put(path, raw):
        path = root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    put('skills/video-theme-library/assets/effect-library/entries.json', json.dumps([record]).encode())
    put(record['contract_path'], contract)
    for name, raw in data.items():
        put('templates/demo/' + name, raw)
    monkeypatch.setattr(resources, 'resource_root', lambda: root)
    # Reader and writer are test doubles: native success and security properties are not asserted here.
    native = _native_windows if template._IS_NT else _posix_fs
    def read_file(base, path, *, limit, expected_sha256=None):
        raw = (Path(base) / path).read_bytes()
        if len(raw) > limit or (expected_sha256 and digest(raw) != expected_sha256):
            raise ContractError('invalid source')
        return raw
    def read_files(base, assets, *, max_total):
        return {a['path']: read_file(base, a['path'], limit=max_total, expected_sha256=a['sha256']) for a in assets}
    def write_tree(dirs, files, dest):
        dest = Path(dest)
        dest.mkdir()
        for directory in dirs:
            (dest / directory).mkdir()
        for name, raw in files:
            (dest / name).write_bytes(raw)
    monkeypatch.setattr(native, 'read_repo_file', read_file)
    monkeypatch.setattr(native, 'read_repo_files', read_files)
    monkeypatch.setattr(native, 'write_tree', write_tree)
    return root, data


def test_cli_success_json_exact_counts(fixture_repo, tmp_path, capsys):
    _, data = fixture_repo
    dest = tmp_path / 'out'
    assert cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(dest)]) == 0
    assert json.loads(capsys.readouterr().out) == {'ok': True, 'id': 'VE-demo', 'into': str(dest),
                                                   'files': 4, 'bytes': sum(map(len, data.values()))}
    assert {rel for _, rel in _scan_project(dest)} == set(data)


def test_cli_twice_destination_unchanged(fixture_repo, tmp_path, capsys):
    dest = tmp_path / 'out'
    args = ['materialize-template', '--id', 'VE-demo', '--into', str(dest)]
    assert cli.main(args) == 0
    before = (dest / 'index.html').read_bytes()
    assert cli.main(args) == 2
    assert (dest / 'index.html').read_bytes() == before
    assert len(capsys.readouterr().out.splitlines()) == 1


def test_invalid_source_no_dest(fixture_repo, tmp_path, capsys):
    root, _ = fixture_repo
    (root / 'templates/demo/index.html').write_bytes(b'bad')
    dest = tmp_path / 'out'
    assert cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(dest)]) == 2
    assert not dest.exists()
    assert not capsys.readouterr().out


@pytest.mark.parametrize('option', ['--station', '--repo-root'])
def test_forbidden_public_options(fixture_repo, tmp_path, option):
    with pytest.raises(SystemExit) as exc:
        cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(tmp_path / 'out'), option, 'x'])
    assert exc.value.code == 2


def test_partial_cleanup_status3(monkeypatch, tmp_path, capsys):
    def uncertain(*args, **kwargs):
        raise template.DestinationStateUncertain(('assets/x.js',))
    monkeypatch.setattr(cli, 'materialize_template', uncertain, raising=False)
    assert cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(tmp_path / 'out')]) == 3
    out = capsys.readouterr()
    assert not out.out
    assert 'inspect' in out.err.lower()
    assert 'assets/x.js' in out.err


def test_uncertain_empty_remaining(monkeypatch, tmp_path, capsys):
    def uncertain(*args, **kwargs):
        raise template.DestinationStateUncertain(())
    monkeypatch.setattr(cli, 'materialize_template', uncertain)
    assert cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(tmp_path / 'out')]) == 3
    out = capsys.readouterr()
    assert not out.out
    assert 'inspect' in out.err.lower()


def test_report_failure_keeps_destination_status3(fixture_repo, tmp_path, monkeypatch):
    dest = tmp_path / 'out'
    class BrokenOutput:
        def write(self, value):
            raise OSError('broken stdout')

        def fileno(self):
            raise OSError('no descriptor')

    monkeypatch.setattr(cli.sys, 'stdout', BrokenOutput())
    assert cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(dest)]) == 3
    assert (dest / 'index.html').is_file()


def test_published_close_failure_status3(monkeypatch, tmp_path, capsys):
    def close_failure(*args):
        raise cli.PublishedButCloseFailed('close failed')
    monkeypatch.setattr(cli, 'materialize_template', close_failure)
    assert cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(tmp_path / 'out')]) == 3
    assert not capsys.readouterr().out


def test_no_process_no_network(fixture_repo, tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('unexpected process or network')
    monkeypatch.setattr(subprocess, 'Popen', forbidden)
    monkeypatch.setattr(socket, 'socket', forbidden)
    monkeypatch.setattr(urllib.request, 'urlopen', forbidden)
    assert cli.main(['materialize-template', '--id', 'VE-demo', '--into', str(tmp_path / 'out')]) == 0
