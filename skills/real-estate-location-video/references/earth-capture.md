# Quay Google Earth tự động (đã kiểm 19/11/2026)

Script: `assets/earth_run.mjs <job.json>` (puppeteer-core + Chrome headless). Mẫu job: `assets/earth_job.example.json`.

## 1. URL và tham số camera

```
https://earth.google.com/web/@<lat>,<lng>,<alt>a,<dist>d,<fov>y,<heading>h,<tilt>t,<roll>r
https://earth.google.com/web/search/<từ+khoá>/@…        # tìm địa điểm, Earth tự giải toạ độ
```
`a` độ cao điểm nhìn (Earth tự chỉnh theo địa hình) · `d` khoảng cách camera tới điểm · `y` FOV dọc (dùng 35) · `h` hướng (độ, 0 = Bắc) · `t` nghiêng (0 = nhìn thẳng xuống) · `r` xoay (0).
Camera đặt được bằng URL ⇒ **bậc thang x4→x1** = 4 URL cùng tâm, `d` = 4·D, 3·D, 2·D, D (D = khoảng cách dự án vừa khung dọc, ≈ 980 m ở dự án mẫu).

## 2. Khung dọc và cắt giao diện

- Quay ở viewport **1080×2150** rồi cắt `{x:0, y:90, width:1080, height:1920}`: bỏ thanh công cụ trên (90 px), phần dưới có thanh trạng thái/nút điều khiển nằm ngoài. Quay thẳng 1080×1920 vẫn chạy nhưng giao diện đè lên ảnh.
- Quay ngang rồi cắt dọc **không đủ phân giải** (1280×720 → 405×720). Luôn quay dọc.

## 3. Phiên quay và cài đặt nền

Một phiên Chrome: mở URL đầu, chờ 18 s (ô ảnh 3D nạp), `Escape`, bấm **Dismiss** hai thẻ mẹo ((637,183) «Access the data catalog…» và (45,148) «Find and manage…» trong khung 1080×2150), rồi đặt nền:

| Việc | Toạ độ (khung 1080×2150) |
|---|---|
| Mở **Basemap settings** (ô bản đồ nhỏ góc dưới-trái) | (47, 2073) |
| Type: Satellite / Map | (100, 800) / (100, 863) |
| Details: Clean / Exploration / Everything | (288, 984) / (288, 1064) / (288, 1144) |
| Đóng bảng (X) | (296, 720) |

Cài đặt nền **lưu qua các lần tải lại** trong cùng phiên → đặt một lần rồi `page.goto` các URL. Dùng **Clean** để không có nhãn của Earth (nhường chỗ cho tag của mình). Toạ độ trên là của giao diện bản 19/11/2026: nếu Earth đổi giao diện, chụp màn hình và đo lại.

## 4. Chuyển động liên tục (screencast)

`page.screencast({path, crop, speed:1})` (30 fps, 1080×1920), thao tác trong lúc quay:

| Chuyển động | Thao tác | Đo được |
|---|---|---|
| Dolly | `mouse.wheel({deltaY})` lặp, cách 90–120 ms | 14 nấc `−120` kéo `d` 900 → 78 m (quá mạnh); 9 nấc `+120` lùi ra ≈ ×2,5 |
| Lia | kéo chuột **trái** từ giữa khung | kéo xuống = đi về Bắc |
| Xoay hướng | kéo chuột **phải** ngang | 200 px ≈ 63° (40° → 103°) |
| Lao xuống từ vùng | URL xa (`d` 120000) rồi 24 nấc `−120`, cách 110 ms | ≈ 9 s |

Sau khi quay: `ffmpeg -i clip.mp4 -c copy fix.mp4` (puppeteer thiếu duration), rồi cắt/đổi tốc độ khớp độ dài cảnh bằng `setpts=(PTS-STARTPTS)*k,fps=30`.

## 5. Bẫy đã gặp

| Bẫy | Cách xử lý |
|---|---|
| Nghiêng ≥ 75° gần mặt đất (`300d,75t`) ảnh vỡ | dùng ≤ 70° và `d` ≥ 400 m (`400d,70t`) |
| Shot chưa nạp xong (R19 ¾ ảnh mờ) | tăng `wait` lên 20–25 s với vùng xa/ít ảnh |
| Thẻ mẹo che góc trên | Dismiss hai thẻ ở shot đầu; thẻ chỉ hiện lần đầu mỗi phiên |
| Nhãn Earth lọt vào ảnh (Exploration) | chọn **Clean** |
| Kiểu **Map + 3D buildings** thiếu toà mới (dự án mẫu) | dùng hiệu ứng 3D MapLibre/OSM (`effects-recipes.md` mục B) |
| Cây a11y của Earth gần như rỗng; không bấm theo `uid` được | bấm theo **toạ độ** (`page.mouse.click`) |
| Trình chụp của công cụ chỉ ghi vào thư mục phiên | script tự ghi ra thư mục project (không qua công cụ chụp) |
| Nhiều cảnh trùng hướng 40° nhìn như lặp | đổi `h` (270 nhìn Tây, 220 nhìn qua hồ) giữa các cảnh |

## 6. Điều chưa kiểm

Quay trên macOS; nhiều viewport khác; số lần thử tải lại khi mạng chậm; kéo chuột đúng một góc nghiêng định trước (chỉ biết xoay hướng); bay liên tục giữa hai toạ độ xa không qua URL.
