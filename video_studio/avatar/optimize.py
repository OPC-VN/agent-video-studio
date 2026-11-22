"""`avatar optimize`: normalize an idle clip before lip-sync, or restore the mouth after it."""
from pathlib import Path
import json
import re
import shutil
import subprocess

from video_studio.contract import ContractError, EngineError
from video_studio.musetalk import process as worker_process
from . import common, latentsync

MAX_SIDE = 1280
MAX_AREA = 1280 * 720
_CROP = re.compile(r"^(\d+):(\d+):(\d+):(\d+)$")


def parse_crop(value):
    """`W:H:X:Y` in source pixels -> tuple of even ints, or None."""
    if value in (None, ""):
        return None
    match = _CROP.match(str(value))
    if not match:
        raise ContractError("crop must be W:H:X:Y in pixels, for example 720:720:0:180.")
    w, h, x, y = (int(v) for v in match.groups())
    if w < 64 or h < 64:
        raise ContractError("crop width and height must be at least 64 pixels.")
    return w - w % 2, h - h % 2, x, y


def scaled(w, h):
    """Largest even size within the MuseTalk/LatentSync bounds that keeps the aspect ratio."""
    factor = min(1.0, MAX_SIDE / max(w, h), (MAX_AREA / (w * h)) ** 0.5)
    return max(2, int(w * factor) // 2 * 2), max(2, int(h * factor) // 2 * 2)


def _probe(ffprobe, video: Path):
    argv = [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height:format=duration", "-of", "json", str(video)]
    try:
        data = json.loads(subprocess.run(argv, capture_output=True, text=True, timeout=30, check=True).stdout)
        stream = data["streams"][0]
        return int(stream["width"]), int(stream["height"]), float(data["format"]["duration"])
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, IndexError) as exc:
        raise ContractError("The source video could not be read by FFprobe.") from exc


def normalize(source, output, crop=None, max_seconds=30.0) -> dict:
    """Silent, 25 fps, H.264, optional crop, scaled within 1280x720 area."""
    root = common.station()
    source, output = common.existing_video(common.inside(source, root)), common.inside(output, root)
    common.new_output(output)
    box = parse_crop(crop)
    ffmpeg, ffprobe = latentsync.tools()
    width, height, duration = _probe(ffprobe, source)
    if box and (box[0] + box[2] > width or box[1] + box[3] > height):
        raise ContractError(f"crop falls outside the {width}x{height} source.")
    cw, ch = (box[0], box[1]) if box else (width, height)
    ow, oh = scaled(cw, ch)
    filters = ["fps=25"] + ([f"crop={box[0]}:{box[1]}:{box[2]}:{box[3]}"] if box else []) \
        + [f"scale={ow}:{oh}:flags=lanczos", "setsar=1"]
    argv = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(source), "-an",
            "-t", f"{max_seconds:g}", "-vf", ",".join(filters), "-c:v", "libx264", "-crf", "16",
            "-pix_fmt", "yuv420p", str(output)]
    try:
        subprocess.run(argv, capture_output=True, timeout=600, check=True)
    except subprocess.CalledProcessError as exc:
        output.unlink(missing_ok=True)
        raise EngineError("FFmpeg could not normalize the clip.") from exc
    return {"task": "normalize", "size": f"{ow}x{oh}", "fps": 25,
            "seconds": round(min(duration, max_seconds), 2), "crop": crop or None}


def restore_mouth(video, output, strength=0.85) -> dict:
    """GFPGAN on the mouth only, then copy the original audio track back."""
    if isinstance(strength, bool) or not isinstance(strength, (int, float)) or not 0 < strength <= 1:
        raise ContractError("strength must be greater than 0 and at most 1.")
    root = common.station()
    video, output = common.existing_video(common.inside(video, root)), common.inside(output, root)
    common.new_output(output)
    python, engine = latentsync.resources()
    gfpgan = latentsync.gfpgan_dir()
    ffmpeg, _ = latentsync.tools()
    worker = Path(__file__).with_name("_mouth_worker.py")
    with common.Staging(engine / "work") as work:
        staged, silent = work / "in.mp4", work / "silent.mp4"
        shutil.copyfile(video, staged)
        # Run a copy from the scratch folder: next to this file, `profile.py` would shadow the stdlib module.
        script = work / worker.name
        shutil.copyfile(worker, script)
        argv = [python, str(script), str(staged), str(silent), str(strength),
                str(gfpgan / "gfpgan" / "weights" / "GFPGANv1.4.pth")]
        completed = worker_process.run(argv, latentsync.child_env(engine), work, total=3600, cwd=gfpgan)
        latentsync._fail(completed, "Mouth restore", (video, output, root, engine))
        try:
            stats = json.loads(completed.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError) as exc:
            raise EngineError("Mouth restore returned an invalid result.") from exc
        mux = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(silent), "-i", str(staged),
               "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-shortest", str(output)]
        try:
            subprocess.run(mux, capture_output=True, timeout=600, check=True)
        except subprocess.CalledProcessError as exc:
            output.unlink(missing_ok=True)
            raise EngineError("FFmpeg could not mux the restored video.") from exc
    return {"task": "mouth", **stats}
