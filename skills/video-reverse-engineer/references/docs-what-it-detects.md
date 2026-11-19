# Có thể phân tích được những gì

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · docs/what-it-detects.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

## Hình ảnh được làm ra như thế nào

Mỗi cảnh được xếp vào một trong 11 loại dưới đây. Cột "Công cụ đo được" nghĩa là: không cần xem ảnh, chỉ bằng xử lý offline vẫn phán được; các loại còn lại phải nhờ mô hình xem ảnh (VLM) hoặc agent xem ảnh.

| Loại | Ví dụ thường gặp | Công cụ đo được | Số video đánh giá |
|---|---|---|---|
| Quay thật | Nói trước camera, vlog, bán hàng livestream, review địa điểm | ✓ | 5 |
| Video do AI tạo | Văn bản / ảnh sinh video, phim ngắn AI | ✓ | 24 |
| Người ảo | Một ảnh chân dung được giọng nói điều khiển để nói | Một phần | 0 |
| Render 3D | Khoa học phổ thông bằng Blender / C4D, hoạt hình sản phẩm | ✓ | 14 |
| Hoạt hình 2D | Vẽ tay, Live2D, hoạt hình nhân vật AE | ✗ cần xem ảnh | 0 |
| Stop-motion | Đất sét, nỉ, rối giấy quay từng khung | ✗ cần xem ảnh | 0 |
| Đoạn phim điện ảnh/truyền hình | Phim ảnh được cắt vào video thuyết minh phim, video cắt ghép (mashup), tổng hợp cảnh nổi tiếng | ✗ cần xem ảnh (công cụ chỉ cho manh mối) | 8 |
| Code / template | Hiệu ứng chữ, UI, biểu đồ, thẻ kiểu slide PPT | ✓ | 16 |
| Quay màn hình / ảnh chụp | Thao tác phần mềm, trang web | ✓ | 11 |
| Ảnh tĩnh pan/zoom | Một ảnh được phóng/dịch chuyển | ✓ | 3 |
| Khung tĩnh | Ảnh hoặc thẻ đứng yên | ✓ | 5 |

Trên cùng một cảnh còn được đánh dấu riêng:

- Lớp chồng hậu kỳ: phụ đề, chữ nhấn, tiêu đề, sticker, template bố cục. Chữ nằm trên vật thể (bao bì, biển hiệu) sẽ cố gắng tách khỏi phụ đề. Chi tiết xem phần "Lớp đồ họa hậu kỳ" bên dưới.
- Tư liệu thật: màn hình quay, ảnh chụp, ảnh, đoạn video được nhúng trong hình; khi phục dựng phải dùng file gốc. Sản phẩm, logo, nhân vật trong hình AI được liệt kê làm ảnh tham chiếu khi phục dựng.
- Xử lý AI trên cảnh quay thật (xem ảnh để suy ra): đổi mặt, đổi khẩu hình, vẽ lại theo phong cách, thay trang phục bằng AI, tách nền thay nền, thêm/xóa vật thể, làm đẹp. Phương án phục dựng sẽ ghi "quay trước, sau khi quay thì xử lý AI bước nào, dùng model nào".

## Cảnh quay thật được quay như thế nào

| Khía cạnh | Tách ra những gì |
|---|---|
| Khung hình | Cỡ cảnh (từ toàn cảnh đến cận cảnh đặc tả), độ cao máy, bố cục |
| Chuyển động máy | Cầm tay / gimbal / chân máy, đẩy kéo lia, máy điện thoại hay máy ảnh, quay chậm / timelapse / đổi tốc độ |
| Ánh sáng | Đèn chính từ phía nào, cao bao nhiêu; tỉ lệ sáng; ánh mềm hay cứng; nhiệt màu; xóa phông; đèn viền, phản quang trong mắt, đèn nhìn thấy trong hình |
| Sơ đồ ánh sáng | 12 kiểu, kèm danh sách thiết bị: ánh mềm trực diện, đèn chính + đèn phụ, ánh cứng một bên, ngược sáng, ánh môi trường ban đêm, low-key, high-key, ánh màu không khí (RGB / neon), tĩnh vật sản phẩm, nắng trực tiếp ngoài trời, trời âm u ngoài trời, ngược sáng ngoài trời |
| Màu | Phong cách (tự nhiên, cam-xanh, Nhật, film, đen trắng, tông tối, bão hòa cao) và độ bão hòa, tương phản, mức đen, nóng-lạnh |
| Dựng | Nhịp, jump cut, cắt đẩy gần, tỉ lệ cảnh chèn, có cắt theo nhịp nhạc hay không |
| Hình thức | Nói trước camera, quay trên mặt bàn, cầm tay giới thiệu hàng, vlog |

Tỉ lệ sáng, mức mềm/cứng, nhiệt màu, màu sắc đo từ điểm ảnh; nguồn sáng là gì, có đèn viền không, có ngoài trời không, tốc độ quay thì bổ sung bằng xem ảnh. Kết quả hai bên được liệt kê song song trong báo cáo.

## Lớp đồ họa hậu kỳ

Toàn bộ video được phân tích theo một timeline, không cắt theo cảnh (một câu phụ đề, một sticker thường vắt qua nhiều điểm cắt).

| Mục | Đo bằng cách nào | Kết quả |
|---|---|---|
| Timeline phụ đề | OCR 2 khung/giây, theo dõi từng câu chữ ở cùng vị trí, rồi căn đầu/cuối với khung mức xám 10 khung/giây đến khoảng 0.1 giây; phụ đề hai dòng được gộp thành một câu | `packaging/subtitles.srt` |
| Kiểu chữ | Đo từ điểm ảnh: màu chữ, màu và độ dày viền, màu khung nền, gradient, từ khóa màu khác (thấy được khi nói tới thì đổi màu), cỡ chữ, nghiêng, độ dày | Cột kiểu trong báo cáo |
| Phân loại chữ | Phụ đề (cùng vị trí liên tục đổi câu), chữ nhấn (cỡ to / màu / nghiêng / viền dày / nhiều màu / bật lên, ít nhất hai mục), tiêu đề (thường trực ở trên cùng), chú thích (thẻ chương, nhãn bám theo vật thể), chữ trong hình | Loại của từng dòng chữ |
| Vào / ra | Xuất hiện thẳng, phóng to bật ra, mờ dần, trượt vào, hiện từng chữ; trong câu có nảy hoặc đổi màu không | Báo cáo, hoạt ảnh trong ASS |
| Sticker / GIF / PiP | Một khối không đổi vị trí trên nền đang chuyển động, có biên rõ; khi chuyển cảnh thì nền đổi hết còn khối này không đổi; khối xuất hiện rồi biến mất giữa cảnh (trên cảnh quay thật chỉ đánh dấu "nghi ngờ"); bên trong chuyển động và có chu kỳ cố định thì là GIF lặp | Thời gian, vị trí, ảnh chụp (`packaging/sticker_XX.jpg`). Thực tế bắt được khoảng một nửa, phần còn lại bổ sung bằng xem ảnh |
| Căn hiệu ứng âm thanh | Mỗi hiệu ứng được căn với sự kiện hình gần nhất (phụ đề / chữ nhấn / sticker xuất hiện, điểm cắt, sai số ±0.2 giây); khi không bật VLM, tìm thêm transient âm thanh tại thời điểm chữ nhấn và sticker xuất hiện làm ứng viên độ tin cậy thấp | Cột "Đối ứng hình" trong bảng hiệu ứng âm thanh |

Ngoài ra xuất `packaging/overlays.ass` (có màu, viền, vị trí, hoạt ảnh bật lên; có thể nén trực tiếp bằng `ffmpeg -vf ass=`, nhưng phải đổi font sang font của video gốc) và `packaging/timeline.json`.

Font là gì, sticker có nội dung gì, phép đo điểm ảnh không xác định được; cần VLM hoặc agent xem ảnh để bổ sung. Trong các cảnh 3D, hoạt hình, có bố cục, vật thể vốn đã xuất hiện đột ngột, nên trên các cảnh này chỉ tính sticker vắt qua điểm cắt hoặc lặp vòng; các mục còn lại ghi là "nội dung hình" và xem lại bằng hình nếu cần. Kết quả đánh giá xem [eval/RESULTS.md](../eval/RESULTS.md).

## Âm thanh

- Giọng người: người thật hay lồng tiếng AI, nội dung lời thoại.
- Nhạc nền: BPM, tông, các đoạn, là AI sinh hay lấy từ thư viện nhạc.
- Hiệu ứng: thời điểm của từng hiệu ứng, loại, và nó rơi vào sự kiện hình nào (phụ đề / chữ nhấn / sticker xuất hiện, điểm cắt).
