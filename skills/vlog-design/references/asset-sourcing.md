# Nguồn tài nguyên: icon, hình người, ảnh, font, màu, motion

> **Kết luận:** lấy theo thứ tự **thư viện có sẵn trong trạm → thư viện mở giấy phép rõ → tự vẽ SVG/CSS → tạo ảnh bằng AI**. Mỗi tài nguyên ghi vào manifest với nguồn, giấy phép, người tạo. Giấy phép ở bảng dưới là ghi chép lúc soạn; **mở trang giấy phép kiểm lại trước khi phát hành** (link không cấp quyền).

## Contents
- Quy tắc chọn
- Icon
- Hình người và nhân vật
- Ảnh, video nền, âm thanh
- Font có dấu tiếng Việt
- Màu
- Motion và thư viện dựng
- Kiểm trước khi dùng

## Quy tắc chọn

1. **Một họ icon cho cả tập.** Trộn hai họ nét khác nhau là lỗi dễ thấy nhất. Chọn theo nét: viền mảnh (outline) cho nền tối tối giản; khối đặc (filled/duotone) cho hoạt họa kể chuyện.
2. **Nhân vật cùng một phong cách** (cùng độ dày nét, cùng bảng màu da/áo). Không trộn người vẽ phẳng với ảnh thật trong cùng khung, trừ khi là cắt dán có chủ đích.
3. **Không lấy hình từ video mẫu.** Chỉ học loại vật và ẩn dụ, tự vẽ hoặc lấy nguồn mở.
4. **Ảnh AI** (cầu tạo ảnh của trạm) chỉ khi không có nguồn mở phù hợp; prompt phải khoá phong cách (màu, nét, góc nhìn, nền) giống cả bộ; ghi prompt và seed vào manifest.
5. Thương hiệu, logo thật của bên thứ ba: chỉ khi nội dung nói về chính sản phẩm đó và theo hướng dẫn dùng logo của họ.

## Icon

| Thư viện | Phong cách | Giấy phép (kiểm lại) | Hợp với |
|---|---|---|---|
| Lucide | viền 2px bo tròn | ISC | bảng tối, UI mock, sơ đồ luồng |
| Tabler Icons | viền 2px, rất nhiều mẫu | MIT | sơ đồ kỹ thuật, nhãn công cụ |
| Phosphor | 6 độ nét (thin → fill, duotone) | MIT | cần cả viền lẫn đặc cùng họ |
| Iconoir | viền mảnh thanh lịch | MIT | phong cách tối giản |
| Heroicons | outline / solid | MIT | giao diện web mock |
| Material Symbols | biến thể nét/độ đặc | Apache-2.0 | giao diện kiểu Google |
| Fluent Emoji (3D, flat) | emoji 3D bóng | MIT | điểm nhấn cảm xúc, hoạt họa vui |
| Noto Emoji | emoji phẳng | Apache-2.0 / OFL | nhãn nhanh |
| OpenMoji | emoji nét viền | CC BY-SA 4.0 (ghi công, chia sẻ tương tự) | chỉ khi chấp nhận điều kiện |
| Simple Icons | logo thương hiệu (SVG) | CC0 cho SVG; logo vẫn thuộc chủ | nhắc tên công cụ thật |

## Hình người và nhân vật

| Nguồn | Mô tả | Giấy phép (kiểm lại) |
|---|---|---|
| Open Peeps | người vẽ tay ghép thân/mặt | CC0 |
| Humaaans | người phẳng ghép tư thế | xem trang (miễn phí thương mại lúc soạn) |
| unDraw | minh hoạ phẳng đổi màu chủ đạo | giấy phép riêng unDraw, miễn phí thương mại, không ghi công |
| Storyset | minh hoạ có sẵn hoạt hoạ | cần ghi công bản miễn phí |
| Tự vẽ SVG | người dạng khối (đầu tròn + thân bo) như video mẫu tối giản | của mình |

Mẹo: hình người tối giản (đầu tròn + vai bo, một màu) đủ cho đa số ẩn dụ «người dùng / khách hàng / đội ngũ» và dễ làm chuyển động hơn minh hoạ chi tiết.

## Ảnh, video nền, âm thanh

| Nguồn | Loại | Giấy phép (kiểm lại) |
|---|---|---|
| Pexels | ảnh, video | Pexels License (dùng tự do, không bán lại nguyên bản) |
| Unsplash | ảnh | Unsplash License |
| Pixabay | ảnh, video, nhạc, SFX | Pixabay Content License |
| Mixkit | video, nhạc, SFX | Mixkit License (xem từng loại) |
| Freesound | SFX | theo từng file: CC0 / CC BY / CC BY-NC |
| YouTube Audio Library | nhạc, SFX | theo từng bài |

## Font có dấu tiếng Việt

| Vai trò | Gợi ý (Google Fonts, OFL) | Ghi chú |
|---|---|---|
| Tiêu đề không chân | Be Vietnam Pro, Inter, Montserrat, Lexend | đủ dấu, nhiều độ đậm |
| Thân, phụ đề | Inter, Be Vietnam Pro, Noto Sans | đọc tốt cỡ nhỏ |
| Có chân / nghiêng nhấn | Playfair Display, Lora, Noto Serif | phụ đề nghiêng kiểu tạp chí |
| Số lớn, đồng hồ | Space Grotesk, JetBrains Mono, Bebas Neue (kiểm dấu) | số đếm, thẻ chương |
| Viết tay | Patrick Hand, Pangolin, Itim, Mali | **bắt buộc kiểm glyph** trước khi dùng |
| Mã, terminal | JetBrains Mono, Fira Code | UI mock, dòng lệnh |

Font hệ điều hành (ví dụ font cài sẵn của Windows) chỉ dùng dựng nội bộ; video đăng công khai dùng font có giấy phép mở hoặc đã mua.

## Màu

- Lấy màu nhận diện của kênh làm **một màu nhấn chính + một màu nhấn phụ**; mọi thứ còn lại là thang xám nền.
- Video mẫu dùng ba hệ: **nền tối gần đen + một màu nhấn cam/đỏ** (tối giản), **nền kem + chữ đen + cam đất** (người + slide), **cảnh vẽ ấm, ánh đèn vàng** (kể chuyện). Chọn một hệ chủ đạo, hệ thứ hai chỉ cho đổi không khí (thẻ chương, đoạn lùi thời gian).
- Kiểm tương phản chữ/nền ≥ 4.5:1 cho chữ thân, ≥ 3:1 cho tiêu đề lớn.
- Công cụ: Coolors, Realtime Colors, Adobe Color (kiểm tương phản).

## Motion và thư viện dựng

| Thư viện | Dùng cho | Giấy phép (kiểm lại) |
|---|---|---|
| GSAP (+ SplitText, DrawSVG, MorphSVG, Flip) | timeline chính trong HyperFrames | GSAP Standard License, miễn phí cả plugin |
| Rough.js | nét phác tay, khung vẽ tay | MIT |
| Lottie (lottie-web) + LottieFiles | icon động có sẵn | MIT (player); từng file theo LottieFiles license |
| Anime.js | chuyển động nhẹ, đơn giản | MIT |
| CSS keyframes / SVG SMIL | hiệu ứng lặp nền | — |
| Remotion | chỉ tham khảo ý tưởng hiệu ứng | giấy phép riêng, giới hạn công ty |

Danh mục motion đã có trong trạm: skill `video-theme-library` (tra theo vai trò cảnh) và skill `hyperframes` (luật viết composition).

## Kiểm trước khi dùng

- Font: dựng một khung thử chứa «Ả Ẫ Ặ Ể Ỗ Ợ Ữ ỹ đ Đ» ở mọi độ đậm sẽ dùng; thấy ô vuông hay dấu lệch là bỏ.
- Icon: cùng `stroke-width`, cùng `viewBox`, cùng màu qua `currentColor`.
- Manifest: mỗi dòng có `id`, `loại`, `nguồn` (URL hoặc «tự vẽ» hoặc «AI: prompt+seed»), `giấy phép`, `dùng ở cảnh`, `trạng thái` (có sẵn / cần tải / cần tạo / cần người duyệt).
