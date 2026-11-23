# Manifest tài nguyên — <mã-tập>

Trạng thái: có sẵn · cần tải · cần tạo · cần quay · cần người duyệt.

**Một dãy ID duy nhất `AS01…` dùng chung cho storyboard và manifest.** Thẻ cảnh (mục 6 của `storyboard.md`) và bảng giọng chỉ viết ID, không viết tên file rời. ID tăng dần, không tái dùng; dòng bỏ giữ ID, trạng thái `bỏ`. Cần asset mới giữa chừng: thêm dòng vào manifest trước, rồi mới viết ID vào thẻ.

Loại: `icon` · `người` · `vật` · `ảnh` · `font` · `màu` · `motion` · `clip` · `giọng` · `nhạc` · `sfx` · `thumbnail` · `take`.

| ID | Loại | Mô tả | Dùng ở cảnh | Nguồn (URL · tự vẽ · AI: prompt + seed · quay · tổng hợp: profile + seed) | Giấy phép | File | Trạng thái |
|---|---|---|---|---|---|---|---|
| AS01 | icon | … | C03, C07 | … | … | assets/icons/… | … |
| AS02 | giọng | câu V001, marker `hao-hung` | C01 | tổng hợp: profile …, seed … | giọng của chính chủ, có lời đồng ý | assets/voice/V001.wav | cần tạo |
| AS03 | take | TK01 = V001–V006, crop 720:720:0:180 | C01–C03 | lip-sync: hồ sơ avatar …, engine LatentSync, guidance 2.5, seed … | mặt của chính chủ, có lời đồng ý | assets/takes/TK01.mp4 | cần tạo |
| AS04 | nhạc | nền, loop ≥ độ dài video, mức dưới giọng … | toàn video | URL · tự soạn · nhạc kênh | nêu giấy phép + yêu cầu ghi nguồn | assets/music/… | cần tải |
| AS05 | sfx | họ «…» (click, whoosh…) | C02, C06 | … | … | assets/sfx/… | … |
| AS06 | thumbnail | khung từ C… giây …, chữ ≤ 4 từ | xuất bản | dựng từ composition | — | assets/thumb/… | cần tạo |

Ghi chú theo loại:
- **giọng:** một dòng một câu V (hoặc một khối câu liền cùng marker); ghi profile, marker, seed đã ghim, kết quả ASR (CER). Không chép giá trị secret hay đường kho giọng.
- **take:** một dòng một take (bảng take avatar mục 5 storyboard); ghi hồ sơ avatar, crop, điểm SyncNet khi đã QA.
- **nhạc / sfx:** ghi giấy phép và nghĩa vụ ghi nguồn (đưa vào mô tả ở mục 7); nhạc chỉ một họ cho cả video.
- **thumbnail:** chỉ là khung tĩnh dựng từ video hoặc từ asset đã có, không thêm khuôn mặt thật khác.

## Khoá phong cách (dùng chung cho mọi ảnh AI)

- Màu: …  · Nét / bóng: …  · Góc nhìn: …  · Nền: …  · Cấm: chữ trong ảnh, logo thật, khuôn mặt người thật.

## Kiểm

- [ ] Mọi ID trong storyboard (thẻ cảnh, bảng giọng, bảng take, gói xuất bản) có dòng ở đây, và ngược lại mọi dòng ở đây được dùng ít nhất một chỗ
- [ ] Một họ icon, cùng stroke-width
- [ ] Font qua thử glyph «Ả Ẫ Ặ Ể Ỗ Ợ Ữ ỹ đ Đ»
- [ ] Mọi dòng có nguồn + giấy phép
- [ ] Mọi giọng / take có lời đồng ý trong hồ sơ trước khi tạo
