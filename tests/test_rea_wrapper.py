"""Lớp bọc rea-video: argv an toàn, môi trường lọc, VLM luôn tắt. Dùng một «rea_video» giả, không mạng."""
import argparse
import json
import os
import sys

import pytest

from video_studio import contract
from video_studio.contract import ContractError, EngineError, StationMissing
from video_studio.reference import rea
from video_studio.reference import build_parser

FAKE = '''
import json, os, sys
if os.environ.get("FAKE_FAIL"):
    sys.stderr.write("boom\\n"); sys.exit(3)
print(json.dumps({"argv": sys.argv[1:], "env": sorted(os.environ), "home": os.environ.get("REA_VIDEO_HOME")}))
'''


@pytest.fixture
def fake(tmp_path, monkeypatch):
    src = tmp_path / "src"
    (src / "rea_video").mkdir(parents=True)
    (src / "rea_video" / "__init__.py").write_text("", encoding="utf-8")
    (src / "rea_video" / "__main__.py").write_text(FAKE, encoding="utf-8")
    monkeypatch.setenv("REA_VIDEO_PYTHON", sys.executable)
    monkeypatch.setenv("REA_VIDEO_SRC", str(src))
    monkeypatch.setenv("REA_VIDEO_HOME", str(tmp_path / "home"))
    return tmp_path


def _args(**kw):
    base = dict(action="decompose", input="clip.mp4", out="out", lang="en", ocr=False, stems=False,
                no_packaging=False, json=False)
    base.update(kw)
    return argparse.Namespace(**base)


def test_actions_registered_in_reference_parser():
    ap = build_parser()
    for act in rea.ACTIONS:
        assert act in ap.format_usage()


def test_decompose_argv_always_vlm_off_and_minimal():
    a = rea.build_argv("py", _args())
    assert "--no-vlm" in a and "--no-whole" in a and "--no-survey" in a
    assert "--no-asr" in a and "--no-speakers" in a and "--no-ocr" in a and "--no-stems" in a
    assert "--vlm" not in a and "--env-file" not in a


def test_optional_switches_only_remove_no_flags():
    a = rea.build_argv("py", _args(ocr=True, stems=True))
    assert "--no-ocr" not in a and "--no-stems" not in a and "--no-vlm" in a


def test_non_media_input_rejected():
    with pytest.raises(ContractError):
        rea.build_argv("py", _args(input="notes.txt"))


def test_unknown_action():
    with pytest.raises(ContractError):
        rea.build_argv("py", _args(action="remake-run"))


def test_remake_and_capsule_commands_not_exposed():
    assert not {"remake", "remake-plan", "remake-run", "capsule", "assemble", "code-remake", "drive", "pdf"} & set(rea.ACTIONS)


def test_missing_config_is_exit_3(monkeypatch):
    monkeypatch.delenv("REA_VIDEO_PYTHON", raising=False)
    monkeypatch.delenv("REA_VIDEO_SRC", raising=False)
    monkeypatch.setattr(rea._env, "env", lambda name: None)
    with pytest.raises(StationMissing) as e:
        rea.resolve()
    assert e.value.code == contract.STATION_MISSING


def test_run_filters_environment(fake, monkeypatch):
    for k in ("REA_VLM_API_KEY", "REA_VLM_BASE_URL", "CAPSULE_CINEMA_PYTHON", "REA_CHROME", "OPENAI_API_KEY"):
        monkeypatch.setenv(k, "secret-value")
    res = rea.run(_args(out=str(fake / "o" / "d")))
    data = json.loads(res["stdout_tail"][-1])
    for k in ("REA_VLM_API_KEY", "REA_VLM_BASE_URL", "CAPSULE_CINEMA_PYTHON", "REA_CHROME", "OPENAI_API_KEY"):
        assert k not in data["env"]
    assert data["home"] == str(fake / "home")
    assert "--no-vlm" in data["argv"] and res["vlm"] == "off" and "stdout_tail" in res["untrusted"]


def test_home_and_userprofile_do_not_point_at_real_home(fake):
    res = rea.run(_args(out=str(fake / "o" / "d")))
    data = json.loads(res["stdout_tail"][-1])
    assert "USERPROFILE" in data["env"] and "HOME" in data["env"]


def test_nonzero_exit_is_engine_error(fake, monkeypatch):
    monkeypatch.setenv("FAKE_FAIL", "1")
    # FAKE_FAIL không nằm trong danh sách cho phép nên không tới được tiến trình con ⇒ ép bằng src riêng
    src = fake / "src2"
    (src / "rea_video").mkdir(parents=True)
    (src / "rea_video" / "__init__.py").write_text("", encoding="utf-8")
    (src / "rea_video" / "__main__.py").write_text("import sys; sys.stderr.write('boom'); sys.exit(3)", encoding="utf-8")
    monkeypatch.setenv("REA_VIDEO_SRC", str(src))
    with pytest.raises(EngineError) as e:
        rea.run(_args(out=str(fake / "o" / "d")))
    assert "mã 3" in str(e.value)


def test_compare_and_videomd_argv():
    c = rea.build_argv("py", argparse.Namespace(action="compare", ref="a.mp4", remake="b.mp4", out="o", every=0.5, worst=8))
    assert c[6] == "compare" and "-o" in c
    v = rea.build_argv("py", argparse.Namespace(action="videomd", dir="d", check=True))
    assert v[-1] == "--check"
