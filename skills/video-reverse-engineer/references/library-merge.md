# Gộp mẫu từ một hoặc nhiều video vào thư viện vlog-design

> **Kết luận:** mỗi video học xong ra **một gói mẫu** (`assets/reference-patterns.md`); gói được gộp dần vào thư viện của skill `vlog-design` theo hợp đồng `skills/vlog-design/references/library-contract.md`. Không ai ghi thẳng vào thư viện; danh sách mã mới phải được người dùng duyệt.

## Contents
- Hai đường vào
- Bước 1 — Lập gói mẫu cho mỗi video
- Bước 2 — Đối chiếu với bảng mã
- Bước 3 — Kiểm chứng trước khi gộp
- Bước 4 — Gộp
- Bước 5 — Cập nhật số và kiểm máy
- Ai làm gì

## Hai đường vào

| Đường | Khi nào | Nguồn cho gói mẫu |
|---|---|---|
| **Một video** | học thêm một video mẫu, hoặc vừa mổ xẻ một video để phục dựng | `decompose` (`VIDEO.md`, `video/rhythm.md`, `timeline.md`, `sound.md`, `packaging.md`) + `review` + `reference-map.md` (skill `video-reference-analysis`); thêm soi dày ở chỗ đổi chế độ bằng `corpus_extract.py strips` |
| **Nhiều video** | học cả một bộ cùng thể loại | `corpus-study.md` bước 1–4 (nhật ký cảnh, soi dày, `stats`) cho từng video |

Cả hai đường đều kết thúc ở bước 1 dưới đây: một gói mẫu mỗi video.

## Bước 1 — Lập gói mẫu cho mỗi video

- Chép mẫu `assets/reference-patterns.md` vào `<trạm>/library/<tên>/evidence/<video>/reference-patterns.md`; cấp mã video `Vnn` tiếp theo trong sổ mã ở `<trạm>/library/<tên>/README.md`.
- Điền mục 1 (số từ `stats`), mục 2 (mỗi mẫu xuất hiện có ý nghĩa một dòng), mục 6 (âm thanh từ `sound.md` hoặc nghe trực tiếp).
- Mốc từ `VIDEO.md` dạng `@N` là mốc chính xác (bậc «đo»); mốc từ lưới 2 s là «ước».
- Xong khi: mọi dòng có nhóm, mã khớp hoặc `XX-NEW-n`, loại mốc, nguồn.

## Bước 2 — Đối chiếu với bảng mã

- **Kiểm tỉ lệ khung trước:** thư viện bố cục là 16:9. Video tỉ lệ khác chỉ gộp các mẫu không phụ thuộc khung (TX, MO, AU, RC…); mẫu LY và số vị trí/kích thước của nó vào file riêng theo tỉ lệ (hợp đồng, mục Tỉ lệ khung).
- Mở `skills/vlog-design/references/pattern-index.md`, so từng dòng theo luật «khớp trước, tạo sau» của hợp đồng: khớp cả «trông thế nào» và «khi dùng» → mã cũ; cùng cấu trúc khác hình thức → biến thể `NNa`; không khớp → `XX-NEW-n` với đủ 9 trường ở mục 3.
- Ghi mục 4 (bằng chứng nâng bậc) và mục 5 (mâu thuẫn).
- Xong khi: không còn dòng nào chưa phân loại.

## Bước 3 — Kiểm chứng trước khi gộp

- Model mạnh rút ngẫu nhiên ≈ 10% dòng (tối thiểu 5), mở khung/lưới tại mốc, xác nhận mô tả và mã.
- Mọi `XX-NEW-n` và mọi đề xuất nâng lên «đo» đều phải được kiểm (không lấy mẫu).
- Chạy kiểm danh tính: gói và mẫu mới không chứa tên kênh, tên người, tên sản phẩm của video mẫu, chữ trên màn hình đủ nhận ra nguồn.
- Xong khi: các dòng kiểm đạt; dòng sai đã sửa hoặc bỏ.

## Bước 4 — Gộp

| Trường hợp | Làm trong file thư viện | Làm trong `pattern-index.md` |
|---|---|---|
| Trùng mẫu cũ | thêm bằng chứng; số đo mới viết thành khoảng | tăng số nguồn; nâng độ tin nếu đủ điều kiện |
| Biến thể | thêm `### XX-NNa · …` ngay dưới mẫu gốc, đủ 9 trường | thêm dòng |
| Mâu thuẫn | giữ mẫu cũ, thêm biến thể mô tả cách làm khác, ghi video nào làm gì | ghi chú |
| Mẫu mới | cấp số cuối dãy, thêm mục đủ 9 trường vào đúng file của nhóm | thêm dòng, trạng thái `dùng` |
| Mẫu sai đã biết | không xoá; ghi «(bỏ — lý do)» | trạng thái `bỏ` |

- **Cổng người:** trước khi ghi, trình danh sách mã mới + mẫu đổi độ tin + mâu thuẫn; chỉ gộp khi người dùng gật.
- Sửa thư viện là sửa repo `agent-video-studio`: theo quy ước của repo (chạy test, cập nhật adapter nếu đổi mô tả skill).

## Bước 5 — Cập nhật số và kiểm máy

- Tính lại tỉ lệ chế độ bằng `corpus_extract.py stats` cho mọi video trong sổ; cập nhật bảng `layout-library.md` §4 và cột «Căn cứ» của bảng ngưỡng ở `workflow.md` bước 3 (ngưỡng chỉ đổi khi người dùng duyệt).
- Chạy `python scripts/build_index.py --check` trong skill `vlog-design` (index khớp tiêu đề thư viện) và `python -m pytest -q tests/test_vlog_design_library.py`.
- Xong khi: kiểm máy xanh; ghi một dòng vào `<trạm>/library/<tên>/README.md`: ngày, video đã gộp, số mã mới, số mẫu nâng bậc.

## Ai làm gì

| Việc | Model |
|---|---|
| Điền gói mẫu từ nhật ký | Sonnet (hoặc Haiku nếu gói ngắn) |
| Đối chiếu mã, kiểm chứng, gộp | Opus |
| Phản biện độc lập khi gộp ≥ 5 mã mới | Fable |
