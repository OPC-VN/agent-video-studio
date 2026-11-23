"""Trích dữ liệu từ một video mẫu để học thành thư viện mẫu (xem references/corpus-study.md).

Cách dùng:
    python corpus_extract.py extract  --input V --out DIR [--every 2] [--width 1280] [--scene 0.25]
    python corpus_extract.py strips   --input V --out DIR --at 38.6,45.6 [--fps 10] [--window 2.4]
    python corpus_extract.py switches --log scene-log.md [--lead 1.2] [--per-pair 0]
    python corpus_extract.py stats    --log scene-log.md [--duration 767]

extract   khung mỗi --every giây (frames/f_NNNN.jpg, giây = (NNNN-1)*every), lưới 4x4 (sheets/s_NNN.jpg,
          trang N ô k ở giây (N-1)*16*every + k*every), mốc cắt cảnh (cuts.txt) và index.json.
strips    mỗi mốc một lưới 6x4 ở --fps khung/giây bắt đầu tại mốc (tr_<giây>.jpg), để soi cơ chế chuyển.
switches  đọc bảng nhật ký cảnh (cột thứ 2 là thời gian «m:ss–m:ss», cột thứ 3 là chế độ P/PA/A/S/PS/AS)
          và in mốc đổi chế độ, kèm mốc gợi ý cho strips (mốc đổi trừ --lead giây). --per-pair N giữ tối đa
          N mốc cho mỗi cặp từ → tới (kể cả chiều ngược) để phủ đều thay vì soi trùng.
stats     tính bằng máy (không để model cộng): tỉ lệ thời lượng từng chế độ, số lần đổi, độ dài cảnh,
          dòng có mốc vượt --duration, chỗ hở / chồng giữa các dòng. Dùng trước khi đưa số vào thư viện.

Cần: ffmpeg trên PATH (extract, strips). Mã thoát: 0 ok · 1 ffmpeg hỏng hoặc stats thấy mốc vượt thời
lượng · 2 gọi sai / không đọc được · 3 thiếu ffmpeg. Chỉ thư viện chuẩn Python 3.9+; tiến trình con luôn là argv list.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

MODES = {"P", "PA", "A", "S", "PS", "AS"}


def _ffmpeg() -> str | None:
    return shutil.which("ffmpeg")


def _run(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace")


def cmd_extract(a: argparse.Namespace) -> int:
    ff = _ffmpeg()
    if not ff:
        print("LỖI: không thấy ffmpeg trên PATH", file=sys.stderr)
        return 3
    src, out = Path(a.input), Path(a.out)
    if not src.is_file():
        print(f"LỖI: không có tệp {src}", file=sys.stderr)
        return 2
    (out / "frames").mkdir(parents=True, exist_ok=True)
    (out / "sheets").mkdir(parents=True, exist_ok=True)
    steps = [
        [ff, "-v", "error", "-y", "-i", str(src), "-vf", f"fps=1/{a.every},scale={a.width}:-2",
         "-q:v", "4", str(out / "frames" / "f_%04d.jpg")],
        [ff, "-v", "error", "-y", "-framerate", "1", "-i", str(out / "frames" / "f_%04d.jpg"),
         "-vf", "scale=480:270,tile=4x4:padding=4:color=white", "-q:v", "3",
         str(out / "sheets" / "s_%03d.jpg")],
    ]
    for argv in steps:
        r = _run(argv)
        if r.returncode != 0:
            print(f"LỖI ffmpeg: {r.stderr.strip()[-400:]}", file=sys.stderr)
            return 1
    r = _run([ff, "-v", "error", "-i", str(src), "-vf",
              f"scale=320:-2,select='gt(scene,{a.scene})',metadata=print:file=-", "-f", "null", "-"])
    cuts = re.findall(r"pts_time:([0-9.]+)", r.stdout)
    (out / "cuts.txt").write_text("\n".join(cuts) + ("\n" if cuts else ""), encoding="utf-8")
    frames = sorted((out / "frames").glob("f_*.jpg"))
    sheets = sorted((out / "sheets").glob("s_*.jpg"))
    index = {"source": src.name, "every_s": a.every, "frames": len(frames), "sheets": len(sheets),
             "sheet_span_s": 16 * a.every, "cuts": len(cuts),
             "frame_time": "(N-1)*every_s", "sheet_cell_time": "(N-1)*16*every_s + k*every_s"}
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(index, ensure_ascii=False))
    return 0


def cmd_strips(a: argparse.Namespace) -> int:
    ff = _ffmpeg()
    if not ff:
        print("LỖI: không thấy ffmpeg trên PATH", file=sys.stderr)
        return 3
    try:
        times = [float(t) for t in a.at.split(",") if t.strip()]
    except ValueError:
        print("LỖI: --at phải là danh sách giây cách nhau bằng dấu phẩy", file=sys.stderr)
        return 2
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cols, rows = 6, 4
    made = []
    for t in times:
        name = out / f"tr_{t:06.1f}.jpg"
        r = _run([ff, "-v", "error", "-y", "-ss", f"{max(t, 0):.2f}", "-i", a.input, "-t", f"{a.window}",
                  "-vf", f"fps={a.fps},scale=384:216,tile={cols}x{rows}:padding=3:color=white",
                  "-frames:v", "1", "-q:v", "3", str(name)])
        if r.returncode != 0:
            print(f"LỖI ffmpeg ở {t}: {r.stderr.strip()[-300:]}", file=sys.stderr)
            return 1
        made.append(name.name)
    print(json.dumps({"strips": made, "fps": a.fps, "cell_s": round(1 / a.fps, 3)}, ensure_ascii=False))
    return 0


def parse_time(text: str) -> float:
    parts = text.strip().split(":")
    total = 0.0
    for p in parts:
        total = total * 60 + float(p)
    return total


TIME = r"\d+:\d{2}(?::\d{2})?(?:\.\d+)?"


def parse_log(log_text: str) -> list[dict]:
    """Dòng bảng nhật ký: cột 1 số thứ tự, cột 2 «m:ss» hoặc «m:ss–m:ss», cột 3 chế độ."""
    rows = []
    for line in log_text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.fullmatch(r"\d+", cells[0]):
            continue
        times = re.findall(TIME, cells[1])
        mode = cells[2].upper().split()[0] if cells[2] else ""
        if not times or mode not in MODES:
            continue
        start = parse_time(times[0])
        end = parse_time(times[1]) if len(times) > 1 else None
        rows.append({"n": int(cells[0]), "start": start, "end": end, "mode": mode})
    for cur, nxt in zip(rows, rows[1:]):
        if cur["end"] is None:
            cur["end"] = nxt["start"]
    return rows


def find_switches(log_text: str, lead: float = 1.2, per_pair: int = 0) -> list[dict]:
    rows = parse_log(log_text)
    out, seen = [], {}
    for prev, cur in zip(rows, rows[1:]):
        if cur["mode"] != prev["mode"]:
            pair = (prev["mode"], cur["mode"])
            seen[pair] = seen.get(pair, 0) + 1
            if per_pair and seen[pair] > per_pair:
                continue
            out.append({"at": cur["start"], "from": prev["mode"], "to": cur["mode"],
                        "strip_at": round(max(cur["start"] - lead, 0), 1)})
    return out


def log_stats(log_text: str, duration: float | None = None) -> dict:
    rows = [r for r in parse_log(log_text) if r["end"] is not None]
    if not rows:
        return {"rows": 0}
    span = {}
    for r in rows:
        span[r["mode"]] = span.get(r["mode"], 0.0) + max(r["end"] - r["start"], 0)
    total = sum(span.values())
    lengths = [r["end"] - r["start"] for r in rows]
    gaps = [f"#{a['n']}→#{b['n']} {'hở' if b['start'] > a['end'] else 'chồng'} {abs(b['start'] - a['end']):.1f} s"
            for a, b in zip(rows, rows[1:]) if abs(b["start"] - a["end"]) > 0.05]
    over = [f"#{r['n']} kết thúc {r['end']:.0f} s > {duration:.0f} s"
            for r in rows if duration is not None and r["end"] > duration + 0.5]
    switches = sum(1 for a, b in zip(rows, rows[1:]) if a["mode"] != b["mode"])
    return {"rows": len(rows), "covered_s": round(total, 1),
            "mode_share_pct": {m: round(100 * v / total, 1) for m, v in sorted(span.items())},
            "person_pct": round(100 * sum(v for m, v in span.items() if m in {"P", "PA", "PS"}) / total, 1),
            "mode_switches": switches, "avg_scene_s": round(sum(lengths) / len(lengths), 1),
            "max_scene_s": round(max(lengths), 1), "gaps_or_overlaps": gaps, "beyond_duration": over}


def cmd_switches(a: argparse.Namespace) -> int:
    try:
        text = Path(a.log).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 2
    sw = find_switches(text, a.lead, a.per_pair)
    if not sw:
        print("LỖI: không thấy dòng bảng có thời gian + chế độ hợp lệ", file=sys.stderr)
        return 2
    print(json.dumps({"switches": sw, "strip_at": ",".join(str(s["strip_at"]) for s in sw)},
                     ensure_ascii=False))
    return 0


def cmd_stats(a: argparse.Namespace) -> int:
    try:
        text = Path(a.log).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 2
    st = log_stats(text, a.duration)
    if not st.get("rows"):
        print("LỖI: không thấy dòng bảng có thời gian + chế độ hợp lệ", file=sys.stderr)
        return 2
    print(json.dumps(st, ensure_ascii=False))
    return 1 if st["beyond_duration"] else 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # console Windows mặc định không in được tiếng Việt
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Trích dữ liệu video mẫu cho việc học bộ mẫu")
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--input", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--every", type=float, default=2)
    e.add_argument("--width", type=int, default=1280)
    e.add_argument("--scene", type=float, default=0.25)
    s = sub.add_parser("strips")
    s.add_argument("--input", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--at", required=True)
    s.add_argument("--fps", type=float, default=10)
    s.add_argument("--window", type=float, default=2.4)
    w = sub.add_parser("switches")
    w.add_argument("--log", required=True)
    w.add_argument("--lead", type=float, default=1.2)
    w.add_argument("--per-pair", type=int, default=0)
    st = sub.add_parser("stats")
    st.add_argument("--log", required=True)
    st.add_argument("--duration", type=float, default=None)
    a = p.parse_args(argv)
    return {"extract": cmd_extract, "strips": cmd_strips, "switches": cmd_switches, "stats": cmd_stats}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
