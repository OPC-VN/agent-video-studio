"""Kiểm cấu trúc skill video-long-to-shorts: frontmatter, liên kết, mẫu, và sự khớp giữa mẫu với script."""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "video-long-to-shorts"
TEMPLATES = SKILL / "assets" / "templates"
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


def load(name):
    spec = importlib.util.spec_from_file_location(f"vlts_{name}_doc", SKILL / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_frontmatter_is_english_one_line_fields_and_names_the_triggers():
    front = TEXT.split("---", 2)[1]
    name = re.search(r"^name: (.+)$", front, re.M).group(1)
    description = re.search(r'^description: "(.+)"$', front, re.M).group(1)
    assert name == "video-long-to-shorts"
    assert description.isascii() and len(description) <= 1024
    for phrase in ("long video", "9:16", "shorts", "Not for"):
        assert phrase in description


def test_every_relative_link_in_skill_and_references_resolves():
    files = [SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]
    assert len(files) == 9, "SKILL.md + 8 reference"
    for md in files:
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", md.read_text(encoding="utf-8")):
            if "://" in target:
                continue
            assert (md.parent / target).exists(), f"{md.name}: liên kết hỏng {target}"


def test_skill_lists_every_reference_script_and_template():
    for path in sorted((SKILL / "references").glob("*.md")):
        assert f"references/{path.name}" in TEXT, path.name
    for path in sorted((SKILL / "scripts").glob("*.py")):
        assert f"scripts/{path.name}" in TEXT, path.name
    for path in sorted(TEMPLATES.iterdir()):
        assert path.name in TEXT, path.name


def test_hard_rules_and_two_human_gates_are_stated():
    for phrase in ("Cổng 1", "Cổng 2", "mã dòng", "không thêm khẳng định", "ICON-GAPS.md",
                   "≥ 3 ý tưởng", "Không đăng short"):
        assert phrase in TEXT, phrase


def test_beats_template_is_a_valid_plan_for_cut_voice():
    cut_voice = load("cut_voice")
    plan = json.loads((TEMPLATES / "beats.json").read_text(encoding="utf-8"))
    audio = [{"id": "voice", "src": "v.wav", "start": 13.6, "end": 348.6, "media_start": 0.0, "volume": 1.0},
             {"id": "voiceEnd", "src": "e.wav", "start": 445.6, "end": 548.9, "media_start": 0.0, "volume": 1.0}]
    for seg in plan["segments"]:
        assert {"id", "tl_in", "tl_out", "first_word", "last_word"} <= set(seg)
        clip = cut_voice.pick_clip(audio, seg)
        assert clip["id"] == seg["clip"] and cut_voice.media_time(clip, seg["tl_in"]) >= 0


def test_frame_template_has_placeholders_zones_and_no_nondeterminism():
    html = (TEMPLATES / "short-frame.html").read_text(encoding="utf-8")
    for slot in ("COMP_ID", "DUR", "HOOK_HTML", "STAGE_HTML", "AVATAR_HTML", "SUBS_HTML",
                 "END_HTML", "MUSIC_HTML", "TIMELINE_JS"):
        assert "{{%s}}" % slot in html, slot
    assert 'data-width="1080"' in html and 'data-height="1920"' in html and 'data-fps="30"' in html
    assert "--sub-top:1590px" in html and "--avatar-d:400px" in html
    code = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    code = re.sub(r"/\*.*?\*/|//[^\n]*", "", code, flags=re.S)
    for banned in ("@keyframes", "animation:", "<animate", "repeat:-1", "Math.random", "Date.now",
                   "requestAnimationFrame", "http://", "https://"):
        assert banned not in code, banned


def test_layout_example_in_docs_passes_gap_scan_schema():
    gap = load("gap_scan")
    for name in ("qa-checklist.md", "example-short.md"):
        text = (SKILL / "references" / name).read_text(encoding="utf-8")
        blocks = [b for b in re.findall(r"```json\n(.*?)```", text, re.S) if '"elements"' in b]
        assert blocks, name
        for block in blocks:
            result = gap.check(json.loads(block))
            assert set(result) >= {"ok", "errors", "warnings"}


def test_eval_cases_cover_trigger_offer_and_near_misses():
    cases = json.loads((ROOT / "evals" / "video-long-to-shorts" / "cases.json").read_text(encoding="utf-8"))
    assert cases["skill_name"] == "video-long-to-shorts" and cases["baseline"] == "not_run"
    kinds = [(c["should_trigger"], c["kind"]) for c in cases["cases"]]
    assert sum(1 for trig, _ in kinds if trig) >= 4 and sum(1 for trig, _ in kinds if not trig) >= 2
    assert len({c["id"] for c in cases["cases"]}) == len(cases["cases"])
