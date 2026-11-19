# Cài rea-video cho `video-reverse-engineer` (ghim SHA, venv riêng, không build)

Mục tiêu: có `REA_VIDEO_PYTHON` + `REA_VIDEO_SRC` mà **không chạy bước build/postinstall của repo ngoài**.
Làm theo `opcos-core:adopt-repo` (inspect trước, cổng người trước khi chạy code ngoài).

## 1. Nguồn ghim (không phải `pip install git+…`)

```bash
git clone -c core.hooksPath=NUL -c core.symlinks=false --depth 1 --no-checkout https://github.com/JuneYaooo/rea-video <đích>
cd <đích> && git sparse-checkout init --no-cone     # chỉ phạm vi đã quét (xem upstream.json: install_scope)
git fetch --depth 1 origin ac470773188574833b839be17abee6162201ddf9 && git checkout --detach ac470773188574833b839be17abee6162201ddf9
git config --local core.hooksPath NUL               # đặt lại sau khi clone
```

Phạm vi giữ: `rea_video/*.py`, `rea_video/aspects/`, `rea_video/capabilities/`, `docs/{decompose,replicate,videomd,what-it-detects}.md`,
`docs/dev/`, `skills/rea-video/{SKILL.md, references/*.md trừ chatcut·capsule-cinema·setup}`, `scripts/{bench_*,validate_capabilities}.py`, `eval/`, LICENSE, NOTICE.
**Loại:** `rea_video/integrations/` (capsule-cinema), `references/chatcut.md` (chỉ dẫn `curl | sh` cài app thương mại),
`scripts/install_skill.sh`, `i18n/`, `README.md`, `docs/cases/` (media demo), `setup.md` (cài `git+https` không ghim).

## 2. Venv riêng, chỉ wheel (không chạy sdist/build)

```bash
python -m venv <runtime>/venvs/agent-video-studio/rea-video
<venv>/Scripts/python -m pip install --only-binary=:all: "numpy>=1.24,<3" "opencv-python-headless>=4.8,<5" \
  "Pillow>=9" "PyYAML>=6" "videomd==1.2.0" "onnxruntime>=1.16" "jsonschema>=4.18"
```

Không `pip install` chính gói `rea-video` (setuptools build + `readme` ngoài phạm vi): chạy từ nguồn bằng `PYTHONPATH`.
`videomd` là gói bên thứ ba (Apache-2.0, 3 module thuần Python, soát tay không có gọi mạng/tiến trình).
Khoá phiên bản: `locks/rea-video-windows.txt` (đã đo 19/11/2026: numpy 2.5.5, opencv-python-headless 4.14.0.94, onnxruntime 1.32.0, videomd 1.2.0).

## 3. Biến môi trường

```
REA_VIDEO_PYTHON=<venv>/Scripts/python.exe
REA_VIDEO_SRC=<đích clone>
REA_VIDEO_HOME=<nơi đặt dữ liệu + model>   # mặc định <trạm>/cache/rea-video
```

Lớp bọc đặt `HOME`/`USERPROFILE` của tiến trình con vào `REA_VIDEO_HOME` và **không chuyển** `REA_VLM_*`, `CAPSULE_*`,
`REA_CHROME`, khoá API.

## 4. Tải model lần đầu (chỉ khi cần, có sha256 cố định theo upstream)

| Model | Khi nào tải | Dung lượng |
|---|---|---|
| YuNet (mặt) | tự tải khi `decompose` (đã chạy trong lần thử) | ~230 KB |
| UVR MDX-Net + BandIt (tách giọng/nhạc/âm) | chỉ khi `--stems` | ~216 MB |
| SenseVoice, diarization | không dùng (không có tiếng Việt) | — |

## 5. Kiểm

```bash
video-studio reference decompose --input <clip> --out <dir> --json    # exit 0
video-studio reference videomd --dir <dir> --check --json             # "符合 VIDEO.md 规范"
python -m pytest -q tests/test_rea_wrapper.py                         # lớp bọc, không cần mạng
```
