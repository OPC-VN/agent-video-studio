# Thư viện chuyển cảnh TR và bản đồ chuyển chế độ

Kết luận: video có người thật dùng **một ngữ pháp chuyển cảnh liên tục** (người co/giãn qua squircle, blur làm keo, 0.6–0.9 s mỗi lần) thay vì cắt cứng; video không người (A, B, C) lại cắt cứng là chính và chỉ dùng chuyển có cơ chế khi đổi ý lớn.

Khuôn mẫu, độ tin, mã video và chế độ: xem `library-contract.md`; danh sách mã: `pattern-index.md`.

## Contents
1. Nguồn số liệu và độ tin cậy
2. TR-01 … TR-14
3. Bản đồ chuyển chế độ (ma trận 6×6)
4. Biên đạo từng bước các đường chuyển chính
5. Nhịp: đổi chế độ, độ dài cảnh, luật
6. Khung người duy nhất xuyên suốt
7. Chỗ chưa chắc

## 1. Nguồn số liệu và độ tin cậy

- **Đáng tin nhất**: ghi chép soi 10 khung/giây ở E (10 mốc) và D (7 mốc), 10 khung/giây ở A (5 mốc), 5 khung/giây ở C (2 mốc): 24 dòng ghi chép trên 45 lưới đã cắt; 8 lưới của B chưa có ghi chép. Thời lượng ở các mốc này là đo (độ chính xác ≈0.1–0.2 s).
- **Kém tin hơn**: nhật ký cảnh theo bước 2 s (đặc biệt D, E nói «cắt cứng»). Khi nhật ký bảo «cắt cứng» mà ghi chép 10 khung/giây cho thấy blur/co, **theo ghi chép 10 khung/giây**. B không có ghi chép riêng: cơ chế B lấy từ nhật ký cảnh (ước).
- Viết tắt thời gian: «tr 38.6» = mốc 38.6 s trong ghi chép chuyển cảnh.

## 2. Các mẫu TR

Mỗi mẫu theo 9 trường của `library-contract.md`; thời lượng của chính chuyển cảnh ghi ở trường **Giữ**, easing ghi ở **Chuyển động**.

### TR-01 · Cắt cứng
- **Trông thế nào:** không có khung chuyển; khung N hình cũ, khung N+1 hình mới. Chủ đạo ở A (≈90%), B, C. Ở D chiếm đa số chuyển giữa các cảnh cùng chế độ; ngoại lệ có chủ đích P → PS (D tr 40.8).
- **Chuyển động:** HyperFrames clip kế tiếp bắt đầu đúng khung N+1, không tween; thường kèm âm bước/whoosh ≤ 0.2 s nếu muốn nhịp.
- **Giữ:** 0 s.
- **Khi dùng:** giữa hai cảnh cùng chế độ và cùng bố cục (A→A, S→S, PS→PS khác cảnh màn hình); khi muốn «nhịp cắt theo lời».
- **Tránh:** cắt cứng **mặt người** khi người sắp đổi kích cỡ/chế độ (xem luật 5.3).
- **Bằng chứng:** A (≈90%, không mốc); B 232–256 s (cắt sang full-bleed S); D tr 40.8 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** clip kế tiếp bắt đầu đúng khung N+1, không tween.
- **Biến thể:** —

### TR-02 · Blur-through (mờ chéo qua blur)
- **Trông thế nào:** cảnh cũ `blur 0→≈20px` + opacity giảm, cảnh mới nằm dưới `blur ≈20px → 0` + opacity tăng, chồng nhau (cross-dissolve qua blur). Thứ vào luôn blur→nét + 0→1; thứ ra nét→blur + 1→0.
- **Chuyển động:** vào `power2.out`, ra `power2.in`. Ví dụ E tr 501.4 toàn khung blur 0.1 s rồi nét dần 0.4 s; D tr 94.8 danh sách mờ + blur 0.4 s trong khi app hiện dưới.
- **Giữ:** 0.1–0.4 s.
- **Khi dùng:** đổi nội dung cùng khung (PA → PS, slide → màn hình, nội dung → trống). Là «keo» chung cho mọi chuyển chế độ.
- **Tránh:** blur > 0.5 s (E giữ tổng ≈0.8 s); blur nhiều lớp chồng làm mờ chữ trong khi vẫn cần đọc.
- **Bằng chứng:** E tr 38.6, tr 115.4 (blur + mờ 0.4 s), tr 501.4; D tr 94.8, tr 596.8 (icon blur→nét); A tr 536 (blur-cut) (tr: soi dày).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** `filter: blur(20px)→0, opacity 0→1, 0.4 s power2.out`; phần tử ra `blur(0)→blur(20px), opacity 1→0, 0.3 s power2.in`.
- **Biến thể:** D tr 94.8 (cross-dissolve qua blur) và E tr 501.4 (toàn khung blur 0.1 s) là hai cách khác nhau; giữ cả hai (xem mục 7).

### TR-03 · Co người thành PIP
- **Trông thế nào:** khung người (toàn khung hoặc squircle lớn) co + bo góc dần (mép cong thành squircle hoặc tròn) và trượt về góc dưới.
- **Chuyển động:** `power3.inOut`. E tr 38.6: blur+bo góc 0.1 s → co và trượt xuống góc trái dưới 0.2 s → squircle ≈14% rộng, mờ tan dần 0.3 s. D tr 6.8: viền cong thành tròn và trượt về góc dưới-trái 0.4 s → PIP tròn ≈12% chiều cao. Một phần tử người (FLIP), đồng thời `filter:blur(8px)→0`.
- **Giữ:** 0.3–0.6 s.
- **Khi dùng:** từ P/PA (người lớn) sang PS/PA nội dung (người nhỏ).
- **Tránh:** cắt rồi dựng lại khung nhỏ (đứt mạch người); đổi hình thể người (tròn ↔ squircle) trong cùng video.
- **Bằng chứng:** E tr 38.6, tr 581.4 (squircle co tiếp nhỏ hơn); D tr 6.8, tr 94.8 (thẻ người co và hạ xuống góc dưới-phải) (tr: soi dày).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** một phần tử người, `gsap.to(person,{width:'14%',left:'2.5%',bottom:'4%',borderRadius:'28px',duration:.4,ease:'power3.inOut'})` (FLIP); đồng thời `filter:blur(8px)→0`.
- **Biến thể:** —

### TR-04 · Trả người về toàn khung
- **Trông thế nào:** từ cảnh có PIP/khung nhỏ sang người toàn khung (đo): **cắt cứng**; một biến thể có **chớp sáng/mờ trắng 0.1 s** ngay trước cắt. Không thấy mốc nào giãn PIP lên toàn khung.
- **Chuyển động:** chuyển động dồn vào lớp chữ vào sau cắt (tên/tiêu đề blur→nét, hạt tụ chữ sau 0.6 s). Biến thể chớp: lớp trắng `opacity 0→0.8→0` trong 0.1 s chồng lên điểm cắt.
- **Giữ:** 0 s (cắt) hoặc 0.1 s (chớp sáng).
- **Khi dùng:** kết đoạn demo, mở mục mới, kết/CTA. Bất đối xứng có chủ đích: rời toàn khung thì co (TR-03), quay về thì cắt.
- **Tránh:** tween giãn PIP chậm lên toàn khung (không có trong mẫu, dễ trông như lỗi zoom).
- **Bằng chứng:** E tr 120.8 (cắt), E tr 362.8 (chớp sáng 0.1 s + cắt), D tr 30.8 (cắt rồi tên blur→nét) (tr: soi dày).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** clip người bắt đầu đúng khung sau; biến thể chớp: lớp trắng `opacity 0→0.8→0` trong 0.1 s chồng lên điểm cắt.
- **Biến thể:** `TR-04a` chớp sáng 0.1 s trước cắt (E tr 362.8).

### TR-05 · Container transform (phần tử phóng thành cảnh)
- **Trông thế nào:** chọn một thẻ trong lưới: thẻ khác tối dần 0.3 s; thẻ được chọn giãn từ chính vị trí của nó ra lấp cửa sổ/khung; tiêu đề đổi; phần tử khung xương mọc ra trước (thanh timeline, panel), nội dung điền sau, mỗi lớp 0.2–0.3 s so le.
- **Chuyển động:** thẻ giãn 0.6 s `power3.inOut`; tổng ≈0.9 s.
- **Giữ:** ≈0.9 s tổng.
- **Khi dùng:** từ «danh sách mục» vào «chi tiết mục» (A→AS/S); thẻ tính năng → wireframe → ảnh màn hình (E 1:20–1:28).
- **Tránh:** thẻ giãn lệch tâm làm mất mạch; chọn thẻ nhưng không dim thẻ khác.
- **Bằng chứng:** A tr 79; E 1:20–1:28 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** FLIP: lấy `getBoundingClientRect` của thẻ, `gsap.fromTo(win,{...rectThẻ},{x:0,y:0,width:'100%',height:'100%',duration:.6,ease:'power3.inOut'})`; thẻ khác `opacity:.25`.
- **Biến thể:** —

### TR-06 · Push-in / zoom vào vùng
- **Trông thế nào:** phóng ≈140% (cảnh minh hoạ) hoặc ≈250% (zoom vào dòng lệnh/ô UI) quanh điểm cần nhìn, có thể kèm cắt khung và vật mới trượt vào.
- **Chuyển động:** `power2.inOut`. C tr 548–553: push-in ≈140% + một tờ báo cáo trượt vào cạnh quả cầu AI; phụ đề đổi câu cùng lúc. E tr 581.4: màn hình phóng ≈250% vào dòng lệnh từ dưới mờ lên, 0.3 s.
- **Giữ:** ≈0.3–0.6 s.
- **Khi dùng:** nhấn vật then chốt, đọc dòng lệnh nhỏ, vào cửa sổ/ô sáng.
- **Tránh:** zoom > ≈250% (chữ vỡ nếu nguồn 720p); zoom quanh tâm khi vùng cần xem lệch.
- **Bằng chứng:** C tr 548–553, 01:00 (push-in vào cửa sổ); E tr 581.4, 1:32, 4:56; B 240–246 s, 300–318 s (ước); D 01:48–02:00, 07:30–07:36 (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 4 nguồn
- **Gợi ý dựng:** `gsap.to(stage,{scale:1.4,transformOrigin:'62% 48%',duration:.5,ease:'power2.inOut'})`.
- **Biến thể:** —

### TR-07 · Mờ về nền
- **Trông thế nào:** nội dung mờ về nền trơn (đen hoặc kem) rồi cảnh mới mờ lên từ nền; có thể kèm phóng nhẹ.
- **Chuyển động:** `sine.inOut`. A tr 420: mờ về đen 0.3 s → cửa sổ mới mờ lên giữa khung kèm phóng nhẹ → dải phim trượt lên từ đáy. D: fade-to-beige (10:14, 12:20) làm sạch nền trước chương mới. B cuối: fade to white vào end card.
- **Giữ:** 0.3–0.4 s mỗi nửa.
- **Khi dùng:** đổi chương, kết đoạn, trước thẻ chương, đổi nền tối ↔ kem.
- **Tránh:** dùng cho mọi cảnh (mệt); mờ về đen khi nền cả video kem (đổi nền gây chói).
- **Bằng chứng:** A tr 420; D 10:14, 12:20; C tr 63–68 (câu hỏi + cảnh mờ 0.4 s); B 1024–1032 s (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 4 nguồn
- **Gợi ý dựng:** `gsap.to(scene,{opacity:0,duration:.3})` rồi `from(next,{opacity:0,scale:.96,duration:.4})`.
- **Biến thể:** —

### TR-08 · Pan/dolly trong thế giới minh hoạ
- **Trông thế nào:** camera ảo dịch ngang (pan) hoặc lùi/tiến (dolly) trên cảnh nhiều lớp; lớp xa trôi chậm hơn lớp gần (parallax); đôi khi lịch lật đổi thời gian.
- **Chuyển động:** `sine.inOut`, chuyển động liên tục. C: pan ngang phố 01:08–01:12; dolly-out từ tủ lạnh ra văn phòng 09:13–09:20. D 12:06–12:14: pan trên canvas thiết kế.
- **Giữ:** ≈2–4 s.
- **Khi dùng:** kể chuyện dài, đổi bối cảnh trong cùng thế giới; không đổi chế độ.
- **Tránh:** pan khi phụ đề đang đọc dở (cho phụ đề đổi ở mốc đổi khung).
- **Bằng chứng:** C 01:08–01:12, 09:13–09:20, 12:34 (kính lúp); D 12:06–12:14 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** 3–4 lớp, `gsap.to('.l1',{x:-400})`, `.l2` −200, `.l3` −80, cùng `duration:3, ease:'sine.inOut'`.
- **Biến thể:** —

### TR-09 · Panel trượt vào/ra
- **Trông thế nào:** panel tính năng trượt từ mép phải vào, kèm blur→nét; viền cam nháy quanh panel mới; chat bên trái dim; thoát: thu lại.
- **Chuyển động:** `power2.out`. Viền cam 0.5 s rồi tắt (E tr 87.4).
- **Giữ:** 0.4–0.5 s.
- **Khi dùng:** đổi trạng thái trong cùng màn hình (PS → PS), không đổi chế độ.
- **Tránh:** panel rộng > 45%; trượt cùng lúc 2 panel.
- **Bằng chứng:** E 0:12, 1:28–1:34, tr 87.4; D 00:44 (khung đỏ chat → artifact); B (card slide-in, giữ nguyên rồi biến mất bằng cắt; không mốc) (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** `gsap.from(panel,{x:'100%',filter:'blur(8px)',duration:.4,ease:'power2.out'})`.
- **Biến thể:** —

### TR-10 · Stinger / wipe thương hiệu
- **Trông thế nào:** hai dải ruy băng vàng cong quét chéo qua người trong 0.2 s rồi lộ người toàn khung; hoặc logo giữ ≈1.2 s rồi blur-cut sang nền trống.
- **Chuyển động:** 2 `div` `clip-path`/SVG `path` quét chéo `x:-120%→120%, 0.2 s power3.inOut`, nền trong suốt dưới; hoặc logo ≈1.2 s + blur-cut. Dùng 1 lần/video ở mở, tối đa 1 lần nữa ở kết.
- **Giữ:** 0.2–0.3 s quét; hoặc logo ≈1.2 s + blur-cut.
- **Khi dùng:** ngay sau logo mở, lúc vào hook từ tên video.
- **Tránh:** stinger giữa video (cản nhịp, trùng mục đích thẻ chương). Dấu ấn của mẫu: chỉ lấy nguyên lý, bắt buộc đổi hình thức (ruy băng là dấu ấn của mẫu): dùng hình nhận diện của kênh, ví dụ dải hai màu thương hiệu quét ngang, logo vẽ nét tự hiện, chữ cái đầu của kênh làm mặt nạ lộ người.
- **Bằng chứng:** E tr 38.6 (ruy băng); A tr 536 (logo → blur-cut) (tr: soi dày).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** 2 `div` `clip-path`/SVG `path` quét chéo `x:-120%→120%, 0.2 s power3.inOut`, nền trong suốt dưới.
- **Biến thể:** `TR-10a` logo giữ ≈1.2 s rồi blur-cut sang nền trống (A tr 536).

### TR-11 · Thẻ chương xen
- **Trông thế nào:** câu hỏi/mục cũ mờ 0.4 s → thẻ chương (số + tiêu đề) vào: LED số 0.6 s, chữ trượt lên theo dòng, gạch chân mọc; thoát: chữ trượt ra, số tắt → mờ sang cảnh mới. Ở E: thẻ là hạt chấm → chữ pixel → chữ serif trên người toàn khung (0.6 + 0.4 + 0.3 s), không cần cảnh riêng.
- **Chuyển động:** xem LY-11 trong `layout-library.md`; hạt chấm bằng canvas hoặc ≈40 `span` `y:-60→0, stagger .01`.
- **Giữ:** ≈2.5 s.
- **Khi dùng:** đổi mục lớn (nhịp 30–106 s/mục ở E; 10 chương/≈18 phút ở C).
- **Tránh:** thẻ chương cho mục < 30 s; thẻ > 6 s. Tòa nhà LED số chương và hạt → chữ pixel là dấu ấn riêng của video mẫu. Dấu ấn của mẫu: chỉ lấy nguyên lý, bắt buộc đổi hình thức.
- **Bằng chứng:** C tr 63–68; E tr 237.4; D tr 596.8 («N /5») (tr: soi dày).
- **Độ tin:** đo · 3 nguồn
- **Gợi ý dựng:** xem LY-11 trong `layout-library.md`; hạt chấm bằng canvas hoặc ≈40 `span` `y:-60→0, stagger .01`.
- **Biến thể:** —

### TR-12 · Giữ vật thể làm mạch (match/morph)
- **Trông thế nào:** một vật ở cảnh cũ biến thành vật ở cảnh mới tại cùng vị trí và kích cỡ (ô sáng → chip; quả cầu → quầy; thẻ tính năng → wireframe → ảnh màn hình). Giữ **một** thuộc tính xuyên suốt (vị trí hoặc hình).
- **Chuyển động:** `power2.inOut`; cùng `div` đổi `src/background` ở giữa tween, hoặc cross-fade hai lớp chồng đúng vị trí.
- **Giữ:** 0.4–0.8 s.
- **Khi dùng:** đổi ý nhưng giữ khái niệm; mượt hơn cắt mà ít tốn hơn pan.
- **Tránh:** morph hai vật khác nghĩa chỉ vì giống hình.
- **Bằng chứng:** C (match-cut ô sáng → chip, quả cầu → quầy; không mốc); E 1:20–1:28 (nhật ký).
- **Độ tin:** ước · 2 nguồn
- **Gợi ý dựng:** cùng `div` đổi `src/background` ở giữa tween, hoặc cross-fade hai lớp chồng đúng vị trí.
- **Biến thể:** —

### TR-13 · Lùi máy lộ bối cảnh
- **Trông thế nào:** zoom-out/dolly-out từ chi tiết ra toàn cảnh (tủ lạnh → văn phòng; cửa sổ → phố); phần tử mới lộ ra theo thứ tự xa dần.
- **Chuyển động:** `power2.out`. Dùng khi chuyển từ ví dụ nhỏ sang bức tranh lớn.
- **Giữ:** ≈1–2 s.
- **Khi dùng:** «đó chỉ là một trường hợp, còn toàn bộ là…».
- **Tránh:** lùi rồi lại tiến ngay (lắc).
- **Bằng chứng:** C 09:13–09:20 (zoom-out khỏi tủ lạnh sang văn phòng) (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** `gsap.fromTo(stage,{scale:2.2,transformOrigin:'30% 55%'},{scale:1,duration:1.4,ease:'power2.out'})`.
- **Biến thể:** —

### TR-14 · Tách đôi so sánh
- **Trông thế nào:** khung đơn chia thành hai panel đối xứng: bên cũ giữ, bên mới trượt vào; «vs» hiện cuối. Ở A là bố cục dựng sẵn, không phải push.
- **Chuyển động:** `power3.out`; `grid 1fr 1fr`, panel phải `x:'50%'→0, opacity 0→1`.
- **Giữ:** 0.4–0.5 s.
- **Khi dùng:** so sánh sáng/tối, gốc/bản sao, miễn phí/trả phí, năm cũ/nay.
- **Tránh:** đổi vai trái/phải giữa các cảnh.
- **Bằng chứng:** A 0:48–0:54, 7:12–7:27, tr 420; B 46–50 s, 224–232 s (tr: soi dày; còn lại: nhật ký).
- **Độ tin:** đo · 2 nguồn
- **Gợi ý dựng:** `grid 1fr 1fr`, panel phải `x:'50%'→0, opacity 0→1`.
- **Biến thể:** —

## 3. Bản đồ chuyển chế độ (ma trận)

Đọc: **hàng = từ**, **cột = tới**. «TR-02+03» nghĩa là dùng cả hai theo thứ tự trong ô. «TR-xx*» = suy diễn, chưa có mốc đo trực tiếp (đã ghi ở mục 7). Ô chéo = đổi cảnh trong cùng chế độ.

| từ \ tới | P | PA | A | S | PS | AS |
|---|---|---|---|---|---|---|
| **P** | TR-01 (cảnh P khác) | TR-02+03 (tr 38.6; D 6.8) | TR-07 hoặc TR-10 | TR-03 → TR-07* | TR-02+03+06 (tr 581.4); D 40.8 cắt cứng ngoại lệ | TR-02* |
| **PA** | TR-04 hoặc TR-07 | TR-09 / TR-02 (đổi nội dung trong khung) | TR-03 rồi TR-07 | TR-03 rồi TR-02* | TR-02 (+TR-03 chạy cùng; E tr 501.4, D tr 94.8) | TR-02* |
| **A** | TR-10 hoặc TR-07 | TR-02 → TR-04* | TR-01 / TR-07 / TR-08 / TR-12 | TR-05 hoặc TR-01 (A, B) | TR-05* | TR-05 hoặc TR-02 (A tr 79, 420) |
| **S** | TR-04* (từ không người, người vào) | TR-04* + TR-02 | TR-07 | TR-01 / TR-06 | TR-04* (người vào PIP) | TR-02* |
| **PS** | TR-04 | TR-02 (người giãn lên, màn hình mờ) | TR-03 + TR-07* | TR-03 (PIP tan 0.3 s) hoặc TR-01 | TR-09 / TR-06 (E tr 87.4, 581.4) | TR-02* |
| **AS** | TR-07 | TR-02* | TR-02 hoặc TR-07 | TR-01 | TR-02* | TR-05 / TR-09 |

Luật đọc ma trận:
- Rời toàn khung (P → PA/PS): TR-02 (blur) + TR-03 (co người); về toàn khung (→ P): TR-04 (cắt cứng, có thể chớp sáng 0.1 s). Cắt cứng P → PS chỉ thấy ở D 40.8.
- Từ A/AS ↔ S: ưu tiên TR-01 vì cả A, B đều dùng (≈90% A); chỉ dùng TR-05 khi ý «chọn rồi vào chi tiết».
- Cùng chế độ khác cảnh: TR-01, trừ cảnh chương (TR-11).

## 4. Biên đạo từng bước các đường chuyển chính

Mốc giây tương đối so với điểm bắt đầu chuyển (t = 0). Giá trị đo ghi rõ; chỗ ước ghi «≈».

### 4.1 P → PA (người toàn khung → người squircle nhỏ + thẻ nội dung phải)
Nguồn: E tr 38.6, D tr 6.8.
- 0.0–0.1: cả khung người blur ≈20px + bo góc (độ cong tăng nhanh).
- 0.1–0.3: khung co về thẻ bo góc, trượt xuống góc dưới trái (đường chéo, `power3.inOut`).
- 0.3–0.6: thành squircle ≈14% rộng (D: tròn ≈12% cao); phần mờ tan; nền tối có lưới chấm + đường sóng mảnh hiện ra.
- 0.4–0.7 (E): thẻ nội dung phải **blur→nét + opacity 0→1 ≈0.3 s**.
- Tổng ≈0.8 s (E). Nếu có lớp nổi (D 6.8): lớp nổi mờ 0.3 s **trước** t = 0.

### 4.2 P → PS (người → squircle góc + màn hình)
Nguồn: E tr 581.4.
- −0.3–0.0: tiêu đề chương trên người mờ dần 0.3 s.
- 0.0–0.3: người blur + bo góc → co thành squircle trên nền tối.
- 0.3–0.6: màn hình phóng ≈250% vào dòng lệnh, từ dưới mờ lên; squircle co tiếp nhỏ hơn (≈14%) về góc dưới trái.
- Ngoại lệ có chủ đích: D 40.8 cắt cứng sang giao diện app toàn khung, người thành thẻ dọc bo góc dưới-phải ≈18% rộng — chỉ dùng khi người đã ở chế độ nổi (PA, thẻ slide).

### 4.3 PA (squircle lớn) → PS
Nguồn: E tr 501.4, D tr 94.8.
- 0.0–0.1: toàn khung blur (E); hoặc (D) danh sách mờ + blur 0.4 s, đồng thời app hiện dần bên dưới.
- 0.1–0.4: squircle lớn ≈40% rộng co về góc dưới trái nhỏ (≈14%); (D) thẻ người co nhỏ và hạ xuống góc dưới-phải.
- 0.1–0.5: màn hình **nét dần** dưới lớp mờ (blur-through) ≈0.4 s.
- 0.5–1.0 (D): thanh bên trái của app **trượt ra** khỏi khung, vùng làm việc phóng nhẹ vào ô nhập; lệnh gõ từng ký tự.

### 4.3b PS → PA / thoát nội dung
Nguồn: E tr 115.4.
- 0.0–0.4: nội dung (tiêu đề + tài liệu + mũi tên cam) **blur + mờ dần 0.4 s**; squircle đứng yên.
- 0.4–: nền trống chờ cảnh sau; nếu cần giãn người về toàn khung (PS → P) dùng TR-04 sau đó (≈0.4–0.6 s, ước).

### 4.4 A → AS / chọn thẻ → vào chi tiết
Nguồn: A tr 79.
- 0.0–0.3: các thẻ khác tối dần; con trỏ trỏ vào thẻ được chọn.
- 0.3–0.9: thẻ được chọn giãn từ vị trí của nó ra lấp cửa sổ (container transform); tiêu đề đổi; thanh timeline mọc ở đáy.
- 0.9–1.6: khung xương trống mờ lên → panel phải trượt vào → URL gõ từng ký tự → các lớp nội dung hiện theo (0.2–0.3 s/lớp, so le).

### 4.5 A → A đổi cảnh lớn
Nguồn: A tr 420, 536.
- Kiểu 1: 0.0–0.3 mờ về đen; 0.3–0.7 cửa sổ mới mờ lên kèm phóng nhẹ; 0.7–1.2 dải phim trượt lên từ đáy; node mờ lên bên trái, đường nối cong tự vẽ.
- Kiểu 2: logo giữ ≈1.2 s trên nền trắng → blur-cut sang nền đen trống → phần tử mờ lên so le → icon bật.

### 4.6 Mở đầu có stinger: stinger → P → PA
Nguồn: E tr 38.6.
- 0.0–0.2: hai dải ruy băng vàng cong quét chéo qua người.
- 0.2–: lộ người toàn khung (giữ ≈2–4 s hoặc theo lời).
- Sau đó: chạy 4.1.

### 4.7 Thẻ chương trên người toàn khung (P + chữ)
Nguồn: E tr 237.4.
- 0.0–0.6: hạt chấm bay vào từ trên; 0.6–1.0: tụ thành chữ pixel; 1.0–1.3: chữ pixel hoà tan sang chữ có chân; số chương cam nhỏ ở trên, phụ đề nhỏ dưới.
- Giữ ≈4–6 s; thoát: chữ mờ 0.3 s rồi chạy 4.2 nếu vào demo.

### 4.8 Chương kể chuyện: câu hỏi → thẻ chương → thế giới
Nguồn: C tr 63–68.
- 0.0–0.4: câu hỏi + cảnh mờ; nền đô thị đêm hiện.
- 0.4–1.0: tòa bật đèn từng ô tạo số (LED, 0.6 s); chữ «CHƯƠNG» + tiêu đề trượt lên từng dòng; gạch chân vàng mọc; giữ ≈2.5 s.
- Thoát: chữ trượt ra theo dòng, số tắt từng ô → mờ sang cảnh mới (blur → nét, phóng nhẹ).

### 4.9 PS → PS trong cùng màn hình
Nguồn: E tr 87.4.
- Squircle đứng yên; 0.0–0.5 viền cam bao nhóm nút rồi tắt; panel trượt từ phải + blur→nét 0.4 s, viền cam nháy; widget mờ → hiện.

### 4.10 Ngược: PS → P / S → PS (người xuất hiện lại)
Đo được (E tr 120.8, 362.8; D tr 30.8): **cắt cứng** sang người toàn khung, có thể chớp trắng 0.1 s trước cắt; 0.5–0.6 s sau cắt chữ mới vào (tên blur→nét, hoặc hạt tụ thành tiêu đề chương). S → PS (người xuất hiện ở PIP) chưa có mốc đo.

## 5. Nhịp

### 5.1 Số liệu quan sát

| Video | Đổi chế độ | Độ dài cảnh trung bình | Ghi chú |
|---|---|---|---|
| A | ≈45–60 lần / 14:56 (≈3–4 lần/phút; 1 lần/15–20 s) | ≈5–6 s (≈12 s nếu gộp theo demo) | Cắt ≈90%; chuyển cơ chế chỉ ở mốc đổi ý lớn |
| B | ≈14 lần (hầu hết trong 234 s đầu; ≈0.8 lần/phút cả video) | ≈9 s (A đầu 3–6 s; S sau 12–20 s) | Cắt chủ đạo; crossfade chỉ ở mở đầu 2 s |
| C | gần 0 (A ≈97%) | ≈9.5 s / 116 cảnh | 10 thẻ chương; chương 01 không thẻ |
| D | 29 lần / 894 s (≈1.9 lần/phút; 1 lần/31 s) | 8.0 s / 112 cảnh; dài nhất 16 s | Vùng dày: 00:42–01:36 |
| E | 69 lần / 767 s (≈5.4 lần/phút; 1 lần/11 s) | 6.2 s (2–24 s); 124 dòng | Chuyển 0.6–0.9 s; giữ cảnh 2–8 s |

### 5.2 Quy tắc nhịp (khuyến nghị tổng hợp)
1. **Giữ cảnh 2–8 s**; PS demo dài tới ≈12–24 s nếu màn hình tự biến động (gõ, panel); tiêu đề chương 4–6 s; thẻ card 8–12 s.
2. **Chuyển 0.6–0.9 s** cho chuyển chế độ có người (E); ≤ 0.4 s cho đổi nội dung trong khung.
3. Quan sát: đổi chế độ mỗi ≈11 s (E, nhanh) đến ≈31 s (D, dịu). Ngưỡng dùng để kiểm nằm ở một chỗ duy nhất: `workflow.md` bước 3.
4. **Cấu trúc lặp mục** (E, ≈40–60 s): P + tiêu đề → PA (cơ chế) → PS (demo) → PA (chi phí/tóm tắt) → mục kế.
5. Chuỗi chuyển **liền** ≤ 2 lần chuyển có cơ chế trong 10 s; nếu thêm thì cắt cứng giữa hai cảnh cùng chế độ.
6. Hạt/particle chỉ ở **đầu mục** (E 2:02, 9:04), không ở giữa mục.
7. Chỉ có **một** stinger thương hiệu (mở) và tối đa một thẻ chương cho mỗi mục.

### 5.3 Luật «không cắt cứng người»
- **Rời toàn khung** (người nhỏ lại): luôn co liên tục (TR-03) kèm blur ngắn; không cắt (ngoại lệ đã thấy: D 40.8).
- **Về toàn khung**: cắt cứng hoặc chớp sáng 0.1 s (TR-04, đo ở E tr 120.8, 362.8; D tr 30.8).
- Cắt giữa hai cảnh P cùng cỡ và nền (jump cut) được phép.
- Nhật ký bước 2 s (D, E) hay ghi «cắt cứng» vì không thấy khung giữa; ghi chép 10 khung/giây thắng.
- Blur không được > 0.4 s kể cả khi vào; khuôn mặt không được chìm hoàn toàn dưới lớp mờ (E giữ squircle thấy được).

## 6. Khung người duy nhất xuyên suốt

Nguyên tắc: **một phần tử người, một hình thể** (squircle bo góc, cạnh vuông vức ở D) đi qua mọi chế độ bằng đổi kích cỡ/vị trí/độ bo; không dựng hai khung người.

| Trạng thái | Kích cỡ | Vị trí | Bo góc | Dùng | Bằng chứng |
|---|---|---|---|---|---|
| Toàn khung | 100% rộng | phủ khung | 0 | P, mở/kết, chuyển mục | E 0:00, 0:38; D 0:00 |
| Squircle lớn | ≈40% rộng (E ghi ≈30–40%) | trái, giữa-cao | lớn (≈28px ở 1280 ước) | PA: tiêu đề + sơ đồ phải | E tr 501.4, 0:28, 3:26 |
| Cột dọc | ≈27% rộng × ≈92% cao | mép phải | vừa | PA có slide (D) | D tr 52.8, 596.8 |
| PIP nhỏ | ≈14% rộng (E) · ≈16% rộng × ≈50% cao, thẻ dọc (D tr 40.8) · tròn ≈12% cao (D 6.8) | góc dưới-trái (E) / dưới-phải (D) | lớn / tròn | PS, nội dung dày | E tr 38.6, 581.4; D tr 94.8 |
| Ẩn | 0 | — | — | hiếm; D ≈00:52 (guess) | D 00:52 |

Chuỗi trạng thái điển hình ở E: toàn khung → (TR-03, 0.8 s) squircle 14% → (TR-04) toàn khung/squircle lớn → (TR-03) squircle 14% … Quy tắc:
- Theo E: **một phía** PIP cho cả video (trái dưới). D là phản ví dụ: PIP tròn dưới trái ở mở đầu, thẻ dọc dưới phải khi xem màn hình; nếu trộn thì mỗi vai một hình thể cố định.
- Luôn đi qua **bậc trung gian** (squircle lớn 40% hoặc cột phải) khi đổi từ toàn khung sang PIP nhỏ nếu có ≥ 0.6 s; chuyển trực tiếp chỉ khi tổng ≤ 0.8 s (E tr 38.6 làm được).
- Khung người có glow nhẹ khi trên nền tối; trên nền kem thì đổ bóng.
- Thứ trong khung người không thay đổi (cùng một video người), chỉ đổi cách cắt (crop) nếu cần giữ mặt trong khung nhỏ.

## 7. Chỗ chưa chắc

- TR-04 đã đo sau review (3 mốc, đều cắt). S → PS (người xuất hiện ở PIP từ cảnh không người) chưa có mốc đo. Các ô ma trận có «*» đều là suy diễn.
- B không có ghi chép chuyển cảnh riêng; cơ chế B (cut, crossfade 2 s ở mở, zoom vào lệnh) lấy từ nhật ký bước 2 s, sai số ±4 s.
- D tr 94.8 và E tr 501.4 mô tả hai cách khác nhau (cross-dissolve qua blur và toàn khung blur 0.1 s); giữ cả hai như biến thể TR-02.
- Easing ghi trong file là gợi ý dựng (power2/power3/sine), **không** đo từ video (khung 10 khung/giây không đủ để suy easing).
- Số lần đổi chế độ của A là ước; D/E tính từ bảng cảnh.
