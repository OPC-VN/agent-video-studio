# Hiệu ứng chữ (TX) và dựng infographic (IG)

Kết luận: chữ trong video mẫu luôn «vào bằng blur→nét hoặc trượt có mask, ở lại đúng thời gian đọc, ra bằng blur/mờ», chỉ một từ khoá đổi màu mỗi câu; còn infographic luôn dựng từng phần theo thứ tự lời nói, mỗi phần hiện đúng lúc từ của nó được nói.

## Contents
1. Thứ bậc chữ và thời gian đọc
2. Hiệu ứng chữ TX-01 → TX-16
3. Dựng infographic IG-01 → IG-12
4. Nhịp khớp lời: quy tắc chung

Khuôn mẫu, độ tin, mã video và chế độ: xem `library-contract.md`; danh sách mã: `pattern-index.md`. «tr N» = mốc N giây trong ghi chép soi dày. Số có «≈» là ước lượng.

---

## 1. Thứ bậc chữ và thời gian đọc

| Bậc | Vai | Cỡ ≈ (so với chiều cao khung 1080) | Số chữ | Thời gian giữ |
|---|---|---|---|---|
| T1 | Số chương / số lớn | 25–40% chiều cao (D: số «4» cỡ rất lớn) | 1–3 ký tự | 2.5–6 s |
| T2 | Tiêu đề chương / câu hỏi / khẳng định | 6–9% | 2–8 từ, 1–2 dòng | 2.5–6 s (D, E 4–6 s; C thẻ chương ≈ 3–4 s) |
| T3 | Nhãn sơ đồ, pill, kicker | 2.5–3.5% | 1–3 từ | 2–4 s (E) |
| T4 | Phụ đề đáy | 3.5–4.5% | 4–10 từ/cụm | 2–4 s (C) |
| T5 | Thẻ chữ đọc được (card, bảng) | 2.8–3.5% | 8–15 từ | 8–12 s (E) |
| T6 | Credit/nguồn | 1.8–2.2% | tên ngắn | suốt cảnh, không animate |

**Thời gian đọc (rút từ bằng chứng):**
- Phụ đề 8–12 từ/cảnh giữ 2–4 s ≈ **0.3–0.5 s/từ** (C).
- Tiêu đề 2–6 từ giữ 2–6 s (D, E): tối thiểu **1.5 s + 0.35 s/từ** (ngưỡng chung, cũng ghi ở `workflow.md` bước 4).
- Thẻ 8–15 từ giữ 8–12 s ≈ **0.7–1.0 s/từ** (E): chỉ đủ để đọc, không để vừa đọc vừa nghe ý khác.
- Nhãn số/giá 1–2 s mỗi nhãn (C); caption kinetic 1–2 s mỗi câu (A).
- 1–3 cụm chữ cùng lúc (E); tiêu đề lớn đúng 1 cụm. Hơn 3 cụm: tách nhịp.
- Quy tắc bấm: chữ phải **vào trước** từ khoá được nói 0–0.3 s, **ở lại** tối thiểu thời gian đọc, **ra** trước khi cảnh đổi 0.3–0.4 s (blur/mờ).

---

## 2. Hiệu ứng chữ (TX)

### TX-01 · Blur → nét + mờ → rõ
- **Trông thế nào:** tiêu đề, nhãn, thẻ nội dung nằm đúng vị trí cuối ngay từ đầu, chỉ khác độ mờ.
- **Chuyển động:** `blur ≈ 20px, opacity 0` → `blur 0, opacity 1` trong 0.3–0.4 s; thoát ngược lại 0.3–0.4 s (E tr 38.6, tr 115.4). Quy tắc chung của E: vào = blur→nét, ra = nét→blur.
- **Giữ:** chưa có
- **Khi dùng:** mặc định cho mọi chữ không có hiệu ứng riêng.
- **Tránh:** blur > 0.6 s (trông như lỗi lấy nét).
- **Bằng chứng:** E tr 38.6, E tr 115.4, D 02:00 (blur-in) (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `filter: blur(20px)→blur(0), opacity 0→1, 0.4s power2.out`.
- **Biến thể:** —

### TX-02 · Gõ từng ký tự (có caret)
- **Trông thế nào:** dòng mono hoặc ô nhập, caret nhấp nháy ở cuối; có thể kèm prefix `>`.
- **Chuyển động:** 25–40 ký tự/giây (≈ 0.03 s/ký tự); lệnh dài ≥ 40 ký tự gõ nhanh hơn hoặc cắt (A tr 79, D tr 94.8).
- **Giữ:** chưa có
- **Khi dùng:** lệnh, prompt, URL, câu hỏi gửi cho hệ thống.
- **Tránh:** gõ cả đoạn dài khi lời đã nói xong.
- **Bằng chứng:** A tr 79 (URL), B 78–86 (prompt), A 5:20, D tr 94.8 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** TextPlugin hoặc cắt `textContent` theo `progress`, `ease:"none"`.
- **Biến thể:** —

### TX-03 · Hạt tụ thành chữ pixel rồi đổi font
- **Trông thế nào:** tiêu đề chương trên cảnh người toàn khung; số chương nhỏ cam trên tiêu đề, phụ đề nhỏ dưới.
- **Chuyển động:** hạt chấm bay vào từ trên 0.6 s → tụ thành chữ pixel/dot-matrix 0.4 s → hoà tan sang chữ có chân (serif) 0.3 s; tổng ≈ 1.3 s (E tr 237.4).
- **Giữ:** chưa có
- **Khi dùng:** mở mục mới, tiêu đề nên «đắt» nhưng không cần cảnh riêng.
- **Tránh:** dùng cho mọi dòng chữ. Hạt → chữ pixel → chữ có chân là dấu ấn riêng của video mẫu. Dấu ấn của mẫu: chỉ lấy nguyên lý, bắt buộc đổi hình thức.
- **Bằng chứng:** E tr 237.4, E 2:02/3:58/6:06 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** canvas hạt hội tụ hoặc chữ pixel (`font` pixel) `opacity` crossfade sang serif 0.3 s, thêm `blur`.
- **Biến thể:** —

### TX-04 · Trượt lên theo dòng có mask
- **Trông thế nào:** mỗi dòng nằm trong «hộp cắt» (`overflow:hidden`); nhãn nhỏ vàng báo chương trên, tiêu đề in hoa 2 dòng dưới, gạch chân vàng mọc sau.
- **Chuyển động:** từng dòng trượt từ `y:100%→0` 0.4 s, so le 0.12 s; gạch chân mở rộng 0.3 s; thoát: chữ trượt ra theo dòng, đèn số tắt (C tr 63–68).
- **Giữ:** ≈ 2.5 s
- **Khi dùng:** thẻ chương, tiêu đề lớn.
- **Tránh:** chưa có
- **Bằng chứng:** C tr 63–68 (soi dày).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** `gsap.from(".line",{yPercent:100,stagger:.12,duration:.4,ease:"power3.out"})` trong cha `overflow:hidden`.
- **Biến thể:** —

### TX-05 · Từ khoá đổi màu / nền nhấn
- **Trông thế nào:** trong câu trắng, một cụm khoá đổi màu theo nghĩa: đỏ = cược/rủi ro, xanh lục = tiền/đạt, vàng = «một người», tím = thuật ngữ (C); cam cho từ nhấn tiêu đề (D); một từ đỏ cuối câu (A 1:12). Có thể thêm nền nhấn mờ sau cụm.
- **Chuyển động:** chữ trắng vào trước, từ khoá đổi màu 0.2 s đúng lúc được nói.
- **Giữ:** chưa có
- **Khi dùng:** mọi câu có một ý chính.
- **Tránh:** ≥ 2 từ khoá/câu; màu không có nghĩa cố định.
- **Bằng chứng:** C (phụ đề có từ khoá đổi màu; không mốc), D 00:56–01:04, A 1:12–1:14, A 3:42–3:48 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** `span` + `color` tween 0.2 s; nền nhấn `background-size 0→100%`.
- **Biến thể:** —

### TX-06 · Gạch ngang chữ cũ → chữ mới
- **Trông thế nào:** từ cũ có vạch ngang xuyên, nhãn đen/trắng mới đè lên ngay dưới/trên (chữ chỉ đơn vị thời gian, đổi từ lớn sang nhỏ).
- **Chuyển động:** vạch vẽ 0.3 s từ trái sang phải → chữ cũ mờ xuống 40% → nhãn mới vào 0.3 s (D 04:50–04:54); `scaleX 0→1` trên `::after`, `transformOrigin:left`.
- **Giữ:** chưa có
- **Khi dùng:** trước → sau, sai → đúng, quyết định bị loại.
- **Tránh:** gạch đỏ chữ không phải cái bị loại.
- **Bằng chứng:** D 04:50–04:54, C 9:13 (bảng kẹp gạch đỏ), B (chữ đỏ + gạch chéo; không mốc) (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** `scaleX 0→1` trên `::after`, `transformOrigin:left`.
- **Biến thể:** —

### TX-07 · Phụ đề đáy nền tối mờ
- **Trông thế nào:** 1–2 dòng sans đậm trắng, nền đen mờ, căn giữa, cách mép đáy ≈ 6–8%; từ khoá đổi màu (TX-05).
- **Chuyển động:** đổi câu bằng cắt hoặc mờ chéo 0.15 s, khớp nhịp cắt hình; 4–10 từ/cụm.
- **Giữ:** chưa có
- **Khi dùng:** thế giới minh hoạ không người nói (LY-12); phụ đề đốt cho video thuyết minh.
- **Tránh:** chồng lên chữ đồ hoạ ở đáy.
- **Bằng chứng:** C (mọi cảnh), B từ 640 s (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** thanh `bottom:7%`, `padding`, `background: rgba(0,0,0,.55)`; chia theo cue lời.
- **Biến thể:** —

### TX-08 · Số LED / lịch lật
- **Trông thế nào:** số kiểu ô đèn (số bằng ô cửa sáng của tòa nhà), hoặc lịch lật.
- **Chuyển động:** ô bật từng ô tạo số 0.6 s (C tr 63–68); lịch lật 0.4 s/số (C 1:12).
- **Giữ:** chưa có
- **Khi dùng:** năm, số chương, ngày.
- **Tránh:** tòa nhà LED số chương là dấu ấn riêng của video mẫu. Dấu ấn của mẫu: chỉ lấy nguyên lý, bắt buộc đổi hình thức.
- **Bằng chứng:** C tr 63–68, C 1:12, C 8:18 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 1 nguồn
- **Gợi ý dựng:** lưới ô bật `opacity` stagger; lật `rotateX`.
- **Biến thể:** —

### TX-09 · Số chương lớn «N /tổng»
- **Trông thế nào:** số rất lớn màu nhấn bên trái + «/5» nhỏ, tên mục đậm 2 dòng, dòng mô tả kèm icon xuất hiện sau ≈ 1.4 s.
- **Chuyển động:** số blur→nét 0.4 s, tên trượt (TX-04), mô tả vào trễ.
- **Giữ:** chưa có
- **Khi dùng:** mốc nhịp mỗi mục trong video dạy.
- **Tránh:** chưa có
- **Bằng chứng:** D tr 596.8, E 01–09 (số cam nhỏ; không mốc) (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** số `font-size ≈ 28vh`, `opacity .0→1`.
- **Biến thể:** —

### TX-10 · Hiện từng từ trái → phải + gạch quét
- **Trông thế nào:** từng từ hiện từ trái sang phải, gạch cam quét dưới cụm tiêu đề.
- **Chuyển động:** từng từ vào cách 0.15–0.25 s, gạch cam quét 0.4 s (B 4–8).
- **Giữ:** chưa có
- **Khi dùng:** tuyên bố mở đầu 5–8 từ.
- **Tránh:** chưa có
- **Bằng chứng:** B 4–8, B 9, B 28 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** tách từ → `stagger:.2, y:20, opacity:0`.
- **Biến thể:** —

### TX-11 · Từ sáng theo nhịp giọng (caption đồng bộ)
- **Trông thế nào:** từng từ trong câu sáng lên, các từ còn lại mờ 50%; waveform chạy bên dưới (A 10:38–10:50).
- **Chuyển động:** sáng đúng khi từ được nói; mỗi từ `color` tween tại `t = start_i`.
- **Giữ:** chưa có
- **Khi dùng:** nhấn nhịp, video dạy ngôn ngữ, khi có timestamp từng từ.
- **Tránh:** khi không có timestamp chính xác.
- **Bằng chứng:** A 10:38–10:50, A 12:14–12:20 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** mỗi từ `color` tween tại `t = start_i`.
- **Biến thể:** —

### TX-12 · Kinetic text lớn + một từ đỏ
- **Trông thế nào:** câu hook in hoa đậm 7–10% chiều cao, có một từ đỏ/cam; số đếm (km, giây) bên cạnh.
- **Chuyển động:** từng cụm vào 0.3 s, số đếm cùng lúc; 1–2 s mỗi câu.
- **Giữ:** 1–2 s mỗi câu
- **Khi dùng:** hook mở đầu, câu chốt.
- **Tránh:** chưa có
- **Bằng chứng:** A 3:42–3:58, A 1:12 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** `stagger`, từ nhấn tween màu.
- **Biến thể:** —

### TX-13 · Khung nhấn bao dòng chữ
- **Trông thế nào:** khung cam bo quanh 1 từ/dòng trong khối chữ (cụm chỉ chi phí, cụm chỉ quy ước dự án trong ảnh chat).
- **Chuyển động:** khung trôi sang dòng kế 0.3 s, không nhấp nháy; `div` viền, `x,y,width` tween tới `getBoundingClientRect` của từ.
- **Giữ:** chưa có
- **Khi dùng:** chỉ ra từ cụ thể trong ảnh màn hình/chat.
- **Tránh:** chưa có
- **Bằng chứng:** E 5:00, 9:22 (mốc giây theo nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** `div` viền, `x,y,width` tween tới `getBoundingClientRect` của từ.
- **Biến thể:** —

### TX-14 · Chữ đánh máy trên giấy
- **Trông thế nào:** tờ giấy nâu, tiêu đề tài liệu cổ (tên công trình kèm năm).
- **Chuyển động:** gõ từng ký tự, kèm chuyển sepia.
- **Giữ:** chưa có
- **Khi dùng:** trích tài liệu, mốc lịch sử.
- **Tránh:** chưa có
- **Bằng chứng:** C 3:58 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### TX-15 · Đóng dấu / chữ đỏ gạch chéo
- **Trông thế nào:** dấu nhãn đỏ; dòng lỗi đỏ trong code, chip X đỏ (B 30–52, B 60–66).
- **Chuyển động:** dấu đập xuống `scale 1.4→1` 0.2 s rồi thẻ tan rã.
- **Giữ:** chưa có
- **Khi dùng:** loại bỏ, cảnh báo, lỗi.
- **Tránh:** chưa có
- **Bằng chứng:** B 30–52, B 60–66 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### TX-16 · Kicker nhỏ cách chữ rộng
- **Trông thế nào:** nhãn cam 1–3 từ in hoa, `letter-spacing ≈ 0.2em`, ngay trên headline (B, nhãn giới thiệu kênh); số mục nhỏ «01…09» (E).
- **Chuyển động:** vào trước headline 0.2 s, blur→nét.
- **Giữ:** chưa có
- **Khi dùng:** đặt ngữ cảnh/ngăn mục.
- **Tránh:** chưa có
- **Bằng chứng:** B 4–8 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

---

## 3. Dựng infographic (IG)

Mỗi loại ghi: bố cục ở **Trông thế nào**, thứ tự xuất hiện ở **Chuyển động**, nhịp khớp lời ở **Giữ**.

### IG-01 · Danh sách số (3–8 mục)
- **Trông thế nào:** LY-10 lưới thẻ hoặc cột dọc có số 01/02/03 (D danh sách 01/02/03); số lớn trái, chữ phải.
- **Chuyển động:** tiêu đề → mục 1 → … → mục N; mỗi mục: số blur→nét, tiêu đề, một dòng mô tả.
- **Giữ:** mục hiện khi lời bắt đầu nói tới nó (trễ ≤ 0.3 s), cách nhau theo lời, ≈ 1 s/thẻ khi lời liệt kê nhanh (B 16–20); mục đã nói giảm còn 60%.
- **Khi dùng:** chưa có
- **Tránh:** hiện hết một lúc; > 8 mục (chia hai khung).
- **Bằng chứng:** B 16–20, A 0:20, D tr 94.8 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** MO-12, `stagger` đặt theo cue.
- **Biến thể:** —

### IG-02 · So sánh 2 cột
- **Trông thế nào:** LY-08 hoặc TR-14; trái/phải đối xứng, «VS» ở giữa, cột trái màu lạnh/xám = cũ, phải màu nhấn = mới.
- **Chuyển động:** tiêu đề → panel trái trượt vào → panel phải trượt vào → «VS» bật → thuộc tính từng hàng lần lượt (cùng hàng hai cột cùng lúc).
- **Giữ:** panel trái khi nói vế A, phải khi nói vế B; thuộc tính khi nói từng điểm; chốt: cột thắng lên 100%, cột kia 50%.
- **Khi dùng:** chưa có
- **Tránh:** màu không nhất quán (trái cũ có lúc đỏ, lúc xanh).
- **Bằng chứng:** B 46–50, B 224–232, A 0:48–0:54, A 7:12–7:27 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** hai timeline con, `x:-60→0` và `x:60→0`.
- **Biến thể:** —

### IG-03 · Trước / sau
- **Trông thế nào:** cùng một khung, trạng thái A → trạng thái B tại chỗ (không tách đôi); hoặc LY-08 kèm nhãn «Trước/Sau».
- **Chuyển động:** trạng thái trước (giữ ≥ 2 s) → dấu chuyển (mũi tên, TX-06 gạch ngang) → trạng thái sau; hai lớp chồng, lớp trước `opacity 1→0`, lớp sau `0→1`, 0.5 s.
- **Giữ:** đổi ngay khi lời nói «bây giờ/sau khi»; đo bằng số (đếm MO-10) cho thấy chênh lệch.
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** D 04:46–04:56 (đơn vị thời gian lớn → nhỏ), A 7:12–7:27 (gốc/bản sao), C 01:12 (lịch 2026→2012), E 7:04–8:16 (cache lạnh→ấm) (nhật ký).
- **Độ tin:** ước · 4 nguồn
- **Gợi ý dựng:** hai lớp chồng, lớp trước `opacity 1→0`, lớp sau `0→1`, 0.5 s.
- **Biến thể:** —

### IG-04 · Flowchart / luồng ngang
- **Trông thế nào:** LY-14; 3–5 khối ngang, đường nối, mũi tên; pill bước màu khác nhau mỗi bước (B: Ý tưởng xanh, Thiết kế tím, Code cam, Kiểm thử vàng, Phát hành xanh lá).
- **Chuyển động:** khối 1 → đường vẽ → khối 2 → … → chấm cam chạy qua cả đường (MO-02) → khối cuối sáng.
- **Giữ:** mỗi khối vào khi lời nhắc tới tên bước (≈ 1 s/khối); chấm chạy khi lời nói «chạy qua tất cả».
- **Khi dùng:** chưa có
- **Tránh:** > 5 khối trên một dòng; đường bắt chéo.
- **Bằng chứng:** B 78–92, B 166–176, E 3:52–3:58, A 5:28–5:34 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** khối `scale .9→1`; MO-01 + MO-02.
- **Biến thể:** —

### IG-05 · Hub / orbit
- **Trông thế nào:** LY-14; nút trung tâm, 4–6 vệ tinh.
- **Chuyển động:** hub vào → vệ tinh bung ra từng cái hoặc vẽ đường tới từng cái → caption cam ở đáy.
- **Giữ:** mỗi vệ tinh khớp một ý được nói (≈ 1 s/vệ tinh); không nói thì bung cùng lúc 0.6 s.
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** B 52–56, D 1:12–1:16, A 5:28–5:40, E 9:08–9:14, C (mạng tím; không mốc) (nhật ký).
- **Độ tin:** ước · 5 nguồn
- **Gợi ý dựng:** MO-06.
- **Biến thể:** —

### IG-06 · Timeline
- **Trông thế nào:** LY-15 (dải timeline đáy + vùng xem trên) hoặc trục năm chạy ngang giữa.
- **Chuyển động:** trục → mốc 1 → marker trượt tới mốc 2 → … mỗi mốc có nhãn năm + 1 cụm chữ; ruler có diamond/marker đỏ; marker `x` timeline, nhãn blur→nét.
- **Giữ:** marker trượt 1–1.5 s đúng khi lời nói chuyển mốc; vật đặc trưng xuất hiện ở mốc (xe đỏ đậu).
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** C 1:08–2:00, A 1:24–1:34 (marker khớp đỉnh nhạc), A 6:56–7:12 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** marker `x` timeline; nhãn blur→nét.
- **Biến thể:** —

### IG-07 · Biểu đồ cột mọc
- **Trông thế nào:** bảng số trái + khung biểu đồ phải (A 1:08–1:12), hoặc biểu đồ giữa.
- **Chuyển động:** trục/nhãn → cột 1 + số → cột 2 + số … → cột nhấn đổi màu cam.
- **Giữ:** mỗi cột 0.5 s, cách 0.3 s; đếm số cùng lúc; đích cuối ghi chú «không phải số đo» nếu số minh hoạ (B 136–146).
- **Khi dùng:** chưa có
- **Tránh:** trục không có đơn vị; hai màu nhấn.
- **Bằng chứng:** A 1:08–1:12, D 02:28–02:30, D 04:46–04:56, B 136–146 (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** `scaleY` + counter (MO-10, MO-11).
- **Biến thể:** —

### IG-08 · Bảng / ma trận
- **Trông thế nào:** bảng 3–5 dòng, 3–4 cột (cột: #, thời gian, việc, chữ trên màn hình); hoặc ma trận 2×2.
- **Chuyển động:** khung bảng → dòng tiêu đề → từng dòng theo thời gian nói; ô nhấn nền vàng/tô viền.
- **Giữ:** mỗi dòng ≈ 1.5–2 s; dòng hiện tại sáng, dòng cũ mờ 60%.
- **Khi dùng:** chưa có
- **Tránh:** hơn 5 dòng cùng lúc (khó đọc); chữ nhỏ hơn 2.8% chiều cao.
- **Bằng chứng:** A 6:04–6:10 (storyboard), D 11:20 (bảng nhiều cột cảnh/lời/ảnh), A 12:14–12:20 (bảng word timing) (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** hàng `opacity .35→1`, nền nhấn `scaleX`.
- **Biến thể:** ma trận 2×2 chưa thấy trong mẫu: ghi «≈ suy ra».

### IG-09 · Checklist tick
- **Trông thế nào:** khối chữ 3–5 dòng có ô vuông hoặc điểm đầu dòng; có thể kèm ổ khoá/khung video bên cạnh (A 1:46–1:50).
- **Chuyển động:** dòng 1 hiện → ✓ xanh bật → dòng 2 … hoặc cả danh sách mờ → ✓ bật lần lượt; ✗ đỏ cho dòng không đạt.
- **Giữ:** ✓ bật đúng lúc nói «đạt/xong» (≈ 0.8 s/dòng, mỗi lần 0.2 s `back.out`).
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** A 1:44–1:50, D 01:08–01:12, A 4:22–4:28 (✓/✗), A 5:34–5:40 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** SVG dấu tick `stroke-dashoffset`.
- **Biến thể:** —

### IG-10 · Sơ đồ cây (thư mục/phân cấp)
- **Trông thế nào:** cây file bên trái, nội dung file chọn bên phải; hoặc cây ngang gốc→nhánh.
- **Chuyển động:** gốc → nhánh cấp 1 (lần lượt) → nhánh cấp 2 của nhánh được nói → mở file chọn; indent `x` 16 px/cấp, mỗi dòng `opacity`, nhánh = MO-01.
- **Giữ:** mỗi nhánh ≈ 0.8–1 s khi lời nhắc; con trỏ chọn (MO-09).
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** A 2:36–2:44 (cây thư mục tài liệu), B 960–976 (trình quản lý tệp), E 3:10–3:48 (nhánh pill sau bóng đèn tại tâm, 5:08–5:16) (nhật ký).
- **Độ tin:** ước · 3 nguồn
- **Gợi ý dựng:** indent `x` 16 px/cấp, mỗi dòng `opacity`, nhánh = MO-01.
- **Biến thể:** cây ngang dạng tổ chức chưa thấy: «≈ suy ra».

### IG-11 · Đồng hồ đo / slider / ngưỡng
- **Trông thế nào:** thanh gradient xanh→đỏ (độ khó), vòng điểm (44→92), slider ngưỡng, thanh pass-mark (3 vòng).
- **Chuyển động:** thang → kim/marker chạy tới giá trị → nhãn kết quả; 1–1.5 s `power2.out`.
- **Giữ:** đúng khi lời đưa con số; 1–1.5 s.
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** B 92–104, B 182–190, B 214–224, A 6:48–6:56 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### IG-12 · Cân đánh đổi / vòng lặp
- **Trông thế nào:** cân (VO-09) hoặc vòng người quay quanh nút (vòng phản hồi của người, E).
- **Chuyển động:** hai vế đặt lên → cân nghiêng → thăng bằng; vòng: nút trung tâm → vòng quay → nhãn người dùng hiện ở điểm kết.
- **Giữ:** nghiêng khớp «lớn dần đến khi…»; 1–1.5 s.
- **Khi dùng:** chưa có
- **Tránh:** chưa có
- **Bằng chứng:** C 3:48, E 9:08–9:14 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

---

## 4. Nhịp khớp lời: quy tắc chung

1. **Một ý nói = một phần hiện.** Phần đó vào trước từ khoá 0–0.3 s; nếu mất hơn 0.5 s thì rút ngắn hiệu ứng, không kéo lời.
2. **Hiện từ trái → phải hoặc trên → dưới** theo chiều đọc; không đảo trong cùng một cảnh.
3. **Đã nói thì giảm 60%, đang nói 100%, chưa nói 35% hoặc ẩn** (E, A).
4. **Nhịp nghỉ:** sau một khối ≥ 4 phần tử, giữ 1.5–2 s tĩnh để người xem đọc.
5. **Thoát trước khi đổi cảnh** 0.3–0.4 s (blur + mờ), không cắt khi chữ còn ở 100%.
6. **Số liệu luôn kèm đơn vị và ghi nguồn môi trường** khi là số đo (B 136–146 ghi «không phải số đo»).
7. **Chuyển động dùng một easing họ:** vào `power2.out`/`power3.out`, ra `power2.in`, nhấn `back.out(1.4)`.
