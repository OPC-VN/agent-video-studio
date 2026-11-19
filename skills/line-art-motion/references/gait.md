# Dáng đi

## Thời gian, tọa độ và tiếp đất

`gait(kind, overrides).pose(phase)` nhận pha theo chu kỳ; `createWalker(...).render(t)` nhận giây tuyệt đối. Đổi giây thành pha bằng `phase = t / period`. `groundSpeed = stride / (duty * period)` là tốc độ trong tọa độ nội bộ; với scale dương `s` tốc độ trên cảnh là `s * groundSpeed`, chiều đi chọn `direction` là `1` hoặc `-1`. Nếu tự đặt vị trí nhân vật, đồng bộ nó với tốc độ đó; không tween vị trí độc lập rồi kỳ vọng chân đứng yên.

Component `createWalker` hiện chọn preset `walk`, `shuffle` hoặc `run`; các tham số `stride` và `period` là của helper `gait`, chưa phải tùy chọn của component. `seed` của walker chưa tạo biến thể hình. Dùng `ground` làm tung độ đường đất của cảnh; kiểm cả scale và chiều đi trong bố cục thật.

Mỗi chân có `reached`: `false` nghĩa là mục tiêu đã bị kẹp vào tầm chi. Khi đó không kết luận chân chạm đất hoặc không trượt. Sau khi đổi chiều dài chi, độ cao hông, nhún hoặc sải, quét cả chu kỳ và kiểm hai chân, kể cả sát điểm nhấc, đặt và nối vòng.

Điểm cổ chân chạm đất chưa chứng minh nét hiển thị chạm đất đúng: mũi chân, hai nét tạo chi, độ dày stroke và bộ lọc mực có thể cắt xuống dưới nền. Xem khung phóng to và cả cảnh chuyển động, điều chỉnh hình hoặc bố cục trước khi bàn giao. Các preset là nguyên liệu minh họa, không phải mô phỏng giải phẫu người.

Muốn nhân vật dừng lại, đừng chỉ kẹp thời gian `render` ở một mốc tùy ý: vận tốc có thể chuyển đột ngột về 0 và giữ chân đang nhấc. Giữ thời gian cục bộ tăng đơn điệu, giảm dần tốc độ tiến thời gian về 0 tại tư thế đứng phù hợp, rồi xem sát hai phía điểm dừng và phát liên tục. Component hiện không có chuyển tiếp đi–đứng đóng gói sẵn; kỹ thuật ghép mới cần được kiểm riêng.
