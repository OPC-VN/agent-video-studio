# Quy tắc review bằng cách xem ảnh

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/review.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Bổ sung cho quy trình ở mục 1 của SKILL.md: cách hợp nhất kết quả xem ảnh với kết quả của công cụ, và mấy loại trường hợp dễ phán sai.

## Quy tắc hợp nhất

Rút ra từ thực nghiệm (repo `eval/RESULTS.md`):

- Khi chỉ có một nguồn xem ảnh (chỉ VLM hoặc chỉ bạn), kết quả xem ảnh chỉ được chọn trong hai ứng viên đứng đầu của công cụ. Khi công cụ đã chắc về "AI / quay thật / người ảo" thì không đổi; cảnh đã qua chuyển mã mà có khung lặp 24→30 sẽ không bị đổi thành quay thật chỉ vì "trông như thật". Khi bản thân cảnh không có khung lặp (nhịp 30fps gốc), nhận định quay thật của bạn được chấp nhận, kể cả khi cả video không được gắn nhãn 30fps gốc vì có lẫn đoạn mở đầu AI; khi ba ứng viên đứng đầu của công cụ đều dưới 0.4 và loại bạn chọn chỉ kém lựa chọn thứ hai một chút, thì cũng lấy theo bạn. Kết quả xem ảnh hữu ích nhất khi phân biệt 3D / hoạt ảnh code / quay màn hình. Hoạt hình 2D, stop-motion và đoạn phim điện ảnh/truyền hình là ngoại lệ: công cụ không đo được ba loại này, nên khi bạn phán là chúng thì chấp nhận ngay; nhưng nếu chỉ một bên xem ảnh thì kết luận vẫn giữ "chờ xác nhận".
- VLM và bạn đều trả lời: phán nhóm lớn trước (sinh / render / quay thật / quay màn hình / ảnh tĩnh), rồi mới phán loại con. Chỉ cần lựa chọn đầu của công cụ được một trong hai bên ủng hộ (cùng loại con hoặc cùng nhóm lớn, ví dụ công cụ phán video AI, bạn phán người ảo) thì theo nhóm lớn của lựa chọn đầu ấy; khi cả hai cùng phản đối công cụ thì hợp nhất theo cách thông thường.
- Cảnh được đánh dấu "có bất đồng" (công cụ và VLM trái ý nhau về việc có phải quay thật không) bắt buộc xem: đối chiếu xem bằng chứng VLM viết có thực sự thấy được trong ảnh chụp không, vì VLM có thể bịa lý do.
- Cảnh có ghi trong `review_tasks.json` rằng "người dùng đã sửa nhãn X thành Y n lần" là loại mà người dùng đã sửa đi sửa lại, cần xem đặc biệt kỹ.

## Quy tắc khi không xem được ảnh (quan trọng)

Trước hết xác định bạn có tự xem được ảnh hay không (có đọc được `storyboard.jpg`, `shots/*.jpg` và mô tả nội dung khung hình không). **Khi không xem được ảnh và cũng không bật VLM:**

- **Không lật lại nhận định của công cụ về cách làm** (quay thật / AI / 3D / code / quay màn hình). Các thống kê điểm ảnh (số màu, mảng phẳng, nhiễu) chính là bằng chứng công cụ đã dùng; bạn dùng lại thì chỉ ra kết luận tương tự hoặc tệ hơn. Thực tế: một agent không xem được ảnh đã phán một bức phác họa bút chì do AI tạo là "thẻ bố cục nền trắng", và một chi tiết 3D có chất kính bị phán là "giao diện code".
- Những gì bạn làm được và nên làm: đối chiếu timeline và điểm cắt; đọc track chữ OCR để loại trừ đọc nhầm; dùng mức âm lượng của `stems/` để xem có giọng người hay không; đọc metadata (dấu AIGC, dấu transcode của nền tảng); liệt kê các cảnh công cụ có độ tin cậy thấp vào mục "điểm chưa chắc".
- Trong kết luận một câu, ghi rõ "chưa bật VLM, chưa xem khung hình", và giữ nguyên các cảnh công cụ đánh dấu "quay thật hay AI, chờ xác nhận".

## Video gốc / video tham chiếu: nêu bằng chứng phản đối trước khi kết luận AI

Video chỉ có một cảnh liền mạch, không có nhãn AIGC, không có khung lặp 24→30, lại mang chất tả thực hoặc thủ công (stop-motion, video đời sống quay từ trên xuống, cảnh mô hình thu nhỏ làm tay) thường bị công cụ phán là AI. Sau khi xem ảnh, nếu không tìm thấy sơ hở AI rõ ràng (biến dạng, texture nhấp nháy, sai vật lý, chữ loạn), **không được cho độ tin cậy cao**: ghi là "AI hay quay thật / stop-motion chờ xác nhận (nghiêng về X)", liệt kê bằng chứng của cả hai phía, và độ tin cậy không quá 0.7.

## Video thuyết minh phim, video cắt ghép: trước hết phán xem có phải đoạn phim được cắt ghép vào không

Khi khung hình nằm lọt trong viền đen, công cụ sẽ ghi "manh mối đoạn phim" trong phần bằng chứng, và gắn cảnh là "video AI hay đoạn phim chờ xác nhận" hoặc "quay thật hay đoạn phim chờ xác nhận". Công cụ không đo được ai là người quay, nên bước này bạn phải xem ảnh:

- Nhận ra diễn viên hoặc bộ phim, ánh sáng và bối cảnh cỡ đoàn phim, diễn viên quần chúng, logo kênh hoặc watermark nền tảng, chữ trong bối cảnh đọc rõ → `film_footage`.
- Khuôn mặt quá hoàn hảo, các nhân vật khác nhau trông rất giống nhau, tay và chữ bị lỗi, texture trôi → `ai_video` (bố cục của video thuyết minh phim ngắn tập AI giống hệt video thuyết minh phim người đóng, đừng chỉ nhìn bố cục).
- Cảnh tác giả tự lên hình nói trước camera, ảnh chụp màn hình hoặc hình AI được chèn vào: gắn nhãn riêng theo từng cảnh.
- `live_action` chỉ dành cho hình ảnh do chính tác giả hoặc khách hàng quay.

## Video đã qua transcode của nền tảng (tải từ WeChat / Douyin / TikTok)

Khi metadata có `Tencent CAPD MTS`, `Wxmm_`, `vid:v…`, công cụ đánh dấu `video_context.transcoded`. Nén lần hai làm mất nhiễu cảm biến và tạo nhịp khung giả, vì vậy:

- Các bằng chứng dựa vào nhiễu không còn hiệu lực; "không có nhiễu" không còn cho thấy là AI. Công cụ sẽ đánh dấu các cảnh này là "quay thật hay AI, chờ xác nhận".
- Bằng chứng vẫn đáng tin: khung lặp 24→30 (mô hình sinh thường xuất 24fps; cả video 30fps gốc, không có khung lặp thì giống điện thoại quay trực tiếp hơn), dấu nhận diện ẩn AIGC, nội dung hình ảnh (tay thật, môi trường thật, vật lý có tự nhiên không; mục này phải xem ảnh hoặc bật VLM).
- Thứ tự ưu tiên khi bằng chứng mâu thuẫn: **khung lặp 24→30 đều đặn + dấu AIGC ẩn** cùng có thì nặng ký hơn việc "xem ảnh không thấy dấu hiệu AI", không được vì thế mà đổi cảnh thành quay thật; tối đa ghi "nghiêng về AI, quay thật chờ xác nhận". Ngược lại, cả video 30fps gốc, không có khung lặp, không có dấu AIGC, cộng với ảnh xem ra bình thường, mới được kết luận quay thật.
- File đã nén lại và bị xóa dấu nền tảng (công cụ tải về đã bỏ metadata, các mẫu trong `docs/cases/videos/` của repo) không bị đánh dấu là transcode, nhưng vẫn có nhịp khung giả. Với cảnh chỉ có "độ nét dao động theo chu kỳ" mà không có khung lặp, công cụ sẽ đánh dấu "AI hay quay thật chờ xác nhận", và kết luận từ việc xem ảnh được phép đổi phán quyết trực tiếp.
