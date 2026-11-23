"""corpus_extract.py (skill video-reverse-engineer): đọc mốc đổi chế độ từ nhật ký cảnh. Không cần ffmpeg."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "corpus_extract", ROOT / "skills" / "video-reverse-engineer" / "assets" / "corpus_extract.py")
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)

LOG = """# Nhật ký
| # | thời gian | chế độ | bố cục |
|---|---|---|---|
| 1 | 0:00–0:02 | P | người giữa |
| 2 | 0:02–0:06 | P | người giữa |
| 3 | 0:06–0:12 | PS | màn hình + PIP |
| 4 | 1:02–1:10 | A | sơ đồ |
| 5 | 1:10–1:12 | ?? | lỗi |
"""


def test_switches_found_with_strip_lead():
    sw = ce.find_switches(LOG, lead=1.2)
    assert [(s["from"], s["to"], s["at"]) for s in sw] == [("P", "PS", 6.0), ("PS", "A", 62.0)]
    assert sw[0]["strip_at"] == 4.8


def test_switches_cli_rejects_empty_log(tmp_path):
    f = tmp_path / "x.md"
    f.write_text("không có bảng", encoding="utf-8")
    assert ce.main(["switches", "--log", str(f)]) == 2


def test_strips_rejects_bad_times(tmp_path, monkeypatch):
    monkeypatch.setattr(ce, "_ffmpeg", lambda: "ffmpeg")
    assert ce.main(["strips", "--input", "v.mp4", "--out", str(tmp_path), "--at", "a,b"]) == 2


RANGED = """| # | thời gian | chế độ |
|---|---|---|
| 1 | 0:00–0:10 | P |
| 2 | 0:10–0:30 | PS |
| 3 | 0:32–0:40 | A |
| 4 | 0:40–1:00 | PS |
| 5 | 1:00–13:18 | PA |
"""


def test_stats_counts_by_machine_and_flags_beyond_duration():
    st = ce.log_stats(RANGED, duration=767)
    assert st["rows"] == 5 and st["mode_switches"] == 4
    assert st["gaps_or_overlaps"] == ["#2→#3 hở 2.0 s"]
    assert st["beyond_duration"] == ["#5 kết thúc 798 s > 767 s"]
    assert st["person_pct"] == round(100 * (10 + 20 + 20 + 738) / 796, 1)


def test_per_pair_limits_repeated_switch_kinds():
    log = RANGED.replace("| 4 | 0:40–1:00 | PS |", "| 4 | 0:40–1:00 | PS |\n| 6 | 1:00–1:05 | A |\n| 7 | 1:05–1:10 | PS |")
    all_sw = ce.find_switches(log)
    one = ce.find_switches(log, per_pair=1)
    assert len(one) < len(all_sw)
    assert len({(s["from"], s["to"]) for s in one}) == len(one)
