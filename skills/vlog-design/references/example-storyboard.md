# Ví dụ storyboard sản xuất điền sẵn (rút gọn)

> **Kết luận:** đây là ví dụ điền theo [`storyboard.md`](../assets/templates/storyboard.md) cho một video hướng dẫn 90 s «giao báo cáo tuần cho trợ lý AI», rút còn **4 cảnh** (P mở đầu, PA, PS demo, P kết CTA) nhưng đủ cả 8 mục. Rút gọn từ một lượt chạy thử, viết chung: không tên người, kênh, sản phẩm thật; mọi số giây là **ước** (≈ 4 âm tiết/giây, chưa đo bằng audio); chưa nghe, chưa render, chưa chạy lip-sync. Dùng để xem **độ chi tiết mỗi trường**, không để chép nội dung.

## Contents
1. Brief và quyết định · 2. Thiết kế chung · 3. Bản đồ cảnh · 4. Bảng giọng · 5. Bảng take avatar · 6. Thẻ cảnh · 7. Gói xuất bản · 8. Kế hoạch dựng

Ví dụ ở dạng gộp (storyboard ≤ 15 cảnh): trường [G] Âm, Caption, 9:16, QA mỗi trường một dòng.

## 1. Brief và quyết định

| Trường | Nội dung |
|---|---|
| Trạng thái · người quyết · nguồn | nháp bước 4; người dùng quyết; nguồn `brief.md`, `beats.md`, `pacing.md` |
| Người xem · vấn đề · thông điệp · hành động | nhân viên văn phòng đã quen Excel/slide, chưa dùng trợ lý AI cho báo cáo · mất cả buổi sáng viết báo cáo tuần · giao việc cho trợ lý AI trong 3 bước và không bỏ bước kiểm · lấy file yêu cầu mẫu ở phần mô tả |
| Chiến dịch | không thuộc chiến dịch (tập thử) |
| Định dạng | 16:9, 1920×1080, 90 s mục tiêu (đoạn trích ≈ 37 s); short 9:16: có |
| Hồ sơ avatar · đồng ý | `avatar-A` · «có» (giả định theo lời người dùng, cần đối chiếu hồ sơ thật trước khi tạo take) |
| Profile giọng · đồng ý · marker | `voice-A` · chưa có lời đồng ý trong phiên → chưa tạo giọng · 8 marker theo manifest (chưa đọc manifest thật) |
| fps dựng so với 25 fps lip-sync | dựng 25 fps cho khớp take, không quy đổi (**chưa kiểm** giới hạn của trình dựng ở 25) |
| Sự thật · giả định | «3 giờ → 20 phút» là số tác giả, hiện kèm nhãn «ước tính»; màn hình dùng giao diện giả (mock), không logo thật |
| Hướng kể | (a) **3 đoạn PS liền, pill «N /3» thay thẻ chương — KHUYẾN NGHỊ** vì mỗi bước ≈ 10 s, thẻ chương rời bị luật nhịp cấm cho mục < 30 s; (b) thẻ chương LY-11 trước mỗi bước: ranh giới rõ hơn nhưng thêm ≈ 9 s |

## 2. Thiết kế chung

| Trường | Nội dung |
|---|---|
| Nhịp cảm xúc | hook câu hỏi → nỗi đau → hứa 3 bước → demo → cảnh báo → CTA |
| Màu · font | nền tối ấm, chữ kem, **một** màu nhấn cam; xanh lá chỉ cho «đạt», đỏ chỉ cho «sai». Font tiêu đề Be Vietnam Pro, mono JetBrains Mono (glyph «Ả Ẫ Ặ Ể Ỗ Ợ Ữ ỹ đ Đ»: **chưa thử**) |
| Chữ | ≤ 7 từ mỗi khối; giữ ≥ 1.5 s + 0.35 s/từ; vào blur→nét (TX-01), ra trước đổi cảnh 0.3 s |
| Vùng an toàn 16:9 | lề 5%, phụ đề y 84–95% (theo `layout-library` §1) |
| Vùng an toàn 9:16 | 1080×1920: chừa 12% trên và 18% dưới cho giao diện nền tảng; phụ đề y 62–72%; vùng cắt giữa 1080×1080 từ 16:9 |
| Khung người duy nhất | squircle một hình thể; PIP luôn dưới-trái 14% rộng; PA dùng squircle 40% hoặc cột phải; P toàn khung chỉ ở mở và kết |
| Màn hình | UI giả, con trỏ ≥ 2% khung, không thông tin riêng |
| Âm | nhạc nền một loop, **−18 dB dưới giọng**, hạ thêm −6 dB trong 300 ms khi giọng vào sau khoảng lặng; một họ SFX «click mềm + whoosh ngắn»; không nhạc ở 4 s đầu |
| Nguồn thiết kế | `assets/MANIFEST.md` (AS01–AS09 bên dưới) |

## 3. Bản đồ cảnh

| Cảnh | Từ–đến | Chương | Chế độ | LY | TR vào | Marker chủ đạo | Ý người xem phải hiểu |
|---|---|---|---|---|---|---|---|
| C01 | 0:00–0:09 | 1 | P | LY-01 | TR-10 | `hao-hung` | viết báo cáo tuần mất bao lâu, và có cách khác |
| C02 | 0:09–0:16 | 1 | PA | LY-02 | TR-03 | `giai-thich` | cách cũ = mở nhiều file, chép tay, viết lại |
| C03 | 0:16–0:25 | 2 | PS | LY-05 | TR-02 | `trung-tinh` | bước 1: gom nguồn vào một thư mục, trợ lý chỉ đọc trong đó |
| C04 | 0:25–0:37 | 3 | P | LY-01 | TR-04 | `nhan-manh` → `gan-gui` → `tram-lang` | không bỏ bước kiểm; lấy file mẫu ở mô tả |

## 4. Bảng giọng

| Mã câu | Cảnh | Marker | Lời TTS đã chuẩn hoá | Nghỉ sau (s) | Giây ước → giây đo | File WAV |
|---|---|---|---|---|---|---|
| V001 | C01 | `hao-hung` | Mỗi sáng thứ Hai, bạn mất bao lâu để viết báo cáo tuần? | 0.4 | 3.5 → *chưa đo* | AS04 *(chưa có)* |
| V002 | C01 | `gan-gui` | Chào bạn, hôm nay mình chỉ cho bạn cách giao việc đó cho trợ lý AI. | 0.5 | 4.3 → *chưa đo* | AS04 *(chưa có)* |
| V003 | C02 | `giai-thich` | Với nhiều người, đó là cả buổi sáng: mở năm file Excel, chép số sang slide, rồi viết lại những việc đã làm. | 0.5 | 6.3 → *chưa đo* | AS04 *(chưa có)* |
| V004 | C03 | `trung-tinh` | Bước một: bạn tạo một thư mục duy nhất và kéo ba file nguồn vào đó. | 0.4 | 4.0 → *chưa đo* | AS04 *(chưa có)* |
| V005 | C03 | `nhan-manh` | Chỉ đọc những gì có trong thư mục này, không đọc gì khác. | 0.5 | 3.3 → *chưa đo* | AS04 *(chưa có)* |
| V006 | C04 | `nhan-manh` | Nhớ một điều: không bao giờ bỏ bước kiểm trước khi gửi. | 0.4 | 3.0 → *chưa đo* | AS04 *(chưa có)* |
| V007 | C04 | `gan-gui` | Nếu bạn muốn file yêu cầu mẫu mình dùng, mình để ở phần mô tả. | 0.4 | 3.8 → *chưa đo* | AS04 *(chưa có)* |
| V008 | C04 | `tram-lang` | Hẹn gặp lại bạn ở tập sau, chúc bạn một tuần làm việc nhẹ nhàng. | 0.5 | 3.8 → *chưa đo* | AS04 *(chưa có)* |

Ghi chú chuẩn hoá: «Excel», «slide», «AI» để nguyên theo bảng đo của `voice-routing`; không có số phiên bản, giờ, ngày, tên miền nên không đổi chữ; không có mảnh câu ngắn đứng riêng. Thứ hai/«file» chưa kiểm bằng ASR.

**Phân bổ marker** (8 câu của đoạn trích; video đủ 90 s ≈ 30 câu sẽ phân bổ lại):

| Marker | Số câu | % | Ghi chú |
|---|---|---|---|
| `trung-tinh` | 1 | 12,5 | V004 |
| `giai-thich` | 1 | 12,5 | V003 |
| `gan-gui` | 2 | 25 | V002 (chào sau câu móc), V007 (CTA) |
| `nhan-manh` | 2 | 25 | V005, V006 |
| `hao-hung` | 1 | 12,5 | V001 |
| `ke-chuyen` | 0 | 0 | đoạn trích không có; bản đủ cần một ví dụ ngắn |
| `hoi-dap` | 0 | 0 | V001 là câu hỏi nhưng dùng làm câu móc |
| `tram-lang` | 1 | 12,5 | V008 (gồm câu chào cuối) |

Kiểm theo luật:
- [x] Video ngắn (< 3 phút): 6 marker ≥ 5; `hao-hung` ở mở, `tram-lang` ở kết. *(Đoạn trích; bản đủ phải xét lại.)*
- [x] Không marker > 35%; `trung-tinh` + `giai-thich` = 25% ≤ 60%.
- [x] Không đoạn > 5 câu liền; V005→V006 cùng `nhan-manh` nhưng khác cảnh (chỉ 2 câu liền).
- [x] `gan-gui` (V007) đứng **trước** `tram-lang` (V008), không liền sau.
- [ ] Mọi marker có trong manifest thật: **chưa kiểm** (chưa đọc manifest của profile).

## 5. Bảng take avatar

| Mã take | Câu V (từ–đến) | Dài (s) | Crop (W:H:X:Y) | Cảnh dùng | Trạng thái | Điểm QA (SyncNet) |
|---|---|---|---|---|---|---|
| TK01 | V001–V008 | ≈ 36 (ước, gồm nghỉ) ≤ 60 | 720:720:0:180 (ví dụ; chốt sau khi xem clip nền) | C01–C04 (toàn khung ở C01, C04; squircle ở C02; PIP ở C03) | chưa chạy | *chưa* |

Một take duy nhất vì tổng < 60 s và mọi cảnh dùng cùng người đang nói; mỗi cảnh cắt đoạn theo mốc giây trong take. Cắt ở các khoảng nghỉ sau V002, V003, V005. Mức đạt: lệch 0, tin cậy ≥ 7. Chưa chạy lip-sync: **chưa có điểm**.

## 6. Thẻ cảnh

### Cảnh C01 — Câu hỏi mở · 0:00–0:09 · chương 1

**Mã mẫu:** Chế độ P · LY-01 · VO-18 · MO: — · TX-16+TX-01 · IG: — · TR vào TR-10 / ra TR-03 · RC-01 · AU: không nhạc

**Câu V + marker:** V001 `hao-hung` · V002 `gan-gui`

**Chữ trên hình + giữ:** kicker «BÁO CÁO TUẦN» + headline «Mất bao lâu?» (3 từ, giữ ≥ 2.6 s)

**Người / màn hình / hoạt hoạ:** TK01 0–9 s, avatar toàn khung lệch trái; chữ nổi bên phải; không màn hình.

**Biên đạo theo giây:**

| Giây | Neo (câu V · từ khoá) | Đối tượng, vị trí đầu → cuối | Hành động · thời lượng · easing | Giữ yên / chưa hiện |
|---|---|---|---|---|
| 0.0 | — | dải nhấn cam: ngoài khung → quét chéo | 0.2 s, power3.inOut, lộ avatar | chữ chưa hiện |
| 0.6 | V001 · «Mỗi sáng» | kicker, phải trên | blur→nét 0.3 s | headline chưa hiện |
| 0.9 | V001 · «bao lâu» | headline, phải giữa | vào 0.3 s | — |
| 3.6 | hết V001 | kicker + headline | mờ ra 0.3 s | avatar giữ |

**Asset ID:** AS03 (take TK01), AS06 (dải nhấn, tự vẽ SVG) · **Âm [G]:** giọng; không nhạc ở 4 s đầu; SFX whoosh AS08 ở giây 0.0 · **Caption [G]:** đốt vào hình, y 84–95% · **9:16 [G]:** bố cục lại: avatar giữa, chữ đẩy lên vùng an toàn 9:16, vùng cắt X:Y:W:H = 420:0:1080:1080 (chưa kiểm) · **QA:** 0.0 «dải nhấn đã lộ mặt xong» · 1.0 «headline không che mặt» · 3.9 «chữ đã ra trước đổi cảnh»

### Cảnh C02 — Cách cũ tốn cả buổi sáng · 0:09–0:16 · chương 1

**Mã mẫu:** PA · LY-02 · VO-02 · MO-12 · TX-05 · IG-01 · TR vào TR-03 / ra TR-02 · RC-05 · AU: nhạc vào ở giây 0.0

**Câu V + marker:** V003 `giai-thich`

**Chữ trên hình + giữ:** «Cả buổi sáng» (3 từ, giữ ≥ 2.6 s)

**Người / màn hình / hoạt hoạ:** avatar co từ toàn khung về trái (≈ 60% rộng, nửa người); lớp nổi phải 38%: 5 thẻ file xếp dọc rồi 1 thẻ slide. TK01 9–16 s.

**Biên đạo theo giây:**

| Giây | Neo | Đối tượng, vị trí đầu → cuối | Hành động · thời lượng · easing | Giữ yên / chưa hiện |
|---|---|---|---|---|
| 0.0 | V003 · «Với nhiều người» | avatar: toàn khung → trái 60% | co 0.6 s kèm blur 0.3 s | lớp phải chưa hiện |
| 1.0 | V003 · «năm file Excel» | thẻ file 1…5, cột phải | bật cách 0.5 s (stagger), thẻ thứ 5 đúng chữ «năm» | thẻ slide chưa hiện |
| 4.0 | V003 · «chép số sang slide» | mũi tên (MO-01) từ thẻ file → thẻ slide | vẽ 0.5 s, sau khi hai thẻ đã có | — |
| 5.0 | V003 · «cả buổi sáng» | từ khoá | đổi cam khi nói (TX-05) | — |

**Asset ID:** AS01 (icon `file-spreadsheet`), AS02 (icon `presentation`), AS03 (take TK01), AS07 (nhạc nền) · **Âm [G]:** nhạc AS07 vào, −18 dB dưới giọng; SFX click AS08 mỗi thẻ file · **Caption [G]:** đốt, lệch phải khỏi avatar · **9:16 [G]:** bố cục lại: thẻ file xếp ngang dưới avatar · **QA:** 0.5 «thẻ không che mặt» · 3.0 «thẻ thứ 5 xuất hiện đúng chữ năm» · 6.5 «mọi thứ ra trước đổi cảnh»

### Cảnh C03 — Bước 1: gom nguồn · 0:16–0:25 · chương 2

**Mã mẫu:** PS · LY-05 · VO-17+VO-18 · MO-08, MO-03 · TX-09 · IG-01 · TR vào TR-02 / ra TR-09 · RC-26 · AU: hạ nhạc khi V004 vào

**Câu V + marker:** V004 `trung-tinh` · V005 `nhan-manh`

**Chữ trên hình + giữ:** pill «1 /3 Gom nguồn» (3 từ, giữ ≥ 2.6 s; không thẻ chương rời)

**Người / màn hình / hoạt hoạ:** màn hình giả (AS05) ≈ 85% vùng; avatar PIP squircle 14% dưới-trái; phụ đề lệch phải = bề rộng PIP + 2%. TK01 25–34 s.

**Biên đạo theo giây:**

| Giây | Neo | Đối tượng, vị trí đầu → cuối | Hành động · thời lượng · easing | Giữ yên / chưa hiện |
|---|---|---|---|---|
| 0.0 | V004 · «Bước một» | avatar: squircle → PIP | thu 0.4 s, blur-through từ C02 | PIP đứng yên suốt cảnh |
| 0.5 | V004 | pill «1 /3 Gom nguồn», dải trên | blur→nét 0.3 s, giữ tới 3.0 | — |
| 3.0 | V004 · «thư mục duy nhất» | thư mục tạo ra giữa màn hình | hiện 0.4 s | file chưa kéo |
| 4.0, 4.8, 5.6 | V004 · «ba file nguồn» | 3 file kéo vào thư mục | 0.5 s mỗi file, viền cam quanh file đang kéo (MO-08) | — |
| 6.5 | V005 · «Chỉ đọc» | viền cam quanh cả thư mục | 0.5 s, giữ tới hết V005 | — |

**Asset ID:** AS05 (UI giả quay màn hình, cần quay/dựng), AS03, AS08 · **Âm [G]:** nhạc hạ thêm −6 dB khi V004 vào (300 ms); SFX click AS08 mỗi file kéo · **Caption [G]:** đốt, lệch phải · **9:16 [G]:** bố cục lại: màn hình phóng vùng thư mục ở giữa, PIP dưới-trái, pill đẩy xuống vùng an toàn · **QA:** 0.5 «PIP không đè nút» · 4.8 «con trỏ ≥ 2% khung, viền cam đúng file đang kéo» · 8.5 «viền cam bao cả thư mục khi nói “chỉ đọc”»

### Cảnh C04 — Không bỏ bước kiểm + kêu gọi · 0:25–0:37 · chương 3

**Mã mẫu:** P · LY-01 · VO-18+VO-17 · MO: — · TX-02 · IG: — · TR vào TR-04 (cắt cứng, chớp 0.1 s tuỳ chọn) / ra — (kết) · RC-36 · AU: nhạc kết, vỉa cuối ra 3 s

**Câu V + marker:** V006 `nhan-manh` · V007 `gan-gui` · V008 `tram-lang`

**Chữ trên hình + giữ:** «File yêu cầu mẫu: ở phần mô tả» (6 từ, giữ ≥ 3.6 s) + mũi tên chỉ xuống

**Người / màn hình / hoạt hoạ:** TK01 34–36 s+, avatar toàn khung; chữ CTA dưới; không màn hình.

**Biên đạo theo giây:**

| Giây | Neo | Đối tượng, vị trí đầu → cuối | Hành động · thời lượng · easing | Giữ yên / chưa hiện |
|---|---|---|---|---|
| 0.0 | V006 | cắt về avatar toàn khung | cắt cứng, chớp 0.1 s | chữ chưa hiện |
| 3.4 | V007 · «file yêu cầu mẫu» | CTA, dưới giữa | gõ theo ký tự (TX-02) ≈ 0.03 s/ký tự | — |
| 4.0 | V007 · «phần mô tả» | mũi tên | nhấp nhẹ chỉ xuống | — |
| 11.0 | hết V008 | toàn khung | mờ đen 0.4 s | nhạc ra 3 s |

**Asset ID:** AS03, AS07, AS09 (thumbnail/end screen, mục 7) · **Âm [G]:** nhạc kết lên nhẹ ở V008 (`tram-lang`) · **Caption [G]:** đốt · **9:16 [G]:** dùng nguyên (avatar giữa, CTA lên vùng an toàn) · **QA:** 0.0 «cắt về đúng khung, mặt không bị che» · 5.0 «mũi tên chỉ đúng vùng mô tả» · 11.6 «mờ đen hết trước nhạc»

## 7. Gói xuất bản

| Trường | Nội dung |
|---|---|
| Chương YouTube | `0:00 Mở đầu` · `0:16 Bước 1: gom nguồn` · … *(rút gọn; mốc ước, cập nhật sau khi ghép)* |
| Tiêu đề | (1) «Giao báo cáo tuần cho trợ lý AI trong 3 bước» · (2) «Đừng mất cả buổi sáng viết báo cáo tuần nữa» (≤ 70 ký tự mỗi bản) |
| Mô tả | dòng 1: «Giao báo cáo tuần cho trợ lý AI trong 3 bước, và đừng bỏ bước kiểm.» dòng 2: «File yêu cầu mẫu ở link dưới.» rồi chương, nguồn và giấy phép nhạc, nhãn «giọng và hình do AI tạo» nếu nền tảng yêu cầu |
| Thumbnail | khung C01 giây 1.0 (avatar + headline); chữ «Mất bao lâu?» (3 từ ≤ 4); AS09 |
| End screen | 5–20 s cuối: dùng 8 s cuối C04; ô video đề xuất phải và nút đăng ký trái, không che chữ CTA |
| CTA | một hành động: lấy file yêu cầu mẫu ở mô tả (nói ở V007, chữ ở C04) |
| Short cắt từ video dài | C02–C03 (≈ 16 s) làm short thử, hook mới ở 3 s đầu: câu hỏi «Còn mất cả buổi sáng?»; bố cục 9:16 theo các thẻ ở mục 6 |

## 8. Kế hoạch dựng

Thứ tự: (1) giọng V001–V008, ASR nghe lại theo câu → (2) điền «giây đo», tính lại mốc → (3) TK01 chạy nền + `avatar qa` → (4) composition theo chương (C03 trước) → (5) ghép + nhạc + SFX → (6) caption → (7) QA mốc từng thẻ → (8) gói xuất bản và short.

- **Phụ thuộc:** audio trước khi căn cue · clip nền và crop trước TK01 · AS05 (quay hoặc dựng UI giả) trước C03.
- **Cảnh rủi ro, thử trước:** C03 (PIP không đè nút) và chuỗi TR-02 → TR-09.
- **Rủi ro:** lip-sync 224–939 s cho 10 s giọng (đo trên RTX 4070) nên TK01 ≈ 36 s chạy vài chục phút; glyph font; giấy phép nhạc.
- **Chưa kiểm:** audio, render, lip-sync, glyph, manifest marker thật, vùng cắt 9:16, giấy phép từng nguồn.
- **Cần người dùng quyết:** tên hồ sơ avatar và profile giọng · quay màn hình thật hay UI giả · nhạc nền · màu/font kênh.

**Manifest rút gọn** (dãy ID chung `AS01…`):

| ID | Loại | Mô tả | Dùng ở | Nguồn · giấy phép | Trạng thái |
|---|---|---|---|---|---|
| AS01 | icon | `file-spreadsheet` | C02 | họ icon nét mảnh nguồn mở · MIT/ISC | cần tải |
| AS02 | icon | `presentation` | C02 | như AS01 | cần tải |
| AS03 | take | TK01 = V001–V008, crop 720:720:0:180 | C01–C04 | lip-sync từ hồ sơ avatar · mặt chính chủ có đồng ý | chưa chạy |
| AS04 | giọng | WAV V001–V008, profile giọng, seed ghim | C01–C04 | tổng hợp · giọng chính chủ có đồng ý | chưa tạo |
| AS05 | clip | UI giả quay màn hình, 3 thao tác kéo file | C03 | tự dựng · không logo thật | cần quay |
| AS06 | vật | dải nhấn cam SVG | C01 | tự vẽ | cần tạo |
| AS07 | nhạc | nền một loop, tối thiểu 40 s | C02, C04 | nguồn mở có giấy phép ghi trong mô tả | cần tải |
| AS08 | sfx | họ «click mềm + whoosh ngắn» | C01–C03 | nguồn mở | cần tải |
| AS09 | thumbnail | khung C01 giây 1.0 + chữ «Mất bao lâu?» | xuất bản | dựng từ composition | cần tạo |
