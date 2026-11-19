# Chữ động, giọng đọc và ghép âm thanh (khâu 6–8, đã chạy thật)

## 1. Lớp phủ và chữ (draft 2)

`assets/build_draft2.example.py` + `assets/draft2_template.html` dựng một composition HyperFrames từ **dữ liệu hiệu ứng** (một danh sách `FX`), không viết tay từng phần tử:

| Loại | Việc | Quy tắc |
|---|---|---|
| `path` | ranh/đường vẽ dần (glow + nét) | toạ độ từ `osm_overlay.svg_paths`; chỉ trên ảnh top-down |
| `pin` | ghim đỏ + vòng sóng | vòng lặp **hữu hạn** (3 lần) |
| `dash` | đường nét đứt tới địa điểm (mặt nạ vẽ dần) | chim bay; điểm cuối vàng |
| `tag` | nhãn 2 dòng «tên / X,XX km chim bay» | `tags_layout` sắp theo y, cách ≥ 124 px; **kẹp trong khung** bằng bề rộng ước lượng (`len(l1)*27`), nếu không `check` báo `canvas_overflow` |
| `card` | thẻ số (số đếm lên, chú thích, nguồn) | host là **layer riêng phủ cả khoảng thẻ** (`kind="layer"`): đặt thẻ ở layer của một cảnh ngắn thì thẻ biến mất khi cảnh hết |
| `text` / `type` | chữ pop / gõ từng ký tự, `[từ khoá]` đổi cam | chữ chính **1/3 trên**; dòng nguồn ≥ 28 px, không viền, bóng đổ |

- Mỗi cảnh = một **host**: nhóm `g` (ảnh + svg + nhãn cùng transform, cho cảnh MapLibre) hoặc `img`/`video` kèm `layer` phủ. Lớp phủ nằm trong host nên zoom/pan của ảnh không làm lệch.
- Font nhúng bằng `@font-face` (Montserrat 800/900, OFL, có tiếng Việt); đặt trong `assets/` của project; đặt `FONT_DIR` khi chạy.
- Sau khi dựng: `npx hyperframes@<bản ghim> check --strict` rồi `video-studio render --project-dir … --out <thư mục NGOÀI project>`.

## 2. Giọng đọc (voice-studio)

1. **Viết lại lời cho engine** (`voice-routing/references/vietnamese-tts-script.md`): số viết bằng chữ, tên tiếng Anh **phiên âm tiếng Việt** (Ê-cô-pác, Cu-su-mi, Vin-com Ô-sần Xi-ti), từ viết tắt dính số thì chèn từ thường. Tránh câu quá ngắn đứng riêng; gộp.
2. **Một câu = một file** theo cảnh: `assets/voice_batch.example.py` nạp engine **một lần** (nạp ≈ 50 s mỗi lần gọi CLI), ghim seed, thu từng câu; nếu dài hơn thời lượng cảnh thì **tự tăng tốc** (tối đa ×1,3) rồi thu lại. Ra `manifest.json` (bắt đầu, thời lượng cho phép, thời lượng thật, tốc độ).
3. Chạy bằng **python của venv engine** (`<runtime>/venvs/agent-voice-studio/omnivoice/…/python`) với `VOICE_STATION=<trạm giọng>`; python hệ thống thường thiếu `torch`.
4. **Kiểm bằng ASR ngược** (`faster-whisper` `small`, `language=vi`): đo tỉ lệ khớp từ giữa lời và bản nhận dạng. Đã đo: câu thường 0,74–1,00; câu có **tên tiếng Anh phiên âm** và **số thập phân** yếu (0,22–0,60). ASR cỡ nhỏ cũng nghe sai tên riêng («Hưng Yên»), nên điểm thấp chỉ là cờ để **người nghe lại**, không kết luận.
5. Profile giọng là của người dùng (`<profile-của-bạn>` mặc định của trạm); **chỉ dùng giọng của chính người dùng hoặc giọng đã đồng ý**.

## 3. Nhạc nền và ghép

- `voice-studio bgm list` / `bgm pick <style>` lấy file từ kho nhạc của trạm (mặc định `calm-corporate`, âm lượng 0,10); dự án khác chọn style theo giọng điệu. Nhạc phải có quyền dùng.
- Ghép bằng ffmpeg: mỗi câu `adelay=<ms>|<ms>` đúng giây bắt đầu cảnh; `amix=normalize=0` rồi `loudnorm=I=-16:TP=-1.5:LRA=9` cho giọng; nhạc `volume=0.11`, `afade` vào 1,2 s ra 2,5 s, `atrim` đúng độ dài; trộn giọng + nhạc `amix=duration=first`; video `-c:v copy`, âm `-c:a aac -b:a 192k`.
- Kiểm: `ffprobe` thấy 2 luồng, độ dài = video; nghe thử **bằng tai người** trước khi bàn giao (máy không kết luận được giọng «tự nhiên»).

## 4. Điều chưa kiểm

Tên tiếng Anh phiên âm đọc có đúng ý người Việt nghe không; nhiều profile/giọng khác nhau; ghép âm thanh ở macOS; thời lượng TTS thật so với bảng «tiếng/giây» của storyboard ở mọi dự án (phải đo lại mỗi dự án).
