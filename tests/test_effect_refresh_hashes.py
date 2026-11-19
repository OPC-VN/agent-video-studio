import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest


@pytest.mark.skipif(os.name != 'nt', reason='refresh uses native Windows filesystem primitives')
def test_refresh_writes_candidate_without_replacing_existing(tmp_path, monkeypatch):
    scripts = Path(__file__).resolve().parents[1] / 'scripts'
    monkeypatch.syspath_prepend(str(scripts))
    spec = importlib.util.spec_from_file_location('refresh_effect_hashes_test', scripts / 'refresh_effect_distribution_hashes.py')
    refresh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(refresh)
    monkeypatch.setattr(refresh, 'ROOT', tmp_path)
    (tmp_path / 'scripts').mkdir()
    (tmp_path / 'README.md').write_bytes(b'updated')
    manifest = {'schema': 'effect-distribution-manifest/1', 'files': {'README.md': 'old'}, 'resources': []}
    original = json.dumps(manifest).encode()
    (tmp_path / refresh.MANIFEST).write_bytes(original)

    assert refresh.main() == 0
    candidate = tmp_path / 'scripts/effect-distribution-manifest.candidate.json'
    result = json.loads(candidate.read_text(encoding='utf-8'))
    assert result['files'] == {'README.md': hashlib.sha256(b'updated').hexdigest()}
    assert (tmp_path / refresh.MANIFEST).read_bytes() == original
    before = candidate.read_bytes()
    with pytest.raises(OSError):
        refresh.main()
    assert candidate.read_bytes() == before
