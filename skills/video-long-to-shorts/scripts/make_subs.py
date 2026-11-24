"""Sinh phụ đề dọc theo cụm 3–5 từ: CHỮ lấy nguyên từ nguồn, MỐC lấy từ nhận dạng giọng.

Cách dùng:
    python make_subs.py --source-map source-map.json --beats beats.json --out subs.json
                        [--asr asr-words.json] [--min-words 3] [--max-words 5] [--max-chars 28]
                        [--json]

Mỗi segment trong beats.json phải có `first_word` và `last_word` (id từ trong source-map).
Chữ phụ đề là dãy từ nguồn giữa hai id đó, không thêm bớt.

`--asr`: file JSON `[[start, end, "từ"], ...]` do công cụ nhận dạng giọng chạy trên CHÍNH file
voice.wav của short (mốc tính theo short). Chữ nguồn và chữ nhận dạng được so khớp; từ không
khớp thì nội suy giữa hai từ khớp gần nhất. Không có `--asr` thì dùng mốc hiển thị của nguồn
quy đổi sang short (`timing: "source"`): mốc này có thể lệch giọng 0,1–0,7 s, chỉ dùng cho bản
nháp và mã thoát là 1.

`--max-chars` là trần ký tự mỗi cụm, thay cho đo bề rộng bằng font thật (đo pixel ở bước dựng).
Mã thoát: 0 đạt · 1 ghi xong nhưng có cảnh báo (mốc nguồn, > 20 % từ không khớp, cụm vượt trần)
· 2 gọi sai hoặc dữ liệu không khớp.
Chỉ dùng thư viện chuẩn Python 3.9+.
"""
from __future__ import annotations

import argparse
import difflib
import json
import math
import re
import sys
from pathlib import Path


class InputError(Exception):
    pass


def norm(text):
    return re.sub(r"[^\w]", "", text.lower())


def segment_words(source_map, seg):
    words = source_map.get("words", [])
    index = {w["id"]: i for i, w in enumerate(words)}
    for key in ("first_word", "last_word"):
        if seg.get(key) not in index:
            raise InputError(f"{seg.get('id')}: {key} '{seg.get(key)}' không có trong source-map")
    a, b = index[seg["first_word"]], index[seg["last_word"]]
    if b < a:
        raise InputError(f"{seg['id']}: last_word đứng trước first_word")
    return words[a:b + 1]


def source_times(words, seg):
    """Mốc hiển thị của nguồn quy đổi sang short; từ thiếu mốc để None."""
    out = []
    for w in words:
        if w.get("t") is None:
            out.append(None)
        else:
            t = seg["short_in"] + (w["t"] - seg["src_tl_in"])
            out.append(min(max(t, seg["short_in"]), seg["short_out"]))
    return out


def asr_times(texts, asr):
    """So khớp chữ nguồn với chữ nhận dạng; trả (mốc, số từ không khớp)."""
    tokens = []                      # (chỉ số từ nguồn, mảnh đã chuẩn hoá)
    for i, text in enumerate(texts):
        for piece in re.split(r"[-\s]+", text):
            if norm(piece):
                tokens.append((i, norm(piece)))
    heard = [(float(a), norm(t)) for a, _b, t in asr if norm(t)]
    matcher = difflib.SequenceMatcher(None, [t for _, t in tokens], [t for _, t in heard],
                                      autojunk=False)
    times = [None] * len(texts)
    for block in matcher.get_matching_blocks():
        for k in range(block.size):
            i = tokens[block.a + k][0]
            if times[i] is None:
                times[i] = heard[block.b + k][0]
    return times, sum(1 for t in times if t is None)


def interpolate(times, lo, hi):
    """Lấp None bằng nội suy tuyến tính; hai đầu neo vào lo / hi."""
    n = len(times)
    out = list(times)
    for i in range(n):
        if out[i] is not None:
            continue
        left = next((j for j in range(i - 1, -1, -1) if out[j] is not None), None)
        right = next((j for j in range(i + 1, n) if times[j] is not None), None)
        t0 = out[left] if left is not None else lo
        t1 = times[right] if right is not None else hi
        i0 = left if left is not None else -1
        i1 = right if right is not None else n
        out[i] = t0 + (t1 - t0) * (i - i0) / (i1 - i0)
    for i in range(1, n):                       # không cho mốc đi lùi
        out[i] = max(out[i], out[i - 1])
    return out


def clauses(items, min_words):
    """Tách theo . ? ! và dấu phẩy khi mệnh đề đã đủ min_words; mệnh đề cụt dính vào mệnh đề sau."""
    parts, cur = [], []
    for item in items:
        cur.append(item)
        text = item[0]
        if re.search(r"[.?!…]$", text) or (text.endswith(",") and len(cur) >= min_words):
            parts.append(cur)
            cur = []
    if cur:
        parts.append(cur)
    merged = []
    for part in parts:
        if merged and len(merged[-1]) < min_words and not re.search(r"[.?!…]$", merged[-1][-1][0]):
            merged[-1] = merged[-1] + part
        else:
            merged.append(part)
    return merged


def chars(group):
    return len(" ".join(x[0] for x in group))


def split_even(clause, max_words, max_chars):
    n = len(clause)
    k = max(1, math.ceil(n / max_words))
    while True:
        base, extra = divmod(n, k)
        groups, i = [], 0
        for j in range(k):
            size = base + (1 if j < extra else 0)
            groups.append(clause[i:i + size])
            i += size
        if all(chars(g) <= max_chars for g in groups) or k >= n:
            return groups
        k += 1


def build(source_map, beats, asr=None, min_words=3, max_words=5, max_chars=28):
    warnings, subs, total, unmatched = [], [], 0, 0
    for seg in beats.get("segments", []):
        words = segment_words(source_map, seg)
        texts = [w["text"] for w in words]
        if asr is not None:
            window = [row for row in asr if seg["short_in"] - 0.5 <= float(row[0]) <= seg["short_out"] + 0.5]
            times, missed = asr_times(texts, window)
        else:
            times = source_times(words, seg)
            missed = sum(1 for t in times if t is None)
        total += len(words)
        unmatched += missed
        times = interpolate(times, seg["short_in"], seg["short_out"])
        times[0] = max(times[0], seg["short_in"])
        items = list(zip(texts, times))
        groups = [g for c in clauses(items, min_words) for g in split_even(c, max_words, max_chars)]
        for k, group in enumerate(groups):
            t0 = max(seg["short_in"], group[0][1] - 0.04)
            nxt = groups[k + 1][0][1] - 0.06 if k + 1 < len(groups) else seg["short_out"] + 0.2
            t1 = max(min(group[-1][1] + 0.55, nxt), t0 + 0.3)
            text = " ".join(x[0] for x in group)
            if len(text) > max_chars:
                warnings.append(f"{seg['id']}: cụm '{text}' dài {len(text)} ký tự (trần {max_chars})")
            subs.append({"segment": seg["id"], "t0": round(t0, 2), "t1": round(t1, 2), "text": text,
                         "words": [[x[0], round(x[1], 2)] for x in group]})
    if asr is None:
        warnings.append("mốc lấy từ nguồn (display_cue), chưa đối chiếu giọng: chỉ dùng cho bản nháp")
    if total and unmatched / total > 0.20:
        warnings.append(f"{unmatched}/{total} từ không có mốc khớp, đã nội suy: kiểm lại bằng tai")
    return {"schema_version": 1, "timing": "asr" if asr is not None else "source",
            "words_total": total, "words_interpolated": unmatched, "subs": subs,
            "warnings": warnings}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source-map", required=True)
    parser.add_argument("--beats", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--asr")
    parser.add_argument("--min-words", type=int, default=3)
    parser.add_argument("--max-words", type=int, default=5)
    parser.add_argument("--max-chars", type=int, default=28)
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
        beats = json.loads(Path(args.beats).read_text(encoding="utf-8"))
        asr = json.loads(Path(args.asr).read_text(encoding="utf-8")) if args.asr else None
        if not 1 <= args.min_words <= args.max_words:
            raise InputError("cần 1 ≤ min-words ≤ max-words")
        result = build(source_map, beats, asr, args.min_words, args.max_words, args.max_chars)
    except (OSError, ValueError, KeyError, TypeError, InputError) as exc:
        print(f"ĐẦU VÀO SAI: {exc}", file=sys.stderr)
        return 2
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8", newline="\n")
    for warning in result["warnings"]:
        print("CẢNH BÁO: " + warning, file=sys.stderr)
    if args.json:
        print(json.dumps({"ok": not result["warnings"], "subs": len(result["subs"]),
                          "timing": result["timing"],
                          "words_interpolated": result["words_interpolated"],
                          "warnings": len(result["warnings"])}, ensure_ascii=True))
    return 1 if result["warnings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
