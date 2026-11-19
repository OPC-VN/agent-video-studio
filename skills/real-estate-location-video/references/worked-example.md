# Ví dụ đã chạy thật: video dự án BĐS 9:16 qua ba bản (v1 → v2 → v3)

> **Kết luận:** cùng một dự án, ba lần dựng cho thấy điều gì đổi theo phản hồi. Dùng làm **khuôn storyboard** cho dự án khác: giữ cấu trúc cảnh, thay dữ kiện bằng research của dự án mới. Toạ độ và số liệu bên dưới là của dự án mẫu trong repo (ví dụ minh hoạ), **không** dùng lại cho dự án khác.

## 1. Khung cảnh chung (khuôn)

| Khối | Mục đích | Cảnh điển hình |
|---|---|---|
| Mở + hook | giữ người xem 3 s đầu | zoom từ rộng xuống dự án + tên dự án gõ chữ |
| Khu vực + chỉ số | «ở đâu, khu vực mạnh thế nào» | viền tỉnh neon + 2 thẻ số có nguồn; viền xã + dân số, diện tích |
| Vào dự án | định vị tuyệt đối | zoom xã → khu đô thị → dự án; ảnh cận cảnh (thật có quyền, hoặc vệ tinh 3D gắn «minh hoạ») |
| Môi trường sát dự án | điểm mạnh vật lý | hồ/công viên **bo viền** + đường nối + số km |
| Khối 3D | bố cục toà nhà | 3–4 góc: mọc + xoay, bay thấp, xoay toàn cảnh, nghiêng từ trên xuống |
| Lân cận + tiện ích | «quanh đây có gì» | khu đô thị/TTTM lân cận kèm km; vòng bán kính + radar + biểu tượng nhóm + chú giải |
| Kết nối | «đi vào trung tâm thế nào» | tên trục chính + cầu + mũi tên vào nội thành; mốc trung tâm kèm km |
| CTA | hành động | chữ CTA + miễn trừ giữ đến hết |

## 2. Ba bản

| | v1 (draft 1, 45 s) | v2 (76 s) | v3 (95,5 s) |
|---|---|---|---|
| Mở đầu | clip Earth 4 s (giật) | như v1, làm chậm (nhân khung) | **zoom liền mạch** toàn quốc → tỉnh 5 s (quay từng khung) |
| Tỉnh | 2 s | 12,4 s, viền + 2 thẻ số | như v2, viền **neon** + đầu sáng |
| Xã | 1,2 s | 5,6 s đứng yên | như v2 + clip zoom tỉnh → xã 3,2 s |
| Zoom vào dự án | 4 ảnh × 0,75 s | 3 bậc × 1,7 s | clip zoom xã → dự án 4,5 s liền mạch |
| Ảnh cận cảnh | — | Earth 3D tĩnh 4,4 s | như v2 |
| Hồ | chip «0,24 km» thoáng qua | **bo viền hồ** + ghim + đường nối + hộp số, giữ 7 s | như v2, viền neon |
| 3D | 1 clip 5 s | 1 clip 6 s | **4 góc**, 22 s |
| Lân cận | tag chồng nhau | 1 đường nối + hộp số | như v2 |
| Tiện ích | danh sách tag | vòng 0,5/1,5 km + biểu tượng + chú giải | thêm **radar quét** |
| Đường | 14 đoạn dài nhất, không tên | 4 trục có tên + cầu + mũi tên | như v2, neon |
| Mốc trung tâm | tag | đường nối + «km» + vòng khoanh hồ | như v2 |
| CTA | mất ở 2 s cuối | layer riêng đến hết | như v2 |
| Lời | 11 câu, tốc độ sát trần | 14 câu, ≤ 3,6 tiếng/s | 18 câu khớp cảnh |

## 3. Thứ tự việc nên lặp lại cho dự án mới

1. Intake (tên, địa chỉ, toạ độ, độ dài 60–75 s, **ảnh thật có quyền?**, CTA, quyền ảnh nền).
2. Research có nguồn (Opus): hành chính hiện hành, chỉ số khu vực, hạ tầng, 3–5 địa điểm kèm toạ độ + km, **tên trục đường + cầu (mức tin cậy)**, 2–3 địa bàn chính của tỉnh nếu muốn, câu không nên nói.
3. Storyboard (Fable, theo khuôn mục 1 + sàn thời gian đọc) → cổng Opus.
4. Quay raw: ảnh tĩnh Earth nghiêng, MapLibre top-down (`maplibre_shots.mjs`, kể cả `mask-water` cho viền hồ), ranh + tên đường (`extract_osm.mjs`), **clip camera mượt** (`camera_path_capture.mjs`).
5. Dựng draft bằng `build_v3.example.py` + `draft2_template.html`; `check --strict`; xem lưới khung.
6. Giọng từng câu (`voice_batch.example.py`) + ghép nhạc nền (`voice-and-mix.md`).
7. Duyệt (checklist [`review-lessons.md`](review-lessons.md)) → người nghe + chốt dữ kiện, quyền → phát hành.

## 4. Điều vẫn chặn phát hành của ví dụ (đừng quên ở dự án mới)

Tên kênh/CTA, nhãn «quảng cáo» theo quy định, quyền ảnh nền (Google Earth, Esri) và điều khoản thương mại, giấy phép nhạc, đồng ý dùng giọng, xác nhận tên dự án và tên đơn vị hành chính hiện hành, xác nhận tên đường và ranh lấy từ OSM, ảnh thật có quyền (nếu muốn thay ảnh vệ tinh minh hoạ).
