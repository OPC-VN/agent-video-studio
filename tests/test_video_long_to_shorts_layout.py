"""Kiểm gap_scan.py của skill video-long-to-shorts (chỉ thư viện chuẩn)."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "video-long-to-shorts" / "scripts" / "gap_scan.py"

spec = importlib.util.spec_from_file_location("vlts_gap_scan", SCRIPT)
gap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gap)


def el(id, t_in, t_out, cx=540, cy=800, w=420, **kw):
    return dict({"id": id, "asset": f"icons/{id}.svg", "t_in": t_in, "t_out": t_out, "cx": cx,
                 "cy": cy, "w": w, "h": w}, **kw)


def layout(elements, scenes=(), duration=10.0, skip=((0, 2.0),)):
    return {"frame": {"w": 1080, "h": 1920}, "duration": duration,
            "zone": {"y0": 200, "y1": 1500}, "skip": [list(s) for s in skip],
            "elements": list(elements), "scenes": list(scenes)}


def balanced():
    return [el("a", 2.0, 10.0, cy=520), el("b", 2.0, 10.0, cy=1180)]


def test_balanced_vertical_stack_passes(tmp_path):
    result = gap.check(layout(balanced()))
    assert result["ok"] and result["warnings"] == [] and result["errors"] == []
    f = tmp_path / "layout.json"
    f.write_text(json.dumps(layout(balanced())), encoding="utf-8")
    assert gap.main([str(f)]) == 0


def test_empty_stretch_longer_than_max_gap_is_error(tmp_path):
    data = layout([el("a", 2.0, 5.0, cy=520), el("b", 2.0, 5.0, cy=1180),
                   el("c", 7.0, 10.0, cy=520), el("d", 7.0, 10.0, cy=1180)])
    result = gap.check(data)
    assert not result["ok"] and "5–6.5 s" in result["errors"][0]
    f = tmp_path / "layout.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    assert gap.main([str(f), "--json"]) == 1
    assert gap.check(data, max_gap=2.0)["ok"], "khoảng hở 2 s lọt khi nới ngưỡng"


def test_small_corner_icons_do_not_count_as_filled():
    data = layout([el("tiny", 2.0, 10.0, cx=900, cy=300, w=160)])
    assert any("trống" in e for e in gap.check(data)["errors"])


def test_same_asset_twice_in_one_frame_is_error_unless_allowed():
    twins = [el("a", 2.0, 10.0, cy=520), dict(el("b", 2.0, 10.0, cy=1180), asset="icons/a.svg")]
    result = gap.check(layout(twins))
    assert any("lặp cùng asset" in e for e in result["errors"])
    twins[1]["allow_repeat"] = True
    assert gap.check(layout(twins))["ok"]


def test_embedded_media_frame_must_not_keep_other_icons():
    data = layout([el("clip", 2.0, 10.0, cy=760, w=960, role="media"),
                   el("a", 4.0, 6.0, cx=880, cy=1350, w=180)])
    result = gap.check(data)
    assert any("media lồng" in e and "4–5.5 s" in e for e in result["errors"])
    alone = layout([el("clip", 2.0, 10.0, cy=760, w=960, role="media"),
                    el("host", 2.0, 10.0, cx=200, cy=1400, w=300, role="avatar")])
    assert gap.check(alone)["ok"], "avatar và phụ đề được ở cùng media"


def test_top_heavy_and_one_sided_layouts_warn():
    top = gap.check(layout([el("a", 2.0, 10.0, cy=420, w=320)]))
    assert top["ok"] and any("có trên thiếu dưới" in w for w in top["warnings"])
    side = gap.check(layout([el("a", 2.0, 10.0, cx=300, cy=520), el("b", 2.0, 10.0, cx=300, cy=1180)]))
    assert any("dồn một bên" in w for w in side["warnings"])
    with_host = layout([el("a", 2.0, 10.0, cx=760, cy=520), el("b", 2.0, 10.0, cx=760, cy=1100),
                        el("host", 2.0, 10.0, cx=220, cy=1360, w=300, role="avatar")])
    assert not any("dồn một bên" in w for w in gap.check(with_host)["warnings"])


def test_motion_repeated_three_scenes_in_a_row_is_error():
    scenes = [{"id": f"C{i}", "t_in": i, "t_out": i + 1, "layout": lay, "motion": mo}
              for i, (lay, mo) in enumerate([("V1", "flow"), ("V2", "flow"), ("V3", "flow"),
                                             ("V4", "orbit")])]
    result = gap.check(layout(balanced(), scenes))
    assert any("3 cảnh liền cùng kiểu chuyển động 'flow'" in e for e in result["errors"])
    scenes[2]["motion"] = "assemble"
    for s in scenes[:3]:
        s["layout"] = "V1"
    result = gap.check(layout(balanced(), scenes))
    assert result["ok"] and any("cùng bố cục 'V1'" in w for w in result["warnings"])


def test_unreadable_layout_is_usage_error(tmp_path):
    bad = tmp_path / "layout.json"
    bad.write_text('{"elements": [{"id": "a"}], "duration": 5}', encoding="utf-8")
    assert gap.main([str(bad)]) == 2
    assert gap.main([str(tmp_path / "none.json")]) == 2
