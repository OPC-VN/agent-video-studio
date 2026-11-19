# Cài đặt và nguồn lấy (đã chạy thật 19/11/2026)

Mục tiêu: máy mới làm theo file này là chạy lại được quy trình mà **không phải đoán**. Mọi phiên bản bên dưới là bản đã dùng và kiểm; nâng bản là việc có chủ đích (chạy lại bước kiểm cuối file).

## 1. Công cụ cần có

| Thành phần | Bản đã dùng | Lấy ở đâu / cài thế nào | Dùng cho |
|---|---|---|---|
| Node.js | 24.12 (cần ≥ 22) | https://nodejs.org (hoặc trình quản lý gói của máy) | chạy các script `.mjs` |
| ffmpeg + ffprobe | 9.0.2 | Windows: `winget install Gyan.FFmpeg`; macOS: `brew install ffmpeg` | ghép khung → clip, nén bản xem |
| Python | ≥ 3.10 (đã dùng 3.12) | https://www.python.org | `geo_cfg.py`, `osm_overlay.py`, `build_composition` |
| Pillow | 12.2.0 | `pip install "Pillow>=10"` | đổi PNG → JPG khi dựng composition |
| HyperFrames (qua `video-studio`) | ghim ở `upstream.json` / `doctor` | `video-studio doctor` chỉ phần thiếu; **không** dùng bản trôi (không ghim) của HyperFrames | `check --strict`, `render` |
| Chrome for Testing | 146.0.7680.153 | cài sẵn khi HyperFrames chạy lần đầu, nằm ở `~/.cache/puppeteer/chrome/<bản>/`; hoặc `npx puppeteer browsers install chrome@146.0.7680.153` | quay Google Earth, MapLibre (headless) |
| puppeteer-core | 25.13.0 | `npm install puppeteer-core@25.13.0` trong thư mục `tools/` của project; hoặc dùng bản trong cache `npx` của HyperFrames | điều khiển Chrome, screenshot, screencast |

Biến môi trường (tuỳ chọn, script tự tìm nếu không đặt):

```
CHROME_BIN=<đường tới chrome(.exe)>
PUPPETEER_CORE_DIR=<thư mục puppeteer-core>
```

## 2. Dịch vụ bản đồ (tải từ mạng lúc quay; không cần khoá)

| Nguồn | URL / cách gọi | Ghi chú và điều khoản |
|---|---|---|
| Google Earth web | `https://earth.google.com/web/@<lat>,<lng>,<alt>a,<dist>d,35y,<heading>h,<tilt>t,0r` và `/web/search/<từ khoá>/@…` | xem không cần đăng nhập. Điều khoản Google cấm dùng ảnh Earth cho quảng cáo/quảng bá; người dùng đã quyết bỏ ghi nguồn và nhận rủi ro. **Ghi quyết định đó vào hồ sơ dự án.** |
| MapLibre GL JS | `https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js` (+ `.css`) | ghim 4.7.1. Offline: `npm pack maplibre-gl@4.7.1` rồi phục vụ cục bộ |
| OpenFreeMap (vector OSM) | style `https://tiles.openfreemap.org/styles/liberty`; nguồn `openmaptiles` | miễn phí, không khoá. Cần ghi nguồn: «OpenFreeMap · © OpenMapTiles · dữ liệu © OpenStreetMap contributors». **Điều khoản dùng thương mại chưa đọc lại: kiểm trước khi phát hành.** |
| Esri World Imagery | `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`, `maxzoom` 19 | không khoá. Điều khoản video thương mại **chưa kiểm**; ảnh có thể **cũ hơn** dữ liệu OSM (ở dự án mẫu: ảnh còn là ruộng, OSM đã có các tháp). |
| GSAP | `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js` | ghim 3.14.2, cùng bản với `templates/_seed` |

Không dùng: `tile.openstreetmap.org` và Nominatim (bị chặn/quá tải ở môi trường đã thử); tra toạ độ bằng trang Google Maps của địa điểm (`…!3d<lat>!4d<lng>` trong URL) hoặc Photon.

## 3. Nơi để script

```
<project>/tools/   ← chép từ skills/real-estate-location-video/assets/
   _paths.mjs  earth_run.mjs  maplibre_shots.mjs  three_d_capture.mjs  extract_osm.mjs  geo-capture.html
   osm_overlay.py  build_composition.example.py  earth_job.example.json
```
`osm_overlay.py` tự tìm `geo_cfg.py` của skill `land-plot-map-video` (cùng repo); nếu chép ra ngoài repo thì đặt `GEO_CFG_PATH`.
Trạm và project theo `video-routing`: file dữ liệu riêng (KML, JSON toạ độ, shot raw) ở trạm, **không** commit.

## 4. Kiểm sau khi cài (làm theo thứ tự)

```bash
node --version && ffmpeg -version | head -1 && python -c "import PIL; print(PIL.__version__)"
node --check tools/earth_run.mjs                       # cú pháp
node -e "import('./tools/_paths.mjs').then(m=>console.log(m.chromePath()))"    # tìm được Chrome
node -e "import('./tools/_paths.mjs').then(m=>console.log(!!m.loadPuppeteer()))"   # tìm được puppeteer-core
node tools/maplibre_shots.mjs raw/maplibre             # 7 ảnh M01–M07 (cần mạng tới Esri/OpenFreeMap)
```
Một shot Earth thử: tạo job 1 shot `kind:"still"` từ `earth_job.example.json`, chạy `node tools/earth_run.mjs job.json`, mở ảnh: phải thấy ảnh 3D nghiêng **không** có thanh công cụ, thẻ mẹo hay nhãn.

## 5. Nâng bản / thay nguồn

Đổi một thành phần → chạy lại bước 4 và một shot mẫu cho từng script, so ảnh với bản cũ. Cập nhật bảng ở đầu file này cùng `docs/CHANGELOG.md`.
