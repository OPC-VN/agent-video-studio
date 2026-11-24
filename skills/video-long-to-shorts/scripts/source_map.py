"""Bóc bản đồ nguồn từ một composition HyperFrames (chỉ đọc) ra source-map.json.

Cách dùng:
    python source_map.py <index.html> [--out source-map.json] [--line-class kara] [--word-class w]
                         [--avatar-class avatar] [--json]

Đọc:
    section[data-start]            → sections (id, class, start, end)
    audio[data-start]              → audio   (id, src, start, end, media_start, volume)
    video[data-start]              → videos  (id, src, start, end, media_start, avatar)
    phần tử có class --line-class  → lines   (id, text, start, end) gồm các từ con có class --word-class
    từ (phần tử con có id)         → words   (id, text, line, t)

Mốc từ `t` = vị trí (đối số cuối) của lệnh GSAP đầu tiên nhắm `'#<id từ>'`, ví dụ
`tl.to('#k3w2',{...},12.4)` hoặc `tl.fromTo('#k3w2',{...},{...},12.4)`. Đây là mốc hiển thị chữ,
KHÔNG phải mốc giọng: nó có thể lệch giọng thật vài phần mười giây (xem
references/audio-cut-and-sync.md). Video là avatar khi class chứa --avatar-class hoặc có
`data-role="avatar"`. Quy đổi thời gian: media = t − start + media_start.

Mã thoát: 0 ghi xong · 1 ghi xong nhưng thiếu dữ liệu cần cho short (không có audio, không có
từ, hoặc có từ thiếu mốc) · 2 gọi sai hoặc không đọc được file.
Chỉ dùng thư viện chuẩn Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SCHEMA_VERSION = 1
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
        "track", "wbr"}
_NUM = r"(-?\d+(?:\.\d+)?)"
_OBJ = r"\{[^{}]*\}"
GSAP_CALL = re.compile(
    r"\.\w+\(\s*['\"]#([\w-]+)['\"]\s*,\s*" + _OBJ + r"\s*(?:,\s*" + _OBJ + r"\s*)?,\s*" + _NUM + r"\s*\)")


def _num(attrs, key, default=None):
    try:
        return float(attrs[key])
    except (KeyError, TypeError, ValueError):
        return default


def _clip(attrs):
    start = _num(attrs, "data-start")
    if start is None:
        return None
    duration = _num(attrs, "data-duration")
    return {"id": attrs.get("id"), "src": attrs.get("src"), "start": start,
            "end": None if duration is None else round(start + duration, 3),
            "media_start": _num(attrs, "data-media-start", 0.0)}


class _Reader(HTMLParser):
    def __init__(self, line_class, word_class, avatar_class):
        super().__init__(convert_charrefs=True)
        self.line_class, self.word_class, self.avatar_class = line_class, word_class, avatar_class
        self.sections, self.audio, self.videos, self.lines, self.words = [], [], [], [], []
        self.duration = None
        self._stack = []          # tên thẻ đang mở
        self._line = None         # (độ sâu, dict dòng)
        self._word = None         # (độ sâu, dict từ)

    def handle_starttag(self, tag, attr_list):
        attrs = {k: (v or "") for k, v in attr_list}
        classes = attrs.get("class", "").split()
        if "data-composition-id" in attrs and self.duration is None:
            self.duration = _num(attrs, "data-duration")
        if tag == "section":
            clip = _clip(attrs)
            if clip:
                self.sections.append({"id": clip["id"], "class": attrs.get("class", ""),
                                      "start": clip["start"], "end": clip["end"]})
        elif tag == "audio":
            clip = _clip(attrs)
            if clip:
                clip["volume"] = _num(attrs, "data-volume", 1.0)
                self.audio.append(clip)
        elif tag == "video":
            clip = _clip(attrs)
            if clip:
                clip["avatar"] = (self.avatar_class in classes
                                  or attrs.get("data-role") == "avatar")
                self.videos.append(clip)
        if self._line is None and self.line_class in classes and attrs.get("id"):
            self._line = (len(self._stack), {"id": attrs["id"], "words": []})
        elif (self._line is not None and self._word is None and self.word_class in classes
              and attrs.get("id")):
            self._word = (len(self._stack), {"id": attrs["id"], "text": "",
                                             "line": self._line[1]["id"]})
        if tag not in VOID:
            self._stack.append(tag)

    def handle_startendtag(self, tag, attr_list):
        self.handle_starttag(tag, attr_list)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag not in self._stack:
            return
        while self._stack:
            closed = self._stack.pop()
            depth = len(self._stack)
            if self._word is not None and depth == self._word[0]:
                word = self._word[1]
                word["text"] = " ".join(word["text"].split())
                if word["text"]:
                    self.words.append(word)
                    self._line[1]["words"].append(word)
                self._word = None
            if self._line is not None and depth == self._line[0]:
                self.lines.append(self._line[1])
                self._line = None
            if closed == tag:
                break

    def handle_data(self, data):
        if self._word is not None:
            self._word[1]["text"] += data


def word_times(html):
    """{id: mốc} — lệnh GSAP đầu tiên nhắm từng id."""
    times = {}
    for match in GSAP_CALL.finditer(html):
        times.setdefault(match.group(1), float(match.group(2)))
    return times


def build(html, source_name, line_class="kara", word_class="w", avatar_class="avatar"):
    reader = _Reader(line_class, word_class, avatar_class)
    reader.feed(html)
    reader.close()
    times = word_times(html)
    for word in reader.words:
        word["t"] = times.get(word["id"])
    lines = []
    for line in reader.lines:
        stamped = [w["t"] for w in line["words"] if w["t"] is not None]
        lines.append({"id": line["id"], "text": " ".join(w["text"] for w in line["words"]),
                      "start": min(stamped) if stamped else None,
                      "end": max(stamped) if stamped else None,
                      "word_ids": [w["id"] for w in line["words"]]})
    lines.sort(key=lambda r: (r["start"] is None, r["start"] or 0.0))
    return {"schema_version": SCHEMA_VERSION, "source": source_name, "duration": reader.duration,
            "time_base": "timeline", "word_time_kind": "display_cue",
            "sections": reader.sections, "audio": reader.audio, "videos": reader.videos,
            "lines": lines,
            "words": [{"id": w["id"], "text": w["text"], "line": w["line"], "t": w["t"]}
                      for w in reader.words]}


def problems(data):
    found = []
    if not data["audio"]:
        found.append("không có clip <audio data-start>: không lập được bản đồ giọng")
    if not data["words"]:
        found.append("không tìm thấy từ nào (kiểm --line-class / --word-class)")
    missing = sum(1 for w in data["words"] if w["t"] is None)
    if missing:
        found.append(f"{missing} từ thiếu mốc GSAP: lấy mốc bằng nhận dạng giọng trên file audio")
    return found


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("html")
    parser.add_argument("--out", default="source-map.json")
    parser.add_argument("--line-class", default="kara")
    parser.add_argument("--word-class", default="w")
    parser.add_argument("--avatar-class", default="avatar")
    parser.add_argument("--json", action="store_true", help="dòng cuối stdout là một object JSON")
    return parser


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    src = Path(args.html)
    try:
        html = src.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"không đọc được {src.name}: {exc}", file=sys.stderr)
        return 2
    data = build(html, src.name, args.line_class, args.word_class, args.avatar_class)
    warnings = problems(data)
    data["warnings"] = warnings
    out = Path(args.out)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                   newline="\n")
    summary = {"ok": not warnings, "out": out.name, "sections": len(data["sections"]),
               "audio": len(data["audio"]), "videos": len(data["videos"]),
               "lines": len(data["lines"]), "words": len(data["words"]), "warnings": warnings}
    for warning in warnings:
        print("CẢNH BÁO: " + warning, file=sys.stderr)
    if args.json:
        print(json.dumps(summary, ensure_ascii=True))
    else:
        print("sections %(sections)d · audio %(audio)d · videos %(videos)d · lines %(lines)d · "
              "words %(words)d" % summary, file=sys.stderr)
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
