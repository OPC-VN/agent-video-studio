"""Shared checks for avatar commands: station, paths, media and staging."""
from pathlib import Path
import hashlib
import os
import shutil
import tempfile
import wave

from video_studio import _env
from video_studio.contract import ContractError, StationMissing
from video_studio.musetalk.runner import _check_path

VIDEO_SUFFIXES = (".mp4", ".mov")


def station() -> Path:
    value, _ = _env.resolve_station()
    if not value or not Path(value).is_dir():
        raise StationMissing("Select an existing video station before running avatar commands.")
    return Path(os.path.abspath(value))


def inside(path, root: Path) -> Path:
    """Absolute path inside the station, without links, junctions or offline files."""
    return _check_path(Path(path), root)


def new_output(path: Path, suffix=".mp4") -> Path:
    if path.exists():
        raise ContractError("The output already exists; select a new output path.")
    if not path.parent.is_dir() or path.suffix.lower() != suffix:
        raise ContractError(f"The output must be a new {suffix.upper().lstrip('.')} in an existing directory.")
    return path


def existing_video(path: Path) -> Path:
    if not path.is_file() or path.suffix.lower() not in VIDEO_SUFFIXES:
        raise ContractError("The video must be an existing local MP4 or MOV file.")
    return path


def wav_seconds(path: Path, limit: float) -> float:
    """Duration of a PCM WAV, rejecting anything empty, compressed or over `limit` seconds."""
    if not path.is_file() or path.suffix.lower() != ".wav":
        raise ContractError("The audio must be an existing WAV file.")
    try:
        with wave.open(str(path), "rb") as wav:
            if wav.getcomptype() != "NONE" or wav.getframerate() <= 0:
                raise ContractError("The audio must be uncompressed PCM WAV.")
            seconds = wav.getnframes() / wav.getframerate()
    except (wave.Error, EOFError, OSError) as exc:
        raise ContractError("The audio is not a valid PCM WAV.") from exc
    if not 0 < seconds <= limit:
        raise ContractError(f"The audio must be between zero and {limit:g} seconds.")
    return seconds


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


class Staging:
    """Scratch folder without spaces: upstream scripts pass paths through a shell unquoted."""

    def __init__(self, parent: Path):
        self.parent = parent

    def __enter__(self) -> Path:
        self.parent.mkdir(parents=True, exist_ok=True)
        self.path = Path(tempfile.mkdtemp(prefix="avatar-", dir=self.parent))
        if any(ch.isspace() for ch in str(self.path)):
            shutil.rmtree(self.path, ignore_errors=True)
            raise StationMissing("The engine folder path contains spaces; move the OpcOS runtime to a path without spaces.")
        return self.path

    def __exit__(self, *exc):
        shutil.rmtree(self.path, ignore_errors=True)
        return False
