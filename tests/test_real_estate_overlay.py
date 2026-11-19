"""osm_overlay.py + script portable của skill real-estate-location-video. Không cần mạng."""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / "skills" / "real-estate-location-video"
_spec = importlib.util.spec_from_file_location("osm_overlay", SK / "assets" / "osm_overlay.py")
ov = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ov)

C = (20.95, 105.93)


def test_center_projects_to_frame_center():
    pts = ov.project_line([[C[1], C[0]]], C, 15)
    assert pts == [[540.0, 960.0]]


def test_clip_drops_far_segments_and_keeps_visible():
    far = [(5000, 5000), (5100, 5100)]
    near = [(10, 10), (200, 300), (400, 500)]
    assert ov.clip_visible(far) == []
    assert ov.clip_visible(near) == [near]


def test_simplify_removes_collinear_points():
    pts = [(0, 0), (50, 0.2), (100, 0), (150, 0.1), (200, 0)]
    assert len(ov.simplify(pts, eps=1.0)) == 2


def test_svg_paths_one_path_per_visible_piece():
    line = [[C[1] + i * 0.0005, C[0]] for i in range(5)]
    ds = ov.svg_paths([line], C, 16)
    assert len(ds) == 1 and ds[0].startswith("M")


def test_scripts_portable_no_machine_paths():
    for f in (SK / "assets").glob("*"):
        if f.suffix in {".mjs", ".py", ".json", ".html"}:
            t = f.read_text(encoding="utf-8")
            assert not re.search(r"[A-Za-z]:[/\\]Users[/\\]", t), f"{f.name} còn đường dẫn máy"
            assert "puppeteer/chrome/win64-" not in t


def test_skill_files_exist():
    for n in ("SKILL.md", "references/setup.md", "references/effects-recipes.md", "references/workflow.md"):
        assert (SK / n).is_file(), n
    head = (SK / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    assert "name: real-estate-location-video" in head
