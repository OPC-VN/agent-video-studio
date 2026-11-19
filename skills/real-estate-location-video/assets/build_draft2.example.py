#!/usr/bin/env python3
"""VÍ DỤ: dựng draft 2 (hiệu ứng + chữ) từ shot raw + lớp phủ chiếu từ toạ độ thật. Ghi comp2/.
Sao chép vào <project>/tools/, sửa PROJ/POI/VIEWS/SCENES/FX theo dự án; số liệu và nguồn lấy từ research."""
import json
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)
RAW = os.path.join(P, "raw")
OUT = os.path.join(P, "comp2")
SK = os.environ.get("SKILLS_DIR") or os.path.normpath(os.path.join(HERE, "..", ".."))  # thư mục skills/ của repo
sys.path.insert(0, os.path.join(SK, "land-plot-map-video", "assets"))
sys.path.insert(0, os.path.join(SK, "real-estate-location-video", "assets"))
import geo_cfg as G          # noqa: E402
import osm_overlay as OV     # noqa: E402
from PIL import Image        # noqa: E402

PROJ = (20.95374525, 105.93237025)
POI = {  # id: (nhãn, lat, lng, km chim bay)  — storyboard D.1
    "cv": ("Công viên Hồ Thiên Nga", 20.9558497, 105.9327031, "0,24"),
    "ku": ("BV Kusumi", 20.9635633, 105.9326817, "1,09"),
    "buv": ("ĐH Anh Quốc (BUV)", 20.9653857, 105.9315862, "1,30"),
    "oc": ("Vincom Ocean City", 20.951753, 105.9736312, "4,29"),
    "tt": ("Cầu Thanh Trì", 20.9945609, 105.9025736, "5,49"),
}
VIEWS = {  # tâm + zoom ô 256 px đúng lúc chụp
    "M01": (20.62, 106.27, 10.8), "M02": (20.95655, 105.93502, 14.5), "M03": (20.9738, 105.9530, 14.4),
    "M04": (PROJ[0], PROJ[1], 15.6), "M05": (20.9596, 105.9322, 16.8), "M06": (20.9732, 105.9381, 14.0),
}
OSM = json.load(open(os.path.join(RAW, "osm_overlays.json"), encoding="utf-8"))

# (id, loại, nguồn, bắt đầu, độ dài, chuyển động, nhòe vào)   loại: g = nhóm ảnh+lớp phủ (MapLibre), img, video
E2 = "earth-clean2/"
SCENES = [
    ("S01", "video", "cut/C_S01.mp4", 0.0, 1.0, None, False),
    ("S16", "video", "cut/C_S16.mp4", 1.0, 3.0, None, True),
    ("S02", "g", "maplibre/M01.png", 4.0, 2.0, (1.00, 1.10), True),
    ("S03a", "g", "maplibre/M02.png", 6.0, 1.2, (1.00, 1.08), True),
    ("S03b", "img", "earth-clean/R06.png", 7.2, 1.3, (1.00, 1.04), True),
    ("S04a", "img", "earth-clean/R06.png", 8.5, 2.8, (1.04, 1.10), False),
    ("S04b", "img", "earth-clean/R07.png", 11.3, 2.7, (1.10, 1.14), False),
    ("S04L", "layer", None, 8.5, 5.5, None, False),
    ("S06a", "img", "earth-clean/R08.png", 14.0, 0.75, (1.00, 1.08), True),
    ("S06b", "img", "earth-clean/R09.png", 14.75, 0.75, (1.00, 1.08), True),
    ("S06c", "img", "earth-clean/R10.png", 15.5, 0.75, (1.00, 1.08), True),
    ("S06d", "img", E2 + "R11.png", 16.25, 0.75, (1.00, 1.08), True),
    ("S08a", "video", "cut/C_S08.mp4", 17.0, 2.2, None, True),
    ("S08b", "img", E2 + "R14.png", 19.2, 1.8, (1.00, 1.10), True),
    ("S09", "g", "maplibre/M03.png", 21.0, 2.0, (1.00, 1.10), True),
    ("S10", "video", "cut/C_3D.mp4", 23.0, 5.0, None, True),
    ("S11", "g", "maplibre/M04.png", 28.0, 2.0, (1.00, 1.10), True),
    ("S13a", "g", "maplibre/M05.png", 30.0, 3.5, (1.00, 1.04), True),
    ("S13b", "g", "maplibre/M06.png", 33.5, 5.0, (1.00, 1.04), True),
    ("S19a", "img", "earth-clean/R18.png", 38.5, 1.2, (1.00, 1.12), True),
    ("S19b", "img", E2 + "R19.png", 39.7, 1.3, (1.12, 1.00), True),
    ("S26a", "img", "earth-clean/R11b.png", 41.0, 2.0, (1.00, 1.08), True),
    ("S26b", "img", E2 + "R21.png", 43.0, 2.0, (1.08, 1.00), False),
]
TOTAL = 45.0
T0 = {s[0]: s[3] for s in SCENES}
FX = []  # danh sách hiệu ứng cho trình thông dịch JS


def pt(view, lat, lng):
    la, lo, z = VIEWS[view]
    x, y = G.to_frame(lat, lng, (la, lo), z)
    return round(x, 1), round(y, 1)


def tags_layout(items):
    """items: [(x,y,l1,l2)] -> [(tx,ty,side)], tránh chồng: sắp theo y, đẩy xuống tối thiểu 120 px."""
    order = sorted(range(len(items)), key=lambda i: items[i][1])
    out = {}
    last = -999
    for i in order:
        x, y = items[i][0], items[i][1]
        ty = max(y - 40, last + 124, 330)
        side = "r" if x < 600 else "l"
        out[i] = (ty, side)
        last = ty
    return out


# ---------- hiệu ứng theo cảnh ----------
# S16: chữ hook
FX.append(dict(t="type", s="S16", x=60, y=300, w=960, size=66, text="SWAN LAKE ONSEN", at=1.2, per=0.05))
FX.append(dict(t="type", s="S16", x=60, y=385, w=960, size=66, text="RESIDENCES", at=2.0, per=0.05))
FX.append(dict(t="type", s="S16", x=60, y=480, w=960, size=50, text="ven [hồ Thiên Nga]", at=2.8, per=0.045, hl=True))

# S02: ranh tỉnh (cấp 4)
for d in OV.svg_paths(OSM["M01"]["b4"], VIEWS["M01"][:2], VIEWS["M01"][2], G, 1.2):
    FX.append(dict(t="path", s="S02", d=d, c="#27e6ff", w=8, at=0.3, dur=1.2))
x, y = pt("M01", *PROJ)
FX.append(dict(t="pin", s="S02", x=x, y=y, at=0.9))
FX.append(dict(t="text", s="S02", x=60, y=300, w=960, size=70, text="TỈNH HƯNG YÊN", at=0.6, color="#27e6ff"))
FX.append(dict(t="text", s="S02", x=60, y=1700, w=960, size=30, text="Tỉnh mới theo NQ 202/2025/QH15, hiệu lực 01/7/2025 · ranh: © OpenStreetMap, tham khảo", at=0.9, color="#ffffff", plain=True))

# S03a: ranh xã (cấp 6) + cấp 4
for d in OV.svg_paths(OSM["M02"]["b4"], VIEWS["M02"][:2], VIEWS["M02"][2], G, 1.2):
    FX.append(dict(t="path", s="S03a", d=d, c="#27e6ff", w=7, at=0.1, dur=0.9))
for d in OV.svg_paths(OSM["M02"]["b6"], VIEWS["M02"][:2], VIEWS["M02"][2], G, 1.2):
    FX.append(dict(t="path", s="S03a", d=d, c="#e4ff3a", w=4, at=0.2, dur=0.9))
x, y = pt("M02", *PROJ)
FX.append(dict(t="pin", s="S03a", x=x, y=y, at=0.5))
FX.append(dict(t="text", s="S03a", x=60, y=300, w=960, size=70, text="XÃ PHỤNG CÔNG", at=0.5, color="#e4ff3a"))
FX.append(dict(t="text", s="S03a", x=60, y=1700, w=960, size=30, text="Xã mới theo NQ 1666/NQ-UBTVQH15 (16/6/2025) · ranh: © OpenStreetMap, tham khảo", at=0.6, color="#ffffff", plain=True))

# S04: ba thẻ số (trên nền Earth)
CARDS = [("45.327", "người", "Xã Phụng Công · 14,61 km²", "VietnamPlus, 9/7/2026", 0.3),
         ("+10,72%", "GRDP", "Hưng Yên mới, 6 tháng 2026 · thứ 5/34", "báo Đại biểu Nhân dân, VOV", 2.3),
         ("20,23", "tỷ USD", "FDI luỹ kế · 1.006 dự án (đến 8/2026)", "VietnamPlus, 9/2026", 4.0)]
for i, (num, unit, cap, src, at) in enumerate(CARDS):
    FX.append(dict(t="card", s="S04L", i=i, num=num, unit=unit, cap=cap, src=src, at=at, y=300 + i * 330))

# S06: nhãn bậc zoom
for i, (sid, lab) in enumerate((("S06a", "x4"), ("S06b", "x3"), ("S06c", "x2"), ("S06d", "x1"))):
    FX.append(dict(t="text", s=sid, x=640, y=300, w=380, size=120, text=lab, at=0.05, color="#ffffff", right=True))

# S08: nhãn môi trường
FX.append(dict(t="chip", s="S08a", x=60, y=420, l1="Hồ Thiên Nga", l2="", at=0.8))
FX.append(dict(t="chip", s="S08b", x=60, y=420, l1="Công viên Hồ Thiên Nga", l2="0,24 km chim bay", at=0.1))

# S09: bố cục lân cận
x, y = pt("M03", *PROJ)
FX.append(dict(t="pin", s="S09", x=x, y=y, at=0.2))
FX.append(dict(t="tag", s="S09", x=x, y=y, tx=60, ty=300, side="r", l1="SWAN LAKE ONSEN", l2="Ecopark", at=0.3, color="#b6ff1a"))
for nm, la, lo, l2, at in (("VINHOMES OCEAN CITY", 20.951753, 105.9736312, "phía Đông", 0.8), ("OCEAN PARK 1", 20.9939238, 105.9595538, "phía Đông Bắc", 1.3)):
    px, py = pt("M03", la, lo)
    FX.append(dict(t="tag", s="S09", x=px, y=py, tx=0, ty=0, side="l", l1=nm, l2=l2, at=at, color="#ffd34d", auto=True))

# S10: nhãn 3D
FX.append(dict(t="text", s="S10", x=60, y=300, w=960, size=60, text="ẢNH VỆ TINH", at=0.2, color="#ffffff", out=2.6))
FX.append(dict(t="text", s="S10", x=60, y=300, w=960, size=60, text="KHỐI 3D MINH HOẠ", at=2.9, color="#ffd34d"))
FX.append(dict(t="text", s="S10", x=60, y=1700, w=960, size=30, text="Khối 3D từ dữ liệu © OpenStreetMap, minh hoạ, không phải hiện trạng", at=3.0, color="#ffffff", plain=True))

# S11: tuyến đường quanh (cấp trunk/primary/secondary)
road_lines = []
for r in OSM["M04"]["roads"]:
    if r["cls"] in ("motorway", "trunk", "primary", "secondary"):
        road_lines += r["lines"]
def _plen(d):
    pts = [tuple(map(float, p.split(","))) for p in d.replace("M", "").split(" L")]
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
_ds = sorted(OV.svg_paths(road_lines, VIEWS["M04"][:2], VIEWS["M04"][2], G, 1.5), key=_plen, reverse=True)
for d in [d for d in _ds if _plen(d) > 260][:14]:
    FX.append(dict(t="path", s="S11", d=d, c="#ffe14d", w=9, at=0.3, dur=1.2))
x, y = pt("M04", *PROJ)
FX.append(dict(t="pin", s="S11", x=x, y=y, at=0.2))
FX.append(dict(t="text", s="S11", x=60, y=300, w=960, size=60, text="ĐƯỜNG QUANH DỰ ÁN", at=0.4, color="#ffe14d"))
FX.append(dict(t="text", s="S11", x=60, y=1700, w=960, size=30, text="Tuyến đường chính: © OpenStreetMap, chưa có tên đường/lối vào được xác nhận", at=0.6, color="#ffffff", plain=True))


def build_13(sid, view, ids, delays, static):
    px, py = pt(view, *PROJ)
    FX.append(dict(t="pin", s=sid, x=px, y=py, at=0.1 if not static else 0.0))
    items = []
    for k in ids:
        nm, la, lo, km = POI[k]
        x, y = pt(view, la, lo)
        items.append((x, y, nm, km + " km chim bay", k))
    lay = tags_layout([(a, b, c, d) for a, b, c, d, _ in items])
    for i, (x, y, nm, l2, k) in enumerate(items):
        ty, side = lay[i]
        at = 0.0 if k in static else delays[k]
        FX.append(dict(t="dash", s=sid, x1=px, y1=py, x2=x, y2=y, at=at, dur=0.0 if k in static else 0.5))
        tx = 40 if side == "r" and x < 540 and False else None
        FX.append(dict(t="tag", s=sid, x=x, y=y, tx=0, ty=ty, side=side, l1=nm, l2=l2, at=at + (0.0 if k in static else 0.25), color="#ffffff", auto=True, fixed_y=ty))


build_13("S13a", "M05", ["cv", "ku", "buv"], {"cv": 0.4, "ku": 1.1, "buv": 1.9}, [])
build_13("S13b", "M06", ["cv", "ku", "buv", "oc", "tt"], {"oc": 1.2, "tt": 2.6}, ["cv", "ku", "buv"])

# S19: Hồ Hoàn Kiếm
FX.append(dict(t="chip", s="S19a", x=60, y=420, l1="DỰ ÁN", l2="", at=0.2))
FX.append(dict(t="chip", s="S19b", x=60, y=420, l1="HỒ HOÀN KIẾM", l2="11,76 km chim bay", at=0.1))
FX.append(dict(t="text", s="S19b", x=60, y=1700, w=960, size=30, text="Toạ độ OSM · tính ngày 19/11/2026 · đường chim bay", at=0.2, color="#ffffff", plain=True))

# S26: CTA
FX.append(dict(t="text", s="S26a", x=60, y=360, w=960, size=84, text="XEM CHI TIẾT", at=0.2, color="#ffffff"))
FX.append(dict(t="text", s="S26a", x=60, y=480, w=960, size=60, text="[TÊN KÊNH / LIÊN HỆ]", at=0.9, color="#b6ff1a"))
FX.append(dict(t="text", s="S26b", x=60, y=1560, w=960, size=28, text="Thông tin tham khảo, cập nhật 11/2026. Khoảng cách tính theo đường chim bay. Ảnh vệ tinh và khối 3D mang tính minh hoạ, không phải hiện trạng.", at=0.1, color="#ffffff", plain=True))


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
    # font
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
        else:  # g
            els.append(f'<div class="clip g" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="{tr}"><img class="m" src="{f}" alt=""><svg class="ov" viewBox="0 0 1080 1920"></svg><div class="lab"></div></div>')
            base_js.append(f'tl.fromTo("#{sid}", {{ scale: {mo[0]} }}, {{ scale: {mo[1]}, duration: {du}, ease: "none" }}, {st});')
        if blur:
            base_js.append(f'tl.fromTo("#{sid}", {{ filter: "blur(14px)" }}, {{ filter: "blur(0px)", duration: 0.25, ease: "power2.out" }}, {st});')
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
