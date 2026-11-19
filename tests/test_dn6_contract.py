import copy
import hashlib

import pytest

from video_studio import runtime_libs as libs, render
from video_studio.contract import ContractError


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    lock = libs.load_lock(); entry = lock['libs']['gsap']; entry['members'][0]['file_sha256'] = hashlib.sha256(b'gsap').hexdigest()
    multi = copy.deepcopy(entry); multi['requires']=['gsap']; multi['members'] = [dict(entry['members'][0], dest='three.module.js', file_sha256=hashlib.sha256(b'module').hexdigest()), dict(entry['members'][0], dest='three.core.js', file_sha256=hashlib.sha256(b'core').hexdigest())]
    lock['libs']['three']=multi; monkeypatch.setattr(libs, 'load_lock', lambda *a, **kw: lock)
    station=tmp_path/'station'; root=station/'runtime-libs/gsap/3.15.0';root.mkdir(parents=True)
    for name, data in {'gsap.min.js':b'gsap','three.module.js':b'module','three.core.js':b'core'}.items(): (root/name).write_bytes(data)
    return station


def test_module_requires_explicit_lib_and_stages_closure(prepared, tmp_path):
    html='<script type="module">import * as THREE from "./three.module.js";</script>'
    assert libs.detect(html)==[]
    dest=tmp_path/'out'; assert set(libs.stage_detected(dest, html, names=['three'], station=prepared)) == {'gsap.min.js','three.module.js','three.core.js'}


@pytest.mark.parametrize('js',['import("https://example.invalid/a.js")','import\ufeff("./three.module.js")','export {x} from "https://example.invalid/x.js"'])
def test_inline_javascript_is_outside_html_check(prepared, js):
    html='<script type="module">'+js+'</script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)==[]


@pytest.mark.parametrize('base',['', '.', './'])
def test_neutral_base_keeps_autodetect(prepared, base):
    assert libs.detect('<base href="'+base+'"><script src="./gsap.min.js?v=1#f"></script>')==['gsap']


@pytest.mark.parametrize('base',['assets/','../','/','index.html','https://example.invalid/'])
def test_non_neutral_base(prepared, base):
    html='<base href="'+base+'"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)
    with pytest.raises(ContractError): libs.assert_no_remote_code(html)


def test_first_base_href_wins(prepared):
    html='<base><base href="." href="https://bad.invalid"><base href="https://bad.invalid"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==['gsap'] and libs.assert_no_remote_code(html, strict=False)==[]


def test_index_utf8_bom_and_invalid(prepared, tmp_path):
    p=tmp_path/'project'; p.mkdir(); index=p/'index.html'; raw=b'\xef\xbb\xbf' + '<script src="gsap.min.js"></script><p>Tiếng Việt</p>'.encode('utf-8')
    index.write_bytes(raw); assert libs.stage_detected(p, station=prepared)==['gsap.min.js']; assert index.read_bytes()==raw
    bad=tmp_path/'bad';bad.mkdir();(bad/'index.html').write_bytes(b'\xff')
    with pytest.raises(ContractError): libs.stage_detected(bad, station=prepared)


def test_write_index_declares_and_verifies_libs(prepared, tmp_path, monkeypatch):
    monkeypatch.setattr(libs._env, 'station_dir', lambda: str(prepared))
    out=tmp_path/'out'; render.write_index(out, '<html></html>', libs=('three',))
    assert (out/'three.core.js').read_bytes()==b'core'
    with pytest.raises(ContractError): render.write_index(tmp_path/'remote','<script src="https://x.invalid/a.js"></script>')


def test_project_lib_flags_validate_before_output(tmp_path):
    for args in (['--project-dir',str(tmp_path),'--lib','unknown'], ['--project-dir',str(tmp_path),'--lib',''], ['--project','news','--input','x','--lib','gsap']):
        assert render.main([*args,'--out',str(tmp_path/'out'),'--json'])==2
        assert not (tmp_path/'out').exists()


def _fake_engine(monkeypatch, captured):
    import subprocess
    from pathlib import Path
    monkeypatch.setattr(render, 'hyperframes_argv', lambda *args, **kw: ['fake', *args])
    monkeypatch.setattr(render, 'engine_versions', lambda: {})
    def check(argv, **kw):
        root=Path(kw['cwd']); captured.append({p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()})
        return subprocess.CompletedProcess(argv, 0, b'', b'')
    monkeypatch.setattr(render.subprocess, 'run', check)
    monkeypatch.setattr(render, 'render_project', lambda proj, out, **kw: Path(out).write_bytes(b'fake'))


def test_user_local_base_self_contained_needs_no_station(prepared, tmp_path, monkeypatch, capsys):
    project=tmp_path/'user'; (project/'assets').mkdir(parents=True)
    (project/'assets/gsap.min.js').write_bytes(b'user')
    (project/'index.html').write_text('<base href="assets/"><script src="gsap.min.js"></script>')
    monkeypatch.setattr(libs._env, 'station_dir', lambda: pytest.fail('station unexpectedly accessed'))
    captured=[];_fake_engine(monkeypatch,captured)
    assert render.main(['--project-dir',str(project),'--out',str(tmp_path/'out')])==0
    assert captured[0]['assets/gsap.min.js']==b'user' and 'gsap.min.js' not in captured[0]
    assert 'base' in capsys.readouterr().err


def test_cli_explicit_lib_multi_sources_and_no_implicit_override(prepared, tmp_path, monkeypatch):
    import socket
    import urllib.request
    def denied(*a, **kw): pytest.fail('unexpected network')
    monkeypatch.setattr(socket.socket,'connect',denied);monkeypatch.setattr(urllib.request,'urlopen',denied)
    project=tmp_path/'user';project.mkdir(); raw=b'<script type="module">import "./three.module.js"</script>'; (project/'index.html').write_bytes(raw)
    source=prepared/'runtime-libs/gsap/3.15.0'; captured=[];_fake_engine(monkeypatch,captured)
    flags=['--lib-file',f'gsap={source/"gsap.min.js"}','--lib-file',f'three:three.module.js={source/"three.module.js"}','--lib-file',f'three:three.core.js={source/"three.core.js"}']
    assert render.main(['--project-dir',str(project),'--out',str(tmp_path/'out1'),*flags])==0
    assert 'three.module.js' not in captured[-1] and 'gsap.min.js' not in captured[-1]
    assert render.main(['--project-dir',str(project),'--out',str(tmp_path/'out2'),'--lib','three','--lib','three',*flags])==0
    assert captured[-1]['three.module.js']==b'module' and captured[-1]['three.core.js']==b'core' and captured[-1]['gsap.min.js']==b'gsap'
    assert (project/'index.html').read_bytes()==raw and not (project/'three.module.js').exists()


def test_non_utf8_index_rejected_before_engine(prepared, tmp_path, monkeypatch):
    project=tmp_path/'user';project.mkdir(); (project/'index.html').write_bytes(b'<meta charset="latin1">\xff')
    monkeypatch.setattr(render,'hyperframes_argv', lambda *a, **kw: pytest.fail('engine invoked'))
    assert render.main(['--project-dir',str(project),'--out',str(tmp_path/'out'),'--lib','gsap','--json'])==2
    assert not (tmp_path/'out').exists()


@pytest.mark.parametrize('src', ['//x.invalid/a.js', r'\\x.invalid/a.js', 'h&#9;ttps://x.invalid/a.js', 'HTTPS:x.invalid/a.js'])
def test_direct_script_urls_still_blocked(src):
    with pytest.raises(ContractError): libs.assert_no_remote_code('<script defer src="'+src+'"></script>')


def test_first_base_non_neutral_wins_and_explicit_still_stages(prepared, tmp_path):
    html='<base href="assets/"><base href="."><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[]
    assert libs.stage_detected(tmp_path/'p', html, names=['gsap'], station=prepared, keep_existing=True)==['gsap.min.js']


def test_template_missing_or_mismatched_lib_never_writes_index(prepared, tmp_path, monkeypatch):
    monkeypatch.setattr(libs._env, 'station_dir', lambda: str(prepared))
    source=prepared/'runtime-libs/gsap/3.15.0/gsap.min.js';source.unlink()
    target=tmp_path/'missing'
    with pytest.raises(Exception) as e: render.write_index(target,'<html></html>',libs=('gsap',))
    from video_studio.contract import StationMissing
    assert isinstance(e.value, StationMissing) and not target.exists()
    target.mkdir(); (target/'gsap.min.js').write_bytes(b'user')
    with pytest.raises(ContractError): render.write_index(target,'<html></html>',libs=('gsap',))
    assert not (target/'index.html').exists() and (target/'gsap.min.js').read_bytes()==b'user'


@pytest.mark.parametrize('tag', ['textarea', 'title', 'xmp', 'iframe', 'noembed', 'noframes', 'noscript'])
def test_base_inside_raw_text_does_not_shadow_real_base(prepared, tag):
    html=f'<{tag}><base href="."><script>ignored</script></{tag}><base href="https://example.invalid/"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[]
    assert libs.assert_no_remote_code(html, strict=False)
    with pytest.raises(ContractError): libs.assert_no_remote_code(html)


@pytest.mark.parametrize('tag',['textarea','title','xmp','iframe'])
def test_script_inside_raw_text_is_not_a_direct_reference(prepared, tag):
    html=f'<{tag}><script src="https://example.invalid/x.js"></script></{tag}><script src="gsap.min.js"></script>'
    assert libs.detect(html)==['gsap'] and libs.assert_no_remote_code(html, strict=False)==[]


@pytest.mark.parametrize('tag', ['script', 'style'])
def test_existing_raw_mode_does_not_shadow_base(prepared, tag):
    html=f'<{tag}><base href="."></{tag}><base href="//example.invalid/"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)


def test_plaintext_remainder_is_not_interpreted_as_html(prepared):
    html='<plaintext><base href="https://example.invalid/"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)==[]


@pytest.mark.parametrize('tag',['textarea','title'])
def test_rcdata_comment_text_does_not_hide_real_script(prepared, tag):
    html=f'<{tag}><!--</{tag}><script src="https://example.invalid/x.js"></script>-->'
    assert libs.assert_no_remote_code(html, strict=False)
    with pytest.raises(ContractError): libs.assert_no_remote_code(html)


def test_inert_template_base_does_not_shadow_real_base(prepared):
    html='<template><base href="."></template><base href="https://example.invalid/"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)


def test_inert_template_script_is_not_a_direct_reference(prepared):
    html='<template><script src="https://example.invalid/x.js"></script></template><script src="gsap.min.js"></script>'
    assert libs.detect(html)==['gsap'] and libs.assert_no_remote_code(html, strict=False)==[]


@pytest.mark.parametrize('tag',['textarea','title','xmp','iframe'])
def test_raw_comment_text_closes_before_following_script(prepared, tag):
    html=f'<{tag}><!-- </{tag}> --><script src="https://example.invalid/x.js"></script>'
    assert libs.assert_no_remote_code(html, strict=False)


def test_nested_inert_template_and_raw_content_do_not_shadow_base(prepared):
    html='<template><textarea><template><base href="."></textarea><template><base href="."></template></template><base href="https://example.invalid/"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)


@pytest.mark.parametrize('tag,closer', [
    ('textarea','</textarea/>'), ('textarea','</textarea data-x>'),
    ('title','</title/>'), ('title','</title data-x>'),
    ('xmp','</xmp/>'), ('iframe','</iframe data-x>'),
    ('script','</script data-x>'), ('style','</style/>'),
])
def test_recovered_raw_end_tags_do_not_hide_script(prepared, tag, closer):
    html=f'<{tag}>text{closer}<script src="https://example.invalid/x.js"></script>'
    assert libs.assert_no_remote_code(html, strict=False)
    with pytest.raises(ContractError): libs.assert_no_remote_code(html)


def test_raw_end_tag_quoted_gt_does_not_close_early(prepared):
    html='<textarea>text</textarea data-x=\"> <base href=.&gt;\"><base href="https://example.invalid/"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)


def test_raw_end_tag_quote_inside_unquoted_value_does_not_hide_script(prepared):
    html='<textarea>text</textarea data-x=a" ><script src="https://example.invalid/x.js"></script>'
    assert libs.assert_no_remote_code(html, strict=False)


@pytest.mark.parametrize('fake_close', ['</ textarea>', '</textarea\u00a0>'])
def test_invalid_end_tag_does_not_expose_fake_base(prepared, fake_close):
    html='<textarea>'+fake_close+'<base href="."></textarea><base href="https://example.invalid/"><script src="gsap.min.js"></script>'
    assert libs.detect(html)==[] and libs.assert_no_remote_code(html, strict=False)


@pytest.mark.parametrize('fragment', ['a/="', 'a /="'])
def test_raw_end_tag_slash_before_equals_does_not_hide_script(prepared, fragment):
    html='<textarea>text</textarea '+fragment+' ><script src="https://example.invalid/x.js"></script>'
    assert libs.assert_no_remote_code(html, strict=False)
    with pytest.raises(ContractError): libs.assert_no_remote_code(html)
