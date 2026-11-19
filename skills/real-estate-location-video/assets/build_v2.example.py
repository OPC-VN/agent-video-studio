#!/usr/bin/env python3
"""VÍ DỤ bản v2 (nhịp chậm 76 s, theo references/pacing-and-clarity.md): ảnh/clip raw + lớp phủ chiếu từ toạ độ thật.
Hiệu ứng mới: viền hồ (poly), vòng bán kính (ring), biểu tượng nhóm (icon), hộp số giữa đường nối (numbox),
chú giải (legend), tên đường (rlabel), mũi tên, màn tối (veil). Ghi comp3/. Sao chép vào <project>/tools/ rồi sửa PROJ/POI/VIEWS/SCENES/FX.
Cần raw/osm_overlays.json + osm_v2.json (extract_osm.mjs) và mặt nạ nước N01w.png (maplibre_shots.mjs, mode mask-water)."""
import json
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)
RAW = os.path.join(P, "raw")
OUT = os.path.join(P, "comp3")
SK = os.environ.get("SKILLS_DIR") or os.path.normpath(os.path.join(HERE, "..", ".."))  # thư mục skills/ của repo
sys.path.insert(0, os.path.join(SK, "land-plot-map-video", "assets"))
sys.path.insert(0, os.path.join(SK, "real-estate-location-video", "assets"))
import geo_cfg as G          # noqa: E402
import osm_overlay as OV     # noqa: E402
import water_outline as WO   # noqa: E402
from PIL import Image        # noqa: E402

PROJ = (20.95374525, 105.93237025)
HK = (21.0285, 105.8523)
POI = {  # id: (nhãn, lat, lng, km chim bay; được kiểm lại bằng haversine bên dưới)
    "cv": ("Công viên Hồ Thiên Nga", 20.9558497, 105.9327031, 0.24),
    "ku": ("BV Kusumi", 20.9635633, 105.9326817, 1.09),
    "buv": ("ĐH Anh Quốc (BUV)", 20.9653857, 105.9315862, 1.30),
    "oc": ("Vincom Ocean City", 20.951753, 105.9736312, 4.29),
    "tt": ("Cầu Thanh Trì", 20.9945609, 105.9025736, 5.49),
    "hk": ("Hồ Hoàn Kiếm", HK[0], HK[1], 11.76),
}


def hav(a, b):
    r = 6371.0088
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


for k, (nm, la, lo, km) in POI.items():  # số trên màn hình phải khớp haversine ±3 %
    assert abs(hav(PROJ, (la, lo)) - km) / km < 0.03, (k, hav(PROJ, (la, lo)), km)


def kmtxt(km):
    return f"{km:.2f}".replace(".", ",") + " km"


VIEWS = {
    "M01": (20.62, 106.27, 10.8), "M02": (20.95655, 105.93502, 14.5), "M03": (20.9738, 105.9530, 14.4),
    "N00": (20.78, 106.12, 10.8), "N06": (20.9528, 105.953, 14.2),
    "N01": (20.960, 105.9325, 15.6), "N05": (PROJ[0], PROJ[1], 15.0), "N03": (20.974, 105.9175, 12.9), "N04": (20.991, 105.892, 12.5),
}
OSM = json.load(open(os.path.join(RAW, "osm_overlays.json"), encoding="utf-8"))
OSM2 = json.load(open(os.path.join(RAW, "osm_v2.json"), encoding="utf-8"))
OSM["N00"] = json.load(open(os.path.join(RAW, "osm_n00.json"), encoding="utf-8"))["N00"]
ML2 = "maplibre2/"
E1, E2 = "earth-clean/", "earth-clean2/"

# (id, loại, nguồn, bắt đầu, độ dài, chuyển động, nhòe vào)   loại: g = nhóm ảnh+lớp phủ (MapLibre), img, video, layer
SCENES = [
    ("S01", "video", "cut/C_S01.mp4", 0.0, 1.0, None, False),
    ("S16", "video", "cut/C_S16_slow.mp4", 1.0, 5.0, None, True),
    ("S02", "g", ML2 + "N00.png", 6.0, 12.4, (1.00, 1.05), True),
    ("S03", "g", "maplibre/M02.png", 18.4, 5.6, (1.00, 1.05), True),
    ("S06a", "img", E1 + "R08.png", 24.0, 1.7, (1.00, 1.05), True),
    ("S06b", "img", E1 + "R09.png", 25.7, 1.7, (1.00, 1.05), True),
    ("S06c", "img", E1 + "R10.png", 27.4, 1.7, (1.00, 1.05), True),
    ("S07", "img", E2 + "R11.png", 29.1, 4.4, (1.00, 1.08), True),
    ("S08", "g", ML2 + "N01.png", 33.5, 7.0, (1.00, 1.04), True),
    ("S10", "video", "cut/C_3D_slow.mp4", 40.5, 6.0, None, True),
    ("S09", "g", ML2 + "N06.png", 46.5, 5.2, (1.00, 1.04), True),
    ("S14", "g", ML2 + "N05.png", 51.7, 7.5, (1.00, 1.03), True),
    ("S11", "g", ML2 + "N03.png", 59.2, 6.8, (1.00, 1.03), True),
    ("S19", "g", ML2 + "N04.png", 66.0, 5.3, (1.00, 1.03), True),
    ("S26a", "img", E1 + "R11b.png", 71.3, 2.5, (1.00, 1.08), True),
    ("S26b", "img", E2 + "R21.png", 73.8, 2.5, (1.08, 1.00), False),
    ("S26L", "layer", None, 71.3, 5.0, None, False),
]
TOTAL = 76.3
T0 = {s[0]: s[3] for s in SCENES}
FX = []


def pt(view, lat, lng):
    la, lo, z = VIEWS[view]
    x, y = G.to_frame(lat, lng, (la, lo), z)
    return round(x, 1), round(y, 1)


def mpp(view):  # mét/pixel tại vĩ độ dự án
    return 156543.03 * math.cos(math.radians(PROJ[0])) / 2 ** VIEWS[view][2]


SRC_Y = 1520  # dòng nguồn: ra khỏi vùng giao diện che (đáy 15 %)

# ---------------- S16: hook (xong trước 4 s, giữ 1 s) ----------------
FX.append(dict(t="type", s="S16", x=60, y=300, w=960, size=66, text="SWAN LAKE ONSEN", at=0.4, per=0.045))
FX.append(dict(t="type", s="S16", x=60, y=385, w=960, size=66, text="RESIDENCES", at=1.2, per=0.045))
FX.append(dict(t="type", s="S16", x=60, y=480, w=960, size=50, text="ven [hồ Thiên Nga]", at=2.0, per=0.04, hl=True))

# ---------------- S02: tỉnh + chỉ số (giữ lâu) ----------------
FX.append(dict(t="veil", s="S02", alpha=0.42, at=3.2, dur=0.8))
for d in OV.svg_paths(OSM["N00"]["b4"], VIEWS["N00"][:2], VIEWS["N00"][2], G, 1.2):
    FX.append(dict(t="path", s="S02", d=d, c="#27e6ff", w=8, at=0.5, dur=1.6))
x, y = pt("N00", *PROJ)
FX.append(dict(t="pin", s="S02", x=x, y=y, at=2.0))
FX.append(dict(t="text", s="S02", x=60, y=300, w=960, size=70, text="TỈNH HƯNG YÊN", at=0.6, color="#27e6ff"))
FX.append(dict(t="text", s="S02", x=60, y=392, w=960, size=30, text="Tỉnh mới theo NQ 202/2025/QH15, hiệu lực 01/7/2025 · ranh © OpenStreetMap, tham khảo", at=1.4, color="#ffffff", plain=True))
FX.append(dict(t="card", s="S02", i=0, num="+10,72%", unit="GRDP", cap="Hưng Yên mới, 6 tháng 2026 · thứ 5/34", src="báo Đại biểu Nhân dân, VOV", at=4.0, y=1040))
FX.append(dict(t="card", s="S02", i=1, num="20,23", unit="tỷ USD", cap="FDI luỹ kế · 1.006 dự án (đến 8/2026)", src="VietnamPlus, 9/2026", at=8.6, y=1350))

# ---------------- S03: xã Phụng Công (đứng yên) ----------------
for d in OV.svg_paths(OSM["M02"]["b4"], VIEWS["M02"][:2], VIEWS["M02"][2], G, 1.2):
    FX.append(dict(t="path", s="S03", d=d, c="#27e6ff", w=7, at=0.2, dur=1.2))
for d in OV.svg_paths(OSM["M02"]["b6"], VIEWS["M02"][:2], VIEWS["M02"][2], G, 1.2):
    FX.append(dict(t="path", s="S03", d=d, c="#e4ff3a", w=5, at=0.6, dur=1.4))
x, y = pt("M02", *PROJ)
FX.append(dict(t="pin", s="S03", x=x, y=y, at=1.8))
FX.append(dict(t="text", s="S03", x=60, y=300, w=960, size=70, text="XÃ PHỤNG CÔNG", at=0.5, color="#e4ff3a"))
FX.append(dict(t="text", s="S03", x=60, y=392, w=960, size=56, text="45.327 người · 14,61 km²", at=1.6, color="#ffffff"))
FX.append(dict(t="text", s="S03", x=60, y=478, w=960, size=28, text="VietnamPlus 9/7/2026; NQ 1666/NQ-UBTVQH15 (16/6/2025) · ranh © OpenStreetMap, tham khảo", at=2.0, color="#ffffff", plain=True))

# ---------------- S06: 3 bậc zoom, nhãn bằng tên nơi chốn ----------------
for sid, lab, col in (("S06a", "XÃ PHỤNG CÔNG", "#e4ff3a"), ("S06b", "KHU ĐÔ THỊ ECOPARK", "#ffffff"), ("S06c", "TỚI ĐÚNG DỰ ÁN", "#ff7a7a")):
    FX.append(dict(t="text", s=sid, x=60, y=300, w=960, size=64, text=lab, at=0.15, color=col))

# ---------------- S07: cận cảnh dự án (vệ tinh 3D, minh hoạ) ----------------
FX.append(dict(t="text", s="S07", x=60, y=300, w=960, size=60, text="SWAN LAKE ONSEN", at=0.4, color="#ffffff"))
FX.append(dict(t="text", s="S07", x=60, y=386, w=960, size=40, text="ẢNH VỆ TINH 3D · MINH HOẠ", at=1.2, color="#ffd34d"))

# ---------------- S08: hồ Thiên Nga bo viền + khoảng cách ----------------
LAKE_SEED = pt("N01", POI["cv"][1], POI["cv"][2])
lake = WO.outline(os.path.join(RAW, ML2, "N01w.png"), LAKE_SEED)
assert lake, "không tìm được hồ"
FX.append(dict(t="poly", s="S08", d=WO.to_svg_d(lake[0]), c="#27e6ff", w=7, fill="rgba(39,230,255,.26)", at=0.6, dur=2.2))
px, py = pt("N01", *PROJ)
cx, cy = pt("N01", POI["cv"][1], POI["cv"][2])
FX.append(dict(t="pin", s="S08", x=px, y=py, at=2.6))
FX.append(dict(t="dash", s="S08", x1=px, y1=py, x2=cx, y2=cy, at=3.2, dur=0.8))
FX.append(dict(t="dash", s="S08", x1=(px + cx) / 2, y1=(py + cy) / 2, x2=770, y2=(py + cy) / 2, at=3.9, dur=0.4))
FX.append(dict(t="numbox", s="S08", x=880, y=(py + cy) / 2, text=kmtxt(POI["cv"][3]), at=4.2, c="#ffd34d", size=40))
FX.append(dict(t="tag", s="S08", x=px, y=py, tx=0, ty=py + 40, side="l", l1="DỰ ÁN", l2="", at=2.9, color="#ff7a7a", auto=True, fixed_y=py + 30))
FX.append(dict(t="text", s="S08", x=60, y=300, w=960, size=70, text="HỒ THIÊN NGA", at=0.5, color="#27e6ff"))
FX.append(dict(t="text", s="S08", x=60, y=392, w=960, size=44, text="Công viên ven hồ cách dự án 0,24 km", at=3.4, color="#ffffff"))
FX.append(dict(t="text", s="S08", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay · ranh hồ © OpenStreetMap, tham khảo · tính 19/11/2026", at=3.4, color="#ffffff", plain=True))

# ---------------- S10: khối 3D + câu bố cục ----------------
FX.append(dict(t="text", s="S10", x=60, y=300, w=960, size=60, text="ẢNH VỆ TINH", at=0.2, color="#ffffff", out=2.4))
FX.append(dict(t="text", s="S10", x=60, y=300, w=960, size=60, text="KHỐI 3D MINH HOẠ", at=2.7, color="#ffd34d"))
FX.append(dict(t="text", s="S10", x=60, y=386, w=960, size=44, text="Các tòa tháp xếp ven mặt hồ", at=3.3, color="#ffffff"))
FX.append(dict(t="text", s="S10", x=60, y=SRC_Y, w=960, size=28, text="Khối 3D từ dữ liệu © OpenStreetMap, minh hoạ, không phải hiện trạng", at=3.0, color="#ffffff", plain=True))

# ---------------- S09: khu đô thị lân cận phía Đông ----------------
px, py = pt("N06", *PROJ)
ox, oy = pt("N06", POI["oc"][1], POI["oc"][2])
FX.append(dict(t="pin", s="S09", x=px, y=py, at=0.4))
FX.append(dict(t="tag", s="S09", x=px, y=py, tx=0, ty=py + 40, side="r", l1="SWAN LAKE ONSEN", l2="", at=0.6, color="#b6ff1a", auto=True, fixed_y=py - 120))
FX.append(dict(t="dash", s="S09", x1=px, y1=py, x2=ox, y2=oy, at=1.4, dur=1.0))
FX.append(dict(t="numbox", s="S09", x=(px + ox) / 2, y=(py + oy) / 2 - 60, text=kmtxt(POI["oc"][3]), at=2.5, c="#ffd34d", size=40))
FX.append(dict(t="tag", s="S09", x=ox, y=oy, tx=0, ty=oy + 40, side="l", l1="VINCOM OCEAN CITY", l2="trung tâm thương mại", at=1.9, color="#ffd34d", auto=True, fixed_y=oy + 30))
FX.append(dict(t="text", s="S09", x=60, y=300, w=960, size=60, text="PHÍA ĐÔNG DỰ ÁN", at=0.3, color="#ffd34d"))
FX.append(dict(t="text", s="S09", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay · toạ độ © OpenStreetMap · tính 19/11/2026", at=1.4, color="#ffffff", plain=True))

# ---------------- S14: vòng bán kính + nhóm tiện ích ----------------
px, py = pt("N05", *PROJ)
m = mpp("N05")
FX.append(dict(t="ring", s="S14", x=px, y=py, r=round(500 / m, 1), c="#ffffff", label="0,5 km", at=0.5, dur=1.0))
FX.append(dict(t="ring", s="S14", x=px, y=py, r=round(1500 / m, 1), c="#ffd34d", label="1,5 km", at=1.4, dur=1.2, fill="rgba(255,211,77,.07)"))
FX.append(dict(t="pin", s="S14", x=px, y=py, at=0.2))
for i, (k, shape, col, at) in enumerate((("cv", "dia", "#3ddc84", 2.2), ("ku", "cross", "#ff5a5a", 3.6), ("buv", "tri", "#5aa8ff", 5.0))):
    nm, la, lo, km = POI[k]
    ix, iy = pt("N05", la, lo)
    FX.append(dict(t="icon", s="S14", x=ix, y=iy, shape=shape, c=col, r=20, at=at))
    FX.append(dict(t="legend", s="S14", y=290 + i * 84, step=84, gap=0, at=at, rows=[(col, nm, kmtxt(km))]))
FX.append(dict(t="text", s="S14", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay, không phải thời gian di chuyển · toạ độ © OpenStreetMap · 19/11/2026", at=2.0, color="#ffffff", plain=True))

# ---------------- S11: trục đường chính + cầu + hướng vào Hà Nội ----------------
rn = OSM2["N03"]["rnames"]


def lines_of(pred):
    out = []
    for r in rn:
        if pred(r):
            out += r["lines"]
    return out


ROUTES = [
    ("Đại lộ Ecopark (ĐT.379)", lambda r: r["name"] == "Đại lộ Ecopark", "#ffe14d"),
    ("Đường liên tỉnh Hà Nội – Hưng Yên (ĐT.379)", lambda r: r["name"] == "Đường liên tỉnh Hà Nội - Hưng Yên", "#ffe14d"),
    ("Cầu Thanh Trì", lambda r: r["name"] == "Cầu Thanh Trì", "#ff9f3a"),
    ("Vành đai 3 (CT.37)", lambda r: r["name"].startswith("Đường cao tốc Vành đai 3"), "#ff9f3a"),
]
at = 0.5
for nm, pred, col in ROUTES:
    for d in OV.svg_paths(lines_of(pred), VIEWS["N03"][:2], VIEWS["N03"][2], G, 1.5):
        FX.append(dict(t="path", s="S11", d=d, c=col, w=11, at=at, dur=1.4))
    at += 0.6
px, py = pt("N03", *PROJ)
bx, by = pt("N03", POI["tt"][1], POI["tt"][2])
hx, hy = pt("N03", *HK)
def _mid_label(pred, text, at, col, dx=0, dy=0):
    """Đặt nhãn tên đường ở giữa mảnh dài nhất nhìn thấy, xoay theo hướng tuyến."""
    best = None
    for d in OV.svg_paths(lines_of(pred), VIEWS["N03"][:2], VIEWS["N03"][2], G, 1.5):
        pts = [tuple(map(float, p.split(","))) for p in d.replace("M", "").split(" L")]
        pts = [p for p in pts if 80 < p[0] < 1000 and 420 < p[1] < 1480]
        if len(pts) < 2:
            continue
        L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        if best is None or L > best[0]:
            best = (L, pts)
    if not best:
        return
    pts = best[1]
    i = len(pts) // 2
    a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
    rot = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    rot = rot - 180 if rot > 90 else rot + 180 if rot < -90 else rot
    FX.append(dict(t="rlabel", s="S11", x=pts[i][0] + dx, y=pts[i][1] + dy, rot=round(rot, 1), text=text, c=col, size=34, at=at))


_mid_label(lambda r: r["name"] == "Đại lộ Ecopark", "Đại lộ Ecopark", 1.6, "#ffe14d", dx=-90, dy=-30)
_mid_label(lambda r: r["name"].startswith("Đường cao tốc Vành đai 3"), "Vành đai 3", 2.8, "#ff9f3a", dy=-34)
FX.append(dict(t="rlabel", s="S11", x=bx - 10, y=by - 52, rot=0, text="Cầu Thanh Trì", c="#ffffff", size=36, at=3.6))
FX.append(dict(t="pin", s="S11", x=px, y=py, at=0.3))
FX.append(dict(t="tag", s="S11", x=px, y=py, tx=0, ty=py + 30, side="r", l1="DỰ ÁN", l2="", at=0.5, color="#ff7a7a", auto=True, fixed_y=py + 30))
FX.append(dict(t="dash", s="S11", x1=px, y1=py, x2=bx, y2=by, at=3.4, dur=1.0))
FX.append(dict(t="numbox", s="S11", x=(px + bx) / 2 + 150, y=(py + by) / 2, text=kmtxt(POI["tt"][3]), at=4.5, c="#ffd34d", size=40))
ang = math.atan2(hy - by, hx - bx)
FX.append(dict(t="arrow", s="S11", x1=bx, y1=by, x2=bx + 170 * math.cos(ang), y2=by + 170 * math.sin(ang), c="#ffffff", w=12, at=4.2, dur=0.8))
FX.append(dict(t="rlabel", s="S11", x=bx + 200 * math.cos(ang) + 20, y=by + 200 * math.sin(ang) - 36, rot=0, text="HÀ NỘI", c="#ffffff", size=44, at=5.0))
FX.append(dict(t="text", s="S11", x=60, y=300, w=960, size=60, text="TRỤC ĐƯỜNG CHÍNH", at=0.4, color="#ffe14d"))
FX.append(dict(t="text", s="S11", x=60, y=386, w=960, size=44, text="Cầu Thanh Trì → vào nội thành Hà Nội", at=4.4, color="#ffffff"))
FX.append(dict(t="text", s="S11", x=60, y=SRC_Y, w=960, size=28, text="Tên đường theo © OpenStreetMap, cần xác nhận · khoảng cách chim bay", at=1.0, color="#ffffff", plain=True))

# ---------------- S19: Hồ Hoàn Kiếm + khoảng cách ----------------
px, py = pt("N04", *PROJ)
hx, hy = pt("N04", *HK)
hk_lake = WO.outline(os.path.join(RAW, ML2, "N04w.png"), (hx, hy), max_gap=60)
if hk_lake:
    FX.append(dict(t="poly", s="S19", d=WO.to_svg_d(hk_lake[0]), c="#27e6ff", w=6, fill="rgba(39,230,255,.4)", at=0.4, dur=1.0))
else:  # hồ quá nhỏ ở khung này: khoanh bằng vòng
    FX.append(dict(t="ring", s="S19", x=hx, y=hy, r=46, c="#27e6ff", w=7, fill="rgba(39,230,255,.18)", at=0.5, dur=0.9))
FX.append(dict(t="pin", s="S19", x=px, y=py, at=0.3))
FX.append(dict(t="dash", s="S19", x1=px, y1=py, x2=hx, y2=hy, at=1.4, dur=1.4))
FX.append(dict(t="numbox", s="S19", x=(px + hx) / 2 + 180, y=(py + hy) / 2, text=kmtxt(POI["hk"][3]), at=2.8, c="#ffd34d", size=40))
FX.append(dict(t="tag", s="S19", x=px, y=py, tx=0, ty=py + 40, side="r", l1="DỰ ÁN", l2="", at=0.5, color="#ff7a7a", auto=True, fixed_y=py + 30))
FX.append(dict(t="tag", s="S19", x=hx, y=hy, tx=0, ty=hy - 90, side="r", l1="HỒ HOÀN KIẾM", l2="", at=0.8, color="#27e6ff", auto=True, fixed_y=hy - 100))
FX.append(dict(t="text", s="S19", x=60, y=300, w=960, size=60, text="TỚI TRUNG TÂM HÀ NỘI", at=0.3, color="#27e6ff"))
FX.append(dict(t="text", s="S19", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay · toạ độ © OpenStreetMap · tính 19/11/2026", at=1.0, color="#ffffff", plain=True))

# ---------------- S26: CTA ----------------
FX.append(dict(t="text", s="S26L", x=60, y=360, w=960, size=84, text="XEM CHI TIẾT", at=0.3, color="#ffffff"))
FX.append(dict(t="text", s="S26L", x=60, y=480, w=960, size=60, text="[TÊN KÊNH / LIÊN HỆ]", at=1.0, color="#b6ff1a"))
FX.append(dict(t="text", s="S26L", x=60, y=1380, w=960, size=28, text="Thông tin tham khảo, cập nhật 11/2026. Khoảng cách tính theo đường chim bay. Ảnh vệ tinh và khối 3D mang tính minh hoạ, không phải hiện trạng.", at=0.2, color="#ffffff", plain=True))


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    names = {}
    for sid, kind, src, st, du, mo, blur in SCENES:
        if kind == "layer":
            continue
        full = os.path.join(RAW, src)
        if not os.path.isfile(full):
            raise SystemExit("thiếu " + full)
        if full not in names:
            base = os.path.splitext(os.path.basename(src))[0]
            if full.endswith(".png"):
                names[full] = base + ".jpg"
                Image.open(full).convert("RGB").save(os.path.join(OUT, "assets", names[full]), quality=92)
            else:
                names[full] = base + ".mp4"
                shutil.copy(full, os.path.join(OUT, "assets", names[full]))
    fdir = os.environ.get("FONT_DIR") or os.path.join(P, "fonts")  # cần Montserrat-800.ttf và -900.ttf (OFL) có tiếng Việt
    for w in ("800", "900"):
        shutil.copy(os.path.join(fdir, f"Montserrat-{w}.ttf"), os.path.join(OUT, "assets", f"Montserrat-{w}.ttf"))
    els, base_js = [], []
    for n, (sid, kind, src, st, du, mo, blur) in enumerate(SCENES):
        tr = n + 1
        if kind == "layer":
            els.append(f'<div class="clip layer" id="L_{sid}" data-start="{st}" data-duration="{du}" data-track-index="{100 + tr}"><svg class="ov" viewBox="0 0 1080 1920"></svg><div class="lab"></div></div>')
            continue
        f = "assets/" + names[os.path.join(RAW, src)]
        if kind == "video":
            els.append(f'<video class="clip m" id="{sid}" src="{f}" muted playsinline data-start="{st}" data-duration="{du}" data-track-index="{tr}"></video>')
            els.append(f'<div class="clip layer" id="L_{sid}" data-start="{st}" data-duration="{du}" data-track-index="{100 + tr}"><svg class="ov" viewBox="0 0 1080 1920"></svg><div class="lab"></div></div>')
        elif kind == "img":
            els.append(f'<img class="clip m" id="{sid}" src="{f}" alt="" data-start="{st}" data-duration="{du}" data-track-index="{tr}">')
            els.append(f'<div class="clip layer" id="L_{sid}" data-start="{st}" data-duration="{du}" data-track-index="{100 + tr}"><svg class="ov" viewBox="0 0 1080 1920"></svg><div class="lab"></div></div>')
            base_js.append(f'tl.fromTo("#{sid}", {{ scale: {mo[0]} }}, {{ scale: {mo[1]}, duration: {du}, ease: "none" }}, {st});')
        else:
            els.append(f'<div class="clip g" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="{tr}"><img class="m" src="{f}" alt=""><svg class="ov" viewBox="0 0 1080 1920"></svg><div class="lab"></div></div>')
            base_js.append(f'tl.fromTo("#{sid}", {{ scale: {mo[0]} }}, {{ scale: {mo[1]}, duration: {du}, ease: "none" }}, {st});')
        if blur:
            base_js.append(f'tl.fromTo("#{sid}", {{ filter: "blur(14px)" }}, {{ filter: "blur(0px)", duration: 0.3, ease: "power2.out" }}, {st});')
    layer_of = {sid: (sid if kind == "g" else "L_" + sid) for sid, kind, *_ in SCENES}
    fx = []
    for e in FX:
        e = dict(e)
        e["host"] = layer_of[e["s"]]
        e["T"] = T0[e["s"]]
        fx.append(e)
    html = TEMPLATE.replace("__ELEMENTS__", "\n      ".join(els)).replace("__BASEJS__", "\n        ".join(base_js)) \
        .replace("__FX__", json.dumps(fx, ensure_ascii=False, separators=(",", ":"))).replace("__TOTAL__", str(TOTAL))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    print(len(SCENES), "cảnh,", len(FX), "hiệu ứng ->", OUT)


TEMPLATE = open(os.path.join(HERE, "draft2_template.html"), encoding="utf-8").read()

if __name__ == "__main__":
    build()
