"""Retrieval behavior across sources, using only synthetic metadata."""
import json

import pytest

from video_studio.effect_library.search import search
from video_studio.effect_library.layout_search import parse_layouts
from video_studio.contract import ContractError
from pathlib import Path


@pytest.fixture
def motion_index(tmp_path):
    entries = []
    for ident, name, coverage in (
        ("PM-diagram", "Diagram workflow", "partial"),
        ("PM-transition", "Smooth transition", "fullscreen"),
        ("PM-rays", "Light rays", "partial"),
        ("PM-lyric", "Lyric emphasis", "partial"),
        ("PM-unrelated", "Light workflow", "partial"),
        ("PM-boundary", "Light", "partial"),
    ):
        entries.append({"id": ident, "name": name, "source_facts": {"url": "https://example.org/"},
                        "sol_analysis": {"coverage": coverage, "scene_roles": ["explain"],
                                         "description": "Ray Johnson" if ident == "PM-boundary" else "",
                                         "ratio_fit": {"9:16": {"fit": "adaptable"}}}})
    path = tmp_path / "motion.json"
    path.write_text(json.dumps({"entries": entries}), encoding="utf-8")
    return path


@pytest.mark.parametrize("query,expected", [
    ("sơ đồ", "PM-diagram"), ("so do", "PM-diagram"), ("diagram", "PM-diagram"),
    ("lời bài hát", "PM-lyric"), ("chuyển cảnh", "PM-transition"),
    ("tia sáng", "PM-rays"),
])
def test_phrase_aliases_and_combined_filters(motion_index, query, expected):
    rows = search(query, {"origin": "prompt_motion", "role": "explain", "ratio": "9:16"},
                  pm_index=motion_index)
    assert [row["id"] for row in rows] == [expected]
    assert rows[0]["rights"] == "unknown"
    assert rows[0]["checks"]["render"] == "not_run"


def test_aliases_respect_phrase_boundaries_and_other_terms(motion_index):
    assert search("tia sáng missing", pm_index=motion_index) == []
    assert [row["id"] for row in search("light workflow", pm_index=motion_index)] == ["PM-unrelated"]
    assert search("something entirely absent", pm_index=motion_index) == []
    assert [row["id"] for row in search(filters={"coverage": "fullscreen"}, pm_index=motion_index)] == ["PM-transition"]
    assert search(filters={"origin": "station"}, pm_index=motion_index) == []
    assert [row["id"] for row in search("tia sáng", pm_index=motion_index)] == ["PM-rays"]


def test_real_layout_catalog_is_partial_and_preserves_status():
    root = Path(__file__).resolve().parents[1]
    rows = search("LAYOUT-flow", layout_root=root)
    assert len(rows) == 1
    assert rows[0]["origin"] == "layout_repo"
    assert rows[0]["kind"] == "reference" and rows[0]["rights"] == "unknown"
    assert rows[0]["layout_tier"] == "S" and rows[0]["checks"]["render"] == "not_run"
    assert search("LAYOUT-flow", {"origin": "layout_repo", "ratio": "9:16"}, layout_root=root) == []
    assert search("LAYOUT-bignum", {"ratio": "9:16"}, layout_root=root)
    assert search("LAYOUT-versus", {"ratio": "16:9"}, layout_root=root)
    assert search("LAYOUT-versus", {"ratio": "9:16"}, layout_root=root)
    results = search("quy trình", {"origin": "layout_repo", "ratio": "9:16"}, layout_root=root)
    assert {row["id"] for row in results} >= {"LAYOUT-process-chips", "LAYOUT-orbit-loop"}
    assert all("Quy trình" in " ".join(row["tags"]) for row in results)
    assert search("LAYOUT-outro-long", layout_root=root) == []  # grouped source row is omitted
    assert search("LAYOUT-clip-embed", layout_root=root) == []  # free-form media is omitted
    assert search("", layout_root=root)


def test_layout_rejects_incomplete_format():
    with pytest.raises(ContractError, match="incomplete"):
        parse_layouts("## 2. Cover\n", "source", "layout_repo")


def test_layout_ratios_follow_column_headings():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs/THEME-LIBRARY.md").read_text(encoding="utf-8")
    text = text.replace("Chọn (16:9) | Chọn (9:16)", "Chọn (9:16) | Chọn (16:9)")
    rows = {row["name"]: row for row in parse_layouts(text, "source", "layout_repo")}
    assert rows["bignum"]["ratios"] == ["16:9"]


def test_layout_ignores_examples_in_fences_and_after_other_headings():
    row = "| **fake · S** | sample | sample |"
    text = "\n".join(["## 2. Cover", "| **real · S** | use | motion |", "```", row, "```",
                      "## Other", row, "## 3. Numbers", "## 4. Structure", "## 5. Comparison", "## 8. End"])
    assert [item["id"] for item in parse_layouts(text, "source", "layout_repo")] == ["LAYOUT-real"]


@pytest.mark.skipif(__import__("os").name != "nt", reason="Windows station reader")
def test_layout_station_fallback_only_when_catalog_missing(tmp_path):
    root = Path(__file__).resolve().parents[1]
    assert search("LAYOUT-flow", layout_root=root, layout_station=tmp_path)[0]["origin"] == "layout_repo"
    (tmp_path / "THEME-LIBRARY.md").write_text("invalid", encoding="utf-8")
    with pytest.raises(ContractError, match="incomplete"):
        search(layout_root=root, layout_station=tmp_path)
