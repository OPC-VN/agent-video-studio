# DN6: inline JavaScript tests now assert the HTML-only contract; prior parser evidence remains in the sprint record.
import copy
import hashlib
import html.parser
import os

import pytest

from video_studio import runtime_libs as libs, render, projects
from video_studio.contract import ContractError, StationMissing


def test_html_parser_accepts_new_cdata_keyword(monkeypatch):
    original = html.parser.HTMLParser.parse_starttag

    def newer_parser(self, index):
        for tag in ('script', 'title', 'textarea'):
            if self.rawdata[index:index + len(tag) + 1].lower() == '<' + tag:
                self.set_cdata_mode(tag, escapable=tag != 'script')
                self.clear_cdata_mode()
                break
        return original(self, index)

    monkeypatch.setattr(html.parser.HTMLParser, 'parse_starttag', newer_parser)
    assert libs.assert_no_remote_code('<script src="./local.js"></script>', strict=True) == []
    for tag in ('title', 'textarea'):
        content = f'<{tag}>&lt;/{tag}&gt;<script src=fake.js></script></{tag}>'
        assert libs._html_references(content + '<script src=gsap.min.js></script>') == (['gsap.min.js'], [])


def test_escaped_comment_marker_in_script_is_not_html_comment():
    assert libs._html_references('<script>const x="&lt;!--";</script>') == ([], [])


def test_html_parser_new_marked_section_recovery_is_not_silent(monkeypatch):
    original = html.parser.HTMLParser.parse_html_declaration

    def newer_parser(self, index):
        if self.rawdata[index:index + 3] == '<![':
            end = self.rawdata.find('>', index + 3)
            self.handle_comment(self.rawdata[index + 2:end])
            return end + 1
        return original(self, index)

    monkeypatch.setattr(html.parser.HTMLParser, 'parse_html_declaration', newer_parser)
    _, violations = libs._html_references('<![IGNORE[><script src=https://example.invalid/x.js></script>]]>')
    assert any('cấu trúc HTML/SVG chưa được hỗ trợ' in item for item in violations)


def test_marked_section_text_in_plaintext_or_rcdata_is_not_a_declaration():
    prefix = '<script src=gsap.min.js></script>'
    assert libs._html_references(prefix + '<plaintext><![CDATA[><script src=fake.js></script>') == (['gsap.min.js'], [])
    assert libs._html_references('<textarea><![IGNORE[><script src=fake.js></script></textarea>' + prefix) == (['gsap.min.js'], [])


def test_incomplete_marked_section_fails_closed():
    _, violations = libs._html_references('<![IGNORE[')
    assert any('cấu trúc HTML/SVG chưa được hỗ trợ' in item for item in violations)


@pytest.mark.skipif(os.name == 'nt', reason='POSIX FIFO required')
def test_publish_rejects_fifo_before_reading(tmp_path, monkeypatch):
    destination = tmp_path / 'runtime.js'
    os.mkfifo(destination)

    def forbid_read(*args, **kwargs):
        raise AssertionError('non-regular destination must not be read')

    monkeypatch.setattr(libs.os, 'fdopen', forbid_read)
    with pytest.raises(ContractError, match='Không ghi đè'):
        libs._publish_files(str(tmp_path), 'project', '', {'runtime.js': b'code'}, project=True)


@pytest.fixture
def lock_and_station(tmp_path, monkeypatch):
    lock = libs.load_lock(); base = lock['libs']['gsap']; base['members'][0]['file_sha256'] = hashlib.sha256(b'gsap').hexdigest()
    lib = copy.deepcopy(base); lib['members'] = [dict(base['members'][0], dest='three.module.js', file_sha256=hashlib.sha256(b'module').hexdigest()), dict(base['members'][0], dest='three.core.js', file_sha256=hashlib.sha256(b'core').hexdigest())]
    lock['libs']['three'] = lib
    monkeypatch.setattr(libs, 'load_lock', lambda path=None: lock)
    station = tmp_path / 'station'; directory = station / 'runtime-libs/gsap/3.15.0'; directory.mkdir(parents=True)
    for name, data in {'gsap.min.js':b'gsap', 'three.module.js':b'module', 'three.core.js':b'core'}.items(): (directory / name).write_bytes(data)
    return lock, station


def test_detect_and_stage_multimember(lock_and_station, tmp_path):
    _, station = lock_and_station
    html = '<script type="module">import * as THREE from "./three.module.js";</script>'
    assert libs.detect(html) == []
    out = tmp_path / 'project'
    assert set(libs.stage_detected(out, html, names=['three'], station=station)) == {'three.module.js', 'three.core.js'}
    assert (out / 'three.core.js').read_bytes() == b'core'


def test_missing_does_not_create_project(lock_and_station, tmp_path):
    lock, station = lock_and_station
    (station / 'runtime-libs/gsap/3.15.0/gsap.min.js').unlink(); project=tmp_path/'project'
    with pytest.raises(StationMissing): libs.stage(['gsap'], project, station=station)
    assert not project.exists()


def test_keep_existing_without_station(lock_and_station, tmp_path, capsys):
    lock, station = lock_and_station
    project=tmp_path/'project';project.mkdir();(project/'gsap.min.js').write_bytes(b'user')
    (station/'runtime-libs/gsap/3.15.0/gsap.min.js').unlink()
    assert libs.stage(['gsap'], project, station=station, keep_existing=True) == []
    assert (project/'gsap.min.js').read_bytes() == b'user'
    assert 'gsap.min.js' in capsys.readouterr().err


@pytest.mark.parametrize('html', ["<script defer src='//example.org/a.js'></script>", '<script type="module">import x from "https://example.org/x.js"</script>'])
def test_direct_remote_script_detected_but_inline_import_ignored(html):
    if ' src=' in html:
        assert libs.assert_no_remote_code(html, strict=False)
        with pytest.raises(ContractError): libs.assert_no_remote_code(html)
    else:
        assert libs.assert_no_remote_code(html, strict=False) == []


def test_write_index_blocks_remote_script_before_creating_project(lock_and_station, tmp_path):
    project = tmp_path / 'project'
    with pytest.raises(ContractError): render.write_index(project, '<script src="https://example.org/a.js"></script>')
    assert not project.exists()


def test_overrides_and_dependency_closure(lock_and_station, tmp_path):
    lock, station = lock_and_station
    lock['libs']['three']['requires'] = ['gsap']
    (station/'runtime-libs/gsap/3.15.0/gsap.min.js').unlink()
    override=tmp_path/'override'; override.write_bytes(b'gsap')
    libs.set_overrides({'gsap': str(override)})
    try:
        dest=tmp_path/'out'
        assert set(libs.stage(['three'], dest, station=station)) == {'gsap.min.js','three.module.js','three.core.js'}
        assert (dest/'gsap.min.js').read_bytes() == b'gsap'
    finally: libs.set_overrides({})


def test_stage_does_not_clobber_even_when_keep_false(lock_and_station, tmp_path):
    lock, station = lock_and_station
    project=tmp_path/'project';project.mkdir(); target=project/'gsap.min.js';target.write_bytes(b'user')
    with pytest.raises(ContractError): libs.stage(['gsap'], project, station=station)
    assert target.read_bytes() == b'user'


def test_detect_direct_attribute_and_ignore_import(lock_and_station):
    html = "<link href='./gsap.min.js?q=1'><script type='module'>import './three.module.js'</script>"
    assert libs.detect(html) == ['gsap']


def test_stage_never_accesses_network(lock_and_station, tmp_path, monkeypatch):
    import socket
    import urllib.request
    _, station = lock_and_station
    def denied(*args, **kwargs): raise AssertionError('network called')
    monkeypatch.setattr(socket.socket, 'connect', denied)
    monkeypatch.setattr(urllib.request, 'urlopen', denied)
    assert libs.stage(['gsap'], tmp_path/'out', station=station) == ['gsap.min.js']


def test_write_index_stages_declared_override_and_blocks_remote_script(lock_and_station, tmp_path):
    override = tmp_path/'override'; override.write_bytes(b'gsap')
    libs.set_overrides({'gsap': str(override)})
    try:
        project = tmp_path/'out'; render.write_index(project, '<script src="gsap.min.js"></script>', libs=('gsap',))
        assert (project/'gsap.min.js').read_bytes() == b'gsap'
        with pytest.raises(ContractError): render.write_index(tmp_path/'remote', '<script src="https://remote/x.js"></script>')
    finally: libs.set_overrides({})


def test_ensure_without_index_and_existing_user_file(lock_and_station, tmp_path):
    _, station=lock_and_station
    seed=station/'demo'; seed.mkdir();(seed/'hyperframes.json').write_text('{}')
    project=projects.ensure('sample', station=str(station))
    from pathlib import Path
    project=Path(project); assert not (project/'index.html').exists()
    (project/'index.html').write_text('<script src="gsap.min.js"></script>')
    (project/'gsap.min.js').write_bytes(b'user')
    projects.ensure('sample', station=str(station))
    assert (project/'gsap.min.js').read_bytes() == b'user'


def test_http_scheme_without_slashes_is_blocked():
    with pytest.raises(ContractError): libs.assert_no_remote_code('<script src="https:evil.js"></script>')


def test_custom_project_only_stages_copy(lock_and_station, tmp_path, monkeypatch, capsys):
    import subprocess
    import types
    _, station = lock_and_station
    project = tmp_path/'custom'; project.mkdir()
    (project/'index.html').write_text('<script src="gsap.min.js"></script><script src="https://example.org/x.js"></script>')
    monkeypatch.setattr(libs._env, 'station_dir', lambda: str(station))
    monkeypatch.setattr(render, 'hyperframes_argv', lambda *a, **kw: ['fake', *a])
    monkeypatch.setattr(render, 'engine_versions', lambda: {})
    def check(argv, **kw):
        from pathlib import Path
        assert (Path(kw['cwd'])/'gsap.min.js').read_bytes() == b'gsap'
        return subprocess.CompletedProcess(argv, 0, b'', b'')
    monkeypatch.setattr(render.subprocess, 'run', check)
    monkeypatch.setattr(render, 'render_project', lambda proj, out, **kw: open(out, 'wb').write(b'video'))
    render.do_render_project_dir(types.SimpleNamespace(project_dir=str(project), out=str(tmp_path/'out')))
    assert not (project/'gsap.min.js').exists()
    assert 'Cảnh báo mã từ xa' in capsys.readouterr().err


def test_ensure_and_write_index_do_not_use_network(lock_and_station, tmp_path, monkeypatch):
    import socket
    import urllib.request
    _, station = lock_and_station
    def denied(*args, **kwargs): raise AssertionError('network called')
    monkeypatch.setattr(socket.socket, 'connect', denied)
    monkeypatch.setattr(urllib.request, 'urlopen', denied)
    monkeypatch.setattr(libs._env, 'station_dir', lambda: str(station))
    seed=station/'demo'; seed.mkdir(); (seed/'hyperframes.json').write_text('{}')
    project=projects.ensure('sample', station=str(station))
    render.write_index(project, '<script src="gsap.min.js"></script>', libs=('gsap',))
    projects.ensure('sample', station=str(station))


@pytest.mark.parametrize('html', [
    '<script type="module">import {\nvalue\n} from "https://example.invalid/x.js"</script>',
    '<script type="module">import/*comment*/("https://example.invalid/x.js")</script>',
    '<script src="\\\\example.invalid/x.js"></script>',
    '<script src="h&#9;ttps://example.invalid/x.js"></script>',
])
def test_direct_script_url_normalization_and_inline_import_scope(html):
    if ' src=' in html:
        with pytest.raises(ContractError): libs.assert_no_remote_code(html)
    else: assert libs.assert_no_remote_code(html, strict=False) == []


@pytest.mark.parametrize('html', [
    '<script type="module">import "https:\\x2f\\x2fexample.invalid/x.js"</script>',
    '<script type="module">import /*a*/ {x} /*b*/ from /*c*/ "//example.invalid/x.js"</script>',
    '<script type="module">import(`https://example.invalid/x.js`)</script>',
])
def test_inline_remote_literal_imports_outside_html_scope(html):
    assert libs.assert_no_remote_code(html, strict=False) == []


def test_import_looking_text_inside_strings_and_comments_ignored():
    html = '''<script>const label = "import('https://example.invalid/x.js')";
    // import('https://example.invalid/x.js')
    /* import('https://example.invalid/x.js') */</script>'''
    assert libs.assert_no_remote_code(html, strict=False) == []


def test_stage_does_not_makedirs_before_safe_anchor(lock_and_station, tmp_path, monkeypatch):
    _, station = lock_and_station
    def denied(*args, **kwargs): raise AssertionError('unsafe makedirs')
    monkeypatch.setattr(libs.os, 'makedirs', denied)
    monkeypatch.setattr(libs, '_publish_files', lambda *a, **kw: None)
    assert libs.stage(['gsap'], tmp_path/'missing'/'project', station=station) == ['gsap.min.js']


def test_stage_rejects_symlinked_parent_before_mkdir(lock_and_station, tmp_path):
    _, station = lock_and_station
    outside=tmp_path/'outside'; outside.mkdir(); alias=tmp_path/'alias'
    try: alias.symlink_to(outside, target_is_directory=True)
    except OSError: pytest.skip('directory symlink unavailable')
    with pytest.raises((OSError, ContractError)):
        libs.stage(['gsap'], alias/'new-project', station=station)
    assert not (outside/'new-project').exists()


def test_detect_does_not_scan_multiline_inline_imports(lock_and_station):
    html = '<script type="module">import {x} from "./three.module.js"; import("./gsap.min.js")</script>'
    assert libs.detect(html) == []


@pytest.mark.skipif(__import__('os').name != 'nt', reason='Windows native no-recall path')
def test_stage_detected_reads_index_with_no_reparse(lock_and_station, tmp_path, monkeypatch):
    from video_studio.effect_library import _native_windows as native
    project = tmp_path/'project'; project.mkdir(); (project/'index.html').write_text('<html></html>')
    def denied(path): raise OSError('reparse or offline parent')
    monkeypatch.setattr(native, 'open_root', denied)
    with pytest.raises(ContractError): libs.stage_detected(project)


def test_stage_detected_rejects_symlinked_index_parent(lock_and_station, tmp_path):
    outside=tmp_path/'outside'; outside.mkdir(); (outside/'index.html').write_text('<html></html>')
    alias=tmp_path/'alias'
    try: alias.symlink_to(outside, target_is_directory=True)
    except OSError: pytest.skip('directory symlink unavailable')
    with pytest.raises(ContractError): libs.stage_detected(alias)


def test_first_duplicate_script_src_matches_browser():
    with pytest.raises(ContractError):
        libs.assert_no_remote_code('<script src="https://example.invalid/x.js" src="local.js"></script>')


@pytest.mark.parametrize('html,expected', [
    ('<script>const r = /"/; import("https://example.invalid/x.js");</script>', 'remote'),
    ('<script>const r = /"/; import("./gsap.min.js");</script>', 'local'),
    ('<script>const q = 10 / 2; import("https://example.invalid/x.js");</script>', 'remote'),
    ('<script>const x = `${import("https://example.invalid/x.js")}`;</script>', 'remote'),
])
def test_inline_import_after_regex_division_or_template_is_not_scanned(lock_and_station, html, expected):
    assert libs.detect(html) == []
    assert libs.assert_no_remote_code(html, strict=False) == []


def test_inline_ambiguous_regex_and_local_import_are_not_scanned(lock_and_station):
    html = '<script>if (ready) /"/.test(value); import("./gsap.min.js");</script>'
    assert libs.detect(html) == [] and libs.assert_no_remote_code(html, strict=False) == []


def test_write_index_rejects_existing_wrong_runtime(lock_and_station, tmp_path):
    project=tmp_path/'project'; project.mkdir()
    old=project/'gsap.min.js'; old.write_bytes(b'user content')
    with pytest.raises(ContractError):
        render.write_index(project, '<script src="gsap.min.js"></script>', libs=('gsap',))
    assert old.read_bytes() == b'user content'
    assert not (project/'index.html').exists()


@pytest.mark.parametrize('html', [
    '<base href="https://example.invalid/"><script src="gsap.min.js"></script>',
    '<base href="//example.invalid/"><script src="gsap.min.js"></script>',
    '<script type="module">export {x} from "https://example.invalid/x.js";</script>',
    '<script type="module">export * /*x*/ from "//example.invalid/x.js";</script>',
])
def test_remote_base_is_flagged_and_inline_reexport_is_not_scanned(html):
    if html.startswith('<base'):
        assert libs.assert_no_remote_code(html, strict=False)
        with pytest.raises(ContractError): libs.assert_no_remote_code(html)
    else: assert libs.assert_no_remote_code(html, strict=False) == []


def test_detect_does_not_scan_inline_local_reexport(lock_and_station):
    assert libs.detect('<script type="module">export {x} from "./three.module.js";</script>') == []


def test_user_project_remote_base_warns_without_blocking(lock_and_station, tmp_path, capsys):
    _, station = lock_and_station
    html='<base href="https://example.invalid/"><script src="gsap.min.js"></script>'
    dest=tmp_path/'user-project'
    assert libs.stage_detected(dest, html, station=station, keep_existing=True) == []
    assert 'Cảnh báo' in capsys.readouterr().err


@pytest.mark.parametrize('html', [
    '<script>const x = `${1} import("https://example.invalid/x.js")`;</script>',
    '<script>const x = `\\${import("https://example.invalid/x.js")}`;</script>',
])
def test_template_text_and_escaped_interpolation_are_not_executed(html):
    assert libs.assert_no_remote_code(html, strict=False) == []


def test_inline_nested_template_import_is_not_scanned():
    html = '<script>const x = `${`${import("https://example.invalid/x.js")}`}`;</script>'
    assert libs.assert_no_remote_code(html, strict=False) == []


@pytest.mark.parametrize('target', ['https://example.invalid/x.js', './gsap.min.js'])
def test_inline_interpolation_regex_and_import_are_not_scanned(lock_and_station, target):
    html = '<script>const t = `${ /}/.test("x"), import("' + target + '") }`;</script>'
    assert libs.detect(html) == [] and libs.assert_no_remote_code(html, strict=False) == []


def test_nested_template_local_import_does_not_warn_remote(lock_and_station):
    html = '<script>const t = `${`${import("./gsap.min.js")}`}`;</script>'
    assert libs.detect(html) == [] and libs.assert_no_remote_code(html, strict=False) == []


@pytest.mark.parametrize('target', ['https://example.invalid/x.js', './gsap.min.js'])
@pytest.mark.parametrize('expression', [
    '(function(){ return /}/; })(), import(TARGET)',
    '(function(){ return /[}\\"`]/; })(), import(TARGET)',
    '(function(){ throw /}/; })(), import(TARGET)',
    '(function*(){ yield /}/; })(), import(TARGET)',
    '(async function(){ await /}/; })(), import(TARGET)',
    '(function(){ return /* } */ /}/; })(), import(TARGET)',
    '(function(){ return "}"; })(), import(TARGET)',
    '(function(){ return 12 / 3 / 2; })(), import(TARGET)',
    '`${(function(){ return /}/; })(), import(TARGET)}`',
])
def test_inline_interpolations_are_outside_html_scope(lock_and_station, expression, target):
    html = '<script>const t = `${' + expression.replace('TARGET', '"' + target + '"') + '}`;</script>'
    assert libs.detect(html) == [] and libs.assert_no_remote_code(html, strict=False) == []


@pytest.mark.parametrize('statement', [
    'import TARGET;', 'import value from TARGET;',
    'import {value as other} from TARGET;', 'import * as ns from TARGET;',
    'import(TARGET);', 'export {value} from TARGET;',
    'export * from TARGET;', 'export * as ns from TARGET;',
])
@pytest.mark.parametrize('target', ['https://example.invalid/x.js', './gsap.min.js'])
def test_inline_import_and_reexport_are_outside_html_scope(lock_and_station, statement, target):
    html = '<script>' + statement.replace('TARGET', '"' + target + '"') + '</script>'
    assert libs.detect(html) == [] and libs.assert_no_remote_code(html, strict=False) == []


@pytest.mark.parametrize('source', [
    r'''const re = /import\("https:\/\/example.invalid\/x.js"\)/;''',
    r'''const re = /[}"'`]/; const x = 10 / 2;''',
    '''const x = `${"import('https://example.invalid/x.js')"}`;''',
    '''const x = `${1 /* } import('https://example.invalid/x.js') */}`;''',
    '''const x = `text ${1} import('https://example.invalid/x.js')`;''',
    '''const x = `\\${import('https://example.invalid/x.js')}`;''',
    '''obj.import("https://example.invalid/x.js"); obj?.import("https://example.invalid/x.js");''',
])
def test_non_executed_import_text_has_no_remote_or_local_findings(lock_and_station, source):
    html = '<script>' + source + '</script>'
    assert libs.assert_no_remote_code(html, strict=False) == []
    assert libs.detect(html) == []


@pytest.mark.parametrize('source', [
    'const t = `${ (function(){ return /unterminated; })() }`;',
    'const t = `${ "unterminated }`;',
    'const t = `${ /* unterminated }`;',
    'const t = `${ `${ 1 }`;',
    'if (ready) /[}"`]/.test(value);',
    'function f() {} /[}"`]/.test(value);',
])
def test_inline_ambiguous_or_unterminated_javascript_is_not_scanned(source):
    assert libs.assert_no_remote_code('<script>' + source + '</script>', strict=False) == []


def test_inline_template_nesting_is_not_scanned():
    source = '`${' * 34 + '1' + '}`' * 34
    assert libs.assert_no_remote_code('<script>' + source + '</script>', strict=False) == []


@pytest.mark.parametrize("content,valid", [(b"gsap", True), (b"wrong", False)])
def test_detected_existing_runtime_can_be_required_to_match(lock_and_station, tmp_path, content, valid):
    _, station = lock_and_station
    project = tmp_path / "project"
    project.mkdir()
    existing = project / "gsap.min.js"
    existing.write_bytes(content)
    html = '<script src="gsap.min.js"></script>'
    if valid:
        assert libs.stage_detected(project, html, station=station, keep_existing=True, verify_existing=True) == []
    else:
        with pytest.raises(ContractError):
            libs.stage_detected(project, html, station=station, keep_existing=True, verify_existing=True)
    assert existing.read_bytes() == content
