# Baseline và lượt chạy thử

Not agent instructions.

## Baseline không-skill: NOT RUN

Chưa chạy phiên mô hình không có skill cho các case.

## Lượt chạy CÓ skill (2026-11-23, Sonnet, subagent)

- Case: `vlog-design-edge` (không clip, lời thoại `fixtures/script-weekly-report.md`, avatar giả định có lời đồng ý).
- Phạm vi: bước 0–5; không dựng khung, không tải tài nguyên, không gọi mạng.
- Kết quả: ra đủ `brief.md`, `clips.md`, `beats.md`, `pacing.md`, `STORYBOARD.md`, `assets/MANIFEST.md` trong project thử ở trạm.
- `pace_check --profile presenter`: thoát 0 lần đầu, 12 cảnh · 90 s · TB 7.5 s/cảnh · 5 lần đổi chế độ · người 86.6% (P 11.1, PA 41.1, PS 34.4, A 13.3).
- Phản hồi của lượt chạy dẫn tới các sửa: pill bước thay thẻ chương cho video ngắn, lý do trần 90%, ranh giới mẫu storyboard chung (ba draft chỉ ở bước 7, gộp trường cho ≤ 15 cảnh), chỗ người trong LY-08, quy ước đếm âm tiết từ ngoại, dòng take avatar, hình thay thế cho stinger.
- Chưa chấm theo rubric bởi người chấm độc lập.
