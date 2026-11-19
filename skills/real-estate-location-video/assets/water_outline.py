#!/usr/bin/env python3
"""Lấy viền một mặt nước (hồ) từ mặt nạ trắng-đen do `maplibre_shots.mjs` chụp ở mode `mask-water`.

Mặt nạ cùng tâm + zoom với ảnh nền nên viền khớp đúng ảnh. Chọn thành phần nước chứa (hoặc gần nhất) điểm hạt giống
`seed` (toạ độ px trên khung), dò viền ngoài, rút gọn, trả một chuỗi `d` của <path> (vẽ dần bằng pathLength=1).
Cần numpy + scipy + Pillow.

    python water_outline.py N01w.png 560 1180 [--eps 1.4] [--max-gap 90]
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

_DIRS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]  # (dy, dx) theo chiều kim đồng hồ


def pick_component(mask, seed, max_gap=90):
    """Nhãn thành phần chứa `seed`; nếu seed ở ngoài nước thì lấy thành phần gần nhất trong `max_gap` px, không thì None."""
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    x, y = int(seed[0]), int(seed[1])
    h, w = mask.shape
    if 0 <= y < h and 0 <= x < w and lab[y, x]:
        return lab == lab[y, x]
    dist, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    yy, xx = min(max(y, 0), h - 1), min(max(x, 0), w - 1)
    if dist[yy, xx] > max_gap:
        return None
    return lab == lab[iy[yy, xx], ix[yy, xx]]


def trace_outer(comp):
    """Dò viền ngoài (Moore neighbour) của thành phần liên thông; trả [(x, y), ...] khép kín."""
    ys, xs = np.nonzero(comp)
    start = (int(ys.min()), int(xs[ys == ys.min()].min()))
    h, w = comp.shape
    pad = np.zeros((h + 2, w + 2), bool)
    pad[1:-1, 1:-1] = comp
    cur = (start[0] + 1, start[1] + 1)
    first = cur
    back = 6  # hướng từ điểm hiện tại tới ô nền đã biết (điểm đầu: phía Tây là nền)
    pts = [cur]
    index = {d: i for i, d in enumerate(_DIRS)}
    for _ in range(4 * h * w):
        moved = False
        for k in range(1, 9):
            d = (back + k) % 8
            ny, nx = cur[0] + _DIRS[d][0], cur[1] + _DIRS[d][1]
            if pad[ny, nx]:
                py, px = cur[0] + _DIRS[(d - 1) % 8][0], cur[1] + _DIRS[(d - 1) % 8][1]  # ô nền vừa duyệt
                back = index[(py - ny, px - nx)]
                cur, moved = (ny, nx), True
                break
        if not moved or cur == first:
            break
        pts.append(cur)
    return [(x - 1, y - 1) for y, x in pts]


def simplify(pts, eps):
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


def outline(mask_png, seed, eps=1.4, max_gap=90, close_px=3):
    """Đường viền (list[(x, y)]) của hồ chứa `seed`; None nếu không có nước gần seed."""
    img = np.asarray(Image.open(mask_png).convert("L")) > 127
    if close_px:  # nối các khe nhỏ do ô vector cắt
        img = ndimage.binary_closing(img, structure=np.ones((3, 3)), iterations=close_px)
    comp = pick_component(img, seed, max_gap)
    if comp is None:
        return None
    comp = ndimage.binary_fill_holes(comp)
    return simplify(trace_outer(comp), eps), comp


def to_svg_d(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        print(__doc__)
        return 2
    eps = float(a[a.index("--eps") + 1]) if "--eps" in a else 1.4
    gap = int(a[a.index("--max-gap") + 1]) if "--max-gap" in a else 90
    res = outline(a[0], (float(a[1]), float(a[2])), eps, gap)
    if res is None:
        print("không có nước gần seed")
        return 1
    pts, comp = res
    ys, xs = np.nonzero(comp)
    print(f"{len(pts)} điểm; bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}; diện tích {int(comp.sum())} px")
    print(to_svg_d(pts)[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
