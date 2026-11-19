# Kết quả đánh giá
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · eval/RESULTS.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Cấu hình chạy: **chỉ dùng phân tích tất định và OCR, không bật VLM** (VLM dùng để bổ sung việc phân biệt "quay thật / AI / 3D", phân biệt ảnh AI với ảnh chụp thật, và âm thanh nhẹ). Lệnh tái lập nằm ở cuối file.

## 1. Cách làm ra hình ảnh (8 loại, có trọng số theo thời lượng cảnh)

| Tập | Số video | Độ chính xác | F1 điểm cắt | Độc lập |
|---|---|---|---|---|
| `labels.yaml` (tập điều chỉnh tham số) | 15 | **98.3%** | 1.00 (2 video có nhãn thật, gồm 14 chỗ chồng mờ 0.25 giây) | Quy tắc được thiết kế trên chính mẫu này |
| `holdout.yaml` | 9 | **99.6%** | — | Lần chạy đầu sai 2 chỗ, từ đó thêm quy tắc phụ thuộc tốc độ khung hình, nên không còn hoàn toàn độc lập |
| `holdout2.yaml` | 7 | **98.9%** | — | Lần đầu chạy sau khi quy tắc cách làm đã chốt |

Ma trận nhầm lẫn của tập điều chỉnh (giây): quay thật 16.0 đúng hết; video AI 141.2 đúng hết; 3D 66.5 đúng hết; render từ code 155.9 đúng, 2.4 bị đoán là 3D; quay màn hình / ảnh chụp màn hình 19.0 đúng hết; ảnh tĩnh 42.8 đúng, 5.3 bị đoán là render từ code.

Bảng này đo bằng cách giải mã lại từ đầu (không dùng đặc trưng đã lưu cache). Khi dùng cache thì kết quả là 99.9% / 99.6% / 99.8%; chênh lệch đến từ một thay đổi ở bước giải mã mà cache chưa bao phủ. Các tập được chia theo đoạn nguồn chứ không theo nhà sản xuất, nên các đoạn của cùng một quy trình sản xuất có thể nằm ở cả tập điều chỉnh lẫn tập giữ lại; con số trên tập giữ lại nên hiểu là "hiệu quả trên mẫu tương tự".

## 2. Tư liệu thật của người dùng (trong cảnh có quay thật / ảnh chụp màn hình / quay màn hình / ảnh chụp hay không, có trọng số theo thời lượng)

| Tập | Độ chính xác | Ghi chú |
|---|---|---|
| labels | 97.6% | Lỗi duy nhất: ảnh nền NASA bán trong suốt, tối màu của mediank bị bỏ sót (hạn chế đã biết) |
| holdout | 99.6% | Lần đầu có 2 báo động sai: phụ đề trên nền code sáng bị coi là ảnh chụp; tóc 3D bị coi là video nhúng. Kết quả sau khi chỉnh quy tắc |
| holdout2 | 97.2% | **Lần đầu chỉ 75.6%**: dải phụ đề bị coi là ảnh/video; ảnh nhúng mặc định là "thật". Sau chỉnh quy tắc thì không còn độc lập. Lỗi còn lại: ảnh chụp trang web nền tối bị bỏ sót |

Các quy tắc chỉnh sau lần chạy đầu:
- Chữ đếm theo từng khung hình đơn, tránh cộng dồn phụ đề ở các thời điểm khác nhau.
- Dải phụ đề không tham gia việc phán đoán ảnh/video.
- Đoạn ảnh/video nhúng mặc định ghi là "thật hay AI chờ xác nhận"; chỉ ảnh chụp màn hình và quay màn hình mới trực tiếp tính là tư liệu thật.
- Trong cảnh 3D chỉ nhận bảng ảnh chụp màn hình.

## 3. Âm thanh

| Mục | Kết quả | Nguồn sự thật |
|---|---|---|
| Có / không có giọng người | 5/5 | tts.py của capsule-cinema, video nói trước camera |
| Có / không có BGM | 4/4 | bgm.py, bgm_fit.json |
| BPM (±4%, kể cả nửa tốc / gấp đôi) | 2/2 (110.0 / 112.3 so với thật 110.15) | bgm_fit.json |
| Tông (key) | 2/2 (D major) | bgm_fit.json |
| Có / không có hiệu ứng âm thanh (≥3 chỗ) | 2/4 | cues.py, danh sách tư liệu |
| Nguồn nhạc | 2/5 (xem bên dưới) | Bản ghi tạo Suno, bản ghi tải từ thư viện nhạc |

**Hiệu ứng âm thanh là điểm yếu của lớp tất định:** trong hỗn âm giọng người + BGM của "Salted egg", đối chiếu với 110 hiệu ứng thật trong cues.py, các đặc trưng tín hiệu không phân biệt được hiệu ứng với phần mở đầu của giọng nói/nhạc (độ chính xác khoảng 0.2, tương đương ngẫu nhiên). Vì vậy hiện chỉ đưa ra "ứng viên độ tin cậy thấp" cho các đỉnh âm bất thường rất nổi bật ngoài giọng người; **danh sách hiệu ứng đầy đủ giao cho VLM (Gemini có khả năng nghe)**.

**Nguồn nhạc** được phán đoán theo "tiên nghiệm về hình thức video + bằng chứng". Quy tắc nằm ở `skills/rea-video/references/audio.md`. Khi không bật VLM và không có thông tin nền tảng:

| Video | Hình thức | Thật | Phán đoán |
|---|---|---|---|
| qing_hiphop_mv | MV rap do AI làm (điệp khúc giọng khô lặp 0.26) | Suno v6 | Do AI sinh 52% ✓ |
| mediank_pure_data | Nhạc nền thuần | Thư viện manten diloty | Thư viện có sẵn 60% ✓ |
| monkey_wine_v3 / salted_egg / birdnest | Thuyết minh TTS + BGM (điệp khúc giọng khô lặp 0.00) | Suno sinh | Thư viện có sẵn 52% ✗ |

Ba ca sai là **hạn chế của chính tiên nghiệm**: video thông thường làm bằng quy trình AI thường cũng dùng BGM do Suno sinh, và nhạc không lời của Suno với nhạc thư viện không tách được về tín hiệu. Trước đây 3/3 đúng là vì "đầy nhạc + có giọng người" dẫn đến nhận nhầm thuyết minh TTS là MV, tức là đúng do may mắn; sau khi thêm phân biệt hát/nói, lý do phán đoán đúng hơn nhưng độ chính xác giảm trung thực. Muốn sửa ba ca này cần nhãn nhạc của nền tảng (`--meta`) hoặc nhận dạng bài hát; vì vậy trong báo cáo, nhạc nền thông thường luôn ghi "nghiêng về thư viện, chờ xác nhận". Lưu ý: ngưỡng phân biệt hát/nói được đặt sau khi xem MV qing, nên thuộc tập phát triển.

**Tách giọng người** (`stems/`): đặt một câu TTS của "Salted egg" lên trên BGM Suno của nó (giọng cao hơn 6 dB), SDR tách giọng 19.7 dB, nhạc nền 19.7 dB; BGM thuần rò vào track giọng −42.5 dB. Tiếng gõ phím trong mediank rơi vào track giọng (hướng đi đã biết của hiệu ứng ngắn). MV rap đo cao độ liên tục trên hỗn âm là 0.44, trên giọng khô chỉ 0.24: số đo trên hỗn âm bị nốt kéo dài của nhạc đệm đẩy lên, nên hiện phân biệt hát/nói luôn đo trên giọng khô.

## 4. Video đã chuyển mã của nền tảng (10 video trong 10 bài của OiiOii, tập phát triển)

`eval/articles.yaml`: tải từ hai bài trên WeChat Official Account, bản chuyển mã của WeChat (30fps, nén lại lần hai). Nhãn thật lấy từ ghi chú của tác giả bài + xem hình thủ công. Quy tắc xử lý chuyển mã được thêm sau khi xem lô video này, nên đây là tập phát triển.

| Video | Nhãn thật | Trước khi thêm quy tắc chuyển mã | Sau khi thêm |
|---|---|---|---|
| v11 Video bán hàng TikTok gốc | Quay thật | AI 100% (0.0) | Quay thật 100%, ghi "thật hay AI chờ xác nhận" (1.0) |
| v09 Video phát hành Gemini | Hoạt ảnh UI 2D | Code 63% + 3D 37% (0.63) | Code 81% + 3D 19% (0.81) |
| v10 Video sản phẩm OiiOii | Hoạt ảnh UI bằng code | Code 78% + 3D 17% (0.83) | Code 92% + 3D 4% (0.96) |
| v04 Video quảng bá gốc | Phần tử 3D + hoạt ảnh chữ | 3D 65% + AI 35% (0.65) | Không đổi (0.65) |
| 6 video AI / ghép màn hình còn lại | — | Đúng hết / 0.8 | Không đổi |
| **Trung bình** | | **0.79** | **0.92** |

Quy tắc chuyển mã có ba điều:
1. Nhận diện chuyển mã của nền tảng (metadata `Tencent CAPD MTS` / `Wxmm_` / `vid:v…`). Sau chuyển mã, bằng chứng "không có nhiễu" không còn được coi là dấu hiệu AI; độ đều nhịp sắc nét (do cấu trúc GOP bị chuyển mã làm giả) không còn được coi là bằng chứng nội suy khung.
2. Bằng chứng tốc độ khung hình ở cấp toàn file: với file 30fps, nếu ≥70% thời lượng các cảnh quay thật không có khung lặp → nghiêng về quay trực tiếp trên điện thoại (video do mô hình sinh thường xuất 24fps, chuyển sang 30fps sẽ có khoảng 20% khung lặp).
3. Khung hình gần như không màu, chỉ dùng vài màu, phẳng → phán là giao diện/tài liệu chứ không phải 3D.

Trước và sau khi thêm ba quy tắc này, điểm của ba tập đánh giá đầu về cách làm không đổi. Bảng trên là điểm từng video tại thời điểm thêm quy tắc; nhóm này hiện chỉ dùng công cụ thì điểm tổng là 88.6% (xem mục 5).

### Đánh giá của agent (dsh, DeepSeek V4.1 Flash, không xem được ảnh)

11 video có nhãn thật: công cụ đúng hết 5 / đúng một phần 5 / sai 1; sau khi dsh kiểm tra thì đúng hết 6 / đúng một phần 2 / sai 3. dsh đã lật kết luận của công cụ 4 lần, 2 đúng 2 sai, cả hai lần sai đều là đổi loại hình ảnh chỉ dựa trên thống kê điểm ảnh. Vì vậy SKILL.md được bổ sung: "Khi không xem được ảnh, không được lật kết luận về cách làm của công cụ". Cách kiểm tra lại xem `eval/agent_test/README.md`.

## 5. Sau khi xem ảnh (cách làm, có trọng số theo thời lượng)

| | holdout (9) | holdout2 (7) | Video chuyển mã (10, tập phát triển) |
|---|---|---|---|
| Chỉ dùng công cụ | 99.6% | 99.8% | 88.6% |
| + mô hình xem ảnh (Gemini) | 99.6% | 99.8% | 99.6% |
| + agent review | 99.6% | 99.8% | 100% |
| Bật cả hai | 99.6% | 99.8% | 98.8% |

Bảng này dùng đặc trưng đã cache (vì vậy "chỉ dùng công cụ" của holdout2 là 99.8%; giải mã từ đầu là 98.9% ở mục 1). Câu trả lời của mô hình xem ảnh đến từ một lần kiểm tra mù: đổi tên video rồi giao cho agent khác chạy đầy đủ quy trình theo `eval/agent_test/JOB.md`.

Khi chỉ có một nguồn xem ảnh, nó chỉ có tác dụng ở chỗ công cụ chưa chắc chắn; trong ba bên (công cụ, mô hình xem ảnh, agent), khi công cụ và bất kỳ bên xem ảnh nào thống nhất thì lấy kết quả đó. Khi hai bên xem ảnh cùng phản đối công cụ thì không ép đổi: đã thử đa số bất kỳ trong ba bên, nhưng nhóm video chuyển mã lại tụt từ 98.4% xuống 91.9%, vì hai mô hình xem ảnh thường nhìn nhầm cùng một hình thành cùng một loại.

## 6. Mẫu chạy lần đầu (quy tắc chưa từng thấy các mẫu này)

| Tập | Chỉ công cụ | + mô hình xem ảnh | + agent review |
|---|---|---|---|
| Bán hàng trên Douyin 2 video (mở hộp quay thật; hướng dẫn lẫn AI và người thật), `daihuo.yaml` | 46.4% | 63.9% | 97.5% |
| Trong đó tư liệu thật | 62.4% | 86.8% | 97.5% |
| Nói trước camera trên Douyin 2 video (cảnh phố đêm; cận cảnh trong nhà), `koubo.yaml`, tập phát triển | 75.5% (51% / 99%) | 88.5% | 96.7% |

Nhóm bán hàng là lần đầu quy tắc hiện có gặp nội dung này, và cho thấy rõ nhất việc chỉ dùng công cụ với video chưa từng thấy sẽ ra sao: cảnh tay quay từ trên xuống, tĩnh sau chuyển mã bị đoán là AI; cảnh quay điện thoại thật (không phải quay màn hình) bị đoán là 3D hoặc AI. Mô hình xem ảnh đoán đúng, nhưng quy tắc hợp nhất khi "công cụ đoán 3D, xem ảnh đoán quay thật" đã theo công cụ, nên phải nhờ agent review mới sửa lại được. Nhóm nói trước camera được điều chỉnh theo đúng hai video này, video cảnh đêm chỉ dùng công cụ vẫn chỉ đạt một nửa.

Điểm cắt: 9 video có điểm cắt được người gán nhãn theo từng khung (nói trước camera, bán hàng, video cắt ghép phim, bán hàng quay thật bằng điện thoại): recall 95%, precision 94%.

### Không bật mô hình xem ảnh, chỉ dùng agent review

Khi không có mô hình xem ảnh (chưa cấu hình VLM hoặc dịch vụ không khả dụng), agent là bên xem ảnh duy nhất. Agent xem contact sheet đầu/giữa/cuối của từng cảnh, kèm bằng chứng của công cụ và quy tắc trong SKILL.md, nên phán đoán của nó có thể vượt ra ngoài hai ứng viên đứng đầu của công cụ. Hai điều kiện: kết luận sau hợp nhất trùng đúng loại agent chọn; và cảnh đó không có quy luật khung lặp 24→30 (tự thân cảnh đó không đo được). Khi chỉ có một bên xem ảnh là mô hình, quy tắc giữ nguyên.

Bảng dưới đây hợp nhất lại đặc trưng đã cache với câu trả lời của agent, có trọng số theo thời lượng:

| Tập | Chỉ công cụ | Chỉ agent review |
|---|---|---|
| Bán hàng (2 video) | 46.4% | 98.6% |
| Video cắt ghép phim (9 video) | 15.5% | 98.8% |
| Nói trước camera (2 video) | 75.5% | 96.8% |
| holdout (9) | 99.6% | 100% |
| holdout2 (7) | 99.8% | 99.8% |
| Video từ bài báo (13, vòng mù thứ hai) | 88.6% | 100% |

Trong video bán hàng gồm một cảnh AI dạy làm, cảnh điện thoại thật quay từ trên xuống bị công cụ đoán 3D hoặc render từ code sau chuyển mã; agent đoán quay thật. Theo quy tắc cũ "phải nằm trong hai ứng viên đứng đầu của công cụ", video này chỉ đạt 40%.

## 7. Phân bố sai số: theo độ phân giải, theo chuyển động camera

`rea-video eval` có hai bảng trong phần tóm tắt: `by_resolution` (chia theo cạnh ngắn của khung hình) và `by_camera` (theo chuyển động camera do công cụ đo). Mỗi mức cho thời lượng, độ chính xác, số cảnh sai và số giây "thật → đoán sai". Bảng dưới tổng hợp 9 nhóm ngoài video cắt ghép phim, chỉ dùng công cụ, có trọng số theo thời lượng. Nhóm video cắt ghép phim (`film.yaml`) chỉ dùng công cụ đạt 15% độ chính xác: công cụ không nhận ra loại "đoạn phim điện ảnh", phải nhờ phán đoán bằng ảnh, nên nhóm này xem riêng, không gộp vào tổng. Mẫu không tìm thấy file video không được tính.

| Độ phân giải | Thời lượng | Độ chính xác | Cảnh sai | Lỗi chính |
|---|---|---|---|---|
| 1080p | 913 giây | 90.5% | 40/283 | Quay thật→3D 21.5 giây; render từ code→3D 18.0 giây; quay thật→render từ code 15.4 giây |
| 720p | 607 giây | 97.6% | 3/145 | Render từ code→ảnh tĩnh pan/zoom 6.0 giây; 3D→ảnh tĩnh pan/zoom 6.0 giây |
| ≤480p | 94 giây | 100% | 0/15 | — |
| >1080p | 16 giây | 100% | 0/1 | — |

| Chuyển động camera | Thời lượng | Độ chính xác | Cảnh sai | Lỗi chính |
|---|---|---|---|---|
| Cố định | 727 giây | 91.6% | 26/184 | Quay thật→3D 18.6 giây; quay thật→render từ code 15.4 giây; render từ code→3D 15.2 giây |
| Chuyển động mượt | 550 giây | 98.0% | 8/142 | 3D→video AI 5.0 giây; quay thật→video AI 3.8 giây |
| Cố định (chủ thể đang chuyển động) | 251 giây | 97.8% | 4/98 | Render từ code→3D 5.1 giây |
| Rung cầm tay | 63 giây | 90.5% | 2/12 | 3D→video AI 5.4 giây |
| Đẩy/kéo/lia toàn ảnh | 38 giây | 53.1% | 3/7 | 3D→ảnh tĩnh pan/zoom 12.0 giây; render từ code→ảnh tĩnh pan/zoom 6.0 giây |

Cách đọc:
- **Máy cố định là nguồn lỗi chính:** khi khung hình gần như không đổi, công cụ chỉ có texture và nhiễu để dựa vào; sau chuyển mã, cảnh quay thật trên điện thoại (cảnh tay quay từ trên xuống, quay màn hình điện thoại thật) dễ bị đoán là 3D hoặc render từ code. Nhóm bán hàng với máy cố định chỉ đạt 41%; cùng nhóm, cảnh chủ thể chuyển động đạt 99%.
- **Đẩy/kéo toàn ảnh** mẫu ít, nhưng lỗi tập trung: cú đẩy chậm cả khung trong 3D và hoạt ảnh code bị đoán là ảnh tĩnh pan/zoom.
- **Độ phân giải và loại nội dung bị trộn vào nhau:** mức 1080p gần như toàn video điện thoại trên Douyin (bán hàng, nói trước camera), mức 720p chủ yếu là mẫu hoạt ảnh code và 3D, nên 1080p thấp chủ yếu phản ánh độ khó của nội dung, không chứng minh được độ phân giải tự gây sai. Muốn đo riêng độ phân giải, cần chuyển cùng một video sang nhiều mức rồi đo lại.

## 8. Đo lại từ đầu (chỉ dùng công cụ)

Tất cả tập đánh giá đã được đo lại từ đầu, không dùng đặc trưng cache, chỉ dùng công cụ, có trọng số theo thời lượng. Các mục trên là kết quả tại thời điểm từng quy tắc được chỉnh; đây là kết quả tổng cho cùng một phiên bản mã. Một số mẫu thiếu file video trên máy, không được tính; số mẫu thiếu được ghi trong ngoặc, nên các nhóm này chỉ mang tính tham khảo.

| Tập | Độ chính xác |
|---|---|
| `labels.yaml` (thiếu 11) | 100% |
| `holdout.yaml` (thiếu 3) | 99.5% (một cảnh 0.5 giây dao động giữa video AI và quay thật, độ tin cậy 0.48; giờ mỗi khung của cảnh được đọc đầy đủ, cảnh này rơi về phía quay thật) |
| `holdout2.yaml` (thiếu 4) | 100% |
| `articles.yaml` video từ bài báo (chuyển mã) | 97.2% |
| `daihuo.yaml` bán hàng | 63.2% |
| `koubo.yaml` nói trước camera | 93.3% |
| `film.yaml` video cắt ghép phim | 15.8% |
| `code_videos.yaml` | 94.8% |
| `code_videos_holdout.yaml` | 100% |
| `particles.yaml` (3 video) | 66.7% (tập mở rộng từ 1 lên 3 video; mẫu bokeh mới chưa nhận ra, mẫu cũ vẫn đúng) |

So với điểm chỉ dùng công cụ đã ghi trước đó, ngoại trừ một cảnh ngắn của holdout, không nhóm nào giảm: video từ bài báo 88.6% → 97.2%; bán hàng 46.4% → 63.2%; nói trước camera 75.5% → 93.3%; video cắt ghép phim 15% → 15.8%. Nhóm bán hàng và video cắt ghép phim chỉ dùng công cụ vẫn chưa đủ, cần review bằng cách xem ảnh (mục 5, 6).

## Hạn chế đã biết

1. Mẫu quay thật chỉ có 3 video (đều là video điện thoại 60fps trên Douyin); không có mẫu Ken Burns thật, mới chỉ thử trên video tổng hợp.
2. Ảnh nền tối / bán trong suốt và ảnh chụp trang web nền tối bị bỏ sót; ảnh sản phẩm và logo chồng lên cảnh quay thật hoặc AI không được phép dò tất định, phụ thuộc VLM.
3. Ảnh nhúng là ảnh chụp thật hay ảnh AI, lớp tất định không phân biệt được.
4. Điểm của việc thêm mô hình xem ảnh và review của agent là tính lại từ đáp án đã cache, chưa đo lại trên đặc trưng giải mã từ đầu; khi chỉ bật mô hình xem ảnh mà không có review của agent, trên tập giữ lại từng thấp hơn chỉ dùng công cụ.
5. Hình nền tối có chi tiết rời rạc (hạt, point cloud, nét mảnh): cùng bộ ngưỡng được đo cả trên ảnh gốc và trên ảnh đã bỏ nền mượt (ánh sáng mềm, tối góc, chuyển màu ở cấp khung, không gồm chính vật thể), nên có nền mềm phía sau vẫn nhận ra; ngưỡng được rút từ tập phát triển (đầu file `particles.yaml` có ghi chú); mẫu halo cũng thuộc tập phát triển. Các đốm bokeh lớn mờ trôi trên nền tối chưa nhận ra được. Bầu trời sao, ánh đèn đêm, giao diện tối chưa có mẫu riêng, nên khả năng bị nhầm thành render từ code chưa được loại trừ.
6. Nguồn nhạc: BGM do AI sinh trong video thông thường không phân biệt được (xem trên); mẫu MV do AI mới có 1 video.

## Tái lập

Đường dẫn video trong danh sách trỏ đến thư mục nguồn tương ứng (`${CAPSULE}` là kho capsule-cinema); nếu không có, công cụ dùng `eval/media/<id mẫu>.<phần mở rộng>`. Video không được phân phối cùng kho; mẫu thiếu được liệt kê trong mục `missing` của kết quả đánh giá, điểm chỉ phủ phần tìm thấy.

```bash
export CAPSULE_CINEMA_ROOT=~/code/github/capsule-cinema
rea-video eval eval/labels.yaml   -o out/eval_main
rea-video eval eval/holdout.yaml  -o out/eval_hold
rea-video eval eval/holdout2.yaml -o out/eval_hold2
rea-video eval eval/articles.yaml -o out/eval_articles
rea-video eval eval/audio_mv.yaml -o out/eval_audio_mv --stems   # chỉ đánh giá âm thanh (--stems tách giọng người trước rồi đo hát/nói)
# Thêm VLM:
rea-video --env-file $CAPSULE_CINEMA_ROOT/.env eval eval/labels.yaml -o out/eval_main_vlm --vlm
```
