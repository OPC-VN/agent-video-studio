---
name: vlog-design
description: "Turn a script, raw clips and an idea into a full storyboard and asset kit for a teaching or storytelling explainer that mixes a presenter or avatar, screen recordings and animation. Use when planning such a video's layouts, visuals, text motion and scene transitions before building. Not for single-mode storyboards such as news, lyric or pure footage edits (video-storyboard-design)."
metadata:
  version: "0.1.0"
  studio_status: "draft"
---

# Video kể chuyện / giảng dạy: người + màn hình + hoạt họa

> **Kết luận:** từ **lời thoại + clip thô + ý tưởng** ra **storyboard có mã mẫu + manifest tài nguyên + khung hình chính đã duyệt**, theo thư viện ngữ pháp học từ 5 video mẫu. Skill thiết kế, không dựng: dựng giao cho `hyperframes`, `video-edit`, giọng cho `voice-routing`.

## Luật cứng

1. **Học ngữ pháp, không chép hình.** Lấy vị trí, nhịp, kiểu chuyển; hình vẽ và vật thể tự làm hoặc lấy nguồn mở có giấy phép ([asset-sourcing](references/asset-sourcing.md)). Dấu ấn riêng của mẫu (ruy băng thương hiệu, toà nhà LED số chương, hạt → chữ pixel → chữ có chân) chỉ lấy nguyên lý, bắt buộc đổi hình thức.
2. **Không bịa cảnh quay thật.** Không có clip người thì dùng avatar có lời đồng ý trong hồ sơ, hoặc bố cục không người; ghi rõ.
3. **Khung hình chính là cổng duyệt.** Chưa có người dùng duyệt (bước 6) thì không dựng cả video.
4. Tải hay tạo tài nguyên, gọi dịch vụ tạo ảnh là thao tác ra ngoài: chỉ khi người dùng cho phép trong phiên.
5. Dữ liệu tập (lời thoại, clip, khung hình) nằm trong trạm, không ghi vào repo.

## Khi nào dùng

- Dùng: lên storyboard, chọn bố cục, hình, hiệu ứng chữ, chuyển cảnh cho video giảng dạy, chia sẻ cộng đồng, vlog kiến thức, kể chuyện có người dẫn hoặc avatar, quay màn hình và hoạt họa.
- Ranh giới: video **trộn** người/avatar + màn hình + hoạt họa, cần nhịp chế độ và manifest → skill này; storyboard một chế độ hoặc chung → `video-storyboard-design`.
- Không dùng: chỉ cắt/dọn footage (`video-cleanup`, `video-edit`); bản tin từ spec (`video-routing`); phân tích một video mẫu mới (`video-reference-analysis`); viết code composition (`hyperframes`).

## Quy trình (chi tiết: [workflow](references/workflow.md))

| Bước | Ra file | Xong khi |
|---|---|---|
| 0 Kiểm đầu vào | `brief.md` | đủ mục, chỗ thiếu ghi «chưa có» |
| 1 Kiểm kê clip thô | `clips.md` | mỗi beat có nguồn hình hoặc nằm trong danh sách cần quay |
| 2 Bảng beat | `beats.md` | tổng giây khớp mục tiêu ±10%, mọi beat có loại ý |
| 3 Chế độ + nhịp | `pacing.md` | `scripts/pace_check.py` thoát 0 hoặc cảnh báo có lý do |
| 4 Thiết kế cảnh | `STORYBOARD.md` (mẫu `assets/templates/storyboard.md`) | mỗi thẻ cảnh đủ trường [B], mã có trong `pattern-index.md` |
| 4b Giọng + take avatar | mục 4–5 storyboard | mỗi câu có mã V + marker sắc thái; mỗi take ≤ 60 s |
| 5 Bộ tài nguyên | `assets/MANIFEST.md` | mỗi dòng có nguồn, giấy phép, trạng thái; ID `AS..` khớp storyboard |
| 5b Gói xuất bản | mục 7 storyboard | chương YouTube, tiêu đề, mô tả, thumbnail, end screen, cảnh cắt short |
| 6 Khung hình chính | `KEYFRAMES/` | người dùng duyệt (trích nguyên văn) |
| 7 Bàn giao dựng | mục 8 storyboard | người dựng bắt tay không phải hỏi lại |

Đầu ra cuối là **một** `STORYBOARD.md`; các file trên là bước trung gian. Ví dụ điền sẵn: [example-storyboard](references/example-storyboard.md).

Hỏng ở bước nào thì sửa tại bước đó rồi chạy lại kiểm của bước, không nhảy qua.

## Thư viện (đọc khi tới bước tương ứng)

- [pattern-index](references/pattern-index.md) — đọc **trước**: mọi mã, một dòng mỗi mã, độ tin, trạng thái.
- [library-contract](references/library-contract.md) — khuôn 9 trường, độ tin, mã video, chế độ, luật thêm/gộp mã. Thư viện lớn dần khi học thêm video qua skill `video-reverse-engineer` (gói mẫu + `library-merge.md`).

- [layout-library](references/layout-library.md) — bước 3–4: bố cục LY, vùng an toàn, phối người + màn hình + hoạt họa, tỉ lệ chế độ.
- [transitions-mode-switch](references/transitions-mode-switch.md) — bước 3–4: chuyển cảnh TR, ma trận chuyển giữa các chế độ, biên đạo theo 0.1 s.
- [visual-vocabulary](references/visual-vocabulary.md) — bước 4–5: vật thể, icon, hình người VO; chuyển động giữa khối MO.
- [text-and-infographic-motion](references/text-and-infographic-motion.md) — bước 4: hiệu ứng chữ TX, dựng infographic/sơ đồ IG.
- [idea-to-visual](references/idea-to-visual.md) — bước 2 và 4: loại ý, thiết bị kể chuyện ST, công thức RC ý → hình.
- [audio-patterns](references/audio-patterns.md) — bước 4–4b: nhạc nền, SFX, khoảng lặng AU.
- Chuẩn chuyển động/bố cục explainer có avatar (icon động, liên kết chạy, chữ không chạm, nền, âm lượng): `video-storyboard-design` → `references/motion-layout-standard.md`. Kênh có `channels/<kênh>/STYLE-GUIDE.md` thì luật kênh thắng thư viện bố cục chung.
- [asset-sourcing](references/asset-sourcing.md) — bước 5: nguồn icon, người, ảnh, font, màu, motion và giấy phép.

## Mẫu và script

- `assets/templates/`: `brief.md`, `clip-inventory.md`, `beat-sheet.md`, `pacing.md`, `storyboard.md` (storyboard sản xuất 8 mục: thiết kế, bản đồ cảnh, bảng giọng, take avatar, thẻ cảnh, xuất bản, kế hoạch dựng), `scene-card.md` (quan hệ với mẫu chung), `asset-manifest.md`.
- `scripts/build_index.py [--check]`: sinh / kiểm `pattern-index.md` từ thư viện.
- `scripts/pace_check.py <pacing.md> [--profile presenter|animation] [--index references/pattern-index.md] [--json]`: kiểm theo bảng ngưỡng chung ở workflow bước 3 (tỉ lệ người, P, người vắng, cảnh liền cùng bố cục, độ dài cảnh, khoảng đổi chế độ, rời toàn khung bằng cắt, mã LY, hở/chồng). Thoát 0 đạt · 1 lỗi nhịp · 2 không đọc được bảng. Python 3.9+, thư viện chuẩn.

## Gotchas

- Người toàn khung cắt cứng sang màn hình trông vụng: co người thành PIP (TR-03) hoặc mờ chéo qua blur (TR-02).
- Sơ đồ hiện một lần là mất nhịp: khối hiện theo lời, đường nối vẽ sau khi khối đích đã có.
- Font thiếu dấu tiếng Việt chỉ lộ khi render: thử glyph ở bước 5.
- Mốc thời gian storyboard là ước lượng; căn lại cue sau khi có audio thật.

## Tiêu chí hoàn thành

Đủ 7 file ở bảng trên trong project của trạm, `pace_check` đạt, manifest không dòng thiếu nguồn, khung hình chính đã được duyệt; báo rõ phần chưa kiểm (chưa nghe audio, chưa render đủ).

**Sau khi video dài đã dựng và giao xong:** hỏi người dùng có muốn đóng gói thành short 9:16 không, kèm ≥ 3 ý tưởng cắt từ lời gốc; đồng ý thì chuyển skill `video-long-to-shorts`.
