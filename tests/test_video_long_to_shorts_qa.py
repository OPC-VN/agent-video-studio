"""Kiểm qa_short.py: phần đọc số là hàm thuần; lượt chạy thật bỏ qua khi máy thiếu ffmpeg."""
import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "video-long-to-shorts" / "scripts" / "qa_short.py"

spec = importlib.util.spec_from_file_location("vlts_qa_short", SCRIPT)
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)

EBUR = """[Parsed_ebur128_0 @ 0] t: 1.2  TARGET:-23 LUFS    M: -20.1 S: -21.0     I: -19.9 LUFS  LRA: 0.0 LU
[Parsed_ebur128_0 @ 0] Summary:

  Integrated loudness:
    I:         -14.1 LUFS
    Threshold: -24.5 LUFS

  Loudness range:
    LRA:         3.2 LU

  True peak:
    Peak:       -1.4 dBFS
"""


def args(*extra):
    return qa.build_parser().parse_args(["x.mp4", *extra])


def probe(**kw):
    return dict({"width": 1080, "height": 1920, "fps": 30.0, "duration": 46.5, "has_audio": True}, **kw)


def failed(rows):
    return [r["check"] for r in rows if not r["ok"]]


def test_parsers_read_the_summary_not_the_running_lines():
    assert qa.parse_ebur128(EBUR) == (-14.1, -1.4)
    assert qa.parse_ebur128("no summary here") == (None, None)
    assert qa.parse_rate("30000/1001") == pytest.approx(29.97, abs=0.001)
    assert qa.parse_first_sound("silence_start: 0\nsilence_end: 0.31 | silence_duration: 0.31") == 0.31
    assert qa.parse_first_sound("silence_start: 12.5\nsilence_end: 13.0") == 0.0
    assert qa.parse_first_sound("") == 0.0
    assert qa.parse_first_sound("silence_start: 0") is None, "im tới hết file"


def test_parse_probe_picks_video_stream_and_audio_flag():
    payload = {"format": {"duration": "40.500000"},
               "streams": [{"codec_type": "audio"},
                           {"codec_type": "video", "width": 1080, "height": 1920,
                            "avg_frame_rate": "30/1"}]}
    assert qa.parse_probe(payload) == probe(duration=40.5)
    with pytest.raises(qa.ProbeError):
        qa.parse_probe({"streams": [{"codec_type": "audio"}]})


def test_evaluate_passes_measured_numbers_and_flags_each_miss():
    assert failed(qa.evaluate(probe(), -14.1, -1.4, 0.3, args())) == []
    assert failed(qa.evaluate(probe(width=1920, height=1080), -14.1, -1.4, 0.3, args())) == ["frame"]
    assert failed(qa.evaluate(probe(fps=25.0, duration=120.0), -14.1, -1.4, 0.3, args())) == ["fps", "duration"]
    assert failed(qa.evaluate(probe(), -19.0, -0.2, 1.4, args())) == ["loudness", "true_peak", "first_sound"]
    assert failed(qa.evaluate(probe(), None, None, None, args())) == ["loudness", "true_peak", "first_sound"]
    assert failed(qa.evaluate(probe(has_audio=False), None, None, None, args())) == ["audio_stream"]
    assert failed(qa.evaluate(probe(duration=68.9), -14.1, -1.4, 0.3, args("--max-dur", "60"))) == ["duration"]


def test_missing_file_is_usage_error_and_missing_tools_exit_3(tmp_path):
    assert qa.main([str(tmp_path / "none.mp4")]) == 2
    fake = tmp_path / "short.mp4"
    fake.write_bytes(b"not a video")
    empty = tmp_path / "no-tools"
    empty.mkdir()
    assert qa.main([str(fake), "--ffmpeg-dir", str(empty)]) == 3


@pytest.mark.skipif(not (shutil.which("ffmpeg") and shutil.which("ffprobe")),
                    reason="máy không có ffmpeg/ffprobe")
def test_real_render_roundtrip(tmp_path):
    clip = tmp_path / "short.mp4"
    made = subprocess.run(
        [shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", "color=c=black:s=1080x1920:r=30:d=3",
         "-f", "lavfi", "-i", "sine=frequency=330:duration=3",
         "-af", "adelay=300:all=1,volume=0.5", "-shortest", "-pix_fmt", "yuv420p", str(clip)],
        capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if made.returncode != 0 or not clip.exists():
        pytest.skip("ffmpeg trên máy không dựng được clip thử: " + made.stderr[-200:])
    probe_, lufs, peak, ffmpeg = qa.measure(clip)
    assert (probe_["width"], probe_["height"], probe_["fps"]) == (1080, 1920, 30.0)
    assert probe_["has_audio"] and lufs is not None and -30 < lufs < -5 and peak is not None
    first = qa.first_sound(clip, ffmpeg, -40)
    assert first is not None and 0.2 <= first <= 0.45
    assert qa.main([str(clip), "--min-dur", "2", "--lufs", str(lufs)]) == 0
    assert qa.main([str(clip), "--min-dur", "2", "--lufs", str(lufs), "--first-sound", "0.1"]) == 1
    assert qa.main([str(clip)]) == 1, "3 s ngắn hơn sàn 15 s mặc định"
