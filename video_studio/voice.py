"""voice.py — MỘT cửa duy nhất của repo này sang repo giọng (`voice_studio`).

Vì sao có file này: `narrate`, `render` và template đều cần giọng, nhưng repo giọng là
**phụ thuộc tuỳ chọn** (extras `[voice]`). Nếu mỗi chỗ tự `import voice_studio` thì máy chưa
cài sẽ ném `ModuleNotFoundError` — một câu đúng sự thật nhưng nói cho sai người: người dùng
đọc traceback không biết phải cài gì. Ở đây mọi lần import đi qua `_mod()`, và cái ném ra là
`StationMissing` (mã 3) kèm đúng câu lệnh phải chạy.

Ba việc:

    narrate(...)      video câm + lời dẫn → MP4 có giọng (và nhạc nền), qua `voice_studio.narrate`
    mix_bgm(...)      trộn một lớp nhạc nền DƯỚI track giọng đã có của một file (tại chỗ)
    synth_text(...)   template bản tin tự tổng hợp từng khối lời đọc; đi qua ĐÚNG parser marker
                      sắc thái của repo giọng (`voice_studio.lab.vlab`): `[hao-hung]` đổi clip,
                      marker lạ bị gỡ, không bao giờ bị đọc thành tiếng

Không tự tổng hợp, không tự gọi ffmpeg: luật giọng (profile bắt buộc, seed ghim, chuẩn RMS) và
luật ghép (fit/shortest, âm lượng nhạc nền) sống ở repo giọng — chép sang đây là hai bản sao
của cùng một bài học, và bản thứ hai luôn là bản lạc hậu.
"""
import argparse
import importlib
import re

from .contract import ContractError, StationMissing

INSTALL_HINT = (
    "cài repo giọng vào CÙNG venv: `pip install -e <bản clone agent-voice-studio>` "
    "(rồi `pip install -e \".[voice]\"` ở repo này). Kiểm bằng `video-studio doctor`.")

__all__ = ["available", "api_version", "module", "narrate", "mix_bgm", "version",
           "MarkedVoice", "load_voice", "strip_markers", "synth_text", "synth_sentences"]


def _mod(name="voice_studio"):
    try:
        return importlib.import_module(name)
    except ImportError as e:
        raise StationMissing(f"bước này cần `{name}` nhưng venv đang chạy chưa có — "
                             + INSTALL_HINT) from e


def module(name):
    """Import một module con của repo giọng (`av`, `engine`, `profiles`, `narrate`…)."""
    _mod()                                  # gói cha trước: thông báo thiếu nói đúng tên gói
    return _mod("voice_studio." + name)


def available():
    """Repo giọng có trong venv này không (không ném lỗi — dùng cho doctor/JSON kết quả)."""
    try:
        importlib.import_module("voice_studio")
        return True
    except ImportError:
        return False


def version():
    """Bản PHÁT HÀNH của gói giọng (`voice_studio.__version__`, vd "0.3.0") — None nếu chưa cài."""
    try:
        return getattr(importlib.import_module("voice_studio"), "__version__", None)
    except ImportError:
        return None


def api_version():
    """Bản HỢP ĐỒNG của repo giọng (`voice_studio.API_VERSION`, vd "1.0.0") — None nếu chưa cài
    hoặc bản quá cũ chưa khai. Đây là nghĩa của khoá `engine.voice_studio` ở MỌI JSON kết quả
    (repo giọng tự trả đúng nghĩa đó ở `speak`/`narrate`); bản phát hành đi khoá riêng
    `engine.voice_studio_version` — xem docs/CONTRACT.md §2."""
    try:
        return getattr(importlib.import_module("voice_studio"), "API_VERSION", None)
    except ImportError:
        return None


def _args(argv, parser_factory):
    """Namespace tham số cho `voice_studio.narrate`.

    Ưu tiên parser CỦA CHÍNH repo giọng: nó biết mặc định của bản đang cài (ngôn ngữ, seed,
    chuẩn RMS), nên bản mới thêm tham số có mặc định vẫn chạy. Bản không có `build_parser`
    thì dựng Namespace tối thiểu.
    """
    if parser_factory is not None:
        try:
            return parser_factory().parse_args(argv)
        except SystemExit as e:
            # argparse thoát bằng `SystemExit`, mà `SystemExit` là `BaseException`: nó KHÔNG
            # bị `contract.run` bắt (`contract.py` bắt `Exception`). Nên một bản
            # `agent-voice-studio` lệch cờ làm `narrate --json` thoát 2 mà KHÔNG có dòng JSON
            # nào — bên gọi đọc dòng cuối stdout theo hợp đồng thì vỡ, không đọc được lỗi.
            # Đổi thành `ContractError`: vẫn mã 2, nhưng đi qua đường hợp đồng.
            raise ContractError(
                "bản `agent-voice-studio` đang cài không nhận bộ cờ này "
                f"(argparse thoát {e.code}): " + " ".join(argv)) from e
    ns = argparse.Namespace(video=None, out=None, text=None, file=None, mode="fit", bgm=None,
                            bgm_volume=None, profile=None, instruct=None, lang=None, speed=None,
                            seed=None, normalize=False, json=False)
    it = iter(argv)
    for tok in it:
        key = tok.lstrip("-").replace("-", "_")
        if key == "normalize":
            ns.normalize = True
        else:
            setattr(ns, key, next(it))
    return ns


def narrate(video, out, *, text=None, file=None, profile=None, instruct=None, lang=None,
            speed=None, seed=None, normalize=False, mode="fit", bgm=None, bgm_volume=None):
    """Lồng giọng vào `video` → `out`. -> dict kết quả của repo giọng.

    `bgm`: tên style / đường dẫn file / "none" để tắt / None = theo cấu hình trạm giọng.
    """
    vn = module("narrate")
    argv = ["--video", str(video), "--out", str(out)]
    if file:
        argv += ["--file", str(file)]
    else:
        argv += ["--text", text or ""]
    argv += ["--mode", mode]
    for flag, val in (("--profile", profile), ("--instruct", instruct), ("--lang", lang),
                      ("--speed", speed), ("--seed", seed), ("--bgm", bgm),
                      ("--bgm-volume", bgm_volume)):
        if val is not None and val != "":
            argv += [flag, str(val)]
    if normalize:
        argv.append("--normalize")
    return vn.narrate(_args(argv, getattr(vn, "build_parser", None)))


def mix_bgm(path, style=None, volume=None):
    """Trộn nhạc nền dưới track giọng sẵn có của `path` (ghi đè tại chỗ). -> True nếu đã trộn.

    `style` None/"none" ⇒ không trộn gì (khác với repo giọng, nơi None nghĩa là "theo biến môi
    trường"): ở đây nhạc nền là một khoá CỦA SPEC, spec không khai thì không được có nhạc.
    """
    if style is None or str(style).strip().lower() in ("", "none", "off"):
        return False
    av = module("av")
    return bool(av.mix_bgm(str(path), bgm=str(style), volume=volume))


# ── Lời đọc có marker sắc thái ─────────────────────────────────────────────────────────────
# `[ten-marker]` trong lời đọc đổi clip tham chiếu của profile (skill `voice-routing`,
# `profile-and-markers.md`). Chỉ `voice_studio.lab.vlab.synth` hiểu nó; `engine.synth` và
# `model.generate` KHÔNG: gửi chúng một chuỗi có `[hao-hung]` là bị đọc thành tiếng. Mọi template
# bản tin tổng hợp qua `synth_text`/`synth_sentences` dưới đây, không gọi engine trực tiếp.

DEFAULT_SEED = 42            # cùng giá trị với `voice_studio.speak.DEFAULT_SEED`
_BRACKET = re.compile(r"\[([A-Za-z0-9][A-Za-z0-9\-]*)\]")
# 13 thẻ phi ngôn ngữ gốc của engine (bản sao của `vlab.NATIVE_TAGS`, chỉ dùng khi chưa cài repo giọng).
_NATIVE_FALLBACK = frozenset({
    "laughter", "sigh", "confirmation-en", "question-en", "question-ah", "question-oh",
    "question-ei", "question-yi", "surprise-ah", "surprise-oh", "surprise-wa", "surprise-yo",
    "dissatisfaction-hnn"})


def _native_tags():
    try:
        return frozenset(module("lab.vlab").NATIVE_TAGS)
    except StationMissing:
        return _NATIVE_FALLBACK


def strip_markers(text, keep_native=False):
    """Gỡ MỌI `[tên]` khỏi lời đọc để HIỂN THỊ (phụ đề, gạch đầu dòng, transcript).

    `keep_native=True` giữ thẻ gốc của engine (`[laughter]`…) — dùng khi đưa chữ cho engine đọc,
    không phải khi vẽ lên màn hình. Marker nằm giữa hai từ thì chừa đúng một dấu cách.
    """
    if not text or "[" not in text:
        return text or ""
    native = _native_tags() if keep_native else frozenset()

    def _drop(m):
        return m.group(0) if m.group(1).lower() in native else " "

    return re.sub(r"[ \t]{2,}", " ", _BRACKET.sub(_drop, text)).strip()


class MarkedVoice:
    """Một giọng đã chọn: tên profile (để biết marker nào hợp lệ) + clone prompt trung tính.

    `synth_text` thấy kiểu này thì đi đường marker-aware. Prompt trần (kiểu cũ) vẫn chạy nhưng
    chỉ bằng clip trung tính và marker bị gỡ — an toàn, không đổi sắc thái.
    """
    __slots__ = ("name", "prompt", "seed")

    def __init__(self, name, prompt=None, seed=DEFAULT_SEED):
        self.name, self.prompt, self.seed = name, prompt, seed

    def __repr__(self):
        return f"MarkedVoice({self.name!r}, seed={self.seed!r})"


def resolve_profile(name=None):
    """Tên profile dùng được (`name` hoặc profile mặc định của trạm); không lùi về giọng ngẫu nhiên."""
    return module("profiles").ensure_default(name=name or None)


def load_voice(model, name=None, seed=DEFAULT_SEED):
    """-> `MarkedVoice` cho `name` (rỗng = profile mặc định của trạm). `seed=None` = chạy tự do."""
    resolved = resolve_profile(name)
    return MarkedVoice(resolved, module("profiles").get_clone_prompt(model, resolved), seed)


def _name_seed(voice):
    if isinstance(voice, MarkedVoice):
        return voice.name, voice.seed
    if voice is None or isinstance(voice, str):
        return resolve_profile(voice), DEFAULT_SEED
    return None, None                       # prompt trần kiểu cũ


def _to_array(audio):
    import numpy as np
    return np.asarray(audio, dtype=np.float32)


def synth_text(model, text, voice, *, language="Vietnamese"):
    """Tổng hợp một khối lời đọc (nhiều câu, nhiều marker được) -> mảng float32.

    `voice`: `MarkedVoice` · tên profile (chuỗi) · None (= profile mặc định) · clone prompt trần.
    Ba dạng đầu qua `vlab.synth`: tách theo marker, mỗi đoạn dùng clip của marker đó, marker lạ bị
    gỡ. Dạng cuối (kiểu cũ) gỡ hết marker rồi đọc bằng clip trung tính.
    """
    name, seed = _name_seed(voice)
    if name is not None:
        audio, _sr, _log = module("lab.vlab").synth(model, text, name, language=language, seed=seed)
        return _to_array(audio)
    audio, _sr = module("engine").synth(strip_markers(text, keep_native=True), prompt=voice,
                                        language=language, model=model)
    return _to_array(audio)


def _split_plain(text):
    parts = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", text or "") if s.strip()]
    return parts or ([text.strip()] if (text or "").strip() else [])


def synth_sentences(model, text, voice, *, language="Vietnamese"):
    """Như `synth_text` nhưng trả `[(câu_hiển_thị, audio)]` — để canh phụ đề theo từng câu.

    Marker có hiệu lực tới marker kế tiếp, qua cả ranh giới câu; `câu_hiển_thị` đã gỡ marker.
    """
    name, seed = _name_seed(voice)
    if name is None:
        return [(s, synth_text(model, s, voice, language=language))
                for s in _split_plain(strip_markers(text, keep_native=True))]
    vlab = module("lab.vlab")
    profile = vlab.load_profile(name)
    known = set(profile["variants"].keys()) if profile else set()
    spans, _unknown = vlab.split_by_marker(text, known)
    out = []
    for marker, chunk in spans:
        for sent in vlab.split_sentences(chunk):
            marked = f"[{marker}] {sent}" if marker else sent
            audio, _sr, _log = vlab.synth(model, marked, name, language=language, seed=seed)
            out.append((strip_markers(sent), _to_array(audio)))
    return out
