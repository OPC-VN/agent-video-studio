"""Owned idea identity is inert and cannot weaken online reference validation."""
import os
import json
import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import capture, materialize, search
from video_studio.effect_library.catalog import CHECKS, _validate_metadata_entry, validate_entry


def idea(identifier="VE-idea-one"):
    return {"id": identifier, "name": identifier, "kind": "reference", "maturity": "reference_only",
            "rights": "owned", "source": "urn:avs:idea:" + identifier, "runtime": "concept",
            "description": "A diagram unfolds one step at a time.", "tags": ["diagram"],
            "roles": ["explain"], "techniques": [], "ratios": [],
            "checks": dict.fromkeys(CHECKS, "not_run")}


@pytest.mark.parametrize("changes", [
    {"source": "urn:avs:idea:VE-other"}, {"source": "urn:avs:idea:VE-idea-one?path=x"},
    {"source": " urn:avs:idea:VE-idea-one", "prompt_text": "not permitted"},
    {"source": "\x00urn:avs:idea:VE-idea-one", "prompt_text": "not permitted"},
    {"rights": "unknown"}, {"rights": "licensed"}, {"maturity": "candidate"},
    {"prompt_text": "private payload"}, {"private_path": "private"},
    {"license_url": "not-a-url"}, {"repository": "private"},
    {"asset": {"path": "a.js", "sha256": "0" * 64}},
])
def test_reject_unauthorized_or_unbounded_idea(changes):
    with pytest.raises((ValueError, ContractError)):
        _validate_metadata_entry(dict(idea(), **changes))


def test_online_reference_still_requires_url():
    item = idea()
    item.update(rights="unknown", source="https://example.org/idea")
    assert _validate_metadata_entry(item)["source"] == "https://example.org/idea"
    item["source"] = "local idea"
    with pytest.raises(ValueError):
        _validate_metadata_entry(item)


def test_idea_payload_rejected_by_all_readers(tmp_path):
    item = dict(idea(), prompt_text="not permitted")
    with pytest.raises(ContractError, match="unsupported"):
        validate_entry(item)
    catalog = tmp_path / "entries.json"
    catalog.write_text(json.dumps([item]), encoding="utf-8")
    with pytest.raises(ContractError, match="unsupported"):
        search(repo_entries=catalog)


@pytest.mark.skipif(os.name != "nt", reason="Windows station capture")
def test_two_owned_ideas_are_distinct_and_cannot_materialize(tmp_path):
    project, target, station = tmp_path / "a", tmp_path / "b", tmp_path / "station"
    project.mkdir(); target.mkdir(); (station / "effect-library" / "entries").mkdir(parents=True)
    first, second = idea(), idea("VE-idea-two")
    assert capture(project, station, first) == first["id"]
    assert capture(project, station, second) == second["id"]
    assert {row["id"] for row in search("diagram", station=station)} == {first["id"], second["id"]}
    with pytest.raises((ValueError, ContractError)):
        capture(project, station, first)
    with pytest.raises((ValueError, ContractError)):
        materialize(station, first["id"], target, "idea.js")
    assert not (target / "idea.js").exists()
