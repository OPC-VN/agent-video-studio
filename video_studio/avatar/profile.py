"""Reusable avatar profiles kept in the video station: `<station>/avatars/<id>/avatar.json`.

A profile stores the consent record, the approved idle clip (with SHA-256), engine settings,
the voice profile name and the QA history. Nothing here is ever written inside the repository.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re

from video_studio.contract import ContractError
from . import common
from .optimize import parse_crop

SCHEMA = "avatar-profile/1"
FOLDER = "avatars"
SUBFOLDERS = ("anchor", "clips", "qa", "renders")
RELATIONS = ("self", "consented")
_ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")
DEFAULT_ENGINE = {"name": "latentsync", "guidance": 2.5, "steps": 30, "seed": 1247,
                  "mouth_strength": 0.85, "bbox_shift": 0}


def _now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _root(station: Path) -> Path:
    return station / FOLDER


def _check_id(profile_id):
    if not isinstance(profile_id, str) or not _ID.match(profile_id):
        raise ContractError("Profile id must be 2-63 lowercase letters, digits or hyphens.")
    return profile_id


def _file(station: Path, profile_id) -> Path:
    return _root(station) / _check_id(profile_id) / "avatar.json"


def _write(path: Path, data: dict):
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(temp, path)


def _rel(path: Path, station: Path) -> str:
    return path.relative_to(station).as_posix()


def create(profile_id, name, relation, consent_quote, scope, clip=None, voice=None, crop=None) -> dict:
    station = common.station()
    path = _file(station, profile_id)
    if path.exists():
        raise ContractError(f"Profile '{profile_id}' already exists.")
    if relation not in RELATIONS:
        raise ContractError("relation must be 'self' (your own face) or 'consented' (written consent).")
    quote = (consent_quote or "").strip()
    if len(quote) < 10:
        raise ContractError("A consent quote of at least 10 characters is required: the words the person used to agree.")
    if not (scope or "").strip():
        raise ContractError("Consent scope is required, for example 'internal lessons, no ads'.")
    if not (name or "").strip():
        raise ContractError("Display name is required.")
    parse_crop(crop)
    data = {
        "schema": SCHEMA, "id": profile_id, "name": name.strip(), "created_at": _now(),
        "consent": {"relation": relation, "quote": quote, "scope": scope.strip(),
                    "granted_at": _now(), "revoked_at": None},
        "clip": None, "crop": crop or None, "engine": dict(DEFAULT_ENGINE),
        "voice": {"profile": voice or None, "speed": 1.0}, "qa_history": [],
    }
    if clip:
        data["clip"] = _clip_entry(Path(clip), station)
    path.parent.mkdir(parents=True, exist_ok=False)
    for sub in SUBFOLDERS:
        (path.parent / sub).mkdir()
    _write(path, data)
    return {"profile": profile_id, "path": str(path.parent)}


def _clip_entry(clip: Path, station: Path) -> dict:
    clip = common.existing_video(common.inside(clip, station))
    return {"path": _rel(clip, station), "sha256": common.sha256(clip)}


def load(profile_id) -> dict:
    station = common.station()
    path = _file(station, profile_id)
    if not path.is_file():
        raise ContractError(f"Profile '{profile_id}' was not found; use `avatar profile list`.")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ContractError(f"Profile '{profile_id}' is unreadable.") from exc
    if data.get("schema") != SCHEMA:
        raise ContractError(f"Profile '{profile_id}' has an unknown schema.")
    return data


def search(query=None) -> dict:
    station = common.station()
    found = []
    needle = (query or "").strip().lower()
    for path in sorted(_root(station).glob("*/avatar.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if needle and needle not in f"{data.get('id', '')} {data.get('name', '')}".lower():
            continue
        consent = data.get("consent") or {}
        last = (data.get("qa_history") or [None])[-1]
        found.append({"id": data.get("id"), "name": data.get("name"),
                      "usable": bool(data.get("clip")) and not consent.get("revoked_at"),
                      "revoked": bool(consent.get("revoked_at")), "last_qa": last})
    return {"profiles": found, "count": len(found)}


def update(profile_id, clip=None, voice=None, crop=None, engine=None) -> dict:
    station = common.station()
    data = load(profile_id)
    if clip:
        data["clip"] = _clip_entry(Path(clip), station)
    if voice:
        data["voice"]["profile"] = voice
    if crop:
        parse_crop(crop)
        data["crop"] = crop
    for key, value in (engine or {}).items():
        if value is not None:
            data["engine"][key] = value
    _write(_file(station, profile_id), data)
    return {"profile": profile_id, "updated": True}


def revoke(profile_id) -> dict:
    station = common.station()
    data = load(profile_id)
    data["consent"]["revoked_at"] = _now()
    _write(_file(station, profile_id), data)
    return {"profile": profile_id, "revoked": True}


def for_render(profile_id) -> dict:
    """Consent and clip integrity gate: returns the clip path and engine settings."""
    station = common.station()
    data = load(profile_id)
    consent = data.get("consent") or {}
    if consent.get("revoked_at"):
        raise ContractError(f"Consent for profile '{profile_id}' was revoked; do not render it.")
    if consent.get("relation") not in RELATIONS or not consent.get("quote"):
        raise ContractError(f"Profile '{profile_id}' has no consent record.")
    clip = data.get("clip")
    if not clip:
        raise ContractError(f"Profile '{profile_id}' has no approved clip; add one with `avatar profile update --clip`.")
    path = common.inside(station / clip["path"], station)
    if not path.is_file() or common.sha256(path) != clip["sha256"]:
        raise ContractError(f"The clip of profile '{profile_id}' is missing or changed since it was approved.")
    return {"clip": path, "engine": data["engine"], "voice": data.get("voice") or {}}


def record_qa(profile_id, video, result: dict) -> dict:
    station = common.station()
    data = load(profile_id)
    video_path = Path(os.path.abspath(video))
    entry = {"at": _now(), "video": _rel(video_path, station) if video_path.is_relative_to(station) else video_path.name,
             **{k: result[k] for k in ("confidence", "av_offset", "passed") if k in result}}
    data.setdefault("qa_history", []).append(entry)
    _write(_file(station, profile_id), data)
    return entry
