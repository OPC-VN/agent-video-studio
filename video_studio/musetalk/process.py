"""Supervise the avatar subprocess with distinct total and inactivity deadlines."""

from dataclasses import dataclass
from pathlib import Path
import os
import subprocess
import tempfile
import time

from video_studio.probe import _kill_tree

TOTAL_SECONDS = 3600
IDLE_SECONDS = 300
TAIL_BYTES = 16 * 1024


@dataclass(frozen=True)
class WorkerOutcome:
    code: int | None
    elapsed_seconds: float
    timeout: str | None
    stdout: str
    stderr: str
    spawn_failed: bool = False


def _tail(file):
    file.seek(max(0, os.fstat(file.fileno()).st_size - TAIL_BYTES))
    return file.read(TAIL_BYTES).decode("utf-8", "replace")


def run(argv, env, directory: Path, *, total=TOTAL_SECONDS, idle=IDLE_SECONDS):
    """Keep worker logs inside the station and return elapsed time, deadline and exit separately."""
    started = time.monotonic()
    with tempfile.TemporaryFile(dir=directory) as output, tempfile.TemporaryFile(dir=directory) as errors:
        group = (
            {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
            else {"start_new_session": True}
        )
        try:
            process = subprocess.Popen(
                argv, env=env, stdin=subprocess.DEVNULL, stdout=output, stderr=errors, **group
            )
        except OSError as exc:
            return WorkerOutcome(None, time.monotonic() - started, None, "", str(exc), spawn_failed=True)

        last_activity = time.monotonic()
        size = (0, 0)
        timed_out = None
        try:
            while process.poll() is None:
                now = time.monotonic()
                latest_size = (os.fstat(output.fileno()).st_size, os.fstat(errors.fileno()).st_size)
                if latest_size != size:
                    size, last_activity = latest_size, now
                if now - started >= total:
                    timed_out = "total"
                elif now - last_activity >= idle:
                    timed_out = "idle"
                if timed_out:
                    _kill_tree(process)
                    break
                time.sleep(min(0.25, total - (now - started), idle - (now - last_activity)))
        except BaseException:
            _kill_tree(process)
            raise
        return WorkerOutcome(process.poll(), time.monotonic() - started, timed_out, _tail(output), _tail(errors))
