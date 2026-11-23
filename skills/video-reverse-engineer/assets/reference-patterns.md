# Gói mẫu của một video — <mã video Vnn> (mẫu điền)

Not agent instructions. Đây là **đầu ra chuẩn** khi học từ MỘT video (nhánh `decompose`/`video-reference-analysis` hoặc một video trong corpus-study), để gộp vào thư viện skill `vlog-design` theo `skills/vlog-design/references/library-contract.md`.

Đặt ở trạm: `<trạm>/library/<tên-thư-viện>/evidence/<video>/reference-patterns.md`. Không ghi vào repo.

## 1. Thông tin video

- Mã: Vnn · **tỉ lệ khung + độ phân giải** (ví dụ 16:9, 1280×720) · loại (chế độ chính) · thời lượng · ngôn ngữ lời · quyền dùng (chỉ học ngữ pháp)
- Video không phải 16:9: mẫu LY và số vị trí/kích thước **không** khớp vào thư viện 16:9 (xem hợp đồng, mục Tỉ lệ khung).
- Nguồn đã dùng: `VIDEO.md` + `video/rhythm.md`, `timeline.md`, `sound.md`, `packaging.md` (nếu chạy decompose) · `scene-log.md` · `transitions/TRANSITIONS.md` · `reference-map.md`
- Số máy tính (`corpus_extract.py stats`): tỉ lệ chế độ P/PA/A/S/PS/AS, số lần đổi chế độ, cảnh TB/dài nhất

## 2. Bảng mẫu (một dòng mỗi lần mẫu xuất hiện có ý nghĩa)

| Mốc | Nhóm | Mã khớp hoặc `XX-NEW-n` | Khớp vì / khác ở | Loại mốc (lưới ±2–4 s / soi dày ±0.1 s / `@N`) | Nguồn |
|---|---|---|---|---|---|
| 0:38.6 | TR | TR-03 | co người thành PIP 0.8 s | soi dày | TRANSITIONS.md |
| 2:02 | TR | TR-04 | quay về toàn khung bằng cắt | soi dày | tr_0120.8 |
| 4:10 | IG | IG-NEW-1 | ma trận 2×2 chưa có trong thư viện | lưới | scene-log #37 |

## 3. Mẫu mới (mỗi `XX-NEW-n` một mục đủ 9 trường theo hợp đồng)

### IG-NEW-1 · Tên ngắn
- **Trông thế nào:** …
- **Chuyển động:** …
- **Giữ:** …
- **Khi dùng:** …
- **Tránh:** …
- **Bằng chứng:** Vnn 4:10 (lưới)
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** …
- **Biến thể:** —

## 4. Bằng chứng nâng bậc cho mẫu cũ

| Mã | Bậc hiện tại (theo `pattern-index.md`) | Bằng chứng mới | Bậc đề xuất |
|---|---|---|---|
| TR-04 | đo · 1 nguồn | Vnn tr 362.8 | đo · 2 nguồn |

## 5. Mâu thuẫn với thư viện

| Mã | Thư viện nói | Video này cho thấy | Đề xuất (biến thể / sửa số / ghi chú) |
|---|---|---|---|

## 6. Âm thanh (nhóm AU)

| Mốc | Loại (nhạc nền / SFX / lặng / hạ nhạc dưới giọng) | Mô tả | Mã khớp hoặc `AU-NEW-n` | Nguồn (`sound.md`, nghe trực tiếp) |
|---|---|---|---|---|

## 7. Chưa kiểm

- Điều không xem/nghe được, mốc nghi sai, lưới đã cắt mà chưa ghi chép.
