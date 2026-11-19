#!/usr/bin/env python3
"""Đổi ranh hành chính / đường lấy từ OSM (extract_osm.mjs) thành đường SVG đúng toạ độ trên khung 1080x1920.

    python osm_overlay.py osm_overlays.json M02 20.95655 105.93502 14.5 b6 b4

Toạ độ là Web Mercator (cùng công thức với geo_cfg.py của skill land-plot-map-video), nên đường khớp ảnh nền chụp
bằng MapLibre/Esri ở CÙNG tâm + zoom (zoom tính theo ô 256 px; MapLibre dùng zoom-1). Chỉ đúng với ảnh top-down (pitch 0).
Lõi chỉ thư viện chuẩn. Nhập geo_cfg từ skill land-plot-map-video (cùng repo) hoặc đặt GEO_CFG_PATH.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920


def _geo():
    path = os.environ.get("GEO_CFG_PATH") or os.path.join(HERE, "..", "..", "land-plot-map-video", "assets", "geo_cfg.py")
    spec = importlib.util.spec_from_file_location("geo_cfg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def project_line(line, center, z, geo=None):
    """[[lon,lat],...] -> [[x,y],...] pixel trên khung (không cắt)."""
    geo = geo or _geo()
    return [geo.to_frame(lat, lon, center, z) for lon, lat in line]


def clip_visible(pts, margin=60):
    """Bỏ đoạn nằm hẳn ngoài khung (giữ lân cận `margin` px); trả các mảnh liên tục."""
    out, cur = [], []
    for x, y in pts:
        if -margin <= x <= W + margin and -margin <= y <= H + margin:
            cur.append((x, y))
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [c for c in out if len(c) > 1]


def simplify(pts, eps=0.7):
    """Bỏ điểm gần như thẳng hàng (Douglas-Peucker rút gọn) để SVG nhẹ."""
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = (dx * dx + dy * dy) ** 0.5 or 1e-9
    idx, dmax = 0, 0.0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            idx, dmax = i, d
    if dmax > eps:
        return simplify(pts[:idx + 1], eps)[:-1] + simplify(pts[idx:], eps)
    return [pts[0], pts[-1]]


def svg_paths(lines, center, z, geo=None, eps=0.7):
    """Danh sách chuỗi `d` của <path>, mỗi mảnh nhìn thấy một path (dùng pathLength=1 để vẽ dần)."""
    geo = geo or _geo()
    ds = []
    for ln in lines:
        for seg in clip_visible(project_line(ln, center, z, geo)):
            seg = simplify(seg, eps)
            ds.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in seg))
    return ds


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    if len(a) < 6:
        print(__doc__)
        return 2
    data = json.load(open(a[0], encoding="utf-8"))
    view, lat, lon, z = a[1], float(a[2]), float(a[3]), float(a[4])
    geo = _geo()
    out = {k: svg_paths(data[view][k], (lat, lon), z, geo) for k in a[5:]}
    print(json.dumps({k: len(v) for k, v in out.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
