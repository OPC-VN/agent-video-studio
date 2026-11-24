"""Ghép giọng của một short từ bản đồ audio nhiều clip, ghi voice.wav + beats.json.

Cách dùng:
    python cut_voice.py --source-map source-map.json --plan beats-plan.json --media-root DIR
                        --out voice.wav --beats-out beats.json [--json]

`beats-plan.json` (mẫu: assets/templates/beats.json):
    {"lead": 0.30, "gap": 0.30, "fade_ms": 25, "tail": 2.5,
     "segments": [{"id": "S1", "tl_in": 246.92, "tl_out": 254.95,
                   "clip": "voice", "gap_after": 0.30, "first_word": "k9w3", "last_word": "k12w5"}]}

`tl_in` / `tl_out` là giây trên timeline bản dài, ĐÃ chỉnh theo số đo (khoảng lặng, trũng năng
lượng), không phải mốc kế hoạch. Mỗi đoạn phải nằm trọn trong MỘT clip audio của bản đồ; đoạn
vắt qua ranh clip thì tách làm hai. `clip` bỏ trống → chọn clip phủ đoạn có volume lớn nhất
(hoà thì mã 2: ghi rõ `clip`). Quy đổi: media = t − start + media_start.

Mỗi đoạn được fade cos hai đầu (`fade_ms`), đặt sau `lead` giây im; giữa các đoạn chèn
`gap_after` (mặc định `gap`); cuối thêm `tail` giây im cho thẻ kết. Với mỗi đoạn, script còn tính
offset avatar: clip video có cờ avatar phủ `tl_in` → `media_start` để đặt vào `data-media-start`.

Chỉ đọc WAV PCM 16-bit; mọi nguồn cùng tần số lấy mẫu và số kênh (đổi trước bằng ffmpeg nếu khác).
Mã thoát: 0 xong · 1 lỗi dữ liệu âm (thiếu file, không phải PCM 16-bit, đoạn vượt độ dài file)
· 2 gọi sai hoặc plan không khớp bản đồ.
Chỉ dùng thư viện chuẩn Python 3.9+.
"""
from __future__ import annotations

import argparse
import array
import json
import math
import sys
import wave
from pathlib import Path


class PlanError(Exception):
    """Plan hoặc bản đồ sai: mã 2."""


class AudioError(Exception):
    """Dữ liệu âm không dùng được: mã 1."""


def media_time(clip, t):
    """Giây trên timeline → giây trong file của clip."""
    return t - clip["start"] + clip.get("media_start", 0.0)


def pick_clip(audio, seg):
    a, b = seg["tl_in"], seg["tl_out"]
    if not b > a:
        raise PlanError(f"{seg['id']}: tl_out phải lớn hơn tl_in")
    covering = [c for c in audio if c["end"] is not None and c["start"] - 1e-6 <= a
                and b <= c["end"] + 1e-6]
    if seg.get("clip"):
        chosen = [c for c in covering if c["id"] == seg["clip"]]
        if not chosen:
            raise PlanError(f"{seg['id']}: clip '{seg['clip']}' không phủ {a}–{b} s")
        return chosen[0]
    if not covering:
        raise PlanError(f"{seg['id']}: không clip audio nào phủ trọn {a}–{b} s "
                        "(đoạn vắt qua ranh clip thì tách làm hai)")
    top = max(c.get("volume", 1.0) for c in covering)
    best = [c for c in covering if c.get("volume", 1.0) == top]
    if len(best) > 1:
        raise PlanError(f"{seg['id']}: {len(best)} clip cùng phủ đoạn, ghi rõ trường clip")
    return best[0]


def avatar_at(videos, seg):
    """Clip avatar phủ đầu đoạn và offset cần đặt vào data-media-start."""
    for v in videos:
        if v.get("avatar") and v["end"] is not None and v["start"] <= seg["tl_in"] < v["end"]:
            return {"id": v["id"], "src": v["src"],
                    "media_start": round(media_time(v, seg["tl_in"]), 3),
                    "covers_segment": seg["tl_out"] <= v["end"] + 1e-6}
    return None


def read_wav(path):
    try:
        with wave.open(str(path), "rb") as w:
            if w.getsampwidth() != 2 or w.getcomptype() != "NONE":
                raise AudioError(f"{path.name}: cần WAV PCM 16-bit")
            samples = array.array("h")
            samples.frombytes(w.readframes(w.getnframes()))
            if sys.byteorder == "big":
                samples.byteswap()
            return samples, w.getframerate(), w.getnchannels()
    except (OSError, EOFError, wave.Error) as exc:
        raise AudioError(f"không đọc được {path.name}: {exc}") from exc


def cut(samples, rate, channels, t0, t1, fade_s):
    i0, i1 = int(round(t0 * rate)), int(round(t1 * rate))
    if i0 < 0 or i1 * channels > len(samples):
        raise AudioError(f"đoạn {t0:.3f}–{t1:.3f} s vượt độ dài file ({len(samples) / channels / rate:.3f} s)")
    part = array.array("h", samples[i0 * channels:i1 * channels])
    frames = i1 - i0
    n = min(int(fade_s * rate), frames // 2)
    for k in range(n):
        gain = 0.5 - 0.5 * math.cos(math.pi * k / n)
        for ch in range(channels):
            head, tail = k * channels + ch, (frames - 1 - k) * channels + ch
            part[head] = int(part[head] * gain)
            part[tail] = int(part[tail] * gain)
    return part


def assemble(source_map, plan, media_root):
    segments = plan.get("segments") or []
    if not segments:
        raise PlanError("plan không có segments")
    lead, gap = float(plan.get("lead", 0.30)), float(plan.get("gap", 0.30))
    fade_s, tail = float(plan.get("fade_ms", 25)) / 1000.0, float(plan.get("tail", 0.0))
    cache, fmt, out, report = {}, None, array.array("h"), []
    for seg in segments:
        for key in ("id", "tl_in", "tl_out"):
            if key not in seg:
                raise PlanError(f"segment thiếu trường {key}")
        clip = pick_clip(source_map.get("audio", []), seg)
        if not clip.get("src"):
            raise PlanError(f"{seg['id']}: clip '{clip['id']}' không có src")
        if clip["src"] not in cache:
            cache[clip["src"]] = read_wav(media_root / clip["src"])
        samples, rate, channels = cache[clip["src"]]
        if fmt is None:
            fmt = (rate, channels)
            out.extend([0] * int(round(lead * rate)) * channels)
        elif fmt != (rate, channels):
            raise AudioError(f"{clip['src']}: tần số/số kênh khác nguồn trước ({rate} Hz, {channels} kênh)")
        m0, m1 = media_time(clip, seg["tl_in"]), media_time(clip, seg["tl_out"])
        short_in = len(out) / channels / rate
        out.extend(cut(samples, rate, channels, m0, m1, fade_s))
        short_out = len(out) / channels / rate
        row = {"id": seg["id"], "clip": clip["id"], "src": clip["src"],
               "src_tl_in": seg["tl_in"], "src_tl_out": seg["tl_out"],
               "media_in": round(m0, 3), "media_out": round(m1, 3),
               "short_in": round(short_in, 3), "short_out": round(short_out, 3),
               "avatar": avatar_at(source_map.get("videos", []), seg)}
        for key in ("first_word", "last_word", "note"):
            if key in seg:
                row[key] = seg[key]
        report.append(row)
        pause = tail if seg is segments[-1] else float(seg.get("gap_after", gap))
        out.extend([0] * int(round(pause * rate)) * channels)
    rate, channels = fmt
    peak = max((abs(s) for s in out), default=0) / 32768.0
    beats = {"schema_version": 1, "total": round(len(out) / channels / rate, 3),
             "sample_rate": rate, "channels": channels, "lead": lead,
             "fade_ms": round(fade_s * 1000, 1), "peak": round(peak, 4), "segments": report}
    return out, beats


def write_wav(path, samples, rate, channels):
    data = array.array("h", samples)
    if sys.byteorder == "big":
        data.byteswap()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data.tobytes())


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source-map", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--media-root", required=True,
                        help="thư mục gốc để giải src của clip audio (thư mục chứa index.html nguồn)")
    parser.add_argument("--out", required=True)
    parser.add_argument("--beats-out", required=True)
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
        source_map = json.loads(Path(args.source_map).read_text(encoding="utf-8"))
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"không đọc được đầu vào: {exc}", file=sys.stderr)
        return 2
    try:
        samples, beats = assemble(source_map, plan, Path(args.media_root))
    except PlanError as exc:
        print(f"PLAN SAI: {exc}", file=sys.stderr)
        return 2
    except AudioError as exc:
        print(f"LỖI ÂM: {exc}", file=sys.stderr)
        return 1
    write_wav(Path(args.out), samples, beats["sample_rate"], beats["channels"])
    Path(args.beats_out).write_text(json.dumps(beats, ensure_ascii=False, indent=1) + "\n",
                                    encoding="utf-8", newline="\n")
    for row in beats["segments"]:
        print("%(id)s %(clip)s media %(media_in).3f–%(media_out).3f → short %(short_in).3f–%(short_out).3f"
              % row, file=sys.stderr)
    if args.json:
        print(json.dumps({"ok": True, "total": beats["total"], "segments": len(beats["segments"]),
                          "peak": beats["peak"]}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
