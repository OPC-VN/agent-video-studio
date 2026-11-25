import base64
import importlib
from pathlib import Path

from PIL import Image
import pytest

from video_studio.contract import ContractError
from video_studio.runtime_libs import assert_no_remote_code


def scene(title="Scene"):
    return {
        "title": title,
        "media": [{"type": "image", "src": "photo.png"}],
        "diagram": {"items": [{"t": "Find", "icon": "search"}, {"t": "Check", "icon": "check"}]},
    }


@pytest.fixture
def top(news, monkeypatch):
    module = importlib.import_module("video_studio.templates.news.top_story_video")
    monkeypatch.setattr(module, "BRAND", {"a": "Example", "b": "News", "site": "example.org", "kicker": ""})
    return module


@pytest.fixture
def story():
    return {"visual_layout": "image-right", "cover_visual": scene("Open"),
            "sections": [scene()], "outro_visual": scene("Close")}


@pytest.mark.parametrize("tag,head", [("L", "_LONG_HEAD"), ("S", "_SHORT_HEAD")])
def test_both_aspects_put_steps_below_title_and_image_in_own_column(top, story, monkeypatch, tag, head):
    blocks = [{"kind": kind, "dur": 4, "beats": None} for kind in ("intro", "sec", "outro")]
    monkeypatch.setattr(top, "_prep_media", lambda *args, **kwargs: [{"kind": "image", "src": "media/photo.png"}])
    body = top._build(story, blocks, 12, getattr(top, head), ".", tag)
    assert_no_remote_code(body)
    assert body.count('class="seg split-story"') == 3
    assert body.count('class="split-image"') == 3
    assert 'class="split-title">Scene</h2><ol class="split-steps">' in body
    assert f'm.fromTo("#{tag}split-1-step1"' in body
    assert "<video" not in body


def test_all_aspects_use_the_configured_mark_and_clear_between_brands(top, tmp_path):
    logo = tmp_path / "logo.png"
    Image.new("RGB", (2, 2), "#4db9db").save(logo)
    packed = base64.b64encode(logo.read_bytes()).decode("ascii")
    top._apply_branding({"a": "Example", "b": "News", "site": "example.org", "logo": str(logo)})
    for head, tag in [(top._LONG_HEAD, "L"), (top._SHORT_HEAD, "S")]:
        body = top._build({}, [], 2, head, str(tmp_path), tag)
        assert f'<span class="mark"><img src="data:image/png;base64,{packed}"' in body
    top._apply_branding({"a": "Next", "b": "News", "site": "example.org"})
    assert top._logo_markup(str(tmp_path)) == ""


@pytest.mark.parametrize("exists", [False, True])
def test_configured_invalid_logo_is_an_error(top, tmp_path, exists):
    top.BRAND["logo"] = "logo.png"
    if exists:
        (tmp_path / "logo.png").write_text("not an image", encoding="utf-8", newline="\n")
    with pytest.raises(ContractError, match="brand.logo"):
        top._logo_markup(str(tmp_path))


def test_rejects_clip_in_the_still_image_column(top, story):
    story["sections"][0]["media"] = [{"type": "video", "src": "motion.mp4"}]
    with pytest.raises(ContractError, match="exactly one local still image"):
        top._split_scenes(story)


def test_rejects_missing_local_image_before_render(top, story, tmp_path):
    with pytest.raises(ContractError, match="missing local image"):
        top._validated_scenes(story, [], str(Path(tmp_path)))


def test_rejects_unrecognized_icon(top, story):
    story["cover_visual"]["diagram"]["items"][0]["icon"] = "unknown"
    with pytest.raises(ContractError, match="supported icons"):
        top._split_scenes(story)
