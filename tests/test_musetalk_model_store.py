"""Regression tests for the MuseTalk runtime model gate."""

import hashlib
import json

import pytest

from video_studio.musetalk import model_store


def test_model_lock_has_unique_exact_artifacts():
    files, lock_sha = model_store.read_lock()
    assert len(lock_sha) == 64
    assert any(item.dest == "musetalkV15/unet.pth" for item in files)
    assert len({item.dest.casefold() for item in files}) == len(files)
    assert all(item.url.startswith("https://") and len(item.digest) == 64 for item in files)


@pytest.mark.parametrize("path", ["../model.bin", "whisper/COM1.bin", "whisper/config.json."])
def test_model_paths_reject_windows_aliases_and_traversal(path):
    with pytest.raises(ValueError, match="relative path"):
        model_store.safe_relative(path)


def test_readiness_requires_exact_model_bytes(tmp_path, monkeypatch):
    engine = tmp_path / "engines" / "agent-video-studio" / "musetalk-1-5"
    models = engine / "models"
    models.mkdir(parents=True)
    receipt = {
        "schema": "opcos-resource/1",
        "category": "engines",
        "repoKey": "agent-video-studio",
        "resourceKey": "musetalk-1-5",
        "installed_by": "agent-video-studio",
        "status": "complete",
    }
    (engine / ".opcos-resource.json").write_text(json.dumps(receipt), encoding="utf-8")

    good_bytes = b"expected model"
    sha = hashlib.sha256(good_bytes).hexdigest()
    item = model_store.Artifact("https://huggingface.co/test", "model.bin", len(good_bytes), sha)
    monkeypatch.setattr(model_store, "read_lock", lambda: ([item], sha))
    model = models / item.dest
    marker = models / ".musetalk-ready.json"
    model.write_bytes(b"replaced bytes")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        model_store.install(engine, verify_only=False)
    assert not marker.exists()

    model.write_bytes(good_bytes)
    model_store.install(engine, verify_only=False)
    model_store.install(engine, verify_only=True)
    assert marker.is_file()

    model.write_bytes(b"replaced bytes")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        model_store.install(engine, verify_only=True)
