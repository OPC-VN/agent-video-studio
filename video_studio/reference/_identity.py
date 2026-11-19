"""Reject mixing measurements from different source byte snapshots."""
import re

from ..contract import ContractError

_SHA256 = re.compile(r'[0-9a-f]{64}')


def require_same_source(snapshot_sha, shots_source, audio_source, provenance_sha=None):
    """Require measurements to share the current snapshot; optional provenance is authoritative when present."""
    def digest(value):
        if not isinstance(value, str) or not _SHA256.fullmatch(value):
            raise ContractError('SHA-256 nguồn không hợp lệ')
        return value
    expected = digest(snapshot_sha)
    sources = (shots_source,) if audio_source is None else (shots_source, audio_source)
    for source in sources:
        if not isinstance(source, dict) or digest(source.get('sha256')) != expected:
            raise ContractError('bằng chứng nguồn không khớp video')
    if provenance_sha is not None and digest(provenance_sha) != expected:
        raise ContractError('SHA-256 hồ sơ nguồn không khớp video')
    return expected
