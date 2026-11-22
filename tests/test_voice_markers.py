"""Marker sắc thái (`[hao-hung]`) trong lời đọc của template bản tin: engine GIẢ — không GPU, không repo giọng.

Điều cần chứng minh, theo luật `voice-routing/references/vietnamese-tts-script.md`:
  1. chữ `[marker]` KHÔNG BAO GIỜ tới `engine.synth` / `model.generate` (nếu tới là bị đọc to);
  2. đường marker-aware chuyển marker đúng cho `vlab.synth` (marker hợp lệ đổi clip);
  3. phụ đề / gạch đầu dòng / transcript hiển thị không mang marker.
"""
import importlib
import re
import types

import pytest

from video_studio import voice

KNOWN = {"hao-hung", "nhan-manh", "trung-tinh"}


class FakeVlab:
    """Bản giả của `voice_studio.lab.vlab`, cùng ngữ nghĩa tách marker/câu (chỉ đủ cho test)."""
    NATIVE_TAGS = {"laughter", "sigh"}
    _B = re.compile(r"\[([a-z0-9][a-z0-9\-]*)\]", re.I)

    def __init__(self):
        self.calls = []

    def load_profile(self, name):
        return {"variants": {k: {} for k in KNOWN}}

    def split_sentences(self, chunk):
        return [s.strip() for s in re.split(r"(?<=[.!?…])\s+", chunk) if s.strip()]

    def split_by_marker(self, text, known):
        spans, unknown, cur, buf, pos = [], [], None, [], 0
        for m in self._B.finditer(text):
            low = m.group(1).lower()
            if low in self.NATIVE_TAGS:
                continue
            buf.append(text[pos:m.start()])
            pos = m.end()
            if low in known:
                chunk = "".join(buf).strip()
                if chunk:
                    spans.append((cur, chunk))
                buf, cur = [], low
            else:
                unknown.append(low)
        buf.append(text[pos:])
        chunk = "".join(buf).strip()
        if chunk:
            spans.append((cur, chunk))
        return spans, unknown

    def synth(self, model, text, profile_name, language="Vietnamese", speed=None, verbose=True, seed=42):
        self.calls.append((text, profile_name, seed))
        return [0.0] * 8, 24000, {}


class FakeEngine:
    def __init__(self):
        self.texts = []

    def synth(self, text, prompt=None, **kw):
        self.texts.append(text)
        return [0.0] * 8, 24000


@pytest.fixture
def fakes(monkeypatch):
    monkeypatch.setattr(voice, "_to_array", lambda a: a)      # CI lõi không có numpy
    vlab, eng = FakeVlab(), FakeEngine()
    table = {"lab.vlab": vlab, "engine": eng,
             "profiles": types.SimpleNamespace(
                 ensure_default=lambda name=None: name or "mac-dinh",
                 get_clone_prompt=lambda model, name=None: "PROMPT")}

    def fake_module(name):
        if name not in table:
            raise voice.StationMissing(name)
        return table[name]

    monkeypatch.setattr(voice, "module", fake_module)
    return vlab, eng


# ── strip_markers ────────────────────────────────────────────────────────────────────────

def test_strip_markers_removes_every_bracket_for_display():
    assert voice.strip_markers("[hao-hung] Xin chào [laughter] bạn. [nhan-manh]Hết.") == \
        "Xin chào bạn. Hết."


def test_strip_markers_keep_native_for_engine():
    out = voice.strip_markers("[hao-hung] Vui [laughter] quá", keep_native=True)
    assert "[hao-hung]" not in out and "[laughter]" in out


def test_strip_markers_leaves_plain_text_alone():
    assert voice.strip_markers("Không có marker, có [Hình 1] chú thích.") == \
        "Không có marker, có [Hình 1] chú thích."
    assert voice.strip_markers(None) == ""


# ── synth_text ───────────────────────────────────────────────────────────────────────────

def test_synth_text_marked_voice_goes_through_vlab_with_marker(fakes):
    vlab, eng = fakes
    mv = voice.MarkedVoice("giong-a", "PROMPT", seed=7)
    voice.synth_text(object(), "[hao-hung] Mở đầu. [nhan-manh] Chốt ý.", mv)
    assert vlab.calls == [("[hao-hung] Mở đầu. [nhan-manh] Chốt ý.", "giong-a", 7)]
    assert eng.texts == []                      # không đường nào chạm engine.synth


def test_synth_text_profile_name_and_none_use_vlab(fakes):
    vlab, _ = fakes
    voice.synth_text(object(), "[hao-hung] A.", "giong-b")
    voice.synth_text(object(), "[hao-hung] B.", None)       # None = profile mặc định của trạm
    assert [c[1] for c in vlab.calls] == ["giong-b", "mac-dinh"]


def test_synth_text_legacy_prompt_never_sends_marker_to_engine(fakes):
    vlab, eng = fakes
    voice.synth_text(object(), "[hao-hung] Mở đầu [laughter] nhé. [loai-la] Hết.", object())
    assert vlab.calls == []
    assert len(eng.texts) == 1
    sent = eng.texts[0]
    assert "[hao-hung]" not in sent and "[loai-la]" not in sent
    assert "[laughter]" in sent                 # thẻ gốc của engine được giữ nguyên


# ── synth_sentences ──────────────────────────────────────────────────────────────────────

def test_synth_sentences_carry_marker_across_sentences_and_clean_display(fakes):
    vlab, _ = fakes
    text = "[hao-hung] Câu một. Câu hai. [nhan-manh] Câu ba. [khong-co] Câu bốn."
    res = voice.synth_sentences(object(), text, "giong-a")
    assert [s for s, _a in res] == ["Câu một.", "Câu hai.", "Câu ba.", "Câu bốn."]
    # marker có hiệu lực tới marker kế; marker lạ bị gỡ và quay về marker đang có
    assert [c[0] for c in vlab.calls] == [
        "[hao-hung] Câu một.", "[hao-hung] Câu hai.", "[nhan-manh] Câu ba.", "[nhan-manh] Câu bốn."]
    assert all("[khong-co]" not in c[0] for c in vlab.calls)


def test_synth_sentences_legacy_prompt_strips_markers(fakes):
    _, eng = fakes
    res = voice.synth_sentences(object(), "[hao-hung] Một. [nhan-manh] Hai.", object())
    assert [s for s, _a in res] == ["Một.", "Hai."]
    assert all("[" not in t for t in eng.texts)


# ── template: lời đọc có marker, chữ hiển thị không có ───────────────────────────────────

def test_synth_long_passes_markers_to_marker_aware_path(news, monkeypatch):
    got = []
    monkeypatch.setattr(voice, "synth_text", lambda model, text, v, **k: got.append((text, v)) or [0])
    monkeypatch.setattr(news.engine, "normalize", lambda a: a, raising=False)
    model = types.SimpleNamespace(sampling_rate=24000)
    mv = voice.MarkedVoice("giong-a", "PROMPT")
    news._synth_long(model, "[hao-hung] Một. [nhan-manh] Hai.", mv)
    assert got == [("[hao-hung] Một. [nhan-manh] Hai.", mv)]      # một lượt, marker nguyên vẹn


def test_synth_long_legacy_prompt_chunks_go_to_synth_text_which_strips(news, monkeypatch):
    got = []
    monkeypatch.setattr(voice, "synth_text", lambda model, text, v, **k: got.append((text, v)) or [0])
    monkeypatch.setattr(news.engine, "normalize", lambda a: a, raising=False)
    model = types.SimpleNamespace(sampling_rate=24000)
    raw = object()
    news._synth_long(model, "Một. Hai.", raw)
    assert got and all(v is raw for _t, v in got)


def test_display_helpers_never_show_marker(news):
    spoken = "[hao-hung] Xin chào các bạn. [nhan-manh] Đây là ý chính."
    events = news._caps_events([], spoken, 0.0, 10.0)
    assert events and all("[" not in t for _s, t in events)
    html, anim = [], []
    news._karaoke_caps([], spoken, 0.0, 10.0, html, anim, "k")
    assert html and all("[" not in h for h in html)
    bullets = news._seg_bullets({"narration": spoken})
    assert bullets and all("[" not in b for b in bullets)
    assert news._words_from_text([0] * 24000, 24000, spoken) is not None


def test_topstory_caption_chunks_never_show_marker(news):
    ts = importlib.import_module("video_studio.templates.news.top_story_video")
    chunks = ts._caption_chunks("[ke-chuyen] Chuyện bắt đầu từ đây. [nhan-manh] Và đây là kết quả.")
    assert chunks and all("[" not in c for c in chunks)
