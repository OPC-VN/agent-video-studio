# Mẫu storyboard chung cho video giới thiệu dự án BĐS (nhiều tình huống, góc quay, chuyển động)

> Do Fable lập từ video mẫu «bds», bản quay thao tác Google Earth và các hiệu ứng đã có; **đã dùng làm gốc cho storyboard dự án thật** (sau đó được Opus duyệt cổng). Ví dụ trong file lấy từ dự án mẫu; thay địa điểm/số liệu bằng của dự án mình. Tham số Google Earth ghi «đề xuất» là giá trị khởi điểm: giá trị đã quay thử xem `earth-capture.md`.

# Mẫu storyboard chung — video giới thiệu dự án BĐS dọc 9:16

Trạng thái: **bản nháp (draft), chưa dựng thử, chờ người dùng duyệt** | Lập ngày 19/11/2026
Căn cứ: `reference-map.md` (mẫu «bds» 30,8 s, 9 beat) · `UAT-rea-video.md` · `storyboard-vincom-openfreemap.md` · `../ge-screen-rec/PLAYBOOK-google-earth.md` · skill `land-plot-map-video` (+ `references/effects-map.md`) · `video-remix-brief` · `video-routing/assets/storyboard.md`.
Tỷ lệ / fps: 9:16, 1080×1920, 30 fps | Thời lượng: 30 / 45 / 60 s theo tình huống.

**Cách đọc:** mục 2 là thư viện cảnh (chọn như chọn gạch), mục 3 là công thức ghép theo loại dự án, mục 4 là các quyết định cần người dùng chốt, mục 5 là quy trình 9 khâu có cổng duyệt.

**Ba điều nói thẳng trước:**
1. Mọi tham số Google Earth ghi «đề xuất» là **giá trị khởi điểm chưa quay thử**. Chỉ 4 bộ đã thấy chạy thật: toàn cảnh `3636843d,0t`; Phụng Công `10854d,35y,0h,45t`; Swan Lake `978.98d,0t`; và `900d,35y,40h,65t` (xem PLAYBOOK).
2. Chuyển động camera **liên tục** trên Google Earth chưa quay tự động được (screencast chưa kiểm). URL chỉ đặt được **tư thế đầu và cuối**; đoạn giữa hiện phải quay tay hoặc chụp từng khung (chưa kiểm).
3. Lớp phủ gắn toạ độ (ranh, đường khoảng cách, vòng bán kính) chỉ **chiếu chính xác** trên ảnh top-down MapLibre pitch 0. Trên shot Google Earth nghiêng, tỉ lệ không theo công thức → phải canh tay hoặc chỉ gắn khi camera đứng yên.

---

## 1. Phân tích video mẫu → công thức cảnh

| Beat mẫu | Giây (đo máy) | Việc làm cho người mua | Thủ pháp | Rút ra cho mẫu chung |
|---|---|---|---|---|
| B0 Mở | 0–0,6 | Giữ chân trong 1 giây đầu | zoom-blur lao xuống | Luôn mở bằng chuyển động mạnh, chưa cần chữ |
| B1 Hook + hứa | 0,6–5,6 | Biết ngay video nói về lô nào, được gì | đa giác lô phát sáng + chữ gõ, từ khoá đổi màu | Trong 5 s đầu: **thấy đối tượng** (ranh sáng) + **một lời hứa** |
| B2 Người dẫn | 5,6–7,2 | Biết ai nói, tạo tin cậy | cutout người chỉ tay | Tuỳ chọn; video dự án có thể thay bằng logo chủ đầu tư/đại lý |
| B3 Chuyển ý | 7,2–9,6 | Báo trước cấu trúc («đầu tiên…») | pan nhòe rồi nét | Một câu chuyển, đánh số bước, giúp người xem theo kịp |
| B4 Vị trí | 9,6–14,6 | Trả lời «ở đâu» theo tầng hành chính | zoom ra từng tầng, ranh xã (vàng) → ranh tỉnh (cyan) vẽ dần, ghim + vòng sóng | **Nhóm yêu cầu 1**: thiếu phần «chỉ số khu vực» → phải bổ sung |
| B5 Cận cảnh diện tích | 14,6–20,9 | Trả lời «rộng bao nhiêu, hình dáng ra sao» | zoom vào, khối xanh + nhãn A×B, camera xoay nhẹ | **Nhóm yêu cầu 2**: mẫu chỉ có 1 góc → cần thêm toàn cảnh, 3D, môi trường, đường |
| B6 Khoảng cách | 20,9–23,7 | Trả lời «cách trung tâm bao xa» | đường nét đứt vẽ dần + nhãn | **Nhóm yêu cầu 3**: mẫu chỉ 1 điểm → nâng lên 3–5 điểm |
| B7 Tiện ích 5 phút | 23,7–28,0 | Trả lời «quanh đây có gì» | vòng bán kính nở + 3 ghim rơi nảy | Giữ; nhãn phải nói đúng «bán kính X m», không gọi là «5 phút» nếu chưa có isochrone |
| B8 CTA | 28,0–30,8 | Bảo người xem làm gì tiếp | chữ lớn + người + nhãn kênh | Giữ; một hành động duy nhất |

**Công thức cảnh (áp cho mọi cảnh trong thư viện):**

> **1 câu hỏi của người mua → 1 mệnh đề lời → 1 chuyển động camera → 1 lớp đồ họa mới → 1 con số hoặc 1 cái tên.**

- Trật tự câu hỏi: **ở đâu → khu này có đáng mua không → dự án trông thế nào → quanh nó có gì → đi đâu mất bao xa → làm gì tiếp**.
- Nhịp mẫu: 9 beat / 30,8 s, khoảng 3 lần đổi cảnh mỗi 10 s; chuyển tầng bản đồ bằng nhòe 0,3–0,6 s rồi nét.
- Mẫu **không có**: chỉ số khu vực, toàn cảnh dự án, cảnh nhà 3D, bố cục dự án lân cận, nhiều điểm khoảng cách. Đây là phần mẫu chung này thêm vào.
- Chưa có số liệu giữ chân/chuyển đổi của mẫu; «vì sao hiệu quả» là giả thuyết.

---

## 2. Thư viện cảnh (26 cảnh, mã S-xx)

**Quy ước tham số**
- Google Earth web: `@lat,lng,<a>a,<d>d,<y>y,<h>h,<t>t,<r>r` — `d` khoảng cách camera (m), `h` hướng (độ), `t` nghiêng (0 = nhìn thẳng xuống), `y` góc nhìn (giữ 35), `r` xoay (giữ 0).
- `D1` = khoảng cách `d` mà **toàn bộ dự án vừa khung dọc**. Phải đo lại cho từng dự án ở khâu 5 (với khu Swan Lake, Earth tự chọn ≈ 979 m; dự án lớn như cả Ecopark sẽ lớn hơn nhiều). «x4→x1» trong tài liệu này = `4·D1 → 3·D1 → 2·D1 → D1` (**ASSUMPTION** về ý «zoom x4→x3→x2→x1» của người dùng; cần người dùng xác nhận).
- MapLibre: `Z` zoom 256 px, `P` pitch, `B` bearing; chụp bằng `geo-capture.html`.
- «Cách quay»: **URL** = đặt tư thế bằng URL; **UI** = thao tác tay trên giao diện; **ML** = MapLibre/OpenFreeMap/Esri.
- Thời lượng là gợi ý; mốc thật đặt theo cue giọng đọc.

### Nhóm 1 — Khu vực và chỉ số khu vực (yêu cầu 1)

| Mã | Mục đích với người mua | Dữ liệu cần | Góc + chuyển động camera | Motion | Lớp hiệu ứng | Giây | Cách quay | Rủi ro / ghi chú |
|---|---|---|---|---|---|---|---|---|
| **S-01 Lao xuống từ vũ trụ** | Giữ chân; định vị «ở Việt Nam, vùng nào» | toạ độ tâm dự án | Từ toàn cảnh `3636843d,0t` (đã thấy) lao tới tầng tỉnh, `t` 0 | zoom-in nhanh + zoom-blur | không chữ, hoặc 1 dòng tên dự án cuối cảnh | 0,6–1,5 | URL 2 tư thế + bay của Earth (UI) hoặc ML Z 7→12 | Earth nạp ảnh chậm khi lao nhanh → nhòe che; hộp «New from Google Earth» che màn hình |
| **S-02 Ranh tỉnh/thành** | «Thuộc tỉnh/thành nào» | ranh ADM4 (OpenFreeMap có), tên sau sắp xếp 2025 | Top-down, khung vừa cả tỉnh; `t` 0, `h` 0. Đề xuất `d` 150.000–300.000 (chưa thử) | zoom-out rồi dừng | ranh tỉnh cyan vẽ dần + tô nhạt; nhãn tên tỉnh; ghim dự án + vòng sóng | 2,5–3,5 | **ML** (chiếu chính xác) | Tô nền cần đa giác kín (tile chỉ có đường biên, chưa kiểm) → lùi về viền sáng |
| **S-03 Ranh quận/huyện, phường/xã** | «Thuộc phường/xã nào» | ranh cấp dưới (KML do người dùng cấp hoặc ADM6, chưa kiểm là cấp nào), tên đúng | Top-down → nghiêng nhẹ; mốc đã thấy: `10854d,45t` (Phụng Công) | zoom-in từ S-02, cuối cảnh nghiêng 0→45 | ranh vàng vẽ dần; nhãn tên nghiêng theo hình (pop) | 2,5–3 | ML cho ranh; Earth URL cho bản nghiêng không ranh | Tên đơn vị hành chính đã đổi năm 2025 → **người dùng xác nhận nhãn** |
| **S-04 Thẻ chỉ số khu vực** | «Khu này đông dân không, đang nóng không» | 2–3 chỉ số **có nguồn + ngày**: dân số/mật độ, khu công nghiệp/việc làm, hạ tầng đã khởi công | Giữ khung S-03, trôi chậm (`h` +5° trong cả cảnh) | drift chậm, nền tối 30 % | 2–3 thẻ số bật lần lượt (số đếm lên), dòng nguồn nhỏ dưới mỗi thẻ | 4–6 | nền: Earth URL nghiêng; thẻ: HyperFrames | **Hiệu ứng thẻ số chưa có trong template**; số không nguồn → bỏ thẻ, không bịa |
| **S-05 Ba điểm mạnh khi mua** | «Vì sao nên xem dự án này» | 3 luận điểm kiểm chứng được (vị trí, hạ tầng, tiện ích nội khu), không phải lời hứa giá | Top-down khu vực, mỗi luận điểm lia tới một vùng | 3 nhịp pan ngắn (whip nhẹ) | vùng sáng (đa giác tô) + nhãn 2–4 từ cho từng điểm mạnh | 4–6 | ML (vùng gắn toạ độ) | Dễ trượt thành quảng cáo lợi nhuận → xem mục 7 |

### Nhóm 2 — Vào dự án: toàn cảnh, môi trường, lân cận, 3D, đường (yêu cầu 2)

| Mã | Mục đích với người mua | Dữ liệu cần | Góc + chuyển động camera | Motion | Lớp hiệu ứng | Giây | Cách quay | Rủi ro / ghi chú |
|---|---|---|---|---|---|---|---|---|
| **S-06 Bậc thang zoom x4→x1** | Dẫn mắt từ khu vực vào đúng dự án, không lạc | toạ độ tâm, `D1` | Cùng `h`, `t` 45: `d` = 4·D1 → 3·D1 → 2·D1 → D1; mỗi bậc dừng 0,4–0,6 s | zoom bậc thang (punch-in), nhòe 0,2 s giữa bậc | nhãn «x4 · x3 · x2 · x1» nhỏ ở góc hoặc khung ngắm thu dần; ranh dự án sáng dần từ bậc x2 | 3–4 | **URL** 4 tư thế (cắt cứng + nhòe) — hợp nhất với khả năng hiện có | Nhãn x4… có thể thừa → tuỳ chọn; ranh trên shot nghiêng phải canh tay |
| **S-07 Toàn cảnh orbit** | «Dự án trông thế nào từ trên cao» | tâm dự án, hướng đẹp nhất (mặt nước/trục chính) | `d` ≈ D1…1,5·D1, `t` 60–65 (65 đã thử), `h` quét 60–90° | orbit chậm, tốc độ đều | tên dự án (chữ gõ) + ranh dự án sáng | 4–6 | UI kéo tay / chuỗi URL đổi `h` từng khung (chưa kiểm) | Orbit tay dễ giật; lưới 3D của Earth ở VN có nơi chưa có nhà 3D → kiểm trước |
| **S-08 Lia môi trường (sông, hồ, núi, khu dân cư)** | Điểm (a): «xung quanh là gì» | danh sách yếu tố tự nhiên + khu dân cư, toạ độ từng cái | `t` 55–65, `d` 2–3·D1; `h` cố định, tâm trượt ngang dọc theo sông/hồ | truck/pan ngang, hoặc «di chuyển qua lại» A→B→A | nhãn tên sông/hồ/núi bám vị trí; vùng nước/xanh tô sáng nhẹ | 4–5 | UI kéo tay; hoặc 2–3 URL + hoà trộn 0,25 s | Nhãn bám vị trí trên shot đang lia cần track → dễ nhất là **dừng 1 s rồi mới bật nhãn** |
| **S-09 Bố cục dự án lân cận** | Điểm (b): «cạnh dự án nào, phân khu nào» | ranh/tâm 2–4 dự án hoặc phân khu lân cận, tên đúng | Top-down hoặc `t` 30, `d` 3–4·D1 | zoom-out nhẹ rồi dừng | đa giác màu khác nhau cho từng dự án + nhãn; dự án chính sáng nhất | 3–5 | **ML** (ranh chính xác) | Gọi tên dự án của bên khác: chỉ nêu tên + vị trí, không so sánh hơn kém |
| **S-10 Nhà 3D kiểu Map** | Thấy rõ khối nhà, tầng cao, bố cục toà | — | Basemap **Map** + **3D buildings**; `d` 0,6–1·D1, `t` 60–65, `h` quét 30–45° | orbit chậm hoặc dolly-in | khối dự án tô màu nổi (khối xanh neon) + nhãn số toà/số tầng (nếu có nguồn) | 3–5 | **UI** (Basemap settings → Map → 3D buildings); hoặc **ML** `esri3d`/OpenFreeMap `fill-extrusion` pitch 50–55 (đã kiểm) | Bật Map/3D trên Earth **chưa tự động được**; chiều cao nhà OSM chỉ gần đúng |
| **S-11 Đường quanh dự án + lối vào** | Điểm (c): «vào bằng đường nào, đường rộng không» | tên + lộ giới các đường tiếp giáp (cần nguồn), vị trí cổng | Top-down `t` 0–20, `d` ≈ 1,5·D1; lia dọc trục chính | dolly dọc đường rồi dừng ở cổng | đường tô sáng vẽ dần theo chiều đi; nhãn tên đường; mũi tên lối vào | 3–5 | **ML** (tuyến = polyline gắn toạ độ) | Polyline đường lấy từ OSM (chưa có công cụ rút tuyến sẵn) hoặc vẽ tay trong KML |
| **S-12 Ranh dự án + diện tích** | «Rộng bao nhiêu» | KML ranh dự án, diện tích theo hồ sơ pháp lý | Top-down, `d` ≈ D1; cuối cảnh nghiêng nhẹ + xoay vài độ | zoom-in nhòe rồi xoay nhẹ | đa giác neon vẽ dần → khối xanh + nhãn A×B / diện tích | 4–6 | **ML** + template (`geo_cfg.py`) | Số tính từ toạ độ lệch số hồ sơ → **dừng, hỏi**; không dùng hull toà nhà làm ranh dự án thật |

### Nhóm 3 — Zoom ra, tag 3–5 điểm và khoảng cách (yêu cầu 3)

| Mã | Mục đích với người mua | Dữ liệu cần | Góc + chuyển động camera | Motion | Lớp hiệu ứng | Giây | Cách quay | Rủi ro / ghi chú |
|---|---|---|---|---|---|---|---|---|
| **S-13 Bản đồ 3–5 điểm quan trọng** | «Đi làm, đi học, đi viện mất bao xa» | 3–5 POI (tên, toạ độ, loại), khoảng cách từng điểm | Top-down, khung vừa dự án + mọi POI | zoom-out từ dự án rồi dừng hẳn | ghim rơi nảy lần lượt (lệch 0,3 s) → đường nét đứt vẽ dần từ dự án tới từng ghim → nhãn «tên · X km» | 5–8 | **ML** + template | Template hiện vẽ **1 đường** tới `trung-tam`; nhiều đường + nhãn km mỗi đường **phải mở rộng**. Khoảng cách là chim bay trừ khi có routing |
| **S-14 Vòng bán kính** | «Trong X km có gì» | bán kính (m), POI trong vòng | Giữ khung S-13 hoặc hẹp hơn | vòng nở từ tâm | 1–3 vòng đồng tâm (vd 1 · 3 · 5 km) + nhãn; POI trong vòng sáng lên | 3–4 | ML + template (1 vòng đã có) | Nhiều vòng: phải thêm; không ghi «5 phút» khi chưa có isochrone |
| **S-15 Bay dọc tuyến tới điểm chính** | Cảm nhận đường đi thật tới 1 điểm quan trọng nhất | tuyến đường (polyline), thời gian đi (cần nguồn) | `t` 55–65, `d` 1.500–3.000 (chưa thử), tâm chạy dọc tuyến, `h` theo hướng đi | fly-along (dolly dọc tuyến), tua nhanh | tuyến sáng chạy trước camera; đồng hồ km đếm lên; ghim đích | 4–6 | UI kéo tay hoặc chuỗi URL dọc tuyến (chưa kiểm) | Cảnh khó nhất; chỉ dùng cho bản 45–60 s; thời gian đi phải có nguồn + giờ đo |

### Nhóm 4 — Góc quay khác (yêu cầu 4; 11 đề xuất)

| Mã | Lý do dùng | Dữ liệu cần | Góc + chuyển động camera | Motion | Lớp hiệu ứng | Giây | Cách quay | Rủi ro / ghi chú |
|---|---|---|---|---|---|---|---|---|
| **S-16 Crane up reveal** | Mở bí mật: từ sát nóc nhà nâng lên lộ cả khu + mặt nước → cảm xúc «wow» | hướng có nền đẹp | `d` 0,3·D1 → 1,5·D1, `t` 75 → 55, `h` giữ | crane up + pull-back | tên dự án hiện khi lộ toàn cảnh | 3–4 | UI / 2 URL + bay của Earth | `t` > 65 chưa thử; sát đất lưới 3D lộ méo |
| **S-17 Dolly thấp dọc mặt nước/trục chính** | Cảm giác «đang đi trong dự án», hợp ven hồ, biển | trục nước/đại lộ | `t` 70–78, `d` 300–600, tâm chạy dọc trục | dolly-in thấp | chữ 1 dòng cảm xúc | 3–4 | UI | Lưới 3D xấu ở tầm thấp → kiểm bằng mắt trước, không đạt thì bỏ |
| **S-18 Top-down xoay la bàn** | Cho thấy hình học quy hoạch (ô bàn cờ, vòng xuyến, kênh) như bản vẽ | — | `t` 0, `d` ≈ D1, `h` 0 → 90 | xoay phẳng (roll cảm giác) | lưới/ranh phân khu vẽ dần | 3 | URL chuỗi `h`; hoặc ML bearing | Dễ chóng mặt → xoay ≤ 90°, chậm |
| **S-19 Whip pan giữa hai điểm** | Nối nhanh «dự án ↔ trung tâm/metro» không tốn giây | 2 toạ độ | cùng `d`, `t`; tâm nhảy A → B | whip + nhòe hướng 0,3 s | nhãn A, nhãn B, số km giữa khung | 1,5–2,5 | 2 URL + nhòe hậu kỳ | Rẻ nhất trong các chuyển động; dùng thay S-15 ở bản 30 s |
| **S-20 Chèn Street View / ảnh mặt đất** | Bằng chứng «đường thật, cổng thật» → tăng tin cậy | điểm có Street View (đường xanh) hoặc ảnh do chủ dự án cấp | ngang tầm mắt | pan chậm, khung trong khung | khung ảnh bo góc đè lên bản đồ, đường nối tới vị trí chụp | 2–3 | UI Street View; **ưu tiên ảnh của chủ dự án** | Ảnh Street View có thể cũ nhiều năm, có mặt người/biển số → rủi ro quyền + sai hiện trạng |
| **S-21 Trước – sau (ảnh lịch sử)** | Cho thấy khu vực đang phát triển bằng hình, không cần hứa | 2 mốc ảnh có ngày | top-down cố định | wipe trái → phải | nhãn năm ở hai nửa | 3–4 | Earth (tính năng ảnh lịch sử trên bản web **chưa kiểm**); hoặc ảnh chủ dự án | Ngày ảnh phải ghi đúng; không suy «sẽ còn tăng» |
| **S-22 Chia đôi vệ tinh | Map 3D** | So ngay «ảnh thật» với «bố cục khối» cùng một góc | — | cùng tư thế, hai basemap | split dọc trượt | vạch chia sáng, nhãn hai nửa | 2–3 | 2 lần quay cùng URL, đổi basemap bằng UI | Cần khớp tư thế tuyệt đối → dùng đúng một URL |
| **S-23 Hướng nắng – hướng nhà** | Người mua VN quan tâm hướng; cho thấy mặt tiền quay hướng nào | hướng mặt chính (độ) | `t` 0–30, `h` 0 (Bắc lên trên) | dừng, la bàn quay vào | la bàn + mũi tên hướng mặt tiền + nhãn «hướng Đông Nam»… | 2–3 | ML + lớp vẽ mới | La bàn chưa có trong template; không tư vấn phong thuỷ, chỉ nêu hướng |
| **S-24 Orbit 360 tua nhanh** | Tóm tắt toàn bộ bốn phía trong 2–3 s, làm cảnh chuyển nhóm | — | `d` ≈ 1,2·D1, `t` 60, `h` 0 → 360 | hyperlapse orbit | chữ N · E · S · W lướt qua hoặc tên vùng mỗi phía | 2–3 | chuỗi URL đổi `h` mỗi khung (chưa kiểm) / UI rồi tua nhanh | Quay tay 360° khó đều → cần tua + ổn định hậu kỳ |
| **S-25 Người dẫn / logo** | Biết ai chịu trách nhiệm lời nói; tin cậy | PNG cắt nền có quyền, hoặc logo | nền giữ cảnh trước | cutout trượt lên, ra bằng blur ngang | chữ lớn 2 dòng | 1,5–2 | template (đã có) | Không dùng người/giọng của video mẫu |
| **S-26 Pull-back kết + CTA** | Đóng vòng: lùi ra để thấy lại vị trí rồi kêu gọi | số liên hệ, tên kênh, 1 hành động | `d` D1 → 3·D1, `t` 60 → 45, `h` +20° | pull-back + orbit nhẹ | chữ lớn CTA + nhãn thương hiệu; dòng miễn trừ nhỏ | 3–4 | 2 URL / UI; lớp chữ: template (đã có) | Dòng miễn trừ ≥ cỡ đọc được (xem mục 7) |

**Phủ yêu cầu:** nhóm 1 → S-01…S-05 · nhóm 2 → S-06…S-12 (môi trường S-08, lân cận S-09, vị trí + đường S-11, 3D S-10) · nhóm 3 → S-13…S-15 · nhóm 4 → S-16…S-24 (9 góc) + S-25, S-26.

---

## 3. Tình huống kịch bản

Thứ tự viết theo trình tự phát. Cảnh trong ngoặc là tuỳ chọn khi kéo dài.

| # | Tình huống | Bộ cảnh và thứ tự | Tổng | Điểm nhấn cảm xúc | KHÔNG nên đưa vào |
|---|---|---|---|---|---|
| T1 | **Đô thị ven hồ/sông** (kiểu khu đô thị xanh) | S-01 → S-16 → S-03 → S-04 → S-06 → S-08 → S-10 → S-13 → S-26 · (thêm S-17, S-12, S-14 cho 60 s) | 45 s (60 s) | Mặt nước + cây xanh: crane lộ hồ, dolly thấp dọc kênh | Khu công nghiệp cạnh bên ở cận cảnh; số «mật độ cây xanh» không nguồn |
| T2 | **Đô thị trung tâm cũ** (căn hộ/thương mại nội đô) | S-01 → S-03 → S-06 → S-10 → S-11 → S-13 → S-14 → S-26 | 30 s (45 s thêm S-04, S-20) | Gần mọi thứ: nhiều ghim dày trong bán kính nhỏ | Toàn cảnh xa (nội đô nhìn rối); cảnh «thiên nhiên» gượng ép |
| T3 | **Đất nền ngoại thành** | S-01 → S-02 → S-03 → S-04 → S-12 → S-11 → S-19 → S-13 → S-26 | 30–45 s | Rõ ràng, sòng phẳng: ranh lô, kích thước, đường vào | Cảnh nhà 3D (chưa có nhà); mọi câu về tăng giá, «sóng hạ tầng»; quy hoạch chưa phê duyệt |
| T4 | **Khu công nghiệp / logistics** | S-01 → S-02 → S-05 → S-09 → S-11 → S-15 → S-13 → S-26 | 45 s | Kết nối: cao tốc, cảng, sân bay, quãng đường tính bằng km | Giọng cảm xúc, cảnh dolly lãng mạn; tiện ích kiểu trường mầm non |
| T5 | **Nghỉ dưỡng biển/núi** | S-16 → S-17 → S-08 → S-24 → S-10 → S-23 → S-13 → S-26 | 45–60 s | Cảnh quan: mở bằng reveal, giữ lâu ở biển/núi | Thẻ chỉ số dân số; cam kết lợi nhuận cho thuê; cảnh lưới 3D méo ở tầm thấp |
| T6 | **Căn hộ gần metro/trục giao thông** | S-01 → S-03 → S-06 → S-11 → S-19 (dự án ↔ ga) → S-15 → S-14 → S-10 → S-26 | 30–45 s | Thời gian: «bước ra là tới ga», đường sáng chạy theo tuyến | Tuyến/ga **chưa vận hành** mà nói như đã có; thời gian đi không ghi giờ đo |
| T7 | **Bản ngắn 30 s bám sát video mẫu** (kiểm quy trình) | S-01 → S-12 (hook) → S-25 → S-03 → S-02 → S-12 → S-13 (1 điểm) → S-14 → S-26 | 30 s | Nhịp nhanh, mỗi câu một lớp | Cảnh mới chưa có công cụ (S-04, S-15) |

Phân bổ thời lượng gợi ý (để ước lượng, mốc thật theo giọng đọc):

| Bản | Mở + hook | Khu vực + chỉ số | Vào dự án (toàn cảnh, 3D, đường) | Điểm quanh + khoảng cách | CTA |
|---|---|---|---|---|---|
| 30 s | 3 | 6 | 10 | 8 | 3 |
| 45 s | 4 | 9 | 16 | 12 | 4 |
| 60 s | 5 | 12 | 22 | 16 | 5 |

---

## 4. Bảng lựa chọn (cần người dùng chốt)

### 4.1 Cách mở đầu
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. Lao xuống từ vũ trụ (S-01) → hook có ranh sáng — KHUYẾN NGHỊ** | Quen mắt (nhiều video dùng); Earth nạp ảnh chậm | Thấp (2 URL + nhòe) | Mặc định; giống mẫu, đã có hiệu ứng |
| B. Crane reveal (S-16) | Đẹp hơn nhưng phụ thuộc lưới 3D và quay tay | Trung bình | Dự án có cảnh quan mạnh (T1, T5) |
| C. Câu hỏi chữ lớn trên nền tối rồi mới vào bản đồ | Mất «ảnh thật» ở giây đầu | Thấp | Khi hook là một con số gây tò mò có nguồn |

Lý do A: ít rủi ro kỹ thuật nhất và đã chứng minh trong bản dựng thử (8/8 ranh beat khớp).

### 4.2 Cách thể hiện chỉ số khu vực
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. 2–3 thẻ số trên nền bản đồ trôi chậm, có dòng nguồn (S-04) — KHUYẾN NGHỊ** | Phải làm hiệu ứng thẻ số; cần số có nguồn | Trung bình | Mặc định |
| B. Vùng tô màu trên bản đồ (heatmap dân cư, vùng KCN) | Cần dữ liệu không gian; dễ gây hiểu sai nếu thô | Cao | Khi có dữ liệu ranh/vùng thật |
| C. Chỉ nói bằng lời, không số trên khung | Yếu về thuyết phục | Rất thấp | Khi chưa có số đủ tin cậy |

Lý do A: số + nguồn trên khung là thứ người mua chụp màn hình lại; ít rủi ro sai hơn bản đồ nhiệt.

### 4.3 Cách chuyển từ khu vực vào dự án
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. Bậc thang x4→x1 bằng 4 tư thế URL + nhòe (S-06) — KHUYẾN NGHỊ** | Không «liền một mạch»; cần đo `D1` | Thấp | Mặc định; khớp ý người dùng và khả năng hiện có |
| B. Một cú bay liền của Earth (quay tay) | Mượt nhưng không lặp lại được, phụ thuộc mạng | Trung bình | Khi có người quay tay tốt |
| C. Zoom liền từng khung bằng MapLibre | Lặp lại được, nhưng nền vector/Esri, không phải lưới 3D Earth; spike chưa làm | Cao (lần đầu) | Khi cần ranh bám suốt đường zoom |

### 4.4 Cách làm cảnh 3D
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. Earth vệ tinh 3D nghiêng (URL) cho toàn cảnh + MapLibre nhà đùn khối cho cảnh «bố cục khối» — KHUYẾN NGHỊ** | Hai kiểu hình trong một video → cần chuyển cảnh rõ (S-22) | Thấp–trung bình | Mặc định; cả hai đường đã chạy thử |
| B. Earth kiểu Map + 3D buildings (như bản quay của người dùng) | Đẹp, đồng bộ, nhưng **chỉ bật được bằng tay** | Trung bình (quay tay) | Khi người dùng tự quay hoặc chấp nhận click theo toạ độ |
| C. Render 3D phối cảnh của chủ đầu tư | Đẹp nhất, quyền sạch nếu được cấp; không phải hiện trạng | Tuỳ nguồn | Khi dự án chưa xây và có tài sản chính thức |

### 4.5 Cách tag địa điểm + khoảng cách
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. Top-down MapLibre: ghim rơi lần lượt + đường nét đứt + nhãn «tên · X km (đường chim bay)» — KHUYẾN NGHỊ** | Chim bay ngắn hơn đường thật → phải ghi rõ | Trung bình (mở rộng template lên nhiều đường) | Mặc định |
| B. Như A nhưng theo đường đi thật + phút di chuyển | Đúng trải nghiệm hơn; cần routing (Valhalla/OSRM chưa dựng; máy chủ công khai từng bị chặn) | Cao | Khi thời gian đi là luận điểm chính (T6) |
| C. Bấm ghim trực tiếp trên Earth (thẻ thông tin + ảnh của Google) | Nhanh nhưng dùng ảnh/thẻ của bên thứ ba, lẫn UI | Thấp | Chỉ để research, **không đưa vào video** |

### 4.6 Cách kết thúc / CTA
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. Pull-back + chữ lớn một hành động + nhãn thương hiệu + dòng miễn trừ (S-26) — KHUYẾN NGHỊ** | — | Thấp (đã có) | Mặc định |
| B. Người dẫn chỉ tay (như mẫu) | Cần PNG có quyền | Thấp | Kênh cá nhân môi giới |
| C. Thẻ tóm tắt 3 dòng (vị trí · quy mô · liên hệ) | Tĩnh, ít năng lượng | Thấp | Video 60 s, người xem cần chụp màn hình |

### 4.7 Bảng màu hiệu ứng
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. Giữ ngữ nghĩa màu của mẫu: vàng-lục = ranh dự án · cyan = ranh hành chính · xanh dương = khối/diện tích · trắng nét đứt = khoảng cách · đỏ = ghim · cam = từ khoá — KHUYẾN NGHỊ** | Neon có thể lệch tông thương hiệu cao cấp | Không (đã có) | Mặc định; nổi trên ảnh vệ tinh |
| B. Hai màu thương hiệu + trắng | Sang hơn; phải kiểm tương phản trên nền vệ tinh | Thấp | Chủ đầu tư có bộ nhận diện chặt |
| C. Trắng + một màu nhấn | Tối giản; khó phân biệt 3 loại ranh | Thấp | Nghỉ dưỡng cao cấp, ít lớp đồ họa |

Quy tắc chung: **một màu = một nghĩa trong cả video**; tối đa 5 màu.

### 4.8 Nhịp cắt
| Phương án | Đánh đổi / rủi ro | Công sức | Khi nào chọn |
|---|---|---|---|
| **A. Theo mệnh đề lời, 3–4 s/cảnh, chuyển bằng nhòe 0,3–0,6 s; hoà trộn 0,25 s chỉ ở ranh bản đồ→bản đồ — KHUYẾN NGHỊ** | — | Thấp | Mặc định; đúng số đo của mẫu và kết quả UAT |
| B. Nhanh 1,5–2,5 s/cảnh | Giữ chân tốt nhưng số liệu không kịp đọc | Trung bình | Bản 15–20 s chạy quảng cáo |
| C. Chậm 5–7 s/cảnh, ít cắt | Sang, nhưng dễ rớt người xem trên nền tảng ngắn | Thấp | Nghỉ dưỡng, bản 60 s |

---

## 5. Quy trình 9 khâu và cổng duyệt

Phân vai duyệt (theo cách người dùng đã dặn): **Fable** duyệt hộ các cổng thường; **Opus** soát độc lập ở cổng có rủi ro sai dữ kiện; **người dùng** chốt các cổng không đảo ngược hoặc liên quan pháp lý/tiền. Đây là đề xuất, người dùng sửa được.

| # | Khâu | Đầu vào | Đầu ra | Công cụ sẵn có | Ai duyệt | Checklist đo được | Không đạt → quay về |
|---|---|---|---|---|---|---|---|
| 1 | **Mẫu storyboard** | video mẫu, yêu cầu của người dùng | file này | `video-reference-analysis`, `reference-map.md` | **người dùng** (một lần) | ≥ 14 cảnh; đủ 4 nhóm yêu cầu; 8 bảng lựa chọn đã chốt phương án | sửa file này |
| 2 | **Research địa chỉ + dự án** | tên dự án, địa chỉ, tài liệu chủ đầu tư | `research.md` + `site.kml` (ranh dự án, tâm, POI, ranh hành chính) + bảng số liệu có nguồn | trang Google Maps/Earth (đối chiếu toạ độ), KML do chủ dự án cấp, tìm web; `geo_cfg.py` → `report.json` | **Opus** soát dữ kiện → **người dùng** xác nhận tên hành chính, ranh, pháp lý | 100 % số liệu có nguồn + ngày; toạ độ tâm đối chiếu ≥ 2 nguồn; ranh dự án do người cấp/duyệt (agent không đoán); 3–5 POI có toạ độ; tên phường/xã/tỉnh theo đơn vị sau sắp xếp 2025; `report.json` không còn cảnh báo chưa xử lý | khâu 2 (thiếu dữ liệu → hỏi người dùng, không bù bằng suy đoán) |
| 3 | **Chọn nội dung cho từng cảnh** | research, tình huống (T1–T7), thời lượng | bảng «cảnh ↔ dữ kiện ↔ câu lời» | mục 2–3 file này | **Fable** | mỗi cảnh đúng 1 câu hỏi người mua + 1 dữ kiện; đủ 4 nhóm yêu cầu; không cảnh nào dùng số chưa qua khâu 2; tổng giây ước lượng lệch ≤ 10 % mục tiêu | khâu 2 nếu thiếu dữ kiện; khâu 3 nếu thừa/thiếu cảnh |
| 4 | **Storyboard hoàn chỉnh** | bảng khâu 3 | storyboard theo khuôn `video-routing/assets/storyboard.md` + **shot list** (mỗi shot: URL Earth đầy đủ hoặc tham số MapLibre) | khuôn storyboard của repo | **Fable** soát → **người dùng** duyệt | mỗi cảnh có: giây, lời, tham số camera đầu–cuối, lớp hiệu ứng, cách quay, nguồn dữ kiện; lời đọc ≈ 4 từ/giây (mẫu: 125 từ / 30,8 s, tức 6,1 từ/giây tính trên 20,6 s lời); mỗi dòng chữ ≤ 25 ký tự, cỡ ≥ 50 px; không vi phạm mục 7 | khâu 3 |
| 5 | **Quay Google Earth lấy shot gốc** | shot list | clip/ảnh raw từng shot + `provenance.json` | URL camera Earth (đã chạy), thao tác UI tay (Map/3D buildings), MapLibre `geo-capture.html` (Esri / OpenFreeMap) cho cảnh top-down; screencast (chưa kiểm) | **Fable** (kỹ thuật) | mỗi shot đúng tư thế trong shot list; không dính UI, hộp thông báo, con trỏ; đủ phân giải sau khi cắt 9:16 (≥ 1080×1920, không phóng quá 100 %); thời lượng ≥ cảnh + 1 s đầu/cuối; ảnh nạp nét (không còn ô mờ) | khâu 5 (quay lại); shot không quay nổi → khâu 4 đổi cảnh |
| 6 | **Chốt cảnh raw** | clip raw | bản ráp thô không hiệu ứng (đúng thứ tự, đúng giây) | `video-edit`, `reference tiles` để soi lưới | **người dùng** (xem bằng mắt) | đủ 100 % cảnh trong storyboard; tổng thời lượng lệch ≤ ±1 s; đúng địa điểm (người dùng gật «đúng dự án»); không cảnh nào lưới 3D méo lộ | khâu 5 |
| 7 | **Thêm hiệu ứng (draft 1)** — diện tích, ranh, địa điểm, khoảng cách | bản thô + `site.kml` | draft 1: lớp đồ họa gắn vị trí | `land-plot-map-video` (template + `geo_cfg.py`), HyperFrames, `check --strict` | **Opus** soát số ↔ `report.json` → **Fable** | `check --strict` sạch; 100 % số trên khung khớp `report.json`/research; đa giác không lệch ranh khi soi lưới khung; mỗi màu một nghĩa; nhãn không đè nhau; khoảng cách ghi rõ «đường chim bay» nếu chưa có routing | lệch vị trí → khâu 2 (toạ độ) hoặc 5 (shot); lỗi hiệu ứng → khâu 7 |
| 8 | **Draft 2** — ảnh + chữ + chữ động | draft 1, lời đã chốt | draft 2 có chữ gõ, từ khoá, thẻ số, nhãn nguồn, CTA | template (chữ gõ, pop), `hyperframes-animation`, `video-theme-library` | **Fable** → **người dùng** | chữ ≥ 50 px, ≤ 25 ký tự/dòng; vùng an toàn trên/dưới không bị che; 1 mệnh đề = 1 lớp đồ họa mới; mọi thẻ số có dòng nguồn; có dòng miễn trừ ở cảnh cuối | khâu 8; sai nội dung → khâu 4 |
| 9 | **Giọng + chuyển cảnh (bản cuối)** | draft 2 | MP4 cuối + ghi chú QA | `video-studio narrate` (ghim profile), `reference transcribe` để lấy cue, `video-studio render`, `rhythm_align.py`, `reference tiles` | **Opus** review cuối → **người dùng** chốt phát hành | mốc đồ họa lệch cue lời ≤ ±0,5 s; thời lượng = giọng + 0,5 s; chuyển cảnh nhòe 0,3–0,6 s; xem **hết** lưới khung; không tư liệu của video mẫu; nhạc/giọng/người dẫn có quyền ghi trong `provenance.json` | lệch nhịp → khâu 9; chữ sai → khâu 8; dữ kiện sai → khâu 2 |

Ghi chú: không khâu nào tự đăng/gửi; phát hành là quyết định riêng của người dùng.

---

## 6. Hiệu ứng ↔ công cụ

### 6.1 Đã có trong template `land-plot-map-video` (đã render + `check` sạch)
| Hiệu ứng | Helper / chỗ làm | Dùng ở cảnh |
|---|---|---|
| Zoom-blur lao vào / chuyển tầng | `blurIn` | S-01, S-06, mọi chuyển cảnh |
| Pan nhòe rồi nét | `fromTo` trên lớp camera | S-08, S-19 |
| Đa giác phát sáng + viền vẽ dần | `glowPoly`, `showPoly`/`drawStroke` | S-02, S-03, S-09, S-12 |
| Chữ gõ + từ khoá đổi màu | `typed` | hook, S-07, S-26 |
| Chữ nghiêng theo hình | `label(..., rot)` | S-02, S-03 |
| Ghim + vòng sóng (lặp hữu hạn) | `circle` repeat 3 | S-02, S-13 |
| Camera xoay nhẹ | rotation + scale | S-12 |
| **Một** đường nét đứt vẽ dần | mask + dashoffset | S-13 (1 điểm) |
| **Một** vòng bán kính nở | scale 0→1 | S-14 |
| Ghim rơi nảy lần lượt (4 biểu tượng) | `bounce.out`, stagger | S-13 |
| Khối xanh + nhãn A×B | scene `size` | S-12 |
| Người dẫn lao vào / trượt ra, CTA | scene `hook`, `cta` | S-25, S-26 |
| Số đo, khoảng cách chim bay tính từ toạ độ | `geo_cfg.py` → `report.json` | S-12, S-13 |
| Nhà 3D đùn khối (OSM trên Esri, pitch 50–55) | `geo-capture.html` `mode=esri3d` | S-10 (đường lùi) |

### 6.2 Còn phải làm / chưa kiểm (nói thẳng)
| Việc | Hiện trạng | Cảnh bị ảnh hưởng |
|---|---|---|
| Quay **liên tục** chuyển động camera Google Earth | Chưa kiểm (screencast trình duyệt chưa thử); hiện chỉ có ảnh tĩnh theo URL | S-07, S-08, S-15, S-16, S-17, S-24 |
| Bật kiểu **Map** + **3D buildings**, **Photos**, mức chi tiết trên Earth | Chỉ có trên giao diện canvas, chưa thấy tham số URL; cây a11y gần rỗng → phải click theo toạ độ hoặc người quay tay | S-10, S-22 |
| Tắt hộp thông báo / mẹo của Earth | Escape đóng hộp lớn; hộp «Dismiss» chưa tự tắt được | mọi shot Earth |
| Khung dọc 9:16 trên Earth | Bản quay của người dùng là 1280×720 ngang; quay ở cửa sổ dọc 1080×1920 **chưa thử**; cắt từ ngang thì thiếu phân giải | mọi shot Earth |
| Gắn lớp phủ toạ độ lên shot Earth **nghiêng/đang chuyển động** | Chưa có: tỉ lệ Earth không theo công thức Mercator; cần khớp camera hoặc canh tay bằng điểm khống chế | S-06, S-07, S-08 khi có ranh |
| Nhiều đường khoảng cách + nhãn km từng đường | Template mới có 1 đường tới `trung-tam` | S-13 |
| Nhiều vòng bán kính đồng tâm | Template có 1 vòng | S-14 |
| Thẻ chỉ số (số đếm lên + dòng nguồn) | Chưa có | S-04 |
| Tô sáng tuyến đường / tuyến chạy trước camera | Chưa có (cần polyline từ KML) | S-11, S-15 |
| Nhiều đa giác dự án lân cận nhiều màu | Chưa có trong CFG (mới có lô + xã + tỉnh) | S-09 |
| Nhãn bậc zoom x4→x1, la bàn, split, wipe trước–sau | Chưa có | S-06, S-23, S-22, S-21 |
| Ranh phường/xã từ OpenFreeMap (`admin_level=6`) | Có đường biên nhưng chưa kiểm là cấp nào; tô nền cần ghép vòng kín | S-03 |
| Khoảng cách theo đường + isochrone | Chưa có routing; Nominatim/Overpass công khai từng bị chặn/quá tải ngày 19/11 | S-13, S-14, S-15 |
| Camera MapLibre từng khung (spike «bản đồ là động cơ») | Chưa làm | phương án 4.3-C |
| Ảnh lịch sử trên Earth web | Chưa kiểm có dùng được không | S-21 |
| Giọng đọc + nhạc cho video BĐS | Chưa làm trong bản thử | khâu 9 |

**Hệ quả cho thứ tự làm:** bản đầu tiên nên là **T7 (30 s)** chỉ dùng cảnh ở 6.1 + shot Earth tĩnh theo URL; mở rộng dần S-13 nhiều điểm → S-04 thẻ số → cảnh chuyển động Earth.

---

## 7. Quy tắc nội dung BĐS

**Không nói**
- Không hứa lợi nhuận, không «chắc chắn tăng giá», «cam kết sinh lời», «lướt sóng», «không mua là tiếc»; không so sánh hạ thấp dự án khác.
- Không nói hạ tầng/tiện ích **chưa có** như đã có. Phải kèm trạng thái: đã vận hành · đang thi công · đã phê duyệt · mới là đề xuất.
- Không gọi vòng tròn mét là «5 phút di chuyển»; không ghi khoảng cách chim bay như quãng đường đi.

**Số liệu**
- Mọi con số trên khung và trong lời có **nguồn + ngày** trong `research.md`; thẻ chỉ số hiện dòng nguồn rút gọn. Không có nguồn → không đưa.
- Diện tích, kích thước, khoảng cách: tính từ toạ độ (`report.json`); lệch số hồ sơ → dừng, hỏi.
- «Hot hay không» diễn đạt bằng dữ kiện kiểm được (dân số, dự án hạ tầng đã khởi công, khu việc làm), không bằng tính từ.

**Cần người dùng / pháp lý xác nhận trước khi phát hành**
- Tình trạng pháp lý dự án và điều kiện được quảng cáo/mở bán; nội dung bắt buộc trong quảng cáo BĐS theo luật hiện hành (**tôi chưa tra điều khoản trong phiên này**).
- Tên đơn vị hành chính sau sắp xếp 2025; ranh dự án; tên và logo chủ đầu tư, đại lý.
- Giá, chính sách bán hàng, tiến độ: chỉ đưa khi có văn bản của chủ đầu tư.
- Dòng miễn trừ ở cảnh cuối (đề xuất): «Thông tin mang tính tham khảo, cập nhật đến <ngày>; khoảng cách đo theo đường chim bay.»

**Quyền ảnh nền và tài sản**
- **Google Earth:** người dùng đã quyết bỏ ghi nguồn; **rủi ro thuộc về người dùng**; ghi quyết định này vào `provenance.json` của từng dự án. Tôi chưa đọc lại điều khoản Google trong phiên này.
- **Esri World Imagery:** điều khoản video thương mại chưa kiểm, có yêu cầu ghi nguồn. **OpenFreeMap/OSM:** cần ghi nguồn (© OpenStreetMap contributors · OpenMapTiles).
- Thẻ thông tin, ảnh người dùng, Street View trên Earth là của bên thứ ba → không đưa vào video (trừ khi người dùng quyết khác); ưu tiên ảnh/flycam của chủ dự án.
- Người dẫn, font, nhạc, giọng: phải có quyền; không dùng bất kỳ tư liệu nào của video mẫu.

---

## 8. Việc chờ người dùng quyết

1. Nghĩa của «zoom x4→x3→x2→x1»: bậc thang khoảng cách `4·D1→D1` (đang giả định) hay cách khác?
2. Chốt 8 bảng lựa chọn mục 4 (đang đề xuất phương án A ở cả 8).
3. Phân vai duyệt mục 5 (Fable / Opus / người dùng) có đúng ý không.
4. Dự án đầu tiên để chạy thử và tình huống (đề xuất: khu Swan Lake – Ecopark theo T1, làm trước bản T7 30 s).
5. Ai quay các shot Earth cần thao tác tay (Map + 3D buildings, orbit): người dùng quay hay agent click theo toạ độ (chưa kiểm)?
