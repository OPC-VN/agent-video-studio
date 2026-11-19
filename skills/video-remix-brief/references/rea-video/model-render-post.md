# Render từ code, ghép và hậu kỳ
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/models/render-post.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Chú thích: `render.code_graphics` = vẽ đồ họa bằng code; `render.compose` = ghép hình; `render.3d_scene` = dựng cảnh 3D; `render.web_capture` = ghi hình trang web; `post.upscale` = siêu phân giải; `post.frame_interp` = nội suy khung hình.

Tổng số mục: 10 công cụ.

---

### 1. `remotion` — Remotion
- **Nhà cung cấp / loại:** Remotion (mã nguồn mở, thương mại cần giấy phép) · render · `ga`
- **Truy cập:** open-weights
- **Năng lực:** `render.code_graphics`, `render.compose`
- **Điểm mạnh:**
  - Viết video bằng React: chữ, giao diện, biểu đồ, đồ họa chuyển động đều chính xác 100% và tham số hóa được.
  - Nhà cung cấp có Agent Skills, dùng trực tiếp với Claude Code và Codex.
  - Kết quả render cố định, có thể so khác biệt từng khung với video gốc ở mức pixel.
- **Điểm yếu:** cảnh chân thực kiểu ảnh chụp cần xếp chồng với lớp sinh.
- **Giấy phép:** commercial: conditional — cá nhân và nhóm nhỏ miễn phí; công ty cần mua giấy phép Remotion.
- **Nguồn:**
  - https://www.tella.com/blog/how-to-use-remotion-agent-skills-with-claude-code
  - https://www.remotion.dev/
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### 2. `motion-canvas` — Motion Canvas
- **Loại:** render · `ga` · mã nguồn mở
- **Năng lực:** `render.code_graphics`
- **Điểm mạnh:** mô tả hoạt ảnh bằng bộ sinh TypeScript, phù hợp cho hiệu ứng giảng giải; giấy phép MIT.
- **Giấy phép:** cho phép thương mại (MIT).
- **Nguồn:** https://motioncanvas.io/
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### 3. `html-gsap-playwright` — HTML + GSAP + Playwright ghi hình
- **Loại:** render · `ga` · tổ hợp mã nguồn mở
- **Năng lực:** `render.code_graphics`, `render.web_capture`
- **Điểm mạnh:**
  - Phù hợp cho demo giao diện: điều khiển trực tiếp trang sản phẩm thật hoặc giao diện dựng lại.
  - Hypit cũng đi theo lối HTML cộng Chromium không đầu.
- **Giấy phép:** cho phép thương mại. GSAP hiện miễn phí (kể cả thương mại); Playwright là Apache 2.0.
- **Nguồn:** https://playwright.dev/
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** medium

### 4. `blender` — Blender
- **Loại:** render · `ga` · mã nguồn mở
- **Năng lực:** `render.3d_scene`
- **Điểm mạnh:** nhập được mô hình sản phẩm 3D do AI sinh; render vòng xoay hoặc tham chiếu khối trắng theo quỹ đạo camera đã suy ngược.
- **Giấy phép:** cho phép thương mại (GPL; nội dung đầu ra không bị ràng buộc).
- **Nguồn:** https://www.blender.org/
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### 5. `ffmpeg` — FFmpeg
- **Loại:** render · `ga` · mã nguồn mở
- **Năng lực:** `render.compose`
- **Điểm mạnh:** cắt, nối, chồng lớp, trộn âm thanh, mã hóa; là nền tảng của mọi bước.
- **Giấy phép:** cho phép thương mại (LGPL/GPL, tùy tùy chọn biên dịch).
- **Nguồn:** https://ffmpeg.org/
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### 6. `seedvr2` — SeedVR2
- **Loại:** post · `ga` · mã nguồn mở (ByteDance Seed)
- **Truy cập:** open-weights, api-aggregator
- **Năng lực:** `post.upscale`
- **Điểm mạnh:** siêu phân giải video khuếch tán một bước; phù hợp để phóng bản nháp 480p lên 1080p.
- **Giấy phép:** commercial: conditional — theo giấy phép kho mã.
- **Nguồn:** https://upsampler.com/blog/seedvr-vs-flashvsr-ai-video-super-resolution-2026
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 7. `flashvsr` — FlashVSR
- **Loại:** post · `ga` · học thuật mã nguồn mở
- **Truy cập:** open-weights, api-aggregator
- **Năng lực:** `post.upscale`
- **Điểm mạnh:** siêu phân giải video dạng luồng, hướng tới thời gian thực, tốc độ nhanh.
- **Giấy phép:** commercial: conditional — theo giấy phép kho mã.
- **Nguồn:** https://upsampler.com/blog/seedvr-vs-flashvsr-ai-video-super-resolution-2026
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 8. `topaz-video` — Topaz Video (gồm dòng Starlight)
- **Loại:** post · `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `post.upscale`, `post.frame_interp`
- **Điểm mạnh:** chuẩn thương mại về siêu phân giải, phóng được lên 4K.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://help.scenario.com/articles/2511466273-upscale-your-videos-up-to-4k-with-topaz
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 9. `real-esrgan` — Real-ESRGAN
- **Loại:** post · `ga` · mã nguồn mở
- **Truy cập:** open-weights
- **Năng lực:** `post.upscale`
- **Điểm mạnh:** nhẹ.
- **Điểm yếu:** video-replicate-studio thử thực tế thấy x4plus có vết ô vuông, không dùng; không khuyến nghị để siêu phân giải video sinh.
- **Giấy phép:** cho phép thương mại (BSD-3-Clause).
- **Nguồn:** https://github.com/derek-zhuolin/video-replicate-studio
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 10. `rife` — RIFE
- **Loại:** post · `ga` · mã nguồn mở
- **Truy cập:** open-weights
- **Năng lực:** `post.frame_interp`
- **Điểm mạnh:** nội suy khung hình thời gian thực; video-replicate-studio đang dùng.
- **Giấy phép:** cho phép thương mại (MIT).
- **Nguồn:** https://github.com/hzwer/ECCV2022-RIFE
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

---

**Ghi chú về số mục:** file nguồn có 10 mục (remotion, motion-canvas, html-gsap-playwright, blender, ffmpeg, seedvr2, flashvsr, topaz-video, real-esrgan, rife). Danh mục trên đánh số đúng theo file; không có mục thứ 11.
