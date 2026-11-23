# Từ vựng hình (VO) và chuyển động giữa các khối (MO)

Kết luận: video giảng dạy/kể chuyện kiểu này kể bằng một bộ hình rất hẹp (UI mock xám tối + một màu nhấn, icon nét, hình người khối, vài vật thể ẩn dụ) và một bộ chuyển động nối khối rất ít (đường tự vẽ, chấm chạy, kéo thả, phóng từ vật được chọn, viền nhấn tạm); sức mạnh đến từ việc giữ đồng bộ phong cách, không từ việc thêm hình.

## Contents
1. Họ hình VO-01 → VO-18
2. Luật đồng bộ phong cách
3. Cách ghép vật thành ẩn dụ
4. Chuyển động nối khối MO-01 → MO-16
5. Biên đạo mẫu (trước → sau)

Khuôn mẫu, độ tin, mã video và chế độ: xem `library-contract.md`; danh sách mã: `pattern-index.md`. «tr N» = mốc N giây trong ghi chép soi dày. Số có «≈» là ước lượng. Mã màu hex trong nhật ký đều là đoán từ ảnh, chưa đo pixel: dùng làm vai trò, không làm giá trị tuyệt đối.

---

## 1. Họ hình (VO)

### VO-01 · Cửa sổ UI mock xám tối giản
- **Trông thế nào:** khung bo góc 8–12 px, thanh tiêu đề có 3 chấm đỏ/vàng/xanh góc trái, nội dung là khối xám + chữ giả, nền khung gần đen; chiếm 55–70% chiều rộng khi đứng một mình (LY-07), 40–48% mỗi bên khi đôi (LY-08). Một màu nhấn duy nhất (cam/vàng) cho nút, viền, trạng thái.
- **Chuyển động:** «khung trống → điền dần»: cửa sổ mờ lên 0.3 s → panel phải trượt vào → từng lớp nội dung hiện so le 0.2–0.3 s (tiêu đề → thẻ → nút → hàng dưới) (A tr 79).
- **Giữ:** chưa có
- **Khi dùng:** nói về phần mềm/quy trình mà không cần quay màn hình thật; giải thích «nó trông thế này».
- **Tránh:** nhồi chữ thật quá nhỏ (không đọc được trong 2 s); dùng 2 màu nhấn.
- **Bằng chứng:** A 0:48, A tr 79, B 146–150 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `div` bo góc + `box-shadow` mờ; con cái `opacity:0,y:12 → 1,0` stagger 0.2 s, `power2.out`.
- **Biến thể:** —

### VO-02 · Thẻ (card) bo góc: icon + 2 dòng chữ + vạch trạng thái
- **Trông thế nào:** thẻ vuông/chữ nhật bo góc, icon nét ở trên, 2 dòng chữ, vạch xanh lá dưới đáy = «đạt/được chọn»; 3–8 thẻ đều nhau xếp hàng hoặc lưới 4×2 giữa khung (LY-10), chiều cao bằng nhau, khe ≈ 2% chiều rộng.
- **Chuyển động:** thẻ bật lên lần lượt theo từng ý được nói, ~1 s/thẻ (B 16–20; A 0:20), trượt từ phải vào rồi giữ.
- **Giữ:** chưa có
- **Khi dùng:** liệt kê, «có N thứ», đề cử, danh mục.
- **Tránh:** hiện cả lưới một lúc (mất nhịp theo lời); thẻ khác chiều cao.
- **Bằng chứng:** A 0:14–0:24, B 16–20, D 5 tile 0:22 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** `scale:0.9→1, opacity:0→1, 0.35s back.out(1.4)`, `stagger: 0.9` khớp lời.
- **Biến thể:** —

### VO-03 · Icon nét mảnh đơn sắc trong tile
- **Trông thế nào:** icon đường mảnh 2 px, một màu (trắng trên nền tối, đen trên nền kem, cam khi cần nhấn), đặt trong tile bo góc ≈ 10–14% chiều rộng khung.
- **Chuyển động:** blur→nét + mờ→rõ 0.3 s; icon «đang nói đến» sáng cam, các icon còn lại giảm xuống ≈ 40% opacity (E 1:04–1:20).
- **Giữ:** chưa có
- **Khi dùng:** khái niệm trừu tượng cần một biểu tượng (cài đặt, tài liệu, nhạc, kiểm tra).
- **Tránh:** trộn icon đặc với icon nét trong một khung; icon nhiều màu.
- **Bằng chứng:** A 0:08, D 0:22, E 0:18/3:10 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** SVG `stroke-width:2; fill:none`; đổi màu bằng `stroke` tween 0.25 s.
- **Biến thể:** —

### VO-04 · Chip/pill nhãn và avatar chữ
- **Trông thế nào:** viên thuốc bo tròn chứa tên (tên kho mã, tên bước, nhãn trạng thái như «Đề xuất»), cao ≈ 4–5% khung; hoặc ô tròn màu chứa chữ viết tắt thay cho người (B: ô chữ viết tắt cho cá nhân, công ty, tiền).
- **Chuyển động:** pill rơi/trượt vào đúng chỗ rồi giữ 2–4 s; pill nhỏ có thể chạy dọc một đường nối (MO-02); `scale 0.8→1 + y:-8→0, 0.3s power3.out`.
- **Giữ:** 2–4 s
- **Khi dùng:** gắn nhãn cho vật vô danh; tên công cụ/bước; trạng thái («Đề xuất», «Miễn phí»).
- **Tránh:** pill dài hơn 3 từ.
- **Bằng chứng:** A 0:44 (pill đầu cảnh), B 52–56, E 3:10 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** `border-radius:999px`, `scale 0.8→1 + y:-8→0, 0.3s power3.out`.
- **Biến thể:** —

### VO-05 · Vật thể đặc/ẩn dụ đơn (quả táo, viên kim cương, đồng xu, ổ khoá, trụ dữ liệu)
- **Trông thế nào:** một vật có khối nhẹ (đổ bóng/ánh sáng), 18–30% chiều cao khung, đặt giữa; đổi màu/trạng thái để kể (táo xanh→cam = chín; ổ khoá đóng→mở = miễn phí). Chưa thấy bộ emoji 3D đúng nghĩa trong 5 video mẫu; vật đặc ở đây là minh hoạ dựng sẵn, nếu muốn emoji 3D thì coi là họ mở rộng, chưa có bằng chứng.
- **Chuyển động:** scale-in + tia sáng flash 0.4 s, rồi đổi trạng thái 0.5 s (B 8–10; B 30–52).
- **Giữ:** chưa có
- **Khi dùng:** một ý = một vật (giá trị, bảo mật, tiền).
- **Tránh:** 2 vật đặc trong cùng khung khi ý chỉ có một.
- **Bằng chứng:** B 8–10 (gem), B 30–52 (ổ khoá), C 0:00 (tiền) (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** `scale 0→1 elastic.out(1,0.6)`; flash = vòng `radial-gradient` opacity 0.8→0.
- **Biến thể:** —

### VO-06 · Hình người khối tối giản (silhouette, avatar tròn đầu-vai)
- **Trông thế nào:** không nét mặt; nhận diện qua tư thế (ngồi bàn đèn, đứng cạnh bàn, đi giữa nhà máy); avatar tròn đầu+vai xám; hoặc avatar chữ.
- **Chuyển động:** gần như đứng yên; chỉ ánh sáng đổi (ánh vàng, nhấp đỏ khi áp lực) (C 14:16); dịch giữa các bàn khi «một người làm nhiều việc» (C 5:22).
- **Giữ:** chưa có
- **Khi dùng:** nhân vật trong câu chuyện, người dùng giả định.
- **Tránh:** thêm biểu cảm mặt (phá đồng bộ).
- **Bằng chứng:** C 1:04, C 5:22, A 0:02–0:06 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** SVG khối; ánh sáng bằng lớp `radial-gradient` đổi opacity 2 s `sine.inOut` lặp.
- **Biến thể:** —

### VO-07 · Nhân vật/mascot đơn giản có trạng thái
- **Trông thế nào:** khối tròn/pixel, 2–3 trạng thái (idle, vẫy tay, vui, nhăn); ma trắng pixel = người phụ, quái cam pixel = tác nhân chính (E); mascot xanh lá phản ứng đúng/sai (A 4:54–5:12).
- **Chuyển động:** đổi trạng thái bằng thay hình 0.15 s kèm bật nhẹ; vui = confetti rơi, sai = nhãn đỏ + mặt nhăn.
- **Giữ:** chưa có
- **Khi dùng:** phản hồi hệ thống, vai trò trong sơ đồ.
- **Tránh:** nhiều hơn 2 nhân vật có màu khác nhau trong một cảnh.
- **Bằng chứng:** A 4:02–5:12, E 2:42–3:02 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** sprite hoặc 3 SVG chồng nhau, bật `opacity` theo state.
- **Biến thể:** —

### VO-08 · Tòa nhà = công ty, cột/chồng tiền = giá trị (thế giới 2.5D)
- **Trông thế nào:** tòa cao đêm navy, cửa sổ vàng sáng; số ô cửa sáng = số nhân viên; chồng/cột tiền xanh lá dưới chân hoặc mọc cạnh = giá trị; skyline hai bên, camera ngang tầm.
- **Chuyển động:** cột tiền vươn lên từ đất 0.8 s `power2.out`; hạt vàng rơi vào từng ô cửa = chia đều; push-in vào một ô sáng = «chỉ một người».
- **Giữ:** chưa có
- **Khi dùng:** kể về công ty, doanh số, quy mô.
- **Tránh:** đổi tỉ lệ tòa/tiền giữa các cảnh (người xem tưởng giá trị đổi).
- **Bằng chứng:** C 0:00–0:06, C 1:25, C 1:44 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** lớp parallax 3 tầng (xa/giữa/gần), `scaleY` cột từ đáy `transform-origin:bottom`.
- **Biến thể:** —

### VO-09 · Cân đòn = đánh đổi
- **Trông thế nào:** cân vàng, hai đĩa mang hai vế (đống giấy vs chip, người vs màn hình), đặt trên vòng đỏ hoặc nền kệ.
- **Chuyển động:** nghiêng dần 1–1.5 s theo lời «lớn dần đến khi…» rồi thăng bằng; dùng lặp 3 lần trong video (C 3:48).
- **Giữ:** chưa có
- **Khi dùng:** chi phí vs lợi ích, A hay B, điểm cân bằng.
- **Tránh:** nghiêng mà không nói vế nào nặng hơn.
- **Bằng chứng:** C 3:48, 10:56, 16:32 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** thanh ngang `rotate:-12→0, 1.2s sine.inOut`, đĩa treo `rotate` ngược để luôn nằm ngang.
- **Biến thể:** —

### VO-10 · Quả cầu sáng = AI
- **Trông thế nào:** cầu xanh lam có mạng nơ-ron mảnh bên trong, hào quang; một quả = trợ lý, nhiều quả quanh người = đội, quả tỏa icon = công cụ.
- **Chuyển động:** nhấp scale 1→1.05 lặp 1.6 s (C 548); tài liệu/icon bay quanh theo quỹ đạo (MO-06).
- **Giữ:** chưa có
- **Khi dùng:** mọi ý «AI làm…», «tác nhân».
- **Tránh:** dùng cầu cho thứ không phải AI.
- **Bằng chứng:** C 6:55, C 5:36–5:44, C tr 548 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** `box-shadow` xanh + `scale` yoyo `repeat:-1`.
- **Biến thể:** —

### VO-11 · Nét đứt = ảo / chưa có / sẽ có
- **Trông thế nào:** viền hoặc thẻ nét đứt (thẻ thanh toán, nhà không tồn tại, ô lựa chọn nền tảng, cửa sổ đang kéo giãn); tòa nhỏ «mọc từ nền nét đứt».
- **Chuyển động:** nét đứt nhích (`stroke-dashoffset` chạy) khi «đang hình thành»; chuyển sang nét liền đặc khi «có thật».
- **Giữ:** chưa có
- **Khi dùng:** khái niệm giả định, tương lai, chỗ trống cần điền.
- **Tránh:** dùng nét đứt cho cả vật thật (mất nghĩa).
- **Bằng chứng:** C 8:14, 8:32, B 146–150, B 384–396 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** SVG `stroke-dasharray:6 6`, tween `strokeDashoffset`.
- **Biến thể:** —

### VO-12 · Bàn cược + chip, ô năm
- **Trông thế nào:** mặt bàn xanh nghiêng 2.5D, ô năm 2025…2030 vàng xếp ngang, chip đỏ/xanh/đen/vàng ở giữa.
- **Chuyển động:** chip trượt tới ô 0.5 s `power2.inOut`, ô chạm sáng vàng.
- **Giữ:** chưa có
- **Khi dùng:** dự đoán, cá cược, «khi nào».
- **Tránh:** quá 6 ô.
- **Bằng chứng:** C 0:16–0:52, C 17:58 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** perspective `rotateX(55deg)` trên mặt bàn; chip `x` tween.
- **Biến thể:** —

### VO-13 · Ranh giới tổ chức: vòng đỏ, kệ, quầy
- **Trông thế nào:** vòng đỏ elip bao nhóm chấm = «bên trong công ty»; kệ tím/xanh nhiều ngăn = thị trường; quầy gỗ có mái = chợ.
- **Chuyển động:** chấm tím gom vào vòng 1 s; vòng co/giãn khi tổ chức đổi cỡ.
- **Giữ:** chưa có
- **Khi dùng:** nói về nội bộ vs bên ngoài, thị trường.
- **Tránh:** chưa có
- **Bằng chứng:** C 2:53–4:24 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** `ellipse stroke` + chấm `x,y` về tâm `power2.inOut`.
- **Biến thể:** —

### VO-14 · Vật dựng dần: nhà nét vẽ → tô màu, tầng lớp
- **Trông thế nào:** khung nhà nét vẽ = cấu trúc (HTML), tô màu = giao diện (CSS), ô vàng dán = logic, tầng dưới đường nét đứt = hạ tầng.
- **Chuyển động:** nét vẽ 1 s → tô màu 0.6 s → hộp mới hiện cạnh.
- **Giữ:** chưa có
- **Khi dùng:** giải thích thứ gồm nhiều lớp.
- **Tránh:** chưa có
- **Bằng chứng:** B 154–182 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** `stroke-dashoffset` rồi `fill` tween.
- **Biến thể:** —

### VO-15 · Mốc thời gian: lịch lật, thanh năm LED, trục năm
- **Trông thế nào:** ô số năm/ngày kiểu đèn LED hoặc lịch lật; trục năm chạy dưới đường phố, marker tròn trượt tới năm, xe đỏ đậu ở năm sự kiện.
- **Chuyển động:** lật 0.4 s mỗi số; marker trượt 1–1.5 s.
- **Giữ:** chưa có
- **Khi dùng:** lịch sử, trước-sau, tiến trình.
- **Tránh:** chưa có
- **Bằng chứng:** C 1:08–2:00, C 1:12 (lịch lật 2026→2012), C 8:18 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** `rotateX` 0→-90→90→0 cho tờ lịch; marker `x` theo `ease:"power1.inOut"`.
- **Biến thể:** —

### VO-16 · Terminal / code (mono)
- **Trông thế nào:** nền đen, chữ mono, dòng nổi vàng/cam, banner pixel lớn khi bắt đầu; khối lệnh có viền trắng khi «sao chép».
- **Chuyển động:** dòng hiện lần lượt từ trên xuống; lệnh gõ từng ký tự (TX-02).
- **Giữ:** chưa có
- **Khi dùng:** cài đặt, lệnh, mã.
- **Tránh:** chưa có
- **Bằng chứng:** A 1:52–2:32, A 11:32–12:56 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** `font-family: mono`, mỗi dòng `opacity 0→1, 0.15s`, stagger 0.25.
- **Biến thể:** —

### VO-17 · Ảnh chụp màn hình thật trong thẻ bo góc
- **Trông thế nào:** ảnh màn hình bo góc đặt giữa nền tối hoặc full-bleed (LY-06); không khung thiết bị; credit nhỏ góc dưới phải.
- **Chuyển động:** zoom 140–250% vào vùng đang nói (TR-06), vạch quét cam ngang khi «đang phân tích» (B 190–198).
- **Giữ:** chưa có
- **Khi dùng:** minh chứng thật, demo.
- **Tránh:** chưa có
- **Bằng chứng:** B 192–198, E tr 581.4 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `scale` + `transformOrigin` đặt đúng vùng.
- **Biến thể:** —

### VO-18 · Hình người dẫn dạng squircle (khi có người thật)
- **Trông thế nào:** ảnh người bo góc kiểu squircle: lớn ≈ 40% rộng (LY-04), nhỏ ≈ 14% rộng góc dưới trái (LY-05); hoặc thẻ dọc ≈ 22% rộng cột phải (LY-03); có glow nhẹ.
- **Chuyển động:** luôn co/giãn liên tục từ toàn khung, không cắt (TR-03/TR-04); `border-radius` tween 0→28%, `width/height/x/y` tween 0.3–0.4 s `power3.inOut`.
- **Giữ:** chưa có
- **Khi dùng:** mọi chế độ có người dẫn.
- **Tránh:** chưa có
- **Bằng chứng:** E tr 38.6, E tr 501.4, D tr 6.8, D tr 94.8 (tr: soi dày).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `border-radius` tween 0→28%, `width/height/x/y` tween 0.3–0.4 s `power3.inOut`.
- **Biến thể:** —

---

## 2. Luật đồng bộ phong cách

1. **Một họ hình chính cho mỗi video:** hoặc UI mock (A, B), hoặc thế giới 2.5D (C), hoặc ảnh người + thẻ (D, E). Họ phụ chỉ làm gia vị, không chiếm quá ≈ 20% thời gian.
2. **Một màu nhấn:** cam hoặc vàng cho «chỗ phải nhìn», xanh lá chỉ cho «đạt/tiền», đỏ chỉ cho «lỗi/rủi ro/cược» (C dùng đỏ=cược, xanh lục=doanh số, vàng=một người, tím=thuật ngữ). Mỗi màu một nghĩa, giữ suốt video.
3. **Một độ dày nét icon, một bán kính bo góc** cho cả video (ví dụ 2 px, 12 px); không trộn icon nét với icon đặc.
4. **Nền tối ấm, chữ kem**; nền sáng kem chỉ dùng cho khối slide chữ hoặc cảnh người nói (D, E).
5. **Một hình thể người duy nhất** xuyên video: luôn biến hình liên tục, không thay bằng khung khác (E).
6. **Mật độ:** 1–3 cụm chữ cùng lúc (E), tiêu đề 2–6 từ (D), thẻ chữ 8–15 từ chỉ giữ khi cần đọc, 8–12 s.
7. **Nhiều hơn 5 vật cùng lúc là quá tải:** chia thành hai nhịp.
8. **Chrome lặp lại làm neo:** pill tên đầu cảnh, thanh tiến độ/playhead đáy khung, số chương cam, logo góc (A, D, E).

## 3. Cách ghép vật thành ẩn dụ

Công thức: **vật cụ thể (danh từ trong lời) + một thuộc tính đo được (cao/đầy/sáng/nghiêng) + một nhãn chữ ngắn.** Nhãn để người xem không phải đoán, thuộc tính để chuyển động kể được.

| Ý trong lời | Vật | Thuộc tính biến thiên | Ví dụ bằng chứng |
|---|---|---|---|
| Công ty / giá trị | tòa nhà + cột tiền | độ cao cột, số ô cửa sáng | C 0:00, C 1:25 |
| Một người vận hành nhiều việc | cửa sổ sáng giữa tòa tối; người + quả cầu | số quả cầu quanh người | C 0:06, C 5:36 |
| Đánh đổi, chi phí vs lợi | cân hai đĩa | độ nghiêng | C 3:48 |
| AI | quả cầu xanh lam | nhịp nhấp, số quả | C 6:55 |
| Không có thật / giả định | nét đứt | nét đứt → liền | C 8:14, 8:32 |
| Quy trình nhiều bước | chuỗi pill nối vạch | bước sáng dần | B 78–86 |
| Kiểm tra / tiêu chí | checklist, ổ khoá | ✓ bật dần | A 1:44–1:50 |
| Thời gian trôi | lịch lật, trục năm | số + marker | C 1:12 |
| Đi sâu vào một vật | push-in vào vùng, kính lúp | độ phóng 140–250% | C tr 548, B 240–246 |
| Rủi ro | khung/chữ đỏ, bảng kẹp gạch đỏ | gạch chéo | C 9:13, E 8:24 |
| Bộ nhớ, chi phí | hộp cache xanh→cam, thanh usage | màu + chiều dài | E 7:04–8:16 |

---

## 4. Chuyển động nối khối (MO)

### MO-01 · Đường nối cong tự vẽ (stroke draw)
- **Trông thế nào:** nét 2–3 px, màu nhấn hoặc trắng; đi từ nút nguồn tới đích theo đường cong nhẹ (bezier), đầu có chấm.
- **Chuyển động:** nút nguồn hiện → đường vẽ 0.5–0.8 s `power2.inOut` → nút đích mờ lên cuối đường (A tr 420).
- **Giữ:** chưa có
- **Khi dùng:** «A dẫn tới B», nguồn → sản phẩm, quan hệ.
- **Tránh:** hai đường cắt nhau không cần thiết.
- **Bằng chứng:** A tr 420, A 0:26, A 11:50 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** SVG `path`, `strokeDasharray=len; strokeDashoffset: len→0`.
- **Biến thể:** —

### MO-02 · Chấm/pill chạy dọc đường
- **Trông thế nào:** chấm cam 8–12 px hoặc pill nhỏ (nhãn hành động ngắn) chạy trên đường nét đứt giữa 2–3 khối.
- **Chuyển động:** một lượt 1.2–1.8 s qua cả đường, lặp 2 lần rồi dừng ở khối cuối; khối cuối sáng khi chấm tới. `duration:1.5, ease:"none"`.
- **Giữ:** chưa có
- **Khi dùng:** dòng dữ liệu, tiến trình, «đi qua các bước».
- **Tránh:** chưa có
- **Bằng chứng:** E 3:10–3:18, B 166–176 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** GSAP MotionPath hoặc `offset-path`; `duration:1.5, ease:"none"`.
- **Biến thể:** —

### MO-03 · Kéo thả vào thư mục
- **Trông thế nào:** vài icon thẻ nổi (bóng, viền sáng), một thư mục lớn cam đất bên phải; con trỏ nhỏ.
- **Chuyển động:** con trỏ trỏ vào icon → nhãn tên hiện → kéo icon vào thư mục 0.5 s `power2.inOut`, icon thu nhỏ về 0; lặp 3–4 icon; xong thì lớp nổi mờ 0.3 s.
- **Giữ:** chưa có
- **Khi dùng:** «gom lại», «cho vào», «nhập vào một nơi».
- **Tránh:** chưa có
- **Bằng chứng:** D tr 6.8 (tr: soi dày).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** con trỏ `x,y` timeline, icon `x,y,scale` theo con trỏ.
- **Biến thể:** —

### MO-04 · Chọn thẻ → phóng thành cảnh (container transform)
- **Trông thế nào:** lưới ≈ 6 thẻ trong một cửa sổ, con trỏ trỏ một thẻ.
- **Chuyển động:** thẻ khác tối dần 0.3 s → thẻ chọn giãn từ vị trí của nó lấp đầy cửa sổ 0.6 s → tiêu đề cửa sổ đổi → thanh timeline mọc ở đáy (A tr 79). Chính là TR-05.
- **Giữ:** chưa có
- **Khi dùng:** «chọn một trong N rồi bắt đầu».
- **Tránh:** chưa có
- **Bằng chứng:** A tr 79 (soi dày).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** FLIP: lấy `getBoundingClientRect` thẻ → tween `left/top/width/height` về khung, `power3.inOut`.
- **Biến thể:** —

### MO-05 · Tách / gộp
- **Trông thế nào:** một khối tách làm hai (so sánh), hoặc nhiều chip gộp vào vòng/ô (chấm tím vào vòng đỏ; hạt tiền vào ô cửa; thẻ đổi cột giữa hai cột trạng thái).
- **Chuyển động:** tách = hai nửa trượt ra 0.5 s kèm nhãn «vs» bật; gộp = các phần tử hút về tâm 0.6–1 s, `power2.in` rồi ngừng mềm.
- **Giữ:** chưa có
- **Khi dùng:** chia nhóm, hợp nhất, phân bổ.
- **Tránh:** chưa có
- **Bằng chứng:** B 46–50, C 1:44, C 2:53–4:24, D 13:56 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** `x/y` tween về điểm đích; `scale 1→0.6` khi vào.
- **Biến thể:** —

### MO-06 · Quỹ đạo quanh tâm (orbit/hub)
- **Trông thế nào:** logo hoặc nút ở tâm, 4–6 pill/icon trên vòng tròn bán kính ≈ 22–30% chiều cao.
- **Chuyển động:** vệ tinh bung từ tâm ra 0.6 s `back.out`, rồi xoay chậm 20–30 s/vòng; hoặc đứng yên và nối bằng đường tự vẽ.
- **Giữ:** chưa có
- **Khi dùng:** một thứ kết nối nhiều thứ, hệ sinh thái.
- **Tránh:** chưa có
- **Bằng chứng:** D 1:12–1:16, B 52–56, A 5:28–5:40, E 9:08–9:14 (nhật ký).
- **Độ tin:** ước · 4 nguồn
- **Gợi ý dựng:** group `rotation: 360, repeat:-1, ease:"none"`; con counter-rotate để chữ không xoay.
- **Biến thể:** —

### MO-07 · Khối trôi lặp (idle float)
- **Trông thế nào:** hình hình học nhỏ/quả cầu/icon lơ lửng quanh cửa sổ chính.
- **Chuyển động:** `y ±6–10 px`, 3–4 s, `sine.inOut`, yoyo, pha lệch giữa các vật; quả cầu AI scale 1→1.05 (1.6 s).
- **Giữ:** chưa có
- **Khi dùng:** làm cảnh sống khi lời nói dài hơn hình mới; giữ khung không chết.
- **Tránh:** trôi mạnh làm lấn chữ.
- **Bằng chứng:** A tr 420, C tr 548 (soi dày).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `gsap.to(el,{y:"+=8",yoyo:true,repeat:-1,duration:3.2,ease:"sine.inOut"})`.
- **Biến thể:** —

### MO-08 · Viền nhấn tạm
- **Trông thế nào:** viền cam/vàng bo góc dày 2–3 px quanh nhóm nút, panel hoặc dòng chữ, cách mép ≈ 6 px.
- **Chuyển động:** hiện 0.15 s → giữ 0.5 s → tắt 0.2 s (E tr 87.4); với chữ trong chat, khung trôi chậm sang dòng kế, không nhấp nháy.
- **Giữ:** 0.5 s (E tr 87.4)
- **Khi dùng:** «nhìn vào đây» thay cho mũi tên.
- **Tránh:** chưa có
- **Bằng chứng:** E tr 87.4, A tr 202, E 5:02 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `outline` hoặc `div` viền; `opacity 0→1→0`, `scale 1.04→1`.
- **Biến thể:** —

### MO-09 · Con trỏ thao tác
- **Trông thế nào:** mũi tên trắng ≈ 2% khung, đổ bóng mềm.
- **Chuyển động:** quét qua các đoạn/thẻ 0.6–1 s (`power2.inOut`), dừng 0.2 s trước mỗi «click»; ô bình luận bật tại vị trí con trỏ (scale 0.9→1 + mờ→rõ).
- **Giữ:** chưa có
- **Khi dùng:** demo không quay màn hình thật.
- **Tránh:** chưa có
- **Bằng chứng:** A tr 202, A 1:16–1:20, D tr 6.8 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `x,y` theo mảng điểm, click = `scale 1→0.85→1, 0.12s`.
- **Biến thể:** —

### MO-10 · Đếm số (counter)
- **Trông thế nào:** số lớn (km, giờ, từ, tiền, điểm) nhảy lên/xuống; kèm đơn vị nhỏ.
- **Chuyển động:** đếm 0.8–1.5 s `power2.out`, dừng ở giá trị đúng; chữ số dùng `tabular-nums` để không rung.
- **Giữ:** chưa có
- **Khi dùng:** số liệu, kết quả đo, tiến trình.
- **Tránh:** chưa có
- **Bằng chứng:** A 3:36–3:58, A 6:26–6:36, B 182–190, D 3:28–3:44 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** `gsap.to(obj,{v:target,duration:1.2,onUpdate:()=>el.textContent=fmt(obj.v)})`.
- **Biến thể:** —

### MO-11 · Cột mọc / thanh dài ra
- **Trông thế nào:** cột/thanh cam trên nền tối, số hiện theo cột.
- **Chuyển động:** mỗi cột mọc 0.5 s, so le 0.3 s, số đếm cùng lúc.
- **Giữ:** chưa có
- **Khi dùng:** so sánh độ lớn; giảm dần («ngày → phút»).
- **Tránh:** chưa có
- **Bằng chứng:** A 1:08–1:12, D 4:46–4:56, D 0:54–0:58 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** `scaleY 0→1`, `transformOrigin:"bottom"`.
- **Biến thể:** —

### MO-12 · Trượt vào so le (stagger entrance)
- **Trông thế nào:** thẻ/dòng vào từ phải hoặc từ dưới 24–40 px, mờ→rõ; hướng vào một chiều trong cả cảnh.
- **Chuyển động:** cách nhau 0.2–0.3 s (A tr 79, B 16–20).
- **Giữ:** chưa có
- **Khi dùng:** mọi danh sách/lớp nội dung.
- **Tránh:** vào từ nhiều hướng khác nhau.
- **Bằng chứng:** A tr 79, B 78–86 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `from:{x:40,opacity:0}, stagger:0.25, duration:0.4, ease:"power2.out"`.
- **Biến thể:** —

### MO-13 · Làm tối phần còn lại (dim-others)
- **Trông thế nào:** các phần tử không được nói tới giảm xuống 30–40% opacity, phần tử đang nói viền cam.
- **Chuyển động:** giảm trong 0.3 s; đổi sang phần tử kế thì hoán đổi (E 1:04–1:20, A tr 79).
- **Giữ:** chưa có
- **Khi dùng:** 3–4 lựa chọn, nói lần lượt từng cái.
- **Tránh:** chưa có
- **Bằng chứng:** E 1:04–1:20, A tr 79 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `gsap.to(others,{opacity:.35,duration:.3})`.
- **Biến thể:** —

### MO-14 · Pop tại điểm (bubble/ô ghi chú)
- **Trông thế nào:** bubble xuất hiện tại vị trí con trỏ; đuôi bubble trỏ vào điểm.
- **Chuyển động:** `scale 0.9→1`, mờ→rõ, 0.25 s `back.out(1.6)`.
- **Giữ:** chưa có
- **Khi dùng:** ghi chú, phản hồi, lời nhắc.
- **Tránh:** chưa có
- **Bằng chứng:** A tr 202, A 3:32–3:36 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### MO-15 · Thanh tiến độ, playhead, vạch quét
- **Trông thế nào:** playhead chạy qua chip/clip; vạch quét cam ngang qua ảnh chụp màn hình khi nói «đang phân tích» (B 190–198); thanh pass-mark dâng 3 vòng (A 6:48–6:56).
- **Chuyển động:** playhead chạy đều (`ease:"none"`); vạch quét 1–1.5 s.
- **Giữ:** chưa có
- **Khi dùng:** thời gian, tiến trình, kiểm tra.
- **Tránh:** chưa có
- **Bằng chứng:** A 3:20–3:26, A 6:48–6:56, B 190–198 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### MO-16 · Máy quay trong thế giới (push-in, pan, dolly-out)
- **Trông thế nào:** push-in ≈ 140% vào vật then chốt kèm vật mới trượt vào cạnh (C tr 548); pan ngang có parallax qua phố (C 1:08–1:12); dolly-out lùi từ vật ra văn phòng (C 9:13–9:20). Liên quan TR-06, TR-08, TR-13.
- **Chuyển động:** push-in ≈ 140%, pan ngang parallax, dolly-out lùi (xem TR-06, TR-08, TR-13).
- **Giữ:** chưa có
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** C tr 548, C 1:08–1:12, C 9:13–9:20 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** container `scale 1→1.4, transformOrigin` tại vật, các lớp nền `x` lệch tốc độ 0.3/0.6/1.
- **Biến thể:** —

---

## 5. Biên đạo mẫu (trước → sau)

**Danh sách 3 mục được nói lần lượt (≈ 9 s):**
1. 0.0 s: thẻ 1, 2, 3 đã nằm hàng ngang, cả ba ở 35% opacity.
2. Lời nói tới mục 1: thẻ 1 lên 100%, viền cam 0.5 s, icon blur→nét 0.3 s (MO-13 + MO-08).
3. Mục 2 và 3: lặp, thẻ trước về 60% (đã nói, vẫn thấy).
4. Câu chốt: cả ba lên 100%, vạch xanh dưới đáy mỗi thẻ mọc 0.3 s.

**Sơ đồ A → B → C có chấm chạy (≈ 8 s):**
1. A hiện (0.3 s) → đường vẽ tới B (0.6 s) → B hiện.
2. Chấm cam chạy A→B (1.2 s); B «bật sáng» khi chấm tới.
3. Lặp đoạn B→C; chấm chạy một lần nữa A→C để chốt.
