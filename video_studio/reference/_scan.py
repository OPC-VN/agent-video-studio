"""Bounded, descriptor-anchored data reads for reference analysis.

This module does not publish files or make a claim about remote filesystem mounts.
"""
import json
import math
import os
import re
from pathlib import PurePosixPath

from ..contract import ContractError

MAX_JSON_BYTES = 20 * 1024 * 1024
MAX_EVIDENCE_BYTES = 32 * 1024 * 1024


def _read(root, relative, limit):
    if os.name == 'nt':
        from ..effect_library import _native_windows as backend
    elif os.name == 'posix':
        from ..effect_library import _posix_fs as backend
    else:
        raise ContractError('nền tảng chưa hỗ trợ đọc an toàn')
    try:
        return backend.read_repo_file(os.path.abspath(root), relative, limit=limit)
    except (OSError, ValueError, TypeError, ContractError) as exc:
        raise ContractError('không đọc được dữ liệu cục bộ an toàn') from exc


def read_json_strict(path, max_bytes=MAX_JSON_BYTES):
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or not 0 < max_bytes <= MAX_JSON_BYTES:
        raise ContractError('trần JSON không hợp lệ')
    try:
        raw = os.fsdecode(path)
        if not raw or '\x00' in raw or raw.startswith(('//', '\\\\')) or '..' in raw.replace('\\', '/').split('/'):
            raise ContractError('đường JSON không an toàn')
        root, name = os.path.split(os.path.abspath(raw))
        data = _read(root, name, max_bytes)
        def pairs(items):
            result = {}
            for key, value in items:
                if key in result:
                    raise ValueError('duplicate key')
                result[key] = value
            return result
        def finite(value):
            number = float(value)
            if not math.isfinite(number):
                raise ValueError('non-finite number')
            return number
        def constant(_):
            raise ValueError('non-finite constant')
        return json.loads(data.decode('utf8'), object_pairs_hook=pairs, parse_float=finite, parse_constant=constant)
    except (UnicodeDecodeError, ValueError, TypeError, RecursionError) as exc:
        raise ContractError('JSON không hợp lệ') from exc


def validate_ref(project, ref):
    """Return None only when an allowed anchored evidence file can be read."""
    if not isinstance(ref, str) or len(ref) > 1024 or any(ord(ch) < 32 or ord(ch) == 127 for ch in ref):
        return 'tham chiếu không hợp lệ'
    kind, separator, rest = ref.partition(':')
    if not separator or kind not in {'frame', 'tile', 'measure', 'cue'}:
        return 'loại tham chiếu không hợp lệ'
    path, marker, anchor = rest.partition('#')
    if marker and (not anchor or '#' in anchor):
        return 'neo tham chiếu không hợp lệ'
    if not path or '\\' in path or path.startswith('/') or re.match(r'^[A-Za-z]:', path):
        return 'đường tham chiếu không hợp lệ'
    parts = PurePosixPath(path).parts
    if not parts or any(part in ('', '.', '..') for part in path.split('/')):
        return 'đường tham chiếu không hợp lệ'
    required = 'transcripts' if kind == 'cue' else 'evidence'
    if len(parts) < 2 or parts[0] != required:
        return 'tham chiếu sai thư mục'
    try:
        _read(project, path, MAX_EVIDENCE_BYTES)
    except (ContractError, OSError, ValueError):
        return 'không đọc được tham chiếu an toàn'
    return None
