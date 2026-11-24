"""Kiểm chuỗi script của skill video-long-to-shorts: bản đồ nguồn → cắt giọng → phụ đề.

Fixture tổng hợp: HTML giả dựng trong test, WAV sinh bằng code. Không cần ffmpeg, Node hay trạm.
"""
import array
import importlib.util
import json
import math
import wave
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "video-long-to-shorts" / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(f"vlts_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


source_map = load("source_map")
cut_voice = load("cut_voice")
make_subs = load("make_subs")

RATE = 8000
HTML = """<!doctype html><html><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="40">
<section id="s1" class="scene" data-start="0" data-duration="20"><img src="a.svg"></section>
<section id="s2" class="scene" data-start="20" data-duration="20"></section>
<audio id="voice" src="assets/voice.wav" data-start="2" data-duration="10" data-volume="1"></audio>
<audio id="voiceB" src="assets/voice.wav" data-start="20" data-duration="6" data-media-start="10"></audio>
<audio id="music" src="assets/music.wav" data-start="0" data-duration="40" data-volume="0.15"></audio>
<video id="take1" class="clip avatar" src="assets/take1.webm" data-start="4" data-duration="8"></video>
<video id="broll" class="clip" src="assets/broll.webm" data-start="20" data-duration="5" data-media-start="3"></video>
<div id="k0" class="kara"><span id="k0w0" class="w">Một</span> <span id="k0w1" class="w hi">người</span>
<span id="k0w2" class="w">có</span> <span id="k0w3" class="w">thể,</span></div>
<div id="k1" class="kara"><span id="k1w0" class="w">dẫn</span> <span id="k1w1" class="w">một</span>
<span id="k1w2" class="w">đội</span> <span id="k1w3" class="w">trợ-lý</span> <span id="k1w4" class="w">số.</span></div>
<div id="k2" class="kara"><span id="k2w0" class="w">Hết</span></div>
</div>
<script>
const tl = gsap.timeline({paused: true});
tl.set('#k0w0',{color:'#fff'},4.0); tl.set('#k0w0',{color:'#aaa'},4.4);
tl.to("#k0w1",{opacity:1,duration:.1},4.5);
tl.fromTo('#k0w2',{opacity:0},{opacity:1},5.0);
tl.set('#k0w3',{color:'#fff'},5.4);
tl.set('#k1w0',{color:'#fff'},6.0); tl.set('#k1w1',{color:'#fff'},6.4);
tl.set('#k1w2',{color:'#fff'},6.8); tl.set('#k1w3',{color:'#fff'},7.2);
tl.set('#k1w4',{color:'#fff'},7.9);
tl.set('#other',{x:1},1.0);
</script></body></html>"""


def write_tone(path, seconds, freq=220.0, rate=RATE):
    samples = array.array("h", (int(12000 * math.sin(2 * math.pi * freq * n / rate))
                                for n in range(int(seconds * rate))))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(samples.tobytes())


def make_source(tmp_path):
    src = tmp_path / "hf"
    src.mkdir()
    (src / "index.html").write_text(HTML, encoding="utf-8")
    write_tone(src / "assets" / "voice.wav", 16)
    out = tmp_path / "source-map.json"
    code = source_map.main([str(src / "index.html"), "--out", str(out)])
    return src, out, code


def test_source_map_reads_clips_words_and_first_gsap_cue(tmp_path):
    _src, out, code = make_source(tmp_path)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert code == 1 and any("thiếu mốc" in w for w in data["warnings"])   # k2w0 không có lệnh GSAP
    assert data["schema_version"] == 1 and data["source"] == "index.html" and data["duration"] == 40
    assert [(s["id"], s["start"], s["end"]) for s in data["sections"]] == [("s1", 0, 20), ("s2", 20, 40)]
    audio = {a["id"]: a for a in data["audio"]}
    assert audio["voiceB"]["media_start"] == 10 and audio["voiceB"]["end"] == 26
    assert audio["music"]["volume"] == 0.15 and audio["voice"]["media_start"] == 0
    videos = {v["id"]: v for v in data["videos"]}
    assert videos["take1"]["avatar"] is True and videos["broll"]["avatar"] is False
    assert videos["broll"]["media_start"] == 3
    words = {w["id"]: w for w in data["words"]}
    assert words["k0w0"]["t"] == 4.0, "mốc là lệnh GSAP ĐẦU TIÊN nhắm id"
    assert words["k0w1"]["t"] == 4.5 and words["k0w2"]["t"] == 5.0 and words["k2w0"]["t"] is None
    assert words["k1w3"]["text"] == "trợ-lý" and "other" not in words
    lines = {line["id"]: line for line in data["lines"]}
    assert lines["k0"]["text"] == "Một người có thể," and lines["k0"]["start"] == 4.0
    assert lines["k1"]["word_ids"][-1] == "k1w4"


def test_source_map_exit_codes(tmp_path):
    assert source_map.main([str(tmp_path / "missing.html")]) == 2
    clean = tmp_path / "clean.html"
    clean.write_text('<audio id="a" src="v.wav" data-start="0" data-duration="5"></audio>'
                     '<div id="k0" class="kara"><span id="k0w0" class="w">Chào</span></div>'
                     "<script>tl.set('#k0w0',{x:1},0.5);</script>", encoding="utf-8")
    assert source_map.main([str(clean), "--out", str(tmp_path / "m.json")]) == 0


PLAN = {"lead": 0.3, "gap": 0.25, "fade_ms": 20, "tail": 1.0, "segments": [
    {"id": "S1", "tl_in": 3.9, "tl_out": 8.4, "first_word": "k0w0", "last_word": "k1w4"},
    {"id": "S2", "tl_in": 21.0, "tl_out": 23.0, "clip": "voiceB", "first_word": "k2w0",
     "last_word": "k2w0"},
]}


def run_cut(tmp_path, plan=PLAN):
    src, smap, _ = make_source(tmp_path)
    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps(plan), encoding="utf-8")
    out, beats = tmp_path / "voice.wav", tmp_path / "beats.json"
    argv = ["--source-map", str(smap), "--plan", str(plan_file), "--media-root", str(src),
            "--out", str(out), "--beats-out", str(beats)]
    return cut_voice.main(argv), out, beats, smap, argv, src


def test_cut_voice_maps_timeline_to_media_per_clip(tmp_path):
    code, out, beats_file, *_ = run_cut(tmp_path)
    assert code == 0
    beats = json.loads(beats_file.read_text(encoding="utf-8"))
    s1, s2 = beats["segments"]
    assert (s1["clip"], s1["media_in"], s1["media_out"]) == ("voice", 1.9, 6.4)
    assert (s2["clip"], s2["media_in"], s2["media_out"]) == ("voiceB", 11.0, 13.0), \
        "media = t − start + media_start của ĐÚNG clip, không một offset chung"
    assert s1["short_in"] == 0.3 and s1["short_out"] == 4.8
    assert s2["short_in"] == 5.05 and beats["total"] == 8.05
    assert s1["avatar"] is None, "avatar chỉ bắt đầu ở 4 s, sau đầu đoạn"
    assert s2["avatar"] is None and s1["first_word"] == "k0w0"
    with wave.open(str(out), "rb") as w:
        assert w.getframerate() == RATE and w.getnframes() == int(8.05 * RATE)
        frames = array.array("h")
        frames.frombytes(w.readframes(w.getnframes()))
    lead = int(0.3 * RATE)
    assert max(abs(x) for x in frames[:lead]) == 0, "đệm đầu im tuyệt đối"
    assert abs(frames[lead]) < 200 and abs(frames[lead + int(4.5 * RATE) - 1]) < 200, "fade hai đầu"
    assert max(abs(x) for x in frames[lead + 400:lead + 800]) > 10000
    assert max(abs(x) for x in frames[-int(0.9 * RATE):]) == 0, "đuôi im cho thẻ kết"


def test_cut_voice_reports_mid_take_avatar_offset(tmp_path):
    plan = {"segments": [{"id": "S1", "tl_in": 6.5, "tl_out": 9.0}]}
    code, _out, beats_file, *_ = run_cut(tmp_path, plan)
    assert code == 0
    avatar = json.loads(beats_file.read_text(encoding="utf-8"))["segments"][0]["avatar"]
    assert avatar == {"id": "take1", "src": "assets/take1.webm", "media_start": 2.5,
                      "covers_segment": True}


@pytest.mark.parametrize("plan", [
    {"segments": [{"id": "S1", "tl_in": 11.0, "tl_out": 21.0, "clip": "voice"}]},   # vắt qua ranh clip
    {"segments": [{"id": "S1", "tl_in": 6.0, "tl_out": 5.0}]},                      # ngược chiều
    {"segments": [{"id": "S1", "tl_in": 13.0, "tl_out": 14.0}]},                    # chỉ nhạc phủ, nhạc vẫn là clip hợp lệ → xem test âm
    {"segments": []},
    {"segments": [{"id": "S1", "tl_in": 5.0}]},
])
def test_cut_voice_rejects_bad_plans(tmp_path, plan):
    only_music = plan["segments"] and plan["segments"][0].get("tl_in") == 13.0
    # 13–14 s chỉ có clip nhạc phủ; file nhạc không tồn tại trong fixture → lỗi âm (1), không phải plan (2)
    assert run_cut(tmp_path, plan)[0] == (1 if only_music else 2)


def test_cut_voice_audio_errors_exit_1(tmp_path):
    past_end = {"segments": [{"id": "S1", "tl_in": 22.0, "tl_out": 25.9, "clip": "voiceB"}]}
    code, _out, _beats, _smap, argv, src = run_cut(tmp_path, past_end)
    assert code == 0                                        # file 16 s đủ cho media 12–15,9
    write_tone(src / "assets" / "voice.wav", 12)            # rút ngắn file: đoạn vượt độ dài
    assert cut_voice.main(argv) == 1
    (src / "assets" / "voice.wav").unlink()
    assert cut_voice.main(argv) == 1


def test_cut_voice_ambiguous_clip_needs_explicit_choice():
    audio = [{"id": "a", "start": 0, "end": 10, "volume": 1.0},
             {"id": "b", "start": 0, "end": 10, "volume": 1.0},
             {"id": "m", "start": 0, "end": 10, "volume": 0.1}]
    seg = {"id": "S1", "tl_in": 1, "tl_out": 2}
    with pytest.raises(cut_voice.PlanError, match="ghi rõ"):
        cut_voice.pick_clip(audio, seg)
    assert cut_voice.pick_clip(audio, dict(seg, clip="b"))["id"] == "b"
    assert cut_voice.pick_clip(audio[1:], seg)["id"] == "b", "giọng thắng nhạc nền theo volume"


def test_make_subs_keeps_source_text_and_takes_timing_from_asr(tmp_path):
    _code, _out, beats_file, smap, *_ = run_cut(tmp_path)
    asr = [[0.42, 0.6, "Một"], [0.9, 1.1, "người"], [1.5, 1.6, "có"], [1.9, 2.1, "thể"],
           [2.5, 2.7, "dẫn"], [2.9, 3.0, "một"], [3.3, 3.5, "đội"], [3.7, 3.9, "trợ"],
           [3.9, 4.1, "lí"], [4.3, 4.6, "số"], [5.1, 5.4, "Hết"]]
    asr_file, out = tmp_path / "asr.json", tmp_path / "subs.json"
    asr_file.write_text(json.dumps(asr), encoding="utf-8")
    code = make_subs.main(["--source-map", str(smap), "--beats", str(beats_file), "--asr",
                           str(asr_file), "--out", str(out)])
    data = json.loads(out.read_text(encoding="utf-8"))
    assert code == 0 and data["timing"] == "asr" and data["warnings"] == []
    texts = [s["text"] for s in data["subs"]]
    assert texts == ["Một người có thể,", "dẫn một đội trợ-lý số.", "Hết"], "chữ nguyên văn từ nguồn"
    first = data["subs"][0]
    assert first["words"][0] == ["Một", 0.42] and first["words"][3] == ["thể,", 1.9]
    assert data["subs"][1]["words"][3][1] == 3.7, "từ có gạch nối lấy mốc mảnh đầu"
    assert all(a["t1"] <= b["t0"] + 1e-9 for a, b in zip(data["subs"], data["subs"][1:]))
    assert all(len(s["words"]) <= 5 for s in data["subs"])


def test_make_subs_without_asr_is_draft_only_and_long_clause_splits(tmp_path):
    _code, _out, beats_file, smap, *_ = run_cut(tmp_path)
    out = tmp_path / "subs.json"
    code = make_subs.main(["--source-map", str(smap), "--beats", str(beats_file), "--out",
                           str(out), "--max-chars", "12"])
    data = json.loads(out.read_text(encoding="utf-8"))
    assert code == 1 and data["timing"] == "source"
    assert any("bản nháp" in w for w in data["warnings"])
    assert data["subs"][0]["words"][0][1] == 0.4, "4,0 s nguồn − 3,9 s đầu đoạn + 0,3 s đệm"
    assert all(len(s["text"]) <= 12 for s in data["subs"])
    assert " ".join(s["text"] for s in data["subs"]) == "Một người có thể, dẫn một đội trợ-lý số. Hết"


def test_make_subs_unknown_word_id_is_usage_error(tmp_path):
    _code, _out, beats_file, smap, *_ = run_cut(tmp_path)
    beats = json.loads(beats_file.read_text(encoding="utf-8"))
    beats["segments"][0]["first_word"] = "k9w9"
    beats_file.write_text(json.dumps(beats), encoding="utf-8")
    assert make_subs.main(["--source-map", str(smap), "--beats", str(beats_file), "--out",
                           str(tmp_path / "s.json")]) == 2
