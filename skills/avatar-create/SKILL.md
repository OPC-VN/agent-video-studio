---
name: avatar-create
description: "Use when someone wants a talking-head avatar of themselves or of a person who agreed in writing: recording or preparing the idle clip, setting up the local lip-sync engine (LatentSync, or MuseTalk for drafts), making footage speak a new WAV, fixing a dark or blurry mouth, scoring lip-sync, or saving and reusing an avatar profile for a new lesson video. Also when asked to skip the checks, use someone else's photo, store face material in the repo, or upload a face to an online video generator."
---

# Tạo avatar nói — một cửa vào

Nhánh con của `video-routing`. Đầu ra là một MP4: người trong clip nói theo một file WAV mới, miệng khép khi im lặng, khẩu hình khớp tiếng. Mọi lệnh là `video-studio avatar …` và tuân hợp đồng mã thoát chung: `0` ok · `1` engine hỏng · `2` gọi sai · `3` thiếu trạm/engine.

Xác định đang ở bước nào, nạp **đúng một** reference cho bước đó:

| Đang làm | Nạp |
|---|---|
| Lần đầu dựng avatar cho một người, quay clip nền, lập hoặc sửa hồ sơ, ghi lời đồng ý, cần prompt cho công cụ tạo video AI | [avatar-profile](references/avatar-profile.md) |
| Chấm một bản dựng, so hai cấu hình, quyết định giao hay dựng lại | [avatar-quality](references/avatar-quality.md) |
| Cần WAV từ kịch bản bằng giọng clone, ghép MP3 hoặc nhạc, khẩu hình trễ ở đoạn đọc nhanh | [avatar-voice](references/avatar-voice.md) |
| Cài engine | `docs/LATENTSYNC.md` (bản dùng thật), `docs/MUSETALK.md` (bản nháp) ở gốc repo |

## Bốn luật đè mọi thứ

**1. Chỉ mặt của chính người dùng, hoặc người đã đồng ý bằng văn bản.**
- "Đồng ý" là lời của **người trong hình**, có phạm vi dùng (ví dụ "bài giảng nội bộ"). Lời người dùng kể lại ("chắc không phiền đâu") không phải đồng ý.
- Ảnh lấy từ mạng xã hội, ảnh công khai, ảnh người nổi tiếng: **từ chối dựng**, kể cả "bản nháp nội bộ". Đưa lối ra hợp lệ:
  - người đó tự gửi clip và lời đồng ý;
  - dùng avatar của chính người dùng;
  - dùng nhân vật minh hoạ không phải người thật.
- Chưa có lời đồng ý thì không tạo hồ sơ. `avatar profile new` bắt buộc `--relation`, `--consent-quote`, `--scope`. `avatar render --profile` từ chối hồ sơ đã thu hồi hoặc clip đã bị đổi.

**2. Mặt người là dữ liệu riêng: chỉ nằm trong trạm.**
- Ảnh, clip, hồ sơ, đặc trưng khuôn mặt và bản dựng chỉ ở `<trạm>/avatars/<id>/` hoặc project trong trạm.
- **Không bao giờ** đặt trong `skills/`, thư mục khác của repo, hay commit lên Git, kể cả khi người dùng bảo "cho tiện commit". Nói rõ lý do, rồi lưu vào trạm.
- Gửi ảnh mặt lên dịch vụ ngoài máy (công cụ tạo video AI, cloud): agent **không tự tải lên**. Đưa prompt cho người dùng tự làm. Chỉ tải hộ khi người dùng xác nhận đích danh **dịch vụ nào, ảnh nào** ngay trong chat.

**3. Không giao bản chưa qua cổng tối thiểu, kể cả khi gấp.**
Ba việc không được bỏ, mất khoảng 2–4 phút:
- `avatar qa`: SyncNet lệch 0 khung và độ tin cậy ≥ 7;
- soi ảnh ở 3 mốc: một chỗ im lặng (miệng phải khép), một chỗ đang nói (không có khe tối), khung cuối;
- `ffprobe` để kiểm có đủ hình và tiếng, thời lượng khớp WAV.

Không kịp dựng LatentSync thì giao bản MuseTalk, nhưng ghi rõ "bản nháp, SyncNet x,xx". Người dùng bảo "khỏi kiểm" vẫn chạy ba việc trên và báo kết quả. Chỉ bỏ khi người dùng nói rõ chấp nhận giao file **chưa kiểm** (ví dụ "tôi chấp nhận file chưa kiểm"; "khỏi kiểm" chưa đủ), và lời giao phải ghi đúng chữ "chưa kiểm".

**4. Đo, đừng đoán.** Mọi nhận định "khớp hơn", "nét hơn" phải kèm điểm SyncNet và ảnh khung đã soi. Đổi một tham số mỗi lần, ghim seed.

## Lối đi chuẩn

```
clip nền ─► optimize normalize ─► profile new ─► WAV (avatar-voice)
                                                     │
          qa ◄── optimize mouth ◄── render ◄─────────┘
           │
           └─► đạt: ghi vào hồ sơ, giao  ·  trượt: avatar-quality → sửa đúng một thứ → dựng lại
```

1. **Kiểm máy:** trạm là thư mục `VIDEO_STATION`, hoặc dựng bằng `video-studio init` (skill `video-routing`). Rồi `video-studio avatar doctor --json`. Mã 3: đọc `engines.<tên>.reason`. Đã được giao cài thì làm theo tài liệu cài, chưa thì báo người dùng.
2. **Clip nền:** người mới **luôn bắt đầu bằng tự quay** 10–20 giây bằng điện thoại, theo checklist ở [avatar-profile](references/avatar-profile.md). Cách này có ngay avatar mà không gửi mặt đi đâu. Công cụ tạo video AI chỉ là phương án thêm khi cần bối cảnh, trang phục hay cử chỉ khác.
3. **Chuẩn hoá** (bỏ tiếng, 25 fps, cắt gần đầu tới ngực, trong giới hạn 1280×720):
   ```
   video-studio avatar optimize --task normalize --input <clip-gốc> --crop W:H:X:Y --out <clip-sẵn>.mp4 --json
   ```
   Khung vuông quanh đầu tới ngực (ví dụ `720:720:0:180` trên khung 720×1280) cho mặt lớn nhất, khớp tốt nhất.
4. **Hồ sơ:** `video-studio avatar profile list <từ khoá>` để tìm hồ sơ cũ. Ảnh gốc và ảnh khung chép tay vào `avatars/<id>/anchor/` (chưa có lệnh). Chưa có hồ sơ thì tạo:
   ```
   video-studio avatar profile new <id> --name "<tên>" --relation self|consented --consent-quote "<nguyên văn>" --scope "<phạm vi>" --clip <clip-sẵn> --voice <profile-giọng> --crop W:H:X:Y
   ```
   Chưa có giọng clone: bỏ `--voice`, dùng WAV tự thu, hoặc dựng profile giọng theo skill `voice-routing` rồi `profile update --voice`.
5. **Dựng:**
   ```
   video-studio avatar render --profile <id> --audio <giọng.wav> --out <ls>.mp4 --json
   ```
   - Mặc định `--engine latentsync`, guidance 2,5, 30 bước. Đo trên RTX 4070: 224–939 giây cho 10 giây video. Chạy nền.
   - `--engine musetalk` (kèm `--bbox-shift -10..-15`): bản nháp khoảng 2 phút, miệng còn hé khi im lặng.
   - WAV tối đa 60 giây (MuseTalk 30 giây, bắt buộc mono 16 kHz PCM16: đổi bằng lệnh ở [avatar-voice](references/avatar-voice.md) mục 3). Bài dài: cắt theo câu, dựng từng đoạn, nối ở bước dựng video.
   - **Gấp, chưa có hồ sơ:** được dùng `--source <clip-sẵn>` thay cho `--profile`, sau khi người dùng xác nhận clip là mặt của chính họ (hoặc người đã đồng ý). Lập hồ sơ sau khi giao.
6. **Làm nét miệng** (chỉ sau LatentSync):
   ```
   video-studio avatar optimize --task mouth --input <ls>.mp4 --out <ls-net>.mp4 --strength 0.85
   ```
   Khẩu hình "o", "u" bị khép bớt thì hạ `--strength` xuống 0,6.
7. **Kiểm:** `video-studio avatar qa --video <ls-net>.mp4 --profile <id> --json`, rồi soi 3 mốc (luật 3). Lệnh có `--profile` thì kết quả được ghi vào lịch sử QA của hồ sơ.
8. **Giao:** đường dẫn MP4 trong trạm, điểm SyncNet, engine và tham số đã dùng, những gì chưa kiểm.

## Tái dùng về sau

Lần sau chỉ cần hồ sơ và một WAV mới: `profile list` → `render --profile` → `optimize --task mouth` → `qa --profile`.
- Đổi clip, giọng hay tham số: `avatar profile update <id> …`. Clip đổi thì mã băm đổi theo, phải soi lại.
- Người trong hình rút đồng ý: `avatar profile revoke <id>`. Từ đó không render được nữa. Hỏi người dùng có xoá thư mục hồ sơ trong trạm không; agent không tự xoá.

## Giấy phép

Khoá học bán tiền: đọc mục "Nguồn và quyền sử dụng" của `docs/LATENTSYNC.md` và `docs/MUSETALK.md`, cùng giấy phép engine giọng, **trước khi phát hành**. Gắn nhãn video có dùng AI nếu nền tảng đăng yêu cầu.
