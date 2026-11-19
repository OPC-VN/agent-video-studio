"""Static checks for the procedural line-art assets and routing cases."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/line-art-motion/assets"
FORBIDDEN = ("Math.random", "Date.now", "performance.now", "setTimeout", "setInterval", "requestAnimationFrame", "pointermove", "fetch(", "https://", "http://")


def scan_forbidden(text):
    return [item for item in FORBIDDEN if item in text]


def test_scanner_detects_each_forbidden_marker():
    for marker in FORBIDDEN:
        assert marker in scan_forbidden("prefix " + marker + " suffix")
    assert scan_forbidden("seek(t)") == []


def test_assets_are_small_and_deterministic():
    files = [p for p in ASSETS.rglob("*") if p.is_file()]
    assert len(files) == 4 and all(p.suffix == ".mjs" for p in files)
    assert sum(p.stat().st_size for p in files) <= 40960
    for p in files:
        text = p.read_text(encoding="utf-8")
        assert not scan_forbidden(text)


def test_skill_has_no_binary_assets():
    forbidden = {".mp4", ".mov", ".mp3", ".wav", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".ttf", ".otf"}
    assert not [p for p in ASSETS.parent.rglob("*") if p.is_file() and p.suffix.lower() in forbidden]


def test_provenance_and_distribution_manifest():
    source = "idea from JDhruv14/line-art-animation @c43d698 (MIT)"
    assert source in (ROOT / "NOTICE").read_text(encoding="utf-8")
    rights = json.loads((ROOT / "skills/video-theme-library/assets/effect-library/distribution-rights.json").read_text(encoding="utf-8"))["files"]
    upstream = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))["sources"]["line-art-animation-reference"]
    files = {p.relative_to(ROOT).as_posix() for p in ASSETS.glob("*.mjs")}
    assert set(upstream["local_paths"]) == files
    assert upstream["code_copied"] is False and upstream["assets_copied"] is False
    helper = "skills/line-art-motion/assets/line-art.mjs"
    assert source in rights[helper]["license"]
    catalog = json.loads((ROOT / "skills/video-theme-library/assets/effect-library/entries.json").read_text(encoding="utf-8"))
    components = {e["asset"]["path"]: e for e in catalog if e.get("id", "").startswith("VE-line-art-")}
    assert set(components) == files - {helper}
    for name, entry in components.items():
        assert entry["rights"] == "owned" and entry["license"]["id"] == "MIT"
        assert entry["asset"]["sha256"] == hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    distribution = json.loads((ROOT / "scripts/effect-distribution-manifest.json").read_text(encoding="utf-8"))
    manifest = distribution["files"]
    assert files <= set(distribution["resources"])
    skill_files = {p.relative_to(ROOT).as_posix() for p in ASSETS.parent.rglob("*") if p.is_file()}
    assert skill_files <= set(distribution["resources"])
    for name in files:
        assert manifest[name] == hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def test_routing_eval_cases_are_unrun_and_balanced():
    data = json.loads((ROOT / "evals/line-art-motion/cases.json").read_text(encoding="utf-8"))
    assert data["status"] == "not_run"
    assert data["skill_name"] == "line-art-motion"
    assert (ROOT / "evals/line-art-motion/rubric.md").is_file()
    assert sum(c["should_trigger"] for c in data["cases"]) >= 3
    assert sum(not c["should_trigger"] for c in data["cases"]) >= 3
    assert len({c["id"] for c in data["cases"]}) == len(data["cases"])
    for case in data["cases"]:
        assert set(case) >= {"id", "kind", "prompt", "should_trigger", "expected_behaviors", "quality_criteria", "fixtures"}
        assert case["fixtures"] and case["expected_behaviors"] and case["quality_criteria"]
        assert case["kind"] == ("positive" if case["should_trigger"] else "negative")


def test_routing_description_and_negative_cases():
    skill = (ASSETS.parent / "SKILL.md").read_text(encoding="utf-8")
    description = next(line for line in skill.splitlines() if line.startswith("description:"))
    assert "Use when" in description and "Not for" in description
    for name in ("lyric-video-effects", "photo-ambient-effects", "video-theme-library"):
        assert name in description
    routing = (ROOT / "skills/video-routing/SKILL.md").read_text(encoding="utf-8")
    assert "line-art-motion" in routing
    data = json.loads((ROOT / "evals/line-art-motion/cases.json").read_text(encoding="utf-8"))
    negatives = " ".join(c["prompt"].lower() for c in data["cases"] if not c["should_trigger"])
    for term in ("lời bài hát", "ảnh tĩnh", "thư viện"):
        assert term in negatives
