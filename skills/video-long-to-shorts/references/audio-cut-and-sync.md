# Cắt giọng, đồng bộ phụ đề và avatar, âm lượng

> **Kết luận:** chữ lấy từ nguồn, **mốc lấy từ nhận dạng giọng trên chính file âm**. Thời gian đi qua bản đồ clip (`media = t − start + media_start`), không qua một offset chung. Avatar cắt giữa take bằng cùng phép quy đổi nên giữ nguyên khớp môi của nguồn.

Số đo dưới đây lấy từ một đợt dựng ba short (giọng 24 kHz mono, engine HyperFrames 0.9.88); nguồn khác thì đo lại.

## Contents
- Bản đồ audio nhiều clip
- Mốc chữ lệch mốc giọng
- Chọn điểm cắt
- Fade, đệm và khe giữa đoạn
- Kiểm sau khi cắt
- Phụ đề
- Avatar giữa take
- Nhạc nền và âm lượng
- Việc chỉ tai người làm được

## Bản đồ audio nhiều clip

Một bản dài thường có vài clip `<audio>`: cùng một file phát làm hai lần với `data-media-start` khác nhau (vì chèn thêm đoạn ở giữa), cộng các file giọng ghép sau.

| Clip | Timeline | File | media_start |
|---|---|---|---|
| voice | 13,6–348,6 | `voice.wav` | 0 |
| voiceCard | 349,45–351,78 | `card.wav` | 0 |
| voiceB | 353,3–445,3 | `voice.wav` | 339,7 |
| voiceEnd | 445,6–548,9 | `ending.wav` | 0 |

- Giây trong file = `t − start + media_start` **của clip phủ t**. Giây 400 ở bảng trên là `400 − 353,3 + 339,7 = 386,4` trong `voice.wav`, không phải `400 − 13,6`.
- Một đoạn của short phải nằm trọn trong một clip; vắt qua ranh thì tách hai đoạn. `cut_voice.py` từ chối (mã 2) thay vì đoán.
- Nhạc nền cũng là một clip phủ cả timeline: script chọn clip có `volume` lớn nhất; hai clip giọng cùng phủ thì ghi rõ `clip` trong plan.

## Mốc chữ lệch mốc giọng

Mốc từ trong `source-map.json` là thời điểm **tô chữ karaoke** (lệnh GSAP), do người dựng bản dài căn bằng mắt hoặc nội suy. Đã đo so với nhận dạng giọng trên file âm:

- clip giọng chính: lệch ±0,03 s;
- clip giọng ghép sau: lệch 0,3–0,5 s, có điểm tới 0,7 s.

Hậu quả thật: một điểm cắt lấy theo mốc chữ đã rơi vào đuôi từ của câu trước. Vì vậy:

1. Mốc chữ chỉ dùng để **tìm vùng** (±1 s) và để dẫn mã dòng.
2. Điểm cắt và mốc phụ đề lấy từ nhận dạng giọng cấp từ, chạy offline trên file âm (mô hình cỡ vừa cho tiếng Việt là đủ).
3. Từ mà nhận dạng nghe sai (tên riêng, từ ngoại) thì dùng mốc nguồn quy đổi hoặc nội suy giữa hai từ khớp; `make_subs.py` làm việc này và báo số từ nội suy.

## Chọn điểm cắt

Thứ tự ưu tiên tại mỗi đầu đoạn:

| Hạng | Điểm cắt | Dấu hiệu đo | Ghi chú |
|---|---|---|---|
| 1 | Khoảng lặng thật giữa hai câu | mức −70 dB trở xuống, dài ≥ 80 ms | vào trước chữ đầu 0,10–0,15 s |
| 2 | Giọng tắt tự nhiên cuối câu | −57 dB rồi về số không | ra sau khi về số không 10–50 ms |
| 3 | Trũng năng lượng giữa lời liền | chỗ yếu nhất trong vùng, −25…−46 dB | chỉ khi cần bỏ từ nối đầu câu; fade bắt buộc; **đánh dấu cần người nghe** |

Bẫy: một trũng sâu ngay sau ranh từ có thể là **khe đóng của phụ âm tắc** (p, t, k) nằm *trong* từ kế. Cắt ở đó là cắt cụt phụ âm đầu. Đối chiếu với mốc từ của nhận dạng giọng: điểm cắt phải nằm **trước** mốc đầu của từ đầu tiên muốn giữ và **sau** mốc cuối của từ muốn bỏ.

Đo bằng đường bao RMS cửa sổ 10–20 ms và bộ dò khoảng lặng của ffmpeg; ghi mỗi điểm vào bảng «mốc kế hoạch → mốc dùng → lý do» trong `SHORTS-PLAN.md`.

## Fade, đệm và khe giữa đoạn

| Tham số | Giá trị | Vì sao |
|---|---|---|
| Fade hai đầu mỗi đoạn | cos 20–30 ms | hết tiếng tách; ngắn hơn phụ âm đầu |
| Đệm đầu short (`lead`) | 0,30 s im | lời vẫn vào trong 0,5 s đầu, hook kịp hiện |
| Khe giữa hai beat (`gap`) | 0,25–0,34 s | đủ nghe là hai ý, không hụt nhịp |
| Khoảng lặng gốc dài (0,8 s) giữa hai câu liền | rút còn ≈ 0,34 s | hai điểm cắt đều nằm trong vùng im |
| Đuôi (`tail`) | 1,5–2,5 s | chỗ cho thẻ kết |

## Kiểm sau khi cắt

1. **Không tiếng tách:** bước nhảy mẫu lớn nhất trong ±30 ms quanh mỗi mối nối ≤ 0,023 (thang −1…1). Đã đo 0,015–0,023 ở điểm cắt giữa lời, ≤ 0,002 ở điểm cắt trong khoảng lặng.
2. **Chữ đầu đúng:** nhận dạng giọng chạy lại trên `voice.wav` đọc đúng từ đầu của từng đoạn.
3. **Không lẫn lời ngoài:** bản nhận dạng của `voice.wav` không có từ nào ngoài dãy từ nguồn đã chọn.
4. Đỉnh mẫu < 1,0; `beats.json` ghi `peak`.

## Phụ đề

- Chữ: dãy từ nguồn giữa `first_word` và `last_word` của từng đoạn, nguyên văn, giữ dấu câu.
- Mốc: nhận dạng giọng trên `voice.wav` (mốc theo short). Từ đầu mỗi đoạn neo vào `short_in` vì công cụ nhận dạng hay trả 0,00 cho từ đầu.
- Nhóm: tách theo `.` `?` `!` và dấu phẩy khi mệnh đề đủ 3 từ; chia đều mỗi mệnh đề thành cụm 3–5 từ; cụm cuối câu có thể 1–2 từ.
- Từ ghép có gạch nối tính là một từ hiển thị, lấy mốc của mảnh đầu.
- Bề rộng: `make_subs.py` chặn theo số ký tự (`--max-chars`); bước dựng đo lại bằng font thật theo [vertical-layout](vertical-layout.md).

## Avatar giữa take

Take avatar trong bản dài thường là một file video có alpha, phát từ khung 0 tại `data-start` của nó. Short bắt đầu giữa take:

```html
<video id="take3" class="clip" src="assets/avatar/take3.webm" muted playsinline
       data-start="8.63" data-duration="9.16" data-media-start="11.74" data-track-index="3"></video>
```

- `data-media-start` = `tl_in − start_của_take + media_start_của_take`; `cut_voice.py` ghi sẵn ở `segments[].avatar.media_start`. `data-start` = `short_in`, `data-duration` = `short_out − short_in`.
- Không cần cắt lại file video. Đã đo: khung render khớp khung take đúng offset (sai số trung bình 1,4–1,5 mức, là nhiễu nén; đối chứng lệch offset cho 2,4–9,7), âm cùng offset tương quan 0,99998, lệch 0 ms.
- Giọng và avatar **cùng điểm vào** thì khớp môi của nguồn được giữ. Nếu rút khoảng lặng giữa hai đoạn, avatar cũng cắt tại đúng hai điểm đó (hai clip video, hoặc đổi take tại ranh có sẵn).
- `covers_segment: false` nghĩa là take hết trước khi đoạn hết: tìm take kế trong `source-map.json` hoặc cho avatar ra ở ranh câu gần nhất.
- Đoạn không có take phủ thì **không có avatar**; không mượn take của lời khác.
- Bằng chứng trên là số học; khớp môi từng âm vẫn cần người xem bản render.

## Nhạc nền và âm lượng

| Mục | Chuẩn đã dùng |
|---|---|
| Giọng sau cắt | ≈ −24 LUFS (giữ nguyên mức nguồn, không nén thêm) |
| Nhạc nền | **một** clip duy nhất suốt short, `data-volume` 0,12 (≈ −34 LUFS), fade vào 1,2 s, fade ra 2 s |
| Master | chuẩn hoá hai lượt về −14 LUFS, true peak −1,5 dBTP, LRA 11 |
| Kết quả đo | −14,1 LUFS, true peak −1,4 dBFS |

- Nhạc là quyết định của Cổng 1 và mang rủi ro giấy phép: ghi nguồn + điều khoản; chưa xác minh thì ghi «chưa xác minh» trong `PUBLISH.md`. Dựng sao cho đổi nhạc chỉ sửa một dòng.
- Kênh có mức chuẩn riêng (ví dụ bám mức của bản đã phát hành) thì theo kênh và truyền `--lufs`, `--tp-max` tương ứng cho `qa_short.py`.
- Không để im tuyệt đối ở đầu: nhạc vào từ 0 s, lời vào ≤ 0,5 s.

## Việc chỉ tai người làm được

Máy chứng minh được «không tách, đúng chữ, đúng mức». Máy không chứng minh được «nghe tự nhiên». Trước khi đăng cần một người nghe: mọi điểm cắt hạng 3 (giữa lời liền), mối nối rút khoảng lặng, và mức nhạc so với giọng trên loa điện thoại. Chưa có người nghe thì ghi rõ từng mốc giây vào danh sách chưa kiểm.
