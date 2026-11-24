# Quy trình: video dài đã xong → ý tưởng → ảnh tĩnh → short 9:16

> **Kết luận:** tám bước, hai cổng người. Việc đắt nhất là sửa sau render, nên mọi quyết định về nội dung chốt ở Cổng 1 và mọi quyết định về hình chốt bằng ảnh tĩnh ở Cổng 2.

## Contents
- Đầu vào và cây thư mục
- Bước 0 — Hỏi và nhận nguồn
- Bước 1 — Bản đồ nguồn
- Bước 2 — Đề xuất ý tưởng, Cổng 1
- Bước 3 — Cắt giọng và phụ đề
- Bước 4 — Thiết kế hình
- Bước 5 — Dựng khung và ảnh tĩnh, Cổng 2
- Bước 6 — Render và QA
- Bước 7 — Gói đăng
- Thời lượng máy đã đo
- Lỗi theo vòng và luật phòng ngừa

## Đầu vào và cây thư mục

| Đầu vào | Bắt buộc | Ghi chú |
|---|---|---|
| Composition nguồn (`index.html` HyperFrames của bản dài) | có | chỉ đọc; không sửa project bản dài |
| File giọng và take avatar mà composition trỏ tới | có | WAV PCM 16-bit; avatar thường là webm có alpha |
| Bộ icon / logo của kênh | nên có | thiếu thì ghi `ICON-GAPS.md` |
| Chuẩn hình kênh (màu, font, nền, nhạc) | nên có | `channels/<kênh>/STYLE-GUIDE.md` thắng số mặc định |
| Chỉ có mp4 | — | ngoài phạm vi: chuyển `video-edit` (cắt khung + phụ đề) |

```text
<trạm>/projects/<mã-tập>-shorts/
  source-map.json            ← bước 1
  SHORTS-PLAN.md             ← bước 2, 4 (kế hoạch + lời chọn Cổng 1)
  <SH-A>/
    beats-plan.json          ← bước 3 (điểm cắt đã đo)
    voice.wav · beats.json · asr-words.json · subs.json
    ICON-GAPS.md             ← bước 4
    tools/build_html.py      ← bước 5: sinh index.html + layout.json (không sửa tay HTML)
    index.html · layout.json · assets/
    stills/contact-v1.png …  ← giữ mọi vòng
    out/<SH-A>.mp4           ← bước 6
    PUBLISH.md               ← bước 7
```

`<skill>` dưới đây là thư mục skill này trong repo; script chạy từ repo, dữ liệu nằm ở trạm.

## Bước 0 — Hỏi và nhận nguồn

Sau khi giao video dài, hỏi **một** câu kèm ý tưởng, không tự làm:

> «Video dài đã xong. Có muốn đóng gói thành short 9:16 không? Ba ý tưởng cắt từ bản gốc: (1) … (2) … (3) … Khuyến nghị bắt đầu bằng (n) vì …»

Ý tưởng lúc này là ước lượng nhanh từ lời thoại (tên, đoạn, độ dài); bảng điểm đầy đủ làm ở bước 2 sau khi người dùng nói có. Người dùng từ chối → dừng.

Người dùng tự yêu cầu làm short thì bỏ câu hỏi, đi thẳng bước 1.

## Bước 1 — Bản đồ nguồn

```text
python <skill>/scripts/source_map.py <nguồn>/index.html --out source-map.json --json
```

- Class dòng/từ khác mặc định thì truyền `--line-class`, `--word-class`; avatar nhận theo `--avatar-class` hoặc `data-role="avatar"`.
- Mã 1 = thiếu audio, thiếu từ, hoặc từ thiếu mốc: ghi cách bù (mốc từ lấy bằng nhận dạng giọng ở bước 3) rồi đi tiếp. Mã 2 = sai đường/sai file.
- Kiểm kê từ bản đồ, ghi đầu `SHORTS-PLAN.md`: bảng clip giọng (id, khoảng timeline, file, `media_start`), bảng take avatar và **các khoảng không có avatar**, tổng số dòng.
- Nguồn không phải HyperFrames: tự viết bộ chuyển ra đúng [hợp đồng](source-contract.md) ở trạm; bộ chuyển riêng của một tập không vào repo.

## Bước 2 — Đề xuất ý tưởng, Cổng 1

1. Quét lời theo dòng, gom các đoạn 15–60 s đứng được một mình (có thể ghép 2–5 đoạn không liền nhau nếu cùng một ý).
2. Chấm theo [selection-rubric](selection-rubric.md); loại ứng viên dính tiêu chí loại.
3. Viết `SHORTS-PLAN.md` từ mẫu: mỗi ứng viên có bảng beat (mã dòng đầu–cuối, mốc timeline, lời nguyên văn rút gọn bằng «…», take avatar), hook, thẻ kết, điểm, rủi ro.
4. Trình **≥ 3** ứng viên (công thức số lượng ở rubric), có khuyến nghị thứ tự.

**Cổng 1 — người dùng chốt:** short nào, thứ tự; có nhạc nền không (kèm rủi ro giấy phép); cho phép nhắc tên hãng/sản phẩm nào; cho phép tạo icon mới hay chỉ dùng kho có sẵn. Ghi lời chọn nguyên văn và ngày vào đầu `SHORTS-PLAN.md`. Người dùng đổi chủ đề thì kiểm lại luật «không thêm khẳng định»: chữ màn hình chỉ dùng ý có trong lời.

## Bước 3 — Cắt giọng và phụ đề

Chi tiết đo và ngưỡng: [audio-cut-and-sync](audio-cut-and-sync.md).

1. Chạy nhận dạng giọng (công cụ offline của trạm) trên **file giọng nguồn** quanh từng beat để có mốc từ thật; tìm điểm cắt theo thứ tự ưu tiên khoảng lặng → trũng năng lượng.
2. Ghi `beats-plan.json` từ mẫu `assets/templates/beats.json`: `tl_in`/`tl_out` **đã chỉnh**, `first_word`/`last_word`, `clip` khi cần, `gap_after`.
3. Cắt:
   ```text
   python <skill>/scripts/cut_voice.py --source-map source-map.json --plan SH-A/beats-plan.json \
     --media-root <nguồn> --out SH-A/voice.wav --beats-out SH-A/beats.json --json
   ```
   `beats.json` có `short_in`/`short_out` từng đoạn và `avatar.media_start` (đặt vào `data-media-start`).
4. Nhận dạng giọng lại trên `voice.wav` → `asr-words.json` dạng `[[start, end, "từ"], …]`; kiểm chữ đầu mỗi đoạn đúng lời nguồn.
5. Phụ đề:
   ```text
   python <skill>/scripts/make_subs.py --source-map source-map.json --beats SH-A/beats.json \
     --asr SH-A/asr-words.json --out SH-A/subs.json --json
   ```
   Không có `--asr` thì mã 1 và chỉ dùng cho nháp. Đo bề rộng cụm bằng font thật ở bước 5.

## Bước 4 — Thiết kế hình

Với mỗi beat lập bảng năm cột trong `SHORTS-PLAN.md`:

| Lời (mốc trong short) | Ý | Icon / logo | Tương tác bên trong + liên kết | Mẫu bố cục |
|---|---|---|---|---|

- Icon vào đúng lúc **từ khoá** được đọc (mốc từ `subs.json`), không gõ cứng.
- Chọn mẫu bố cục V0–V9 ở [vertical-layout](vertical-layout.md); đổi mẫu theo mạch ý, không quá 2 cảnh liền cùng kiểu chuyển động.
- Đối chiếu kho icon: ý nào không có icon hợp → dòng trong `ICON-GAPS.md` (ý, icon tạm, đề xuất). Không dùng icon «gần đúng» cho ý chính mà không báo.
- Cần icon/logo mới: hỏi người dùng trước; cách xin tấm icon ở [motion-icons](motion-icons.md).
- Hook (0–2 s) và thẻ kết: soát luật «không thêm khẳng định».

## Bước 5 — Dựng khung và ảnh tĩnh, Cổng 2

1. Viết `tools/build_html.py` của short: đọc `beats.json` + `subs.json`, sinh `index.html` (từ `assets/templates/short-frame.html`) **và** `layout.json`. Không sửa tay HTML đã sinh; sửa script rồi chạy lại. Luật composition theo skill `hyperframes` và mục «Tất định kỹ thuật» của `video-storyboard-design/references/motion-layout-standard.md`.
2. `python <skill>/scripts/gap_scan.py SH-A/layout.json --json` phải thoát 0; cảnh báo thì sửa hoặc ghi lý do.
3. Lint composition, rồi chụp khung tĩnh bằng công cụ snapshot của engine: **mỗi cụm phụ đề đổi ý một khung**, thêm khung giữa các lần đổi bố cục; ghép bảng thumbnail có nhãn giây → `stills/contact-vN.png`.
4. Tự soi theo [qa-checklist](qa-checklist.md) trước khi gửi.

**Cổng 2 — gửi bảng ảnh tĩnh + danh sách nợ** (icon còn ở mức sàn, icon tạm, chỗ chưa đo). Người dùng góp ý → sửa script → vòng mới `v2`, `v3`…, giữ bảng ảnh các vòng để so. Chỉ sang bước 6 khi có lời duyệt; trích nguyên văn vào `PUBLISH.md`.

Short đầu tiên qua Cổng 2 xong mới dựng các short sau, dùng lại hàm dựng icon, phụ đề, avatar của nó.

## Bước 6 — Render và QA

```text
video-studio render --project-dir <SH-A> --out <SH-A>/out
python <skill>/scripts/qa_short.py <SH-A>/out/<SH-A>.mp4 --json
```

- Âm: giọng + một clip nhạc nền (nếu được chọn) + master về mức đăng; số ở [audio-cut-and-sync](audio-cut-and-sync.md). Short dài hơn trần vì lời gốc dài thì nới `--max-dur` và ghi lý do, không cắt cụt câu.
- Sau cổng tự động: mục «mắt và tai người» của [qa-checklist](qa-checklist.md). Việc chưa có người làm ghi «chưa kiểm».

## Bước 7 — Gói đăng

`PUBLISH.md` mỗi short: tiêu đề (≤ 60 ký tự, không thêm khẳng định), mô tả 1–2 câu + CTA về bản dài (link để trống nếu bản dài chưa đăng), hashtag, tên hãng được nhắc và lời cho phép, nguồn + giấy phép nhạc, số đo QA, lời duyệt Cổng 2, danh sách chưa kiểm. **Không tự đăng**; đăng là việc của người dùng hoặc pipeline marketing.

## Thời lượng máy đã đo

Một máy trạm Windows có GPU, engine HyperFrames 0.9.88, short 40–70 s: render nháp ≈ 1–1,7 phút; chụp 14–34 khung tĩnh ≈ 20 s; một tấm 12 icon bằng công cụ sinh ảnh ≈ 7 phút. Máy khác thì đo lại, không chép số.

## Lỗi theo vòng và luật phòng ngừa

| Lỗi bị bắt khi duyệt | Luật phòng ngừa |
|---|---|
| Nhiều chip chữ, chỉ một hình động | mọi ý thành icon/logo động; chữ chỉ còn phụ đề, hook, thẻ kết |
| Avatar to chiếm chỗ | avatar tròn nhỏ, góc dưới trái hoặc giữa theo bố cục |
| Phụ đề lơ lửng giữa khung | phụ đề sát đáy, trên vùng giao diện nền tảng |
| Icon tạm cho ý không có icon | `ICON-GAPS.md` + hỏi trước khi tạo |
| Icon dồn 1/4 trên, giữa khung trống, có khung trống hẳn | bộ mẫu bố cục dọc; `gap_scan` rà 0,5 s; icon vào lớn rồi thu về lưới |
| Đổi màu icon ra ngoài bảng màu | phân vai bằng màu bệ/quầng trong bảng màu + đạo cụ |
| Khoảng thưa khi liệt kê | ô chờ nét đứt hiện trước, tới lời thì lắp vào |
| Hiện logo hãng không được nhắc | chỉ logo hãng có trong lời của beat, đúng lúc nói; «nền tảng khác» dùng icon chung |
| Icon phụ không liên quan lời | icon phụ cũng sinh từ lời của beat |
| Hai icon giống nhau trong một khung | `gap_scan` báo lặp asset |
| Icon chỉ sáng lên, không «sống» | ≥ 2 thành phần bên trong tương tác; liên kết chạy |
