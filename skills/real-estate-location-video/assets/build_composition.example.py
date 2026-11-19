#!/usr/bin/env python3
"""Dựng composition HyperFrames bản RAW (chưa hiệu ứng) cho dự án mẫu từ shot đã quay.

    python build_composition.py            # ghi comp/index.html + comp/assets/
Scenes theo storyboard 45 s (bảng B, đã duyệt). Mỗi mục: id, loại (img|video), tệp, bắt đầu, độ dài, chuyển động.
Lõi chỉ thư viện chuẩn + Pillow (đổi PNG -> JPG nhẹ hơn).
"""
import json
import os
import shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)
RAW = os.path.join(P, "raw")
OUT = os.path.join(P, "comp")
ASSETS = os.path.join(OUT, "assets")

# (id, kind, source relative to raw/, start, dur, motion)   motion: (scale0, scale1, x0, x1, y0, y1)   blur=true: nhòe vào
SCENES = [
    ("S01a", "img", "earth-clean/R01.png", 0.0, 0.5, (1.00, 1.35, 0, 0, 0, 0), True),
    ("S01b", "img", "earth-clean/R02.png", 0.5, 0.5, (1.30, 1.00, 0, 0, 0, 0), True),
    ("S16", "video", "cut/C_S16.mp4", 1.0, 3.0, None, True),
    ("S02", "img", "maplibre/M01.png", 4.0, 2.0, (1.00, 1.22, 0, 0, 0, 0), True),
    ("S03a", "img", "maplibre/M02.png", 6.0, 1.2, (1.00, 1.15, 0, 0, 0, 0), True),
    ("S03b", "img", "earth-clean/R06.png", 7.2, 1.3, (1.00, 1.04, 0, 0, 0, 0), True),
    ("S04a", "img", "earth-clean/R06.png", 8.5, 2.8, (1.04, 1.10, 0, 0, 0, 0), False),
    ("S04b", "img", "earth-clean/R07.png", 11.3, 2.7, (1.10, 1.14, 0, 0, 0, 0), False),
    ("S06a", "img", "earth-clean/R08.png", 14.0, 0.75, (1.00, 1.08, 0, 0, 0, 0), True),
    ("S06b", "img", "earth-clean/R09.png", 14.75, 0.75, (1.00, 1.08, 0, 0, 0, 0), True),
    ("S06c", "img", "earth-clean/R10.png", 15.5, 0.75, (1.00, 1.08, 0, 0, 0, 0), True),
    ("S06d", "img", "earth-clean/R11.png", 16.25, 0.75, (1.00, 1.08, 0, 0, 0, 0), True),
    ("S08", "video", "cut/C_S08.mp4", 17.0, 4.0, None, True),
    ("S09", "img", "maplibre/M03.png", 21.0, 3.0, (1.00, 1.18, 0, 0, 0, 0), True),
    ("S10", "video", "cut/C_S10.mp4", 24.0, 3.0, None, True),
    ("S11", "img", "maplibre/M04.png", 27.0, 3.0, (1.00, 1.20, 0, 0, 0, -60), True),
    ("S13a", "img", "maplibre/M05.png", 30.0, 3.5, (1.00, 1.10, 0, 0, 0, 0), True),
    ("S13b", "img", "maplibre/M06.png", 33.5, 5.0, (1.00, 1.10, 0, 0, 0, 0), True),
    ("S19a", "img", "earth-clean/R18.png", 38.5, 1.2, (1.00, 1.12, 0, -40, 0, 0), True),
    ("S19b", "img", "earth-clean/R19.png", 39.7, 1.3, (1.12, 1.00, 40, 0, 0, 0), True),
    ("S26a", "img", "earth-clean/R11b.png", 41.0, 2.0, (1.00, 1.08, 0, 0, 0, 0), True),
    ("S26b", "img", "earth-clean/R20.png", 43.0, 2.0, (1.08, 1.00, 0, 0, 0, 0), False),
]
TOTAL = 45.0


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(ASSETS)
    names = {}
    for sid, kind, src, st, du, mo, blur in SCENES:
        full = os.path.join(RAW, src)
        if not os.path.isfile(full):
            raise SystemExit(f"thiếu {full}")
        if full not in names:
            base = os.path.splitext(os.path.basename(src))[0]
            if kind == "img":
                names[full] = base + ".jpg"
                Image.open(full).convert("RGB").save(os.path.join(ASSETS, names[full]), quality=92)
            else:
                names[full] = base + ".mp4"
                shutil.copy(full, os.path.join(ASSETS, names[full]))
    els, tw = [], []
    for n, (sid, kind, src, st, du, mo, blur) in enumerate(SCENES):
        f = "assets/" + names[os.path.join(RAW, src)]
        if kind == "img":
            els.append(f'<img class="clip m" id="{sid}" src="{f}" alt="" data-start="{st}" data-duration="{du}" data-track-index="{n + 1}">')
            s0, s1, x0, x1, y0, y1 = mo
            tw.append(f'tl.fromTo("#{sid}", {{ scale: {s0}, x: {x0}, y: {y0} }}, {{ scale: {s1}, x: {x1}, y: {y1}, duration: {du}, ease: "none" }}, {st});')
        else:
            els.append(f'<video class="clip m" id="{sid}" src="{f}" muted playsinline data-start="{st}" data-duration="{du}" data-track-index="{n + 1}"></video>')
        if blur:
            tw.append(f'tl.fromTo("#{sid}", {{ filter: "blur(14px)" }}, {{ filter: "blur(0px)", duration: 0.25, ease: "power2.out" }}, {st});')
    html = f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <title>swan-lake-onsen raw</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      html, body {{ margin: 0; padding: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #master-root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      .m {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; transform-origin: 50% 50%; }}
    </style>
  </head>
  <body>
    <!-- RAW: chỉ shot Google Earth/MapLibre đã quay, chưa hiệu ứng/chữ/giọng. Mốc theo storyboard 45 s. -->
    <div id="master-root" data-composition-id="master" data-width="1080" data-height="1920" data-start="0" data-duration="{TOTAL}">
      {chr(10).join("      " + e for e in els).strip()}
      <script>
        window.__timelines = window.__timelines || {{}};
        const tl = gsap.timeline({{ paused: true }});
        {chr(10).join("        " + t for t in tw).strip()}
        window.__timelines["master"] = tl;
      </script>
    </div>
  </body>
</html>
"""
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    json.dump([s[:5] for s in SCENES], open(os.path.join(P, "raw", "scenes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(SCENES), "cảnh,", TOTAL, "s ->", OUT)


if __name__ == "__main__":
    build()
