"""Pinned runtime libraries: validated lock and bounded, verified reads."""
import base64
import binascii
import hashlib
import json
import os
import re
import stat
from collections.abc import Iterable, Mapping
from typing import Any
from importlib import resources
from urllib.parse import urlsplit

from . import _env
from .contract import ContractError, EngineError, StationMissing

_NAME = re.compile(r'^[a-z0-9]+(?:[.-][a-z0-9]+)*$')
_VERSION = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*)?$')
_DEST = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*\.(?:js|mjs|css)$', re.I)
_HEX = re.compile(r'^[a-f0-9]{64}$')
_RESERVED = re.compile(r'^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)', re.I)


def lock_path() -> str:
    return str(resources.files('video_studio').joinpath('locks', 'runtime-libs.json'))


def _bad(where):
    raise ContractError(f'Khoá runtime không hợp lệ: {where}')


def _component(value, pattern):
    return isinstance(value, str) and bool(pattern.fullmatch(value)) and not _RESERVED.match(value)


def load_lock(path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    try:
        with open(path or lock_path(), encoding='utf-8-sig') as f:
            data = json.load(f)
    except (OSError, ValueError, TypeError) as exc:
        raise ContractError(f'Không đọc được khoá runtime: {exc}') from exc
    if not isinstance(data, dict) or data.get('schema_version') != 1 or type(data.get('schema_version')) is not int:
        _bad('schema_version')
    packages, libs = data.get('packages'), data.get('libs')
    if not isinstance(packages, dict) or not packages or not isinstance(libs, dict) or not libs:
        _bad('packages/libs')
    for name, p in packages.items():
        if not _component(name, _NAME) or not isinstance(p, dict): _bad(f'packages.{name}')
        if not _component(p.get('version'), _VERSION): _bad(f'packages.{name}.version')
        url = p.get('tarball_url')
        try: u = urlsplit(url) if isinstance(url, str) else None
        except ValueError: u = None
        if not u or u.scheme != 'https' or u.netloc != 'registry.npmjs.org' or not u.path or u.query or u.fragment: _bad(f'packages.{name}.tarball_url')
        if not isinstance(p.get('tarball_sha256'), str) or not _HEX.fullmatch(p['tarball_sha256']): _bad(f'packages.{name}.tarball_sha256')
        try:
            integrity = p['npm_integrity']
            if not isinstance(integrity, str) or not integrity.startswith('sha512-') or len(base64.b64decode(integrity[7:], validate=True)) != 64: raise ValueError()
        except (KeyError, ValueError, binascii.Error): _bad(f'packages.{name}.npm_integrity')
        if type(p.get('tarball_max_bytes')) is not int or p['tarball_max_bytes'] <= 0: _bad(f'packages.{name}.tarball_max_bytes')
        lic = p.get('license')
        if not isinstance(lic, dict) or any(not isinstance(lic.get(k), str) or not lic[k] for k in ('id', 'terms_url', 'read_on')): _bad(f'packages.{name}.license')
    for name, lib in libs.items():
        if not _component(name, _NAME) or not isinstance(lib, dict): _bad(f'libs.{name}')
        if not isinstance(lib.get('package'), str) or lib['package'] not in packages: _bad(f'libs.{name}.package')
        if not isinstance(lib.get('requires'), list) or any(not isinstance(x, str) or x not in libs for x in lib['requires']): _bad(f'libs.{name}.requires')
        ms = lib.get('members')
        if not isinstance(ms, list) or not ms: _bad(f'libs.{name}.members')
        for m in ms:
            if not isinstance(m, dict): _bad(f'libs.{name}.members')
            member, dest = m.get('member'), m.get('dest')
            if not isinstance(member, str) or '\\' in member or not member.startswith('package/') or any(x in ('', '.', '..') for x in member.split('/')): _bad(f'libs.{name}.member')
            if not _component(dest, _DEST) or '..' in dest: _bad(f'libs.{name}.dest')
            if not isinstance(m.get('file_sha256'), str) or not _HEX.fullmatch(m['file_sha256']): _bad(f'libs.{name}.file_sha256')
            if type(m.get('max_bytes')) is not int or m['max_bytes'] <= 0: _bad(f'libs.{name}.max_bytes')
    for name in libs:
        seen = set()
        for dep in resolve([name], data):
            for m in libs[dep]['members']:
                key = m['dest'].casefold()
                if key in seen: _bad(f'libs.{name}.dest trùng: {m["dest"]}')
                seen.add(key)
    return data


def _entry(kind, name, lock):
    entries = (lock or load_lock())[kind]
    if name not in entries:
        raise ContractError(f'{kind}: {name!r} không hợp lệ; chọn: {", ".join(sorted(entries))}')
    return entries[name]


def package_entry(name: str, lock: dict[str, Any] | None = None) -> dict[str, Any]: return _entry('packages', name, lock)
def lib_entry(name: str, lock: dict[str, Any] | None = None) -> dict[str, Any]: return _entry('libs', name, lock)
def members(name: str, lock: dict[str, Any] | None = None) -> list[dict[str, Any]]: return lib_entry(name, lock)['members']


def resolve(names: Iterable[str], lock: dict[str, Any] | None = None) -> list[str]:
    lock = lock or load_lock(); order = []; done = set(); active = set()
    def visit(name):
        entry = lib_entry(name, lock)
        if name in active: _bad(f'libs.{name}.requires vòng')
        if name in done: return
        active.add(name)
        for dep in entry['requires']: visit(dep)
        active.remove(name); done.add(name); order.append(name)
    for name in names: visit(name)
    return order


def station_dir(package: str, station: str | os.PathLike[str] | None = None) -> str:
    p = package_entry(package)
    return os.path.join(os.fspath(station) if station is not None else _env.station_dir(), 'runtime-libs', package, p['version'])


def station_path(lib: str, dest: str, station: str | os.PathLike[str] | None = None) -> str:
    entry = lib_entry(lib)
    if dest not in [m['dest'] for m in entry['members']]: raise ContractError(f'Đích {dest!r} không thuộc {lib}')
    return os.path.join(station_dir(entry['package'], station), dest)


def _read_bounded(path: str | os.PathLike[str], max_bytes: int) -> bytes:
    try:
        if os.name == 'nt':
            from .effect_library import _native_windows as native
            parent, name = os.path.split(os.path.abspath(path)); root = native.open_root(parent)
            try:
                handle = native.open_file(root, name)
                try: data = native.read_all(handle, max_bytes)
                finally: native.close(handle)
            finally: native.close(root)
        else:
            # Traverse from an anchored root with openat; O_NOFOLLOW on only the
            # final file would still allow a parent directory to redirect the read.
            raw = os.fsdecode(path)
            if raw.startswith('//') or '..' in raw.split('/'):
                raise ValueError('đường dẫn không an toàn')
            full = os.path.abspath(raw)
            parts = [part for part in full.split('/') if part and part != '.']
            if not parts:
                raise ValueError('đường dẫn không phải tệp')
            directory = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                for part in parts[:-1]:
                    child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                    os.close(directory)
                    directory = child
                fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | getattr(os, 'O_NONBLOCK', 0), dir_fd=directory)
                try:
                    s = os.fstat(fd)
                    if not stat.S_ISREG(s.st_mode) or s.st_size > max_bytes: raise ValueError('tệp không thường hoặc quá lớn')
                    with os.fdopen(fd, 'rb', closefd=False) as f: data = f.read(max_bytes + 1)
                    if len(data) > max_bytes: raise ValueError('tệp quá lớn')
                finally: os.close(fd)
            finally: os.close(directory)
    except (OSError, ValueError) as exc:
        raise ContractError(f'Không đọc được thư viện: {exc}') from exc
    return data


def read_verified(path: str | os.PathLike[str], sha256: str, max_bytes: int) -> bytes:
    data = _read_bounded(path, max_bytes)
    if hashlib.sha256(data).hexdigest() != sha256: raise ContractError('SHA-256 không khớp khoá runtime')
    return data


def status(station: str | os.PathLike[str] | None = None) -> list[dict[str, Any]]:
    lock = load_lock(); result = []
    for name, lib in lock['libs'].items():
        state = 'ok'
        for dep in resolve([name], lock):
            entry = lock['libs'][dep]
            for m in entry['members']:
                path = station_path(dep, m['dest'], station)
                if not os.path.lexists(path):
                    if state != 'mismatch': state = 'missing'
                else:
                    try: read_verified(path, m['file_sha256'], m['max_bytes'])
                    except ContractError: state = 'mismatch'
        p = lock['packages'][lib['package']]
        result.append(dict(name=name, package=lib['package'], version=p['version'], state=state, path_rel=f"runtime-libs/{lib['package']}/{p['version']}"))
    return result


def load(names: Iterable[str], station: str | os.PathLike[str] | None = None, overrides: Mapping[str, str | os.PathLike[str]] | None = None) -> dict[str, bytes]:
    lock = load_lock(); overrides = overrides or {}; output = {}; keys = set()
    for name in resolve(names, lock):
        ms = members(name, lock)
        for m in ms:
            key = m['dest'].casefold()
            if key in keys: raise ContractError(f'Đích thư viện trùng: {m["dest"]}')
            keys.add(key)
            path = overrides.get(f'{name}:{m["dest"]}') or (overrides.get(name) if len(ms) == 1 else None) or station_path(name, m['dest'], station)
            if not os.path.lexists(path): raise StationMissing(f'Thiếu thư viện {name}; chạy: video-studio libs fetch {name}')
            output[m['dest']] = read_verified(path, m['file_sha256'], m['max_bytes'])
    return output


def fetch_plan(names, station=None):
    lock = load_lock()
    selected = resolve(names or list(lock['libs']), lock)
    plans = {}
    for name in selected:
        lib = lock['libs'][name]; package = lib['package']; p = lock['packages'][package]
        if package not in plans:
            plans[package] = dict(package=package, version=p['version'], url=p['tarball_url'],
                                  max_bytes=p['tarball_max_bytes'], libs=[], license=p['license']['id'],
                                  terms_url=p['license']['terms_url'], dest_dir=station_dir(package, station))
        plans[package]['libs'].append(name)
    return list(plans.values())


def _extract_package(blob, package, selected, lock):
    import base64
    import gzip
    import io
    import tarfile
    import zlib
    p = lock['packages'][package]
    if len(blob) > p['tarball_max_bytes'] or hashlib.sha256(blob).hexdigest() != p['tarball_sha256']:
        raise ContractError('Tarball vượt trần hoặc SHA-256 không khớp')
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512(blob).digest()).decode('ascii')
    if integrity != p['npm_integrity']: raise ContractError('npm integrity không khớp')
    expected = {}
    for name in selected:
        for m in lock['libs'][name]['members']:
            if m['member'] in expected and expected[m['member']] != m:
                raise ContractError('Member tarball trùng định nghĩa')
            expected[m['member']] = m
    output = {}
    try:
        # Bound the entire decompressed tar, including unselected members.
        with gzip.GzipFile(fileobj=io.BytesIO(blob), mode='rb') as compressed:
            unpacked = compressed.read(128 * 1024 * 1024 + 1)
        if len(unpacked) > 128 * 1024 * 1024: raise ContractError('Tarball giải nén vượt trần')
        with tarfile.open(fileobj=io.BytesIO(unpacked), mode='r:') as archive:
            found = set()
            for index, item in enumerate(archive):
                if index >= 8192: raise ContractError('Tarball quá nhiều member')
                # Never materialize tar paths; reject ambiguous entries anywhere in archive.
                if item.name.startswith('/') or '\\' in item.name or any(x in ('.', '..') for x in item.name.split('/')):
                    raise ContractError('Đường tarball không an toàn')
                if item.name not in expected: continue
                if item.name in found or not item.isfile(): raise ContractError('Member tarball trùng hoặc không phải tệp')
                found.add(item.name); m = expected[item.name]
                if item.size > m['max_bytes']: raise ContractError('Member vượt trần')
                stream = archive.extractfile(item)
                if stream is None: raise ContractError('Không đọc được member')
                data = stream.read(m['max_bytes'] + 1)
                if len(data) != item.size or hashlib.sha256(data).hexdigest() != m['file_sha256']:
                    raise ContractError('SHA-256 member không khớp')
                output[m['dest']] = data
            if found != set(expected): raise ContractError('Thiếu member trong tarball')
    except (tarfile.TarError, EOFError, OSError, ValueError, zlib.error, RecursionError) as exc:
        raise ContractError(f'Tarball không hợp lệ: {exc}') from exc
    return output


def _publish_files(station, package, version, files, *, project=False):
    """Create files without replacing user data, anchored to a non-reparse station."""
    import uuid
    if not project and not os.path.isdir(station):
        raise StationMissing('Chưa có trạm; chạy: video-studio init')
    if project and '..' in os.fspath(station).replace('\\', '/').split('/'):
        raise ContractError('Đường project không an toàn')
    if os.name == 'nt':
        from .effect_library import _native_windows as native
        handles = []; pending = []
        try:
            if project:
                absolute = os.path.abspath(station)
                drive, _ = os.path.splitdrive(absolute)
                if not drive or drive.startswith('\\\\'): raise ContractError('Project phải nằm trên ổ cục bộ')
                ancestor = absolute
                parts = []
                while not os.path.isdir(ancestor):
                    ancestor, part = os.path.split(ancestor)
                    if not part: raise ContractError('Không có thư mục cha của project')
                    parts.insert(0, part)
                # open_root rejects any reparse point in the entire ancestor path.
                root = native.open_root(ancestor)
            else:
                root = native.open_root(os.path.abspath(station))
                parts = ['runtime-libs', package, version]
            handles.append(root)
            for part in parts:
                try: child = native.open_directory(root, part)
                except OSError: child = native.create_directory(root, part)
                handles.append(child); root = child
            for dest, data in files.items():
                try:
                    old = native.open_file(root, dest)
                except OSError:
                    old = None
                if old is not None:
                    try:
                        try: existing = native.read_all(old, len(data))
                        except ValueError as exc: raise ContractError(f'Không ghi đè tệp sẵn có: {dest}') from exc
                    finally: native.close(old)
                    if existing != data: raise ContractError(f'Không ghi đè tệp sẵn có: {dest}')
                    continue
                h = native.create_file(root, 'stage-' + uuid.uuid4().hex); pending.append((h, dest))
                native.write_all(h, data); native.flush(h)
            for h, dest in pending:
                native.rename_no_replace(h, root, dest)
            for h, _ in pending: native.close(h)
            pending.clear()
        except BaseException:
            for h, _ in pending:
                try: native.delete_on_close(h)
                except OSError: pass
                try: native.close(h)
                except OSError: pass
            raise
        finally:
            for h in reversed(handles): native.close(h)
    else:
        # Open each directory by handle to prevent symlink traversal or swaps.
        raw = os.path.abspath(station); parts = [x for x in raw.split('/') if x]
        root = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW); pending = []
        staging = None; stage_name = None; stage_identity = None
        try:
            for part in parts + ([] if project else ['runtime-libs', package, version]):
                try: child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root)
                except FileNotFoundError:
                    os.mkdir(part, dir_fd=root)
                    child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root)
                os.close(root); root = child
            for dest, data in files.items():
                try: existing = os.open(dest, os.O_RDONLY | os.O_NOFOLLOW | getattr(os, 'O_NONBLOCK', 0), dir_fd=root)
                except FileNotFoundError: existing = None
                if existing is not None:
                    try:
                        st = os.fstat(existing)
                        if not stat.S_ISREG(st.st_mode):
                            raise ContractError(f'Không ghi đè tệp sẵn có: {dest}')
                        with os.fdopen(existing, 'rb', closefd=False) as f: old = f.read(len(data) + 1)
                        if old != data: raise ContractError(f'Không ghi đè tệp sẵn có: {dest}')
                    finally: os.close(existing)
                    continue
                if staging is None:
                    stage_name = 'stage-' + uuid.uuid4().hex
                    os.mkdir(stage_name, 0o700, dir_fd=root)
                    staging = os.open(stage_name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root)
                    st = os.fstat(staging)
                    if (not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid() or
                            stat.S_IMODE(st.st_mode) != 0o700):
                        raise ContractError('Thư mục staging không riêng tư hoặc sai chủ')
                    stage_identity = (st.st_dev, st.st_ino)
                temp = 'item-' + uuid.uuid4().hex
                fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=staging)
                pending.append((temp, dest))
                with os.fdopen(fd, 'wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
            published = []
            for temp, dest in pending:
                try:
                    os.link(temp, dest, src_dir_fd=staging, dst_dir_fd=root, follow_symlinks=False)
                except OSError as exc:
                    done = ', '.join(published) if published else '(không có)'
                    error = ContractError if isinstance(exc, FileExistsError) else EngineError
                    retry = ('kiểm tra project rồi thử lại' if project else
                             f'kiểm tra tệp đích và xung đột, rồi chạy lại video-studio libs fetch {package}')
                    raise error(
                        f'Cấp thư viện dở dang; đã cấp: {done}. {retry}: {exc}'
                    ) from exc
                published.append(dest)
        finally:
            try:
                if staging is not None:
                    for temp, _ in pending:
                        try: os.unlink(temp, dir_fd=staging)
                        except FileNotFoundError: pass
                    # Removing this directory by name races another process renaming
                    # it. Retain it empty rather than delete somebody else's directory.
                    if stage_identity is not None:
                        from . import contract
                        contract.log(f'Giữ thư mục staging rỗng {stage_name}; không xoá theo tên.')
            finally:
                if staging is not None: os.close(staging)
                os.close(root)


def fetch(names, yes, from_file=None, station=None, fetcher=None):
    from . import _netfetch
    from .contract import EngineError
    lock = load_lock(); plan = fetch_plan(names, station)
    if not yes: raise ContractError('needs_confirmation')
    station = os.fspath(station) if station is not None else _env.station_dir()
    if not os.path.isdir(station): raise StationMissing('Chưa có trạm; chạy: video-studio init')
    all_members = [(name, m) for item in plan for name in item['libs'] for m in members(name, lock)]
    destinations = [m['dest'] for _, m in all_members]
    if len({name.casefold() for name in destinations}) != len(destinations):
        raise ContractError('Đích thư viện trùng')
    if from_file is not None and isinstance(from_file, dict) and set(from_file) != set(destinations):
        raise ContractError('Thiếu hoặc thừa member --from-file')
    if from_file is not None and not isinstance(from_file, dict) and len(all_members) != 1:
        raise ContractError('Cần DEST=PATH cho từng member')
    result = []
    for item in plan:
        selected = item['libs']; files = {}
        if from_file is not None:
            selected_members = [(n, m) for n in selected for m in members(n, lock)]
            mapping = from_file if isinstance(from_file, dict) else {selected_members[0][1]['dest']: from_file}
            for _, m in selected_members: files[m['dest']] = read_verified(mapping[m['dest']], m['file_sha256'], m['max_bytes'])
        else:
            get = fetcher or _netfetch.fetch_public
            try: final, _, blob = get(item['url'], max_bytes=item['max_bytes'], allowed_hosts={'registry.npmjs.org'})
            except _netfetch.FetchError as exc:
                raise (EngineError if exc.kind == 'network' else ContractError)(str(exc)) from exc
            except OSError as exc: raise EngineError(f'Lỗi mạng: {exc}') from exc
            from urllib.parse import urlsplit
            try: u = urlsplit(final)
            except (TypeError, ValueError) as exc: raise ContractError('URL chuyển hướng không hợp lệ') from exc
            if u.scheme != 'https' or u.netloc != 'registry.npmjs.org': raise ContractError('Host chuyển hướng không được phép')
            if not isinstance(blob, bytes): raise ContractError('Phản hồi không phải bytes')
            files = _extract_package(blob, item['package'], selected, lock)
        _publish_files(station, item['package'], item['version'], files)
        result.append(dict(package=item['package'], libs=selected, files=list(files)))
    return result


def _parser():
    import argparse
    ap = argparse.ArgumentParser(prog='video-studio libs')
    sub = ap.add_subparsers(dest='action', required=True)
    for action in ('status', 'plan', 'fetch', 'path'):
        cmd = sub.add_parser(action)
        if action in ('plan', 'fetch'): cmd.add_argument('names', nargs='*')
        if action == 'path': cmd.add_argument('name')
        if action == 'fetch':
            cmd.add_argument('--yes', action='store_true')
            cmd.add_argument('--from-file', action='append', dest='from_files')
        cmd.add_argument('--json', action='store_true')
    return ap


def main(argv=None):
    from . import contract
    args, code = contract.parse(_parser(), argv)
    if code is not None: return code
    if args.action == 'fetch' and not args.yes:
        try: plan = fetch_plan(args.names)
        except Exception as exc: return contract.run(lambda _: (_ for _ in ()).throw(exc), args, args.json)
        contract.log('Chưa tải gì; kiểm tra kế hoạch và chạy lại với --yes:', json.dumps(plan, ensure_ascii=False))
        if args.json: contract.emit({'ok': False, 'code': 2, 'error': 'needs_confirmation', 'plan': plan})
        return 2
    def run(a):
        if a.action == 'status': result = status()
        elif a.action == 'plan': result = fetch_plan(a.names)
        elif a.action == 'fetch':
            supplied = a.from_files
            if supplied:
                if len(supplied) == 1 and '=' not in supplied[0]: supplied = supplied[0]
                else:
                    pairs = [x.partition('=') for x in supplied]
                    if any(not k or not sep or not v for k, sep, v in pairs) or len({k for k, _, _ in pairs}) != len(pairs):
                        raise ContractError('--from-file cần DEST=PATH, không trùng')
                    supplied = {k: v for k, _, v in pairs}
            result = fetch(a.names, True, from_file=supplied)
        else:
            lock = load_lock(); result = []
            for name in resolve([a.name], lock):
                for m in members(name, lock):
                    path = station_path(name, m['dest'])
                    try: read_verified(path, m['file_sha256'], m['max_bytes'])
                    except ContractError as exc: raise StationMissing(f'Thiếu hoặc lệch {name}; chạy: video-studio libs fetch {name}') from exc
                    result.append({'dest': m['dest'], 'path': path})
        if not a.json:
            if a.action == 'path':
                for entry in result: print(entry['dest'] + '\t' + entry['path'])
            else: print(json.dumps(result, ensure_ascii=False, indent=2))
        return {'items': result}
    return contract.run(run, args, args.json)


_overrides = {}


def set_overrides(mapping: dict[str, str]) -> None:
    global _overrides
    _overrides = dict(mapping)


def get_overrides() -> dict[str, str]:
    return dict(_overrides)


# HTML references are parsed separately from publication, so callers can warn on
# remote code before they opt into the strict gate.
def _html_references(html):
    """Inspect direct HTML references only; inline JavaScript is not parsed."""
    from html.parser import HTMLParser

    class UnsupportedStructure(Exception):
        """Stop instead of guessing how an HTML5 parser would recover."""

    class Reader(HTMLParser):
        svg_children = {'svg': {'path', 'defs', 'rect'}, 'defs': {'pattern'},
                        'pattern': {'path'}, 'path': set(), 'rect': set()}
        svg_attributes = {'class', 'id', 'width', 'height', 'viewbox', 'fill',
                          'stroke', 'stroke-width', 'stroke-linecap',
                          'stroke-linejoin', 'd', 'patternunits', 'aria-hidden'}
        # Only conventional attribute syntax is supported in foreign content.
        # HTMLParser's recovery is deliberately not used to widen this subset.
        svg_start = re.compile(
            r'''<[a-zA-Z][a-zA-Z0-9]*(?:[ \t\n\f\r]+[a-zA-Z][a-zA-Z0-9-]*'''
            r'''[ \t\n\f\r]*=[ \t\n\f\r]*(?:"[^"]*"|'[^']*'|[^\s"'=<>`]+))*'''
            r'''[ \t\n\f\r]*/?>''')

        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.local = []; self.remote = []; self.base = None; self.raw = None; self.templates = 0
            self.svg = []

        def unsupported_structure(self, reason):
            self.remote.append(f'dòng {self.getpos()[0]}: cấu trúc HTML/SVG chưa được hỗ trợ ({reason})')
            raise UnsupportedStructure

        def foreign_start(self, tag, attrs, *, closed=False):
            # Run before raw/RCDATA handling: SVG style/title and MathML can
            # otherwise hide a browser-visible HTML script from HTMLParser.
            # Template contents still affect foreign parsing and may break out
            # of the template. Only actual raw/RCDATA text is inert here.
            if self.raw is not None:
                return False
            if not self.svg and tag != 'svg':
                if tag == 'math' or ':' in tag:
                    self.unsupported_structure('tag hoặc namespace ngoài tập SVG')
                return False
            if self.svg and tag not in self.svg_children[self.svg[-1]]:
                self.unsupported_structure('tag hoặc cây SVG ngoài tập hỗ trợ')
            if not self.svg_start.fullmatch(self.get_starttag_text()):
                self.unsupported_structure('cú pháp thuộc tính SVG')
            seen = set()
            for key, value in attrs:
                if key in seen or value is None:
                    self.unsupported_structure('thuộc tính SVG trùng hoặc thiếu giá trị')
                seen.add(key)
                if key == 'xmlns' and not self.svg and value == 'http://www.w3.org/2000/svg':
                    continue
                if key not in self.svg_attributes:
                    self.unsupported_structure('thuộc tính hoặc namespace SVG ngoài tập hỗ trợ')
            if not closed:
                self.svg.append(tag)
            return True

        def handle_data(self, data):
            # This is an HTML tokenizer marker even when it occurs in a JS
            # string. HTMLParser does not model script escaped/double-escaped
            # states, so never trust the following raw closer in that case.
            if self.cdata_elem == 'script' and '<!--' in data:
                self.unsupported_structure('marker HTML comment trong raw script')
            if self.svg and data.strip(' \t\n\f\r'):
                self.unsupported_structure('nội dung SVG không phải khoảng trắng')

        def parse_comment(self, i, report=1):
            if self.svg:
                self.unsupported_structure('comment trong SVG')
            # Canonical comment bodies contain no double hyphen. Reject other
            # forms before HTMLParser can recover and swallow later HTML.
            text = self.rawdata[i + 4:]
            end = text.find('-->')
            if end < 0 or text.startswith(('>', '->')):
                self.unsupported_structure('HTML comment chưa đóng hoặc mở không chuẩn')
            body = text[:end]
            if '--' in body or '<!--' in text[:end + 3]:
                self.unsupported_structure('HTML comment có -- trong nội dung hoặc marker lồng')
            return super().parse_comment(i, report)

        def handle_comment(self, data):
            if self.svg:
                self.unsupported_structure('comment trong SVG')

        def handle_pi(self, data):
            if self.svg:
                self.unsupported_structure('processing instruction trong SVG')

        def handle_decl(self, decl):
            if self.svg:
                self.unsupported_structure('declaration trong SVG')

        def parse_marked_section(self, i, report=1):
            self.unsupported_structure('CDATA hoặc marked section ngoài raw/RCDATA')

        def parse_html_declaration(self, i):
            if self.raw == 'plaintext':
                return len(self.rawdata)
            if self.raw is None and self.rawdata.startswith('<![', i):
                self.unsupported_structure('CDATA hoặc marked section ngoài raw/RCDATA')
            return super().parse_html_declaration(i)

        def set_cdata_mode(self, elem, *, escapable=False):
            # HTMLParser otherwise treats a literal <script> inside RCDATA as
            # a real script and can swallow the enclosing </textarea>.
            if self.raw is None:
                self._set_raw_mode(elem)
        def _set_raw_mode(self, elem):
            super().set_cdata_mode(elem)
            # Browsers also close raw text for malformed end tags containing
            # attributes or a slash. HTMLParser's default regex misses them.
            # HTML case matching is ASCII-only; Unicode casefold lookalikes
            # such as long s or dotless i must remain raw text.
            self.interesting = re.compile(r'</' + re.escape(elem) + r'(?=[ \t\n\f\r/>])', re.I | re.ASCII)
        def parse_endtag(self, i):
            if self.svg:
                match = re.match(r'</([a-zA-Z][a-zA-Z0-9]*)[ \t\n\f\r]*>', self.rawdata[i:])
                if match is None:
                    self.unsupported_structure('thẻ đóng SVG không chuẩn hoặc chưa hoàn tất')
            if self.cdata_elem is None:
                return super().parse_endtag(i)
            match = re.match(r'</' + re.escape(self.cdata_elem) + r'(?=[ \t\n\f\r/>])',
                             self.rawdata[i:], re.I | re.ASCII)
            if not match:
                return super().parse_endtag(i)
            # A '>' inside a quoted end-tag attribute is not the end of the tag.
            cursor = i + match.end(); quote = None; state = 'before'
            while cursor < len(self.rawdata):
                ch = self.rawdata[cursor]
                if quote:
                    if ch == quote: quote = None; state = 'after_value'
                elif ch == '>':
                    elem = self.cdata_elem
                    self.handle_endtag(elem)
                    self.clear_cdata_mode()
                    return cursor + 1
                elif state == 'before_value':
                    if ch in "'\"": quote = ch
                    elif ch not in ' \t\n\f\r': state = 'unquoted'
                elif state == 'unquoted':
                    if ch in ' \t\n\f\r': state = 'before'
                elif state == 'name':
                    if ch == '=': state = 'before_value'
                    elif ch == '/': state = 'before'
                    elif ch in ' \t\n\f\r': state = 'after_name'
                elif state == 'after_name':
                    if ch == '=': state = 'before_value'
                    elif ch == '/': state = 'before'
                    elif ch not in ' \t\n\f\r': state = 'name'
                elif state == 'after_value':
                    if ch in ' \t\n\f\r' or ch == '/': state = 'before'
                    else: state = 'name'
                elif ch not in ' \t\n\f\r' and ch != '/':
                    state = 'name'
                cursor += 1
            return -1
        def handle_endtag(self, tag):
            if self.raw is not None:
                if self.raw == tag and tag != 'plaintext': self.raw = None
                return
            if self.svg:
                if tag != self.svg[-1]:
                    self.unsupported_structure('thẻ đóng SVG lệch cây')
                self.svg.pop()
                return
            if not self.templates and (tag in ('svg', 'math') or ':' in tag):
                self.unsupported_structure('thẻ đóng foreign không có thẻ mở')
            if tag == 'template' and self.templates:
                self.templates -= 1
        def handle_startendtag(self, tag, attrs):
            if self.foreign_start(tag, attrs, closed=True):
                return
            # In HTML the slash does not close non-void elements.
            self.handle_starttag(tag, attrs)
            if tag in ('script', 'style') and self.raw is None:
                self.set_cdata_mode(tag)
        @staticmethod
        def normalize(value):
            return value.strip(''.join(chr(i) for i in range(33))).translate({ord('\t'): None, ord('\n'): None, ord('\r'): None})
        def handle_starttag(self, tag, attrs):
            if self.raw is not None: return
            if self.foreign_start(tag, attrs): return
            if tag in ('textarea', 'title', 'xmp', 'iframe', 'noembed', 'noframes', 'noscript', 'plaintext'):
                self.raw = tag
                # HTMLParser otherwise treats <!-- inside RCDATA as a comment
                # and swallows the real closing tag inside that text.
                if tag != 'plaintext': self._set_raw_mode(tag)
                return
            if tag == 'template':
                self.templates += 1
                return
            if self.templates: return
            first = {}
            for key, value in attrs: first.setdefault(key, value)
            line = self.getpos()[0]
            if tag == 'base' and 'href' in first and self.base is None:
                self.base = self.normalize(first['href'] or '')
                if self.base not in ('', '.', './'):
                    normalized = self.base.replace('\\', '/')
                    kind = 'mã từ xa' if re.match(r'^(?:https?:|//)', normalized, re.I) else 'base thay đổi gốc'
                    self.remote.append(f'dòng {line}: {kind}')
            if tag in ('script', 'link'):
                value = first.get('src' if tag == 'script' else 'href')
                if value is None: return
                value = self.normalize(value)
                if tag == 'script' and re.match(r'^(?:https?:|//)', value.replace('\\', '/'), re.I):
                    self.remote.append(f'dòng {line}: mã từ xa')
                self.local.append(value)
    reader = Reader()
    try:
        reader.feed(html)
        reader.close()
        if reader.cdata_elem == 'script' and '<!--' in reader.rawdata:
            reader.unsupported_structure('marker HTML comment trong raw script còn mở')
        if reader.svg:
            reader.unsupported_structure('EOF khi cây SVG còn mở')
    except UnsupportedStructure:
        return [], reader.remote
    return (reader.local if reader.base in (None, '', '.', './') else []), reader.remote


def detect(html: str) -> list[str]:
    from urllib.parse import urlsplit
    lock = load_lock(); values, _ = _html_references(html); found = set()
    for value in values:
        try: parsed = urlsplit(value)
        except ValueError: continue
        if parsed.scheme or parsed.netloc or value.startswith('//'): continue
        path = parsed.path
        if path.startswith('./'): path = path[2:]
        if not path or '/' in path or '\\' in path: continue
        for name, lib in lock['libs'].items():
            if any(m['dest'] == path for m in lib['members']): found.add(name)
    return [name for name in lock['libs'] if name in found]


def assert_no_remote_code(html: str, *, strict: bool = True) -> list[str]:
    violations = _html_references(html)[1]
    if strict and violations: raise ContractError('HTML bị chặn: ' + '; '.join(violations))
    return violations


def stage(names: Iterable[str], project_dir: str | os.PathLike[str], *, required: bool = True,
          keep_existing: bool = False, station: str | os.PathLike[str] | None = None,
          overrides: Mapping[str, str | os.PathLike[str]] | None = None,
          verify_existing: bool = False) -> list[str]:
    from . import contract
    lock = load_lock(); order = resolve(names, lock); mapping = get_overrides() if overrides is None else overrides
    selected = []; seen = set()
    for name in order:
        ms = members(name, lock)
        for m in ms:
            dest = m['dest']; key = dest.casefold()
            if key in seen: raise ContractError(f'Đích thư viện trùng: {dest}')
            seen.add(key); target = os.path.join(project_dir, dest)
            if os.path.lexists(target):
                if not keep_existing: raise ContractError(f'Không ghi đè tệp project: {dest}')
                try: read_verified(target, m['file_sha256'], m['max_bytes'])
                except ContractError as exc:
                    if verify_existing: raise ContractError(f'Tệp project {dest} không khớp khoá runtime') from exc
                    contract.log(f'Cảnh báo: giữ tệp project {dest} khác khoá runtime')
                continue
            source = mapping.get(f'{name}:{dest}') or (mapping.get(name) if len(ms) == 1 else None) or station_path(name, dest, station)
            if not os.path.lexists(source):
                if not required: return []
                raise StationMissing(f'Thiếu thư viện {name}; chạy: video-studio libs fetch {name}')
            selected.append((dest, read_verified(source, m['file_sha256'], m['max_bytes'])))
    if not selected: return []
    _publish_files(os.fspath(project_dir), 'project', '', dict(selected), project=True)
    return [dest for dest, _ in selected]


def stage_detected(project_dir: str | os.PathLike[str], html: str | None = None, *, required: bool = True,
                   keep_existing: bool = False, station: str | os.PathLike[str] | None = None,
                   names: Iterable[str] = (), verify_existing: bool = False) -> list[str]:
    from . import contract
    if html is None:
        try:
            html = _read_bounded(os.path.join(project_dir, 'index.html'), 64 * 1024 * 1024).decode('utf-8-sig')
        except UnicodeDecodeError as exc:
            raise ContractError('index.html không phải UTF-8') from exc
    warnings = assert_no_remote_code(html, strict=not keep_existing)
    for warning in warnings:
        if 'cấu trúc HTML/SVG chưa được hỗ trợ' in warning:
            label = 'cấu trúc HTML/SVG chưa được hỗ trợ'
        else:
            label = 'base thay đổi gốc' if 'base thay đổi gốc' in warning else 'mã từ xa'
        contract.log(f'Cảnh báo {label}: {warning}')
    return stage(list(dict.fromkeys([*names, *detect(html)])), project_dir, required=required, keep_existing=keep_existing, station=station, verify_existing=verify_existing)
