# Kiểm tra

## Kiểm một cảnh trước khi dùng lại

1. Chạy `node --test tests/line-art.test.cjs`. Với cấu hình của cảnh riêng, kiểm hai chân tại pha đứng/vung, hai phía thời điểm nhấc và đặt, ranh giới chu kỳ, `reached` và hướng/scale đã chọn. Đo độ trượt trong tọa độ thế giới, không chỉ so tọa độ cục bộ.
2. Kiểm thứ tự tua tiến, lùi, xáo và lặp lại; tách kiểm DOM hoặc trạng thái khỏi kiểm khung do engine render. Với GSAP, kiểm cả trường hợp tua mà callback bị tắt; gọi trạng thái đầu sau mount. Xem ví dụ setter trong [component-cards.md](component-cards.md).
3. Render thực bằng `video-studio render` trên engine ghim. Xem khung phóng to và xem chuyển động liên tục nếu công cụ hỗ trợ; nếu chỉ có ảnh rời, ghi rõ đó là ảnh rời. Chọn thêm các khung sát nhau quanh điểm chân chạm đất và kiểm mũi chân, nét dày, giao nhau, tương phản, điểm treo, mép khung.
4. Render hai lượt cùng project và engine, ghi mã thoát, kích thước, fps, thời lượng, số khung, hệ điều hành; so khung, vùng nhân vật đang chuyển động và vùng đối chứng tĩnh bằng phương pháp đã chốt của dự án. Số đo nền tĩnh không chứng minh vùng chân đúng. Không suy ngưỡng chung từ một phép đo cục bộ; nếu chưa có ngưỡng, báo số đo và trạng thái chưa nghiệm thu.
5. Tạo một project khác từ thư mục trống, cấp component **và** `line-art.mjs` cùng thư mục; thử import, mount, tua và render trước khi tuyên bố tái sử dụng. `materialize-repo` một file chưa tự cấp helper.

Khi cần tối ưu hình, giữ nguyên seed, camera, bố cục và thời lượng; tạo hai bản chỉ đổi một tham số, ghi tên và giá trị A/B. Xem cả hai ở cùng tốc độ; ghi thời điểm và hiện tượng cụ thể rồi điều chỉnh tiếp. Máy chỉ xác nhận phát hết và số khung; người xem đánh giá nhịp, ý nghĩa và độ dễ đọc. Nếu chưa xem phát liên tục thì không báo đã duyệt nhịp.

Đo vùng chuyển động trên toàn quỹ đạo của người, đầu, chân, mũi chân và cả bề dày nét; ghi tọa độ ROI và kiểm nó còn bao phủ ở đầu lẫn cuối cảnh. So riêng vùng tĩnh và vùng động. Quét độ tương phản giữa mực và nền trong suốt khoảng thời gian dùng, đặc biệt khi nội suy ngày–đêm: kiểm chữ của engine không bảo đảm kiểm nét SVG. Nếu nét mờ, điều chỉnh dải màu hoặc khoảng thời gian rồi render lại; ghi giới hạn khi chưa chứng minh toàn bộ vòng màu.

Nếu mực chuyển từ tối hơn nền sang sáng hơn nền bằng nội suy liên tục, sẽ có đoạn độ sáng gần nhau. Khi cần đi qua đoạn đó, thử đường viền tương phản độc lập, chuyển màu bằng một cut có chủ đích, hoặc giữ cùng quan hệ sáng–tối trong đoạn; kiểm lại hình đã render. Khi chỉ dùng một cửa sổ màu an toàn, ghi khoảng thời gian hoặc pha đã kiểm, không suy toàn vòng an toàn.

Kiểm số học, kiểm tìm lại catalog, kiểm trình duyệt, render và xem hình là các bằng chứng riêng. Test giả DOM không chứng minh engine đã tua đúng; render một cảnh cũng không chứng minh component đã được tái dùng.
