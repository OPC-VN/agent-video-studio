"""Rà bố cục một short theo dữ liệu dựng (layout.json): khoảng trống, lệch, lặp, tập trung media.

Cách dùng:
    python gap_scan.py <layout.json> [--step 0.5] [--max-gap 1.0] [--min-size 300]
                       [--min-fill 0.45] [--max-offset 140] [--max-run 2] [--json]

`layout.json` do script dựng của short ghi ra cùng lúc sinh HTML (hợp đồng ở
references/qa-checklist.md):
    {"frame": {"w": 1080, "h": 1920}, "duration": 46.5,
     "zone": {"y0": 200, "y1": 1500},            vùng hoạt họa (trên dải phụ đề)
     "skip": [[0, 2.0], [44.0, 46.5]],           khoảng chỉ có hook / thẻ kết
     "elements": [{"id": "i1", "asset": "icons/post.png", "role": "icon",
                   "t_in": 8.9, "t_out": 14.6, "cx": 540, "cy": 700, "w": 420, "h": 400}],
     "scenes": [{"id": "A1", "t_in": 0.3, "t_out": 8.3, "layout": "V1", "motion": "flow-down"}]}

`role` ∈ icon · logo · media (video/ảnh lồng) · avatar · link · text. Mặc định là icon.

Kiểm tại mỗi bước `--step` giây:
    lỗi      không có phần tử nội dung (icon/logo/media) rộng ≥ min-size nằm trong vùng hoạt họa
             liên tục > max-gap giây · hai phần tử cùng `asset` hiện cùng lúc (trừ khi có
             "allow_repeat": true) · khung có media mà vẫn còn icon/logo khác · > max-run cảnh
             liền cùng `motion`
    cảnh báo nội dung chỉ phủ < min-fill chiều cao vùng (có trên thiếu dưới) · tâm nội dung lệch
             ngang > max-offset px khi khung không có avatar (dồn một bên) · > max-run cảnh liền
             cùng `layout`

Đây là đo máy theo toạ độ khai báo, không thay mắt người xem ảnh tĩnh.
Mã thoát: 0 đạt (có thể kèm cảnh báo) · 1 có lỗi · 2 gọi sai hoặc không đọc được file.
Chỉ dùng thư viện chuẩn Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CONTENT = {"icon", "logo", "media"}


def _spans(times, step):
    """Gộp các mốc liền nhau thành (đầu, cuối, độ dài)."""
    spans = []
    for t in times:
        if spans and abs(t - spans[-1][1] - step) < 1e-6:
            spans[-1][1] = t
        else:
            spans.append([t, t])
    return [(a, b, round(b - a + step, 3)) for a, b in spans]


def _fmt(spans):
    return ", ".join(f"{a:g}–{b:g} s" for a, b, _ in spans)


def _runs(scenes, key, max_run):
    found, run = [], []
    for scene in scenes + [None]:
        value = scene.get(key) if scene else None
        if run and value is not None and value == run[-1].get(key):
            run.append(scene)
            continue
        if len(run) > max_run and run[-1].get(key):
            found.append((run[0].get(key), [s.get("id") for s in run]))
        run = [scene] if scene else []
    return found


def check(data, step=0.5, max_gap=1.0, min_size=300, min_fill=0.45, max_offset=140, max_run=2):
    frame = data.get("frame") or {"w": 1080, "h": 1920}
    zone = data.get("zone") or {"y0": 200, "y1": 1500}
    duration = float(data["duration"])
    skip = [tuple(map(float, pair)) for pair in data.get("skip", [])]
    elements = data.get("elements", [])
    for e in elements:
        for key in ("id", "t_in", "t_out", "cx", "cy", "w"):
            if key not in e:
                raise ValueError(f"phần tử thiếu trường {key}: {e.get('id')}")
        e.setdefault("role", "icon")
        e.setdefault("h", e["w"])
    zone_h = zone["y1"] - zone["y0"]
    empty, thin, skew, dup, focus = [], [], [], {}, []
    steps = int(duration / step + 1e-6)
    for n in range(1, steps + 1):
        t = round(n * step, 3)
        if t >= duration or any(a <= t < b for a, b in skip):
            continue
        live = [e for e in elements if e["t_in"] <= t < e["t_out"]]
        content = [e for e in live if e["role"] in CONTENT]
        seen = {}
        for e in content:
            if e.get("asset") and not e.get("allow_repeat"):
                seen.setdefault(e["asset"], []).append(e["id"])
        for asset, ids in seen.items():
            if len(ids) > 1:
                dup.setdefault((asset, tuple(sorted(ids))), []).append(t)
        if any(e["role"] == "media" for e in content) and any(e["role"] != "media" for e in content):
            focus.append(t)
        main = [e for e in content if e["w"] >= min_size and zone["y0"] <= e["cy"] <= zone["y1"]]
        if not main:
            empty.append(t)
            continue
        if any(e["role"] == "media" for e in content):
            continue
        top = max(zone["y0"], min(e["cy"] - e["h"] / 2 for e in content))
        bottom = min(zone["y1"], max(e["cy"] + e["h"] / 2 for e in content))
        if (bottom - top) / zone_h < min_fill:
            thin.append(t)
        if not any(e["role"] == "avatar" for e in live):
            left = min(e["cx"] - e["w"] / 2 for e in content)
            right = max(e["cx"] + e["w"] / 2 for e in content)
            if abs((left + right) / 2 - frame["w"] / 2) > max_offset:
                skew.append(t)
    errors, warnings = [], []
    long_gaps = [s for s in _spans(empty, step) if s[2] > max_gap]
    if long_gaps:
        errors.append(f"vùng hoạt họa trống > {max_gap:g} s (không icon ≥ {min_size} px): {_fmt(long_gaps)}")
    for (asset, ids), times in sorted(dup.items()):
        errors.append(f"lặp cùng asset '{asset}' trong một khung ({', '.join(ids)}): {_fmt(_spans(times, step))}")
    if focus:
        errors.append(f"khung có media lồng mà còn icon/logo khác: {_fmt(_spans(focus, step))}")
    scenes = data.get("scenes", [])
    for value, ids in _runs(scenes, "motion", max_run):
        errors.append(f"{len(ids)} cảnh liền cùng kiểu chuyển động '{value}': {', '.join(map(str, ids))}")
    for value, ids in _runs(scenes, "layout", max_run):
        warnings.append(f"{len(ids)} cảnh liền cùng bố cục '{value}': {', '.join(map(str, ids))}")
    thin_spans = [s for s in _spans(thin, step) if s[2] > max_gap]
    if thin_spans:
        warnings.append(f"nội dung phủ < {min_fill:.0%} chiều cao vùng (có trên thiếu dưới): {_fmt(thin_spans)}")
    skew_spans = [s for s in _spans(skew, step) if s[2] > max_gap]
    if skew_spans:
        warnings.append(f"nội dung lệch ngang > {max_offset} px (dồn một bên): {_fmt(skew_spans)}")
    return {"ok": not errors, "steps": steps, "errors": errors, "warnings": warnings,
            "empty_steps": empty}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("layout")
    parser.add_argument("--step", type=float, default=0.5)
    parser.add_argument("--max-gap", type=float, default=1.0)
    parser.add_argument("--min-size", type=float, default=300)
    parser.add_argument("--min-fill", type=float, default=0.45)
    parser.add_argument("--max-offset", type=float, default=140)
    parser.add_argument("--max-run", type=int, default=2)
    parser.add_argument("--json", action="store_true", help="dòng cuối stdout là một object JSON")
    return parser


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    try:
        data = json.loads(Path(args.layout).read_text(encoding="utf-8"))
        if args.step <= 0:
            raise ValueError("--step phải dương")
        result = check(data, args.step, args.max_gap, args.min_size, args.min_fill,
                       args.max_offset, args.max_run)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"không đọc được layout: {exc}", file=sys.stderr)
        return 2
    for line in result["errors"]:
        print("LỖI: " + line, file=sys.stderr)
    for line in result["warnings"]:
        print("CẢNH BÁO: " + line, file=sys.stderr)
    if args.json:
        print(json.dumps(result, ensure_ascii=True))
    elif result["ok"]:
        print("ĐẠT: %d bước rà, %d cảnh báo" % (result["steps"], len(result["warnings"])),
              file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
