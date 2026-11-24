# Ví dụ: một short mẫu «Giới thiệu cộng đồng X»

> Ví dụ trung tính, dựng lại theo cấu trúc của một short đã qua bốn vòng duyệt ảnh tĩnh. Tên, lời và mốc là minh hoạ; dữ liệu thật của một tập nằm ở trạm, không ở repo.

## Contents
- Nguồn và ý tưởng
- Bảng beat và điểm cắt
- Hình: beat → icon → bố cục
- Trích `layout.json`
- Bốn vòng ảnh tĩnh
- Kết quả kiểm

## Nguồn và ý tưởng

Bản dài 9 phút 20 s, kênh mẫu về làm việc với trợ lý AI. Bản đồ nguồn: 4 clip giọng (một file phát hai lần + hai file ghép sau), 5 take avatar, 220 dòng lời.

Ứng viên SH-A, 78 điểm: ghép **ba chỗ không liền nhau** thành một lời giới thiệu trọn ý — (1) người nói kể vừa lập cộng đồng X, (2) nội dung sẽ đăng ở đâu và mời chia sẻ, (3) lời mời tham gia. Avatar có ở 75 % số giây. Short này được dựng đầu tiên vì gom đủ rủi ro: hai file giọng, cắt giữa câu, cắt avatar giữa take.

Hook 0–2 s: «Cộng đồng X là gì?» (câu hỏi; không viết «cộng đồng lớn nhất…» vì lời không nói).

## Bảng beat và điểm cắt

| Beat | Dòng | Timeline bản dài | Lời | Avatar |
|---|---|---|---|---|
| A1 | k93w7–k95 | 246,92–251,85 | «ngoài nhóm cũ thì mình xây thêm một cộng đồng mới gọi là cộng đồng X,» | không |
| A2 | k96–k97 | 251,82–254,95 | «mặc dù tên gọi là công ty một người.» | không |
| A3 | k205w2–k208 | 457,34–466,50 | «mọi bài viết, video, blog và cả các buổi phát trực tiếp mình đều đăng trên nhóm của cộng đồng X…» | take 10, giữa take +11,74 s |
| A4 | k209–k216 | 467,00–486,62 | «và mình khuyến khích mọi người đăng bài chia sẻ… để cộng đồng có nhiều tương tác tích cực.» | take 11, +0,40 s |
| A5 | k129w8–k132 | 333,12–339,45 | «hãy thử tham khảo series này và tham gia cùng cộng đồng X để chúng ta cùng trao đổi.» | take 7, giữa take +4,24 s |

| Điểm | Mốc kế hoạch | Mốc dùng | Hạng | Ghi chú |
|---|---|---|---|---|
| A1 vào («ngoài») | 246,90 | 246,92 | trũng −25 dB | lời liền với từ nối trước đó; khe −46 dB cách đó 0,18 s là âm tắc của từ kế, không phải ranh. **Cần người nghe** |
| A3 vào («mọi») | 457,10 | 457,34 | lặng −70 dB | mốc chữ lệch giọng 0,34 s ở clip ghép sau; mốc kế hoạch cắt vào đuôi từ trước |
| A3 → A4 | 466,18 / 466,55 | 466,50 → 467,00 | lặng | rút khoảng lặng gốc 0,82 s còn 0,34 s; `gap_after: 0` |
| A5 vào («hãy») | 333,05 | 333,12 | trũng −32 dB | vào giữa dòng. **Cần người nghe** |

`cut_voice.py` ra `voice.wav` 46,5 s (đệm đầu 0,30 s, đuôi 2,4 s cho thẻ kết), bốn đoạn S1–S4; `make_subs.py --asr` ra 38 cụm 3–5 từ, cụm rộng nhất 804 px ở cỡ 64 px.

## Hình: beat → icon → bố cục

| Lời (mốc trong short) | Ý | Icon / logo | Tương tác bên trong + liên kết | Mẫu |
|---|---|---|---|---|
| 0–2 s | câu hỏi mở | logo kênh + chữ hook | logo bật nảy, chữ trượt lên | V0 |
| «ngoài nhóm cũ» 0,3 s → «cộng đồng mới» 2,9 s | cũ sinh ra mới | huy hiệu nhóm cũ ↓ mạng người | tín hiệu chạy trên cạnh mạng, nút sáng lần lượt; chấm chạy xuống | V1 |
| «gọi là cộng đồng X» 4,3 s | đặt tên | logo cộng đồng thay huy hiệu ở đỉnh cột | logo lắp vào đúng chỗ huy hiệu cũ | V1 (giữ) |
| «công ty một người» 6,6 s | nghĩa của tên | người dưới đèn + toà nhà | cửa sổ toà nhà bật dần, đèn chiếu quét | V7 không avatar (hai icon giữa khung) |
| «bài viết» 9,1 · «video» 9,9 · «blog» 10,4 · «phát trực tiếp» 11,9 s | bốn loại nội dung | trang giấy · chuỗi video · cửa sổ blog · máy quay | dòng chữ chạy + bút; ô video sáng lần lượt; lông ngòi sáng; chấm nháy + sóng | V3, avatar dưới trái |
| «trên nhóm … cộng đồng X» 14,6 s | tất cả về một nơi | logo nền tảng + mạng người | bốn icon thu lên hàng trên; chấm chạy từ hàng trên xuống đích | V3 → V1 |
| «hỏi đáp» 22 · «ví dụ» 24,4 · «tìm tòi» 26,6 · «sản phẩm» 30 s | thứ nên chia sẻ | bong bóng hỏi đáp · bảng mẫu · bóng đèn · hộp mở | mỗi icon vào lớn, một lúc một cái; hàng phụ: avatar ┄ nền tảng ┄ cộng đồng | V7 × 4, đổi kiểu vào |
| «tương tác tích cực» 36,8 s | kết quả | mạng người + thư bay + tim/ngón tay | thư bay theo đường cong có hạt đuôi; tim nổi lệch pha | V1 chéo |
| «tham khảo series» 37,9 → 39,8 s | lời mời | lộ trình bậc → nền tảng video + chuỗi video | đốm sáng nhảy bậc; nút phát chạy qua từng ô | V5 → V1 |
| «tham gia cùng cộng đồng X» 42,3 s | đích | mạng người + logo cộng đồng | hai icon cạnh nhau dưới chuỗi video | V1 (giữ) |
| 44,1–46,5 s | thẻ kết | logo kênh + «Xem tập đầy đủ trên kênh» | — | V9 |

Điểm đáng chú ý: không có chip chữ; logo nền tảng chỉ xuất hiện khi lời đọc tên nó; ở hàng phụ cạnh avatar logo nền tảng **không** lặp khi nó đang là icon chính phía trên.

## Trích `layout.json`

```json
{"frame": {"w": 1080, "h": 1920}, "duration": 46.5,
 "zone": {"y0": 200, "y1": 1080},
 "skip": [[0, 2.0], [44.1, 46.5]],
 "elements": [
  {"id": "old",  "asset": "icons/old-group.png", "t_in": 0.8,  "t_out": 4.3,  "cx": 540, "cy": 420, "w": 330},
  {"id": "net",  "asset": "icons/community.png", "t_in": 2.9,  "t_out": 6.4,  "cx": 540, "cy": 860, "w": 460},
  {"id": "post", "asset": "icons/post.png",      "t_in": 9.1,  "t_out": 14.4, "cx": 330, "cy": 460, "w": 400},
  {"id": "vids", "asset": "icons/video-row.png", "t_in": 9.9,  "t_out": 14.4, "cx": 760, "cy": 460, "w": 400},
  {"id": "host", "asset": "avatar", "role": "avatar", "t_in": 8.63, "t_out": 44.04, "cx": 250, "cy": 1300, "w": 400}
 ],
 "scenes": [
  {"id": "A1", "t_in": 0.3,  "t_out": 6.4,  "layout": "V1", "motion": "flow-down"},
  {"id": "A2", "t_in": 6.4,  "t_out": 8.6,  "layout": "V7", "motion": "pop"},
  {"id": "A3", "t_in": 8.6,  "t_out": 17.8, "layout": "V3", "motion": "grid-then-collapse"},
  {"id": "A4", "t_in": 17.8, "t_out": 37.4, "layout": "V7", "motion": "hero-swap"},
  {"id": "A5", "t_in": 37.7, "t_out": 44.0, "layout": "V5", "motion": "step-runner"}
 ]}
```

## Bốn vòng ảnh tĩnh

| Vòng | Người duyệt bắt | Sửa |
|---|---|---|
| v1 | quá nhiều chip chữ; chỉ một hình động; avatar bán thân chiếm nửa khung; phụ đề lơ lửng giữa | bỏ chip, mỗi ý một icon động; avatar tròn 400 px; phụ đề sát đáy |
| v2 | 8 ý không có icon hợp, đang dùng icon tạm | xin phép rồi tạo một tấm 12 icon (8 + 4 dự phòng) theo khoá phong cách kênh |
| v3 | icon dồn 1/4 trên, giữa khung trống; icon nhỏ lẻ ở góc; có khung trống hẳn ở 38,6 s | cụm icon xếp dọc giữa vùng; icon vào lớn rồi thu về lưới; lấp bằng icon theo lời; rà 0,5 s |
| v4 | đạt | — |

Góp ý chung sau khi duyệt cả loạt, đã thành luật của skill: icon phải có thành phần bên trong tương tác chứ không chỉ sáng lên; đường liên kết phải chạy; bố cục theo tư duy infographic; không lặp trong một khung; khung có media lồng thì chỉ còn media.

## Kết quả kiểm

- Rà 0,5 s: ở đợt dựng gốc làm bằng đoạn rà nằm trong script dựng (v3 lộ khung trống quanh 38,6 s, v4 hết). `gap_scan.py` là bản đóng gói lại của đoạn rà đó; **chưa chạy trên short gốc** vì lúc ấy chưa có `layout.json`.
- `qa_short.py` chạy trên bản render thật: 1080×1920 · 30 fps · 46,5 s · −14,1 LUFS · true peak −1,4 dBFS · tiếng đầu 0,30 s — thoát 0.
- `source_map.py` và `cut_voice.py` chạy lại trên nguồn thật cho đúng bản đồ và đúng các mốc `media_in` / `short_in` / offset avatar của bản dựng tay.
- Chưa kiểm khi giao: người nghe hai điểm cắt giữa lời (0,3 s và 37,7 s); xem trên điện thoại; giấy phép nhạc nền.
