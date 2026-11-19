"""Hợp đồng GSAP cục bộ cho template bản tin và seed."""
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "video_studio/templates/news/news_video.py": 3,
    "video_studio/templates/news/news_v2.py": 2,
    "video_studio/templates/news/top_story_video.py": 2,
    "templates/_seed/index.html": 1,
}


@pytest.mark.parametrize("relative, expected", SOURCES.items())
def test_templates_use_only_local_gsap(relative, expected):
    text = (ROOT / relative).read_text(encoding="utf-8")
    scripts = re.findall(r'<script\s+src=["\']([^"\']*gsap[^"\']*)["\']', text, re.I)
    assert scripts == ["gsap.min.js"] * expected, (relative, scripts)


def test_news_html_stages_gsap(news, monkeypatch, tmp_path):
    import hashlib
    import news_harness as harness
    from video_studio import render, runtime_libs

    original_write_index = render.write_index
    captured = harness.install(monkeypatch, news, tmp_path / "source")
    harness.weekly(news, [{"headline": "Tin", "narration": "Tin mới."}], tmp_path / "out.mp4")
    html = captured[-1]
    head = html.split("</head>", 1)[0]
    assert re.findall(r'<script\s+src=["\']([^"\']*gsap[^"\']*)["\']', head, re.I) == ["gsap.min.js"]

    lock = runtime_libs.load_lock()
    lock["libs"]["gsap"]["members"][0]["file_sha256"] = hashlib.sha256(b"test gsap").hexdigest()
    monkeypatch.setattr(runtime_libs, "load_lock", lambda path=None: lock)
    override = tmp_path / "gsap-source.js"
    override.write_bytes(b"test gsap")
    runtime_libs.set_overrides({"gsap": str(override)})
    try:
        project = tmp_path / "project"
        original_write_index(project, html, libs=("gsap",))
        assert (project / "gsap.min.js").read_bytes() == b"test gsap"
        assert '<script src="gsap.min.js"></script>' in (project / "index.html").read_text(encoding="utf-8")
    finally:
        runtime_libs.set_overrides({})


@pytest.mark.parametrize("project", ["news", "news-weekly", "topstory", "repo-today"])
def test_generated_head_has_one_local_gsap(project, news, monkeypatch, tmp_path):
    import importlib
    import news_harness as harness
    from video_studio import render

    family = importlib.import_module("video_studio.templates.news")
    topstory = importlib.import_module("video_studio.templates.news.top_story_video")
    v2 = importlib.import_module("video_studio.templates.news.news_v2")
    captured = harness.install(monkeypatch, news, tmp_path / "project", topstory)
    monkeypatch.setattr(topstory.av, "mux", lambda *args, **kwargs: None, raising=False)
    monkeypatch.setattr(family, "_voice", lambda spec: (None, None, harness.MODEL))
    monkeypatch.setattr(topstory, "_synth_section_beats", lambda *args: ([0] * 24000, 1, []))
    monkeypatch.setattr(topstory, "_voice_track", lambda *args: [])
    monkeypatch.setattr(v2, "_proj", lambda: str(tmp_path / "project"))
    monkeypatch.setattr(v2.engine, "load", lambda: harness.MODEL, raising=False)
    monkeypatch.setattr(v2, "_caption_blocks", lambda *args: ([0] * 24000, 1, []))

    spec = {"date": "2026-01-02", "brand": harness.MIN_BRAND,
            "outputs": {"long": True, "short": False},
            "segments": [{"headline": "Tin", "narration": "Tin mới."}],
            "top_story": {"headline": "Tin", "sections": [{"title": "Tin"}]},
            "scenes": [{"narration": "Tin mới.", "title": "Tin"}]}
    handler = {"news": family.render_daily, "news-weekly": family.render_weekly,
               "topstory": family.render_topstory, "repo-today": family.render_repo_today}[project]
    handler(spec, str(tmp_path / "out"))
    assert len(captured) == 1
    assert captured.libs == [("gsap",)]
    head = captured[0].split("</head>", 1)[0]
    scripts = re.findall(r'<script\s+src=["\']([^"\']*gsap[^"\']*)["\']', head, re.I)
    assert scripts == ["gsap.min.js"]


def test_all_six_news_writes_declare_gsap():
    import ast
    calls = []
    for name in ("news_video.py", "news_v2.py", "top_story_video.py"):
        tree = ast.parse((ROOT / "video_studio/templates/news" / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "write_index" and isinstance(node.func.value, ast.Name) and node.func.value.id == "render":
                calls.append(node)
                keyword = next((x for x in node.keywords if x.arg == "libs"), None)
                assert keyword and ast.literal_eval(keyword.value) == ("gsap",)
    assert len(calls) == 6
