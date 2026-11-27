# Baseline và lượt chạy thử

Not agent instructions.

## Baseline không-skill: NOT RUN

Chưa chạy phiên mô hình không có skill cho các case.

## Lượt chạy CÓ skill: NOT RUN

Chưa chạy case nào với skill đã đóng gói. Chưa chấm theo rubric.

## Căn cứ hiện có (không phải lượt eval)

- Skill rút từ một đợt dựng tay ba short 9:16 (40,5 s, 46,5 s, 68,9 s) từ một video dài 9 phút, người duyệt đã duyệt đạt cả ba sau 2–4 vòng ảnh tĩnh. Đợt đó làm **trước** khi có skill, nên không chứng minh skill dẫn được agent khác tới cùng kết quả.
- Script của skill đã chạy lại trên nguồn thật của đợt đó: `source_map.py` ra cùng bản đồ (30 cảnh, 7 clip audio, 17 clip video, 220 dòng, 1.815 từ, mốc từ trùng hết) với bộ đọc viết tay; `cut_voice.py` ra cùng `media_in` / `short_in` và cùng offset avatar với bản cắt tay của một short (lệch mẫu lớn nhất 10/32.768); `qa_short.py` thoát 0 trên cả ba bản render (−14,1 LUFS, true peak −1,4 dBFS, tiếng đầu 0,30 s).
- `make_subs.py` chạy với bản nhận dạng giọng thật của một short ra đúng 38/38 cụm phụ đề và 164 mốc từ của bản làm tay (lệch lớn nhất 0,00 s).
- `gap_scan.py` mới chỉ chạy trên fixture tổng hợp của bộ test (đợt dựng tay chưa ghi `layout.json`); `assets/templates/short-frame.html` chưa qua lượt render nào.
