# Hợp đồng thư viện mẫu

> **Kết luận:** mọi mẫu trong thư viện `vlog-design` (và mọi gói mẫu do `video-reverse-engineer` sinh ra) theo **một** khuôn: tiêu đề `### XX-NN · Tên`, 9 trường cố định, một nhãn độ tin. Nhờ vậy học thêm một hay nhiều video chỉ là **gộp** vào thư viện, không viết lại.

## Contents
- Tỉ lệ khung
- Nhóm mã
- Khuôn một mẫu
- Độ tin
- Mã video và chế độ
- Luật mã mới, biến thể, bỏ
- Gộp mẫu từ video mới
- Kiểm máy

## Tỉ lệ khung

- **Thư viện hiện tại là 16:9** (khung chuẩn 1920×1080; bộ video học đầu tiên đều 1280×720). Mọi vị trí, kích thước trong mẫu là **% của khung 16:9**.
- Video mẫu tỉ lệ khác (9:16, 1:1, 4:5) **không gộp vào các mẫu 16:9**: mẫu bố cục (LY), vùng an toàn và kích thước người/khung là của riêng tỉ lệ đó. Khi có, lập file riêng theo tỉ lệ (ví dụ `layout-library-9x16.md`, mã `LY-V01`…) và ghi tỉ lệ ở trường «Trông thế nào». Mẫu không phụ thuộc khung (đa số TX, MO, AU, RC) được gộp, ghi rõ tỉ lệ nguồn trong «Bằng chứng».
- Bản 9:16 trong storyboard (short cắt từ video dài) là **bản phụ suy ra từ 16:9**: chưa có mẫu đo, mọi số vùng cắt và vùng an toàn dọc là đề xuất, phải kiểm khi dựng.

## Nhóm mã

| Nhóm | Nghĩa | File |
|---|---|---|
| LY | bố cục khung (vị trí người / màn hình / slide / chữ) | `layout-library.md` |
| TR | chuyển cảnh và chuyển chế độ | `transitions-mode-switch.md` |
| VO | vật thể, icon, hình người, UI mock | `visual-vocabulary.md` |
| MO | chuyển động liên kết giữa các khối | `visual-vocabulary.md` |
| TX | hiệu ứng chữ | `text-and-infographic-motion.md` |
| IG | dựng infographic, sơ đồ, flowchart | `text-and-infographic-motion.md` |
| ST | thiết bị kể chuyện | `idea-to-visual.md` |
| RC | công thức ý → hình (ghép các mã trên) | `idea-to-visual.md` |
| AU | âm thanh: nhạc nền, SFX, khoảng lặng, hạ nhạc dưới giọng | `audio-patterns.md` |

Danh sách mọi mã hiện có, độ tin và trạng thái: [`pattern-index.md`](pattern-index.md). Đọc file này trước khi tra thư viện chi tiết.

## Khuôn một mẫu

````markdown
### XX-NN · Tên ngắn
- **Trông thế nào:** vị trí (% khung), kích thước, màu theo vai trò (nền / nhấn / chữ)
- **Chuyển động:** trước → sau, thứ tự, giây; easing là gợi ý
- **Giữ:** bao lâu trên màn hình (giây)
- **Khi dùng:** loại ý trong lời thoại / loại đoạn
- **Tránh:** lỗi hay gặp, chỗ không hợp
- **Bằng chứng:** mã video + mốc + loại mốc, ví dụ «V05 tr 38.6 (soi dày)», «V04 1:35 (lưới)»
- **Độ tin:** đo | ước | suy ra · số video làm chứng (ví dụ «đo · 2 nguồn»)
- **Gợi ý dựng:** 1–3 dòng CSS/GSAP/HyperFrames
- **Biến thể:** `XX-NNa` …, hoặc «—»
````

- RC là ngoại lệ có chủ đích: một dòng đậm `**RC-NN · «câu thoại mẫu».**` rồi chuỗi mã ghép + nhịp + bằng chứng; vẫn bắt buộc có **Độ tin**.
- Trường không có dữ liệu ghi «chưa có», không bỏ trường.
- Không tên kênh, tên người, tên sản phẩm của video mẫu; không chép chữ trên màn hình đủ để nhận ra nguồn (tên panel, giá, tiêu đề riêng) — mô tả chung («nhãn tên tính năng», «số tiền»). Trích lời ≤ 12 chữ.

## Độ tin

| Bậc | Khi nào | Ví dụ |
|---|---|---|
| **đo** | có mốc soi dày ≥ 5 khung/giây, hoặc mốc chính xác của công cụ (`@N` trong `VIDEO.md`), hoặc khung lớn đo trực tiếp | «V05 tr 38.6» |
| **ước** | từ lưới mỗi 2 s hoặc nhật ký cảnh (sai ±2–4 s) | «V04 1:35 (lưới)» |
| **suy ra** | không có mốc; tổng hợp hoặc đối xứng | ô `*` trong ma trận chuyển cảnh |

- Nâng bậc chỉ khi có mốc mới **đúng loại** (ước → đo cần soi dày tại mốc đó).
- Chiều ngược của một chuyển cảnh là mẫu **riêng**, phải đo riêng; không suy theo đối xứng (đã sai một lần: co ra có chuyển động nhưng quay về là cắt).
- Mẫu chỉ một video làm chứng ghi «1 nguồn»; khuyến nghị dựa trên «1 nguồn» phải nói rõ.

## Mã video và chế độ

- Mã video trong thư viện: `V01`, `V02`… theo thứ tự nhận vào, không tái dùng. Sổ mã ↔ file nằm ở trạm (`<trạm>/library/<tên>/README.md`), không ghi vào repo. Bộ học đầu tiên dùng bí danh A–E = V01–V05.
- Chế độ hình: **P** người toàn khung (kể cả có chữ / lớp nổi) · **PA** người + slide/hoạt họa (kể cả người ở cột bên slide) · **A** chỉ hoạt họa/slide · **S** giao diện phần mềm/web thật được quay · **PS** người + giao diện thật · **AS** hoạt họa phủ trên giao diện thật.

## Luật mã mới, biến thể, bỏ

1. **Khớp trước, tạo sau.** So «trông thế nào» và «khi dùng» với mẫu cùng nhóm trong `pattern-index.md`. Khớp cả hai → nối bằng chứng vào mẫu cũ.
2. **Biến thể** `XX-NNa`, `XX-NNb` (chữ thường): cùng cấu trúc và cách dùng, khác hình thức hoặc thông số.
3. **Mã mới:** chỉ khi không mẫu nào khớp cả hai trường; lấy số kế tiếp cuối dãy; không tái dùng số.
4. **Bỏ:** giữ dòng trong index, trạng thái `bỏ` + lý do; không xoá mục khỏi file thư viện mà ghi «(bỏ — xem …)».
5. Trong gói mẫu chưa gộp, mẫu mới đặt tạm `XX-NEW-1`, `XX-NEW-2`; số thật chỉ cấp lúc gộp.

## Gộp mẫu từ video mới

Quy trình gộp nằm ở skill `video-reverse-engineer`, file `references/library-merge.md`. Tóm tắt:

| Trường hợp | Làm |
|---|---|
| Trùng mẫu cũ | thêm bằng chứng, tăng số nguồn; số đo mới ghi thành khoảng («≈14–16%») |
| Mâu thuẫn mẫu cũ | giữ cả hai: mẫu cũ + biến thể mới, ghi rõ video nào làm gì |
| Mẫu mới | cấp mã cuối dãy, thêm dòng index, người dùng duyệt danh sách mã mới |
| Số tỉ lệ / ngưỡng | tính lại bằng `corpus_extract.py stats` trên toàn bộ nhật ký; cập nhật bảng ở `layout-library.md` §4 và bảng ngưỡng `workflow.md` bước 3 |

## Kiểm máy

- `python scripts/pace_check.py <pacing.md> --index references/pattern-index.md`: mã LY trong bảng nhịp phải có trong index và không ở trạng thái `bỏ`.
- Khi sửa thư viện: mọi tiêu đề `### XX-NN · ` có một dòng index và ngược lại (test `tests/test_vlog_design_library.py`).
