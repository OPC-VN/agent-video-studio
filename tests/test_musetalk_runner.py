from pathlib import Path

import pytest

from video_studio import contract


def test_child_environment_preserves_windows_username_without_inheriting_unrelated_values(monkeypatch):
    from video_studio import _env

    monkeypatch.setenv("USERNAME", "test-user")
    monkeypatch.setenv("MUSE_TEST_UNRELATED", "not-copied")
    env = _env.musetalk_child_env()
    assert env["USERNAME"] == "test-user"
    assert "MUSE_TEST_UNRELATED" not in env


def test_runner_rejects_media_outside_selected_station(tmp_path, monkeypatch):
    from video_studio.musetalk import runner

    station = tmp_path / "station"
    station.mkdir()
    monkeypatch.setattr(runner._env, "resolve_station", lambda: (str(station), "test"))
    with pytest.raises(contract.ContractError):
        runner.run(tmp_path / "outside.mp4", station / "voice.wav", station / "out.mp4")


def test_runner_does_not_overwrite_output(tmp_path, monkeypatch):
    from video_studio.musetalk import runner

    monkeypatch.setattr(runner._env, "resolve_station", lambda: (str(tmp_path), "test"))
    source, audio, output = (tmp_path / n for n in ("source.mp4", "audio.wav", "out.mp4"))
    for path in (source, audio, output):
        path.write_bytes(b"fixture")
    with pytest.raises(contract.ContractError):
        runner.run(source, audio, output)
    assert output.read_bytes() == b"fixture"


def test_runner_rejects_invalid_wav_before_starting_worker(tmp_path, monkeypatch):
    from video_studio.musetalk import runner

    monkeypatch.setattr(runner._env, "resolve_station", lambda: (str(tmp_path), "test"))
    source, audio = tmp_path / "source.mp4", tmp_path / "audio.wav"
    source.write_bytes(b"fixture")
    audio.write_bytes(b"not wave")
    with pytest.raises(contract.ContractError):
        runner.run(source, audio, tmp_path / "out.mp4")


def test_image_source_requires_matching_magic(tmp_path):
    from video_studio.musetalk import source

    image = tmp_path / "portrait.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"fixture")
    assert source.kind(image) == "png"
    image.write_bytes(b"not a png")
    with pytest.raises(ValueError):
        source.kind(image)
