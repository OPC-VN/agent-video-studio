---
name: line-art-motion
description: Use when creating seekable procedural line-art characters or hanging objects with gait, wind, ink, day-night color or draw-on in HyperFrames. Not for lyric typography or icons beside lyrics (lyric-video-effects), photo overlays (photo-ambient-effects), reference selection (video-theme-library), or general animation (hyperframes-animation).
---

# Hoạt họa nét mực thủ tục

Dùng các module trong `assets/` cho cảnh SVG tự vẽ. Cấp cả `line-art.mjs` và module component cùng thư mục; mỗi component import helper tương đối. Công cụ materialize một file chưa tự cấp helper.

Tạo DOM bằng `mount` một lần, sau đó gọi `render(t)` bằng thời gian tuyệt đối của timeline paused. Không đặt filter lên nền giấy; `ink-scene` yêu cầu nhóm nét có thuộc tính `data-ink-layer`. Nét vẽ dần nhận phần tử thực và thời điểm bắt đầu, thời lượng dương.

Không dùng đồng hồ thực, ngẫu nhiên không seed, vòng tự chạy, sự kiện con trỏ hoặc mạng trong trạng thái cảnh.

Chân đứng không trượt khi nhân vật tiến với `groundSpeed`; ở helper `gait`, thay tốc độ bằng stride hoặc period, không thay tốc độ nhân vật riêng. `createWalker` hiện chỉ chọn preset, chưa nhận stride/period tùy chỉnh. Khi chân không với tới mục tiêu, hình học kẹp về tầm chi và không còn bảo đảm chạm đất. Mỗi `filterId` phải duy nhất trong toàn document.

Chạy `node --test tests/line-art.test.cjs` và render cảnh thực trước khi nghiệm thu. Bộ số học không thay cho kiểm tra hình và khả năng nạp module của engine.

Chi tiết: [phong cách](references/style.md), [dáng đi](references/gait.md), [vật lý](references/seek-safe-physics.md), [kiểm tra](references/verify.md), [thẻ component](references/component-cards.md).
