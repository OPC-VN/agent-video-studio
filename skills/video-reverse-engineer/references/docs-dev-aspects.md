# Chiều phân tích kỹ thuật quay (aspects): cách mở rộng

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · docs/dev/aspects.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Mỗi chiều là một module trong `rea_video/aspects/`, chịu trách nhiệm toàn bộ quy trình của một vấn đề. Thêm chiều mới không cần sửa pipeline, prompt, mẫu review, báo cáo hay đánh giá:

| Bước | Phương pháp | Sản phẩm |
|---|---|---|
| Đo từng cảnh | `measure(ctx)`: `ctx.frames` các khung lấy mẫu, `ctx.subjects` chủ thể từng khung (khuôn mặt / vùng rõ nét / tâm khung), `ctx.features` đặc trưng chuyển động và texture | `shot.aspects.<key>.measured` |
| Hỏi qua hình | `shot_fields` / `video_fields`: `Field(key, tên tiếng Trung, câu hỏi, prefer)` | Tự động đi vào prompt VLM và `review_answers.json` |
| Diễn giải từng cảnh | `interpret(shot)` | `shot.aspects.<key>.result` |
| Tổng hợp cả video | `summarize(shots, b)`: trả về `result` (giá trị có thể đánh giá), `lines` (dòng tóm tắt), `fields` (bảng đối chiếu đo / VLM / xem ảnh / kết luận) | `breakdown.aspects.<key>` |
| Đánh giá | `check(gt, summary)`, mặc định so sánh các trường trong `result` | Trong `eval/*.yaml` viết `aspects: {<key>: {<trường>: giá trị chấp nhận}}` |

Trường có `prefer="seen"` lấy kết luận từ xem ảnh làm chuẩn (agent ưu tiên hơn VLM); `prefer="measured"` lấy đo lường làm chuẩn, còn kết luận xem ảnh được hiển thị song song.

Các chiều hiện có: `framing` khung hình (cỡ cảnh, góc máy, bố cục), `camera` máy quay (cầm tay/cố định, chuyển động máy, ống kính, thiết bị), `lighting` ánh sáng (hướng đèn chính, tỉ lệ sáng, mềm/cứng, nhiệt màu, sơ đồ ánh sáng + thiết bị; bảng quy tắc `SETUPS` có thể thêm dòng), `editing` cắt ghép (nhịp, số máy quay, jump cut, cắt đẩy gần, cắt đúng khoảng ngắt hơi, tỉ lệ chèn cảnh), `format` hình thức (nói trước camera / quay trên mặt bàn / cầm tay giới thiệu vật / vlog).

Thêm chiều mới: viết một lớp con `Aspect`, cuối module gọi `register(...)`, rồi import trong `aspects/__init__.py` theo thứ tự phụ thuộc. Chiều nào cần kết quả của chiều khác (như `format` dùng `editing`) thì đặt sau chiều đó.
