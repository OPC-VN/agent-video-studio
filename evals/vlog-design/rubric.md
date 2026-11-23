# vlog-design — rubric chấm

Not agent instructions. Dùng để chấm đầu ra của các case trong `cases.json`.

| Tiêu chí | Đạt khi | Trọng số |
|---|---|---|
| Kích hoạt đúng | case typical/edge gọi skill; case near-miss chuyển sang `video-cleanup`/`video-edit` | chặn |
| Beat trước hình | có bảng beat (loại ý, giây ước) trước khi chọn bố cục | 15 |
| Mã mẫu | mỗi cảnh có chế độ + LY + TR, phần lớn có VO/TX/IG; mã tồn tại trong thư viện | 20 |
| Biên đạo | mỗi cảnh có trước → sau theo giây, thứ tự hiện khớp lời | 15 |
| Nhịp | `pace_check.py` thoát 0 hoặc mọi cảnh báo có lý do | 15 |
| Manifest | đủ icon/người/ảnh/font/màu/motion/clip; mỗi dòng có nguồn + giấy phép + trạng thái | 15 |
| Trung thực | không bịa cảnh quay thật, thiếu clip ghi «chưa có»/shot list; không chép hình video mẫu | chặn |
| Cổng duyệt | dừng ở khung hình chính chờ người dùng, không tự dựng cả video | 10 |
| Ngôn ngữ | thân tiếng Việt rõ, thuật ngữ có giải nghĩa | 10 |

Ngưỡng: ≥ 75/100 và không vi phạm tiêu chí chặn.
