"""Thư viện mẫu vlog-design khớp hợp đồng: index sinh tự động khớp tiêu đề, mỗi mẫu đủ trường và có độ tin."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "vlog-design"
REFS = SKILL / "references"

spec = importlib.util.spec_from_file_location("build_index", SKILL / "scripts" / "build_index.py")
bi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bi)

FIELDS = ("Trông thế nào", "Chuyển động", "Giữ", "Khi dùng", "Tránh", "Bằng chứng", "Độ tin",
          "Gợi ý dựng", "Biến thể")
HEAD = re.compile(r"^###\s+((?:LY|TR|VO|MO|TX|IG|ST|AU)-\d{2}[a-z]?)\s+·\s+")


def test_index_matches_library_and_no_duplicate_codes():
    assert bi.main(["--check"]) == 0


def test_every_pattern_has_all_fields_and_trust():
    missing = []
    for f in sorted(REFS.glob("*.md")):
        if f.name in bi.SKIP:
            continue
        sections, cur = {}, None
        for line in f.read_text(encoding="utf-8").splitlines():
            m = HEAD.match(line)
            if m:
                cur = m.group(1)
                sections[cur] = []
            elif line.startswith("#"):
                cur = None
            elif cur:
                sections[cur].append(line)
        for code, body in sections.items():
            text = "\n".join(body)
            for field in FIELDS:
                if f"**{field}:**" not in text and f"**{field}**:" not in text:
                    missing.append(f"{f.name} {code} thiếu «{field}»")
    assert not missing, "\n".join(missing[:30])


def test_every_rc_recipe_has_trust():
    text = (REFS / "idea-to-visual.md").read_text(encoding="utf-8")
    rc = [ln for ln in text.splitlines() if ln.startswith("**RC-")]
    assert rc and all("Độ tin" in ln for ln in rc)


def test_index_trust_values_use_contract_levels():
    items, errors = bi.collect(REFS)
    assert not errors
    bad = [i["code"] for i in items if not re.match(r"(đo|ước|suy ra)\b", i["trust"])]
    assert not bad, bad
