# Vẽ nét SVG bằng GSAP core

`VE-gsap-core-draw` vẽ dần một đường SVG với GSAP core 3.15.0, không cần plugin DrawSVG. Cấp GSAP cục bộ theo hash bằng `--gsap-file`; không chép thư viện vào repo hoặc dùng CDN.

Mã recipe do dự án tự viết và thuộc giấy phép MIT của repo. GSAP là thư viện riêng, có điều khoản riêng; MIT của recipe không áp dụng cho GSAP và không khẳng định quyền phân phối GSAP.

Tạo path có `pathLength="1"` và stroke, rồi nạp `core-draw.js` sau GSAP. Tạo timeline `paused`, gọi `addCoreDraw(timeline, path, {duration: 2})` và đăng ký timeline với HyperFrames. Nếu bộ kiểm HTML không nhận thuộc tính `pathLength`, đặt thuộc tính bằng `path.setAttribute('pathLength', '1')` trước khi gọi recipe.

Recipe sử dụng `fromTo`, tắt làm tròn pixel, không dựa vào thứ tự tua. Test trình duyệt kiểm năm mốc theo ba thứ tự; cần truyền đường GSAP đã có sẵn qua `GSAP_TEST_FILE` khi chạy `python -m pytest tests/test_gsap_core_draw_seek.py -q`. Thiếu biến thì test bỏ qua, không tính đạt. Chưa kiểm các hình nhiều path hoặc độ tương thích giữa trình duyệt và hệ điều hành.
