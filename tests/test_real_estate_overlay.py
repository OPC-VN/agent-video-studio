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


def test_water_outline_traces_lake_from_mask(tmp_path):
    import pytest
    pytest.importorskip("numpy")
    pytest.importorskip("scipy")
    from PIL import Image, ImageDraw
    spec = importlib.util.spec_from_file_location("water_outline", SK / "assets" / "water_outline.py")
    wo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wo)
    im = Image.new("L", (1080, 1920), 0)
    ImageDraw.Draw(im).ellipse([200, 300, 400, 500], fill=255)       # hồ cần lấy
    ImageDraw.Draw(im).ellipse([800, 1200, 860, 1260], fill=255)     # hồ khác, không được lẫn vào
    p = tmp_path / "w.png"
    im.save(p)
    pts, comp = wo.outline(str(p), (300, 400))
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    assert 195 <= min(xs) <= 205 and 395 <= max(xs) <= 405 and 295 <= min(ys) <= 305
    assert comp[1230, 830] == 0                                      # không lẫn hồ thứ hai
    assert wo.outline(str(p), (300, 240), max_gap=90) is not None     # seed sát hồ: lấy hồ gần nhất
    assert wo.outline(str(p), (600, 900), max_gap=90) is None        # seed xa mọi nước
    assert wo.to_svg_d(pts).startswith("M") and wo.to_svg_d(pts).endswith("Z")


def test_camera_path_examples_are_valid():
    """camera_paths.example.json: mỗi spec có khoá camera tăng dần theo t và z/lat/lon hợp lệ."""
    data = json.loads((SK / "assets" / "camera_paths.example.json").read_text(encoding="utf-8"))
    specs = {k: v for k, v in data.items() if not k.startswith("_")}
    assert len(specs) >= 6
    for name, sp in specs.items():
        ts = [k["t"] for k in sp["keys"]]
        assert ts == sorted(ts) and ts[0] == 0 and ts[-1] == sp["secs"], name
        for k in sp["keys"]:
            assert 0 < k["z"] <= 19 and -90 < k["lat"] < 90 and -180 < k["lon"] < 180 and 0 <= k["pitch"] <= 75, name
            assert 0 <= k["sat"] <= 1 and 0 <= k["rise"] <= 1, name


def test_template_has_no_infinite_repeat_or_pulsing_pin():
    html = (SK / "assets" / "draft2_template.html").read_text(encoding="utf-8")
    assert "repeat: -1" not in html and "repeat:-1" not in html
    pin = html[html.index('e.t === "pin"'):html.index('e.t === "dash"')]
    assert "repeat" not in pin   # ghim không còn vòng sóng lặp
