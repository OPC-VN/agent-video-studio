# Hồ sơ avatar: đồng ý, clip nền, chuẩn hoá, tái dùng

Một hồ sơ = một người + một clip nền đã duyệt + tham số đã chốt. Tất cả nằm trong trạm, ở `<trạm>/avatars/<id>/`:

```
avatars/<id>/
├─ avatar.json   hồ sơ máy đọc (lệnh `avatar profile` ghi, đừng sửa tay)
├─ PROFILE.md    ghi chú người đọc: mẫu ở cuối trang này
├─ anchor/       ảnh gốc, ảnh khung đầu/cuối
├─ clips/        clip gốc và clip đã chuẩn hoá
├─ qa/           ảnh khung đã soi, ghi chú QA
└─ renders/      bản dựng
```

## 1. Đồng ý: làm trước mọi thứ

| Trường hợp | Làm gì |
|---|---|
| Chính người dùng | `--relation self`. Câu đồng ý chính là lời người dùng trong chat, ví dụ "dùng mặt tôi cho bài giảng". |
| Người khác, đã có lời đồng ý bằng văn bản (tin nhắn, email, giấy ký) | `--relation consented`. Chép **nguyên văn** câu đồng ý vào `--consent-quote`, ghi phạm vi vào `--scope`. Bản gốc (ảnh chụp tin nhắn) để trong `anchor/`. |
| Người khác, chưa có lời đồng ý, hoặc chỉ có lời người dùng kể lại | **Dừng.** Đưa người dùng mẫu tin nhắn để xin đồng ý (bên dưới). Chưa có thì không quay, không dựng, không tạo hồ sơ. |
| Ảnh lấy từ mạng xã hội, ảnh công khai, người nổi tiếng, người đã mất | **Từ chối**, kể cả "bản nháp". Lối ra: người đó tự gửi clip và lời đồng ý, dùng avatar của chính người dùng, hoặc dùng nhân vật minh hoạ. |
| Trẻ em | Cần đồng ý của cha mẹ hoặc người giám hộ, theo đúng quy trình trên. |

Mẫu tin nhắn xin đồng ý (người dùng tự gửi):
> "Mình muốn dùng hình ảnh và giọng của bạn để làm avatar AI nói trong [phạm vi, ví dụ: video bài giảng nội bộ]. Video chỉ dùng cho [phạm vi], không dùng quảng cáo. Bạn có thể rút lại bất cứ lúc nào. Bạn đồng ý không?"

Phạm vi là giới hạn cứng. Muốn dùng ngoài phạm vi (bán khoá học, quảng cáo) thì phải xin lại. Người đó rút lại thì chạy `avatar profile revoke <id>`.

## 2. Clip nền: người mới tự quay trước

Đây là đường mặc định: có avatar ngay, không gửi mặt lên dịch vụ nào, giữ danh tính chuẩn nhất.

**Checklist quay bằng điện thoại (10–20 giây):**
- **Khung:** đầu tới ngực, mặt chiếm khoảng 30–40 % chiều cao khung, nhìn thẳng ống kính, lệch ≤ 15°.
- **Miệng khép suốt clip, không nói.** Chớp mắt, thở, gật nhẹ một lần là đủ.
- Tay để dưới khung hình hoặc ở ngực, **không bao giờ lên quá cằm**.
- Điện thoại đặt trên giá, không cầm tay. Không zoom, không lia.
- **Sáng:** đứng trước cửa sổ hoặc đèn mềm, không ngược sáng, không bóng gắt dưới mũi.
- **Nền:** trơn, không có người hay ảnh người phía sau.
- Không đeo kính phản sáng. Không để râu, tóc hay khẩu trang che môi.
- Quay 1080p, 25 hoặc 30 fps. Quay 3 bản, chọn bản ổn định nhất.
- Muốn có cử chỉ: quay thêm clip riêng với động tác chậm kiểu đưa tay lên, giữ, hạ xuống (MuseTalk phát xuôi rồi ngược, động tác nhanh sẽ lộ).

Chép clip vào `avatars/<id>/clips/` (bản local, không dùng bản chỉ có trên cloud), rồi chuẩn hoá.

## 3. Chuẩn hoá và chọn khung cắt

```
video-studio avatar optimize --task normalize --input clips/goc.mp4 --crop W:H:X:Y --out clips/san-sang.mp4
```

- Lệnh tự bỏ tiếng, đưa về 25 fps, H.264, cắt theo `--crop` và thu nhỏ vào giới hạn 1280 cạnh dài, diện tích ≤ 1280×720.
- **Chọn crop:** khung vuông quanh đầu tới ngực, cằm nằm khoảng 60 % chiều cao khung. Ví dụ clip dọc 720×1280 có đầu ở phần trên thì dùng `720:720:0:180`. Mở một khung bằng trình xem ảnh để đo toạ độ.
- Mặt lớn thì khẩu hình rõ: LatentSync dựng vùng mặt ở 256 px, mặt nhỏ trong khung rộng sẽ nhoè.
- Cần cả khung rộng: dựng trên bản cắt gần, rồi ghép lại vào khung rộng ở bước dựng video (lớp phủ). Cách này chưa đo trong repo; soi kỹ viền ghép.

## 4. Phương án thêm: công cụ tạo video AI

Dùng khi cần bối cảnh, trang phục hay cử chỉ mà tự quay khó làm. Áp được cho mọi nền tảng có chế độ **ảnh đầu / ảnh cuối** (start/end frame, frames-to-video, image-to-video).

**Luật:**
- Người dùng tự tải ảnh lên. Agent chỉ soạn prompt (luật 2 của skill).
- Ảnh đầu **=** ảnh cuối **=** một ảnh khung gốc. Clip sẽ khép vòng, mặt khó trôi.
- Ảnh khung gốc ưu tiên ảnh thật chụp đúng bố cục. Ảnh do AI vẽ lại phải được chính người trong hình xác nhận là giống.
- Tạo 3–4 bản, chọn bản giữ mặt giống nhất **và** miệng khép suốt clip.
- Đọc điều khoản nền tảng về ảnh người thật và watermark trước khi dùng cho sản phẩm.

**Prompt A: chuyển động tối thiểu (dùng trước)**
```text
Animate this exact photograph with minimal, natural movement. Keep the person's face, identity, hairstyle, skin, clothing, lighting, framing and background exactly as in the image, with no changes.

The person looks calmly into the camera with lips gently closed for the entire clip. They do not speak and their mouth does not move. They blink naturally two or three times, breathe softly so the chest rises very slightly, and the head stays centered and still, with at most a barely perceptible slow nod. The video starts and ends on exactly this pose.

Locked-off tripod shot: no camera movement, no zoom, no pan, no cut. Photorealistic, sharp focus on the face, consistent exposure.

Audio: silence, no dialogue, no music.
```

**Prompt B: có cử chỉ giảng bài.** Thay `[GESTURE]` bằng một dòng ở bảng dưới, mỗi clip một cử chỉ.
```text
Animate this exact photograph. Keep the person's face, identity, hairstyle, skin, clothing, lighting and background exactly as in the image. The camera framing stays the same.

They are a calm, confident lecturer explaining an idea, but their lips stay gently closed the whole time: they do not speak and their mouth does not move, as if pausing thoughtfully between sentences. Eyes stay on the camera, natural blinks, small centered head movements.

[GESTURE]

Hands always stay below the chin, at chest level, and never cover or touch the face, mouth or chin. Hands are anatomically correct with five fingers, moving smoothly and slowly. The clip starts and ends on exactly the pose in the image, with hands out of frame.

Locked-off tripod shot: no camera movement, no zoom, no pan, no cut. Photorealistic, sharp focus on the face.

Audio: silence, no dialogue, no music.
```

| Cử chỉ | `[GESTURE]` |
|---|---|
| giải thích | `Both hands rise into frame from below to chest height with open palms, make two gentle explanatory movements, hold for a moment, then lower out of frame.` |
| liệt kê | `The right hand rises to chest height and counts one, two, three on the fingers with calm pauses, then lowers out of frame.` |
| chỉ sang slide | `The right hand rises to chest height and makes a smooth open-palm gesture toward the side of the frame, holds briefly, then lowers out of frame.` |
| nhấn mạnh | `Both hands meet at chest height with fingertips touching, then open outward slightly in a confident gesture, then lower out of frame.` |

**Danh sách tránh** (dán vào ô negative prompt nếu nền tảng có):
```text
talking, lip movement, mouth opening, smile, teeth, face change, different person, morphing, hairstyle change, clothing change, background change, hand covering mouth, hand touching face, extra fingers, fused fingers, camera movement, zoom, text, logo, flicker
```

**Ảnh khung gốc quá hẹp** (ví dụ cần 16:9 từ ảnh dọc): dùng công cụ sửa ảnh, lệnh `Extend this photo to a 16:9 canvas. Keep the person, face, clothing and lighting exactly unchanged; extend only the background and shoulders naturally.` Kiểm vai, áo không méo.

Clip tải về đặt trong `clips/`, rồi chuẩn hoá như mục 3.

## 5. Tiêu chí duyệt clip nền

| # | Kiểm | Đạt khi |
|---|---|---|
| 1 | Giống người thật | người quen nhận ra ngay; mắt, mũi, tóc không lệch |
| 2 | Miệng | khép suốt clip, không mấp máy |
| 3 | Một mặt | đúng một khuôn mặt ở mọi khung, không có ảnh người ở nền |
| 4 | Tay | không khung nào tay lên quá cằm; đủ 5 ngón, không dính ngón |
| 5 | Máy quay | đứng yên; khung đầu gần giống khung cuối |
| 6 | Lặp | xem 3 vòng xuôi–ngược không thấy giật ở điểm đổi chiều |
| 7 | Vật thể lạ | không có chữ, logo, người phụ |

Đạt cả 7 thì mới `avatar profile new --clip` (hoặc `profile update --clip`). Lệnh ghi mã băm của clip; clip bị sửa sau đó thì render từ chối cho tới khi duyệt lại.

## 6. Mẫu `PROFILE.md` (ghi chú người đọc, để trong thư mục hồ sơ)

```markdown
# Avatar <id>

| Mục | Giá trị |
|---|---|
| Người trong hình | <tên hiển thị> — chính người dùng / đã đồng ý |
| Đồng ý | "<nguyên văn>" · phạm vi: <…> · ngày: <…> · bản gốc: anchor/<file> |
| Clip nền | clips/<file> — tự quay / công cụ AI <tên> · ngày duyệt |
| Khung cắt | W:H:X:Y |
| Engine | latentsync · guidance 2.5 · 30 bước · seed 1247 · miệng 0.85 |
| Giọng | profile <tên> ở voice-studio · speed 1.0 |

## Biến thể
| Mã | Bối cảnh | Trang phục | Khung | Clip |
|---|---|---|---|---|

## Ghi chú QA
<ngày> · <bản dựng> · SyncNet <x,xx> / lệch <n> · soi: <…>
```

Không ghi mô tả sinh trắc học (tỉ lệ khuôn mặt, đặc điểm nhận dạng) vào bất kỳ file nào ngoài trạm.
