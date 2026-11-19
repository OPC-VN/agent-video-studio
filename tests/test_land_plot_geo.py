"""geo_cfg.py của skill land-plot-map-video: toạ độ thật -> pixel/mét/CFG. Không cần mạng."""
import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "land-plot-map-video"
_spec = importlib.util.spec_from_file_location("geo_cfg", SKILL / "assets" / "geo_cfg.py")
geo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(geo)

LAT, LON = 21.0, 105.85  # điểm thử chung, không gắn địa danh thật

KML = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document>
<Placemark><name>lo-dat</name><Polygon><outerBoundaryIs><LinearRing><coordinates>
{LON-0.0003},{LAT-0.00018},0 {LON+0.0003},{LAT-0.00018},0 {LON+0.0003},{LAT+0.00018},0 {LON-0.0003},{LAT+0.00018},0 {LON-0.0003},{LAT-0.00018},0
</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>
<Placemark><name>trung-tam</name><Point><coordinates>{LON+0.004},{LAT+0.012},0</coordinates></Point></Placemark>
<Placemark><name>tien-ich-truong</name><Point><coordinates>{LON+0.001},{LAT+0.001},0</coordinates></Point></Placemark>
</Document></kml>"""


def test_center_maps_to_frame_center():
    assert geo.to_frame(LAT, LON, (LAT, LON), 18) == [540.0, 960.0]


def test_north_is_up_east_is_right():
    x, y = geo.to_frame(LAT + 0.001, LON + 0.001, (LAT, LON), 18)
    assert x > 540 and y < 960


def test_meters_per_pixel_matches_formula():
    # 156543.03392 * cos(lat) / 2^z
    assert geo.m_per_px(LAT, 19) == pytest.approx(156543.03392 * math.cos(math.radians(LAT)) / 2 ** 19, rel=1e-3)


def test_pixel_distance_equals_ground_distance():
    z = 17
    a = geo.to_frame(LAT, LON, (LAT, LON), z)
    b = geo.to_frame(LAT, LON + 0.002, (LAT, LON), z)
    px = b[0] - a[0]
    assert px * geo.m_per_px(LAT, z) == pytest.approx(geo.haversine_m((LAT, LON), (LAT, LON + 0.002)), rel=5e-3)


def test_haversine_one_degree_lat():
    assert geo.haversine_m((0, 0), (1, 0)) == pytest.approx(111195, rel=1e-3)


def test_parse_kml_rejects_doctype():
    with pytest.raises(ValueError):
        geo.parse_kml('<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "b">]><kml/>')


def test_parse_kml_rejects_out_of_range():
    bad = KML.replace(f"{LON+0.004},{LAT+0.012}", "300,10")
    with pytest.raises(ValueError):
        geo.parse_kml(bad)


def test_polygon_metrics_rectangle():
    site = geo.parse_kml(KML)
    m = geo.polygon_metrics(site["lo-dat"])
    # 0.0006° lon × 0.00036° lat ≈ 62.4 m × 40.0 m
    assert m["A_m"] == pytest.approx(62.4, abs=1.5) and m["B_m"] == pytest.approx(40.0, abs=1.5)
    assert m["area_m2"] == pytest.approx(m["A_m"] * m["B_m"], rel=0.02)


def test_build_projects_polygon_inside_frame_and_reports_warnings():
    cfg, plan, rep = geo.build(geo.parse_kml(KML), radius_m=500)
    for x, y in cfg["hook"]["poly"]:
        assert 0 <= x <= geo.W and 0 <= y <= geo.H
    assert "thiếu «ranh-xa»: cảnh `where` không vẽ ranh xã" in rep["warnings"]
    assert {i["file"] for i in plan["images"]} >= {"assets/plot.jpg", "assets/radius.jpg", "assets/city.jpg"}
    # bán kính pixel khớp mét thật
    z = rep["zoom"]["radius"]
    assert cfg["radius"]["r"] * geo.m_per_px(LAT, z) == pytest.approx(500, rel=0.03)
    # khoảng cách trong nhãn bằng số tính được
    shown = int(cfg["city"]["dist"].replace(".", "").replace("≈ ", "").replace(" m", ""))
    assert abs(shown - rep["dist_to_center_m_straight"]) <= 1


def test_build_requires_lot_and_center():
    site = geo.parse_kml(KML)
    del site["trung-tam"]
    with pytest.raises(ValueError):
        geo.build(site, 400)


def test_poi_outside_radius_warns():
    cfg, plan, rep = geo.build(geo.parse_kml(KML), radius_m=50)
    assert any("ngoài bán kính" in w for w in rep["warnings"])


def test_inject_replaces_markers_only():
    html = "a /*CFG-BEGIN*/ const CFG = {}; /*CFG-END*/ b"
    out = geo.inject(html, {"brand": "X</script>"})
    assert out.startswith("a ") and out.endswith(" b") and "</script>" not in out
    with pytest.raises(ValueError):
        geo.inject("no markers", {})


def test_template_has_markers_and_no_place_defaults():
    html = (SKILL / "assets" / "land-plot-template" / "index.html").read_text(encoding="utf-8")
    assert "/*CFG-BEGIN*/" in html and "/*CFG-END*/" in html
    assert "Bắc Giang" not in html


def test_cli_end_to_end(tmp_path):
    k = tmp_path / "s.kml"
    k.write_text(KML, encoding="utf-8")
    tpl = SKILL / "assets" / "land-plot-template" / "index.html"
    out = tmp_path / "o"
    assert geo.main([str(k), "--out", str(out), "--template", str(tpl), "--radius-m", "400"]) == 0
    assert json.loads((out / "cfg.json").read_text(encoding="utf-8"))["hook"]["poly"]
    assert "const CFG" in (out / "index.html").read_text(encoding="utf-8")
    assert geo.main([str(tmp_path / "none.kml"), "--out", str(out), "--radius-m", "400"]) == 2
