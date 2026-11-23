# Thư viện âm thanh AU (nhạc nền, SFX, khoảng lặng, hạ nhạc dưới giọng)

Kết luận: bộ mẫu đầu (5 video, A–E) gần như **không phân tích tiếng**: nhật ký cảnh chỉ ghi hình và lời thoại, nên mọi mẫu AU dưới đây hoặc chỉ có dấu vết gián tiếp (waveform, nhãn «Music/Voiceover» trên màn hình, lời kể về tiếng) hoặc là thông lệ dựng chưa có bằng chứng («suy ra · 0 nguồn»). Lần học sau cần thêm **cột âm** vào nhật ký cảnh (nhạc có/không, mức so với giọng, SFX ở mốc nào, khoảng lặng bao lâu) rồi mới nâng độ tin.

Khuôn mẫu, độ tin, mã video và chế độ: xem `library-contract.md`; danh sách mã: `pattern-index.md`.

## Contents
1. Giới hạn bằng chứng
2. AU-01 … AU-07
3. Việc cần làm ở lần học sau

## 1. Giới hạn bằng chứng

- Nhật ký cảnh có cột chữ trên màn hình, chuyển động, chuyển cảnh, lời thoại; **không có cột âm**. Dấu hiệu âm thanh tìm được chỉ là: waveform và track nhạc/giọng vẽ trong cảnh nói về dựng video (A), và một câu lời thoại nói về tiếng (A 1:30).
- Không có mẫu nào ở đây được nghe hay đo trên tệp âm thanh. Mốc «ước» chỉ nói **hình** ở mốc đó liên quan đến âm, không nói tiếng ở mốc đó ra sao.
- Mẫu «suy ra · 0 nguồn» là thông lệ dựng chung, đặt vào thư viện để có chỗ gắn bằng chứng sau; chưa dùng làm khuyến nghị chắc.

## 2. Các mẫu AU

### AU-01 · Đặt mốc hình theo đỉnh nhạc
- **Trông thế nào:** (hình, vì chưa có tiếng đo) timeline có track nhạc dạng waveform xanh lá, marker kim cương đỏ đặt đúng đỉnh waveform; clip biểu đồ cột cam đặt ở một đỉnh.
- **Chuyển động:** marker thêm dần lên đỉnh nhạc; playhead chạy qua các clip và dừng ở clip khớp đỉnh.
- **Giữ:** chưa có
- **Khi dùng:** nói về dựng theo nhạc; muốn hình đổi đúng nhịp nhạc.
- **Tránh:** chưa có
- **Bằng chứng:** A 1:24–1:34 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** lấy mốc đỉnh từ phân tích nhịp của bản nhạc rồi đặt `data-start` clip hình theo mốc đó; chưa có số đo từ mẫu.
- **Biến thể:** —

### AU-02 · Âm nhấn (SFX) khi phần tử hiện
- **Trông thế nào:** một tiếng ngắn gắn với mỗi lần một phần tử mới hiện trên màn hình (thẻ, chữ, icon).
- **Chuyển động:** tiếng bắt đầu cùng khung phần tử vào; độ dài và âm sắc: chưa có.
- **Giữ:** chưa có
- **Khi dùng:** khi muốn nhịp hiện của phần tử nghe được, nhất là danh sách bật từng mục.
- **Tránh:** chưa có
- **Bằng chứng:** chưa có tiếng đo; lời thoại A 1:30 nói «mỗi thứ hiện trên màn có một tiếng» (lời kể, nhật ký), không xác nhận video đó dùng.
- **Độ tin:** suy ra · 0 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### AU-03 · Whoosh / âm bước khi cắt hoặc chuyển cảnh
- **Trông thế nào:** tiếng quét hoặc tiếng chạm ≤ 0.2 s đặt tại điểm cắt cứng hoặc chuyển.
- **Chuyển động:** ≤ 0.2 s tại điểm chuyển (con số lấy từ ghi chú ở TR-01, không có mốc đo).
- **Giữ:** ≤ 0.2 s (theo TR-01)
- **Khi dùng:** khi muốn «nhịp cắt theo lời» cho cắt cứng (TR-01).
- **Tránh:** chưa có
- **Bằng chứng:** chưa có; ghi chú «âm bước/whoosh ≤ 0.2 s nếu muốn nhịp» ở TR-01 là thông lệ, không có mốc từ video mẫu.
- **Độ tin:** suy ra · 0 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### AU-04 · Hạ nhạc dưới giọng (ducking)
- **Trông thế nào:** nhạc nền thấp hơn giọng khi có lời; trở về mức cao hơn trong khoảng không lời.
- **Chuyển động:** mức nhạc xuống khi giọng vào, lên khi giọng ra; thời gian lên/xuống và mức chênh: chưa có.
- **Giữ:** chưa có
- **Khi dùng:** mọi đoạn có nhạc nền và giọng đọc.
- **Tránh:** chưa có
- **Bằng chứng:** chưa có; track nhạc và track giọng chỉ thấy vẽ trên màn hình ở A (9:32–9:38, 14:42–14:54), không cho biết mức âm.
- **Độ tin:** suy ra · 0 nguồn
- **Gợi ý dựng:** tween mức âm lượng của phần tử nhạc theo mốc vào/ra của lời; chưa có số đo từ mẫu.
- **Biến thể:** —

### AU-05 · Khoảng lặng trước câu chốt / cuối video
- **Trông thế nào:** một quãng không lời (có thể không nhạc) trước câu chốt hoặc ở cuối.
- **Chuyển động:** chưa có
- **Giữ:** ≈ 3–4 s im lặng cuối (con số ghi ở RC-35, chưa có phép đo tiếng).
- **Khi dùng:** kết vòng câu chuyện (RC-35); để người xem tự nghĩ sau câu hỏi treo (ST-01).
- **Tránh:** chưa có
- **Bằng chứng:** chưa có; hình ở C 15:52, 17:58 (cảnh kết vòng) không cho biết có lặng hay không.
- **Độ tin:** suy ra · 0 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

### AU-06 · Chữ sáng theo nhịp giọng (đồng bộ chữ–giọng)
- **Trông thế nào:** từng từ của câu sáng lên đúng lúc được nói, waveform giọng chạy bên dưới (xem TX-11).
- **Chuyển động:** mỗi từ đổi màu tại thời điểm bắt đầu từ đó; các từ còn lại mờ 50%.
- **Giữ:** chưa có
- **Khi dùng:** nhấn nhịp, dạy ngôn ngữ, khi có timestamp từng từ.
- **Tránh:** khi không có timestamp chính xác từng từ.
- **Bằng chứng:** A 10:38–10:50, A 12:14–12:20 (nhật ký).
- **Độ tin:** ước · 1 nguồn
- **Gợi ý dựng:** dùng timestamp từng từ của bản chép lời làm mốc tween màu (xem TX-11).
- **Biến thể:** —

### AU-07 · Đổi nhạc / nhịp theo chương
- **Trông thế nào:** nhạc nền đổi sắc thái hoặc nhịp khi vào chương mới, ăn khớp thẻ chương.
- **Chuyển động:** chưa có
- **Giữ:** chưa có
- **Khi dùng:** video nhiều chương (C: 10 thẻ chương; E: nhịp mục 30–106 s).
- **Tránh:** chưa có
- **Bằng chứng:** chưa có; thẻ chương có hình (C tr 63–68, E tr 237.4) nhưng không có dữ liệu về nhạc ở các mốc đó.
- **Độ tin:** suy ra · 0 nguồn
- **Gợi ý dựng:** chưa có
- **Biến thể:** —

## 3. Việc cần làm ở lần học sau

- Thêm **cột âm** vào nhật ký cảnh: nhạc (có/không, đổi ở mốc nào), mức nhạc so với giọng, SFX (mốc, gắn với hình nào), khoảng lặng (mốc, bao lâu).
- Phân tích tiếng bằng công cụ (dò nhịp, mức âm theo thời gian) rồi ghi mốc kèm bậc «đo»; hiện chưa mẫu nào đạt bậc đó.
- Khi có số đo: nâng AU-02/03/04/05/07 theo luật nâng bậc trong `library-contract.md`, và gộp AU-01 với mốc đo thật.
