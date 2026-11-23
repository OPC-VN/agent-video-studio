# Storyboard sản xuất — <mã-tập>

> **Kết luận:** file này thay mẫu chung `../video-routing/assets/storyboard.md` cho video **người/avatar + màn hình + hoạt hoạ** (skill `vlog-design`). Giữ tinh thần mẫu chung (mốc là ước lượng, không ô trống không giải thích) nhưng thêm bốn thứ mẫu chung không có: **bảng giọng có marker**, **bảng take avatar**, **mã mẫu thư viện trên mỗi thẻ cảnh**, **gói xuất bản**. Mẫu chung không bị sửa.

## Cách điền

- **Bắt buộc** (đánh dấu **[B]**): không điền thì bước kế tiếp không chạy được. **Gộp được** (đánh dấu **[G]**): storyboard ≤ 15 cảnh được gộp thành một dòng cho mỗi cảnh.
- Ô chưa biết ghi «chưa có» + cách bù; ô không áp dụng ghi «—» + lý do ngắn. Không để trống.
- Mốc thời gian là **ước** cho đến khi mục 4 có cột «giây đo» (sau khi có WAV); sau đó cột đo thắng.
- Mã mẫu (LY, VO, MO, TX, IG, TR, RC, AU) lấy từ thư viện `vlog-design`; mã không có trong `pattern-index.md` thì không dùng.
- Không ghi tên người, đường dẫn máy, secret. Tên profile giọng và hồ sơ avatar là tên trong trạm, được ghi.

## 1. Brief và quyết định

| Trường | Nội dung | |
|---|---|---|
| Trạng thái · người quyết · nguồn | … (`brief.md`, `beats.md`, `pacing.md`) | **[B]** |
| Người xem · vấn đề · thông điệp một câu · hành động sau xem | … | **[B]** |
| Chiến dịch (nếu thuộc một chiến dịch: tên, vai trò của tập trong chiến dịch, tập trước/sau, thông điệp chung) | … hoặc «không thuộc chiến dịch» | **[B]** |
| Định dạng · tỉ lệ (16:9 chính, 9:16 phụ) · độ dài mục tiêu · nền tảng | … | **[B]** |
| Hồ sơ avatar · lời đồng ý dùng mặt | tên hồ sơ trong trạm · «có» (trích) / «chưa» | **[B]** nếu có người |
| Profile giọng · lời đồng ý dùng giọng | tên profile · số marker của manifest (`voice-studio profiles list --json`) | **[B]** |
| fps dựng so với 25 fps lip-sync | fps dựng = … ; take avatar ra 25 fps. Nếu fps dựng ≠ 25: quy đổi take về fps dựng bằng một bước ghi trong mục 8 (không để trình dựng tự nội suy), kiểm lại môi–tiếng sau quy đổi | **[B]** |
| Sự thật có nguồn · giả định · giới hạn diễn đạt | số tác giả tự đưa → nhãn «ước tính» trên hình | **[B]** |
| Hướng kể (khi có lựa chọn thật): 2–3 hướng, ưu nhược, công sức, hướng chọn + lý do | … | [G] bỏ nếu không có lựa chọn thật |

## 2. Thiết kế chung

| Trường | Nội dung | |
|---|---|---|
| Nhịp cảm xúc, motif | hook → … → chốt | **[B]** |
| Màu (nền / chữ / nhấn / đạt / sai) + font tiêu đề / thân (đã thử glyph «Ả Ẫ Ặ Ể Ỗ Ợ Ữ ỹ đ Đ») | … | **[B]** |
| Cỡ chữ theo bậc (T1…T6), chữ ≤ 7 từ mỗi khối, giữ ≥ 1.5 s + 0.35 s/từ | … | **[B]** |
| Vùng an toàn **16:9** (lề %, vùng phụ đề y %) | … theo `layout-library` | **[B]** |
| Vùng an toàn **9:16** — bản phụ suy ra từ 16:9, thư viện chưa có mẫu dọc, số là đề xuất phải kiểm (khung 1080×1920: trên/dưới chừa cho giao diện nền tảng, vùng phụ đề, vùng cắt giữa 1080×1080 từ 16:9) | … theo `docs/SHORT_LAYOUT.md` | **[B]** nếu có short |
| **Khung người duy nhất**: một hình thể (squircle…), PIP ở đâu/rộng %, PA dùng cỡ nào, P toàn khung chỉ ở đâu | … | **[B]** nếu có người |
| Màn hình: thật hay giả (UI mock không logo thật), che thông tin riêng, cỡ con trỏ | … | **[B]** nếu có S/PS/AS |
| Âm: mức nhạc **dưới** giọng (dB hoặc % so với giọng), hạ nhạc khi giọng vào (ms), họ SFX (một họ, ví dụ «click mềm + whoosh ngắn»), khoảng lặng có chủ đích | … theo `audio-patterns` (mã AU) | **[B]** |
| Nguồn thiết kế: asset, quyền, trạng thái | trỏ `assets/MANIFEST.md` | **[B]** |

## 3. Bản đồ cảnh **[B]**

LY, chế độ, TR, chương khớp từng chữ với `pacing.md` (cùng một nguồn; sửa ở đâu thì sửa cả hai và chạy lại `pace_check`).

| Cảnh | Từ–đến | Chương | Chế độ | LY | TR vào | Marker chủ đạo | Ý người xem phải hiểu |
|---|---|---|---|---|---|---|---|
| C01 | 0:00–0:04 | 1 | P | LY-01 | TR-10 | `hao-hung` | … |

## 4. Bảng giọng **[B]**

Kịch bản đã **chuẩn hoá theo `voice-routing/references/vietnamese-tts-script.md`**: số phiên bản tách khỏi chữ viết tắt, giờ/ngày/tên miền viết thành chữ, từ ngoại ngữ để nguyên hoặc viết hoa chữ đầu theo bảng đo, không mảnh câu ngắn đứng riêng. Marker lấy từ manifest của profile, không tự nghĩ.

| Mã câu | Cảnh | Marker | Lời TTS đã chuẩn hoá | Nghỉ sau (s) | Giây ước → giây đo | File WAV |
|---|---|---|---|---|---|---|
| V001 | C01 | `hao-hung` | … | 0.4 | 3.6 → *chưa đo* | *chưa có* |

- Mã câu `V001…` tăng dần, không tái dùng; câu bỏ giữ mã, ghi «bỏ». Một cảnh có thể có nhiều câu V; một câu V không vắt qua hai cảnh (muốn vắt thì tách câu).
- «Giây ước» = số âm tiết ÷ 4 (chưa đo); «giây đo» = độ dài WAV thật, điền ở bước 4b của quy trình. Mốc cảnh ở mục 3 tính lại từ cột này.
- Câu đầu mỗi chương luôn ghi marker rõ, không dựa marker còn hiệu lực từ chương trước. Mỗi đoạn marker 1–5 câu.

**Phân bổ marker** (điền sau khi có bảng; nguồn quy ước: `voice-routing`, mục «Phân bổ sắc thái theo bố cục video»):

| Marker | Số câu | % | Ghi chú |
|---|---|---|---|
| `trung-tinh` | … | … | |
| `giai-thich` | … | … | |
| `gan-gui` | … | … | |
| `nhan-manh` | … | … | |
| `hao-hung` | … | … | |
| `ke-chuyen` | … | … | |
| `hoi-dap` | … | … | |
| `tram-lang` | … | … | |

Kiểm theo luật (ghi Đạt / Không đạt + lý do):
- [ ] Video ≥ ~3 phút (~30 câu): đủ 8 marker, mỗi marker ≥ 1 đoạn. Video ngắn hơn: ≥ 5 marker, có `hao-hung` ở mở và `nhan-manh` hoặc `tram-lang` ở kết.
- [ ] Không marker nào > 35% số câu; `trung-tinh` + `giai-thich` ≤ 60%.
- [ ] Không đoạn nào > 5 câu liền cùng marker; không đổi marker từng câu một.
- [ ] Không đặt `gan-gui` liền sau `tram-lang`; cặp marker mà báo cáo profile ghi là khó phân biệt không đứng liền nhau.
- [ ] Mọi marker có trong manifest; mọi từ ngoại ngữ đã qua bước chuẩn hoá.

## 5. Bảng take avatar **[B] nếu có avatar** (không có người: ghi «—, bố cục không người»)

Mỗi take = một lần chạy lip-sync, **≤ 60 s WAV** (giới hạn của engine LatentSync, `docs/LATENTSYNC.md`); lip-sync mất 224–939 s cho 10 s giọng (đo trên RTX 4070) nên chạy nền và gom take.

| Mã take | Câu V (từ–đến) | Dài (s) | Crop clip nền (W:H:X:Y) | Cảnh dùng | Trạng thái | Điểm QA (SyncNet: tin cậy / lệch) |
|---|---|---|---|---|---|---|
| TK01 | V001–V006 | 38.2 | 720:720:0:180 | C01–C03, C12 | chưa chạy | *chưa* |

- Trạng thái: chưa chạy · đang chạy · xong chưa QA · đạt · làm lại (lý do).
- Mức đạt: **lệch = 0 và tin cậy ≥ 7** (`video-studio avatar qa`); sau làm nét vùng miệng, soi mốc im lặng (miệng khép) và mốc đang nói (không có khe tối).
- Cắt take tại chỗ **nghỉ giữa câu**, không giữa câu. Take dùng cho cả PIP lẫn toàn khung thì crop một lần, tỉ lệ khung thu phóng ở composition.
- Một take dùng cho nhiều cảnh: ghi cả danh sách cảnh; mỗi cảnh cắt đoạn bằng mốc giây trong take, không chạy lại.

## 6. Thẻ cảnh — lặp một thẻ cho mỗi cảnh **[B]**

Storyboard ≤ 15 cảnh được **gộp** các trường đánh dấu [G] (Âm, Caption, 9:16, QA) thành **một dòng** mỗi trường; storyboard > 15 cảnh điền đủ. Trường **[B]** không bao giờ gộp bỏ.

### Cảnh [ID] — [tên] · [từ–đến] · chương [n]

**Mã mẫu [B]:** Chế độ … · LY-… · VO-… · MO-… · TX-… · IG-… · TR vào … / ra … · RC-… · AU-…

**Câu V + marker [B]:** V00x `marker` · V00y `marker` (lời nằm ở mục 4, không chép lại ở đây; chỉ chép nếu cần cue từ khoá)

**Chữ trên hình + thời gian giữ [B]:** «…» (n từ ≤ 7, giữ ≥ 1.5 s + 0.35 s/từ = … s)

**Người / màn hình / hoạt hoạ [B]:** vị trí và cỡ theo % khung (người: toàn khung / squircle 40% / PIP 14% góc …; màn hình: toàn khung / cửa sổ / phóng vùng …; hoạt hoạ: vùng nào). Take avatar: TKxx, đoạn …–… s.

**Biên đạo theo giây [B]** (neo vào câu V; 0.0 = đầu cảnh):

| Giây | Neo vào (câu V · từ khoá) | Đối tượng, vị trí đầu → cuối | Hành động · thời lượng · easing | Giữ yên / chưa được hiện |
|---|---|---|---|---|
| 0.0 | V001 · «…» | … | … | … |

**Asset ID [B]:** AS03, AS11, … (khớp `assets/MANIFEST.md`; asset chưa có ID thì thêm vào manifest trước, không viết tên file rời)

**Âm [G]:** nhạc (AUxx, mức dưới giọng …) · SFX tại mốc (AS… ở giây …) · hạ nhạc (giây … → …) · khoảng lặng (nếu có)

**Caption [G]:** đốt vào hình / SRT rời / tắt; vị trí tránh PIP (lệch phải = bề rộng PIP + 2%)

**9:16 [G]:** dùng nguyên (vùng cắt 1080×1080 giữa) / bỏ khỏi short (lý do) / bố cục lại (LY mới, vùng cắt X:Y:W:H, đẩy chữ lên vùng an toàn 9:16)

**QA [B]:** 3 mốc (đầu · giữa · cuối, giây) + **điều phải đúng** ở mỗi mốc (ví dụ «0.0: mặt không bị chữ che» · «giữa: thẻ thứ 5 xuất hiện đúng khi nói chữ năm» · «cuối: chữ ra trước đổi cảnh 0.3 s»). Motion phụ thuộc thời gian thì seek ngược một lần.

## 7. Gói xuất bản **[B]** (video đăng thật; bản nháp nội bộ ghi «—, chưa xuất bản»)

| Trường | Nội dung |
|---|---|
| Chương YouTube | `0:00 Tên chương`… (mốc **đo** sau khi ghép; chương đầu phải bắt đầu `0:00`, mỗi chương ≥ 10 s, ≥ 3 chương thì YouTube mới tách) |
| Tiêu đề | ≤ 70 ký tự, từ khoá chính ở đầu; 2 phương án |
| Mô tả | 2 dòng đầu chứa thông điệp + CTA (hiện trước nút «xem thêm»), rồi chương, link tài nguyên, nguồn/giấy phép nhạc, nhãn «giọng và hình do AI tạo» nếu nền tảng yêu cầu |
| Thumbnail | khung lấy từ cảnh … giây …; chữ **≤ 4 từ**; mặt/nhân vật nhìn về chữ; tương phản đọc được ở 168 px ngang |
| End screen | 5–20 s cuối: cảnh nào, vùng đặt video đề xuất + nút đăng ký (không che chữ CTA), nhạc kết |
| CTA | một hành động chính (nói trong V…, hiện chữ ở C…) |
| Short cắt từ video dài | danh sách cảnh: C…–C… (độ dài ≤ 60 s), lý do chọn, hook mới ở 3 s đầu (cảnh nào), bố cục 9:16 theo mục 6 |

## 8. Kế hoạch dựng **[B]**

Thứ tự (mỗi bước ghi Xong khi; chi tiết ở `references/workflow.md`):

1. **Giọng:** tổng hợp từng câu V → ASR nghe lại theo câu → sửa cách viết câu lỗi (mục 4 cột WAV).
2. **Đo mốc:** điền «giây đo», tính lại mốc cảnh mục 3 và neo cue mục 6.
3. **Take avatar:** chạy lip-sync theo mục 5 (chạy nền), `avatar qa`.
4. **Composition theo chương** (HyperFrames), cảnh rủi ro cao trước.
5. **Ghép** + nhạc + SFX (mức theo mục 2).
6. **Caption** (đốt / SRT).
7. **QA** theo mốc từng thẻ, rồi xem cả video ở tốc độ thật.
8. **Gói xuất bản** (mục 7) và bản short (nếu có).

Còn lại phải ghi:
- **Phụ thuộc:** audio trước khi căn cue · crop clip nền trước take · quy đổi fps (nếu fps dựng ≠ 25) trước composition.
- **Cảnh rủi ro, thử trước:** …
- **Rủi ro:** thời gian máy lip-sync · glyph font · giấy phép từng nguồn · môi–tiếng sau quy đổi fps.
- **Chưa kiểm:** (liệt kê: chưa nghe audio, chưa render, chưa chạy lip-sync, chưa thử glyph…)
- **Cần người dùng quyết:** …
