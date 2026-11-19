"""Run the JavaScript regression suite as part of pytest."""

import shutil
import subprocess
from pathlib import Path

import pytest


def test_node_suite():
    node = shutil.which("node")
    if node is None:
        pytest.skip("not_run: thiếu Node")
    root = Path(__file__).resolve().parents[1]
    tests = sorted((root / "tests").glob("*.test.cjs"))
    required = {
        "gsap-seek-check.test.cjs",
        "lens-flare.test.cjs",
        "lyric-ambient.test.cjs",
        "lyric-audio-visualizer.test.cjs",
    }
    assert required <= {path.name for path in tests}, "Required Node tests are missing"
    result = subprocess.run(
        [node, "--test", *(str(path) for path in tests)],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
