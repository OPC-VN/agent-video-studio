# Top Story hai cột

Chọn `top_story.visual_layout: image-right` khi brief yêu cầu ảnh ở bên phải trong cả 16:9 và 9:16.
Mỗi cảnh có tiêu đề và các bước infographic ở bên trái. Ảnh hiển thị suốt cảnh, còn thẻ và icon
lần lượt xuất hiện bằng timeline HyperFrames. Layout mặc định của Top Story tiếp tục dùng được
cho spec chưa khai trường này.

## Hợp đồng đầu vào

- Nếu kênh có logo, khai `brand.logo` bằng đường dẫn PNG, JPEG hoặc WebP cục bộ.
  Thanh thương hiệu trên cả hai tỷ lệ dùng ảnh này. Runner chiến dịch lấy từ
  `campaign.md: identity.logo`, với đường dẫn tương đối tính từ thư mục kênh.
- Giữ lời đọc trong `intro`, `intro_short`, `outro`, `outro_short` và các trường lời đọc trong chương.
- Khai `cover_visual`, từng phần trong `sections` và `outro_visual` theo cùng khuôn hình.
  Đường ảnh tương đối tính từ thư mục chứa spec, tránh thư mục media tạm của project.
- `diagram.items` nhận 2–4 hành động. Icon hiện có gồm `search`, `profile`, `chat`, `chart`, `edit`,
  `check`, `handoff`, `list`, `shield`. Dùng nhãn hành động ngắn trong bản dọc.

```json
{
  "title": "Đọc tín hiệu để sửa nội dung",
  "media": [{"type": "image", "src": "assets/dashboard.png"}],
  "media_alt": "Ảnh màn hình bảng tín hiệu tương tác",
  "media_credit": "Ảnh · Tổ chức phát hành",
  "diagram": {
    "type": "process",
    "items": [
      {"t": "Quan sát", "d": "Khách hay hỏi gì?", "icon": "chart"},
      {"t": "Bổ sung", "d": "Sửa tài liệu nguồn", "icon": "edit"},
      {"t": "Kiểm lại", "d": "Hỏi lại như khách", "icon": "check"}
    ]
  }
}
```

Engine kiểm dữ liệu ảnh và thẻ trước TTS. Ở lớp chuẩn bị chiến dịch, tự xác minh nội dung và quyền
dùng của ảnh, so trùng với số trước và giữ lượt nếu thiếu ảnh. Xem MP4 cả hai tỷ lệ sau render,
tại đầu cảnh và sau khi thẻ cuối xuất hiện.
