# Từ nội dung đến ảnh dựng được lại

## 1. Brief và sơ đồ

Viết một câu người xem phải nhớ, sau đó lập dàn ý gồm tiêu đề, 2–5 khối, điểm kết và chú thích/nguồn nếu cần. Kiểm tra quan hệ: mũi tên chỉ thời gian, chuyển giao hoặc nguyên nhân có căn cứ; không gắn cho các nhóm ngang hàng. So sánh dùng cùng tiêu chí, cùng đơn vị và cùng mốc. Chốt kích thước đích, khung an toàn và bố cục nháp trước khi sinh ảnh. Đổi tỷ lệ khung thì bố trí lại, không kéo giãn bản ngang hoặc cắt mất chữ.

Mẫu đặc tả mỗi hình:

```text
ID: step-02-review
Vai trò: trả lời câu hỏi “ai kiểm tra kết quả?”
Động từ / đối tượng: đối chiếu hai tài liệu
Chi tiết bằng chứng: tay đánh dấu cùng một mục trên hai bản in
Kiểu hình: cảnh người chân thực, góc nghiêng, chủ thể bên phải
Bố cục: ô phải, chừa lề hướng về cột chữ; không che mũi tên
Không sinh: chữ, số, logo, watermark, hình minh họa khác
```

Ví dụ đối chiếu: “Tìm tài liệu → Kiểm nguồn → Giao việc cho AI”. Dùng ba cảnh khác nhau: người mở ngăn hồ sơ; bàn tay đối chiếu hai tờ giấy; người chỉ vào sơ đồ phân việc cạnh máy tính. Cảnh cuối không được sao lại cảnh đầu với màu nền mới. Nếu ý là so sánh các cách làm, đổi thành hai cột theo cùng tiêu chí thay vì dùng hàng mũi tên.

## 2. Tạo và duyệt từng tài sản

- Prompt cho trình tạo ảnh: “Ảnh chân thực một người đang đối chiếu hai tờ giấy trắng tại bàn, ngón tay chỉ vào vị trí tương ứng, góc nghiêng 3/4, ánh sáng mềm từ trên trái, chủ thể đặt bên phải khung, chừa khoảng trống bên trái, phong cách nhiếp ảnh biên tập. Không chữ, ký hiệu, logo hoặc watermark. Xuất nền trong suốt nếu là tài sản cắt nền.”
- Lưu bản sinh nguyên gốc và prompt; nếu công cụ không hỗ trợ alpha, chọn nền đơn màu hoặc dùng công cụ tách nền có sẵn. Kiểm viền trên cả nền sáng/tối, bàn tay/đạo cụ, sự hợp lý của động tác và góc sáng. Đổi prompt hoặc sinh lại khi sai nghĩa dù hình đẹp. Không thay người thật bằng bản mô phỏng nếu dự án chưa cấp quyền.
- Chuẩn hóa theo loạt: thống nhất ánh sáng, độ đậm và bảng màu, nhưng đa dạng tư thế, khung ảnh, đồ vật và icon. Asset tạo ra chưa mặc định là file hợp lệ: mở file thật, kiểm kích thước, nền và giấy phép/nguồn nếu sao chép. Nếu chỉ có preview không lưu được, không báo đã có asset.

## 3. Ghép và xuất

1. Chọn một nguồn chỉnh sửa được: HTML/CSS, SVG có lớp, hoặc dự án thiết kế của trạm. Giữ chữ tiếng Việt trong tệp UTF-8 riêng/spec; áp font có đầy đủ glyph, khóa đúng font/version nếu nền tảng hỗ trợ. Giữ logo SVG/PNG duyệt riêng; không rast hóa chữ hoặc logo trước khi cần.
2. Xếp nền → đường dẫn và khối → ảnh/cutout → chữ và logo. Dùng grid và vùng đệm; đặt cutout bằng contain hoặc crop có điểm neo, không kéo sai tỷ lệ. Chi tiết bị che thì đổi vùng chữ hoặc ảnh, không nén dòng vô tội vạ. Nếu dùng HTML/CSS cho xuất tĩnh, mở canvas đúng viewport, chờ font và ảnh thực sự tải, xuất ảnh vùng canvas tại kích thước yêu cầu; không dùng screenshot cửa sổ có thanh trình duyệt.
3. So chữ với nguồn ở bản xuất: dấu, ngắt dòng, tên riêng, số liệu, chú thích; kiểm không có chữ ngầm trong ảnh sinh, logo đúng, alpha sạch, thứ tự đọc rõ khi thu nhỏ. Duyệt preview 560–620 px với ảnh ngang; không chấp nhận bản preview trong trình biên tập nếu chưa mở file cuối. Với video, kiểm các khung đầu/cuối của hiệu ứng và thời gian đọc; render qua luồng của repo, không tự đổi phiên bản engine.
4. Bàn giao PNG và bản chỉnh sửa, assets đã dùng, font/tham chiếu và nguồn, brief/prompt cùng hướng dẫn tái tạo nêu renderer, phiên bản nếu có, lệnh hoặc bước xuất, kích thước và thứ tự lớp. Đặt tên theo ID/khổ/phiên bản, giữ bản trước. Bảng đối chiếu theo loạt cần cho thấy bài nào thực sự bị lặp bố cục, icon hoặc cảnh. Ghi trạng thái riêng cho nội dung, asset, render và duyệt; không suy là đã đăng.

Dừng bàn giao ở mức nháp nếu còn số liệu chưa kiểm, thiếu logo chuẩn đã yêu cầu, chưa xem được ảnh cuối, hoặc thiếu quyền đối với tài sản.