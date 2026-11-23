"""Đếm skill canonical và kiểm hoặc đồng bộ con số trong tài liệu."""
import argparse
import re
import sys
from pathlib import Path

WORDS = {
    "en": ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"),
    "vi": ("một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười", "mười một", "mười hai", "mười ba", "mười bốn", "mười lăm", "mười sáu", "mười bảy", "mười tám", "mười chín", "hai mươi"),
}
NUM_WORDS = {word: n for words in WORDS.values() for n, word in enumerate(words, 1)}
CLAIMS = [
    ("AGENTS.md", r"cộng\s+(\d+)\s+skill", ("total",), False),
    ("AGENTS.md", r"(\d+)\s+skill\s+\((\d+)\s+của repo\s*\+\s*(\d+)\s+chưng cất", ("total", "own", "upstream"), False),
    ("README.md", r"\*\*(\d+) skills\*\*", ("total",), True),
    ("README.md", r"(\w+) written for this repo", ("own",), True),
    ("README.md", r"\*\*(\d+) distilled", ("upstream",), True),
    ("README.md", r"sees all (\d+)", ("total",), True),
    ("README.vi.md", r"\*\*(\d+) skill\*\*", ("total",), True),
    ("README.vi.md", r"(\w+(?: \w+)?) skill của chính repo", ("own",), True),
    ("README.vi.md", r"\*\*(\d+) skill chưng cất", ("upstream",), True),
    ("README.vi.md", r"đủ (\d+) skill", ("total",), True),
    ("hosts/README.md", r"của (\d+) skill", ("total",), True),
    ("docs/index.html", r'data-to="(\d+)">(\d+)</b> skill cho agent', ("total", "total"), True),
    ("docs/index.html", r"(\d+) skill = (\d+) skill của chính repo này \+ (\d+) skill chưng cất", ("total", "own", "upstream"), True),
]


def _skills(root):
    return sorted((root / "skills").rglob("SKILL.md"))


def count_skills(root: Path) -> tuple[int, int, int]:
    skills = _skills(root)
    upstream = sum(p.is_relative_to(root / "skills" / "hyperframes") for p in skills)
    return len(skills) - upstream, upstream, len(skills)


def claimed(text: str, pattern: str) -> list[str]:
    return [group for match in re.finditer(pattern, text) for group in match.groups()]


def to_int(token: str) -> int:
    if token.isdecimal():
        return int(token)
    if token.lower() not in NUM_WORDS:
        raise ValueError(f"chưa biết số bằng chữ: {token}; thêm vào NUM_WORDS")
    return NUM_WORDS[token.lower()]


def check(root: Path) -> list[str]:
    own, upstream, total = count_skills(root)
    actual = {"own": own, "upstream": upstream, "total": total}
    errors = []
    texts = {rel: (root / rel).read_text(encoding="utf-8") for rel, _, _, _ in CLAIMS}
    for rel, pattern, roles, required in CLAIMS:
        tokens = claimed(texts[rel], pattern)
        if not tokens and required:
            errors.append(f"không tìm thấy câu nêu số skill trong {rel}: {pattern}")
        for index, token in enumerate(tokens):
            role = roles[index % len(roles)]
            try:
                value = to_int(token)
            except ValueError as exc:
                errors.append(f"{rel}: {exc}")
                continue
            if value != actual[role]:
                errors.append(f"{rel} ghi {value} skill ({role}), cây có {actual[role]}")
    names = {p.parent.name for p in _skills(root) if not p.is_relative_to(root / "skills" / "hyperframes")}
    for rel, pattern in (("README.md", r"written for this repo\s*\((.*?)\)"),
                         ("README.vi.md", r"skill của chính repo này\s*\((.*?)\)")):
        match = re.search(pattern, texts[rel], re.DOTALL)
        section = match.group(1) if match else ""
        for name in sorted(names):
            if not re.search(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", section):
                errors.append(f"{rel} thiếu tên skill {name} trong danh sách")
    return errors


def _print(message: str) -> None:
    # Stdout có thể dùng bảng mã cũ trên Windows hoặc khi chuyển hướng.
    encoding = sys.stdout.encoding or "utf-8"
    print(message.encode(encoding, errors="backslashreplace").decode(encoding))


def write(root: Path) -> list[str]:
    own, upstream, total = count_skills(root)
    actual = {"own": own, "upstream": upstream, "total": total}
    changed = []
    for rel in ("README.md", "README.vi.md", "hosts/README.md", "docs/index.html"):
        path = root / rel
        text = path.read_text(encoding="utf-8")
        original = text
        for claim_rel, pattern, roles, _ in CLAIMS:
            if claim_rel != rel:
                continue
            matches = list(re.finditer(pattern, text))
            for match in reversed(matches):
                for i in reversed(range(1, len(roles) + 1)):
                    token = match.group(i)
                    value = actual[roles[i - 1]]
                    if not token.isdecimal():
                        language = "vi" if rel == "README.vi.md" else "en"
                        if not 1 <= value <= len(WORDS[language]):
                            raise ValueError(f"chưa có số bằng chữ cho {value}; thêm vào WORDS")
                        replacement = WORDS[language][value - 1]
                    else:
                        replacement = str(value)
                    start, end = match.span(i)
                    text = text[:start] + replacement + text[end:]
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed.append(rel)
    if changed:
        _print("Nhắc: làm mới hash manifest phân phối nếu README.md thay đổi.")
    for error in check(root):
        if error.startswith("AGENTS.md"):
            _print(f"{error}; sửa tay cần người dùng chấp thuận.")
    return changed


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    if args.write:
        for path in write(root):
            _print(path)
    errors = check(root)
    for error in errors:
        _print(error)
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
