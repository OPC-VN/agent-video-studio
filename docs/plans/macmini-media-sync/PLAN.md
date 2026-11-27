---
title: PLAN — macmini-media-sync (video side — asset-first production)
date: 2026-11-25
revision: 3
status: draft_waiting_owner_decisions
master: agent-marketing-team/docs/plans/macmini-media-sync/PLAN.md
executor: Codex (branch macmini-media-sync, PR, CI Windows + macOS)
evaluator: Claude
---

# PLAN — macmini-media-sync · phần video: rà tài nguyên trước khi dựng

> Kế hoạch chủ (mục tiêu, pha, cổng, bảo vệ dữ liệu Mac, đăng bài): `agent-marketing-team/docs/plans/macmini-media-sync/PLAN.md`. File này chỉ nói repo video phải đổi gì và Codex cài đặt nó ra sao trên Mac mini.

## 0. Mục tiêu của repo video trong kế hoạch

1. **Đóng gói xuống Mac:** bản `main` mới nhất (0.10.1 + skill video-long-to-shorts sau khi push) cài song song ở `~/Studio-next/agent-video-studio`, trạm video mới ở `~/Studio-next/workspaces/video`, chạy được trên macOS arm64.
2. **Dời rà soát lên trước:** thêm **cổng tài nguyên** (S1b–S3) chặn ngay trước storyboard/render; bỏ kiểu rà video thành phẩm rồi bắt làm lại.
3. **Đóng gói thành phẩm có trạng thái** (S7 `READY`) để repo marketing đăng mà không cần nhìn lại tài nguyên.

## 1. Hiện trạng repo (đã đọc)

- CLI `video-studio`: `init, libs, doctor, render, edit, cleanup, reference, preview, avatar, narrate, migrate, uninstall` (`video_studio/cli.py`). **Không có** lệnh rà tài nguyên.
- Chuẩn mới ở dạng tài liệu: `skills/video-storyboard-design/references/motion-layout-standard.md` (17 mã CK-*, gồm CK-ICON-MOTION, CK-ICON-PARTS, CK-ICON-BASE, CK-LINK, CK-HASH), `storyboard-stills-first.md` (7 bước, chương ≥ 10 s, không im trước giọng), `creative-icon-brainstorm.md`. Chưa có code kiểm.
- Kiểm quyền/nguồn có sẵn để dùng lại: `video_studio/effect_library/catalog.py` (quyền owned/licensed + trường giấy phép), `video_studio/reference/fetch.py` (`_preflight`, tải mạng có hạn giờ).
- Template tin: `video_studio/templates/news/` (repo_today, news, news-weekly, topstory, daily_news_media, daily_hot_video) — dùng GSAP cục bộ: phải `video-studio libs fetch gsap --yes` trước render đầu tiên (thiếu → exit 3).
- `skills/video-long-to-shorts/scripts/qa_short.py` (exit 0/1/2, 3 khi thiếu ffmpeg) — chỉ có sau khi push `ac72677`.
- macOS: python3.12, Node ≥ 22, `ffmpeg-full` đứng đầu PATH, HyperFrames ghim 0.8.54 qua npx (`docs/INSTALL.md`). Lock chỉ có bản Windows; render arm64 bản hiện tại **chưa xác nhận**.

## 2. Thiết kế cổng tài nguyên

### 2.1 Tệp hợp đồng (đặt trong thư mục project của lượt dựng)

| Tệp | Ai ghi | Nội dung chính |
|---|---|---|
| `asset-requirements.json` | S1b (runner marketing hoặc agent viết kịch bản) | mỗi cảnh: `scene_id`, `role` (icon_motion, gif, news_image, logo, chart, footage), `required` true/false, mô tả cần tìm, `fallback` (tên tài nguyên dự phòng của kênh hoặc `text_only`) |
| `asset-manifest.json` | S2 (agent gom) | mỗi mục: `scene_id`, `role`, `path`, `source_url`, `rights` (owned / licensed / editorial-with-credit), `credit`, `sha256`, `width`, `height`, `mime`, `animated`, `fetched_at` |
| `asset-report.json` | S3 (lệnh máy) | từng mục `pass / fail / degraded` + lý do; tổng `status`: `ready / degraded / needs-human`; `attempt` hiện tại |

### 2.2 Lệnh mới

`video-studio assets check --project <dir> [--json]`
- Kiểm **tất định** (chặn thật): đủ mọi mục `required` theo `asset-requirements.json`; file mở được, đúng mime; độ phân giải tối thiểu theo vai trò (ví dụ ảnh tin ≥ 1280 px cạnh dài cho 16:9); `role=icon_motion|gif` phải có hoạt cảnh (gif/webp/lottie nhiều khung) — CK-ICON-MOTION; ảnh tin phải có `source_url` + `rights` + `credit` (dùng lại logic `effect_library/catalog.py`); không trùng `sha256` giữa các cảnh; icon thuộc bộ đã duyệt khi kênh khai (CK-ICON-BASE).
- Kiểm **khớp nội dung** (ảnh có đúng tin không) **không** nằm trong lệnh máy: agent gom (S2) tự chấm và ghi `match_note`; lệnh chỉ đọc cờ đó, không gọi model.
- Mã thoát theo hợp đồng CLI 0/1/2/3 (`docs/CONTRACT.md`): 0 = `ready` **hoặc** `degraded` (trạng thái nằm trong dòng JSON cuối, khoá `status`), 2 = `needs-human` (thiếu mục bắt buộc hoặc lỗi tất định), 3 = thiếu công cụ (ffprobe). Không thêm mã mới.
- Lõi chỉ dùng thư viện chuẩn (AGENTS.md §4): đọc kích thước/số khung qua `ffprobe` (argv list, không shell), không thêm Pillow.

`video-studio assets lock --project <dir>`: ghi `asset-manifest.lock` (sha256 của manifest + mọi file). Từ đây đổi tài nguyên = phải check lại.

### 2.3 Vòng làm lại có trần

- Runner gọi S2 → `assets check`. Kết quả `needs-human` do thiếu mục **bắt buộc** → gọi lại S2 chỉ cho mục thiếu, tối đa `runtime.asset_retry_max` (mặc định 2) lượt; bộ đếm `attempt` ghi trong `asset-report.json` nên khởi động lại không về 0.
- Mục **không bắt buộc** thiếu → thay `fallback`, ghi `degraded`, đi tiếp ngay, không vòng lại.
- Hết lượt mà vẫn thiếu mục bắt buộc → dừng job, `needs-human`, báo Telegram (qua runner marketing). **Không render, không đăng.**

### 2.4 Render từ chối khi chưa qua cổng

- `video-studio render` cho các template tin (và mọi template khai `requires_asset_gate: true`) kiểm có `asset-manifest.lock` khớp và `asset-report.json` ở `ready|degraded`; thiếu → exit 2 với thông báo rõ. Cờ `--skip-asset-gate` chỉ cho dựng thử tay, ghi cảnh báo vào output.
- Template đọc tài nguyên **chỉ** từ `asset-manifest.json` (không tự tải giữa lúc render).

### 2.5 Đóng gói S7

`video-studio package --project <dir> --out <chiến dịch>/out/<ngày>/package`:
- Kiểm kỹ thuật bằng máy (không có agent xem video): ffprobe độ dài, tỉ lệ khung (16:9 / 9:16), có âm thanh, `silencedetect` không im đầu > 0,5 s, chương ≥ 10 s khi có chapters, file phụ đề có; với short dùng `qa_short.py` nếu có.
- Dựng trong `package.tmp-<id>/`, xong đổi tên nguyên tử sang `<id>/` với `package.json`: `state: READY`, `id`, băm video, băm manifest, tiêu đề, mô tả, thumbnail, chapters, cờ `degraded`, danh sách credit ảnh (để mô tả/bình luận ghi nguồn).
- Trượt kiểm kỹ thuật → `state: FAILED_QA`, không đăng; **không** quay lại S2.
- `package.tmp-*` quá 24 giờ → đổi thành `abandoned-<id>/` (không xoá).

## 3. Áp dụng skill và template mới

| Việc | Chi tiết |
|---|---|
| Storyboard ảnh tĩnh trước | Job tự động: thay "dừng duyệt người" bằng kiểm máy CK-* làm được bằng code (bắt đầu với CK-ICON-MOTION, CK-HASH, chương ≥ 10 s, không im trước giọng); các CK còn lại ghi `manual` trong báo cáo |
| Icon động | S2 phải lấy icon có hoạt cảnh (gif/lottie) theo `creative-icon-brainstorm.md`; cổng S3 chặn icon tĩnh ở vai trò `icon_motion` |
| Marker giọng | Template tin đọc lời có marker sắc thái qua trạm voice (đã có từ 0.10.0); không đổi |
| Short 9:16 | Dùng skill video-long-to-shorts sau khi push; short từ video dài cũng đi qua `package` |
| Adapter skill | Sau khi cài/kéo bản mới trên Mac: `python scripts/build_host_adapters.py` để Codex/Claude thấy skill mới |

## 4. Việc trong repo video

Repo video có 7 **việc** (TK) trong kế hoạch này:

| Mã | Việc | Kiểm |
|---|---|---|
| TK-V1 — Lược đồ 3 tệp hợp đồng | JSON schema + ví dụ trong `docs/` và `samples/` | test đọc/ghi schema |
| TK-V2 — `assets check` | mục 2.2, mã thoát | test từng luật (icon tĩnh bị chặn, thiếu credit bị chặn, thiếu mục không bắt buộc → degraded) |
| TK-V3 — `assets lock` + render từ chối | mục 2.4 | test render exit 2 khi thiếu lock |
| TK-V4 — `package` | mục 2.5, đổi tên nguyên tử, FAILED_QA, abandoned | test với video mẫu ngắn (ffmpeg sinh) |
| TK-V5 — Template tin đọc từ manifest | sửa `templates/news/*` | test dựng spec từ manifest mẫu |
| TK-V6 — Tài liệu + skill | cập nhật `skills/video-routing`, `video-storyboard-design` trỏ cổng mới; `docs/CHANGELOG.md` | cổng chống rò `tests/test_no_identity_leak.py` xanh |
| TK-V7 — macOS | thêm khoá `darwin` cho runtime nếu cần; CI macOS chạy test mới với `ffmpeg-full` | `.github/workflows/tests.yml` xanh 2 OS |

## 5. Cài trên Mac (Codex, pha P2 của kế hoạch chủ)

1. `git clone` repo vào `~/Studio-next/agent-video-studio` ở mốc ghi trong báo cáo P0.
2. Venv chung `~/Studio-next/.venv` (python3.12): `pip install -e ~/Studio-next/agent-video-studio` và `pip install -e "~/Studio-next/agent-voice-studio[engine]"` (theo `docs/INSTALL.md`).
3. Tắt telemetry HyperFrames theo `docs/INSTALL.md`; `npx --yes hyperframes@0.8.54 browser ensure`; `video-studio libs plan gsap` → `video-studio libs fetch gsap --yes`.
4. Trạm mới `~/Studio-next/workspaces/video` (`video-studio init` trỏ đúng thư mục **mới**, rỗng). Chép (`rsync -a`, không `--delete`) `assets/` từ trạm video cũ và asset dùng chung chủ máy chuyển sang; **không** `video-studio migrate` trên trạm cũ.
5. `video-studio doctor` exit 0; render một mẫu `news-mini` để xác nhận arm64 (ghi thời gian).
6. Sau khi PR của TK-V1…V7 được gộp: `git pull --ff-only` ở clone **mới**, chạy lại doctor + test.

## 6. Ngoài phạm vi repo video

Đăng bài, hàng chờ, Kira, lịch chạy: repo marketing. Giọng: repo voice.
