"""LatentSync 1.5 lip-sync and SyncNet scoring through the local engine (docs/LATENTSYNC.md)."""
from pathlib import Path
import re
import shutil
import subprocess

from video_studio import _env
from video_studio.contract import ContractError, EngineError, StationMissing
from video_studio.musetalk import process as worker_process
from . import common

RESOURCE = "latentsync-1-5"
GFPGAN_RESOURCE = "gfpgan"
CHECKPOINTS = ("latentsync_unet.pt", "whisper/tiny.pt", "auxiliary/syncnet_v2.model", "auxiliary/sfd_face.pth")
GFPGAN_WEIGHTS = ("GFPGANv1.4.pth", "detection_Resnet50_Final.pth", "parsing_parsenet.pth")
AUDIO_LIMIT_SECONDS = 60
GUIDANCE_RANGE = (1.0, 4.0)
STEPS_RANGE = (10, 60)
SYNC_MIN_CONFIDENCE = 7.0
SYNC_MAX_OFFSET = 0


def resources():
    """-> (python, engine dir). Raises StationMissing when anything the engine needs is absent."""
    python = _env.runtime_venv_python(RESOURCE)
    engine_value = _env.runtime_resource("engines", RESOURCE)
    if not python or not engine_value:
        raise StationMissing("LatentSync runtime is missing. See docs/LATENTSYNC.md.")
    engine = Path(engine_value)
    src = engine / "src"
    missing = [name for name in CHECKPOINTS if not (src / "checkpoints" / name).is_file()]
    if not (src / "scripts" / "inference.py").is_file() or missing:
        raise StationMissing(f"LatentSync source or checkpoints are missing: {', '.join(missing) or 'src'}.")
    if not any((engine / "hf-home" / "hub").glob("models--stabilityai--sd-vae-ft-mse")):
        raise StationMissing("LatentSync VAE cache is missing; run one online inference as in docs/LATENTSYNC.md.")
    return python, engine


def gfpgan_dir() -> Path:
    value = _env.runtime_resource("engines", GFPGAN_RESOURCE)
    weights = Path(value) / "gfpgan" / "weights" if value else None
    if not weights or any(not (weights / name).is_file() for name in GFPGAN_WEIGHTS):
        raise StationMissing("GFPGAN weights are missing. See docs/LATENTSYNC.md.")
    return Path(value)


def child_env(engine: Path) -> dict:
    env = _env.musetalk_child_env()
    home = engine / "home"  # keeps any "~" cache of the engine away from the user's profile
    home.mkdir(exist_ok=True)
    env.update({"TORCH_HOME": str(engine / "torch-home"), "HF_HOME": str(engine / "hf-home"),
                "PYTHONUTF8": "1", "HOME": str(home), "USERPROFILE": str(home)})
    return env


def tools():
    ffmpeg, ffprobe = _env.musetalk_ffmpeg_tools()
    if not ffmpeg or not ffprobe:
        raise StationMissing("FFmpeg/FFprobe is missing.")
    return ffmpeg, ffprobe


def doctor() -> dict:
    try:
        python, engine = resources()
        tools()
        probe = subprocess.run([python, "-c", "import torch, face_alignment; assert torch.cuda.is_available()"],
                               env=child_env(engine), capture_output=True, timeout=120)
        if probe.returncode:
            return {"ready": False, "reason": "LatentSync needs a working CUDA-enabled PyTorch."}
    except (OSError, subprocess.TimeoutExpired):
        return {"ready": False, "reason": "LatentSync CUDA probe did not finish."}
    except StationMissing as exc:
        return {"ready": False, "reason": str(exc)}
    try:
        gfpgan_dir()
        restore = True
    except StationMissing:
        restore = False
    return {"ready": True, "mouth_restore": restore}


def check_params(guidance, steps, seed):
    if isinstance(guidance, bool) or not isinstance(guidance, (int, float)) \
            or not GUIDANCE_RANGE[0] <= guidance <= GUIDANCE_RANGE[1]:
        raise ContractError(f"guidance must be from {GUIDANCE_RANGE[0]} to {GUIDANCE_RANGE[1]}.")
    if isinstance(steps, bool) or not isinstance(steps, int) or not STEPS_RANGE[0] <= steps <= STEPS_RANGE[1]:
        raise ContractError(f"steps must be an integer from {STEPS_RANGE[0]} to {STEPS_RANGE[1]}.")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ContractError("seed must be a non-negative integer.")


def _fail(completed, label, privates):
    if completed.timeout:
        kind = "inactivity" if completed.timeout == "idle" else "total duration"
        raise EngineError(f"{label} reached its {kind} deadline after {completed.elapsed_seconds:.1f}s.")
    if completed.spawn_failed:
        raise EngineError(f"{label} could not start.")
    if completed.code:
        tail = (completed.stderr.strip().splitlines() or [""])[-1]
        for private in privates:
            tail = tail.replace(str(private), "[local path]")
        raise EngineError(f"{label} failed (exit {completed.code}): {tail[:400]}")


def render(source, audio, output, guidance=2.5, steps=30, seed=1247) -> dict:
    check_params(guidance, steps, seed)
    root = common.station()
    source, audio, output = (common.inside(p, root) for p in (source, audio, output))
    common.existing_video(source)
    seconds = common.wav_seconds(audio, AUDIO_LIMIT_SECONDS)
    common.new_output(output)
    python, engine = resources()
    tools()
    src = engine / "src"
    with common.Staging(engine / "work") as work:
        staged_video, staged_audio, staged_out = work / f"in{source.suffix.lower()}", work / "in.wav", work / "out.mp4"
        shutil.copyfile(source, staged_video)
        shutil.copyfile(audio, staged_audio)
        argv = [python, "-m", "scripts.inference", "--unet_config_path", "configs/unet/stage2.yaml",
                "--inference_ckpt_path", "checkpoints/latentsync_unet.pt", "--inference_steps", str(steps),
                "--guidance_scale", str(guidance), "--seed", str(seed), "--video_path", str(staged_video),
                "--audio_path", str(staged_audio), "--video_out_path", str(staged_out)]
        total = max(worker_process.TOTAL_SECONDS, int(seconds * 150) + 600)
        completed = worker_process.run(argv, child_env(engine), work, total=total, cwd=src)
        _fail(completed, "LatentSync", (source, audio, output, root, engine))
        if not staged_out.is_file() or staged_out.stat().st_size == 0:
            raise EngineError("LatentSync did not produce a video.")
        shutil.move(str(staged_out), output)
    return {"engine": "latentsync", "guidance": guidance, "steps": steps, "seed": seed,
            "audio_seconds": round(seconds, 2), "elapsed_seconds": round(completed.elapsed_seconds, 1)}


_CONFIDENCE = re.compile(r"SyncNet confidence:\s*(-?\d+(?:\.\d+)?)")
_OFFSET = re.compile(r"AV offset:\s*(-?\d+)")


def parse_sync(text: str) -> dict:
    confidence, offset = _CONFIDENCE.findall(text), _OFFSET.findall(text)
    if not confidence or not offset:
        raise EngineError("SyncNet returned no score (no face tracked for at least 2 seconds?).")
    conf, off = float(confidence[-1]), int(offset[-1])
    passed = abs(off) <= SYNC_MAX_OFFSET and conf >= SYNC_MIN_CONFIDENCE
    return {"confidence": conf, "av_offset": off, "passed": passed,
            "threshold": {"confidence": SYNC_MIN_CONFIDENCE, "av_offset": SYNC_MAX_OFFSET}}


def syncnet(video) -> dict:
    root = common.station()
    video = common.existing_video(common.inside(video, root))
    python, engine = resources()
    tools()
    src = engine / "src"
    with common.Staging(engine / "work") as work:
        staged = work / "qa.mp4"
        shutil.copyfile(video, staged)
        shutil.rmtree(src / "detect_results", ignore_errors=True)
        argv = [python, "-m", "eval.eval_sync_conf", "--video_path", str(staged), "--temp_dir", str(work / "tmp")]
        try:
            completed = worker_process.run(argv, child_env(engine), work, total=1800, cwd=src)
        finally:
            shutil.rmtree(src / "detect_results", ignore_errors=True)
        _fail(completed, "SyncNet", (video, root, engine))
        return parse_sync(completed.stdout + "\n" + completed.stderr)
