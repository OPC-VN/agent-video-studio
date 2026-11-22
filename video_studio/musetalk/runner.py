"""Opt-in, local-only MuseTalk runner."""
from pathlib import Path
import contextlib
import io
import json
import os
import stat
import subprocess
import wave

from video_studio import _env
from video_studio.contract import ContractError, EngineError, StationMissing
from . import process as worker_process
from . import source as source_format

RESOURCE = "musetalk-1-5"


def _check_path(path: Path, station: Path) -> Path:
    path = Path(os.path.abspath(path))
    if not path.is_relative_to(station):
        raise ContractError("Avatar inputs and output must be inside the selected video station.")
    for entry in (*reversed(path.parents), path):
        try:
            info = entry.lstat()
        except FileNotFoundError:
            continue
        attrs = getattr(info, "st_file_attributes", 0)
        if stat.S_ISLNK(info.st_mode) or attrs & (
            getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
            | getattr(stat, "FILE_ATTRIBUTE_OFFLINE", 0)
        ):
            raise ContractError("Avatar paths cannot use links, junctions or offline files.")
    return path


BBOX_SHIFT_LIMIT = 30


def run(source: Path, audio: Path, output: Path, bbox_shift: int = 0):
    if isinstance(bbox_shift, bool) or not isinstance(bbox_shift, int) or abs(bbox_shift) > BBOX_SHIFT_LIMIT:
        raise ContractError(f"bbox_shift must be an integer from -{BBOX_SHIFT_LIMIT} to {BBOX_SHIFT_LIMIT}.")
    station_value, _ = _env.resolve_station()
    if not station_value or not Path(station_value).is_dir():
        raise StationMissing("Select an existing video station before running the avatar engine.")
    station = Path(os.path.abspath(station_value))
    source, audio, output = (_check_path(Path(p), station) for p in (source, audio, output))
    if output.exists():
        raise ContractError("The avatar output already exists; select a new output path.")
    if not source.is_file() or not audio.is_file():
        raise ContractError("Avatar source video and audio must exist as regular local files.")
    if not output.parent.is_dir() or output.suffix.lower() != ".mp4":
        raise ContractError("Avatar output must be an MP4 in an existing directory.")
    try:
        source_kind = source_format.kind(source)
    except (OSError, ValueError) as exc:
        raise ContractError("The source must be a local MP4, MOV, PNG or JPEG.") from exc
    if audio.suffix.lower() != ".wav":
        raise ContractError("The audio must be WAV.")
    try:
        with wave.open(str(audio), "rb") as wav:
            if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getcomptype()) != (1, 2, 16000, "NONE"):
                raise ContractError("Avatar audio must be mono 16 kHz PCM16 WAV.")
            if not 0 < wav.getnframes() <= 30 * 16000:
                raise ContractError("Avatar audio must be between zero and 30 seconds.")
            samples = wav.getnframes()
            if len(wav.readframes(samples)) != samples * 2:
                raise ContractError("Avatar audio is truncated.")
            expected_frames = samples * 25 // 16000
            if expected_frames == 0:
                raise ContractError("Avatar audio is too short to produce a frame.")
    except (wave.Error, EOFError, OSError) as exc:
        raise ContractError("Avatar audio is not a valid PCM WAV.") from exc
    python, engine, ffmpeg, ffprobe = _resources()
    _probe_source(source, ffprobe, source_kind)
    _verify_models(engine)
    worker = Path(__file__).with_name("_worker.py")
    command = [python, "-I", "-B", str(worker), str(source), str(audio), str(output),
               str(engine / "models"), ffmpeg, ffprobe, str(expected_frames), source_kind, str(bbox_shift)]
    completed = worker_process.run(command, _env.musetalk_child_env(), output.parent)
    if completed.timeout:
        label = "inactivity" if completed.timeout == "idle" else "total duration"
        raise EngineError(f"The avatar worker reached its {label} deadline after {completed.elapsed_seconds:.1f}s.")
    if completed.spawn_failed:
        raise EngineError("The avatar worker could not start.")
    if completed.code:
        reason = next((line for line in reversed(completed.stderr.splitlines())
                       if line.startswith("Avatar engine failed:")), "Avatar engine failed.")
        for private in (source, audio, output, station, engine):
            reason = reason.replace(str(private), "[local path]")
        raise EngineError(f"{reason[:500]} (worker exit {completed.code})")
    try:
        result = json.loads(completed.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError) as exc:
        raise EngineError("The avatar worker returned an invalid result.") from exc
    if not output.is_file() or output.stat().st_size == 0:
        raise EngineError("The avatar worker did not produce a video.")
    return result


def doctor() -> dict:
    try:
        python, engine, _, _ = _resources()
        _verify_models(engine)
        probe = subprocess.run([python, "-I", "-B", "-c",
                                "from transformers import WhisperModel; import torch,cv2,onnxruntime,soundfile,diffusers; "
                                "assert torch.cuda.is_available(); torch.ones(1, device='cuda').sum().item()"],
                               env=_env.musetalk_child_env(), capture_output=True, timeout=90)
        if probe.returncode:
            raise StationMissing("MuseTalk requires a working CUDA-enabled PyTorch installation.")
    except (OSError, subprocess.TimeoutExpired):
        return {"ready": False, "reason": "MuseTalk CUDA probe did not finish."}
    except (StationMissing, EngineError) as exc:
        return {"ready": False, "reason": str(exc)}
    return {"ready": True}


def _resources():
    python = _env.runtime_venv_python(RESOURCE)
    engine_value = _env.runtime_resource("engines", RESOURCE)
    ffmpeg, ffprobe = _env.musetalk_ffmpeg_tools()
    if not python or not engine_value or not ffmpeg or not ffprobe:
        raise StationMissing("MuseTalk runtime or FFmpeg/FFprobe is missing.")
    engine = Path(engine_value)
    if not engine.is_dir():
        raise StationMissing("MuseTalk model directory is missing.")
    from . import model_store
    venv = Path(python).parent.parent
    try:
        model_store.regular_path(Path(python))
        receipt = venv / ".opcos-resource.json"
        model_store.regular_path(receipt)
        data = json.loads(receipt.read_text(encoding="utf-8"))
        if any(data.get(key) != value for key, value in {
            "schema": "opcos-resource/1", "category": "venvs", "repoKey": "agent-video-studio",
            "resourceKey": RESOURCE, "status": "complete",
        }.items()):
            raise ValueError("invalid receipt")
    except (OSError, ValueError, TypeError) as exc:
        raise StationMissing("MuseTalk venv receipt is missing or invalid.") from exc
    return python, engine, ffmpeg, ffprobe


def _verify_models(engine: Path):
    from . import model_store
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            model_store.install(engine, True)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise StationMissing("MuseTalk model integrity verification failed.") from exc


def _probe_source(source: Path, ffprobe: str, source_kind: str):
    decoder = (["-f", "mov", "-enable_drefs", "0"] if source_kind == "mov" else
               ["-f", "image2", "-pattern_type", "none", "-c:v", source_kind])
    argv = [ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe", *decoder,
            "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(source)]
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=30, check=True,
                                env=_env.musetalk_child_env())
        data = json.loads(result.stdout)
        stream = data["streams"][0]
        width, height = int(stream["width"]), int(stream["height"])
        dimensions_ok = 0 < width <= 1280 and 0 < height <= 1280 and width * height <= 1280 * 720
        duration_ok = source_kind != "mov" or 0 < float(data["format"]["duration"]) <= 30
        if not (dimensions_ok and duration_ok):
            raise ValueError("outside bounds")
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, IndexError, TypeError) as exc:
        raise ContractError("Source exceeds the supported image dimensions or 30-second video limit.") from exc
