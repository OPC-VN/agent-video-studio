# Thư viện bố cục LY (layout) cho video giảng dạy / kể chuyện

Kết luận: 15 bố cục LY phủ được cả năm video mẫu; video có người thật chỉ cần 5 bố cục (LY-01…05) cộng nhóm không người (LY-06…15) để xen, và quy tắc đắt giá nhất là giữ **một khung người duy nhất** đổi kích cỡ chứ không đổi hình thể.

Khuôn mẫu, độ tin, mã video và chế độ: xem `library-contract.md`; danh sách mã: `pattern-index.md`.

## Contents
1. Lưới vùng an toàn 16:9
2. Quy ước đọc mỗi mẫu
3. LY-01 … LY-15
4. Phối người + màn hình + hoạt họa (bảng chọn LY theo loại đoạn, tỉ lệ chế độ, khuyến nghị cân đối)
5. Chỗ chưa chắc

## 1. Lưới vùng an toàn 16:9

> **Mọi bố cục trong file này là 16:9.** Không dùng trực tiếp cho khung dọc; bản 9:16 xem `library-contract.md`, mục Tỉ lệ khung.

Khung chuẩn 1920×1080 (mẫu gốc đo ở 1280×720; mọi số dưới đây là **% khung** nên đổi được). Dựa theo vị trí lặp lại ở D, E, B, C.

```
x: 0%        5%                                  95%      100%
y:0 +--------+------------------------------------+--------+
    | dải trên 0-8%: pill chương (D), pill repo   | logo   |
    | giữa-trên (A), logo kênh góc phải (B)       | kênh   |
 8% +--------+------------------------------------+--------+
    |  lề    |   VÙNG NỘI DUNG CHÍNH              |  lề    |
    |  5%    |   (tiêu đề, thẻ, sơ đồ, màn hình)  |  5%    |
84% +--------+------------------------------------+--------+
    |        |  VÙNG PHỤ ĐỀ 84%-95%, giữa         |  tag   |
95% +--------+------------------------------------+--------+
    | PIP trái dưới: squircle người ≈14% rộng (E)          |
100%+------------------------------------------------------+
```

| Vùng | Toạ độ (≈ % khung) | Dùng cho | Luật |
|---|---|---|---|
| Lề an toàn | 5% trái/phải, 6% trên/dưới | Mọi chữ | Không đặt chữ ngoài lề; vật trang trí được tràn |
| Dải trên | y 0–8% | Pill tên chương (D), pill tên repo (A), logo kênh (B, góc phải trên) | ≤ 1 pill + ≤ 1 logo cùng lúc |
| Vùng nội dung | x 5–95%, y 8–84% | Tiêu đề, thẻ, sơ đồ, màn hình | Cột người (nếu có) ăn vào bên phải 22–25% hoặc góc dưới 14% |
| Vùng phụ đề | y 84–95%, rộng ≤ 70% giữa khung | Phụ đề đốt (nền đen mờ, từ khoá đổi màu) | Khi có PIP trái dưới: phụ đề lệch phải bằng bề rộng PIP + 2% |
| PIP trái dưới | rộng ≈14%, tâm (≈10%, ≈86%) | Squircle người khi xem màn hình (E) | Đẩy panel/nút của màn hình tránh khu này |
| PIP phải dưới | rộng ≈16%, cao ≈50% (D tr 40.8) | Thẻ người dọc/chữ nhật khi xem màn hình (D) | Không dùng cùng lúc tag credit |
| Cột người phải | x 75–100%, cao tràn | Thẻ dọc khi có slide (D, ≈27% rộng × ≈92% cao, tr 52.8) | Slide co về x 5–70% |

Nên chọn **một** phía PIP cho cả video (E: dưới-trái). D trộn PIP tròn dưới-trái (mở) với thẻ dọc dưới-phải (màn hình): nếu trộn, mỗi vai một hình thể cố định. Không đặt nút/thanh trượt của UI mock sát cạnh trên vùng phụ đề (cách ≥ 2%).

## 2. Quy ước đọc mỗi mẫu

Mỗi mẫu theo 9 trường của `library-contract.md`. Sơ đồ ASCII nằm dưới mỗi mẫu (P = người, S = màn hình, L = slide/thẻ, T = chữ). Vị trí tính theo % khung.

## 3. Các mẫu

### LY-01 · Người toàn khung + chữ nổi
- **Trông thế nào:** người phủ 100% khung, lệch trái hoặc phải (E 0:00, 0:38); nền phòng kem/sáng. Chữ nổi: số mục cam nhỏ trên tiêu đề, tiêu đề lớn 1 cụm, phụ đề nhỏ dưới. Mật độ chữ: 1–3 cụm. Định nghĩa: P = người toàn khung, kể cả khi có chữ hay lớp nổi.
- **Chuyển động:** tiêu đề vào bằng hạt chấm bay từ trên (0.6 s) → tụ thành chữ pixel (0.4 s) → hoà tan sang chữ có chân (0.3 s) (E tr 237.4).
- **Giữ:** 2 s (câu mở) đến 4–6 s (tiêu đề chương).
- **Khi dùng:** mở video, mở mục mới, kết/CTA.
- **Tránh:** để người đứng một mình quá ≈8 s không có lớp nổi; D ≈2% (0:00–0:08, 0:32–0:40), E 11.2%. Hiệu ứng tiêu đề hạt → chữ pixel → chữ có chân là dấu ấn riêng của video mẫu. Dấu ấn của mẫu: chỉ lấy nguyên lý, bắt buộc đổi hình thức.
- **Bằng chứng:** E 0:00, 0:38, 2:02, tr 237.4; D 0:00–0:08 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** video người `object-fit: cover` toàn khung; tiêu đề `filter: blur(12px)→0, opacity 0→1, 0.4 s power2.out` + đổi font ở mốc 0.3 s.
- **Biến thể:** `LY-01a` nền tối lệch phải (tự giới thiệu); `LY-01b` logo chữ giữa khung 2–6 s (hoạt họa mở).
```
+----------------------------+
| T(số mục cam nhỏ)          |
|  [  P người toàn khung  ]  |
|        lệch trái/phải      |
|  T tiêu đề (pixel→serif)   |
|  . . . phụ đề . . .        |
+----------------------------+
```

### LY-02 · Người toàn khung + lớp nổi một bên
- **Trông thế nào:** người toàn khung nhưng chừa ≈35–40% một bên cho thẻ nổi (bóng đổ, viền sáng): thẻ icon app, thẻ bài đăng mạng xã hội, thẻ bằng cấp, lưới logo khách hàng. Nền phòng tối ấm (D) hoặc kem. Chữ 3–10 từ.
- **Chuyển động:** thẻ trượt vào / bật tại chỗ 0.3 s; con trỏ kéo thả vào thư mục; thoát: lớp nổi mờ 0.3 s trước khi người co (D tr 6.8).
- **Giữ:** 3–6 s.
- **Khi dùng:** nêu bằng chứng uy tín, đưa 1 ví dụ tức thời khi người vẫn nói.
- **Tránh:** lớp nổi che mặt.
- **Bằng chứng:** D tr 6.8, tr 40.8 (thẻ trang web nổi bên phải + dòng chữ lớn dưới), 0:32–0:40; E 0:28–0:32 (lưới logo) (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** thẻ `x: 40→0, opacity 0→1, 0.3 s power2.out`, `stagger: 0.15`, `box-shadow` mềm.
- **Biến thể:** —
```
+----------------------------+
|  P toàn khung    | L lớp   |
|  (người lệch     | nổi 35% |
|   trái ≈60%)     | thẻ icon|
|  phụ đề góc phải dưới      |
+----------------------------+
```

### LY-03 · Người cột phải (thẻ dọc) + slide trái
- **Trông thế nào:** thẻ người cao tràn, sát mép phải, rộng ≈22–25% khung; phần còn lại nền kem (slide chữ, ≈#F3EDE2 ước) hoặc nền tối có lưới mờ (chương). Tiêu đề, số chương lớn màu nhấn, danh sách 01/02/03. Chữ: tiêu đề 2–6 từ, caption 6–10 từ, ≤ 3 khối.
- **Chuyển động:** mục vào lần lượt `stagger 0.3 s`; icon/dòng mô tả blur→nét sau 1.4 s (D tr 596.8); nhãn mới màu đen đè lên nhãn cũ có vạch gạch ngang (chữ chỉ đơn vị thời gian, đổi từ lớn sang nhỏ).
- **Giữ:** 4–16 s (D: cảnh trung bình 8.0 s).
- **Khi dùng:** khái niệm, liệt kê, so sánh hai thanh, thẻ chương «N /5».
- **Tránh:** đảo trái-phải người giữa các mục (D giữ cột phải cố định).
- **Bằng chứng:** D 0:54–1:34, tr 596.8, 05:12, 06:48, 07:12 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** `grid-template-columns: 1fr 23%`; thẻ người `border-radius: 28px`; số chương `font-size: 18vh`.
- **Biến thể:** `LY-03a` nền tối + lưới mờ (chương); `LY-03b` squircle người ở trái (E, xem LY-04).
```
+--------------------+-------+
| T tiêu đề / số lớn |  P    |
| L slide / sơ đồ    | thẻ   |
| (x 5–72%)          | dọc   |
|                    | 22–25%|
+--------------------+-------+
```

### LY-04 · Squircle lớn trái + tiêu đề/icon phải
- **Trông thế nào:** squircle (hình chữ nhật bo góc lớn kiểu iOS) chiếm ≈40% chiều rộng bên trái; phải là tiêu đề + icon nét cam + thẻ sơ đồ. Nền tối có lưới chấm. Chữ: 1 tiêu đề + 2–4 nhãn.
- **Chuyển động:** từ LY-01 người co về squircle 0.5 s; thoát bằng toàn khung blur 0.1 s rồi squircle co về góc (E tr 501.4). Người là **một** `div` đổi kích cỡ, không dựng hai bản.
- **Giữ:** 4–8 s. Đây là **trạng thái trung gian** giữa toàn khung và PIP — để chuyển mượt, không để lâu.
- **Khi dùng:** giải thích cơ chế bằng sơ đồ nhỏ; hỏi–đáp.
- **Tránh:** chữ bên phải > 12 từ.
- **Bằng chứng:** E 0:28, 1:04, 3:26, 4:28, 8:20, tr 501.4 (E ghi squircle ≈30–40% rộng) (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** người là **một** `div` đổi `width/height/left/top/border-radius` (FLIP), không dựng hai bản.
- **Biến thể:** —
```
+----------------------------+
| ( P squircle ) |  T tiêu đề|
| ≈40% rộng,     |  icon nét |
|  cao ≈70%      |  cam      |
+----------------------------+
```

### LY-05 · Màn hình toàn khung + người PIP góc
- **Trông thế nào:** màn hình thật phủ khung; squircle người ≈14% rộng dưới-trái, có glow nhẹ (E) hoặc thẻ dọc ≈16% rộng × ≈50% cao dưới-phải (D); tag credit nhỏ góc đối diện. Chữ trong UI dày (30–60 từ), chữ đồ hoạ thêm ≤ 3 cụm.
- **Chuyển động:** panel phải trượt vào ≈0.4–0.5 s; viền cam nhấn 0.5 s thay mũi tên; zoom ≈250% vào dòng lệnh khi cần đọc.
- **Giữ:** 6–24 s (PS dài ≥ 12 s là bình thường; D có chuỗi PS liên tục 05:18–07:58).
- **Khi dùng:** demo tính năng, gõ lệnh, đọc kết quả.
- **Tránh:** PIP đè nút bấm; đổi phía PIP giữa các cảnh.
- **Bằng chứng:** E 6:14, 8:24, 10:16, tr 87.4, tr 581.4; D 0:42–0:52, 05:18–07:58 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** PIP `position:absolute; left:2.5%; bottom:4%; width:14%`; panel `x:'100%'→0, filter: blur(8px)→0, 0.4 s`.
- **Biến thể:** `LY-05a` tách đôi terminal + trình duyệt, viền cam pane đang chạy (E 9:48); `LY-05b` thẻ nổi trên ô nhập (E 4:58).
```
+----------------------------+
|   S màn hình toàn khung    |
|   (≈85% khung cho UI)      |
| (P) PIP 14%     tag credit |
+----------------------------+
```

### LY-06 · Màn hình toàn khung không người + callout
- **Trông thế nào:** màn hình phủ 100%, không PIP; callout = viền cam bo góc quanh 1 dòng/nút hoặc vạch quét cam ngang (B 190–198 s); logo kênh góc trên-phải (B). Chữ: UI + phụ đề đốt.
- **Chuyển động:** vào bằng cắt (B) hoặc zoom vào vùng; callout tự tắt sau 0.5 s (E).
- **Giữ:** 12–20 s (B nửa sau gần như S liên tục).
- **Khi dùng:** đoạn thao tác dài.
- **Tránh:** > 40 s không đổi hình và không callout (B nửa sau dễ mệt).
- **Bằng chứng:** B 232–256 s, 800–1000 s; A 1:58–2:08, 11:32–12:50 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** callout `border: 3px solid var(--accent); border-radius: 10px`, pulse 0.5 s; zoom `scale 1→2.5` với `transform-origin` tại vùng.
- **Biến thể:** —
```
+----------------------------+
|   S màn hình toàn khung    |
|   [khung cam nhấn]         |
|   . . . phụ đề . . .       |
+----------------------------+
```

### LY-07 · Cửa sổ UI mock giữa nền tối
- **Trông thế nào:** cửa sổ (3 chấm đèn giao thông góc trái) ≈55–65% rộng, giữa khung; nền gần đen (≈#0C0C0E ước) + một màu nhấn; pill tên ở giữa trên; thanh tiến độ đáy. Chữ 3–5 từ.
- **Chuyển động:** «khung trống → điền dần»: cửa sổ mờ lên (+ phóng nhẹ), panel phải trượt vào, URL gõ từng ký tự, các lớp nội dung vào so le 0.2–0.3 s (A tr 79).
- **Giữ:** 2–6 s (A: cảnh ≈5–6 s).
- **Khi dùng:** giới thiệu công cụ/tính năng khi không có màn hình thật.
- **Tránh:** nhiều màu nhấn; icon nhiều màu.
- **Bằng chứng:** A 0:44–0:48, 1:44–2:08, 4:00–4:14, tr 79 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** `border-radius: 14px`; `gsap.from('.layer',{opacity:0,y:12,stagger:.25,duration:.3,ease:'power2.out'})`.
- **Biến thể:** —
```
+----------------------------+
|     [pill repo / tên]      |
|    +----------------+      |
|    |  cửa sổ mock   |      |
|    |  ●●●           |      |
|    +----------------+      |
|       playhead / bar       |
+----------------------------+
```

### LY-08 · Hai cửa sổ cạnh nhau
- **Trông thế nào:** hai panel đối xứng ≈44% rộng, hở ≈4% giữa, chữ «vs» hoặc mũi tên đôi giữa; trái = gốc/cũ, phải = mới/bản sao. Nền có khối hình học lơ lửng trôi lặp (A tr 420). Chữ 2–6 từ mỗi bên. Khi có người (PA/PS): người ở PIP ≈ 14% góc dưới trái như LY-05; hai cửa sổ dồn vào x 20–95%.
- **Chuyển động:** panel trái vào trước, phải trượt vào +0.3 s, nhãn «vs» bật cuối; viền cam quanh bên đang nói.
- **Giữ:** 6–15 s.
- **Khi dùng:** so sánh (miễn phí/trả phí, trước/sau, gốc/bản sao, terminal + trình duyệt).
- **Tránh:** đổi vai trái/phải giữa cảnh.
- **Bằng chứng:** A 0:48–0:54, 7:12–7:27, tr 420; B 46–50 s, 224–232 s; E 9:48, 10:02 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** `display:grid; grid-template-columns: 1fr 1fr; gap: 4%`; `outline: 3px solid var(--accent)` bật/tắt 0.3 s.
- **Biến thể:** —
```
+----------------------------+
| [ A cửa sổ ] vs [ B cửa sổ ]|
|   trái ≈44%     phải ≈44%  |
+----------------------------+
```

### LY-09 · Cửa sổ chính + panel bên
- **Trông thế nào:** UI chính 55–75% rộng, panel tính năng (danh sách, tệp, giao diện, lịch sử…) trượt từ phải rộng 25–45%; chat bên trái dim; viền cam nháy quanh panel mới. Chữ dày trong panel (tên, số, thanh tiến độ).
- **Chuyển động:** panel `x:100%→0` + blur→nét 0.4 s; chat `opacity 1→0.5`; thoát: thu lại ≈0.5 s.
- **Giữ:** 6–12 s.
- **Khi dùng:** tính năng có «thông tin phụ» (chi phí, token, danh sách file, cảnh báo).
- **Tránh:** panel > 45% rộng, che ô nhập.
- **Bằng chứng:** E 0:12, 6:14, 8:24, 10:16, tr 87.4; D 00:44 (chat | artifact, khung đỏ chọn cột); B 92–104 s (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** `position:absolute; right:0; width:35%`; `gsap.from(panel,{x:'100%',filter:'blur(10px)',duration:.4,ease:'power2.out'})`.
- **Biến thể:** —
```
+----------------------------+
|  S chính (55-75%)  | panel |
|  chat bên trái dim | 25-45%|
|  (P) PIP 14%               |
+----------------------------+
```

### LY-10 · Lưới thẻ
- **Trông thế nào:** 3–9 thẻ đều nhau (cùng cao, bo góc, icon + 2 dòng chữ), căn giữa; lưới 3×3 icon cam bo góc trên nền đen (E 0:18); card row 3–8 thẻ (A); lưới 6 thumbnail (A 1:16). Chữ 2–4 từ/thẻ.
- **Chuyển động:** thẻ bật từng cái `stagger 0.2–0.3 s` theo nhịp lời; thẻ đang nói viền cam, thẻ khác tối 0.3 s; con trỏ hover làm nổi thẻ.
- **Giữ:** 4–10 s.
- **Khi dùng:** liệt kê ≥ 3 mục, chọn trong n phương án.
- **Tránh:** > 9 thẻ; thẻ khác kích thước.
- **Bằng chứng:** A 0:14–0:24, 1:04–1:16, tr 79; E 0:18, 1:04–1:20; D 00:22, 08:38 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** `grid-template-columns: repeat(3,1fr); gap:3%`; `gsap.from(cards,{scale:.9,opacity:0,stagger:.2,duration:.35,ease:'back.out(1.4)'})`.
- **Biến thể:** —
```
+----------------------------+
|  [T lead-in]               |
|  [] [] []                  |
|  [] [] []   (3×2, 3×3)     |
+----------------------------+
```

### LY-11 · Thẻ chương / số lớn
- **Trông thế nào:** số chương rất lớn + «/tổng» nhỏ, tên mục đậm 2 dòng; nền kem hoặc tối; người là thẻ dọc phải (D tr 596.8). Ở C: tòa nhà đêm, đèn LED tạo số chương, nhãn «CHƯƠNG» nhỏ vàng, tiêu đề in hoa 2 dòng, giữ ≈2.5 s (tổng ≈3–4 s). Ở E: chữ pixel → serif trên người toàn khung (xem LY-01). Chữ ≤ 12 từ.
- **Chuyển động:** (C) câu hỏi mờ 0.4 s → nền đô thị đêm; tòa bật đèn từng ô tạo số (0.6 s); chữ trượt lên theo dòng (mask); gạch chân vàng mọc; thoát: chữ trượt ra, số tắt từng ô → mờ sang cảnh mới.
- **Giữ:** 2.5–6 s.
- **Khi dùng:** mỗi lần đổi mục (E: mục dài 30–106 s).
- **Tránh:** thẻ > 6 s; thẻ chương cho mục chỉ ≈10 s. Tòa nhà LED số chương và hạt → chữ pixel là dấu ấn riêng của video mẫu. Dấu ấn của mẫu: chỉ lấy nguyên lý, bắt buộc đổi hình thức.
- **Bằng chứng:** D tr 596.8, 05:12, 06:48; C tr 63–68; E tr 237.4; B 118–124 s (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 4 nguồn
- **Gợi ý dựng:** số `font-size:26vh`; chữ `clip-path: inset(0 0 100% 0)→inset(0)` theo dòng, `stagger .15`.
- **Biến thể:** —
```
+----------------------------+
|  N /5  (số lớn, màu nhấn)  |
|  TIÊU ĐỀ 2 DÒNG            |
|  mô tả + icon (blur→nét)   |
|                     [P dọc]|
+----------------------------+
```

### LY-12 · Thế giới minh hoạ toàn khung + phụ đề đáy
- **Trông thế nào:** toàn khung là thế giới phẳng có chiều sâu (3–4 lớp parallax); nhân vật silhouette không nét mặt; AI = quả cầu xanh lam mạng nơ-ron; phụ đề đốt 1–2 dòng, 4–10 từ, nền đen mờ, từ khoá đổi màu theo nghĩa. Nền theo chương (navy đêm, sepia, hoàng hôn). Mật độ chữ: 8–12 từ/cảnh (≈3–5 từ/giây).
- **Chuyển động:** pan ngang parallax, push-in vào ô sáng, dolly-out lộ văn phòng, lịch lật đổi thời gian.
- **Giữ:** ≈9.5 s/cảnh (C).
- **Khi dùng:** kể chuyện, ẩn dụ dài.
- **Tránh:** > 3 màu từ khoá khác nghĩa trong 1 cảnh.
- **Bằng chứng:** C 00:00, 01:08, 06:41, 09:33, 11:30, 14:28 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** 3–4 lớp ảnh `x` lệch tỉ lệ ≈0.2/0.5/1.0 để parallax; phụ đề `div` ở `bottom: 5%`.
- **Biến thể:** —
```
+----------------------------+
|   cảnh 2.5D: phố / tòa /   |
|   quầy / bàn cược          |
|   silhouette nhân vật      |
| ░░ phụ đề đốt (84–95%) ░░  |
+----------------------------+
```

### LY-13 · Câu hỏi / khẳng định lớn giữa khung
- **Trông thế nào:** chữ có chân, to, giữa khung, từ khoá vàng + gạch chân vàng ngắn; nền là cảnh truyện làm mờ hoặc nền kem trơn; cụm kết luận vàng glow (B). Chữ 4–12 từ.
- **Chuyển động:** chữ hiện từng từ trái → phải hoặc trượt lên (B 3, 9, 28 s); kết thúc mờ 0.4 s vào thẻ chương (C tr 63–68).
- **Giữ:** 2–4 s.
- **Khi dùng:** câu hỏi tu từ trước chương, chốt kết luận, hook.
- **Tránh:** > 2 câu liên tiếp.
- **Bằng chứng:** C tr 63–68; B 3 s, 9 s, 28 s; A 1:12–1:14 (một từ đỏ trong câu trắng) (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** `gsap.from('.w',{y:20,opacity:0,stagger:.12,duration:.3})`; gạch chân `scaleX 0→1`.
- **Biến thể:** —
```
+----------------------------+
|   “Câu hỏi treo”           |
|   từ khoá màu + gạch chân  |
|          (nền = cảnh mờ)   |
+----------------------------+
```

### LY-14 · Sơ đồ trung tâm (hub/orbit) hoặc luồng ngang
- **Trông thế nào:** hub 1 nút giữa + 3–5 vệ tinh (A 5:28–5:40, B 52–56 s) hoặc orbit icon quanh logo (D 01:12–01:16); luồng ngang 3–5 pill/hộp nối bằng nét (B 78–88 s; A 8:14–8:30). Nền tối + 1 nhấn; đường nối cong tự vẽ. Chữ 1–3 từ/nút.
- **Chuyển động:** nút vào so le 0.2 s; đường nối vẽ `stroke-dashoffset 1→0, 0.6 s`; chấm chạy dọc đường; nút đang nói sáng cam.
- **Giữ:** 4–12 s.
- **Khi dùng:** quy trình, kiến trúc, hệ sinh thái.
- **Tránh:** > 7 nút; đường nối cắt chữ.
- **Bằng chứng:** A 5:28–5:40, 8:14–8:30, tr 420; B 52–56, 78–92, 166–176; E 3:10–3:18, 5:08–5:16 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** SVG `path` + `strokeDasharray`; `MotionPath` cho chấm chạy.
- **Biến thể:** —
```
 hub:        flow:
   o  o      (o)──▶[ ]──▶[card]
  o (H) o     nét vẽ dần, chấm chạy
   o  o
```

### LY-15 · Dải timeline đáy + vùng xem trên
- **Trông thế nào:** khung xem trước ≈65–70% cao ở trên; dưới ≈20–25% là timeline: ruler, kim cương đỏ, waveform xanh lá, khối clip; playhead đỏ chạy. Chữ ít.
- **Chuyển động:** dải phim trượt lên từ đáy (A tr 420); marker đặt vào đỉnh waveform; khối clip kéo.
- **Giữ:** 8–20 s.
- **Khi dùng:** nói về dựng, thời lượng, nhạc, các đoạn.
- **Tránh:** dùng khi chủ đề không liên quan thời gian.
- **Bằng chứng:** A 1:24–1:34, 13:48–14:54; D 10:46–10:52 (timeline các đoạn có tên) (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** dải `y:'100%'→0, 0.5 s power3.out`; playhead `x` với `ease:'none'`.
- **Biến thể:** —
```
+----------------------------+
|   khung xem trước (S/A)    |
|  ruler ◆ ◆   ▇▇ waveform   |
|  [Video][Music] playhead đỏ|
+----------------------------+
```

## 4. Phối người + màn hình + hoạt họa

### 4.1 Chọn LY theo loại đoạn

| Loại đoạn | LY chính | LY phụ / xen | Chế độ | Ghi chú dựng |
|---|---|---|---|---|
| Mở đầu (hook, 0–40 s) | LY-01 → LY-02 | LY-07 (logo), LY-05 (cho thấy sản phẩm 6–18 s) | P → PA/PS | E: người 2 s → logo 4 s → PS demo ≈12 s → ≥ 9 icon → PA uy tín (28–38 s) |
| Khái niệm (X là gì) | LY-04 hoặc LY-03 | LY-14 (hub) | PA | Sơ đồ 3 khối bên phải, pill chạy dọc đường nối |
| Liệt kê (≥ 3 mục) | LY-10 | LY-03 (danh sách 01/02/03) | PA hoặc A | Thẻ bật theo nhịp lời; thẻ đang nói viền cam |
| So sánh | LY-08 | LY-03 (hai thanh), LY-13 | PA / A | Trái = cũ/gốc, phải = mới; «vs» giữa |
| Demo (thao tác) | LY-05 | LY-09, LY-06 | PS / S | Viền cam thay mũi tên; zoom ≈250% vào dòng lệnh |
| Số liệu / chart | LY-03 (chart mọc cột) hoặc LY-07 | LY-14 | PA / A | KPI đếm lại; popover SQL khi hỏi «số từ đâu» (D 03:28–03:44) |
| Kể chuyện | LY-12 | LY-13 (câu hỏi), LY-11 (chương) | A | Push-in/pan trong thế giới; thẻ chương là cảnh truyện |
| Kết / CTA | LY-01 | LY-03 (PDF xếp chồng), end card | P → A | E 12:22–12:44: người toàn khung → tài liệu + mũi tên chỉ xuống → end card |
| Chuyển mục | LY-11 | LY-01 (hạt chấm → chữ) | P/PA | 4–6 s mỗi lần; đừng dùng cho mục < 30 s |

### 4.2 Tỉ lệ thời lượng từng chế độ ở năm video

| Video | P | PA | A | S | PS | AS | Ghi chú |
|---|---|---|---|---|---|---|---|
| A (≈896 s) | ≈0% | ≈0% (1 lần 2 s) | ≈35% | ≈40% | 0% | ≈25% | ước từ sheet 2 s |
| B (1032 s) | 0% | 0% | ≈17% | ≈78% | 0% | ≈4% | A tập trung 0–234 s; sau đó gần như S liên tục; còn lại end card |
| C (≈1103 s) | 0% | 0% | ≈97% | 0% | 0% | ≈3% | ≈3 cảnh trình soạn code |
| D (894 s) | ≈2% | ≈33% (43 cảnh, ≈300 s) | 0% | ≈0.2% | 64% (68 cảnh, 576 s) | 0% | nhật ký gán 0:00–0:08 và 0:32–0:40 là PA; theo định nghĩa P (người toàn khung kể cả chữ nổi) tính lại ≈2% |
| E (767 s) | 11.2% | 41.8% | 2.3% | 6.8% | 35.8% | 1.6% | 124 dòng; trung bình 6.2 s/cảnh |

Số lần đổi chế độ: A ≈45–60 (≈1 lần/15–20 s); B ≈14 (hầu hết trong 234 s đầu); C gần 0; D 29 (≈1 lần/31 s); E 69 (≈1 lần/11 s). Cấu trúc lặp mỗi mục ở E (≈40–60 s): P+chữ → PA (cơ chế) → PS (demo) → PA (chi phí/tóm tắt) → mục kế.

### 4.3 Khuyến nghị cân đối cho video người + hoạt họa + màn hình

| Chế độ | Khuyến nghị | Căn cứ |
|---|---|---|
| P (+ chữ nổi) | 10–15% | E 11.2%, D ≈2%; cần ≥ 1 lần ở mở và 1 lần ở kết |
| PA | 35–40% | E 41.8%, D 35% |
| PS | 30–35% | E 35.8%; tới 64% nếu video thiên về demo (D) |
| A | 3–8% | E 2.3%: chỉ cho logo/9 icon/kể chuyện ngắn |
| S | 4–7% | E 6.8%; chỉ khi muốn người nghỉ |
| AS | 1–3% | E 1.6% |

Nếu có phần **kể chuyện** (phong cách C): mỗi chương kể chuyện ≤ ≈90 s ở chế độ A rồi quay lại người ở thẻ chương kế; đừng chạy A ≈97% khi cần giữ gương mặt người. Người không vắng quá ≈60 s (D: người có mặt ở ≈99% video; E: squircle có mặt ở mọi đoạn demo). Con số 60 s và các ngưỡng % ở bảng trên là **khuyến nghị tổng hợp**, không phải số đo trực tiếp.

## 5. Chỗ chưa chắc

- Tỉ lệ A, B, C và mốc thời gian là ước từ contact sheet 2 s (sai số ±2–4 s); D, E tính từ bảng cảnh (E: cộng ≈766 s).
- Toạ độ % PIP/cột người đo trên khung 1280×720 theo quan sát, ≈±2%; kích thước LY-02 (35–40%), LY-07 (55–65%), LY-08 (44%) là ước, chưa đo pixel.
- Hex màu là ước từ ảnh.
