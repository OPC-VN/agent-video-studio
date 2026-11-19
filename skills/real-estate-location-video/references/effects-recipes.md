# Công thức hiệu ứng (đã làm và được người dùng đánh giá tốt)

Mọi hiệu ứng phải **trả lời một câu hỏi của người mua** và gắn vào **một mệnh đề lời** (một mệnh đề = một lớp đồ họa mới). Số đo trên khung tính từ toạ độ, không gõ tay.

## A. Tô viền ranh hành chính (bản đồ top-down)

**Kết quả:** đường biên tỉnh (cyan) và cấp thấp hơn (vàng) vẽ đúng chỗ trên ảnh vệ tinh, vẽ dần khi vào cảnh.

1. **Nguồn dữ liệu:** lớp `boundary` của OpenFreeMap (vector OSM). `admin_level` 2 quốc gia · **4 tỉnh/thành** · **6 cấp thấp hơn** (sau sắp xếp 2025 suy luận là xã/phường: **cần người xác nhận**) · không có cấp 8. Lọc `maritime != 1`. Chỉ có **đường biên** (không có đa giác) → vẽ viền sáng, **không tô nền**; muốn tô cần KML của người dùng.
2. **Lấy dữ liệu:** `assets/extract_osm.mjs` đặt MapLibre đúng **tâm + zoom của ảnh nền** (zoom MapLibre = zoom ô 256 px − 1), chờ `idle` + 1,5 s, `querySourceFeatures('openmaptiles', {sourceLayer:'boundary', filter})` → toạ độ lon/lat → `osm_overlays.json`. Khung nhìn càng xa số mảnh càng lớn (khung tỉnh ≈ 1.060 mảnh cấp 6): **ở khung tỉnh chỉ vẽ cấp 4**.
3. **Chiếu ra pixel:** `assets/osm_overlay.py` (`svg_paths`) dùng Web Mercator của `geo_cfg.to_frame` với **cùng tâm và zoom** → chuỗi `d` của `<path>` trên khung 1080×1920. **Chỉ đúng ảnh top-down pitch 0.** Kiểm bằng cách vẽ chồng lên ảnh trước khi dựng (đã làm ở `raw/overlay_check.png`: viền khớp sông và khu dân cư).
4. **Vẽ dần:** mỗi mảnh `<path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" stroke-linejoin="round">`; GSAP `strokeDashoffset 1→0`, 1,0–1,6 s, `power2.inOut`, so le 0,03 s giữa các mảnh. Hai lớp: lớp **glow** (cùng path, `stroke-width` + 10, `filter: blur(9px)` bằng `feGaussianBlur stdDeviation=9`) dưới lớp nét.
5. **Màu/độ dày:** tỉnh `#27e6ff` 6–9 px; cấp 6 `#e4ff3a` 3–4 px; ghim dự án đỏ `#e11d2e` + vòng sóng trắng (lặp **hữu hạn** 3 lần).
6. **Nhóm chung:** lớp phủ nằm **cùng nhóm transform** với ảnh nền (zoom/pan 1,10–1,22 lần) — tách riêng thì viền trôi.
7. **Nhãn:** «TỈNH …», «XÃ …» đặt tay hoặc theo KML; tên đơn vị hành chính phải **người xác nhận** (đã đổi sau 2025). Nguồn rút gọn: «© OpenStreetMap», «ranh tham khảo, không phải ranh pháp lý».
8. **Giới hạn:** không biết đa giác nào là «xã của dự án» khi chỉ có đường; muốn đánh dấu đúng thì cần KML hoặc ghép đường thành vòng kín (chưa làm).

## B. Hiệu ứng 3D: vệ tinh → nhà mọc lên → kiểu Map

**Kết quả:** ảnh vệ tinh, các toà nhà **mọc lên theo chiều cao** (tháp cao tô xanh/vàng), vệ tinh mờ dần để lộ bản đồ sáng (nước, công viên, đường) rồi camera xoay quanh.

Script `assets/three_d_capture.mjs` (MapLibre + OpenFreeMap + Esri), quay **từng khung** (150 khung = 5 s, 30 fps) rồi `ffmpeg -framerate 30 -i f%04d.png -c:v libx264 -crf 17 -pix_fmt yuv420p`.

| Thông số | Giá trị đã dùng | Quy tắc |
|---|---|---|
| Style | `liberty` | ẩn **mọi lớp `symbol`** (không nhãn) |
| Ảnh vệ tinh | lớp `raster` Esri chèn **trước lớp `building`** | nằm trên nước/đường/công viên, dưới nhà; mờ dần làm lộ bản đồ |
| Nhà mọc | hệ số `K` nhân `render_height` (`fill-extrusion-height`), `K = 1−(1−t)³` trong 0,7–2,3 s | `setPaintProperty` từng khung; khi `K > 0,02` đặt lớp `building` phẳng `fill-opacity 0` |
| Màu theo chiều cao | nội suy `render_height`: 0 `#e8ecf1` · 30 `#cfe3f7` · 60 `#8fd3ff` · 100 `#4fc3ff` · 140 `#ffd34d`; opacity 0,96 | tháp cao nổi bật mà không cần biết vị trí dự án |
| Vệ tinh mờ | opacity 1→0 trong 2,7–4,0 s | |
| Camera | tâm dự án, zoom ô 256 px 17 → 17,35, pitch 55, bearing 40° → 85° (`easeInOut`) | xoay vừa phải; quá nhanh gây nhoè |
| Chờ tải ô | làm nóng 5 mốc (0, 1,5, 3, 4,5, hết) mỗi mốc 1,2 s; mỗi khung chờ `idle` tối đa 2,5 s | thiếu bước này khung đầu bị trống |

**Vì sao làm bằng MapLibre mà không bật «3D buildings» của Google Earth:** dữ liệu 3D của Google (kiểu Map) **chưa có các toà tháp mới** của dự án mẫu (chỉ thấy bãi cỏ), trong khi dữ liệu OSM đã có. Ngược lại ảnh Esri **cũ hơn** OSM: vệ tinh còn là ruộng mà nhà đã mọc — dùng để **nhấn «khối dự kiến/minh hoạ»**, luôn gắn nhãn «KHỐI 3D MINH HOẠ» và không để hiểu là hiện trạng. Kiểm bằng mắt: khối có hiện đúng cụm tháp không.

## C. Hiệu ứng đã có từ `land-plot-map-video` (dùng lại)

Ghim + vòng sóng, đường nét đứt khoảng cách (mask + dashoffset), vòng bán kính, nhãn nghiêng pop `back.out(2)`, chữ gõ từng ký tự, zoom-blur vào/ra, khối xanh neon + nhãn A×B. Chi tiết và bẫy: `skills/land-plot-map-video/references/effects-map.md`. Tag địa điểm: 2 dòng, dòng 1 tên ≤ 25 ký tự, dòng 2 «X,XX km chim bay»; bật theo thứ tự đọc; **luôn ghi «chim bay»** khi chưa có routing.

## D. Camera Google Earth (shot điện ảnh)

Dolly (lăn chuột), lia (kéo chuột trái), xoay hướng (kéo chuột phải ngang), bậc thang zoom x4→x1 (4 URL cách đều khoảng cách `d`), nhòe vào/ra ở chỗ nối. Thao tác, toạ độ giao diện và bẫy: `earth-capture.md`.

## E. Quy tắc chung

1. Hai nguồn hình: **Earth** cho cảnh điện ảnh (toàn cảnh, 3D nghiêng); **MapLibre top-down** cho **mọi cảnh có lớp phủ toạ độ** (ranh, khoảng cách, bán kính). Trên shot Earth nghiêng chỉ đặt tay ghim ở tâm khung.
2. Lớp phủ **chung nhóm transform** với ảnh; hiệu ứng chạy **khi camera đã dừng**, không vẽ khi đang xoay.
3. Mọi lặp hữu hạn, không `Math.random`, một timeline `paused` đăng ký vào `window.__timelines`.
4. Chữ ≥ 50 px (dòng nguồn ≥ 28 px: cần người chấp nhận), tiếng Việt kiểm dấu; 15 % đáy để trống.
5. Số liệu có nguồn + ngày; không giá, không «chắc chắn tăng giá», không phút di chuyển khi chưa có routing.

## F. Hiệu ứng bổ sung từ bản v2 (đã chạy thật; nhịp xem `pacing-and-clarity.md`)

Mọi loại dưới đây là một mục trong danh sách `FX` của `assets/build_v2.example.py` + `draft2_template.html`.

| Hiệu ứng (`t`) | Việc | Cách làm | Quy tắc / bẫy |
|---|---|---|---|
| **Bo viền hồ** (`poly`) | khoanh một mặt nước có tên, viền sáng vẽ dần rồi tô nhạt | chụp `mode: mask-water` (trắng trên đen, cùng tâm + zoom với ảnh nền) bằng `maplibre_shots.mjs`; `water_outline.outline(mask, seed)` chọn mặt nước chứa/ gần nhất điểm `seed` (toạ độ POI của đối tượng), dò viền, rút gọn → `d` khép kín | **Không** lấy đa giác từ `querySourceFeatures`: bị cắt ở mép ô vector, viền có đường ngang giả. Mặt nước nhỏ hơn ~40 px ở khung đó (vd hồ trung tâm ở khung 12 km) thì khoanh bằng `ring` thay vì `poly`. Kiểm bằng mắt: viền phải trùng mặt nước trong ảnh vệ tinh; tên hồ là của người xác nhận |
| **Vòng bán kính** (`ring`) | «trong X km có gì» | bán kính px = mét ÷ `156543,03 × cos(vĩ độ) ÷ 2^zoom` (zoom ô 256 px); nở lần lượt; nhãn ở **đáy** vòng để không đè biểu tượng | cấp vòng theo dữ liệu thật của dự án (vd 0,5 · 1,5 km), luôn «chim bay», không ghi phút |
| **Biểu tượng nhóm** (`icon`) + **chú giải** (`legend`) | bệnh viện (`cross`), trường (`tri`), công viên (`dia`), thương mại (`sq`) | toạ độ từ research; mỗi biểu tượng hiện cùng lúc với dòng chú giải của nó («tên · X,XX km») | điểm gần nhau thì biểu tượng nhỏ (r ≈ 20) và để tên ở chú giải, không dán nhãn lên bản đồ |
| **Hộp số giữa đường nối** (`numbox`) + `dash` | «dự án ↔ đối tượng ↔ số km» trên một khung | `dash` từ dự án tới đối tượng, hộp số đặt cạnh trung điểm (hoặc nối bằng một `dash` ngắn nếu đoạn quá ngắn) | số km tính haversine và **assert ±3 %** với số research trong `build` |
| **Tên đường + cầu** (`rlabel`, `path`) | nêu rõ tuyến chính, tuyến qua cầu vào nội thành | `extract_osm.mjs` xuất `rnames` (tên, `ref`, cầu) từ lớp `transportation_name`; chọn tuyến **theo vai trò/tên**, không theo độ dài; nhãn đặt giữa mảnh dài nhất, xoay theo hướng, ép góc vào (−90°, 90°] | tên OSM chỉ là gợi ý: **người xác nhận**. Không khẳng định hai tuyến nối với nhau khi chưa kiểm; ghi «tuyến chính» + khoảng cách chim bay tới cầu |
| **Mũi tên hướng** (`arrow`) | «→ Hà Nội» | từ cầu hướng về toạ độ trung tâm | một nhãn ngắn ở đầu mũi tên |
| **Màn tối** (`veil`) | tăng độ đọc thẻ số trên bản đồ sáng | `opacity` 0 → 0,4 trước khi thẻ hiện | đặt trước các phần tử khác của cảnh |

**Mốc trung tâm (vd Hồ Hoàn Kiếm):** luôn có đường nối + số km trên một khung đứng yên; ảnh thật chỉ khi có quyền (xem `pacing-and-clarity.md` mục 5).
**Chưa làm:** nhãn bám toà trên khối 3D (`map.project` từng khung), biểu tượng POI tự động từ lớp `poi` (chưa kiểm tên/hoạt động nên không đưa lên màn hình).

## G. Bản v3: neon, đường sáng, radar, nhiều góc 3D (đã chạy thật)

| Hiệu ứng | Cách làm | Quy tắc |
|---|---|---|
| **Viền neon** (`path`, `poly`) | `neon()` trong `draft2_template.html`: quầng blur lớn + quầng vừa + nét màu + lõi trắng mảnh + **đầu sáng** chạy dẫn đường cùng nhịp vẽ; xong thì một nhịp sáng rồi giữ | nét 8–12 px; viền chạy **sau khi camera dừng**; ranh chỉ «tham khảo» khi nguồn OSM |
| **Đường chấm sáng chạy** (`dash`) | nét đứt có lớp sáng mờ phía dưới, «kiến bò» (dashoffset một tween tuyến tính) và tia sáng chạy từ dự án tới đối tượng 3 lần | không `repeat:-1`; điểm cuối vàng |
| **Radar quét** (`ring` với `radar:true`) | `conic-gradient` quay (`rotation`) trong vòng bán kính, kèm 2 vòng đồng tâm mờ; quét `turns` vòng rồi tắt | chỉ cho vòng chính (vd 1,5 km); biểu tượng POI hiện đúng lúc lời nhắc tới |
| **Ghim** (`pin`) | chấm bật một lần + quầng đứng yên | **cấm** vòng sóng lặp |
| **Zoom liền mạch** | `camera_path_capture.mjs` + `camera_paths.example.json` (D1 toàn quốc→tỉnh, D2 tỉnh→xã, D3 xã→dự án) | khung cuối clip = khung nhìn cảnh tĩnh kế tiếp |
| **Nhiều góc 3D** | cùng script với `buildings:true`: E1 nhà mọc + xoay, E2 bay thấp từ phía hồ (pitch ~68°, bearing ~175–195° = nhìn về phía Nam), E3 xoay toàn cảnh (pitch 52°, bearing 0→200°), E4 nghiêng từ trên xuống (pitch 0→62°) | `sat` ≥ 0,85 ở E2–E4; mỗi góc 5–6 s; nhãn «KHỐI 3D MINH HOẠ» + dòng nguồn OSM |
