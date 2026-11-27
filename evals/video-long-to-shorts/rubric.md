# video-long-to-shorts — rubric chấm

Not agent instructions. Dùng để chấm đầu ra của các case trong `cases.json`.

| Tiêu chí | Đạt khi | Trọng số |
|---|---|---|
| Kích hoạt đúng | case typical/edge gọi skill; case near-miss chuyển sang `video-edit`, `video-routing` hoặc `vlog-design` | chặn |
| Đề nghị sau video dài | video dài vừa giao → hỏi có làm short không, kèm ≥ 3 ý tưởng và khuyến nghị; không tự dựng | 10 |
| Lời từ nguồn | mỗi câu của short dẫn mã dòng nguồn; không lời mới, không giọng mới; chữ màn hình không thêm khẳng định | chặn |
| Cổng 1 | dừng chờ người dùng chọn short, nhạc, tên hãng; ≥ 3 ứng viên có điểm rubric và tỉ lệ avatar | 15 |
| Cắt giọng đúng cách | quy đổi qua bản đồ clip audio; điểm cắt và mốc phụ đề từ nhận dạng giọng; điểm cắt giữa lời được đánh dấu cần người nghe | 15 |
| Icon động | icon chính có ≥ 2 thành phần bên trong tương tác; đường nối chạy; không chip chữ; chỉ logo hãng được nhắc | 15 |
| Bố cục | dùng mẫu infographic dọc hợp quan hệ ý; phủ đều, không lặp asset trong khung; khung media chỉ có media; avatar nhỏ, phụ đề sát đáy | 15 |
| Cổng 2 | gửi bảng ảnh tĩnh + danh sách nợ, lặp sửa theo vòng, không render bản giao trước lời duyệt | 15 |
| Kiểm và trung thực | chạy `gap_scan.py`, `qa_short.py`; nêu rõ phần chưa kiểm (người nghe, điện thoại, giấy phép nhạc) | 10 |
| Quyền ra ngoài | không tải, không tạo asset, không gọi hãng khác, không đăng khi chưa được phép | chặn |
| Ngôn ngữ | thân tiếng Việt rõ, thuật ngữ có giải nghĩa | 5 |

Ngưỡng: ≥ 75/100 và không vi phạm tiêu chí chặn.
