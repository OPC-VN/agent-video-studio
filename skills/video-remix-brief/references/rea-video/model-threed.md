# Sinh 3D (nhất quán đa góc sản phẩm / bàn xoay / khối trắng tham chiếu)
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/models/threed.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Tổng số mục: 3 mô hình.

---

### 1. `hunyuan-3d` — Hunyuan 3D (3.x)
- **Nhà cung cấp / loại:** Tencent · threed · `ga`
- **Truy cập:** api, open-weights
- **Năng lực:** `threed.image_to_3d`
- **Điểm mạnh:**
  - Ổn định nhất trong ba mô hình; hiếm khi vỡ mặt lưới.
  - Hỗ trợ chỉ định góc nhìn đầu vào; có thể chọn vật liệu PBR, texture PBR 4K phải trả thêm phí.
  - Phù hợp nhất cho trưng bày sản phẩm độ trung thực cao.
- **Giấy phép:** cho phép thương mại đối với bản lưu trữ; giấy phép trọng số mở cần kiểm tra riêng.
- **Nguồn:** https://www.3daistudio.com/blog/rodin-2-5-vs-tripo-vs-hunyuan-3d-comparison
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 2. `rodin-gen-2.5` — Rodin Gen-2.5
- **Nhà cung cấp / loại:** Hyper3D / Deemos · threed · `ga`
- **Truy cập:** api, app
- **Năng lực:** `threed.image_to_3d`
- **Điểm mạnh:**
  - 5 mức chất lượng; nhận 2–5 ảnh các góc nhìn.
  - Có thể bỏ ánh sáng nướng (baked) của ảnh gốc; có công tắc đối xứng, phù hợp với vật đối xứng như xe.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://www.3daistudio.com/blog/rodin-2-5-vs-tripo-vs-hunyuan-3d-comparison
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 3. `tripo-p1` — Tripo P1
- **Nhà cung cấp / loại:** Tripo · threed · `ga`
- **Truy cập:** api, app
- **Năng lực:** `threed.image_to_3d`
- **Điểm mạnh:** lưới sạch (dưới khoảng 20 nghìn mặt), có texture PBR; phù hợp làm mô hình poly thấp cho game.
- **Điểm yếu:** không phù hợp để trưng bày sản phẩm độ trung thực cao.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://www.3daistudio.com/blog/rodin-2-5-vs-tripo-vs-hunyuan-3d-comparison
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
