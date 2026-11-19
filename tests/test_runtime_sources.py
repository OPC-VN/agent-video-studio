"""Kiểm tra sổ các thư viện runtime và đối chiếu mã hiện hành."""
import json
import re
from pathlib import Path

import pytest

from video_studio.render import PREVIEW_GSAP_SHA256

ROOT = Path(__file__).resolve().parents[1]

IDEA_REFERENCE_KEYS = {"repo", "ref", "license", "relationship", "status", "code_copied",
                       "assets_copied", "inspect", "local_paths", "upstream_paths", "checked_on", "how"}
IDEA_REFERENCE_REQUIRED = IDEA_REFERENCE_KEYS
EXCLUDED_BY_INSPECT = ()
IDEA_REFERENCES = {
    "openmotion-reference": ("nexu-io/openmotion", "d9ebe30bbcbb39e89bef9308d96e705cc06cc6be", "Apache-2.0"),
    "rea-video-reference": ("JuneYaooo/rea-video", "b08faf2eb53690fc92ddf94576a8c7c3a4a87f89", "Apache-2.0"),
    "line-art-animation-reference": ("JDhruv14/line-art-animation", "c43d698913cf0ad44f984c7ae14c5348010594d3", "MIT"),
}


def _sources():
    return json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))["sources"]


@pytest.mark.parametrize("key", ["gsap-runtime", "threejs-runtime"])
def test_runtime_source_is_ledgered(key):
    sources = _sources()
    assert key in sources, f"upstream.json thiếu {key}"
    entry = sources[key]
    assert entry["relationship"] == "runtime_dependency"
    assert entry["code_copied"] is False, key
    assert entry["binaries_copied"] == 0
    if key == "gsap-runtime":
        assert entry["license_url"] == "https://gsap.com/community/standard-license/"
        assert entry["terms_read_on"] == "2026-11-14"
        assert entry["terms_read_via"]
        assert entry["redistribution"]
    else:
        assert entry["status"] == "planned"
        assert entry["version"] == "0.187.0"
        assert entry["license"] == "MIT"
        assert entry["pinned_sha256"] is None


def test_gsap_ledger_matches_code():
    sources = _sources()
    if "gsap-runtime" not in sources:
        pytest.skip("gsap-runtime chưa có trong sổ")
    entries = sources["gsap-runtime"]["in_use"]
    assert len(entries) == 1
    lock = json.loads((ROOT / "video_studio/locks/runtime-libs.json").read_text(encoding="utf-8"))
    gsap = lock["libs"]["gsap"]
    package = lock["packages"][gsap["package"]]
    assert entries[0]["version"] == package["version"]
    assert entries[0]["sha256"] == gsap["members"][0]["file_sha256"] == PREVIEW_GSAP_SHA256
    assert "CDN" not in entries[0]["delivery"]


def test_notice_names_runtime_libs():
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    runtime = notice.split("Phần CHƯNG CẤT", 1)[0].lower()
    assert "gsap" in runtime
    assert "three.js" in runtime


def test_no_vendored_runtime_libs():
    pattern = re.compile(r"^(?:gsap|three)[\w.-]*\.m?js$|\.min\.js$", re.IGNORECASE)
    found = [str(path.relative_to(ROOT)) for directory in ("skills", "templates", "video_studio")
             for path in (ROOT / directory).rglob("*") if path.is_file() and pattern.search(path.name)
             and path.relative_to(ROOT).as_posix() != "skills/real-estate-location-video/assets/three_d_capture.mjs"]
    assert not found, f"Tệp thư viện được vendor: {found}"


@pytest.mark.parametrize("key", IDEA_REFERENCES)
def test_idea_reference_is_pinned_and_inspected(key):
    sources = _sources()
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    repo, ref, license_name = IDEA_REFERENCES[key]
    if key in EXCLUDED_BY_INSPECT:
        assert key not in sources
        assert repo not in notice
        pytest.skip("nguồn bị loại theo kết quả inspect")
    assert key in sources, f"upstream.json thiếu {key}"
    entry = sources[key]
    assert IDEA_REFERENCE_REQUIRED <= entry.keys()
    assert entry["repo"] == repo
    assert re.fullmatch(r"[0-9a-f]{40}", entry["ref"])
    assert entry["ref"] == ref
    assert entry["license"] == license_name
    assert entry["relationship"] == "idea_reference"
    assert entry["status"] in {"active", "excluded"}
    assert entry["code_copied"] is False
    assert entry["assets_copied"] is False
    inspect = entry["inspect"]
    assert inspect["verdict"] in {"Đạt", "Đạt có điều kiện"}
    assert inspect["ancestry"] in {"reachable", "unverified"}
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", inspect["scanned_on"])
    inspect_text = json.dumps(inspect, ensure_ascii=False)
    assert not any(part in inspect_text for part in ("\\", "C:", "/Users/"))
    assert repo in notice and ref in notice


@pytest.mark.parametrize("key", IDEA_REFERENCES)
def test_idea_reference_has_no_extra_keys(key):
    if key in EXCLUDED_BY_INSPECT:
        pytest.skip("nguồn bị loại theo kết quả inspect")
    assert key in _sources(), f"upstream.json thiếu {key}"
    assert set(_sources()[key]) == IDEA_REFERENCE_KEYS
