---
name: video-long-to-shorts
description: "Turn a finished long video into a set of 9:16 shorts or reels rebuilt from its own source (narration, avatar takes, icons): propose short ideas, cut voice at measured points, design balanced vertical infographic layouts with animated icons, get still frames approved, then render and QA. Use when asked to make shorts, reels or vertical clips from a long video, and right after a long video is delivered, to offer shorts. Not for cropping footage only (video-edit), news shorts from a spec (video-routing), or storyboarding a new long video (vlog-design)."
metadata:
  version: "0.1.0"
  studio_status: "draft"
---

# Video dài → loạt short / reel 9:16

> **Kết luận:** từ **một video dài đã xong** (composition HyperFrames + giọng + take avatar + bộ icon) ra **≥ 3 short dọc 1080×1920 dựng lại từ nguồn**, qua hai cổng người: **Cổng 1** chọn ý tưởng, **Cổng 2** duyệt ảnh tĩnh (lặp sửa tới khi đạt) rồi mới render. Chuẩn rút từ một đợt dựng tay ba short đã được chủ kênh duyệt.

## Luật cứng

1. **Lời chỉ lấy nguyên từ nguồn, có mã dòng.** Mỗi câu trong short dẫn mã dòng/từ của `source-map.json`; không viết lời mới, không tạo giọng mới. Cần lời mới là việc khác (`voice-routing`), hỏi người dùng trước.
2. **Chữ màn hình không thêm khẳng định.** Chỉ ba loại chữ: phụ đề (nguyên văn), hook mở đầu (câu hỏi hoặc ý có trong lời), thẻ kết. Con số, tính từ, lời hứa không có trong lời gốc thì không lên hình.
3. **Mọi ý thành logo hoặc icon động, không chip chữ.** Icon chính của câu có ≥ 2 thành phần bên trong tương tác; icon nối nhau có liên kết chạy ([motion-icons](references/motion-icons.md)).
4. **Chỉ hiện logo hãng được nhắc tên, đúng lúc nói.** Không lặp một asset hai lần trong một khung; không lặp một kiểu chuyển động quá 2 cảnh liền.
5. **Bố cục cân đối, lấp đầy vùng hoạt họa** theo bộ mẫu infographic dọc ([vertical-layout](references/vertical-layout.md)); khung có video/ảnh lồng thì chỉ còn media đó, phụ đề và avatar nhỏ.
6. **Hai cổng người, không tự qua.** Chưa có lời chọn ý tưởng thì không cắt giọng; chưa có lời duyệt ảnh tĩnh (trích nguyên văn) thì không render bản giao. Im lặng không phải duyệt.
7. **Không tải, không tạo asset mới, không gọi dịch vụ hay agent hãng khác** khi người dùng chưa cho phép trong phiên. Thiếu icon thì ghi `ICON-GAPS.md` và hỏi.
8. Dữ liệu tập (bản đồ nguồn, giọng cắt, ảnh tĩnh, file render) nằm trong trạm, không ghi vào repo. Không đăng short: gói đăng dừng ở file và chữ.

## Khi nào dùng

- Dùng: «làm short/reel/clip dọc từ video này», «cắt video dài thành short», «đóng gói lại cho TikTok/Reels/Shorts».
- **Tự đề nghị:** vừa giao xong một video dài (từ `vlog-design`, `video-storyboard-design` hoặc bản dựng HyperFrames) → hỏi một câu: «Có muốn đóng gói thành short không?» kèm **≥ 3 ý tưởng** chấm theo [selection-rubric](references/selection-rubric.md). Người dùng từ chối thì dừng, không hỏi lại trong phiên.
- Không dùng: chỉ có mp4, cần cắt khung và chèn phụ đề (`video-edit`); bản tin short từ spec (`video-routing` → `render`); storyboard video dài mới (`vlog-design`); viết HTML/GSAP của composition (`hyperframes`).

## Quy trình (chi tiết: [workflow](references/workflow.md))

| Bước | Ra file (trong project short ở trạm) | Xong khi |
|---|---|---|
| 0 Hỏi và nhận nguồn | — | người dùng muốn làm short; có đường tới composition nguồn |
| 1 Bản đồ nguồn | `source-map.json` | `scripts/source_map.py` thoát 0, hoặc 1 với cảnh báo đã ghi cách bù |
| 2 Đề xuất ý tưởng | `SHORTS-PLAN.md` (mẫu `assets/templates/SHORTS-PLAN.md`) | ≥ 3 ứng viên có điểm rubric, mã dòng, mốc, tỉ lệ avatar |
| **Cổng 1** | lời chọn trong `SHORTS-PLAN.md` | người dùng chốt short nào, thứ tự, nhạc, tên được nhắc |
| 3 Cắt giọng + phụ đề | `beats-plan.json` → `voice.wav`, `beats.json`, `subs.json` | `cut_voice.py` thoát 0; `make_subs.py --asr` thoát 0 |
| 4 Thiết kế hình | bảng beat → icon → bố cục trong `SHORTS-PLAN.md`, `ICON-GAPS.md` | mỗi ý có icon + tương tác bên trong + mẫu bố cục; chỗ thiếu đã hỏi |
| 5 Dựng khung + ảnh tĩnh | `index.html`, `layout.json`, `stills/contact.png` | `gap_scan.py` thoát 0; bảng ảnh mỗi cụm phụ đề một khung |
| **Cổng 2** | lời duyệt (nguyên văn) | người dùng duyệt ảnh tĩnh; chưa đạt thì sửa, đánh số vòng, gửi lại |
| 6 Render + QA | `out/<mã>.mp4` | `qa_short.py` thoát 0; người nghe điểm cắt, xem trên điện thoại |
| 7 Gói đăng | `PUBLISH.md` | tiêu đề, mô tả, CTA, nợ còn mở; không tự đăng |

Hỏng ở bước nào thì sửa tại bước đó rồi chạy lại kiểm của bước, không nhảy qua. Dựng **một short tới hết Cổng 2 trước**, rồi mới làm các short còn lại: chuẩn hình chốt ở short đầu.

## Tài liệu đi kèm (đọc khi tới bước tương ứng)

| File | Đọc khi | Nội dung |
|---|---|---|
| [workflow](references/workflow.md) | trước bước 0 | từng bước: đầu vào, đầu ra, lệnh, lỗi thường gặp |
| [source-contract](references/source-contract.md) | bước 1 | hợp đồng `source-map.json`, `beats.json`, `subs.json`; nguồn không phải HyperFrames |
| [selection-rubric](references/selection-rubric.md) | bước 2 | trục, trọng số, tiêu chí loại, công thức số lượng |
| [audio-cut-and-sync](references/audio-cut-and-sync.md) | bước 3 | bản đồ audio nhiều clip, mốc lệch, điểm cắt, fade, avatar giữa take, âm lượng |
| [vertical-layout](references/vertical-layout.md) | bước 4–5 | khung 1080×1920, vùng an toàn, phụ đề, avatar, bộ mẫu bố cục V0–V9 |
| [motion-icons](references/motion-icons.md) | bước 4–5 | icon động tương tác thành phần, liên kết chạy, tách lớp, khi nào xin icon mới |
| [qa-checklist](references/qa-checklist.md) | bước 5–6 | cổng tự động, `layout.json`, mắt và tai người, rà 0,5 s |
| [example-short](references/example-short.md) | lần đầu dùng | một short mẫu trung tính: beat, bố cục, chuyển động, kết quả kiểm |

## Mẫu và script

- `assets/templates/`: `SHORTS-PLAN.md`, `beats.json` (plan cắt giọng), `ICON-GAPS.md`, `short-frame.html` (khung 1080×1920: nền, vùng hoạt họa, avatar tròn, dải phụ đề; màu và font qua biến CSS).
- `scripts/source_map.py <index.html> --out source-map.json`: section, audio, video (`data-start`, `data-media-start`), dòng và từ karaoke, mốc từ theo lệnh GSAP.
- `scripts/cut_voice.py --source-map … --plan … --media-root … --out voice.wav --beats-out beats.json`: ghép đoạn giọng qua bản đồ nhiều clip, fade cos, đệm, tính offset avatar.
- `scripts/make_subs.py --source-map … --beats … --asr … --out subs.json`: cụm 3–5 từ, chữ từ nguồn, mốc từ nhận dạng giọng.
- `scripts/gap_scan.py <layout.json>`: rà mỗi 0,5 s khoảng trống, lệch, lặp asset, khung media, lặp kiểu chuyển động.
- `scripts/qa_short.py <short.mp4>`: khung, fps, thời lượng, LUFS, true peak, lời vào ≤ 0,5 s.

Mã thoát chung: `0` đạt · `1` có lỗi hoặc cảnh báo cần xử lý · `2` gọi sai / đầu vào sai (sửa, đừng thử lại) · `3` thiếu ffmpeg (chỉ `qa_short.py`). `--json` thì dòng cuối stdout là một object JSON. Python 3.9+, thư viện chuẩn; nhận dạng giọng và đo bề rộng chữ bằng font thật là công cụ của trạm, không thuộc script.

## Gotchas

- Mốc chữ karaoke của bản dài **không phải** mốc giọng: đã đo lệch 0,1–0,7 s, lớn nhất ở clip giọng ghép sau. Điểm cắt và phụ đề lấy mốc từ nhận dạng giọng trên chính file âm.
- Bản dài có nhiều clip `<audio>` (cùng file, `data-media-start` khác nhau): không bao giờ dùng một offset chung.
- Short lấy lời từ đoạn không có avatar thì cần bố cục không avatar; tỉ lệ giây có avatar là một trục của rubric.
- Icon nguồn nhỏ phóng lớn bị mềm; đổi màu bằng bộ lọc xoay sắc cho ra màu ngoài bảng màu kênh. Phân vai bằng màu bệ/quầng trong bảng màu và đạo cụ.
- Khe năng lượng thấp giữa lời liền có thể là âm tắc của phụ âm, không phải ranh từ: luôn cho nhận dạng giọng đọc lại chữ đầu đoạn sau khi cắt.
- Kênh có `channels/<kênh>/STYLE-GUIDE.md` thì màu, font, nền, nhạc, cổng tên nội bộ của kênh thắng số mặc định ở đây.

## Tiêu chí hoàn thành

Mỗi short: lời nguyên văn có mã dòng; `gap_scan` và `qa_short` thoát 0; lời duyệt ảnh tĩnh của người dùng được trích; đã nêu phần **chưa kiểm** (chưa có người nghe điểm cắt giữa lời, chưa xem trên điện thoại, giấy phép nhạc chưa xác minh) trong `PUBLISH.md`. `NOT_CHECKED` không phải đạt.
