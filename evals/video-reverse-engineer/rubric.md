# video-reverse-engineer — rubric chấm

Not agent instructions. Dùng để chấm đầu ra của các case trong `cases.json`.

| Tiêu chí | Đạt khi | Trọng số |
|---|---|---|
| Chọn nhánh đúng | bộ nhiều video dài → corpus-study; một video ngắn → decompose + review; cắt ghép → không dùng skill | chặn |
| Quyền và danh tính | hỏi trước khi gửi khung có mặt người thật; thư viện không tên kênh/người/đường dẫn máy; không chép hình | chặn |
| Số do máy tính | tỉ lệ, số đếm lấy từ `corpus_extract.py stats`; không mốc vượt thời lượng | 25 |
| Soi dày đủ chiều | mỗi kiểu đổi chế độ chính có mốc đo cả hai chiều; số lưới = số dòng ghi chép | 25 |
| Mẫu đủ trường | trông thế nào · chuyển động · khi dùng · tránh · bằng chứng · gợi ý dựng; nhãn đo/ước/suy ra | 25 |
| Kiểm chứng | rút ≈ 10% mẫu đối chiếu khung; có review độc lập trước khi dùng | 25 |

Ngưỡng: ≥ 75/100 và không vi phạm tiêu chí chặn.
