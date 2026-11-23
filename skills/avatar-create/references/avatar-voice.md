# Giọng cho avatar: nhận từ voice-studio, chuẩn hoá, ghép

Avatar nói theo **một file WAV**. Giọng clone tạo ở repo `agent-voice-studio` (skill `voice-routing`). Trang này nói cách nhận, chuẩn hoá và ghép giọng đó cho đúng yêu cầu của engine.

## 1. Quyền

Giọng cũng phải theo cùng luật đồng ý với khuôn mặt. Người trong hình và chủ giọng có thể là hai người khác nhau; cần lời đồng ý của cả hai. Không ghép mặt người A với giọng người B nếu B chưa đồng ý cho việc đó.

## 2. Tạo WAV từ kịch bản

1. Kịch bản viết theo `voice-routing` → `references/vietnamese-tts-script.md`: số, chữ viết tắt, tên nước ngoài viết lại cho engine đọc đúng. Gắn marker sắc thái (`[ten-marker]`) theo manifest của profile, không đổi profile giữa bài; `voice-studio speak` đọc marker, marker lạ bị gỡ.
2. Đọc bằng profile giọng ghi trong hồ sơ avatar (`voice.profile`), ghim seed:
   ```
   voice-studio speak --file loi.txt --profile <profile> --seed <số> --out <trạm-video>/avatars/<id>/renders/loi.wav --json
   ```
   Không dùng `--instruct` cho bản giao: mỗi câu sẽ ra một giọng khác.
3. Cho ASR nghe lại bản đọc trước khi dựng hình (luật "đo, đừng tin tai" của voice-studio). Dựng hình mất 4–16 phút cho 10 giây; sửa lời sau khi dựng là mất công gấp đôi.

## 3. Chuẩn hoá WAV cho engine

| Engine | Yêu cầu | Tối đa |
|---|---|---|
| LatentSync | WAV PCM | 60 giây mỗi lần (giới hạn của lệnh) |
| MuseTalk | WAV PCM16, mono, 16 kHz | 30 giây mỗi lần |

Một lệnh đưa MP3, M4A hay WAV bất kỳ về dạng dùng được cho cả hai:
```
ffmpeg -i <vào> -ac 1 -ar 16000 -c:a pcm_s16le <ra>.wav
```

Bài dài hơn giới hạn: cắt tại chỗ nghỉ giữa câu, mỗi đoạn 15–45 giây, dựng từng đoạn, nối ở bước dựng video. Không cắt giữa từ: khẩu hình ở mép đoạn sẽ hỏng.

## 4. Giọng có nhạc nền hoặc hiệu ứng (bản mix)

Engine đọc khẩu hình từ **giọng**. Nhạc và hiệu ứng làm khẩu hình sai.
- Dựng hình bằng **WAV chỉ có giọng** (stem lời).
- Sau khi dựng, thay tiếng bằng bản mix cuối cùng:
  ```
  ffmpeg -i <avatar>.mp4 -i <mix>.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -shortest <giao>.mp4
  ```
- Bản mix phải giữ **đúng thời điểm** của giọng (không cắt, không chèn khoảng lặng ở đầu). Lệch 40 ms là thấy.
- Chỉ có bản mix, không có stem lời: tách giọng bằng `voice-studio clean` trước, rồi dựng bằng giọng đã tách và ghép lại bản mix gốc.
- Chạy `avatar qa` trên **bản giao** (sau khi ghép mix). Điểm tụt nhiều so với bản chỉ có giọng thì nhạc đang lấn giọng, cần hạ nhạc.

## 5. Tốc độ đọc và khẩu hình

- Mặc định giữ `speed` 1.0 trong hồ sơ giọng và hồ sơ avatar.
- **Giả thuyết, chưa đo:** LatentSync làm mượt theo nhóm 16 khung, nên đọc chậm hơn có thể giúp môi theo kịp đoạn nhanh.
- Chỉ thử khi SyncNet < 7 hoặc thấy môi trễ ở đoạn nhanh:
  1. đổi sang marker sắc thái có nhịp chậm hơn ở đầu đoạn đọc nhanh (tên marker lấy từ `<profile>.profile.json`, nhịp từng marker xem báo cáo kiểm thử của profile; phân bổ theo `voice-routing`, `vietnamese-tts-script.md`, mục "Phân bổ sắc thái theo bố cục video"); profile không có marker thì bỏ bước này;
  2. rồi mới thử `speed` 0,95, sau đó 0,9, cùng seed.
- Giữ mức mới khi SyncNet tăng ≥ 0,3 **và** ASR vẫn nghe đúng. Ghi mức đã chọn vào `voice.speed` của hồ sơ, kèm điểm đo.

## 6. Bàn giao giữa hai repo

| Bước | Repo | Đầu ra |
|---|---|---|
| Kịch bản → WAV giọng | voice-studio (`speak`) | `renders/<tên>.wav` trong thư mục hồ sơ avatar |
| WAV → avatar | video-studio (`avatar render`, `optimize`, `qa`) | `renders/<tên>.mp4` |
| Avatar + slide + nhạc | video-studio (`render --project-dir`, `edit`) | video bài giảng |

Lồng tiếng cho video không có avatar (chỉ slide) dùng `video-studio narrate`, không dùng luồng avatar.

## Đoạn nối thêm vào video đã duyệt

Chỉ làm take mới cho đoạn lời mới, không render lại take cũ; kiểm mối nối giữa take cũ và mới (hình, âm, lệch ≤ 1 khung).
