"""Sinh hoặc kiểm references/pattern-index.md từ các file thư viện mẫu.

Cách dùng (từ thư mục skill vlog-design):
    python scripts/build_index.py            # ghi lại references/pattern-index.md
    python scripts/build_index.py --check    # chỉ so; khác thì thoát 1

Đọc mọi `references/*.md`, nhận:
    tiêu đề `### XX-NN · Tên` hoặc `### XX-NNa · Tên`   (XX ∈ LY TR VO MO TX IG ST AU)
    dòng đậm `**RC-NN · «…».** … Độ tin: …`
Độ tin lấy từ dòng `- **Độ tin:** …` trong mục (hoặc «Độ tin: …» trên dòng RC). Tiêu đề chứa «(bỏ» → trạng thái `bỏ`.
Mã trùng ở hai nơi là lỗi. Mã thoát: 0 ok · 1 index lệch (--check) hoặc mã trùng · 2 thiếu thư mục.
Chỉ thư viện chuẩn Python 3.9+.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GROUPS = ("LY", "TR", "VO", "MO", "TX", "IG", "ST", "AU", "RC")
HEAD = re.compile(r"^###\s+((?:LY|TR|VO|MO|TX|IG|ST|AU)-\d{2}[a-z]?)\s+·\s+(.+?)\s*$")
RC = re.compile(r"^\*\*(RC-\d{2}[a-z]?)\s+·\s+(.+?)\*\*(.*)$")
TRUST = re.compile(r"Độ tin:\**\s*(.+?)\s*$")
SKIP = {"pattern-index.md", "library-contract.md", "workflow.md", "asset-sourcing.md", "example-storyboard.md"}


def collect(ref_dir: Path) -> tuple[list[dict], list[str]]:
    items, errors, seen = [], [], {}
    for f in sorted(ref_dir.glob("*.md")):
        if f.name in SKIP:
            continue
        cur = None
        for line in f.read_text(encoding="utf-8").splitlines():
            m = HEAD.match(line)
            r = RC.match(line) if not m else None
            if m or r:
                code, name = (m or r).group(1), (m or r).group(2).strip()
                name = name.rstrip(".").strip()
                cur = {"code": code, "name": name, "file": f.name, "trust": "chưa ghi",
                       "status": "bỏ" if "(bỏ" in name else "dùng"}
                if code in seen:
                    errors.append(f"{code} trùng ở {seen[code]} và {f.name}")
                seen[code] = f.name
                items.append(cur)
                if r:
                    t = TRUST.search(r.group(3))
                    if t:
                        cur["trust"] = t.group(1).rstrip(".")
                continue
            if cur is not None and line.startswith("#"):
                cur = None
                continue
            if cur is not None and cur["trust"] == "chưa ghi" and "Độ tin" in line:
                t = TRUST.search(line)
                if t:
                    cur["trust"] = t.group(1).rstrip(".")

    def key(it):
        g, rest = it["code"].split("-", 1)
        return (GROUPS.index(g), int(rest[:2]), rest[2:])
    items.sort(key=key)
    return items, errors


def render(items: list[dict]) -> str:
    counts = {g: sum(1 for i in items if i["code"].startswith(g + "-")) for g in GROUPS}
    lines = [
        "# Bảng mã mẫu (sinh tự động — đừng sửa tay)",
        "",
        "> **Kết luận:** mọi mã mẫu của thư viện, một dòng mỗi mã. Đọc file này trước khi tra file chi tiết; "
        "khuôn và luật mã ở `library-contract.md`. Sinh lại: `python scripts/build_index.py`.",
        "",
        "Tỉ lệ khung: **16:9** (mọi vị trí, kích thước là % khung 1920×1080).",
        "",
        "Số mã: " + " · ".join(f"{g} {n}" for g, n in counts.items() if n) + f" · tổng {len(items)}.",
        "",
        "## Contents",
        "",
    ] + [f"- {g}" for g in GROUPS if counts[g]]
    for g in GROUPS:
        group = [i for i in items if i["code"].startswith(g + "-")]
        if not group:
            continue
        lines += ["", f"## {g}", "", "| Mã | Tên | File | Độ tin | Trạng thái |", "|---|---|---|---|---|"]
        for it in group:
            name = it["name"].replace("|", "/")
            lines.append(f"| {it['code']} | {name} | `{it['file']}` | {it['trust']} | {it['status']} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Sinh / kiểm pattern-index.md")
    p.add_argument("--check", action="store_true")
    p.add_argument("--refs", default=str(Path(__file__).resolve().parent.parent / "references"))
    a = p.parse_args(argv)
    ref_dir = Path(a.refs)
    if not ref_dir.is_dir():
        print(f"LỖI: không có thư mục {ref_dir}", file=sys.stderr)
        return 2
    items, errors = collect(ref_dir)
    for e in errors:
        print(f"LỖI: {e}", file=sys.stderr)
    text = render(items)
    target = ref_dir / "pattern-index.md"
    if a.check:
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        if old.replace("\r\n", "\n") != text:
            print("LỖI: pattern-index.md lệch thư viện — chạy lại build_index.py", file=sys.stderr)
            return 1
        print(f"index khớp: {len(items)} mã")
        return 1 if errors else 0
    target.write_text(text, encoding="utf-8", newline="\n")
    print(f"đã ghi {target.name}: {len(items)} mã")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
