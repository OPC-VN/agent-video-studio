"""Pure validation of template metadata and project paths."""

import os
import re
import unicodedata
from collections.abc import Iterable
from pathlib import PurePosixPath

from video_studio._paths import is_device_name
from video_studio.contract import ContractError
from .catalog import _relative

CONTRACT_HEADINGS = (
    'Nguồn gốc và quyền',
    'Bất biến sáng tạo',
    'Hợp đồng câu chuyện và thay thế',
    'Thời gian và khung hình',
    'Yêu cầu vật liệu',
    'Kiểm duyệt',
)
LOCKED_EXTS = frozenset({'.glb', '.gltf', '.geojson', '.wasm', '.pmtiles', '.pbf', '.hdr', '.bin'})
_IS_NT = os.name == 'nt'


def _parts(path):
    if not isinstance(path, str):
        raise ContractError('Path must be a string')
    parts = _relative(path).parts
    if '/'.join(parts) != path or len(parts) > 8:
        raise ContractError('Path must be canonical and within depth limit')
    from ._native_windows import _component
    for part in parts:
        if is_device_name(part):
            raise ContractError('Invalid path component')
        try:
            _component(part)
        except (ValueError, UnicodeError) as exc:
            raise ContractError('Invalid path component') from exc
    return parts


def _key(parts):
    return tuple(unicodedata.normalize('NFC', part).casefold() for part in parts)


def project_relpath(entry: dict, path: str) -> str:
    root = _parts(entry.get('template_root'))
    parts = _parts(path)
    if len(parts) <= len(root) or parts[:len(root)] != root:
        raise ContractError('Asset must be inside template root')
    return '/'.join(parts[len(root):])


def check_project_paths(paths: Iterable[str]) -> None:
    from video_studio.render import ASSET_DIR, FORBIDDEN_NAMES, STATIC_EXTS
    seen = set()
    normalized_dirs = {}
    has_index = False
    for path in paths:
        parts = _parts(path)
        if any(part.lower() in FORBIDDEN_NAMES for part in parts):
            raise ContractError('Forbidden project name')
        if len(parts) > 1 and parts[0] != ASSET_DIR:
            raise ContractError('Only assets directory is allowed at project root')
        suffix = PurePosixPath(parts[-1]).suffix.lower()
        if suffix not in STATIC_EXTS or suffix in LOCKED_EXTS:
            raise ContractError('Project file is not an allowed static resource')
        key = _key(parts)
        if any(key == other or key[:len(other)] == other or other[:len(key)] == key for other in seen):
            raise ContractError('Conflicting project paths')
        for length in range(1, len(parts)):
            prefix = parts[:length]
            previous = normalized_dirs.setdefault(_key(prefix), prefix)
            if previous != prefix:
                raise ContractError('Conflicting project directory names')
        seen.add(key)
        has_index = has_index or path == 'index.html'
    if not has_index:
        raise ContractError('Project requires root index.html')


def validate_template_entry(entry: dict) -> None:
    if not isinstance(entry, dict) or entry.get('kind') != 'template':
        raise ContractError('Expected template entry')
    assets = entry.get('assets')
    if 'asset' in entry or not isinstance(assets, list) or not 2 <= len(assets) <= 64:
        raise ContractError('Template requires a multi-file bundle')
    root = _parts(entry.get('template_root'))
    contract = _parts(entry.get('contract_path'))
    digest = entry.get('contract_sha256')
    if not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest):
        raise ContractError('Template requires contract SHA-256')
    root_key, contract_key = _key(root), _key(contract)
    if contract_key[:len(root_key)] == root_key or root_key[:len(contract_key)] == contract_key:
        raise ContractError('Contract must be outside project tree')
    paths = []
    for asset in assets:
        if not isinstance(asset, dict):
            raise ContractError('Invalid template asset')
        asset_path = asset.get('path')
        if _key(_parts(asset_path)) == contract_key:
            raise ContractError('Contract cannot be an asset')
        paths.append(project_relpath(entry, asset_path))
    check_project_paths(paths)
    if entry.get('maturity') == 'implemented' and entry.get('checks', {}).get('render') != 'pass':
        raise ContractError('implemented template requires render evidence')


def _unfenced_lines(text: str, include_fenced: bool = False):
    fence_char = None
    fence_length = 0
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence_char is None and match:
            if match.group(1)[0] != '`' or '`' not in match.group(2):
                fence_char = match.group(1)[0]
                fence_length = len(match.group(1))
                continue
        elif fence_char is not None and match:
            if (match.group(1)[0] == fence_char and len(match.group(1)) >= fence_length
                    and not match.group(2).strip()):
                fence_char = None
                continue
        if fence_char is None:
            yield line, False
        elif include_fenced:
            yield line, True


def _sections(text: str, include_fenced: bool = False) -> list[tuple[str, list[str]]]:
    sections = []
    for line, fenced in _unfenced_lines(text, include_fenced):
        match = None if fenced else re.match(r'^ {0,3}##(?!#)\s+', line)
        heading = line[match.end():].rstrip() if match else ''
        if heading:
            sections.append((heading, []))
        elif sections:
            sections[-1][1].append(line)
    return sections


def contract_headings_of(text: str) -> list[str]:
    return [re.sub(r'^\d+\.\s+', '', heading) for heading, _ in _sections(text)]


def _cells(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith('|') or not line.endswith('|'):
        return []
    return [cell.strip() for cell in line[1:-1].split('|')]


def slot_files(text: str) -> list[str]:
    sections = _sections(text)
    if len(sections) < 3:
        raise ContractError('Contract is missing the slot section')
    lines = sections[2][1]
    header = ['chỗ thay', 'file', 'số lần xuất hiện', 'kiểu nội dung', 'giới hạn']
    files = []
    found = False
    index = 0
    while index < len(lines):
        if [cell.casefold() for cell in _cells(lines[index])] != header:
            index += 1
            continue
        if found or index + 1 >= len(lines):
            raise ContractError('Invalid slot table')
        found = True
        separator = _cells(lines[index + 1])
        if len(separator) != 5 or not all(re.fullmatch(r':?-{3,}:?', cell) for cell in separator):
            raise ContractError('Invalid slot table separator')
        index += 2
        while index < len(lines) and _cells(lines[index]):
            cells = _cells(lines[index])
            if len(cells) != 5 or not all(cells):
                raise ContractError('Invalid slot table row')
            if not re.fullmatch(r'[0-9]+', cells[2]) or not any(c != '0' for c in cells[2]):
                raise ContractError('Slot count must be a positive integer')
            files.append(cells[1])
            index += 1
    if not found or not files:
        raise ContractError('Slot table requires at least one row')
    return files


def check_contract(raw: bytes, entry: dict, project_paths: Iterable[str]) -> None:
    """Check verified snapshot bytes; the caller is responsible for digest verification."""
    if not isinstance(raw, bytes) or len(raw) > 1024 * 1024:
        raise ContractError('Contract must be bytes no larger than 1 MiB')
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ContractError('Contract must be UTF-8') from exc
    sections = _sections(text, include_fenced=True)
    expected = [f'{number}. {heading}' for number, heading in enumerate(CONTRACT_HEADINGS, 1)]
    if [heading for heading, _ in sections] != expected:
        raise ContractError('Contract must have six ordered headings')
    if any(not any(line.strip() for line in body) for _, body in sections):
        raise ContractError('Contract sections must not be empty')
    paths = set(project_paths)
    if any(path not in paths for path in slot_files(text)):
        raise ContractError('Slot file must belong to the project bundle')


def load_template(identifier: str, repo_root: os.PathLike | str | None = None) -> tuple[dict, dict[str, bytes]]:
    """Load and validate a repository template as an in-memory snapshot."""
    from . import resources
    from .catalog import validate_entry
    from .search import _strict_json_loads

    if _IS_NT:
        from . import _native_windows as reader
    else:
        from . import _posix_fs as reader
    if not isinstance(identifier, str):
        raise ContractError('Invalid repository template ID')
    root = resources.resource_root() if repo_root is None else repo_root
    catalog_path = 'skills/video-theme-library/assets/effect-library/entries.json'
    try:
        raw = reader.read_repo_file(root, catalog_path, limit=16 * 1024 * 1024)
        records = _strict_json_loads(raw.decode('utf-8-sig'))
    except (ContractError, OSError, ValueError, UnicodeError) as exc:
        raise ContractError(f'Cannot read catalog for {identifier}: {catalog_path}') from exc
    if not isinstance(records, list):
        raise ContractError(f'Invalid catalog for {identifier}: {catalog_path}')
    seen = set()
    selected = None
    for record in records:
        validate_entry(record)
        key = record['id'].casefold()
        if key in seen:
            raise ContractError(f'Duplicate catalog ID: {record["id"]}')
        seen.add(key)
        if record['id'] == identifier:
            selected = record
    if selected is None:
        raise ContractError(f'Template not found: {identifier}')
    if selected['kind'] != 'template' or selected['rights'] not in {'owned', 'licensed'}:
        raise ContractError(f'Entry is not a reusable template: {identifier}')
    contract_path = selected['contract_path']
    try:
        contract = reader.read_repo_file(root, contract_path, limit=1024 * 1024,
                                         expected_sha256=selected['contract_sha256'])
    except (ContractError, OSError, ValueError) as exc:
        raise ContractError(f'Cannot read contract for {identifier}: {contract_path}') from exc
    try:
        snapshots = reader.read_repo_files(root, selected['assets'], max_total=64 * 1024 * 1024)
    except ContractError as exc:
        raise ContractError(f'Cannot read assets for {identifier}: {exc}') from exc
    except (OSError, ValueError) as exc:
        raise ContractError(f'Cannot read assets for {identifier}') from exc
    paths = [project_relpath(selected, asset['path']) for asset in selected['assets']]
    files = {path: snapshots[asset['path']] for path, asset in zip(paths, selected['assets'])}
    check_contract(contract, selected, paths)
    return selected, files


class DestinationStateUncertain(OSError):
    """Destination needs inspection before any retry."""

    def __init__(self, remaining: tuple[str, ...]):
        self.remaining = tuple(remaining)
        super().__init__('Destination state uncertain; inspect before retrying')


def plan_tree(files: dict[str, bytes]) -> tuple[list[str], list[tuple[str, bytes]]]:
    """Validate the complete snapshot and plan deterministic creation order."""
    if not isinstance(files, dict) or not 2 <= len(files) <= 64:
        raise ContractError('Template snapshot requires 2 to 64 files')
    if any(not isinstance(data, bytes) for data in files.values()):
        raise ContractError('Template snapshot values must be bytes')
    if sum(len(data) for data in files.values()) > 64 * 1024 * 1024:
        raise ContractError('Template snapshot exceeds 64 MiB')
    check_project_paths(files)
    directories = set()
    for path in files:
        parts = _parts(path)
        for length in range(1, len(parts)):
            prefix = parts[:length]
            directories.add('/'.join(prefix))
    return sorted(directories, key=lambda path: (path.count('/'), path)), sorted(files.items())


def write_project(files: dict[str, bytes], dest: os.PathLike | str) -> dict[str, int]:
    """Write only a validated snapshot through the platform-specific writer."""
    dirs, ordered = plan_tree(files)
    if _IS_NT:
        from . import _native_windows as writer
    else:
        from . import _posix_fs as writer
    writer.write_tree(dirs, ordered, dest)
    return {'files': len(ordered), 'bytes': sum(len(data) for _, data in ordered)}


def materialize_template(identifier: str, dest, repo_root=None) -> dict:
    """Snapshot a template before writing its validated assets to a new project."""
    _, files = load_template(identifier, repo_root)
    counts = write_project(files, dest)
    return {'ok': True, 'id': identifier, 'into': os.fspath(dest), **counts}
