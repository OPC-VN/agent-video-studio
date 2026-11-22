# Kiểm chất lượng avatar: thang đo, bài test, quyết định

Một bản dựng chỉ được giao khi qua **cổng tối thiểu**. Bài test sâu dùng khi chọn cấu hình mới hoặc bản dựng trượt.

## 1. Cổng tối thiểu: mọi bản giao, kể cả khi gấp

| # | Kiểm | Cách | Đạt khi |
|---|---|---|---|
| G1 | Khớp tiếng–hình | `video-studio avatar qa --video <mp4> --json` | `av_offset` = 0 **và** `confidence` ≥ 7 |
| G2 | Miệng khi im lặng | Trích 1 khung ở một chỗ nghỉ giữa câu, xem ảnh | môi khép |
| G3 | Miệng khi nói | Trích 1 khung ở một nguyên âm mở ("a", "o") | thấy răng hoặc lưỡi, không có khe tối, không nhoè |
| G4 | Đủ hình, đủ tiếng | `ffprobe` | có cả luồng hình và tiếng; thời lượng lệch WAV ≤ 0,1 giây |

Trích khung để soi (giây thứ `t`):
```
ffmpeg -ss <t> -i <mp4> -frames:v 1 qa/khung-<t>.png
```
Tìm chỗ im lặng: đọc WAV, chọn đoạn nghỉ dài nhất, hoặc dùng `ffmpeg -af silencedetect=n=-35dB:d=0.3`.

Không qua cổng thì không giao bản dùng thật. Hết giờ: giao kèm nhãn "bản nháp, chưa đạt G<n>", nêu rõ điểm.

## 2. Thang đo

| Thước đo | Ý nghĩa | Ngưỡng | Ghi chú |
|---|---|---|---|
| SyncNet confidence | Mức môi khớp âm thanh, model SyncNet chấm | ≥ 7 đạt · 6–7 xem lại · < 6 trượt | video thật thường đạt 7–9; mặt phải theo dõi được ≥ 2 giây |
| AV offset | Hình lệch tiếng bao nhiêu khung (1 khung = 40 ms ở 25 fps) | 0 | ±1 thấy được bằng mắt ở đoạn nói nhanh |
| Mặt bị mất khi làm nét | `face_missed` trong kết quả `optimize --task mouth` | 0 | > 0: khung đó giữ nguyên bản cũ, có thể chớp ở vùng miệng |
| Thời gian dựng | `elapsed_seconds` | để lập kế hoạch | LatentSync 22–94 giây cho mỗi giây video trên RTX 4070 (đo 22/11/2026, lần chậm có thể do GPU đang bận việc khác) |

Điểm tham chiếu đo ngày 22/11/2026 trên clip 720×720, 10 giây tiếng Việt: MuseTalk `--bbox-shift -15` đạt 4,79, lệch 1 · LatentSync guidance 2,5 đạt **7,94**, lệch 0 · sau làm nét miệng đạt 7,80, lệch 0.

## 3. Bài test khi đổi cấu hình (A/B)

Dùng khi đổi engine, guidance, khung cắt, clip nền hay tốc độ giọng.
1. Cố định một WAV thử 8–12 giây, có cả đoạn đọc nhanh lẫn chỗ nghỉ. Ghim seed.
2. Đổi **đúng một** tham số. Đặt tên file theo tham số, ví dụ `thu-g30.mp4`.
3. Chạy `avatar qa` cho từng bản. Ghi vào bảng: tham số, confidence, offset, thời gian.
4. Soi G2, G3 ở **cùng mốc giây** cho mọi bản. Ghép cạnh nhau để so:
   ```
   ffmpeg -i a.mp4 -i b.mp4 -filter_complex hstack=inputs=2 so-sanh.mp4
   ```
5. Chọn bản tốt hơn khi confidence tăng ≥ 0,3 mà G2, G3 không xấu đi. Chênh < 0,3 là nhiễu, giữ cấu hình cũ.
6. Đạt thì ghi tham số vào hồ sơ: `avatar profile update <id> --guidance …`.

## 4. Bản trượt: triệu chứng → sửa một thứ

| Triệu chứng | Nguyên nhân hay gặp | Thử |
|---|---|---|
| Miệng hé khi im lặng | MuseTalk | chuyển `--engine latentsync`; còn ở MuseTalk thì `--bbox-shift -10..-15` |
| Khe tối hoặc răng nhoè trong miệng | LatentSync dựng mặt ở 256 px | `optimize --task mouth`; cắt khung gần hơn để mặt lớn hơn |
| "o", "u" bị khép bớt sau làm nét | GFPGAN quá mạnh | `--strength 0.6` |
| Đoạn đọc nhanh môi trễ | model làm mượt theo nhóm 16 khung | xem [avatar-voice](avatar-voice.md) mục tốc độ; không dời tiếng (dời 40 ms làm điểm tụt) |
| Miệng mở ít, nói lí nhí | guidance thấp | guidance 2,5 → 3,0 |
| `qa` báo không có điểm | không theo dõi được mặt ≥ 2 giây | mặt quá nhỏ, bị che, hoặc quay nghiêng: kiểm clip nền theo tiêu chí ở [avatar-profile](avatar-profile.md) |
| Viền hàm lộ vệt, màu da lệch | clip nền sáng thay đổi | quay lại clip nền với ánh sáng đều |
| Vùng miệng chớp | `face_missed` > 0 | xem khung bị mất mặt; tay che hoặc quay đầu quá mạnh |
| Giật ở điểm lặp (MuseTalk) | cử chỉ nhanh trong clip nền | chọn clip nền có cử chỉ chậm hoặc ít cử chỉ hơn |

## 5. Lời giao

Ghi đủ: đường dẫn MP4 trong trạm · engine và tham số · SyncNet confidence và offset · G2, G3 đã soi ở giây nào · những gì **chưa** kiểm (ví dụ chưa xem ở tốc độ thật, chưa nghe hết). Có `--profile` thì `avatar qa --profile <id>` tự ghi lịch sử vào hồ sơ.
