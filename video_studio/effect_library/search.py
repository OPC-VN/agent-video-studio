"""Search existing Prompt Motion metadata and explicit effect catalogs offline."""
import json
import math
import os
import re
from pathlib import Path
import unicodedata

from video_studio.contract import ContractError
from .catalog import CHECKS, validate_entry
from .resources import resource_root


_IS_NT = os.name == "nt"

# Explicit, phrase-level equivalents. Do not expand individual words such as
# "light" or "so": they have unrelated meanings in many queries.
_QUERY_ALIASES = (
    ("so do", "diagram"),
    ("loi bai hat", "lyric", "lyrics"),
    ("chuyen canh", "transition"),
    ("tia sang", "tia nang", "light ray", "light rays", "sun ray", "sun rays"),
)


def _repo_reader():
    if _IS_NT:
        from . import _native_windows as reader
    else:
        from . import _posix_fs as reader
    return reader


def _verify_repo_bundle(repo_root, record):
    """Verify the entire bundle through the bounded platform reader."""
    _repo_reader().read_repo_files(repo_root, record["assets"], max_total=64 * 1024 * 1024)


def _strict_json_loads(text):
    """Parse catalog JSON without duplicate keys or non-finite numbers."""
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON field: {key}")
            result[key] = value
        return result

    def finite_float(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError("non-finite JSON number")
        return result

    def invalid_constant(value):
        raise ValueError("non-finite JSON number")

    try:
        return json.loads(text, object_pairs_hook=unique_pairs, parse_float=finite_float,
                          parse_constant=invalid_constant)
    except RecursionError as exc:
        raise ValueError("JSON nesting exceeds parser limit") from exc


def _fold(value):
    value = unicodedata.normalize("NFD", str(value).lower().replace("đ", "d"))
    return "".join(c for c in value if unicodedata.category(c) != "Mn")


def _query_groups(query):
    """Produce AND groups of exact token phrases, with bounded alternatives."""
    tokens = re.findall(r"\w+", _fold(query))
    aliases = sorted(((tuple(alias.split()), group) for group in _QUERY_ALIASES
                      for alias in group), key=lambda pair: -len(pair[0]))
    groups = []
    i = 0
    while i < len(tokens):
        match = next(((phrase, group) for phrase, group in aliases
                      if tuple(tokens[i:i + len(phrase)]) == phrase), None)
        if match:
            phrase, group = match
            groups.append(tuple(tuple(alias.split()) for alias in group))
            i += len(phrase)
        else:
            groups.append(((tokens[i],),))
            i += 1
    return tokens, groups


def _contains_phrase(tokens, phrase):
    size = len(phrase)
    return any(tuple(tokens[i:i + size]) == tuple(phrase) for i in range(len(tokens) - size + 1))


def _text_values(value):
    """Keep metadata values separate so phrases cannot cross field boundaries."""
    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _text_values(item)
    elif value is not None:
        yield str(value)


def _ratio_matches(entry, ratio, include_unknown):
    if ratio in entry.get("ratios", []):
        return True
    if not include_unknown:
        return False
    if entry.get("origin") == "prompt_motion":
        return ratio not in entry.get("ratio_fit", {})
    return entry.get("ratios") == []


def _load(path):
    try:
        if os.name == "nt":
            from contextlib import ExitStack
            from . import _native_windows as native

            absolute = os.path.abspath(os.fspath(path))
            with ExitStack() as handles:
                parent = native.open_root(os.path.dirname(absolute))
                handles.callback(native.close, parent)
                source = native.open_file(parent, os.path.basename(absolute))
                handles.callback(native.close, source)
                return _strict_json_loads(native.read_all(source, limit=16 * 1024 * 1024).decode("utf-8-sig"))
        return _strict_json_loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise ContractError(f"Cannot read catalog {path}: {exc}") from exc


def _pm(path):
    data = _load(path)
    result = []
    for e in data["entries"]:
        a, s = e.get("sol_analysis", {}), e.get("source_facts", {})
        result.append({"id": e["id"], "name": e["name"], "kind": "reference", "maturity": "reference_only",
                       "rights": "unknown", "source": s.get("url"), "file": e.get("file"),
                       "tags": a.get("keywords", []), "roles": a.get("scene_roles", []),
                       "techniques": a.get("techniques", []),
                       "coverage": a.get("coverage"),
                       "ratios": [k for k, v in a.get("ratio_fit", {}).items() if v.get("fit") in ("preferred", "adaptable")],
                       "ratio_fit": a.get("ratio_fit", {}),
                       "description": a.get("description", ""), "origin": "prompt_motion",
                       "checks": dict.fromkeys(CHECKS, "not_run"), "checks_origin": "default_not_run"})
    return result


def search(query="", filters=None, station=None, repo_entries=None, pm_index=None, limit=10, distilled_root=None, include_unknown_ratio=False, layout_root=None, layout_station=None):
    """Return matching records; caller supplies each desired source, no network or writes."""
    if not isinstance(limit, int) or limit < 1:
        raise ContractError("limit must be a positive integer")
    filters = filters or {}
    base_filters = {"kind", "maturity", "rights", "role", "technique", "ratio", "runtime", "origin", "coverage"}
    evidence_filters = {f"check.{key}" for key in CHECKS}
    if set(filters) - base_filters - evidence_filters:
        raise ContractError("Unknown filter")
    if not isinstance(include_unknown_ratio, bool) or (include_unknown_ratio and not filters.get("ratio")):
        raise ContractError("include_unknown_ratio requires a ratio filter and a boolean value")
    if "ratio" in filters and (not isinstance(filters["ratio"], str) or not filters["ratio"].strip()):
        raise ContractError("Invalid ratio filter")
    runtime_terms = None
    if "runtime" in filters:
        value = filters["runtime"]
        if not isinstance(value, str) or not (runtime_terms := re.findall(r"\d+(?:\.\d+)+|\w+", _fold(value))):
            raise ContractError("Invalid runtime filter")
    for key in evidence_filters & filters.keys():
        value = filters[key]
        if not isinstance(value, str) or value not in {"not_run", "pass", "fail"}:
            raise ContractError(f"Invalid evidence filter: {key}")
    entries = _pm(pm_index) if pm_index else []
    if distilled_root is not None:
        from .distilled_sources import load_distilled
        entries.extend(load_distilled(distilled_root))
    if layout_station is not None and layout_root is None:
        raise ContractError("layout_station requires layout_root")
    if layout_root is not None:
        from .layout_search import load_layouts
        entries.extend(load_layouts(layout_root, layout_station))
    if repo_entries:
        catalog_path = Path(os.path.abspath(os.fspath(repo_entries)))
        try:
            raw = _repo_reader().read_repo_file(catalog_path.parent, catalog_path.name,
                                                limit=16 * 1024 * 1024)
            data = _strict_json_loads(raw.decode("utf-8-sig"))
        except (ContractError, OSError, ValueError, UnicodeError) as exc:
            raise ContractError(f"Cannot read repo catalog {catalog_path}: {exc}") from exc
        if not isinstance(data, list):
            raise ContractError("Repo entries must be a list")
        catalog_ids = set()
        for record in data:
            validate_entry(record)
            key = record["id"].casefold()
            if key in catalog_ids:
                raise ContractError(f"Duplicate catalog ID: {record['id']}")
            catalog_ids.add(key)
        root = None
        for record in data:
            assets = record.get("assets")
            if assets is None and record.get("asset") is not None:
                assets = [record["asset"]]
            if assets is not None:
                try:
                    if root is None:
                        root = resource_root()
                    if record.get("assets") is not None:
                        _verify_repo_bundle(root, record)
                    else:
                        asset = assets[0]
                        _repo_reader().read_repo_file(root, asset["path"], limit=64 * 1024 * 1024,
                                                      expected_sha256=asset["sha256"])
                except (ContractError, OSError, ValueError) as exc:
                    category = "bundle" if record.get("assets") is not None else "asset"
                    path = f" ({assets[0]['path']})" if category == "asset" else ""
                    raise ContractError(f"Cannot verify repo {category} for {record['id']}{path}: {exc}") from exc
            entries.append(dict(record, origin="repo"))
    if station is not None:
        station = Path(station)
        if station.is_symlink() or not station.is_dir() or (station / "effect-library").is_symlink():
            raise ContractError("Invalid station or symlink")
        directory = station / "effect-library" / "entries"
        if directory.is_symlink():
            raise ContractError("Station entries must not be a symlink")
        if not directory.exists():
            raise ContractError("Station entries directory is missing")
        if os.name == "nt":
            from ._native_windows import search_experiment
            try:
                experimental = search_experiment(directory)
                entries.extend(dict(record, origin="station") for record in experimental)
            except (OSError, ValueError, KeyError) as exc:
                if "0xc0000034" in str(exc):
                    raise ContractError(f"Invalid or missing station entry manifest: {exc}") from exc
                raise ContractError(f"Invalid experimental station entry: {exc}") from exc
        else:
            raise ContractError("Station search unavailable: secure handle-relative reader not verified on this platform")
    seen = set()
    for e in entries:
        if e["id"].casefold() in seen:
            raise ContractError(f"Duplicate ID: {e['id']}")
        seen.add(e["id"].casefold())
    terms, groups = _query_groups(query)
    if query.strip() and not terms:
        return []
    matches = []
    exact_query = unicodedata.normalize("NFC", query.strip()).casefold()
    for e in entries:
        if runtime_terms is not None:
            runtime = e.get("runtime")
            if not isinstance(runtime, str) or not set(runtime_terms).issubset(re.findall(r"\d+(?:\.\d+)+|\w+", _fold(runtime))):
                continue
        if any((e["checks"][k[6:]] != v if k.startswith("check.") else
                not _ratio_matches(e, v, include_unknown_ratio) if k == "ratio" else
                v not in e.get({"role": "roles", "technique": "techniques"}.get(k, k), []) if k in {"role", "technique"} else
                e.get(k) != v) for k, v in filters.items() if k != "runtime"):
            continue
        fields = [re.findall(r"\w+", _fold(value)) for key in (
            "id", "name", "description", "tags", "roles", "techniques", "ratios",
            "runtime", "source", "repository", "prompt_text")
                  for value in _text_values(e.get(key))]
        assets = e.get("assets") or ([e["asset"]] if isinstance(e.get("asset"), dict) else [])
        fields.extend(re.findall(r"\w+", _fold(asset["path"])) for asset in assets
                      if isinstance(asset, dict) and isinstance(asset.get("path"), str))
        exact_id = bool(exact_query) and unicodedata.normalize("NFC", e["id"]).casefold() == exact_query
        if not exact_id and any(not any(_contains_phrase(field, alternative)
                                        for alternative in group for field in fields)
                                for group in groups):
            continue
        consecutive = bool(terms) and any(_contains_phrase(field, terms) for field in fields)
        matches.append((-exact_id, -consecutive, e["id"], e))
    matches.sort(key=lambda item: (item[0], item[1], item[2]))
    return [e for _, _, _, e in matches[:limit]]
