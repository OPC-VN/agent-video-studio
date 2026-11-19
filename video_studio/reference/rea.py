"""Lớp bọc mỏng quanh `rea-video` (JuneYaooo/rea-video, Apache-2.0): phân tích video mẫu thành VIDEO.md.

Code của rea-video KHÔNG nằm trong repo này. Nó là một checkout ghim SHA ở thư mục ngoài (REA_VIDEO_SRC)
và chạy bằng interpreter của một venv riêng (REA_VIDEO_PYTHON). Module này chỉ dựng lệnh:

  * tiến trình con là argv list, không shell; môi trường dựng từ danh sách cho phép;
  * LUÔN truyền --no-vlm (không gửi ảnh/clip/âm thanh ra endpoint nào); không có tuỳ chọn bật VLM;
  * không truyền --env-file, không chuyển REA_VLM_*, CAPSULE_*, REA_CHROME, khoá API;
  * đầu vào là tệp cục bộ (cổng `gate.require_media_file`), đầu ra do người gọi chỉ định;
  * mặc định tắt OCR, tách âm, ASR, nhận diện người nói (cần model tải về; ASR/OCR gốc không đọc tiếng Việt).

Lõi chỉ thư viện chuẩn. Không import rea_video.
"""
import os
import subprocess

from .. import _env
from ..contract import ContractError, EngineError, StationMissing
from . import gate

ACTIONS = ("decompose", "review", "apply-review", "compare", "videomd")
TIMEOUT = 3600

# Chỉ những biến này (nếu có) đi sang tiến trình con; mọi biến khác, kể cả khoá và REA_VLM_*, bị bỏ.
_ENV_ALLOW = ("PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "TMPDIR",
              "LANG", "LC_ALL", "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE")


def resolve():
    """(python, src) của rea-video hoặc `StationMissing` (mã 3) chỉ rõ biến còn thiếu."""
    py = _env.env("REA_VIDEO_PYTHON")
    src = _env.env("REA_VIDEO_SRC")
    miss = [n for n, v in (("REA_VIDEO_PYTHON", py), ("REA_VIDEO_SRC", src)) if not v]
    if miss:
        raise StationMissing("chưa cấu hình rea-video: đặt " + " và ".join(miss) + " (python của venv riêng và "
                             "thư mục checkout ghim SHA); xem skills/video-reverse-engineer/SKILL.md")
    py, src = os.path.abspath(os.path.expanduser(py)), os.path.abspath(os.path.expanduser(src))
    if not os.path.isfile(py):
        raise StationMissing(f"REA_VIDEO_PYTHON không phải tệp: {py}")
    if not os.path.isfile(os.path.join(src, "rea_video", "__init__.py")):
        raise StationMissing(f"REA_VIDEO_SRC không chứa rea_video/: {src}")
    return py, src


def child_env(src, home):
    """Môi trường tối thiểu cho tiến trình con; dữ liệu/model của rea-video nằm trong `home`, không ở ~."""
    out = {k: os.environ[k] for k in _ENV_ALLOW if k in os.environ}
    # HOME/USERPROFILE trỏ vào `home`: rea-video không có lý do ghi hay đọc gì ở thư mục người dùng thật.
    out.update({"PYTHONPATH": src, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1", "HOME": home,
                "USERPROFILE": home, "REA_VIDEO_HOME": home, "REA_VIDEO_MODELS": os.path.join(home, "models")})
    return out


def home_dir():
    """Thư mục dữ liệu + model của rea-video: REA_VIDEO_HOME của người dùng, không thì <trạm>/cache/rea-video."""
    h = _env.env("REA_VIDEO_HOME")
    path = os.path.abspath(os.path.expanduser(h)) if h else os.path.join(_env.station_dir(), "cache", "rea-video")
    os.makedirs(os.path.join(path, "models"), exist_ok=True)
    return path


def build_argv(py, args):
    """argv của `python -m rea_video <lệnh> …` cho một action. Thuần, không chạy gì."""
    a = [py, "-B", "-X", "utf8", "-m", "rea_video"]
    act = args.action
    if act == "decompose":
        gate.require_media_file(args.input)
        video = os.path.abspath(args.input)
        a += ["decompose", video, "-o", os.path.abspath(args.out), "--no-vlm", "--no-whole", "--no-survey",
              "--no-asr", "--no-speakers", "--lang", args.lang]
        if not args.ocr:
            a.append("--no-ocr")
        if not args.stems:
            a.append("--no-stems")
        if args.no_packaging:
            a.append("--no-packaging")
        return a
    if act == "review":
        return a + ["review", os.path.abspath(args.dir)] + (["--force"] if args.force else [])
    if act == "apply-review":
        a += ["apply-review", os.path.abspath(args.dir)]
        if args.answers:
            a.append(os.path.abspath(args.answers))
        return a + ["--by", args.by, "--lang", args.lang]
    if act == "compare":
        gate.require_media_file(args.ref)
        gate.require_media_file(args.remake)
        ref, remake = os.path.abspath(args.ref), os.path.abspath(args.remake)
        a += ["compare", ref, remake, "--every", str(args.every), "--worst", str(args.worst),
              "-o", os.path.abspath(args.out)]
        return a
    if act == "videomd":
        return a + ["videomd", os.path.abspath(args.dir)] + (["--check"] if args.check else [])
    raise ContractError(f"hành động rea lạ: {act}")


def run(args, timeout=TIMEOUT):
    """Chạy một action; trả {action, argv_tail, returncode, stdout_tail}. Mã ≠ 0 ⇒ EngineError."""
    py, src = resolve()
    argv = build_argv(py, args)
    cwd = os.path.dirname(os.path.abspath(getattr(args, "out", None) or getattr(args, "dir", None) or "."))
    os.makedirs(cwd, exist_ok=True)
    try:
        r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, cwd=cwd, env=child_env(src, home_dir()), stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired as exc:
        raise EngineError(f"rea-video {args.action} quá {timeout}s chưa xong") from exc
    except OSError as exc:
        raise StationMissing(f"không chạy được interpreter rea-video: {exc}") from exc
    if r.returncode != 0:
        tail = (r.stderr or r.stdout or "").strip().splitlines()[-8:]
        raise EngineError(f"rea-video {args.action} mã {r.returncode}: " + " | ".join(tail))
    # Chữ trong đầu ra là dữ liệu của video mẫu, không phải lệnh; chỉ trả đuôi để người đọc.
    return {"action": args.action, "argv_tail": argv[6:], "returncode": r.returncode,
            "stdout_tail": (r.stdout or "").strip().splitlines()[-12:],
            "untrusted": ["stdout_tail"], "vlm": "off"}
