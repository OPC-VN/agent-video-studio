from pathlib import Path
import base64
from PIL import Image
import tempfile
import unittest
from unittest.mock import patch

from video_studio.contract import ContractError
from video_studio.runtime_libs import assert_no_remote_code
from video_studio.templates.news import top_story_video as top


def scene(title="Scene"):
    return {
        "title": title,
        "media": [{"type": "image", "src": "photo.png"}],
        "diagram": {"items": [{"t": "Find", "icon": "search"}, {"t": "Check", "icon": "check"}]},
    }


class TopStoryImageRightTests(unittest.TestCase):
    def setUp(self):
        self.story = {"visual_layout": "image-right", "cover_visual": scene("Open"),
                      "sections": [scene()], "outro_visual": scene("Close")}

    def test_both_aspects_put_steps_below_title_and_image_in_own_column(self):
        blocks = [{"kind": kind, "dur": 4, "beats": None} for kind in ("intro", "sec", "outro")]
        brand = {"a": "Example", "b": "News", "site": "example.org", "kicker": ""}
        with patch.object(top, "BRAND", brand), patch.object(
                top, "_prep_media", return_value=[{"kind": "image", "src": "media/photo.png"}]):
            for head, tag in [(top._LONG_HEAD, "L"), (top._SHORT_HEAD, "S")]:
                with self.subTest(tag=tag):
                    body = top._build(self.story, blocks, 12, head, ".", tag)
                    assert_no_remote_code(body)
                    self.assertEqual(body.count('class="seg split-story"'), 3)
                    self.assertEqual(body.count('class="split-image"'), 3)
                    self.assertIn('class="split-title">Scene</h2><ol class="split-steps">', body)
                    self.assertIn(f'm.fromTo("#{tag}split-1-step1"', body)
                    self.assertNotIn("<video", body)

    def test_all_aspects_use_the_configured_mark_and_clear_between_brands(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(top, "BRAND", {}):
            logo = Path(tmp) / "logo.png"
            Image.new("RGB", (2, 2), "#4db9db").save(logo)
            packed = base64.b64encode(logo.read_bytes()).decode("ascii")
            top._apply_branding({"a": "Example", "b": "News", "site": "example.org", "logo": str(logo)})
            for head, tag in [(top._LONG_HEAD, "L"), (top._SHORT_HEAD, "S")]:
                body = top._build({}, [], 2, head, tmp, tag)
                self.assertIn(f'<span class="mark"><img src="data:image/png;base64,{packed}"', body)
            top._apply_branding({"a": "Next", "b": "News", "site": "example.org"})
            self.assertEqual(top._logo_markup(tmp), "")

    def test_configured_missing_logo_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(top, "BRAND", {"logo": "missing.png"}):
            with self.assertRaisesRegex(ContractError, "brand.logo"):
                top._logo_markup(tmp)

    def test_rejects_non_image_bytes_as_logo(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(top, "BRAND", {"logo": "logo.png"}):
            (Path(tmp) / "logo.png").write_text("not an image", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "brand.logo"):
                top._logo_markup(tmp)

    def test_rejects_clip_in_the_still_image_column(self):
        self.story["sections"][0]["media"] = [{"type": "video", "src": "motion.mp4"}]
        with self.assertRaisesRegex(ContractError, "exactly one local still image"):
            top._split_scenes(self.story)

    def test_rejects_missing_local_image_before_render(self):
        with tempfile.TemporaryDirectory() as path:
            with self.assertRaisesRegex(ContractError, "missing local image"):
                top._validated_scenes(self.story, [], str(Path(path)))

    def test_rejects_unrecognized_icon(self):
        self.story["cover_visual"]["diagram"]["items"][0]["icon"] = "unknown"
        with self.assertRaisesRegex(ContractError, "supported icons"):
            top._split_scenes(self.story)
