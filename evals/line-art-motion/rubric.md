# Tiêu chí đánh giá định tuyến

Mỗi ca chạy riêng với prompt và fixtures đã ghi; không cung cấp nhãn kỳ vọng cho mô hình.

- Ca dương đạt khi chọn `line-art-motion` cho nhân vật hoặc vật nét mực chuyển động thủ tục, có thể tua theo thời gian.
- Ca âm đạt khi không chọn skill này và chuyển đúng nhu cầu sang `lyric-video-effects`, `photo-ambient-effects` hoặc `video-theme-library` tương ứng.
- Ghi lựa chọn thực tế, giải thích ngắn và kết quả từng ca. Không suy kết quả từ kiểm tra tĩnh; khi chưa chạy mô hình giữ `not_run`.
