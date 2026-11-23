# Quy trình: lời thoại + clip thô + ý tưởng → storyboard → bộ tài nguyên → sẵn sàng dựng

> **Kết luận:** đi đúng 8 bước (kèm 4b bảng giọng + take avatar và 5b gói xuất bản), mỗi bước ra một file trong project của trạm; bước 6 (khung hình chính) là cổng người duyệt trước khi tốn công dựng cả video.

## Contents
- Đầu vào và cây thư mục project
- Bước 0 — Kiểm đầu vào
- Bước 1 — Kiểm kê clip thô
- Bước 2 — Bảng beat
- Bước 3 — Kế hoạch chế độ và nhịp
- Bước 4 — Thiết kế cảnh
- Bước 4b — Bảng giọng + take avatar
- Bước 5 — Bộ tài nguyên
- Bước 5b — Gói xuất bản
- Bước 6 — Khung hình chính (cổng duyệt)
- Bước 7 — Bàn giao dựng
- Lỗi thường gặp

## Đầu vào và cây thư mục project

| Đầu vào | Bắt buộc | Dạng |
|---|---|---|
| Lời thoại | có | `.docx`, `.md`, `.txt`; tiếng Việt hoặc song ngữ |
| Ý tưởng / brief | có | vài câu: người xem, thông điệp, hành động sau xem, độ dài |
| Clip thô | không | thư mục: cảnh người nói, quay màn hình, cảnh nền (b-roll) |
| Bộ kênh | nên có | màu, font, logo, hồ sơ avatar, tên profile giọng |

Project nằm trong trạm (`video-studio` chọn trạm; không ghi vào repo):

```text
<trạm>/projects/<mã-tập>/
  brief.md          ← bước 0
  clips.md          ← bước 1
  beats.md          ← bước 2
  pacing.md         ← bước 3 (bảng nhịp, kết quả pace_check)
  STORYBOARD.md     ← bước 4, 4b, 5b (mẫu storyboard sản xuất, 8 mục)
  assets/MANIFEST.md, assets/icons/, assets/images/, assets/fonts/  ← bước 5 (dãy ID AS01…)
  assets/voice/ (WAV từng câu V), assets/takes/ (take avatar), assets/music/, assets/sfx/, assets/thumb/  ← bước 4b, 5, 5b
  KEYFRAMES/        ← bước 6
  build/            ← bước 7 (composition HyperFrames)
```

## Bước 0 — Kiểm đầu vào

- Làm: đọc lời thoại trọn vẹn; viết `brief.md` từ [mẫu brief](../assets/templates/brief.md): người xem, mục tiêu, thông điệp một câu, độ dài, định dạng (16:9 mặc định), bộ kênh, quyền dùng mặt/giọng, điều chưa biết.
- Xong khi: brief đủ mục, mọi chỗ thiếu ghi «chưa có» kèm cách bù.
- Dừng nếu: dùng mặt hay giọng một người thật mà chưa có lời đồng ý trong hồ sơ avatar/giọng → hỏi người dùng.

## Bước 1 — Kiểm kê clip thô

- Làm: với mỗi clip chạy `video-studio cleanup inspect --input <clip> --json`; clip có lời thì lấy transcript (skill `video-reference-analysis`, mục transcript). Ghi `clips.md` theo [mẫu](../assets/templates/clip-inventory.md): loại (người nói / màn hình / nền), đoạn dùng được (từ–đến), khung hình người (toàn thân, nửa người, cận), nền (sạch, cần tách nền), chất lượng tiếng.
- Không có clip: ghi rõ; người nói thay bằng avatar dựng bằng skill `avatar-create` hoặc bố cục không người; màn hình thì lập **shot list cần quay** (thao tác, độ dài, độ phân giải, ẩn thông tin riêng).
- Xong khi: mỗi beat sau này có nguồn hình hoặc nằm trong danh sách cần quay/tạo.

## Bước 2 — Bảng beat

- Làm: chia lời thoại thành beat theo [mẫu](../assets/templates/beat-sheet.md). Một beat = một ý người xem phải hiểu, 1–3 câu, ≈ 6–15 s. Ước thời lượng: tiếng Việt đọc thường ≈ 4 âm tiết/giây (**ước, chưa đo**: đo lại từ transcript có mốc hoặc audio giọng của kênh rồi ghi vào brief). Từ ngoại đếm theo cách đọc (Excel = 2, AI = 2, email = 2). Câu móc (hook) mở đầu 3–5 s được làm beat riêng ngắn hơn 6 s.
- Gán **loại ý** cho mỗi beat theo [idea-to-visual](idea-to-visual.md) (giới thiệu, đặt vấn đề, khái niệm, quy trình, so sánh, số liệu, công cụ, demo, chuyện kể, cảnh báo, kết luận, CTA) và gạch chân **danh từ cụ thể** sẽ thành hình.
- Gom beat thành chương (3–6 chương cho video 10–15 phút); mỗi chương mở bằng một câu hỏi hoặc tiêu đề.
- Xong khi: tổng thời lượng ước khớp mục tiêu ±10%, mọi beat có loại ý.

## Bước 3 — Kế hoạch chế độ và nhịp

- Làm: gán chế độ hình cho từng beat: **P** người toàn khung · **PA** người + hoạt họa/slide · **A** hoạt họa · **S** màn hình · **PS** người + màn hình · **AS** hoạt họa trên màn hình. Luật chọn ở [layout-library](layout-library.md), mục phối người + màn hình + hoạt họa.
- **Bảng ngưỡng chung** (nguồn duy nhất; file thư viện chỉ ghi số quan sát và trỏ về đây; sửa trong brief nếu kênh muốn khác):

| Ngưỡng | Hồ sơ `presenter` (có người dẫn/avatar) | Hồ sơ `animation` (thiên hoạt họa) | Căn cứ |
|---|---|---|---|
| Người xuất hiện P + PA + PS | 60–90% (trần 90% để chừa chỗ cho hoạt họa/màn hình «thở»; video < 2 phút được nới `--person-max 95`, ghi lý do) | 30–60% | E ≈ 89%, D ≈ 99% |
| P (người toàn khung, kể cả chữ nổi) | ≤ 15% | ≤ 15% | E 11.2%, D ≈ 2% |
| Người vắng mặt liên tục | ≤ 60 s (cảnh báo) | không kiểm | E, D |
| Khoảng giữa hai lần đổi chế độ | ≤ 45 s (cảnh báo) | ≤ 45 s | E ≈ 11 s, D ≈ 31 s |
| Cảnh liền cùng mã LY | ≤ 3 (lỗi; với S/PS/AS chỉ cảnh báo vì demo dài là bình thường) | như trái | D chạy LY-05 liền 05:18–07:58 |
| Cảnh không có chuyển động mới | ≤ 20 s (cảnh báo) | ≤ 20 s | E 2–8 s, PS tới 24 s |
| Rời toàn khung P → PA/PS bằng TR-01 | cảnh báo (nên TR-03) | — | E, D tr 6.8 |

  - Mỗi chương mở bằng thẻ chương (LY-11) hoặc câu hỏi lớn (LY-13). Video < 3 phút hoặc mục < 30 s: thay thẻ chương bằng pill bước «N/tổng» (TX-09) đặt trong cảnh, không dựng cảnh chương riêng.
  - Cột TR ghi một mã chính; chuyển ghép ghi `TR-03+TR-07`.
  - Một beat thường tách 1–3 cảnh; ghi mã beat ở cột `Beat` của bảng nhịp.
- Ghi bảng vào `pacing.md` rồi chạy `python scripts/pace_check.py <project>/pacing.md --profile presenter` (hoặc `animation`); sửa đến khi không còn lỗi, hoặc ghi lý do giữ.
- Xong khi: `pace_check` thoát 0 hoặc mọi cảnh báo có lý do.

## Bước 4 — Thiết kế cảnh

- Làm: mỗi beat chọn một công thức RC ở [idea-to-visual](idea-to-visual.md), rồi chốt:
  - bố cục LY ([layout-library](layout-library.md)), vị trí người/màn hình/khối chữ;
  - hình VO và chuyển động khối MO ([visual-vocabulary](visual-vocabulary.md));
  - chữ TX và cách dựng infographic IG ([text-and-infographic-motion](text-and-infographic-motion.md));
  - chuyển cảnh TR vào và ra ([transitions-mode-switch](transitions-mode-switch.md)).
- Viết `STORYBOARD.md` theo **[mẫu storyboard sản xuất](../assets/templates/storyboard.md)** (8 mục; thẻ cảnh ở mục 6). Mẫu chung của trạm (`../video-routing/assets/storyboard.md`) chỉ là tham chiếu tinh thần, không điền; quan hệ hai mẫu ở [scene-card](../assets/templates/scene-card.md). Mục 4 (bảng giọng) và 5 (take avatar) điền ở bước 4b ngay sau đây; mục 7 (gói xuất bản) ở bước 5b.
- Luật: mỗi cảnh **một điểm nhìn chính**; chữ trên hình ≤ 7 từ mỗi khối, giữ ≥ 1.5 s + 0.35 s/từ (ngưỡng chung); mọi thứ của bước tương lai ẩn trước cue lời; biên đạo neo vào **mã câu V**, không neo vào giây tuyệt đối khi đã có bảng giọng.
- Storyboard ≤ 15 cảnh được gộp các trường [G] (Âm, Caption, 9:16, QA); trường [B] không bỏ.
- Xong khi: mọi cảnh có đủ trường [B] của thẻ mục 6 và mã LY/VO/TX/IG/TR; không ô trống không giải thích.

## Bước 4b — Bảng giọng + take avatar

- Làm (thiết kế, luôn làm được): viết lại lời thoại thành **kịch bản nói** theo `voice-routing` (`references/vietnamese-tts-script.md`): chuẩn hoá số phiên bản, giờ, ngày, tên miền, từ ngoại ngữ; gắn marker từ manifest của profile theo bảng «Phân bổ sắc thái theo bố cục video»; đánh mã câu `V001…`, gán câu vào cảnh, ước nghỉ sau. Điền mục 4 của storyboard gồm bảng phân bổ marker (số câu, %) và tick kiểm theo luật.
- Làm (thiết kế): xếp câu V thành take avatar ≤ 60 s mỗi take, cắt ở chỗ nghỉ giữa câu, chốt crop clip nền và cảnh dùng. Điền mục 5. Ghi fps dựng ở mục 1; khác 25 thì ghi cách quy đổi.
- Làm (chạy thật, **chỉ khi người dùng giao và hồ sơ có lời đồng ý** mặt/giọng; tạo giọng hay take là thao tác ra ngoài theo luật cứng 4): tổng hợp giọng qua `voice-routing` → ASR nghe lại → điền «giây đo» và file WAV → tính lại mốc cảnh mục 3 → `video-studio avatar render` / `optimize` / `qa` theo `docs/LATENTSYNC.md` (chạy nền, 224–939 s cho 10 s giọng); điền điểm QA mục 5.
- Chưa chạy được: ghi «chưa đo / chưa chạy» ở các cột tương ứng; mốc vẫn là ước.
- Xong khi: mỗi câu thoại có mã V, marker và cảnh; phân bổ marker đạt luật hoặc có lý do; mỗi câu V thuộc đúng một take (hoặc «—, bố cục không người»); mọi take ≤ 60 s. Nếu đã chạy thật: mốc cảnh đã tính lại từ giây đo và take đạt QA (lệch 0, tin cậy ≥ 7).

## Bước 5 — Bộ tài nguyên

- Làm: quét toàn bộ thẻ cảnh, lập `assets/MANIFEST.md` theo [mẫu](../assets/templates/asset-manifest.md): icon, hình người, vật thể, ảnh, font, màu, motion component, clip cần quay, take người cần ghi.
- Lấy nguồn theo [asset-sourcing](asset-sourcing.md): một họ icon, một phong cách nhân vật, font có đủ dấu tiếng Việt; ảnh AI chỉ khi không có nguồn mở, prompt khoá phong cách chung (màu, nét, góc nhìn, nền).
- Tải hay tạo tài nguyên là thao tác ra ngoài: chỉ làm khi người dùng đã cho phép trong phiên; ghi nguồn + giấy phép từng dòng.
- Manifest dùng **một dãy ID `AS01…`** chung với storyboard; thêm loại giọng, nhạc, SFX, thumbnail, take avatar. Mọi ID trong thẻ cảnh, bảng giọng, bảng take, gói xuất bản phải có dòng trong manifest.
- Xong khi: mọi dòng manifest có trạng thái (có sẵn / cần tải / cần tạo / cần quay / cần người duyệt) và nguồn; không ID mồ côi hai phía.

## Bước 5b — Gói xuất bản

- Làm: điền mục 7 của storyboard: chương YouTube (mốc + tên), tiêu đề (2 phương án), mô tả (2 dòng đầu = thông điệp + CTA; nguồn/giấy phép nhạc), thumbnail (khung nguồn + chữ ≤ 4 từ), end screen 5–20 s, CTA, danh sách cảnh cắt short (mỗi short ≤ 60 s, hook mới ở 3 s đầu, bố cục 9:16 theo mục 6).
- Mốc chương dựa mốc cảnh: còn là ước thì ghi «ước, cập nhật sau khi ghép»; chương đầu bắt đầu `0:00`.
- Video chỉ để nội bộ / chưa đăng: ghi «—, chưa xuất bản» và lý do.
- Xong khi: mọi trường mục 7 có nội dung hoặc «—» kèm lý do; thumbnail và end screen có asset ID trong manifest.

## Bước 6 — Khung hình chính (cổng duyệt)

- Làm: dựng 6–9 ảnh tĩnh 1920×1080 cho các bố cục chính (mở đầu, thẻ chương, người + slide, màn hình + PIP, sơ đồ, số liệu, kể chuyện) bằng HyperFrames (skill `hyperframes`), xuất PNG + một ảnh ghép.
- Tự xem từng ảnh: chữ chồng chữ, tràn mép, tương phản, vùng phụ đề, khuôn mặt bị che. Sửa rồi mới gửi.
- Gửi người dùng chọn: nền chủ đạo, giữ/bỏ/sửa từng khung. **Chưa được duyệt thì không dựng cả video.**
- Xong khi: người dùng duyệt (trích nguyên văn vào `KEYFRAMES/REVIEW.md`).

## Bước 7 — Bàn giao dựng

- Làm: chuyển storyboard thành việc dựng: composition HyperFrames theo chương (skill `hyperframes`), render qua `video-studio render`; giọng đọc qua skill `voice-routing` của repo giọng (kịch bản có nhãn sắc thái theo profile kênh); cắt clip người qua `video-edit`.
- Ghi trong `STORYBOARD.md` mục 8 (kế hoạch dựng): thứ tự giọng → đo mốc → take → composition theo chương → ghép → caption → QA, phụ thuộc (audio trước khi căn cue, quy đổi fps), cảnh cần thử trước, rủi ro, điều chưa kiểm.
- Xong khi: người dựng (người hoặc agent) có thể bắt tay mà không phải hỏi lại.

## Lỗi thường gặp

- Học video mẫu rồi **chép hình**: chỉ học ngữ pháp (vị trí, nhịp, kiểu chuyển); vật thể và hình vẽ phải tự làm hoặc từ nguồn mở.
- Người nói chiếm cả video: video mẫu có người chỉ để P thuần 0–11%; còn lại người ở PIP hoặc cột bên.
- Cắt cứng người toàn khung sang màn hình: dùng TR-03 (co thành PIP) hoặc TR-02.
- Sơ đồ hiện cả một lần: dựng từng khối theo lời, đường nối vẽ sau khi khối đích đã hiện.
- Font không có dấu tiếng Việt: kiểm glyph ở bước 5, không đợi tới lúc render.
- Căn cue theo giây ước khi đã có (hoặc sắp có) WAV: neo biên đạo vào mã câu V, tính lại mốc sau khi đo.
- Một take lip-sync dài hơn 60 s hoặc cắt giữa câu: chia lại ở chỗ nghỉ, mỗi take ≤ 60 s.
- Dựng ở fps khác 25 mà để trình dựng tự nội suy take avatar: môi–tiếng có thể lệch; quy đổi có chủ đích và kiểm lại.
- Gắn marker lên câu không hợp cho đủ 8 sắc thái, hoặc đặt `gan-gui` liền sau `tram-lang`: xem luật phân bổ ở `voice-routing`.
- ID asset viết rời trong thẻ cảnh mà không có dòng manifest (hoặc ngược lại): giữ một dãy `AS01…`.
