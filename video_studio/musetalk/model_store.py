"""Install and verify the model bytes for the optional Windows MuseTalk engine."""

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener

RESOURCE_KEY = "musetalk-1-5"
REPO_KEY = "agent-video-studio"
LOCK_PATH = Path(__file__).resolve().parents[1] / "locks" / "musetalk-models.json"
CHUNK_SIZE = 4 * 1024 * 1024
MAX_ARTIFACT_SIZE = 4_000_000_000
SHA256 = re.compile(r"[0-9a-f]{64}")
REVISION = re.compile(r"[0-9a-f]{40}")
COMPONENT = re.compile(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*")


@dataclass(frozen=True)
class Artifact:
    url: str
    dest: str
    size: int
    digest: str


def safe_relative(value: str) -> str:
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{n}" for n in range(1, 10)), *(f"LPT{n}" for n in range(1, 10))}
    if any(
        not COMPONENT.fullmatch(part) or part.endswith(".") or part.split(".", 1)[0].upper() in reserved
        for part in value.split("/")
    ):
        raise ValueError("The MuseTalk lock contains an invalid relative path.")
    return value


def artifact_url(row: dict) -> str:
    if "url" in row:
        url = row["url"]
        prefix = "https://media.githubusercontent.com/media/opencv/opencv_zoo/"
        name = "/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
        if not url.startswith(prefix) or not url.endswith(name):
            raise ValueError("Unexpected model publisher URL.")
        if not REVISION.fullmatch(url[len(prefix):-len(name)]):
            raise ValueError("The GitHub model must be pinned to a full commit.")
        return url
    repo = safe_relative(row["repo"])
    if len(repo.split("/")) != 2 or not REVISION.fullmatch(row["revision"]):
        raise ValueError("The Hugging Face repo must be pinned to a full revision.")
    return f"https://huggingface.co/{repo}/resolve/{row['revision']}/{safe_relative(row['path'])}"


def read_lock() -> tuple[list[Artifact], str]:
    data = LOCK_PATH.read_bytes()
    lock = json.loads(data)
    if lock.get("schema") != "musetalk-model-lock/1" or lock.get("status") != "complete":
        raise ValueError("The MuseTalk model lock has not been finalized.")
    artifacts = []
    destinations = set()
    for row in lock["artifacts"]:
        dest = safe_relative(row["dest"])
        size, digest = row["bytes"], row["sha256"]
        if type(size) is not int or not 0 < size <= MAX_ARTIFACT_SIZE or not SHA256.fullmatch(digest):
            raise ValueError(f"Invalid size or SHA-256 for {dest}.")
        if dest.casefold() in destinations:
            raise ValueError(f"Duplicate model destination: {dest}.")
        destinations.add(dest.casefold())
        artifacts.append(Artifact(artifact_url(row), dest, size, digest))
    if not artifacts:
        raise ValueError("The model lock has no artifacts.")
    return artifacts, hashlib.sha256(data).hexdigest()


def regular_path(path: Path) -> None:
    """Reject links, junctions and placeholders before accessing a runtime path."""
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        attributes = getattr(info, "st_file_attributes", 0)
        if stat.S_ISLNK(info.st_mode) or attributes & (
            getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0) | getattr(stat, "FILE_ATTRIBUTE_OFFLINE", 0)
        ):
            raise ValueError(f"Unexpected reparse point or offline path: {item}.")


def model_dir(engine: Path) -> Path:
    engine = engine.absolute()
    if engine.parts[-3:] != ("engines", REPO_KEY, RESOURCE_KEY):
        raise ValueError("Use the path from opcos-runtime resolve engines agent-video-studio musetalk-1-5.")
    receipt = engine / ".opcos-resource.json"
    regular_path(receipt)
    manifest = json.loads(receipt.read_text(encoding="utf-8"))
    expected = {
        "schema": "opcos-resource/1",
        "category": "engines",
        "repoKey": REPO_KEY,
        "resourceKey": RESOURCE_KEY,
        "installed_by": REPO_KEY,
        "status": "complete",
    }
    if any(manifest.get(name) != value for name, value in expected.items()):
        raise ValueError("The engine directory does not have a matching OpcOS ownership receipt.")
    return engine / "models"


class PublisherRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        url = urlsplit(newurl)
        host = url.hostname or ""
        allowed = ("huggingface.co", "hf.co", "githubusercontent.com")
        if (
            url.scheme != "https" or url.port not in (None, 443) or url.username or url.password
            or not any(host == domain or host.endswith("." + domain) for domain in allowed)
        ):
            raise ValueError("Unexpected redirect while downloading a MuseTalk model.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def verify(path: Path, item: Artifact) -> None:
    regular_path(path)
    if not path.is_file() or path.stat().st_size != item.size:
        raise ValueError(f"Missing or wrong-sized model: {item.dest}.")
    with path.open("rb") as src:
        digest = hashlib.file_digest(src, "sha256").hexdigest()
    if digest != item.digest:
        raise ValueError(f"SHA-256 mismatch for {item.dest}.")


def download(path: Path, item: Artifact) -> None:
    regular_path(path)
    if path.exists():
        verify(path, item)
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=".musetalk-", suffix=".part", dir=path.parent, delete=False) as out:
        part = Path(out.name)

    deadline = time.monotonic() + 1800
    try:
        digest = hashlib.sha256()
        size = 0
        opener = build_opener(PublisherRedirect())
        with opener.open(item.url, timeout=45) as response, part.open("wb") as out:
            while data := response.read(CHUNK_SIZE):
                size += len(data)
                if size > item.size or time.monotonic() > deadline:
                    raise ValueError(f"Download limits exceeded for {item.dest}.")
                digest.update(data)
                out.write(data)
        if size != item.size or digest.hexdigest() != item.digest:
            raise ValueError(f"Publisher content did not match the lock for {item.dest}.")
        try:
            os.link(part, path)
        except FileExistsError:
            verify(path, item)
    finally:
        part.unlink(missing_ok=True)


def install(engine: Path, verify_only: bool) -> None:
    files, lock_hash = read_lock()
    models = model_dir(engine)
    marker = models / ".musetalk-ready.json"
    regular_path(marker)
    ready = {"schema": "musetalk-model-ready/1", "lock_sha256": lock_hash, "artifact_count": len(files)}
    if verify_only and (not marker.is_file() or json.loads(marker.read_text(encoding="utf-8")) != ready):
        raise ValueError("The runtime has no readiness receipt matching the current model lock.")
    for item in files:
        path = models / item.dest
        print(f"{'Verify' if verify_only else 'Prepare'} {item.dest}", file=sys.stderr, flush=True)
        if verify_only:
            verify(path, item)
        else:
            download(path, item)
    if not verify_only:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=models, delete=False) as out:
            part = Path(out.name)
            json.dump(ready, out)
        try:
            os.replace(part, marker)
        finally:
            part.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", required=True, type=Path, help="OpcOS engine directory")
    parser.add_argument("--verify-only", action="store_true", help="Check the readiness receipt and file bytes offline")
    args = parser.parse_args()
    try:
        install(args.engine_dir, args.verify_only)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"MuseTalk models: {exc}", file=sys.stderr)
        return 1
    print("MuseTalk models verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
