"""Cổng tự động cho file short đã render: kích thước, fps, thời lượng, âm lượng, lời vào sớm.

Cách dùng:
    python qa_short.py <short.mp4> [--width 1080] [--height 1920] [--fps 30]
                       [--min-dur 15] [--max-dur 90] [--lufs -14] [--lufs-tol 1.0]
                       [--tp-max -1.0] [--first-sound 0.5] [--noise-db -40]
                       [--ffmpeg-dir DIR] [--json]

Kiểm:
    khung       đúng width × height, fps đúng (lệch ≤ 0,01)
    thời lượng  trong [min-dur, max-dur] giây; có luồng audio
    âm lượng    tích hợp trong lufs ± lufs-tol (ebur128), true peak ≤ tp-max dBTP
    lời vào     tiếng đầu tiên vượt noise-db xuất hiện trong first-sound giây đầu

Cổng này không nghe được điểm cắt và không nhìn được bố cục: hai việc đó thuộc người duyệt
(references/qa-checklist.md).
Mã thoát: 0 đạt · 1 có mục không đạt · 2 gọi sai hoặc không đọc được file · 3 thiếu
ffmpeg/ffprobe. Tiến trình con gọi bằng danh sách đối số, không qua shell.
Chỉ dùng thư viện chuẩn Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


class ToolMissing(Exception):
    pass


class ProbeError(Exception):
    pass


def find_tool(name, tool_dir=None):
    found = shutil.which(name, path=str(tool_dir)) if tool_dir else shutil.which(name)
    if not found:
        raise ToolMissing(name)
    return found


def _run(argv, timeout=300):
    try:
        return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired as exc:
        raise ProbeError(f"{Path(argv[0]).name} quá {timeout} s") from exc


def parse_rate(text):
    num, _, den = (text or "0/1").partition("/")
    try:
        return float(num) / float(den or 1)
    except (ValueError, ZeroDivisionError):
        return 0.0


def parse_probe(payload):
    """JSON của ffprobe → {width, height, fps, duration, has_audio}."""
    streams = payload.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if video is None:
        raise ProbeError("file không có luồng video")
    duration = payload.get("format", {}).get("duration") or video.get("duration") or 0
    return {"width": int(video.get("width", 0)), "height": int(video.get("height", 0)),
            "fps": round(parse_rate(video.get("avg_frame_rate") or video.get("r_frame_rate")), 3),
            "duration": round(float(duration), 3),
            "has_audio": any(s.get("codec_type") == "audio" for s in streams)}


def parse_ebur128(stderr):
    """Khối Summary của bộ lọc ebur128 → (LUFS tích hợp, true peak) hoặc None."""
    tail = stderr[stderr.rfind("Summary:"):] if "Summary:" in stderr else ""
    lufs = re.search(r"\bI:\s*(-?\d+(?:\.\d+)?)\s*LUFS", tail)
    peak = re.search(r"\bPeak:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*dBFS", tail)
    def to_float(match):
        if match is None:
            return None
        return float("-inf") if "inf" in match.group(1) else float(match.group(1))

    return to_float(lufs), to_float(peak)


def parse_first_sound(stderr):
    """Đầu ra silencedetect → giây có tiếng đầu tiên (0.0 nếu file không mở bằng im lặng)."""
    start = re.search(r"silence_start:\s*(-?\d+(?:\.\d+)?)", stderr)
    if start is None or float(start.group(1)) > 0.02:
        return 0.0
    end = re.search(r"silence_end:\s*(-?\d+(?:\.\d+)?)", stderr)
    return None if end is None else float(end.group(1))


def evaluate(probe, lufs, peak, first_sound, args):
    rows = []

    def add(name, ok, got, want):
        rows.append({"check": name, "ok": bool(ok), "got": got, "want": want})

    add("frame", (probe["width"], probe["height"]) == (args.width, args.height),
        f"{probe['width']}x{probe['height']}", f"{args.width}x{args.height}")
    add("fps", abs(probe["fps"] - args.fps) <= 0.01, probe["fps"], args.fps)
    add("duration", args.min_dur <= probe["duration"] <= args.max_dur, probe["duration"],
        f"{args.min_dur:g}–{args.max_dur:g} s")
    add("audio_stream", probe["has_audio"], probe["has_audio"], True)
    if probe["has_audio"]:
        add("loudness", lufs is not None and abs(lufs - args.lufs) <= args.lufs_tol, lufs,
            f"{args.lufs:g} ± {args.lufs_tol:g} LUFS")
        add("true_peak", peak is not None and peak <= args.tp_max, peak, f"≤ {args.tp_max:g} dBTP")
        add("first_sound", first_sound is not None and first_sound <= args.first_sound,
            first_sound, f"≤ {args.first_sound:g} s")
    return rows


def measure(path, tool_dir=None):
    ffprobe, ffmpeg = find_tool("ffprobe", tool_dir), find_tool("ffmpeg", tool_dir)
    r = _run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    if r.returncode != 0:
        raise ProbeError(f"ffprobe không đọc được file: {r.stderr.strip()[:300]}")
    probe = parse_probe(json.loads(r.stdout or "{}"))
    lufs = peak = first = None
    if probe["has_audio"]:
        r = _run([ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af",
                  "ebur128=peak=true", "-f", "null", "-"])
        lufs, peak = parse_ebur128(r.stderr)
    return probe, lufs, peak, ffmpeg


def first_sound(path, ffmpeg, noise_db):
    r = _run([ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af",
              f"silencedetect=noise={noise_db:g}dB:d=0.05", "-f", "null", "-"])
    return parse_first_sound(r.stderr)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("video")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=float, default=30)
    parser.add_argument("--min-dur", type=float, default=15)
    parser.add_argument("--max-dur", type=float, default=90)
    parser.add_argument("--lufs", type=float, default=-14)
    parser.add_argument("--lufs-tol", type=float, default=1.0)
    parser.add_argument("--tp-max", type=float, default=-1.0)
    parser.add_argument("--first-sound", type=float, default=0.5)
    parser.add_argument("--noise-db", type=float, default=-40)
    parser.add_argument("--ffmpeg-dir")
    parser.add_argument("--json", action="store_true", help="dòng cuối stdout là một object JSON")
    return parser


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    path = Path(args.video)
    if not path.is_file():
        print(f"không thấy file: {path.name}", file=sys.stderr)
        return 2
    try:
        probe, lufs, peak, ffmpeg = measure(path, args.ffmpeg_dir)
        first = first_sound(path, ffmpeg, args.noise_db) if probe["has_audio"] else None
    except ToolMissing as exc:
        print(f"thiếu công cụ: {exc} (cài ffmpeg hoặc truyền --ffmpeg-dir)", file=sys.stderr)
        return 3
    except (ProbeError, ValueError) as exc:
        print(f"không đo được: {exc}", file=sys.stderr)
        return 2
    rows = evaluate(probe, lufs, peak, first, args)
    ok = all(r["ok"] for r in rows)
    for r in rows:
        print("%s %-12s đo %s · cần %s" % ("ĐẠT  " if r["ok"] else "TRƯỢT", r["check"], r["got"],
                                         r["want"]), file=sys.stderr)
    if args.json:
        print(json.dumps({"ok": ok, "file": path.name, "checks": rows}, ensure_ascii=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
