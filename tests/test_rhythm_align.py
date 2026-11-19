"""rhythm_align.py (skill video-reverse-engineer): so mốc nhịp hai thư mục decompose. Không cần mạng."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "rhythm_align", ROOT / "skills" / "video-reverse-engineer" / "assets" / "rhythm_align.py")
ra = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ra)


def _mk(tmp, name, body):
    d = tmp / name / "video"
    d.mkdir(parents=True)
    (d / "rhythm.md").write_text(body, encoding="utf-8")
    return str(tmp / name)


REF = "- #1: 0.000s @0 first, 0.600s @18 change\n- #2: 5.000s @150 first, 6.000s @180 change\n"
REM = "- #1: 0.000s @0 first, 0.700s @21 change\n- #2: 5.200s @156 first, 9.000s @270 change\n"


def test_read_marks_counts_shots_and_cuts(tmp_path):
    m = ra.read_marks(_mk(tmp_path, "a", REF))
    assert m["shots"] == 2 and m["marks"] == [0.0, 0.6, 5.0, 6.0] and m["cuts"] == [5.0]


def test_align_recall_precision_and_beats(tmp_path):
    out = ra.align(ra.read_marks(_mk(tmp_path, "a", REF)), ra.read_marks(_mk(tmp_path, "b", REM)), 0.5, [0.6, 5.0])
    assert out["recall"] == 0.75        # 6.0 không có mốc bản dựng trong ±0.5
    assert out["precision"] == 0.75     # 9.0 không có mốc mẫu
    assert out["beats_total"] == 2 and out["beats_ref_within_tol"] == 2 and out["beats_remake_within_tol"] == 2


def test_cli_missing_dir_is_exit_2(tmp_path, capsys):
    assert ra.main([str(tmp_path / "x"), str(tmp_path / "y")]) == 2


def test_cli_json_output(tmp_path, capsys):
    a, b = _mk(tmp_path, "a", REF), _mk(tmp_path, "b", REM)
    assert ra.main([a, b, "--tol", "0.5", "--beats", "0.6"]) == 0
    assert json.loads(capsys.readouterr().out)["tol_s"] == 0.5
