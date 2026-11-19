"""Partial, read-only adapter for the existing theme layout catalog."""
import os
import re

from video_studio.contract import ContractError
from .catalog import CHECKS

_SECTIONS = {"2", "3", "4", "5", "8"}
_ROW = re.compile(r"^\|\s*\*\*([a-z0-9]+(?:-[a-z0-9]+)*)\s*·\s*(S|A|B|NEW)\*\*\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")


def parse_layouts(document, source, origin):
    """Index single-ID table rows only; grouped IDs and free-form media are omitted."""
    section = None
    seen_sections = set()
    rows = []
    seen = set()
    ratios = {}
    uses = {}
    ratio_columns = {}
    fence = None
    for line in document.splitlines():
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            token = fence_match.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        heading = re.match(r"^##\s+(\d+)\.\s+", line)
        if heading:
            section = heading.group(1)
            if section in _SECTIONS:
                if section in seen_sections:
                    raise ContractError("Duplicate layout catalog section")
                seen_sections.add(section)
            continue
        if re.match(r"^#{1,2}\s+", line):
            section = None
            continue
        if section == "1" and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) == 4:
                if all(any(ratio in cell for cell in cells[2:]) for ratio in ("16:9", "9:16")):
                    ratio_columns = {ratio: next(i for i in (2, 3) if ratio in cells[i])
                                     for ratio in ("16:9", "9:16")}
                    continue
                for ratio, index in ratio_columns.items():
                    cell = cells[index]
                    for identifier in re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", cell):
                        ratios.setdefault(identifier, set()).add(ratio)
                        uses.setdefault(identifier, set()).add(cells[0])
        if section not in _SECTIONS:
            continue
        match = _ROW.fullmatch(line)
        if not match:
            continue
        identifier, tier, anatomy, motion = match.groups()
        if identifier in seen or not anatomy or not motion:
            raise ContractError("Duplicate or incomplete layout record")
        seen.add(identifier)
        rows.append({"id": "LAYOUT-" + identifier, "name": identifier,
                     "kind": "reference", "maturity": "reference_only", "rights": "unknown",
                     "source": source, "origin": origin, "layout_tier": tier,
                     "description": anatomy + " | " + motion, "tags": ["layout", identifier],
                     "roles": [], "techniques": [], "ratios": [],
                     "checks": dict.fromkeys(CHECKS, "not_run"), "checks_origin": "default_not_run"})
    if seen_sections != _SECTIONS or not rows or fence is not None:
        raise ContractError("Unsupported or incomplete layout catalog format")
    for row in rows:
        row["ratios"] = sorted(ratios.get(row["name"], ()))
        row["tags"].extend(sorted(uses.get(row["name"], ())))
    return rows


def load_layouts(repo_root, station=None):
    """Select one catalog; Windows station leaf absence alone permits fallback."""
    if station is not None:
        if os.name != "nt":
            raise ContractError("Station layout search unavailable: secure absence check not verified on this platform")
        from . import _native_windows as native
        try:
            with native.open_root_chain_read(os.path.abspath(os.fspath(station))) as (root, stack):
                try:
                    handle = native._reader_open(root, "THEME-LIBRARY.md", False)
                except native.ReaderOpenError as exc:
                    if exc.ntstatus != 0xC0000034:
                        raise
                else:
                    stack.callback(native.close, handle)
                    data = native._reader_read_handle(handle, 2 * 1024 * 1024, None)
                    return parse_layouts(data.decode("utf-8-sig"), "THEME-LIBRARY.md", "layout_station")
        except (OSError, ValueError, UnicodeError) as exc:
            raise ContractError(f"Cannot safely read station layout catalog: {exc}") from exc
    from .search import _repo_reader
    try:
        data = _repo_reader().read_repo_file(repo_root, "docs/THEME-LIBRARY.md", limit=2 * 1024 * 1024)
        return parse_layouts(data.decode("utf-8-sig"), "docs/THEME-LIBRARY.md", "layout_repo")
    except (OSError, ValueError, UnicodeError) as exc:
        raise ContractError(f"Cannot safely read repo layout catalog: {exc}") from exc
