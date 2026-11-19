import hashlib
import json

import pytest

from video_studio import render, runtime_libs


@pytest.fixture
def setup_render(tmp_path, monkeypatch):
    lock = runtime_libs.load_lock()
    lock['libs']['gsap']['members'][0]['file_sha256'] = hashlib.sha256(b'fixture').hexdigest()
    original = lock['libs']['gsap']
    lock['libs']['multi'] = {**original, 'members': [
        {**original['members'][0], 'dest': 'one.js'},
        {**original['members'][0], 'dest': 'two.js'},
    ]}
    monkeypatch.setattr(runtime_libs, 'load_lock', lambda *a, **k: lock)
    monkeypatch.setattr(runtime_libs, 'station_path', lambda name, dest, station=None: str(tmp_path / 'station' / dest))
    captured = []
    original_set = runtime_libs.set_overrides
    def record_overrides(mapping):
        original_set(mapping)
        if mapping:
            captured.append(dict(mapping))
    monkeypatch.setattr(runtime_libs, 'set_overrides', record_overrides)
    monkeypatch.setattr(render, '_template', lambda project: lambda data, out: captured.append(data.get('_gsap_bytes')) or [])
    source = tmp_path / 'spec.json'
    source.write_text(json.dumps({'schema_version': 1, 'brand': {'a': 'A', 'b': 'B', 'site': 'example.invalid'}, 'outputs': {'long': True, 'short': False}}), encoding='utf-8')
    asset = tmp_path / 'gsap.js'
    asset.write_bytes(b'fixture')
    def run(*flags, project='effect-preview'):
        return render.main(['--project', project, '--input', str(source), '--out', str(tmp_path / 'out'), *flags])
    return run, asset, captured


def test_lib_file_alias_equals_gsap_file(setup_render):
    run, asset, captured = setup_render
    assert run('--gsap-file', str(asset)) == 0
    assert captured[-2:] == [{'gsap': str(asset)}, b'fixture']
    assert run('--lib-file', f'gsap={asset}') == 0
    assert captured[-2:] == [{'gsap': str(asset)}, b'fixture']


def test_unknown_lib_name_exit_2(setup_render, capsys):
    run, asset, _ = setup_render
    assert run('--lib-file', f'unknown={asset}') == 2
    assert 'gsap' in capsys.readouterr().err


def test_effect_preview_uses_station_lib_without_flag(setup_render, tmp_path):
    run, _, captured = setup_render
    station = tmp_path / 'station'
    station.mkdir()
    (station / 'gsap.min.js').write_bytes(b'fixture')
    assert run() == 0
    assert captured[-1] == b'fixture'


def test_effect_preview_missing_lib_exit_3(setup_render, capsys):
    run, _, _ = setup_render
    assert run() == 3
    assert 'libs fetch gsap' in capsys.readouterr().err


def test_multi_members_and_invalid_flags(setup_render):
    run, asset, captured = setup_render
    assert run('--lib-file', f'multi:one.js={asset}', '--lib-file', f'multi:two.js={asset}', project='news') == 0
    assert captured[-2] == {'multi:one.js': str(asset), 'multi:two.js': str(asset)}
    for flag in ('multi=x', 'multi:bad.js=x', 'gsap=', 'missing-equals'):
        assert run('--lib-file', flag, project='news') == 2
    assert run('--gsap-file', str(asset), '--lib-file', f'gsap={asset}') == 2


def test_preview_constant_matches_lock():
    assert render.PREVIEW_GSAP_SHA256 == runtime_libs.members('gsap')[0]['file_sha256']


def test_override_hash_mismatch_and_state_reset(setup_render, capsys):
    run, asset, _ = setup_render
    asset.write_bytes(b'tampered')
    assert run('--lib-file', f'gsap={asset}') == 2
    assert 'SHA-256' in capsys.readouterr().err
    assert runtime_libs.get_overrides() == {}


def test_preview_verified_reader_uses_pinned_hash(tmp_path, monkeypatch):
    payload = b'fixture'
    path = tmp_path / 'gsap.js'
    path.write_bytes(payload)
    monkeypatch.setattr(render, 'PREVIEW_GSAP_SHA256', hashlib.sha256(payload).hexdigest())
    assert render._read_preview_gsap(str(path)) == payload
    path.write_bytes(b'tampered')
    with pytest.raises(render.ContractError, match='SHA-256'):
        render._read_preview_gsap(str(path))


def test_multi_member_flags_reach_verified_loader(setup_render, tmp_path, monkeypatch):
    run, first, _ = setup_render
    second = tmp_path / 'second.js'
    second.write_bytes(b'fixture')
    loaded = {}
    def template(data, out):
        loaded.update(runtime_libs.load(['multi'], overrides=runtime_libs.get_overrides()))
        return []
    monkeypatch.setattr(render, '_template', lambda project: template)
    assert run('--lib-file', f'multi:one.js={first}',
               '--lib-file', f'multi:two.js={second}', project='news') == 0
    assert loaded == {'one.js': b'fixture', 'two.js': b'fixture'}
    assert runtime_libs.get_overrides() == {}


def test_override_interface_types():
    from typing import get_type_hints
    assert get_type_hints(runtime_libs.set_overrides) == {'mapping': dict[str, str], 'return': type(None)}
    assert get_type_hints(runtime_libs.get_overrides) == {'return': dict[str, str]}


def test_project_dir_wrong_detected_lib_stops_before_engine(tmp_path, monkeypatch):
    lock = runtime_libs.load_lock()
    lock['libs']['gsap']['members'][0]['file_sha256'] = hashlib.sha256(b'valid').hexdigest()
    monkeypatch.setattr(runtime_libs, 'load_lock', lambda *a, **k: lock)
    calls = []
    monkeypatch.setattr(render.subprocess, 'run', lambda *a, **k: calls.append(a))
    project = tmp_path / 'project'
    project.mkdir()
    (project / 'index.html').write_text('<script src="gsap.min.js"></script>', encoding='utf-8')
    source = project / 'gsap.min.js'
    source.write_bytes(b'wrong')
    assert render.main(['--project-dir', str(project), '--out', str(tmp_path / 'out')]) == 2
    assert calls == []
    assert source.read_bytes() == b'wrong'


def test_project_dir_strict_error_reports_both_output_streams(tmp_path, monkeypatch, capsys):
    import subprocess
    project = tmp_path / 'project'
    project.mkdir()
    (project / 'index.html').write_text('<html></html>', encoding='utf-8')
    calls = []
    def run(*args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args[0], 1, stdout=b'Lint: missing timeline registry', stderr=b'GPU probe')
    monkeypatch.setattr(render.subprocess, 'run', run)
    monkeypatch.setattr(render, 'hyperframes_argv', lambda *args, **kwargs: ['stub', *args])
    assert render.main(['--project-dir', str(project), '--out', str(tmp_path / 'out')]) == 2
    output = capsys.readouterr().err
    assert 'Lint: missing timeline registry' in output
    assert 'GPU probe' in output
    assert len(calls) == 1
