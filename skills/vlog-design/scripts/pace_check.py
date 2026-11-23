"""Kiểm nhịp một bảng cảnh (pacing.md) của video người + hoạt họa + màn hình.

Cách dùng:
    python pace_check.py <pacing.md> [--profile presenter|animation] [--person-min N] [--person-max N]
                         [--p-max 15] [--max-same-layout 3] [--max-scene 20] [--switch-max 45]
                         [--absent-max 60] [--index references/pattern-index.md] [--json]

Ngưỡng mặc định lấy từ bảng ngưỡng chung (references/workflow.md, bước 3):
    presenter: người xuất hiện 60–90%, người vắng liên tục ≤ absent-max giây (cảnh báo);
    animation: người xuất hiện 30–60%, không kiểm người vắng.
    --person-min / --person-max ghi đè khoảng của hồ sơ.

Đầu vào: file Markdown có một bảng với các cột (tên cột không phân biệt hoa thường):
    Cảnh | [Beat] | Từ | Đến | Chế độ | LY | TR | Chương
Thời gian dạng `mm:ss`, `h:mm:ss` hoặc số giây. Chế độ ∈ P, PA, A, S, PS, AS. TR = chuyển cảnh vào cảnh.

Kiểm:
    lỗi      tỉ lệ người ngoài khoảng · P > p-max % · > max-same-layout cảnh liền cùng LY (chế độ P/PA/A)
             · hở / chồng thời gian · mã LY sai dạng (LY-NN hoặc LY-NNa) · với --index: mã không có
             trong pattern-index hoặc đã bỏ
    cảnh báo cảnh liền cùng LY ở S/PS/AS · cảnh > max-scene s · giữ một chế độ > switch-max s
             · người vắng > absent-max s (presenter) · rời P sang PA/PS bằng TR-01

Mã thoát: 0 đạt (có thể kèm cảnh báo) · 1 có lỗi nhịp · 2 gọi sai hoặc không đọc được bảng.
Chỉ dùng thư viện chuẩn Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MODES = {"P", "PA", "A", "S", "PS", "AS"}
PERSON = {"P", "PA", "PS"}
SCREENISH = {"S", "PS", "AS"}
PROFILES = {"presenter": (60.0, 90.0), "animation": (30.0, 60.0)}
LY_RE = re.compile(r"(?i)LY-(\d{2})([a-z]?)")
ALIASES = {
    "scene": ("cảnh", "canh", "scene", "id"),
    "start": ("từ", "tu", "start", "from"),
    "end": ("đến", "den", "end", "to"),
    "mode": ("chế độ", "che do", "mode"),
    "layout": ("ly", "layout", "bố cục"),
    "transition": ("tr", "transition", "chuyển"),
    "chapter": ("chương", "chuong", "chapter"),
}


def parse_time(text: str) -> float:
    text = text.strip()
    if re.fullmatch(r"\d+(\.\d+)?", text):
        return float(text)
    parts = text.split(":")
    if not all(re.fullmatch(r"\d+(\.\d+)?", p) for p in parts) or not 2 <= len(parts) <= 3:
        raise ValueError(f"thời gian không hợp lệ: {text!r}")
    total = 0.0
    for p in parts:
        total = total * 60 + float(p)
    return total


def norm_ly(text: str) -> str:
    m = LY_RE.fullmatch(text.strip())
    return f"LY-{m.group(1)}{m.group(2).lower()}" if m else text.strip()


def read_index(path: Path) -> dict[str, str]:
    """pattern-index.md → {mã: trạng thái}."""
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and re.fullmatch(r"[A-Z]{2}-\d{2}[a-z]?", cells[0]):
            out[cells[0]] = cells[4]
    return out


def read_table(path: Path) -> list[dict]:
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    if len(rows) < 2:
        raise ValueError("không thấy bảng cảnh có tiêu đề và ít nhất một dòng")
    header = [h.lower() for h in rows[0]]
    index = {}
    for key, names in ALIASES.items():
        for i, h in enumerate(header):
            if h in names:
                index[key] = i
                break
    missing = [k for k in ("scene", "start", "end", "mode", "layout") if k not in index]
    if missing:
        raise ValueError(f"thiếu cột: {', '.join(missing)}")
    out = []
    for cells in rows[1:]:
        def get(k):
            return cells[index[k]] if k in index and index[k] < len(cells) else ""
        mode = get("mode").upper()
        if mode not in MODES:
            raise ValueError(f"cảnh {get('scene')}: chế độ {mode!r} không thuộc {sorted(MODES)}")
        start, end = parse_time(get("start")), parse_time(get("end"))
        if end <= start:
            raise ValueError(f"cảnh {get('scene')}: Đến phải lớn hơn Từ")
        out.append({"scene": get("scene"), "start": start, "end": end, "mode": mode,
                    "layout": norm_ly(get("layout")), "transition": get("transition").upper(),
                    "chapter": get("chapter")})
    return out


def check(rows: list[dict], a: argparse.Namespace, index: dict[str, str] | None = None) -> dict:
    errors, warnings = [], []
    pmin, pmax = PROFILES[a.profile]
    pmin = a.person_min if a.person_min is not None else pmin
    pmax = a.person_max if a.person_max is not None else pmax
    total = rows[-1]["end"] - rows[0]["start"]
    by_mode = {m: 0.0 for m in sorted(MODES)}
    for r in rows:
        by_mode[r["mode"]] += r["end"] - r["start"]
    share = {m: round(100 * v / total, 1) for m, v in by_mode.items()}
    person = round(sum(share[m] for m in PERSON), 1)
    if not pmin <= person <= pmax:
        errors.append(f"người xuất hiện {person}% ngoài khoảng {pmin:g}–{pmax:g}% (hồ sơ {a.profile})")
    if share["P"] > a.p_max:
        errors.append(f"P {share['P']}% > {a.p_max:g}%")
    for r in rows:
        if r["layout"] and not LY_RE.fullmatch(r["layout"]):
            errors.append(f"{r['scene']}: mã bố cục {r['layout']!r} sai dạng LY-NN")
        elif r["layout"] and index is not None:
            if r["layout"] not in index:
                errors.append(f"{r['scene']}: {r['layout']} không có trong pattern-index")
            elif index[r["layout"]] == "bỏ":
                errors.append(f"{r['scene']}: {r['layout']} đã bỏ")
    for prev, cur in zip(rows, rows[1:]):
        gap = round(cur["start"] - prev["end"], 2)
        if abs(gap) > 0.05:
            errors.append(f"{prev['scene']}→{cur['scene']}: {'hở' if gap > 0 else 'chồng'} {abs(gap)} s")
        if prev["mode"] == "P" and cur["mode"] in {"PA", "PS"} and cur["transition"] == "TR-01":
            warnings.append(f"{cur['scene']}: rời toàn khung bằng cắt cứng — nên co người (TR-03)")
    run = 1
    for prev, cur in zip(rows, rows[1:]):
        run = run + 1 if cur["layout"] and cur["layout"] == prev["layout"] else 1
        if run > a.max_same_layout:
            msg = f"{cur['scene']}: {run} cảnh liền cùng {cur['layout']}"
            (warnings if cur["mode"] in SCREENISH else errors).append(msg)
    for r in rows:
        if r["end"] - r["start"] > a.max_scene:
            warnings.append(f"{r['scene']}: dài {r['end'] - r['start']:.1f} s > {a.max_scene:g} s — cần chuyển động mới bên trong")
    last_switch, switches = rows[0]["start"], 0
    for prev, cur in zip(rows, rows[1:]):
        if cur["mode"] != prev["mode"]:
            switches += 1
            if cur["start"] - last_switch > a.switch_max:
                warnings.append(f"{prev['scene']}: giữ chế độ {prev['mode']} {cur['start'] - last_switch:.0f} s > {a.switch_max:g} s")
            last_switch = cur["start"]
    if rows[-1]["end"] - last_switch > a.switch_max:
        warnings.append(f"cuối video giữ chế độ {rows[-1]['mode']} {rows[-1]['end'] - last_switch:.0f} s > {a.switch_max:g} s")
    if a.profile == "presenter":
        absent_from = None
        for r in rows + [{"mode": "P", "start": rows[-1]["end"], "scene": "(hết)"}]:
            if r["mode"] in PERSON:
                if absent_from is not None and r["start"] - absent_from > a.absent_max:
                    warnings.append(f"người vắng {r['start'] - absent_from:.0f} s liền trước {r['scene']} > {a.absent_max:g} s")
                absent_from = None
            elif absent_from is None:
                absent_from = r["start"]
    return {"profile": a.profile, "scenes": len(rows), "duration_s": round(total, 1),
            "mode_share_pct": share, "person_pct": person, "mode_switches": switches,
            "avg_scene_s": round(total / len(rows), 1), "errors": errors, "warnings": warnings}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Kiểm nhịp bảng cảnh pacing.md")
    p.add_argument("file")
    p.add_argument("--profile", choices=sorted(PROFILES), default="presenter")
    p.add_argument("--person-min", type=float, default=None)
    p.add_argument("--person-max", type=float, default=None)
    p.add_argument("--p-max", type=float, default=15)
    p.add_argument("--max-same-layout", type=int, default=3)
    p.add_argument("--max-scene", type=float, default=20)
    p.add_argument("--switch-max", type=float, default=45)
    p.add_argument("--absent-max", type=float, default=60)
    p.add_argument("--index", default=None, help="pattern-index.md để kiểm mã LY tồn tại")
    p.add_argument("--json", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    for stream in (sys.stdout, sys.stderr):  # bảng mã console Windows mặc định không in được tiếng Việt
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        rows = read_table(Path(a.file))
        index = read_index(Path(a.index)) if a.index else None
    except (OSError, ValueError) as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 2
    result = check(rows, a, index)
    if a.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"{result['scenes']} cảnh · {result['duration_s']} s · TB {result['avg_scene_s']} s/cảnh · "
              f"đổi chế độ {result['mode_switches']} lần · người {result['person_pct']}% (hồ sơ {a.profile})")
        print("Tỉ lệ chế độ: " + ", ".join(f"{m} {v}%" for m, v in result["mode_share_pct"].items()))
        for e in result["errors"]:
            print(f"LỖI: {e}")
        for w in result["warnings"]:
            print(f"CẢNH BÁO: {w}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
