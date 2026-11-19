# Bài học từ các cổng duyệt (checklist cho người/agent duyệt)

> **Kết luận:** các lỗi dưới đây đã gặp thật ở video mẫu (3 vòng: raw, bản hoàn chỉnh v1, phản hồi người dùng → v2, v3). Dùng làm **checklist duyệt cổng** trước khi đưa bản dựng cho người xem. Mỗi dòng: lỗi → dấu hiệu → cách sửa → khâu nên bắt.

## 1. Cổng raw (khâu 5, Opus duyệt shot Earth/MapLibre)

| Lỗi | Dấu hiệu | Cách sửa |
|---|---|---|
| Nhãn/UI còn sót trên ảnh Earth (nhãn địa danh, thẻ mẹo) | chữ lạ trên ảnh «Clean» | đặt lại nền Clean, tắt thẻ mẹo, chụp lại |
| Ảnh chưa tải hết khi chụp | vùng mờ/ô vuông thô | tăng thời gian chờ, chụp lại |
| Các shot lặp hướng nhìn (cùng heading) | nhiều cảnh nhìn như nhau | đổi heading (vd 40° → 270°, 220°) |
| Cảnh «chia đôi Earth/Map» không thực hiện được | tài liệu đề ra nhưng không có shot | thay bằng clip hiệu ứng 3D MapLibre và **ghi thay đổi vào storyboard** |
| Shot nghiêng quá (75°) bị vỡ | bóng tối/hình méo | đổi `t` về 55–65° hoặc dùng bản top-down |

## 2. Cổng bản hoàn chỉnh v1 (khâu 6–8)

| # | Lỗi | Cách sửa (đã áp dụng ở bản sau) |
|---|---|---|
| 1 | Chữ hook gõ sát cuối cảnh nên **không hiện đủ** | đặt `at` sớm (0,15/0,75/1,4), `per` nhỏ; chữ hook **xong trước 4 s** và giữ ≥ 1 s |
| 2 | **CTA mất ở 2 s cuối** vì gắn vào một cảnh ngắn; dòng miễn trừ 28 px chỉ hiện 2 s | CTA và miễn trừ gắn vào **layer riêng phủ cả khoảng CTA**; miễn trừ ≥ 4 s, đặt trong vùng an toàn (không phải 15 % đáy) |
| 3 | Nhãn «ẢNH VỆ TINH» đè lên cảnh đã là khối 3D | nhãn chỉ hiện đúng khoảng của nó (`out`), rồi «KHỐI 3D MINH HOẠ» |
| 4 | **Lời nói khác nhãn trên hình** («phân khu Ecopark» trong khi nhãn là khu đô thị khác) | lời phải mô tả đúng nhãn; thêm vạch nối cho nhãn xa điểm |
| 5 | 3 tag gần nhau chồng lên ghim, nét đứt cắt qua chữ | gộp cụm gần thành một chú giải; tag nền mờ vẽ **trên** nét đứt; chú giải (`legend`) thay vì dán nhãn lên bản đồ |
| 6 | Dòng nguồn ở y = 1700 (vùng giao diện TikTok/Reels che) | dòng nguồn y ≈ 1520 |
| 7 | Ranh vẽ từ `admin_level 6` ghi nhãn «XÃ»: sau sáp nhập OSM cấp 6 có thể là ranh cũ | ghi «ranh tham khảo © OSM», **người xác nhận**; sai thì bỏ viền, giữ nhãn + ghim |
| 8 | Thẻ số cuối chỉ hiện 1,5 s, thiếu chủ thể («FDI» của tỉnh nào) | thẻ ≥ 2,5 s, chú thích có chủ thể và ngày |
| 9 | Câu lời tăng tốc ×1,2 sát trần; tên tiếng Anh và số thập phân đọc sai | giảm chữ hoặc dài cảnh; phiên âm tên; **người nghe lại** (ASR cỡ nhỏ chỉ là cờ) |

## 3. Phản hồi của người dùng sau bản v1 (gốc của bản v2/v3)

- **Nhanh quá** (zoom, tag, thẻ số, khung hành chính) → sàn thời gian đọc ([`pacing-and-clarity.md`](pacing-and-clarity.md)).
- **Chưa hình dung được vị trí** → viền neon đậm vẽ dần, khoảng dừng giữa các bậc, hồ/đối tượng nhắc tới phải được **bo viền**.
- **Khoảng cách phải thấy cả hai đầu** → khung quan hệ (dự án ↔ đối tượng ↔ số km).
- **Muốn tiện ích theo vòng bán kính** → cảnh vòng 0,5/1,5 km + biểu tượng nhóm + radar.
- **Nhà 3D rất hay** → thêm 4 góc (mọc + xoay, bay thấp từ phía hồ, xoay toàn cảnh, nghiêng từ trên xuống).
- **Zoom giật** → đo nguyên nhân (Earth quay ra ~6 khung/giây thật), chuyển sang quay từng khung (`camera_path_capture.mjs`).
- **Vòng tròn nhấp nháy lặp khó chịu** → ghim chỉ bật một lần, mọi lặp hữu hạn.

## 4. Câu hỏi duyệt nhanh (trả lời được bằng mắt)

1. Mỗi bậc hành chính đứng yên ≥ 2 s sau khi viền vẽ xong? Mỗi tag ≥ 2 s? Mỗi thẻ số ≥ 2,5 s?
2. Mỗi câu về khoảng cách có đủ điểm đầu, điểm cuối (được khoanh) và số km trên cùng một khung?
3. Đối tượng được nhắc trong lời có hiện và có tên trên bản đồ? Lời có khớp nhãn?
4. Có chữ nào mất vì gắn vào cảnh ngắn? CTA và miễn trừ còn đến hết video?
5. Có nhãn «minh hoạ» cho mọi ảnh vệ tinh 3D / khối 3D? Có dòng nguồn trong vùng an toàn?
6. Zoom liền mạch (đo khung khác nhau ≈ 100 %)? Có vòng sóng lặp hoặc `repeat:-1`?
7. Số liệu trên khung = số trong research (haversine ±3 %, nguồn + ngày)? Có câu cấm (giá, «chắc chắn tăng giá», phút di chuyển)?
8. Điều chưa kiểm đã ghi rõ (âm thanh nghe bằng tai, hiển thị trên điện thoại, quyền ảnh/nhạc/giọng)?
