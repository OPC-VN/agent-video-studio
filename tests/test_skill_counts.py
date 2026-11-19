from pathlib import Path

import pytest

from scripts import skill_counts as counts

ROOT = Path(__file__).resolve().parents[1]


def make_tree(root):
    for name in [f"own-{i}" for i in range(9)]:
        path = root / "skills" / name / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("skill", encoding="utf-8")
    for name in ["up-1", "up-2"]:
        path = root / "skills" / "hyperframes" / name / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("skill", encoding="utf-8")
    (root / "skills" / "not-a-skill").mkdir()
    names = " ".join(f"own-{i}" for i in range(9))
    files = {
        "AGENTS.md": "cộng 27 skill\n27 skill (6 của repo + 21 chưng cất\n",
        "README.md": f"**27 skills**: six written for this repo ({names}) and **21 distilled; sees all 27.",
        "README.vi.md": f"**27 skill**: sáu skill của chính repo này ({names}) và **21 skill chưng cất; đủ 27 skill.",
        "hosts/README.md": "của 27 skill",
        "docs/index.html": 'data-to="27">27</b> skill cho agent\n27 skill = 6 skill của chính repo này + 21 skill chưng cất',
    }
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_count_matches_tree(tmp_path):
    make_tree(tmp_path)
    assert counts.count_skills(tmp_path) == (9, 2, 11)
    paths = list((ROOT / "skills").rglob("SKILL.md"))
    upstream = sum("hyperframes" == path.relative_to(ROOT / "skills").parts[0] for path in paths)
    assert counts.count_skills(ROOT) == (len(paths) - upstream, upstream, len(paths))


def test_claimed_detects_stale_number():
    assert counts.claimed("**27 skills**: six written", r"\*\*(\d+) skills\*\*") == ["27"]
    assert counts.claimed("six written for this repo", r"(\w+) written for this repo") == ["six"]


def test_num_words_one_to_twelve():
    for language in ("en", "vi"):
        for number, word in enumerate(counts.WORDS[language], 1):
            assert counts.to_int(word) == number
    assert counts.to_int("29") == 29


def test_unknown_word_errors():
    with pytest.raises(ValueError, match="chưa biết số bằng chữ"):
        counts.to_int("unknown")


def test_check_reports_each_stale_file(tmp_path):
    make_tree(tmp_path)
    errors = counts.check(tmp_path)
    for rel in ("AGENTS.md", "README.md", "README.vi.md", "hosts/README.md", "docs/index.html"):
        assert any(rel in error and "cây có" in error for error in errors)
    (tmp_path / "hosts/README.md").write_text("missing", encoding="utf-8")
    assert any("không tìm thấy câu nêu số skill" in e for e in counts.check(tmp_path))


def test_write_fixes_four_files_and_never_touches_agents(tmp_path, capsys):
    make_tree(tmp_path)
    before = (tmp_path / "AGENTS.md").read_bytes()
    assert set(counts.write(tmp_path)) == {"README.md", "README.vi.md", "hosts/README.md", "docs/index.html"}
    assert (tmp_path / "AGENTS.md").read_bytes() == before
    assert "nine written" in (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "chín skill" in (tmp_path / "README.vi.md").read_text(encoding="utf-8")
    assert 'data-to="11">11</b>' in (tmp_path / "docs/index.html").read_text(encoding="utf-8")
    assert "manifest" in capsys.readouterr().out
    assert all(e.startswith("AGENTS.md") for e in counts.check(tmp_path))


def test_write_is_idempotent(tmp_path):
    make_tree(tmp_path)
    counts.write(tmp_path)
    assert counts.write(tmp_path) == []


def test_every_own_skill_listed_in_readmes(tmp_path):
    make_tree(tmp_path)
    for name in ("README.md", "README.vi.md"):
        path = tmp_path / name
        path.write_text(path.read_text(encoding="utf-8").replace("own-3", ""), encoding="utf-8")
    errors = counts.check(tmp_path)
    assert sum("own-3" in error for error in errors) == 2
    assert not any("not-a-skill" in error for error in errors)


def test_main_reports_errors_and_fixes_writable_documents(tmp_path, monkeypatch, capsys):
    make_tree(tmp_path)
    monkeypatch.setattr(counts, "__file__", str(tmp_path / "scripts" / "skill_counts.py"))
    assert counts.main(["--check"]) == 1
    assert "cây có" in capsys.readouterr().out
    assert counts.main(["--write"]) == 1  # AGENTS.md cần duyệt và sửa riêng.
    (tmp_path / "AGENTS.md").write_text("không ghi số", encoding="utf-8")
    assert counts.main([]) == 0


def test_check_reports_unknown_number_word(tmp_path):
    make_tree(tmp_path)
    path = tmp_path / "README.md"
    path.write_text(path.read_text(encoding="utf-8").replace("six written", "unknown written"), encoding="utf-8")
    assert any("chưa biết số bằng chữ" in error for error in counts.check(tmp_path))


def test_check_detects_visible_page_number_drift(tmp_path):
    make_tree(tmp_path)
    counts.write(tmp_path)
    (tmp_path / "AGENTS.md").write_text("không ghi số", encoding="utf-8")
    page = tmp_path / "docs/index.html"
    page.write_text(page.read_text(encoding="utf-8").replace('data-to="11">11', 'data-to="11">27'), encoding="utf-8")
    assert any("docs/index.html ghi 27 skill (total), cây có 11" in error for error in counts.check(tmp_path))
    counts.write(tmp_path)
    assert 'data-to="11">11</b>' in page.read_text(encoding="utf-8")
    assert counts.check(tmp_path) == []


def test_write_with_cp1252_stdout(tmp_path, monkeypatch):
    import io
    import sys

    make_tree(tmp_path)
    monkeypatch.setattr(counts, "__file__", str(tmp_path / "scripts" / "skill_counts.py"))
    output = io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict")
    monkeypatch.setattr(sys, "stdout", output)
    assert counts.main(["--write"]) == 1
    assert 'data-to="11">11</b>' in (tmp_path / "docs/index.html").read_text(encoding="utf-8")
    output.flush()
    assert b"manifest" in output.buffer.getvalue()


def test_adding_skill_and_syncing_docs_passes(tmp_path):
    make_tree(tmp_path)
    (tmp_path / "AGENTS.md").write_text("không ghi số", encoding="utf-8")
    new_skill = tmp_path / "skills" / "own-new" / "SKILL.md"
    new_skill.parent.mkdir()
    new_skill.write_text("skill", encoding="utf-8")
    for rel in ("README.md", "README.vi.md"):
        path = tmp_path / rel
        path.write_text(path.read_text(encoding="utf-8").replace("own-8)", "own-8 own-new)"), encoding="utf-8")
    counts.write(tmp_path)
    assert counts.count_skills(tmp_path) == (10, 2, 12)
    assert counts.check(tmp_path) == []
