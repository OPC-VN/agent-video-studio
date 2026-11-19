#!/usr/bin/env python3
"""Toạ độ thật -> CFG của template land-plot (skill land-plot-map-video).

Nguyên tắc: toạ độ (lat/lon) là nguồn sự thật; pixel được TÍNH RA bằng Web Mercator.
Chỉ dùng thư viện chuẩn, không mạng. Dùng:

    python geo_cfg.py site.kml --out DIR [--template index.html] [--radius-m 400] [--copy copy.json]

Ghi vào DIR: capture-plan.json (ảnh nào, tâm, zoom, kích thước), cfg.json (CFG đã chiếu),
report.json (số đo tính được + cảnh báo) và index.html (nếu có --template, đã chèn CFG).

Quy ước tên Placemark trong KML:
    lo-dat        Polygon   ranh lô đất (bắt buộc)
    trung-tam     Point     điểm trung tâm thành phố/địa danh đích (bắt buộc)
    tien-ich-*    Point     tiện ích (tien-ich-truong, tien-ich-y-te, tien-ich-cho -> book/cross/star)
    ranh-xa       Polygon   ranh xã (tuỳ chọn)
    ranh-tinh     Polygon   ranh tỉnh (tuỳ chọn)
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

W, H = 1080, 1920
TILE = 256
EARTH_R = 6371008.8  # m, bán kính trung bình: haversine và mét cục bộ
MERC_R = 6378137.0  # m, bán kính Web Mercator: mét/pixel


# ---------------------------------------------------------------- KML
def parse_kml(text: str) -> dict:
    """KML -> {'lo-dat': [(lon,lat)...], ...}. Từ chối DOCTYPE/ENTITY (không tin tệp ngoài)."""
    if re.search(r"<!\s*(DOCTYPE|ENTITY)", text, re.I):
        raise ValueError("KML có DOCTYPE/ENTITY: bị từ chối")
    root = ET.fromstring(text)
    out: dict = {}
    for pm in root.iter():
        if not pm.tag.endswith("Placemark"):
            continue
        name = ""
        coords = None
        for el in pm.iter():
            tag = el.tag.split("}")[-1]
            if tag == "name" and el.text:
                name = el.text.strip().lower()
            elif tag == "coordinates" and el.text and coords is None:
                coords = el.text
        if not name or coords is None:
            continue
        pts = []
        for tok in coords.split():
            parts = tok.split(",")
            if len(parts) < 2:
                raise ValueError(f"toạ độ lỗi ở «{name}»: {tok!r}")
            lon, lat = float(parts[0]), float(parts[1])
            if not (-180 <= lon <= 180 and -85.05 <= lat <= 85.05):
                raise ValueError(f"toạ độ ngoài miền ở «{name}»: {tok!r}")
            pts.append((lon, lat))
        if len(pts) > 1 and pts[0] == pts[-1]:
            pts = pts[:-1]  # bỏ điểm đóng
        out[name] = pts
    return out


# ---------------------------------------------------------------- chiếu
def world_px(lat: float, lon: float, z: float) -> tuple[float, float]:
    s = TILE * (2.0 ** z)
    x = s * (lon + 180.0) / 360.0
    siny = math.sin(math.radians(lat))
    y = s * (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi))
    return x, y


def to_frame(lat: float, lon: float, center: tuple[float, float], z: float) -> list[float]:
    """(lat,lon) -> pixel trên khung W×H có tâm = center (lat,lon) ở zoom z."""
    cx, cy = world_px(center[0], center[1], z)
    x, y = world_px(lat, lon, z)
    return [round(x - cx + W / 2, 1), round(y - cy + H / 2, 1)]


def m_per_px(lat: float, z: float) -> float:
    return 2 * math.pi * MERC_R * math.cos(math.radians(lat)) / (TILE * 2.0 ** z)


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * EARTH_R * math.asin(math.sqrt(h))


def centroid(poly_lonlat: list) -> tuple[float, float]:
    """Trọng tâm đơn giản (lat, lon) theo trung bình đỉnh; đủ cho lô nhỏ."""
    return (sum(p[1] for p in poly_lonlat) / len(poly_lonlat), sum(p[0] for p in poly_lonlat) / len(poly_lonlat))


def _local_m(poly_lonlat: list, ref: tuple[float, float]) -> list[tuple[float, float]]:
    k = math.cos(math.radians(ref[0]))
    return [((lo - ref[1]) * math.radians(1) * EARTH_R * k, (la - ref[0]) * math.radians(1) * EARTH_R)
            for lo, la in poly_lonlat]


def polygon_metrics(poly_lonlat: list) -> dict:
    """Diện tích (m²) và hình chữ nhật bao nhỏ nhất A×B (m), tính phẳng cục bộ."""
    ref = centroid(poly_lonlat)
    pts = _local_m(poly_lonlat, ref)
    area = 0.0
    for i, (x1, y1) in enumerate(pts):
        x2, y2 = pts[(i + 1) % len(pts)]
        area += x1 * y2 - x2 * y1
    area = abs(area) / 2
    best = None
    for i, (x1, y1) in enumerate(pts):
        x2, y2 = pts[(i + 1) % len(pts)]
        ang = math.atan2(y2 - y1, x2 - x1)
        c, s = math.cos(-ang), math.sin(-ang)
        rx = [p[0] * c - p[1] * s for p in pts]
        ry = [p[0] * s + p[1] * c for p in pts]
        a, b = max(rx) - min(rx), max(ry) - min(ry)
        if best is None or a * b < best[0] * best[1]:
            best = (a, b)
    a, b = sorted(best, reverse=True)
    return {"area_m2": round(area, 1), "A_m": round(a, 1), "B_m": round(b, 1)}


def fit_zoom(points_lonlat: list, center: tuple[float, float], frac_w: float, frac_h: float,
             zmin: float = 3, zmax: float = 20) -> float:
    """Zoom lớn nhất để mọi điểm nằm trong frac_w×W và frac_h×H quanh tâm."""
    z = zmax
    while z > zmin:
        ok = True
        for lo, la in points_lonlat:
            x, y = to_frame(la, lo, center, z)
            if abs(x - W / 2) > frac_w * W / 2 or abs(y - H / 2) > frac_h * H / 2:
                ok = False
                break
        if ok:
            return round(z, 2)
        z = round(z - 0.05, 2)
    return zmin


# ---------------------------------------------------------------- CFG
ICONS = {"truong": "book", "y-te": "cross", "cho": "star"}
DEFAULT_COPY = {
    "brand": "TÊN KÊNH",
    "line1": "Trực quan, sinh động",
    "line2": "và [thuyết phục khách hàng]",
    "say": "TÔI CÓ THỂ GIÚP BẠN\nLÀM ĐIỀU ĐÓ",
    "intro": "Đầu tiên là phần\ngiới thiệu tổng quát",
    "pin_label": "Vị trí lô đất",
    "commune_label": "Xã nào ?",
    "province_label": "Tỉnh nào ?",
    "city_label": "Trung tâm",
    "radius_label": "Bán kính",
    "cta1": "Nếu bạn đang cần",
    "cta2": "[1 video] như vậy",
    "cta_sub": "Liên hệ ngay",
}
TIMES = {"hook": (0, 7.17), "intro": (7.17, 9.57), "where": (9.57, 14.63), "size": (14.63, 20.9),
         "city": (20.9, 22.2), "radius": (22.2, 27.97), "cta": (27.97, 30.8)}  # đo từ video mẫu bằng rea-video (rhythm.md)


def build(site: dict, radius_m: float, copy: dict | None = None) -> tuple[dict, dict, dict]:
    """-> (cfg, capture_plan, report). Raise ValueError nếu thiếu dữ liệu bắt buộc."""
    c = dict(DEFAULT_COPY, **(copy or {}))
    for need in ("lo-dat", "trung-tam"):
        if need not in site:
            raise ValueError(f"KML thiếu Placemark «{need}»")
    lot = site["lo-dat"]
    if len(lot) < 3:
        raise ValueError("«lo-dat» phải là polygon ≥ 3 đỉnh")
    city = site["trung-tam"][0]
    cen = centroid(lot)
    warns: list[str] = []
    met = polygon_metrics(lot)
    dist = haversine_m(cen, (city[1], city[0]))

    z_plot = min(19.5, fit_zoom(lot, cen, 0.62, 0.42))
    z_intro = round(z_plot - 2.0, 2)
    z_cta = round(z_plot - 1.0, 2)
    plan: list[dict] = []

    def img(name, center, z):
        plan.append({"file": f"assets/{name}.jpg", "lat": round(center[0], 7), "lon": round(center[1], 7),
                     "zoom": z, "width": W, "height": H,
                     "m_per_px": round(m_per_px(center[0], z), 4)})

    img("plot", cen, z_plot)
    img("area", cen, z_intro)
    img("cta", cen, z_cta)
    lot_px = [to_frame(la, lo, cen, z_plot) for lo, la in lot]

    # where: tâm lô, zoom vừa ranh tỉnh (nếu có) hoặc xã, không thì mặc định 13
    outer = site.get("ranh-tinh") or site.get("ranh-xa")
    if site.get("ranh-xa") is None:
        warns.append("thiếu «ranh-xa»: cảnh `where` không vẽ ranh xã")
    if site.get("ranh-tinh") is None:
        warns.append("thiếu «ranh-tinh»: cảnh `where` không vẽ ranh tỉnh")
    z_where = fit_zoom(outer, cen, 0.9, 0.8) if outer else 13.0
    img("region", cen, z_where)
    commune = site.get("ranh-xa")
    province = site.get("ranh-tinh")

    # city: tâm = giữa lô và trung tâm
    mid = ((cen[0] + city[1]) / 2, (cen[1] + city[0]) / 2)
    z_city = fit_zoom([(cen[1], cen[0]), city], mid, 0.7, 0.7)
    img("city", mid, z_city)

    # radius: vòng tròn đường kính ≈ 0.8 W, bán kính tính từ mét thật
    r_px_target = 0.4 * W
    z_rad = round(math.log2(2 * math.pi * MERC_R * math.cos(math.radians(cen[0])) * r_px_target
                            / (TILE * radius_m)), 2)
    img("radius", cen, z_rad)
    r_px = radius_m / m_per_px(cen[0], z_rad)

    pois = []
    for name, pts in sorted(site.items()):
        if name.startswith("tien-ich") and pts:
            key = name.replace("tien-ich-", "", 1)
            px = to_frame(pts[0][1], pts[0][0], cen, z_rad)
            inside = math.hypot(px[0] - W / 2, px[1] - H / 2) <= r_px
            if not inside:
                warns.append(f"«{name}» nằm ngoài bán kính {radius_m:g} m")
            pois.append([px[0], px[1], ICONS.get(key, "dot")])
    if not pois:
        warns.append("không có «tien-ich-*»: cảnh `radius` không có ghim tiện ích")

    def box(key, z):  # thời gian + nền
        t0, t1 = TIMES[key]
        return {"t0": t0, "t1": t1}

    cfg = {
        "brand": c["brand"], "person": "assets/person.png",
        "hook": {**box("hook", 0), "bg": "assets/plot.jpg", "poly": lot_px, "line1": c["line1"], "line2": c["line2"],
                 "say": c["say"], "sayAt": 5.6},
        "intro": {**box("intro", 0), "bg": "assets/area.jpg", "text": c["intro"]},
        "where": {**box("where", 0), "bg": "assets/region.jpg",
                  "pin": to_frame(cen[0], cen[1], cen, z_where), "pinLabel": c["pin_label"],
                  "commune": None, "province": None},
        "size": {**box("size", 0), "bg": "assets/plot.jpg", "poly": lot_px,
                 "label": f"{round(met['A_m'])}×{round(met['B_m'])} m"},
        "city": {**box("city", 0), "bg": "assets/city.jpg",
                 "from": to_frame(cen[0], cen[1], mid, z_city), "to": to_frame(city[1], city[0], mid, z_city),
                 "label": c["city_label"], "dist": f"≈ {round(dist):,} m".replace(",", ".")},
        "radius": {**box("radius", 0), "bg": "assets/radius.jpg", "pin": [W / 2, H / 2], "r": round(r_px, 1),
                   "label": f"{c['radius_label']} {radius_m:g} m", "pois": pois},
        "cta": {**box("cta", 0), "bg": "assets/cta.jpg", "line1": c["cta1"], "line2": c["cta2"], "sub": c["cta_sub"]},
    }
    for key, poly, lab, rot in (("commune", commune, c["commune_label"], 38), ("province", province, c["province_label"], -12)):
        if poly:
            px = [to_frame(la, lo, cen, z_where) for lo, la in poly]
            at = [round(sum(p[0] for p in px) / len(px), 1), round(sum(p[1] for p in px) / len(px) + 120, 1)]
            cfg["where"][key] = {"poly": px, "label": lab, "at": at, "rot": rot}
    # nếu thiếu ranh: dùng đa giác rỗng bị bỏ ở template? -> thay bằng hộp nhỏ quanh ghim để template không vỡ
    for key in ("commune", "province"):
        if cfg["where"][key] is None:
            cfg["where"][key] = {"poly": [], "label": "", "at": [W / 2, H / 2], "rot": 0}

    report = {"centroid_lat_lon": [round(cen[0], 7), round(cen[1], 7)], **met,
              "dist_to_center_m_straight": round(dist, 1), "radius_m": radius_m,
              "zoom": {"plot": z_plot, "area": z_intro, "region": z_where, "city": z_city, "radius": z_rad, "cta": z_cta},
              "warnings": warns,
              "note": "khoảng cách là đường chim bay; vùng 5 phút là vòng tròn mét, chưa phải isochrone theo đường"}
    return cfg, {"images": plan, "projection": "web-mercator, tâm ảnh = (lat,lon), zoom fractional, 256px/tile@z0"}, report


# ---------------------------------------------------------------- inject
CFG_RE = re.compile(r"/\*CFG-BEGIN\*/.*?/\*CFG-END\*/", re.S)


def inject(template_html: str, cfg: dict) -> str:
    if not CFG_RE.search(template_html):
        raise ValueError("template thiếu cặp marker /*CFG-BEGIN*/ … /*CFG-END*/")
    body = ",\n".join("  " + json.dumps(k) + ": " + json.dumps(v, ensure_ascii=False, separators=(",", ":"))
                      for k, v in cfg.items()).replace("</", "<\\/")
    js = "/*CFG-BEGIN*/ const CFG = {\n" + body + "\n}; /*CFG-END*/"
    return CFG_RE.sub(lambda _m: js, template_html, count=1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kml")
    ap.add_argument("--out", required=True)
    ap.add_argument("--template")
    ap.add_argument("--radius-m", type=float, required=True, help="bán kính vùng 5 phút, mét (do người dùng cấp)")
    ap.add_argument("--copy", help="JSON ghi đè chữ hiển thị")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252, nhãn tiếng Việt sẽ lỗi
    except (AttributeError, OSError):
        pass
    try:
        site = parse_kml(Path(a.kml).read_text(encoding="utf-8"))
        copy = json.loads(Path(a.copy).read_text(encoding="utf-8")) if a.copy else None
        cfg, plan, report = build(site, a.radius_m, copy)
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        for name, obj in (("cfg.json", cfg), ("capture-plan.json", plan), ("report.json", report)):
            (out / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        if a.template:
            (out / "index.html").write_text(inject(Path(a.template).read_text(encoding="utf-8"), cfg), encoding="utf-8")
    except (ValueError, OSError, ET.ParseError) as e:
        print(f"[geo_cfg] LỖI: {e}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
