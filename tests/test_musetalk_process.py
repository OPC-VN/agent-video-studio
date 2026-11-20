"""Exercise the success, spawn-error and deadline outcomes without loading models."""

import os
import sys

import pytest

from video_studio.musetalk import process


def test_worker_outcome_captures_each_stream(tmp_path):
    command = [sys.executable, "-B", "-c", "import sys; print('result'); print('progress', file=sys.stderr)"]
    station_logs = tmp_path / 'logs'
    station_logs.mkdir()
    outcome = process.run(command, dict(os.environ), station_logs)
    assert outcome.code == 0
    assert outcome.timeout is None
    assert outcome.stdout.strip() == "result"
    assert outcome.stderr.strip() == "progress"
    assert outcome.elapsed_seconds >= 0
    assert not list(station_logs.iterdir())


def test_worker_outcome_records_spawn_failure(tmp_path):
    outcome = process.run([str(tmp_path / "missing")], {}, tmp_path)
    assert outcome.spawn_failed
    assert outcome.code is None
    assert outcome.timeout is None


@pytest.mark.parametrize(
    ("total", "idle", "expected"), [(0.5, 5, "total"), (5, 0.5, "idle")]
)
def test_worker_outcome_distinguishes_deadlines(tmp_path, total, idle, expected):
    command = [sys.executable, "-B", "-c", "import time; time.sleep(60)"]
    outcome = process.run(command, dict(os.environ), tmp_path, total=total, idle=idle)
    assert outcome.timeout == expected
    assert outcome.code is not None
    assert outcome.elapsed_seconds >= min(total, idle)
