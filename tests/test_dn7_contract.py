"""DN7: a small SVG subset, without pretending to parse all HTML5 foreign content."""
import copy
import hashlib
from pathlib import Path
import re
import subprocess
from types import SimpleNamespace

import pytest

from video_studio import render, runtime_libs as libs
from video_studio.contract import ContractError


LOCAL = '<script src="gsap.min.js"></script>'
REMOTE = '<script src="https://example.invalid/x.js"></script>'
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def station(tmp_path, monkeypatch):
    lock = copy.deepcopy(libs.load_lock())
    lock['libs']['gsap']['members'][0]['file_sha256'] = hashlib.sha256(b'gsap').hexdigest()
    monkeypatch.setattr(libs, 'load_lock', lambda *args, **kwargs: lock)
    result = tmp_path / 'station'
    directory = result / 'runtime-libs' / 'gsap' / lock['packages']['gsap']['version']
    directory.mkdir(parents=True)
    (directory / 'gsap.min.js').write_bytes(b'gsap')
    monkeypatch.setattr(libs._env, 'station_dir', lambda: str(result))
    return result


@pytest.mark.parametrize('foreign', [
    '<svg><style><p>', '<svg><title><p>', '<svg><desc><p>',
    '<svg><foreignObject>', '<svg><script>',
    '<math><style><p>', '<math><annotation-xml encoding="text/html">',
])
def test_foreign_ambiguity_is_flagged_before_raw_mode(foreign):
    html = LOCAL + '\n' + foreign + REMOTE
    findings = libs.assert_no_remote_code(html, strict=False)
    assert any('dòng 2' in item and 'cấu trúc HTML/SVG chưa được hỗ trợ' in item for item in findings)
    assert libs.detect(html) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


@pytest.mark.parametrize('foreign', [
    '<svg><path></svg>', '<svg><path/></rect></svg>', '<svg><svg/></svg>',
    '<svg><pattern/></svg>', '<svg><defs><path/></defs></svg>',
    '<svg><path><rect/></path></svg>', '<svg><circle/></svg>',
    '<svg onclick="x()"/>', '<svg><path href="#x"/></svg>',
    '<svg xmlns="https://example.invalid/svg"/>', '<svg xmlns=""/>',
    '<svg><path xmlns="http://www.w3.org/2000/svg"/></svg>',
    '<svg xmlns:xlink="http://www.w3.org/1999/xlink"/>',
    '<svg><path xlink:href="#x"/></svg>', '<svg:svg/>',
    '<svg><![CDATA[<path/>]]></svg>', '<svg><?marker value?></svg>',
    '<svg><!-- marker --></svg>', '<svg><!DOCTYPE svg></svg>',
    '<svg>text</svg>', '<svg>&lt;path/&gt;</svg>',
    '<svg>', '<svg><path/>', '<svg><defs><pattern>',
    '<svg><path/></svg extra>', '<svg><path/></svg/>', '</svg>', '</math>',
    '<svg width="1" width="2"/>', '<svg width/>', '<svg ="x"/>',
    '<svg><path d="M0 0"',
])
def test_foreign_unbalanced_or_unknown_structure_is_not_silent(foreign):
    html = LOCAL + foreign + LOCAL
    assert any('cấu trúc HTML/SVG chưa được hỗ trợ' in item
               for item in libs.assert_no_remote_code(html, strict=False))
    assert libs.detect(html) == []


def test_existing_svg_logo_and_seed_are_supported():
    paths = [ROOT / 'video_studio/templates/news/news_video.py',
             ROOT / 'templates/_seed/index.html',
             *sorted((ROOT / 'tests/fixtures/news_images').glob('*.html'))]
    blocks = [block for path in paths
              for block in re.findall(r'<svg\b.*?</svg>', path.read_text(encoding='utf-8'), re.S)]
    assert len(blocks) == 11
    for svg in blocks:
        assert libs.assert_no_remote_code(svg, strict=False) == []
        assert libs.detect(LOCAL + svg + LOCAL) == ['gsap']


def test_generated_news_html_keeps_supported_svg(news, tmp_path, monkeypatch):
    import news_harness as harness

    captured = harness.install(monkeypatch, news, tmp_path / 'generated')
    from video_studio import voice as voice_mod
    monkeypatch.setattr(voice_mod, 'synth_text', lambda *args, **kwargs: [0] * 24000)
    news.make({'title': 'Tin', 'summary': 'Tin mới.'}, str(tmp_path / 'daily.mp4'), '2026-01-02',
              model=harness.MODEL, brand=harness.MIN_BRAND)
    for short in (False, True):
        harness.weekly(news, [{'headline': 'Tin', 'narration': 'Tin mới.'}],
                       tmp_path / 'weekly.mp4', short=short)
    assert len(captured) == 3
    for html in captured:
        assert len(re.findall(r'<svg\b', html)) == 1
        assert libs.assert_no_remote_code(html, strict=False) == []
        assert libs.detect(html) == ['gsap']


@pytest.mark.parametrize('svg', [
    '<svg/>', '<svg></svg>', '<SVG><PATH d="M0 0" /></SVG>',
    '<svg width=10><path d="M0 0"></path><rect width="2"/></svg>',
    '<svg xmlns="http://www.w3.org/2000/svg"><defs><pattern id="g" patternUnits="userSpaceOnUse">'
    '<path d="M0 0"/></pattern></defs><rect fill="url(#g)"/></svg>',
])
def test_direct_html_after_supported_svg_is_still_checked(svg):
    assert libs.assert_no_remote_code(svg, strict=False) == []
    assert libs.detect(svg + LOCAL) == ['gsap']
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(svg + REMOTE)
    assert libs.detect(LOCAL + svg + '<base href="assets/">' + LOCAL) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(svg + '<base href="assets/">')


@pytest.mark.parametrize('unsupported', ['<svg><style><p>', '<!--a--b-->'])
def test_template_structure_fails_before_stage_or_index(tmp_path, monkeypatch, unsupported):
    def denied(*args, **kwargs):
        raise AssertionError('stage must not run')
    monkeypatch.setattr(libs, 'stage', denied)
    project = tmp_path / 'new'
    with pytest.raises(ContractError, match='cấu trúc HTML/SVG chưa được hỗ trợ'):
        render.write_index(project, LOCAL + unsupported + LOCAL, libs=('gsap',))
    assert not project.exists()


@pytest.mark.parametrize('explicit', [False, True])
@pytest.mark.parametrize('unsupported', ['<svg><style><p>', '<!--a--b-->'])
def test_user_structure_warning_disables_all_autodetect(station, tmp_path, monkeypatch, capsys,
                                                      explicit, unsupported):
    source = tmp_path / 'source'
    source.mkdir()
    raw = b'\xef\xbb\xbf' + (LOCAL + unsupported + LOCAL + '<p>Tiếng Việt</p>').encode('utf-8')
    (source / 'index.html').write_bytes(raw)
    if not explicit:
        def denied(*args, **kwargs):
            raise AssertionError('autodetect must not read station')
        monkeypatch.setattr(libs, 'station_path', denied)
    monkeypatch.setattr(render, 'hyperframes_argv', lambda *args, **kwargs: ['fake', *args])
    monkeypatch.setattr(render, 'engine_versions', lambda: {})
    captured = []
    def check(argv, **kwargs):
        project = Path(kwargs['cwd'])
        assert project != source
        assert (project / 'index.html').read_bytes() == raw
        runtime = project / 'gsap.min.js'
        assert runtime.exists() == explicit
        if explicit:
            assert runtime.read_bytes() == b'gsap'
        captured.append(project)
        return subprocess.CompletedProcess(argv, 0, b'', b'')
    monkeypatch.setattr(render.subprocess, 'run', check)
    monkeypatch.setattr(render, 'render_project', lambda project, out, **kwargs: Path(out).write_bytes(b'fake'))
    render.do_render_project_dir(SimpleNamespace(project_dir=str(source), out=str(tmp_path / 'output'),
                                                lib=['gsap'] if explicit else []))
    assert captured
    assert (source / 'index.html').read_bytes() == raw
    assert not (source / 'gsap.min.js').exists()
    assert 'Cảnh báo cấu trúc HTML/SVG chưa được hỗ trợ' in capsys.readouterr().err


@pytest.mark.parametrize('wrapper', [
    '<script>const x = "FOREIGN";</script>', '<style>/* FOREIGN */</style>',
    '<textarea>FOREIGN</textarea>', '<title>FOREIGN</title>',
    '<!-- FOREIGN -->',
])
def test_inert_html_and_javascript_do_not_enter_foreign_guard(wrapper):
    html = wrapper.replace('FOREIGN', '<svg><foreignObject></foreignObject></svg>') + LOCAL
    assert libs.assert_no_remote_code(html, strict=False) == []
    assert libs.detect(html) == ['gsap']


@pytest.mark.parametrize('foreign', [
    '<svg><title>', '<svg><style>', '<math><style>',
])
def test_template_foreign_breakout_is_flagged_before_raw_mode(foreign):
    html = LOCAL + '<template>' + foreign + '</template>' + REMOTE + LOCAL
    assert any('cấu trúc HTML/SVG chưa được hỗ trợ' in item
               for item in libs.assert_no_remote_code(html, strict=False))
    assert libs.detect(html) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


def test_template_html_references_are_inert_and_supported_svg_keeps_nesting():
    html = ('<template>' + REMOTE + '<template><svg><path d="M0 0"/></svg></template>'
            '<style>/* <svg><title> */</style><textarea><math></textarea>'
            '</template>' + LOCAL)
    assert libs.assert_no_remote_code(html, strict=False) == []
    assert libs.detect(html) == ['gsap']


@pytest.mark.parametrize('tail', [
    '<base href="."></script><base href="https://example.invalid/">' + LOCAL,
    '<template></script>' + REMOTE,
])
@pytest.mark.parametrize('nested', ['<script>', '<ScRiPt >', '<script/>', '<script\n>'])
def test_script_double_escape_does_not_hide_real_base_or_script(tail, nested):
    html = LOCAL + '<script><!--' + nested + '</script>' + tail
    assert any('cấu trúc HTML/SVG chưa được hỗ trợ' in item
               for item in libs.assert_no_remote_code(html, strict=False))
    assert libs.detect(html) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


@pytest.mark.parametrize('text', [
    'const text = "<script>";', 'const text = "-->";',
    '<![CDATA[<script>]]>', 'const text = "<scr&#105;pt>";',
])
def test_script_without_double_escape_keeps_direct_html_detection(text):
    html = '<script>' + text + '</script>' + LOCAL
    assert libs.assert_no_remote_code(html, strict=False) == []
    assert libs.detect(html) == ['gsap']
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html + REMOTE)


@pytest.mark.parametrize('text', [
    '<!-- plain HTML comment -->', '<!-- unclosed comment',
    '<!--<scriptx></scriptx> -->', '<!--comment--><script>',
    'const text = "<!--";', '<!--<scr&#105;pt> -->',
])
def test_script_html_comment_marker_is_conservatively_unsupported(text):
    html = LOCAL + '<script>' + text + '</script>' + LOCAL
    assert libs.assert_no_remote_code(html, strict=False)
    assert libs.detect(html) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


@pytest.mark.parametrize('malformed', [
    '<![CDATA[>' + REMOTE + ']]>', '<![IGNORE[>' + REMOTE + ']]>',
    '<!-->' + REMOTE + '-->', '<!--->' + REMOTE + '-->',
    '<!-- x --!>' + REMOTE + '-->', '<!-- x <!-- nested -->' + REMOTE,
    '<!--<!-->' + REMOTE,
    '<!-- x -- >' + REMOTE + '-->', '<!-- unclosed',
])
def test_marked_sections_and_comment_recovery_are_not_silent(malformed):
    html = LOCAL + malformed + LOCAL
    assert any('cấu trúc HTML/SVG chưa được hỗ trợ' in item
               for item in libs.assert_no_remote_code(html, strict=False))
    assert libs.detect(html) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


@pytest.mark.parametrize('comment', [
    '<!--a--b-->', '<!-- -- -->', '<!--a---b-->', '<!--\nTiếng Việt -- nội dung\n-->',
])
@pytest.mark.parametrize('wrapper', ['{}', '<template>{}</template>'])
def test_comment_body_with_double_hyphen_is_unsupported(comment, wrapper):
    html = LOCAL + '\n' + wrapper.format(comment) + LOCAL
    findings = libs.assert_no_remote_code(html, strict=False)
    assert any('dòng 2' in item and 'cấu trúc HTML/SVG chưa được hỗ trợ' in item
               for item in findings)
    assert libs.detect(html) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


@pytest.mark.parametrize('tag', ['style', 'textarea', 'title', 'xmp', 'iframe',
                                 'noembed', 'noframes', 'noscript'])
def test_comment_body_rule_does_not_parse_raw_or_rcdata(tag):
    html = f'<{tag}><!--a--b-->{REMOTE}</{tag}>' + LOCAL
    assert libs.assert_no_remote_code(html, strict=False) == []
    assert libs.detect(html) == ['gsap']


@pytest.mark.parametrize('comment', ['<!---->', '<!--a-b-->', '<!---x-->',
                                     '<!-- plain comment -->', '<!-- ' + REMOTE + ' -->',
                                     '<!--\nmultiple\nlines\n-->'])
def test_canonical_comments_remain_inert(comment):
    html = comment + '<template>' + comment + '</template>' + LOCAL
    assert libs.assert_no_remote_code(html, strict=False) == []
    assert libs.detect(html) == ['gsap']


def test_script_html_comment_marker_at_eof_is_not_silent():
    html = LOCAL + '<script><!--<script>'
    assert libs.assert_no_remote_code(html, strict=False)
    assert libs.detect(html) == []


def test_double_escaped_script_user_warning_keeps_explicit_lib(station, tmp_path, capsys):
    html = LOCAL + '<script><!--<script></script><base href="."></script><base href="https://example.invalid/">' + LOCAL
    autodetect = tmp_path / 'autodetect'
    assert libs.stage_detected(autodetect, html, keep_existing=True, station=station) == []
    assert not autodetect.exists()
    explicit = tmp_path / 'explicit'
    assert libs.stage_detected(explicit, html, keep_existing=True, station=station, names=['gsap']) == ['gsap.min.js']
    assert (explicit / 'gsap.min.js').read_bytes() == b'gsap'
    assert 'Cảnh báo cấu trúc HTML/SVG chưa được hỗ trợ' in capsys.readouterr().err


def test_double_escaped_script_template_fails_before_stage_or_index(tmp_path, monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError('stage must not run')
    monkeypatch.setattr(libs, 'stage', denied)
    project = tmp_path / 'new'
    with pytest.raises(ContractError, match='cấu trúc HTML/SVG chưa được hỗ trợ'):
        render.write_index(project, '<script><!--<script></script><template></script>' + REMOTE, libs=('gsap',))
    assert not project.exists()


@pytest.mark.parametrize('tag, false_closer', [
    ('script', 'ſcript'), ('script', 'scrıpt'), ('script', 'scrİpt'),
    ('style', 'ſtyle'), ('title', 'tıtle'), ('title', 'tİtle'),
    ('iframe', 'ıframe'), ('noscript', 'noſcript'), ('noframes', 'noframeſ'),
])
def test_unicode_casefold_does_not_close_html_raw_or_rcdata(tag, false_closer):
    html = f'<{tag}>text</{false_closer}><textarea></{tag}>' + REMOTE
    assert libs.assert_no_remote_code(html, strict=False)
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


@pytest.mark.parametrize('false_closer', ['ſcript', 'scrıpt', 'scrİpt'])
@pytest.mark.parametrize('trap', ['<base href=".">', '<!--'])
def test_unicode_raw_closer_cannot_supply_fake_base_or_comment(false_closer, trap):
    html = (f'<script>const t="</{false_closer}>' + trap + '";</script>'
            '<base href="https://example.invalid/">' + LOCAL + REMOTE + '-->')
    assert libs.assert_no_remote_code(html, strict=False)
    assert libs.detect(html) == []
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html)


@pytest.mark.parametrize('tag', ['script', 'style', 'title', 'textarea', 'iframe',
                                 'xmp', 'noembed', 'noframes', 'noscript'])
@pytest.mark.parametrize('closer_case', ['upper', 'mixed'])
def test_ascii_case_still_closes_raw_or_rcdata(tag, closer_case):
    closer = tag.upper() if closer_case == 'upper' else ''.join(
        ch.upper() if index % 2 else ch for index, ch in enumerate(tag))
    html = f'<{tag}>text</{closer}>' + LOCAL
    assert libs.assert_no_remote_code(html, strict=False) == []
    assert libs.detect(html) == ['gsap']
    with pytest.raises(ContractError):
        libs.assert_no_remote_code(html + REMOTE)
