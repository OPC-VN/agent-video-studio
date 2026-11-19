# Phục dựng theo báo cáo

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · docs/replicate.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Phần "tự phục dựng" trong báo cáo mở đầu bằng việc xác định video này thuộc loại nào (nói trước camera, unboxing / quay trên mặt bàn, vlog, phim thật, phim ngắn AI, quảng cáo sản phẩm AI, MV nhạc AI, người ảo nói trước camera, clip AI ngắn, 3D / hoạt hình, video thuyết minh phim / video cắt ghép (mashup), khoa học phổ thông bằng hiệu ứng, hướng dẫn quay màn hình, video từ ảnh tĩnh pan/zoom, video cắt ghép theo nhịp nhạc, biểu diễn nhảy / hành động), rồi liệt kê các bước theo thứ tự sản xuất của loại video đó. Loại chỉ quyết định có những bước nào và sắp xếp ra sao; nội dung của từng bước đều lấy từ chính video gốc:

- Quay: cỡ cảnh, góc máy, ánh sáng đo được (hướng đèn chính, tỉ lệ sáng, mềm/cứng, nhiệt màu), màu sắc, và cách bố trí ánh sáng suy ra từ phép đo
- Sinh: số đơn vị sinh, gọi model nào bao nhiêu lần, ảnh đầu vào khung đầu và ảnh tham chiếu của từng đơn vị
- Dựng: số cảnh, trung bình bao nhiêu giây một lần cắt, jump cut và cắt đẩy gần, các chuyển cảnh không phải cắt cứng
- Đồ họa hậu kỳ: số câu phụ đề, vị trí, màu, cách vào, file SRT lưu timeline phụ đề
- Âm thanh: nguồn giọng người và nhạc nền, BPM, tông, số lượng hiệu ứng âm thanh
- Bước cuối: ghép các cảnh đã làm trở lại timeline gốc, xuất một clip so sánh đặt cạnh video gốc

Bước nào lần này không đo được thì không viết. Một video thường có nhiều cách làm cùng lúc; khi một loại chiếm tới một phần tư thời lượng, các bước của loại đó cũng được liệt kê. Dưới đây là cách làm cụ thể cho từng loại hình ảnh, cuối cùng agent ghép lại theo timeline gốc.

## Cảnh quay thật: tự quay

1. Báo cáo đưa ra kế hoạch buổi quay: tổng số cảnh, mỗi cảnh có bao nhiêu máy, quay cái nào trước; cỡ cảnh, cầm tay hay chân máy, đèn chính từ đâu, có cần đèn phụ không, và danh sách thiết bị. Các cảnh của cùng một bối cảnh dù trong thành phẩm bị tách ra vẫn được xếp quay chung.
2. Quay xong một buổi, gửi tư liệu cho agent và nói "theo bảng phân cảnh, cắt tư liệu tôi quay vào đúng chỗ". 
3. Agent sẽ cắt từng tư liệu vào đúng vị trí và thời lượng của cảnh tương ứng, ghép lại theo timeline gốc, rồi xuất một clip so sánh đặt cạnh video gốc để bạn xem nhịp có đúng không. Cảnh chưa quay thì dùng video gốc làm chỗ giữ chỗ, nên có thể quay từng buổi và xem ngay.

## Cảnh do AI tạo: giao cho mô hình video

1. Báo cáo đưa ra các đơn vị sinh: cảnh cùng bối cảnh, liền nhau được gộp thành một lần sinh; ghi rõ dùng model nào, cần chuẩn bị ảnh tham chiếu nào (ảnh sản phẩm, ảnh nhân vật), prompt nhiều cảnh (tiếng Trung và tiếng Anh), và lần sinh tiếp theo nối với lần trước như thế nào.
2. Có hai cách làm:
   - Thủ công: dán prompt của đơn vị và ảnh tham chiếu lên trang web như Jimeng, Kling để sinh, rồi gửi video đã sinh cho agent để ghép lại vào timeline gốc.
   - Tự động: nếu đã cài [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema), nói "dùng capsule-cinema để phục dựng cảnh AI", agent sẽ gọi model video để sinh, rồi tự ghép lại và xuất clip so sánh. Gọi model video tốn tiền, nên agent sẽ chạy thử miễn phí trước, sau khi bạn xác nhận mới sinh chính thức.
3. Hiện tại sinh tự động vẫn gọi model một lần cho mỗi cảnh. Báo cáo đã có sẵn prompt để sinh nhiều cảnh trong một lần; cách này tiết kiệm tiền hơn nhưng hiện chỉ đi được theo đường thủ công.

## Cảnh nhảy và động tác: điều khiển bằng video gốc

Các cảnh nhảy, đánh nhau, tập gym mà điểm chính là động tác toàn thân biên độ lớn mới thuộc loại này. Cảnh bán hàng, nói chuyện, hát hay nói liên tục chỉ có chuyển động nhỏ thì không thuộc loại này; cứ đi theo đơn vị sinh bình thường, đổi khẩu hình hoặc người ảo là đủ. Nếu chỉ sinh theo khung đầu–cuối, động tác giữa sẽ do mô hình đoán, dễ mất biên đạo và nhịp, nên báo cáo tách riêng thành "điều khiển bằng động tác", không đưa vào đơn vị sinh.

1. Để agent chạy `rea-video drive <thư mục báo cáo>`: xóa phụ đề và sticker, cắt tại các chỗ động tác dừng hoặc gần điểm nhịp thành các đoạn khoảng 10 giây, mỗi đoạn một video điều khiển.
2. Chuẩn bị một ảnh thiết lập nhân vật (toàn thân chính diện, nghiêng, sau lưng và cận mặt, cùng một bộ trang phục); mỗi đoạn đều dùng ảnh này.
3. Phần lớn trường hợp chỉ cần dùng thẳng video điều khiển làm tham chiếu, không cần chuyển sang depth hay tạo mô hình trắng: một người, toàn thân, một cảnh liền mạch thì dùng Kling motion control; nhiều người, có chuyển máy hoặc có cắt giữa chừng thì dùng Seedance 2.5 omni reference; muốn chạy cục bộ thì dùng Wan Animate. Báo cáo sẽ chọn sẵn một cách theo các tiêu chí này, prompt đã viết xong:
   - Nền gốc lộn xộn (đường phố, đám đông, đồ đạc), hoặc không gian mới khác xa gốc: chuyển thành video depth (`--depth` hoặc Video Depth Anything) rồi mới đưa vào, chỉ giữ lại động tác, không gian và chuyển máy.
   - Đổi cả không gian lẫn góc máy, hoặc bộ động tác này sẽ dùng nhiều lần: chuyển chuyển động bắt được thành mô hình trắng, rồi dựng lại góc máy trong Blender và render, sau đó sinh bằng tham chiếu mô hình trắng.
   - Biểu cảm khuôn mặt là điểm chính: giữ nguyên cách tham chiếu trực tiếp video gốc. Depth, khung xương và mô hình trắng chỉ mang thân người, biểu cảm sẽ mất.
   - Nhân vật mới là kiểu chibi (đầu to thân nhỏ), động vật, hoạt hình, tỉ lệ cơ thể khác nhiều: dùng video khung xương (DWPose + Wan VACE).
4. Đưa các đoạn đã sinh cho agent, agent sẽ dùng `rea-video drive --join` để ghép lại vào timeline gốc, rồi xuất clip so sánh đặt cạnh video gốc, đối chiếu với bản nhạc gốc xem các điểm nhịp.

## Hoạt hình và giao diện: viết code

Báo cáo đưa ra nội dung chữ, bố cục và nhịp hoạt ảnh của từng đoạn. Bảo agent "viết một dự án Remotion theo báo cáo"; sau đó sửa nội dung chỉ cần sửa dữ liệu. Hiện công cụ chưa tự sinh dự án này, agent phải tự viết.

## Ảnh tĩnh pan/zoom: dựng ngay trên máy

Một ảnh cộng với tốc độ zoom và pan đo được, agent dựng ngay trên máy, không cần gọi model.

## Âm thanh: ba track làm riêng

- Giọng người: báo cáo có kịch bản, dùng TTS để sinh hoặc tự thu.
- Nhạc nền: tìm trong thư viện theo BPM, tông và phong cách, hoặc dùng Suno để sinh.
- Hiệu ứng: thêm theo bảng thời điểm.
