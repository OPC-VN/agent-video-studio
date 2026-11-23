"""Kiểm script nhịp cảnh của skill vlog-design (chỉ thư viện chuẩn, không cần trạm)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "vlog-design" / "scripts" / "pace_check.py"

spec = importlib.util.spec_from_file_location("pace_check", SCRIPT)
pace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pace)

HEADER = "| Cảnh | Beat | Từ | Đến | Chế độ | LY | TR | Chương |\n|---|---|---|---|---|---|---|---|\n"


def write(tmp_path, rows):
    f = tmp_path / "pacing.md"
    f.write_text("# Bảng nhịp\n\n" + HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return str(f)


def run(f, *extra):
    a = pace.build_parser().parse_args([f, *extra])
    return pace.check(pace.read_table(Path(f)), a)


PRESENTER = [
    "| C01 | B01 | 0:00 | 0:10 | P | LY-01 | TR-10 | 1 |",
    "| C02 | B01 | 0:10 | 0:28 | PA | LY-03 | TR-03 | 1 |",
    "| C03 | B02 | 0:28 | 0:46 | PS | LY-05 | TR-02 | 1 |",
    "| C04 | B03 | 0:46 | 1:04 | A | LY-14 | TR-02 | 2 |",
    "| C05 | B04 | 1:04 | 1:40 | PA | LY-04 | TR-02 | 2 |",
]


def test_presenter_profile_passes_presenter_heavy_video(tmp_path):
    f = write(tmp_path, PRESENTER)
    assert pace.main([f]) == 0
    assert run(f)["person_pct"] == 82.0


def test_animation_profile_rejects_same_video(tmp_path):
    f = write(tmp_path, PRESENTER)
    assert pace.main([f, "--profile", "animation"]) == 1


def test_too_much_p_and_gap_fail(tmp_path):
    f = write(tmp_path, [
        "| C01 | B01 | 0:00 | 0:40 | P | LY-01 | TR-10 | 1 |",
        "| C02 | B02 | 0:41 | 1:00 | PA | LY-03 | TR-02 | 1 |",
    ])
    joined = " ".join(run(f)["errors"])
    assert "P " in joined and "hở" in joined
    assert pace.main([f]) == 1


def test_same_layout_run_error_for_slides_warning_for_screen(tmp_path):
    slides = write(tmp_path, [
        f"| C0{i} | B01 | 0:{i*10:02d} | 0:{i*10+10:02d} | PA | LY-03 | TR-02 | 1 |" for i in range(4)
    ])
    assert any("liền cùng LY-03" in e for e in run(slides)["errors"])
    screen = write(tmp_path, [
        f"| C0{i} | B01 | 0:{i*10:02d} | 0:{i*10+10:02d} | PS | LY-05 | TR-09 | 1 |" for i in range(4)
    ])
    res = run(screen)
    assert not any("liền cùng" in e for e in res["errors"])
    assert any("liền cùng LY-05" in w for w in res["warnings"])


def test_cut_leaving_fullframe_and_long_absence_warn(tmp_path):
    f = write(tmp_path, [
        "| C01 | B01 | 0:00 | 0:08 | P | LY-01 | TR-10 | 1 |",
        "| C02 | B01 | 0:08 | 0:20 | PS | LY-05 | TR-01 | 1 |",
        "| C03 | B02 | 0:20 | 1:30 | A | LY-14 | TR-02 | 1 |",
        "| C04 | B03 | 1:30 | 3:00 | PA | LY-03 | TR-03 | 2 |",
    ])
    warns = " ".join(run(f)["warnings"])
    assert "rời toàn khung" in warns and "người vắng 70 s" in warns


def test_bad_layout_code_and_bad_table(tmp_path):
    f = write(tmp_path, ["| C01 | B01 | 0:00 | 0:30 | PA | layout3 | TR-02 | 1 |"])
    assert any("sai dạng" in e for e in run(f)["errors"])
    bad = tmp_path / "x.md"
    bad.write_text("không có bảng", encoding="utf-8")
    assert pace.main([str(bad)]) == 2
