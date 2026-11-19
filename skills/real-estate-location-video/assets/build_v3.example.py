#!/usr/bin/env python3
"""VÍ DỤ bản v3: clip zoom liền mạch (camera_path_capture.mjs, quay từng khung), nhiều góc nhà 3D, viền neon, đường chấm sáng, radar.
Cảnh nối tiếp theo bảng SEQ (thời điểm bắt đầu tự cộng dồn); lời đọc khai trong VOICE theo (cảnh, độ lệch). Ghi comp4/ + voice_lines_v3.json.
Sao chép vào <project>/tools/ rồi sửa PROJ/POI/VIEWS/SEQ/FX; clip D*/E* quay bằng camera_paths.example.json."""
import json
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)
RAW = os.path.join(P, "raw")
OUT = os.path.join(P, "comp4")
SK = os.environ.get("SKILLS_DIR") or os.path.normpath(os.path.join(HERE, "..", ".."))  # thư mục skills/ của repo
sys.path.insert(0, os.path.join(SK, "land-plot-map-video", "assets"))
sys.path.insert(0, os.path.join(SK, "real-estate-location-video", "assets"))
import geo_cfg as G          # noqa: E402
import osm_overlay as OV     # noqa: E402
import water_outline as WO   # noqa: E402
from PIL import Image        # noqa: E402

PROJ = (20.95374525, 105.93237025)
HK = (21.0285, 105.8523)
POI = {
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


for k, (nm, la, lo, km) in POI.items():
    assert abs(hav(PROJ, (la, lo)) - km) / km < 0.03, (k, hav(PROJ, (la, lo)), km)


def kmtxt(km):
    return f"{km:.2f}".replace(".", ",") + " km"


VIEWS = {
    "M02": (20.95655, 105.93502, 14.5), "N00": (20.78, 106.12, 10.8), "N06": (20.9528, 105.953, 14.2),
    "N01": (20.960, 105.9325, 15.6), "N05": (PROJ[0], PROJ[1], 15.0), "N03": (20.974, 105.9175, 12.9), "N04": (20.991, 105.892, 12.5),
    "D3": (PROJ[0], PROJ[1], 17.2),
}
OSM = json.load(open(os.path.join(RAW, "osm_overlays.json"), encoding="utf-8"))
OSM["N00"] = json.load(open(os.path.join(RAW, "osm_n00.json"), encoding="utf-8"))["N00"]
OSM2 = json.load(open(os.path.join(RAW, "osm_v2.json"), encoding="utf-8"))
ML2, CAM, E1, E2 = "maplibre2/", "cam/", "earth-clean/", "earth-clean2/"

# (id, loại, nguồn, độ dài, chuyển động, nhòe vào)  — thời điểm bắt đầu tính nối tiếp
SEQ = [
    ("D1", "video", CAM + "D1.mp4", 5.0, None, False),        # zoom liền mạch: toàn quốc → tỉnh
    ("S02", "g", ML2 + "N00.png", 12.4, (1.00, 1.04), False),
    ("D2", "video", CAM + "D2.mp4", 3.2, None, False),        # tỉnh → xã
    ("S03", "g", "maplibre/M02.png", 5.6, (1.00, 1.04), False),
    ("D3", "video", CAM + "D3.mp4", 4.5, None, False),        # xã → Ecopark → dự án
    ("S07", "img", E2 + "R11.png", 4.4, (1.00, 1.08), True),
    ("S08", "g", ML2 + "N01.png", 7.0, (1.00, 1.03), True),
    ("E1", "video", CAM + "E1.mp4", 6.0, None, True),         # vệ tinh → khối 3D mọc, xoay
    ("E2", "video", CAM + "E2.mp4", 5.0, None, True),         # bay thấp từ phía hồ
    ("E3", "video", CAM + "E3.mp4", 6.0, None, True),         # xoay toàn cảnh
    ("E4", "video", CAM + "E4.mp4", 5.0, None, True),         # nghiêng dần từ trên xuống
    ("S09", "g", ML2 + "N06.png", 5.2, (1.00, 1.03), True),
    ("S14", "g", ML2 + "N05.png", 9.0, (1.00, 1.02), True),
    ("S11", "g", ML2 + "N03.png", 6.8, (1.00, 1.03), True),
    ("S19", "g", ML2 + "N04.png", 5.3, (1.00, 1.03), True),
    ("S26a", "img", E1 + "R11b.png", 2.5, (1.00, 1.08), True),
    ("S26b", "img", E2 + "R21.png", 2.5, (1.08, 1.00), False),
]
SCENES, T0, t = [], {}, 0.0
for sid, kind, src, du, mo, blur in SEQ:
    SCENES.append((sid, kind, src, round(t, 2), du, mo, blur))
    T0[sid] = round(t, 2)
    t += du
SCENES.append(("S26L", "layer", None, T0["S26a"], 5.0, None, False))
T0["S26L"] = T0["S26a"]
TOTAL = round(t + 0.1, 1)
FX = []
VOICE = []  # (id, scene, offset, allot, lời)


def pt(view, lat, lng):
    la, lo, z = VIEWS[view]
    x, y = G.to_frame(lat, lng, (la, lo), z)
    return round(x, 1), round(y, 1)


def mpp(view):
    return 156543.03 * math.cos(math.radians(PROJ[0])) / 2 ** VIEWS[view][2]


SRC_Y = 1520
NOTE3D = "Khối 3D từ dữ liệu © OpenStreetMap, minh hoạ, không phải hiện trạng"

# ---- D1: hook trên đoạn zoom mở đầu ----
FX.append(dict(t="type", s="D1", x=60, y=300, w=960, size=66, text="SWAN LAKE ONSEN", at=0.5, per=0.045))
FX.append(dict(t="type", s="D1", x=60, y=385, w=960, size=66, text="RESIDENCES", at=1.3, per=0.045))
FX.append(dict(t="type", s="D1", x=60, y=480, w=960, size=50, text="ven [hồ Thiên Nga]", at=2.1, per=0.04, hl=True))
VOICE.append(("V01", "D1", 0.6, 4.4, "Xoan Lếch Ôn-sen Rê-di-đần-xơ, căn hộ ven hồ Thiên Nga."))

# ---- S02: tỉnh + chỉ số ----
FX.append(dict(t="veil", s="S02", alpha=0.42, at=3.2, dur=0.8))
for d in OV.svg_paths(OSM["N00"]["b4"], VIEWS["N00"][:2], VIEWS["N00"][2], G, 1.2):
    FX.append(dict(t="path", s="S02", d=d, c="#27e6ff", w=10, at=0.5, dur=1.8))
x, y = pt("N00", *PROJ)
FX.append(dict(t="pin", s="S02", x=x, y=y, at=2.2))
FX.append(dict(t="text", s="S02", x=60, y=300, w=960, size=70, text="TỈNH HƯNG YÊN", at=0.6, color="#27e6ff"))
FX.append(dict(t="text", s="S02", x=60, y=392, w=960, size=30, text="Tỉnh mới theo NQ 202/2025/QH15, hiệu lực 01/7/2025 · ranh © OpenStreetMap, tham khảo", at=1.4, color="#ffffff", plain=True))
FX.append(dict(t="card", s="S02", i=0, num="+10,72%", unit="GRDP", cap="Hưng Yên mới, 6 tháng 2026 · thứ 5/34", src="báo Đại biểu Nhân dân, VOV", at=4.0, y=1040))
FX.append(dict(t="card", s="S02", i=1, num="20,23", unit="tỷ USD", cap="FDI luỹ kế · 1.006 dự án (đến 8/2026)", src="VietnamPlus, 9/2026", at=8.6, y=1350))
VOICE.append(("V02", "S02", 0.4, 3.6, "Dự án thuộc tỉnh Hưng Yên mới."))
VOICE.append(("V03", "S02", 4.2, 4.4, "Hưng Yên tăng trưởng hơn mười phần trăm nửa đầu năm hai không hai sáu, đứng thứ năm cả nước."))
VOICE.append(("V04", "S02", 8.8, 3.4, "Vốn đầu tư nước ngoài luỹ kế hơn hai mươi tỷ đô la."))

# ---- D2: zoom tỉnh → xã ----
FX.append(dict(t="text", s="D2", x=60, y=300, w=960, size=64, text="ZOOM VÀO XÃ PHỤNG CÔNG", at=0.6, color="#e4ff3a"))

# ---- S03: xã ----
for d in OV.svg_paths(OSM["M02"]["b4"], VIEWS["M02"][:2], VIEWS["M02"][2], G, 1.2):
    FX.append(dict(t="path", s="S03", d=d, c="#27e6ff", w=9, at=0.2, dur=1.3))
for d in OV.svg_paths(OSM["M02"]["b6"], VIEWS["M02"][:2], VIEWS["M02"][2], G, 1.2):
    FX.append(dict(t="path", s="S03", d=d, c="#e4ff3a", w=8, at=0.6, dur=1.6))
x, y = pt("M02", *PROJ)
FX.append(dict(t="pin", s="S03", x=x, y=y, at=2.0))
FX.append(dict(t="text", s="S03", x=60, y=300, w=960, size=70, text="XÃ PHỤNG CÔNG", at=0.5, color="#e4ff3a"))
FX.append(dict(t="text", s="S03", x=60, y=392, w=960, size=56, text="45.327 người · 14,61 km²", at=1.6, color="#ffffff"))
FX.append(dict(t="text", s="S03", x=60, y=478, w=960, size=28, text="VietnamPlus 9/7/2026; NQ 1666/NQ-UBTVQH15 (16/6/2025) · ranh © OpenStreetMap, tham khảo", at=2.0, color="#ffffff", plain=True))
VOICE.append(("V05", "S03", 0.2, 5.0, "Vị trí cụ thể: xã Phụng Công, hơn bốn mươi lăm nghìn dân."))

# ---- D3: zoom xã → Ecopark → dự án ----
FX.append(dict(t="text", s="D3", x=60, y=300, w=960, size=64, text="KHU ĐÔ THỊ ECOPARK", at=1.2, color="#ffffff", out=2.8))
FX.append(dict(t="text", s="D3", x=60, y=386, w=960, size=64, text="TỚI ĐÚNG DỰ ÁN", at=3.4, color="#ff7a7a"))
x, y = pt("D3", *PROJ)
FX.append(dict(t="pin", s="D3", x=x, y=y, at=3.6))
VOICE.append(("V06", "D3", 0.2, 4.4, "Từ xã Phụng Công, vào khu đô thị Ê-cô-pác, rồi tới đúng vị trí dự án."))

# ---- S07: cận cảnh ----
FX.append(dict(t="text", s="S07", x=60, y=300, w=960, size=60, text="SWAN LAKE ONSEN", at=0.4, color="#ffffff"))
FX.append(dict(t="text", s="S07", x=60, y=386, w=960, size=40, text="ẢNH VỆ TINH 3D · MINH HOẠ", at=1.2, color="#ffd34d"))
VOICE.append(("V07", "S07", 0.2, 3.9, "Đây là hình ảnh vệ tinh ba chiều của dự án."))

# ---- S08: hồ ----
lake = WO.outline(os.path.join(RAW, ML2, "N01w.png"), pt("N01", POI["cv"][1], POI["cv"][2]))
assert lake, "không tìm được hồ"
FX.append(dict(t="poly", s="S08", d=WO.to_svg_d(lake[0]), c="#27e6ff", w=8, fill="rgba(39,230,255,.26)", at=0.6, dur=2.4))
px, py = pt("N01", *PROJ)
cx, cy = pt("N01", POI["cv"][1], POI["cv"][2])
FX.append(dict(t="pin", s="S08", x=px, y=py, at=2.8))
FX.append(dict(t="dash", s="S08", x1=px, y1=py, x2=cx, y2=cy, c="#ffd34d", at=3.3, dur=0.8))
FX.append(dict(t="dash", s="S08", x1=(px + cx) / 2, y1=(py + cy) / 2, x2=770, y2=(py + cy) / 2, c="#ffd34d", at=4.0, dur=0.4))
FX.append(dict(t="numbox", s="S08", x=880, y=(py + cy) / 2, text=kmtxt(POI["cv"][3]), at=4.3, c="#ffd34d", size=40))
FX.append(dict(t="tag", s="S08", x=px, y=py, tx=0, ty=py + 40, side="l", l1="DỰ ÁN", l2="", at=3.0, color="#ff7a7a", auto=True, fixed_y=py + 30))
FX.append(dict(t="text", s="S08", x=60, y=300, w=960, size=70, text="HỒ THIÊN NGA", at=0.5, color="#27e6ff"))
FX.append(dict(t="text", s="S08", x=60, y=392, w=960, size=44, text="Công viên ven hồ cách dự án 0,24 km", at=3.5, color="#ffffff"))
FX.append(dict(t="text", s="S08", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay · ranh hồ © OpenStreetMap, tham khảo · tính 19/11/2026", at=3.5, color="#ffffff", plain=True))
VOICE.append(("V08", "S08", 0.2, 6.4, "Ngay cạnh dự án là hồ Thiên Nga. Công viên ven hồ cách chưa tới ba trăm mét chim bay."))

# ---- E1–E4: các góc nhà 3D ----
FX.append(dict(t="text", s="E1", x=60, y=300, w=960, size=60, text="ẢNH VỆ TINH", at=0.2, color="#ffffff", out=2.4))
FX.append(dict(t="text", s="E1", x=60, y=300, w=960, size=60, text="KHỐI 3D MINH HOẠ", at=2.7, color="#ffd34d"))
FX.append(dict(t="text", s="E1", x=60, y=386, w=960, size=44, text="Các tòa tháp xếp ven mặt hồ", at=3.3, color="#ffffff"))
FX.append(dict(t="text", s="E1", x=60, y=SRC_Y, w=960, size=28, text=NOTE3D, at=3.0, color="#ffffff", plain=True))
VOICE.append(("V09", "E1", 0.3, 5.2, "Nhìn khối ba chiều: các tòa tháp xếp ven mặt hồ."))
FX.append(dict(t="text", s="E2", x=60, y=300, w=960, size=60, text="NHÌN TỪ PHÍA HỒ", at=0.3, color="#ffd34d"))
FX.append(dict(t="text", s="E2", x=60, y=386, w=960, size=44, text="Góc bay thấp về phía dự án", at=1.0, color="#ffffff"))
FX.append(dict(t="text", s="E2", x=60, y=SRC_Y, w=960, size=28, text=NOTE3D, at=1.0, color="#ffffff", plain=True))
VOICE.append(("V09b", "E2", 0.3, 4.4, "Góc bay thấp từ phía hồ nhìn vào dự án."))
FX.append(dict(t="text", s="E3", x=60, y=300, w=960, size=60, text="TOÀN CẢNH DỰ ÁN", at=0.3, color="#ffd34d"))
FX.append(dict(t="text", s="E3", x=60, y=386, w=960, size=44, text="Xoay quanh dãy tòa tháp", at=1.0, color="#ffffff"))
FX.append(dict(t="text", s="E3", x=60, y=SRC_Y, w=960, size=28, text=NOTE3D, at=1.0, color="#ffffff", plain=True))
VOICE.append(("V09c", "E3", 0.3, 5.0, "Xoay quanh toàn bộ dãy tòa tháp của dự án."))
FX.append(dict(t="text", s="E4", x=60, y=300, w=960, size=60, text="BỐ CỤC TỔNG THỂ", at=0.3, color="#ffd34d"))
FX.append(dict(t="text", s="E4", x=60, y=386, w=960, size=44, text="Từ trên cao nghiêng xuống", at=1.0, color="#ffffff"))
FX.append(dict(t="text", s="E4", x=60, y=SRC_Y, w=960, size=28, text=NOTE3D, at=1.0, color="#ffffff", plain=True))
VOICE.append(("V09d", "E4", 0.3, 4.2, "Và bố cục tổng thể nhìn từ trên cao."))

# ---- S09: phía Đông ----
px, py = pt("N06", *PROJ)
ox, oy = pt("N06", POI["oc"][1], POI["oc"][2])
FX.append(dict(t="pin", s="S09", x=px, y=py, at=0.4))
FX.append(dict(t="tag", s="S09", x=px, y=py, tx=0, ty=py - 120, side="r", l1="SWAN LAKE ONSEN", l2="", at=0.6, color="#b6ff1a", auto=True, fixed_y=py - 120))
FX.append(dict(t="dash", s="S09", x1=px, y1=py, x2=ox, y2=oy, c="#ffd34d", at=1.4, dur=1.0))
FX.append(dict(t="numbox", s="S09", x=(px + ox) / 2, y=(py + oy) / 2 - 60, text=kmtxt(POI["oc"][3]), at=2.5, c="#ffd34d", size=40))
FX.append(dict(t="tag", s="S09", x=ox, y=oy, tx=0, ty=oy + 40, side="l", l1="VINCOM OCEAN CITY", l2="trung tâm thương mại", at=1.9, color="#ffd34d", auto=True, fixed_y=oy + 30))
FX.append(dict(t="text", s="S09", x=60, y=300, w=960, size=60, text="PHÍA ĐÔNG DỰ ÁN", at=0.3, color="#ffd34d"))
FX.append(dict(t="text", s="S09", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay · toạ độ © OpenStreetMap · tính 19/11/2026", at=1.4, color="#ffffff", plain=True))
VOICE.append(("V10", "S09", 0.2, 4.8, "Phía Đông là trung tâm thương mại Vin-com Ô-sần Xi-ti, cách bốn phẩy ba cây số chim bay."))

# ---- S14: vòng bán kính + radar ----
px, py = pt("N05", *PROJ)
m = mpp("N05")
FX.append(dict(t="ring", s="S14", x=px, y=py, r=round(500 / m, 1), c="#ffffff", label="0,5 km", at=0.5, dur=1.0))
FX.append(dict(t="ring", s="S14", x=px, y=py, r=round(1500 / m, 1), c="#3ddc84", label="1,5 km", at=1.4, dur=1.2, fill="rgba(61,220,132,.07)", radar=True, sweep=3.6, turns=2))
FX.append(dict(t="pin", s="S14", x=px, y=py, at=0.2))
for i, (k, shape, col, at) in enumerate((("cv", "dia", "#3ddc84", 3.0), ("ku", "cross", "#ff5a5a", 4.8), ("buv", "tri", "#5aa8ff", 6.6))):
    nm, la, lo, km = POI[k]
    ix, iy = pt("N05", la, lo)
    FX.append(dict(t="icon", s="S14", x=ix, y=iy, shape=shape, c=col, r=20, at=at))
    FX.append(dict(t="legend", s="S14", y=290 + i * 84, step=84, gap=0, at=at, rows=[(col, nm, kmtxt(km))]))
FX.append(dict(t="text", s="S14", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay, không phải thời gian di chuyển · toạ độ © OpenStreetMap · 19/11/2026", at=2.0, color="#ffffff", plain=True))
VOICE.append(("V11", "S14", 0.3, 7.6, "Trong bán kính một cây số rưỡi có công viên, bệnh viện Cu-su-mi cách một phẩy một cây số, và Đại học Anh Quốc cách một phẩy ba."))

# ---- S11: trục đường ----
rn = OSM2["N03"]["rnames"]


def lines_of(pred):
    return [ln for r in rn if pred(r) for ln in r["lines"]]


ROUTES = [
    (lambda r: r["name"] == "Đại lộ Ecopark", "#ffe14d"),
    (lambda r: r["name"] == "Đường liên tỉnh Hà Nội - Hưng Yên", "#ffe14d"),
    (lambda r: r["name"] == "Cầu Thanh Trì", "#ff9f3a"),
    (lambda r: r["name"].startswith("Đường cao tốc Vành đai 3"), "#ff9f3a"),
]
at = 0.5
for pred, col in ROUTES:
    for d in OV.svg_paths(lines_of(pred), VIEWS["N03"][:2], VIEWS["N03"][2], G, 1.5):
        FX.append(dict(t="path", s="S11", d=d, c=col, w=12, at=at, dur=1.5))
    at += 0.6


def _mid_label(pred, text, at, col, dx=0, dy=0):
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
px, py = pt("N03", *PROJ)
bx, by = pt("N03", POI["tt"][1], POI["tt"][2])
hx, hy = pt("N03", *HK)
FX.append(dict(t="rlabel", s="S11", x=bx - 10, y=by - 52, rot=0, text="Cầu Thanh Trì", c="#ffffff", size=36, at=3.6))
FX.append(dict(t="pin", s="S11", x=px, y=py, at=0.3))
FX.append(dict(t="tag", s="S11", x=px, y=py, tx=0, ty=py + 30, side="r", l1="DỰ ÁN", l2="", at=0.5, color="#ff7a7a", auto=True, fixed_y=py + 30))
FX.append(dict(t="dash", s="S11", x1=px, y1=py, x2=bx, y2=by, c="#ffffff", at=3.4, dur=1.0))
FX.append(dict(t="numbox", s="S11", x=(px + bx) / 2 + 150, y=(py + by) / 2, text=kmtxt(POI["tt"][3]), at=4.5, c="#ffd34d", size=40))
ang = math.atan2(hy - by, hx - bx)
FX.append(dict(t="arrow", s="S11", x1=bx, y1=by, x2=bx + 170 * math.cos(ang), y2=by + 170 * math.sin(ang), c="#ffffff", w=12, at=4.2, dur=0.8))
FX.append(dict(t="rlabel", s="S11", x=bx + 200 * math.cos(ang) + 20, y=by + 200 * math.sin(ang) - 36, rot=0, text="HÀ NỘI", c="#ffffff", size=44, at=5.0))
FX.append(dict(t="text", s="S11", x=60, y=300, w=960, size=60, text="TRỤC ĐƯỜNG CHÍNH", at=0.4, color="#ffe14d"))
FX.append(dict(t="text", s="S11", x=60, y=386, w=960, size=44, text="Cầu Thanh Trì → vào nội thành Hà Nội", at=4.4, color="#ffffff"))
FX.append(dict(t="text", s="S11", x=60, y=SRC_Y, w=960, size=28, text="Tên đường theo © OpenStreetMap, cần xác nhận · khoảng cách chim bay", at=1.0, color="#ffffff", plain=True))
VOICE.append(("V12", "S11", 0.2, 6.2, "Trục chính: đại lộ Ê-cô-pác, Vành đai ba, cầu Thanh Trì vào Hà Nội, cách năm phẩy năm cây số."))

# ---- S19: Hồ Hoàn Kiếm ----
px, py = pt("N04", *PROJ)
hx, hy = pt("N04", *HK)
hk_lake = WO.outline(os.path.join(RAW, ML2, "N04w.png"), (hx, hy), max_gap=60)
if hk_lake:
    FX.append(dict(t="poly", s="S19", d=WO.to_svg_d(hk_lake[0]), c="#27e6ff", w=6, fill="rgba(39,230,255,.4)", at=0.4, dur=1.0))
else:
    FX.append(dict(t="ring", s="S19", x=hx, y=hy, r=46, c="#27e6ff", w=8, fill="rgba(39,230,255,.2)", at=0.5, dur=0.9))
FX.append(dict(t="pin", s="S19", x=px, y=py, at=0.3))
FX.append(dict(t="dash", s="S19", x1=px, y1=py, x2=hx, y2=hy, c="#ffd34d", at=1.4, dur=1.4))
FX.append(dict(t="numbox", s="S19", x=(px + hx) / 2 + 180, y=(py + hy) / 2, text=kmtxt(POI["hk"][3]), at=2.8, c="#ffd34d", size=40))
FX.append(dict(t="tag", s="S19", x=px, y=py, tx=0, ty=py + 40, side="r", l1="DỰ ÁN", l2="", at=0.5, color="#ff7a7a", auto=True, fixed_y=py + 30))
FX.append(dict(t="tag", s="S19", x=hx, y=hy, tx=0, ty=hy - 90, side="r", l1="HỒ HOÀN KIẾM", l2="", at=0.8, color="#27e6ff", auto=True, fixed_y=hy - 100))
FX.append(dict(t="text", s="S19", x=60, y=300, w=960, size=60, text="TỚI TRUNG TÂM HÀ NỘI", at=0.3, color="#27e6ff"))
FX.append(dict(t="text", s="S19", x=60, y=SRC_Y, w=960, size=28, text="Đường chim bay · toạ độ © OpenStreetMap · tính 19/11/2026", at=1.0, color="#ffffff", plain=True))
VOICE.append(("V13", "S19", 0.2, 4.8, "Hồ Hoàn Kiếm cách khoảng mười hai cây số chim bay."))

# ---- CTA ----
FX.append(dict(t="text", s="S26L", x=60, y=360, w=960, size=84, text="XEM CHI TIẾT", at=0.3, color="#ffffff"))
FX.append(dict(t="text", s="S26L", x=60, y=480, w=960, size=60, text="[TÊN KÊNH / LIÊN HỆ]", at=1.0, color="#b6ff1a"))
FX.append(dict(t="text", s="S26L", x=60, y=1380, w=960, size=28, text="Thông tin tham khảo, cập nhật 11/2026. Khoảng cách tính theo đường chim bay. Ảnh vệ tinh và khối 3D mang tính minh hoạ, không phải hiện trạng.", at=0.2, color="#ffffff", plain=True))
VOICE.append(("V14", "S26L", 0.4, 3.8, "Muốn xem kỹ hơn, hãy liên hệ ngay."))


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
    layer = lambda sid, st, du, tr: f'<div class="clip layer" id="L_{sid}" data-start="{st}" data-duration="{du}" data-track-index="{100 + tr}"><svg class="ov" viewBox="0 0 1080 1920"></svg><div class="lab"></div></div>'  # noqa: E731
    for n, (sid, kind, src, st, du, mo, blur) in enumerate(SCENES):
        tr = n + 1
        if kind == "layer":
            els.append(layer(sid, st, du, tr))
            continue
        f = "assets/" + names[os.path.join(RAW, src)]
        if kind == "video":
            els.append(f'<video class="clip m" id="{sid}" src="{f}" muted playsinline data-start="{st}" data-duration="{du}" data-track-index="{tr}"></video>')
            els.append(layer(sid, st, du, tr))
        elif kind == "img":
            els.append(f'<img class="clip m" id="{sid}" src="{f}" alt="" data-start="{st}" data-duration="{du}" data-track-index="{tr}">')
            els.append(layer(sid, st, du, tr))
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
    lines = [dict(id=i, start=round(T0[s] + off, 2), allot=allot, text=text, scene=s) for i, s, off, allot, text in VOICE]
    json.dump(lines, open(os.path.join(HERE, "voice_lines_v3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(SCENES), "cảnh,", len(FX), "hiệu ứng, tổng", TOTAL, "s ->", OUT)


TEMPLATE = open(os.path.join(HERE, "draft2_template.html"), encoding="utf-8").read()

if __name__ == "__main__":
    build()
