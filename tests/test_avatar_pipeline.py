"""Avatar profile, optimize, LatentSync and SyncNet contracts without GPU, FFmpeg or models."""
import json
import os
import sys
import wave
from pathlib import Path
from types import SimpleNamespace

import pytest

from video_studio import avatar_cmd, contract
from video_studio.avatar import common, latentsync, optimize, profile


@pytest.fixture
def station(tmp_path, monkeypatch):
    root = tmp_path / "station"
    root.mkdir()
    monkeypatch.setattr(common._env, "resolve_station", lambda: (str(root), "test"))
    return root


def _wav(path: Path, seconds=1.0, rate=16000):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\0\0" * int(rate * seconds))
    return path


def _new(station, pid="me-studio", clip=None, **kw):
    args = dict(name="Me", relation="self", consent_quote="Tôi đồng ý dùng mặt mình cho bài giảng",
                scope="bài giảng nội bộ", clip=clip)
    args.update(kw)
    return profile.create(pid, **args)


# ── profile ─────────────────────────────────────────────────────────────────────────────

def test_profile_create_writes_only_inside_station(station):
    clip = station / "idle.mp4"
    clip.write_bytes(b"clip")
    result = _new(station, clip=clip)
    folder = station / "avatars" / "me-studio"
    assert Path(result["path"]) == folder
    data = json.loads((folder / "avatar.json").read_text(encoding="utf-8"))
    assert data["consent"]["relation"] == "self" and data["consent"]["revoked_at"] is None
    assert data["clip"] == {"path": "idle.mp4", "sha256": common.sha256(clip)}
    assert data["engine"]["name"] == "latentsync" and data["voice"]["speed"] == 1.0
    assert all((folder / sub).is_dir() for sub in profile.SUBFOLDERS)


@pytest.mark.parametrize("override", [
    {"relation": "friend"}, {"consent_quote": "ok"}, {"scope": " "}, {"name": ""}, {"crop": "big"},
])
def test_profile_create_requires_consent_record(station, override):
    with pytest.raises(contract.ContractError):
        _new(station, **override)
    assert not (station / "avatars" / "me-studio").exists()


@pytest.mark.parametrize("pid", ["Me", "a", "../x", "me studio"])
def test_profile_id_is_a_plain_slug(station, pid):
    with pytest.raises(contract.ContractError):
        _new(station, pid=pid)


def test_profile_rejects_clip_outside_station(station, tmp_path):
    outside = tmp_path / "outside.mp4"
    outside.write_bytes(b"clip")
    with pytest.raises(contract.ContractError):
        _new(station, clip=outside)


def test_profile_search_filters_and_reports_usability(station):
    clip = station / "idle.mp4"
    clip.write_bytes(b"clip")
    _new(station, "me-studio", clip=clip)
    _new(station, "guest-lan", name="Lan", relation="consented")
    assert profile.search()["count"] == 2
    hits = profile.search("lan")["profiles"]
    assert [h["id"] for h in hits] == ["guest-lan"] and hits[0]["usable"] is False
    assert profile.search("studio")["profiles"][0]["usable"] is True


def test_render_gate_refuses_revoked_missing_or_changed_clip(station):
    clip = station / "idle.mp4"
    clip.write_bytes(b"clip")
    _new(station, clip=clip)
    assert profile.for_render("me-studio")["clip"] == clip
    clip.write_bytes(b"edited")
    with pytest.raises(contract.ContractError, match="changed"):
        profile.for_render("me-studio")
    profile.update("me-studio", clip=clip)
    profile.revoke("me-studio")
    with pytest.raises(contract.ContractError, match="revoked"):
        profile.for_render("me-studio")


def test_render_gate_requires_clip(station):
    _new(station)
    with pytest.raises(contract.ContractError, match="no approved clip"):
        profile.for_render("me-studio")


def test_update_keeps_unset_engine_values_and_records_qa(station):
    _new(station)
    profile.update("me-studio", engine={"guidance": 3.0, "steps": None}, voice="voice-x")
    data = profile.load("me-studio")
    assert data["engine"]["guidance"] == 3.0 and data["engine"]["steps"] == 30
    assert data["voice"]["profile"] == "voice-x"
    entry = profile.record_qa("me-studio", station / "out.mp4", {"confidence": 7.9, "av_offset": 0, "passed": True})
    assert entry["video"] == "out.mp4"
    assert profile.load("me-studio")["qa_history"][-1]["passed"] is True


# ── optimize ────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("value, expected", [
    (None, None), ("720:720:0:180", (720, 720, 0, 180)), ("721:719:3:4", (720, 718, 3, 4)),
])
def test_parse_crop(value, expected):
    assert optimize.parse_crop(value) == expected


@pytest.mark.parametrize("value", ["720x720", "32:32:0:0", "-1:2:3:4", "1:2:3"])
def test_parse_crop_rejects_bad_values(value):
    with pytest.raises(contract.ContractError):
        optimize.parse_crop(value)


@pytest.mark.parametrize("size, expected", [
    ((720, 720), (720, 720)), ((1080, 1920), (720, 1280)), ((1920, 1080), (1280, 720)), ((1440, 1440), (960, 960)),
])
def test_scaled_stays_within_engine_bounds(size, expected):
    w, h = optimize.scaled(*size)
    assert (w, h) == expected and w * h <= optimize.MAX_AREA and max(w, h) <= optimize.MAX_SIDE


def test_restore_mouth_rejects_bad_strength_before_touching_files(station):
    for strength in (0, 1.5, True):
        with pytest.raises(contract.ContractError):
            optimize.restore_mouth(station / "in.mp4", station / "out.mp4", strength=strength)


def test_normalize_refuses_existing_output(station):
    src, out = station / "in.mp4", station / "out.mp4"
    src.write_bytes(b"v")
    out.write_bytes(b"keep")
    with pytest.raises(contract.ContractError):
        optimize.normalize(src, out)
    assert out.read_bytes() == b"keep"


# ── LatentSync ──────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("params", [(0.5, 30, 1), (2.5, 5, 1), (2.5, 30, -1), (True, 30, 1), (2.5, 30.0, 1)])
def test_latentsync_param_contract(params):
    with pytest.raises(contract.ContractError):
        latentsync.check_params(*params)


def test_latentsync_rejects_inputs_outside_station(station, tmp_path):
    with pytest.raises(contract.ContractError):
        latentsync.render(tmp_path / "outside.mp4", station / "a.wav", station / "o.mp4")


def test_latentsync_rejects_long_or_invalid_audio(station):
    src = station / "in.mp4"
    src.write_bytes(b"v")
    _wav(station / "long.wav", seconds=61, rate=8000)
    (station / "bad.wav").write_bytes(b"nope")
    for name in ("long.wav", "bad.wav"):
        with pytest.raises(contract.ContractError):
            latentsync.render(src, station / name, station / "o.mp4")


def test_latentsync_missing_runtime_is_station_missing(station, monkeypatch):
    monkeypatch.setattr(latentsync._env, "runtime_venv_python", lambda key: None)
    src = station / "in.mp4"
    src.write_bytes(b"v")
    _wav(station / "a.wav")
    with pytest.raises(contract.StationMissing):
        latentsync.render(src, station / "a.wav", station / "o.mp4")
    assert latentsync.doctor()["ready"] is False


def _fake_engine(tmp_path, monkeypatch):
    engine = tmp_path / "engine"
    for name in latentsync.CHECKPOINTS:
        (engine / "src" / "checkpoints" / name).parent.mkdir(parents=True, exist_ok=True)
        (engine / "src" / "checkpoints" / name).write_bytes(b"w")
    (engine / "src" / "scripts").mkdir(parents=True)
    (engine / "src" / "scripts" / "inference.py").write_text("")
    (engine / "hf-home" / "hub" / "models--stabilityai--sd-vae-ft-mse").mkdir(parents=True)
    monkeypatch.setattr(latentsync._env, "runtime_venv_python", lambda key: sys.executable)
    monkeypatch.setattr(latentsync._env, "runtime_resource", lambda cat, key: str(engine))
    monkeypatch.setattr(latentsync._env, "musetalk_ffmpeg_tools", lambda: ("ffmpeg", "ffprobe"))
    return engine


def test_latentsync_render_stages_without_spaces_and_moves_result(station, tmp_path, monkeypatch):
    engine = _fake_engine(tmp_path, monkeypatch)
    src = station / "my clip.mp4"
    src.write_bytes(b"video")
    _wav(station / "giọng nói.wav")
    seen = {}

    def fake_run(argv, env, directory, *, total, cwd):
        seen.update(argv=argv, cwd=cwd, env=env, total=total)
        out = Path(argv[argv.index("--video_out_path") + 1])
        out.write_bytes(b"result")
        return SimpleNamespace(code=0, timeout=None, spawn_failed=False, stdout="", stderr="", elapsed_seconds=1.0)

    monkeypatch.setattr(latentsync.worker_process, "run", fake_run)
    out = station / "out.mp4"
    result = latentsync.render(src, station / "giọng nói.wav", out, guidance=2.5, steps=30, seed=7)
    assert out.read_bytes() == b"result"
    assert seen["cwd"] == engine / "src"
    staged = [a for a in seen["argv"] if a.startswith(str(engine))]
    assert staged and not any(" " in a for a in staged)
    assert seen["env"]["TORCH_HOME"].endswith("torch-home") and "--seed" in seen["argv"]
    assert result["engine"] == "latentsync" and result["seed"] == 7
    assert not list((engine / "work").iterdir())


def test_latentsync_engine_failure_hides_private_paths(station, tmp_path, monkeypatch):
    _fake_engine(tmp_path, monkeypatch)
    src = station / "in.mp4"
    src.write_bytes(b"video")
    _wav(station / "a.wav")
    monkeypatch.setattr(latentsync.worker_process, "run", lambda *a, **k: SimpleNamespace(
        code=1, timeout=None, spawn_failed=False, stdout="", stderr=f"boom at {station}", elapsed_seconds=1.0))
    with pytest.raises(contract.EngineError) as err:
        latentsync.render(src, station / "a.wav", station / "o.mp4")
    assert str(station) not in str(err.value)
    assert not (station / "o.mp4").exists()


@pytest.mark.parametrize("text, passed", [
    ("Input video: x\nSyncNet confidence: 7.94\nAV offset: 0", True),
    ("SyncNet confidence: 7.94\nAV offset: 1", False),
    ("SyncNet confidence: 6.99\nAV offset: 0", False),
])
def test_parse_sync_verdict(text, passed):
    assert latentsync.parse_sync(text)["passed"] is passed


def test_parse_sync_without_score_is_engine_error():
    with pytest.raises(contract.EngineError):
        latentsync.parse_sync("Face not detected")


def test_staging_refuses_paths_with_spaces(tmp_path):
    with pytest.raises(contract.StationMissing):
        with common.Staging(tmp_path / "has space"):
            pass


# ── CLI ─────────────────────────────────────────────────────────────────────────────────

def test_cli_profile_round_trip(station, capsys):
    rc = avatar_cmd.main(["profile", "new", "me-studio", "--name", "Me", "--relation", "self",
                          "--consent-quote", "Tôi đồng ý dùng mặt mình", "--scope", "bài giảng", "--json"])
    assert rc == 0
    rc = avatar_cmd.main(["profile", "list", "me", "--json"])
    payload = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert rc == 0 and payload["count"] == 1


def test_cli_profile_new_without_consent_is_contract_error(station):
    assert avatar_cmd.main(["profile", "new", "me-studio", "--name", "Me", "--relation", "self",
                            "--scope", "x"]) == contract.CONTRACT_ERROR


def test_cli_render_defaults_to_latentsync(station, monkeypatch):
    calls = {}
    monkeypatch.setattr(latentsync, "render", lambda *a, **k: calls.setdefault("ls", (a, k)) and {"engine": "latentsync"})
    rc = avatar_cmd.main(["render", "--source", str(station / "s.mp4"), "--audio", str(station / "a.wav"),
                          "--out", str(station / "o.mp4")])
    assert rc == 0 and calls["ls"][1] == {"guidance": 2.5, "steps": 30, "seed": 1247}


def test_cli_render_bbox_shift_only_with_musetalk(station):
    assert avatar_cmd.main(["render", "--source", "s.mp4", "--audio", "a.wav", "--out", "o.mp4",
                            "--bbox-shift", "-10"]) == contract.CONTRACT_ERROR


def test_cli_render_with_profile_uses_profile_clip_and_settings(station, monkeypatch):
    clip = station / "idle.mp4"
    clip.write_bytes(b"clip")
    _new(station, clip=clip)
    profile.update("me-studio", engine={"name": "musetalk", "bbox_shift": -15})
    seen = {}
    from video_studio.musetalk import runner
    monkeypatch.setattr(runner, "run", lambda s, a, o, shift: seen.update(source=s, shift=shift) or {})
    rc = avatar_cmd.main(["render", "--profile", "me-studio", "--audio", str(station / "a.wav"),
                          "--out", str(station / "o.mp4")])
    assert rc == 0 and seen == {"source": clip, "shift": -15}


def test_cli_render_revoked_profile_is_refused(station):
    clip = station / "idle.mp4"
    clip.write_bytes(b"clip")
    _new(station, clip=clip)
    profile.revoke("me-studio")
    assert avatar_cmd.main(["render", "--profile", "me-studio", "--audio", "a.wav",
                            "--out", "o.mp4"]) == contract.CONTRACT_ERROR


def test_cli_doctor_reports_station_missing_when_no_engine_ready(monkeypatch):
    from video_studio.musetalk import runner
    monkeypatch.setattr(latentsync, "doctor", lambda: {"ready": False, "reason": "x"})
    monkeypatch.setattr(runner, "doctor", lambda: {"ready": False, "reason": "y"})
    assert avatar_cmd.main(["doctor"]) == contract.STATION_MISSING
    monkeypatch.setattr(runner, "doctor", lambda: {"ready": True})
    assert avatar_cmd.main(["doctor"]) == contract.OK
