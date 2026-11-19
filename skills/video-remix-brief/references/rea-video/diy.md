# Tự làm

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/diy.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Người dùng tự quay, tự cắt, hoặc tự sinh thủ công trên nền tảng khác (các trang như Jimeng, Kling), làm theo phương án quay và bảng phân cảnh của báo cáo; agent ghép tư liệu trở lại timeline gốc.

## Chi phí

- Bản thân rea-video không thu phí.
- Sinh thủ công trên nền tảng khác thì chịu phí của nền tảng đó; thiết bị và địa điểm quay tự lo.

## Khi người dùng muốn tự làm: hướng dẫn họ

1. Trước hết đưa các bước trong phần 2 «Làm theo các bước» của báo cáo (xem `remake.md`, mục «Làm theo các bước») và danh sách tư liệu cần chuẩn bị (quay gì, mỗi đoạn dài bao lâu, prompt của các đơn vị sinh nằm ở đâu).
2. Khi người dùng quay hoặc sinh xong, chỉ cần gửi đường dẫn file; phần còn lại agent làm: gắn với cảnh tương ứng, ghi `mine.json`, chạy `rea-video remake`, đưa `remake/compare.mp4` cho người dùng xem, và theo `remake/status.md` báo còn những cảnh và âm thanh nào phải làm.

## Ghép lại timeline gốc

1. Theo bảng phân cảnh (số cảnh và thời lượng trong `report.md`), gắn tư liệu với từng cảnh. Nếu một đoạn dài bao phủ nhiều cảnh thì trước hết dùng ffmpeg cắt theo chuyển động; nếu chưa chắc về tương ứng thì đưa ảnh chụp cho người dùng xác nhận.
2. Ghi vào `out/ref/remake/mine.json`: `{"results": {"<số cảnh>": {"video": "<đường dẫn tuyệt đối của tư liệu>"}, ...}}`. Nếu một đơn vị «sinh» thủ công bao phủ nhiều cảnh thì ghi dạng `{"G2": {"unit": "G2", "shots": [4, 5, 6], "video": "<đường dẫn>", "trim_to": <số giây của đơn vị>}}`; `remake` sẽ cắt theo điểm cắt gốc để chia lại cho từng cảnh.
3. Chạy `rea-video remake out/ref`. Mỗi đoạn tư liệu được căn theo chuyển động để khớp nhịp của cảnh gốc tương ứng (điểm bắt đầu/kết thúc động tác và đỉnh chuyển động nằm đúng thời điểm trong gốc). Mức tăng tốc tối đa 3 lần, làm chậm tối đa 1.25 lần; phần vượt thì cắt bỏ. Đoạn không có động tác rõ thì đổi tốc đều cho cả đoạn. Điểm cắt căn theo số khung gốc nên không bị lệch dần. Cảnh chưa điền thì tạm dùng video gốc làm chỗ giữ chỗ, âm thanh lấy từ gốc. Kết quả: `remake/remake.mp4`, `remake/compare.mp4` so sánh trái-phải, và `remake/status.md`. Báo cho người dùng biết cảnh nào còn là video gốc và âm thanh nào còn phải thay.
   - Chỉ muốn ghép mà không vẽ lại cảnh code thì dùng `rea-video assemble out/ref/breakdown.json <đường dẫn results.json>`.
   - Phụ đề gắn lại (`remake` mặc định có; `assemble` phải thêm `--overlays`): phụ đề, chữ nhấn và tiêu đề đo được được phủ lên cảnh đã thay theo đúng kiểu gốc (cảnh video gốc vốn đã có chữ nên không phủ thêm). Font là sans-serif thông dụng, màu và khung nền là giá trị đo được nên có thể khác gốc một chút. Sticker chỉ được liệt kê trong `stickers_to_add` của `assemble_log.json`; phải tự tìm tư liệu để dán.
