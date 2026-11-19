# Hiệu ứng ↔ mã trong template ↔ chỗ tra thêm

Mọi hiệu ứng là GSAP trên **một** timeline `master` (`paused`), tua được; helper nằm đầu
`assets/land-plot-template/index.html`. Muốn biến thể: tra thư viện trước, sáng tác sau
(`video-theme-library`), rồi **chuyển thành thời gian composition xác định** (không chuột/cuộn/đồng hồ).

| Hiệu ứng thấy trong mẫu | Cách làm trong template | Chỉnh ở đâu | Tra biến thể |
|---|---|---|---|
| Zoom-blur lao vào / chuyển tầng | `blurIn(cam, t, dur, fromScale, blur)`: `scale` lớn + `filter: blur()` về 1 / 0 | tham số 3 số cuối; mỗi scene tự gọi | `motion_find.py --role transition --ratio 9:16` |
| Pan nhòe rồi nét | `fromTo` x/y/scale/blur trên `-cam` | scene `intro` | `--q "pan"` |
| Đa giác phát sáng (viền neon + fill mờ) | `glowPoly` = polygon fill + hai viền (một blur) dùng `pathLength=1` | màu stroke/fill, độ dày `w` | `--technique ui` |
| Viền vẽ dần | `showPoly`/`drawStroke`: `stroke-dashoffset` 1→0 | `dur` | `--technique path` |
| Chữ gõ ký tự + từ khoá đổi màu | `typed` tách `span.ch`; `[từ khoá]` → class `hl`; stagger opacity/y | cỡ chữ (đối số cuối), `per` | `--technique typography` |
| Chữ nghiêng theo hình («XÃ NÀO ?») | `label(..., rot)` + `back.out(2)` pop | `at`, `rot` trong `CFG.where` | — |
| Ghim + vòng sóng | `circle` lặp **hữu hạn** (`repeat: 3`) | số lần lặp | — |
| Camera xoay nhẹ khi cận cảnh | `rotation` + `scale` trên `-cam`, `sine.inOut` | scene `size` | `hyperframes-animation` (camera lướt) |
| Đường nét đứt vẽ dần | `mask` chứa nét đặc có `dashoffset` động, nét đứt vẽ bên dưới mặt nạ | `from/to`, `stroke-dasharray` | `--technique path` |
| Vòng bán kính nở | `scale` 0→1 quanh tâm (`transformOrigin` = toạ độ ghim) | `r` | — |
| Ghim rơi nảy lần lượt | `y: -420 → 0`, `bounce.out`, lệch `i*0.3` s | `pois`, biểu tượng `book/cross/star/dot` | — |
| Người dẫn lao vào / trượt ra | PNG `scale 2.2→1` + blur; ra `x` âm + blur | scene `hook`, `cta` | `--role cta` |

## Bẫy đã gặp khi dựng thử

- **Chữ dài tự xuống dòng** và đè dòng dưới (`content_overlap` của `check`): cỡ 50–60 px, ≤ ~25 ký tự/dòng.
- Hai thuộc tính trên cùng phần tử: đặt trạng thái đầu bằng `fromTo`, **không** bằng CSS `transform`.
- Lớp nhòe/lớn hơn khung báo `container_overflow` (mức `ℹ`, cố ý): đã gắn `data-layout-allow-overflow`.
- `out/` nằm **trong** thư mục project bị từ chối (mã 2): xuất ra thư mục ngoài.
- Template nạp GSAP từ CDN như `templates/_seed`; offline thì chép bản GSAP cục bộ vào `assets/` và đổi thẻ `<script>` (chưa kiểm ở đây).
- Ảnh giữ chỗ trong demo tạo bằng Pillow, **không phải** ảnh vệ tinh: chỉ để duyệt nhịp.
