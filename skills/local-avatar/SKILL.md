---
name: local-avatar
description: Use when someone asks to make their own photo or footage speak with recorded audio, change the words in a talking head, or verify a local Windows MuseTalk avatar render.
---

# Avatar nói bằng MuseTalk

1. Chốt ảnh hoặc footage một người và WAV mà người dùng có quyền sử dụng. Ưu tiên footage gần chính diện, rõ miệng và 25 fps. Với tư liệu riêng, dùng bản cục bộ trong trạm video. Nếu đầu vào ở ngoài trạm, dùng bản sao đã được cho phép trong project. Với tệp chỉ có trên cloud, hỏi người dùng đặt bản local.
2. Chạy `video-studio avatar doctor --json`. Mã 3 là thiếu runtime, model hoặc công cụ. Nếu đã được giao cài, theo quy trình trong `docs/MUSETALK.md` ở gốc repo.
3. Gọi `video-studio avatar render --source <ảnh-hoặc-video> --audio <WAV> --out <MP4-mới> --json`. Lệnh này dùng engine avatar riêng. Dịch vụ ngoài máy chỉ được dùng khi người dùng giao rõ việc gửi dữ liệu.
4. Soi chân dung, vùng môi và các điểm đổi hướng chuyển động. Kiểm cả thời lượng và âm thanh nguồn trong MP4. Với bài nói, nghe và xem các mốc mở đầu, chuyển tiếp, cuối đoạn. Lưu MP4 ở trạm video.
