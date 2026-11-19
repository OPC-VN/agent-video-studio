#!/usr/bin/env python3
"""So nhịp hai video qua `video/rhythm.md` của rea-video (mẫu vs bản dựng). Chỉ thư viện chuẩn, không mạng.

    python rhythm_align.py REF_DIR REMAKE_DIR [--tol 0.5] [--beats 0.5,5.3,6.8] [--json]

REF_DIR / REMAKE_DIR là thư mục `reference decompose`. Đọc các dòng «0.600s @18 change|first|cut» trong
`video/rhythm.md`. Trả: số cảnh, các mốc, recall (mốc của mẫu có mốc bản dựng trong ±tol), precision
(mốc bản dựng có mốc mẫu trong ±tol), và với --beats: độ lệch từ ranh beat tới mốc gần nhất mỗi bên.
Mã thoát 0 luôn (đây là bộ đo, không là cổng); ngưỡng do người dùng chốt.
"""
import argparse
import json
import os
import re
import sys

MARK = re.compile(r"(\d+(?:\.\d+)?)s @\d+ (first|change|cut)")
SHOT = re.compile(r"^- #(\d+):", re.M)


def read_marks(dirpath):
    path = os.path.join(dirpath, "video", "rhythm.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    marks = sorted({round(float(m.group(1)), 3) for m in MARK.finditer(text)})
    return {"shots": len(SHOT.findall(text)), "marks": marks,
            "cuts": sorted({round(float(m.group(1)), 3) for m in MARK.finditer(text) if m.group(2) == "first"} - {0.0})}


def _near(x, pool):
    return min(pool, key=lambda p: abs(p - x)) if pool else None


def align(ref, remake, tol=0.5, beats=()):
    r, m = ref["marks"], remake["marks"]
    hit_r = [x for x in r if _near(x, m) is not None and abs(_near(x, m) - x) <= tol]
    hit_m = [x for x in m if _near(x, r) is not None and abs(_near(x, r) - x) <= tol]
    out = {"tol_s": tol, "ref_shots": ref["shots"], "remake_shots": remake["shots"],
           "ref_hard_cuts": ref["cuts"], "remake_hard_cuts": remake["cuts"],
           "ref_marks": len(r), "remake_marks": len(m),
           "recall": round(len(hit_r) / len(r), 3) if r else None,
           "precision": round(len(hit_m) / len(m), 3) if m else None}
    if beats:
        rows = []
        for b in beats:
            nr, nm = _near(b, r), _near(b, m)
            rows.append({"beat_s": b, "ref_mark": nr, "ref_delta": None if nr is None else round(nr - b, 3),
                         "remake_mark": nm, "remake_delta": None if nm is None else round(nm - b, 3)})
        out["beats"] = rows
        out["beats_ref_within_tol"] = sum(1 for x in rows if x["ref_delta"] is not None and abs(x["ref_delta"]) <= tol)
        out["beats_remake_within_tol"] = sum(1 for x in rows if x["remake_delta"] is not None and abs(x["remake_delta"]) <= tol)
        out["beats_total"] = len(rows)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref")
    ap.add_argument("remake")
    ap.add_argument("--tol", type=float, default=0.5)
    ap.add_argument("--beats", default="", help="ranh beat (giây), cách nhau bằng dấu phẩy")
    a = ap.parse_args(argv)
    try:
        beats = [float(x) for x in a.beats.split(",") if x.strip()]
        res = align(read_marks(a.ref), read_marks(a.remake), a.tol, beats)
    except (OSError, ValueError) as e:
        print(f"[rhythm_align] LỖI: {e}", file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
