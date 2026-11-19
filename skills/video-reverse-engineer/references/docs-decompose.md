# Phương pháp phân rã: cách xác định một cảnh "được làm ra như thế nào"

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · docs/decompose.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Mục tiêu: với mỗi cảnh, đưa ra cách làm của hình ảnh nền, các lớp chồng lên, bằng chứng và độ tin cậy, rồi đưa ra hướng phục dựng.

## 1. Hệ thống phân loại

| Nhãn | Ý nghĩa | Hướng phục dựng (rea_video/capabilities/routing.yaml) |
|---|---|---|
| `live_action` | Quay thật | R07: xấp xỉ bằng AI image-to-video, hoặc quay lại |
| `ai_video` | Video do AI tạo | R07: khung đầu–cuối + prompt, sinh bằng capsule-cinema |
| `avatar` | Người ảo nói trước camera | R03: nhân bản giọng nói + người ảo |
| `cg_3d` | Render 3D | R08: dựng mô hình 3D và render, hoặc xấp xỉ bằng AI sinh theo khung đầu–cuối |
| `code_render` | Render từ code/template (MG, chữ, UI, biểu đồ, thẻ) | R01: phục dựng bằng Remotion/HTML |
| `screen_capture` | Quay màn hình/chụp màn hình | R02: quay lại giao diện thật |
| `still_motion` | Ảnh tĩnh + đẩy, kéo, lia, trượt máy (pan/zoom) | R17: một ảnh + tham số chuyển động đo được, phục dựng chính xác ngay trên máy |
| `static_hold` | Khung tĩnh đứng yên | R18: một ảnh |

Lớp chồng (overlay) được liệt kê riêng: phụ đề, tiêu đề, chú thích chữ, miếng dán đồ họa, bố cục template. Cùng một cảnh có thể vừa là "video AI + phụ đề code".

## 2. Bằng chứng lấy từ đâu

Phần đo tất định (deterministic: đo bằng thuật toán, không dùng AI) lo các vấn đề "đo được", VLM (mô hình thị giác-ngôn ngữ) lo các vấn đề "hiểu được hình". Hai bên phân công rõ ràng:

| Vấn đề | Phương pháp | Độ tin cậy |
|---|---|---|
| Cắt cảnh ở đâu | Khoảng cách histogram HSV và sai khác điểm ảnh, cộng ngưỡng thích nghi cục bộ; diện tích thay đổi phải đủ lớn, phần tử bật lên không tính là cắt cảnh. Jump cut / cắt đẩy gần (push-in): nhảy đột ngột trong cùng một góc máy ở một khung, mức nhảy vượt xa biến thiên của các khung trước sau và các khung trước sau thì ổn định; ánh chớp, ánh lửa sáng lên rồi trở lại như cũ trong một-hai khung không tính là cắt cảnh. Chồng mờ (cross dissolve): khung giữa có phải là hỗn hợp tuyến tính của hai khung đầu cuối không, và dùng optical flow để loại trừ chuyển động đẩy/kéo. Chuyển cảnh: đo điểm đầu và điểm cuối của từng ranh giới, rồi phân loại thành fade / chớp trắng / chồng mờ (dissolve) / quét (wipe) / trượt (slide) / lia nhanh (whip) / zoom / xoay / mờ / glitch / rung; wipe và slide có kèm hướng | Cao (hai video có nhãn chuẩn đạt F1=1.0, trong đó một video có 14 chỗ chồng mờ 0.25s) |
| Hình có chuyển động không | Tỉ lệ khung lặp hoàn toàn theo từng điểm ảnh, chênh lệch khung đầu và khung cuối | Cao |
| Có phải một ảnh đang zoom/pan không | Khớp biến đổi tương tự bằng optical flow LK (RANSAC): tỉ lệ inlier cao, sai số dư nhỏ, không có chuyển động cục bộ, và sau khi bù chuyển động gần như không còn phần dư | Cao |
| Texture là của hình render hay của hình quay/chụp | Tỉ lệ khối phẳng 8×8, số màu cần để phủ 95% điểm ảnh, tỉ lệ cạnh thẳng ngang/dọc, nhiễu Immerkær | Cao (phân biệt render với ảnh chụp) |
| Compositing 2D / hoạt ảnh code | Điểm ảnh nền hoàn toàn không đổi qua từng khung, chỉ một vùng cục bộ chuyển động | Cao |
| Tốc độ khung hình gốc | Quy luật khung lặp (24→30 thì khoảng 20%, chu kỳ 4–6); dao động độ nét theo chu kỳ do nội suy khung (khi không có khung lặp thì chỉ là bằng chứng yếu vì nén lại cũng tạo ra được); gốc ≥48fps và không có khung lặp | Trung bình đến cao: mô hình sinh thường xuất 24/25fps, điện thoại hay quay 60fps |
| Quay thật, AI hay 3D | Nhiễu cảm biến và nhiễu theo thời gian, rung tay, dấu vân tay tốc độ khung; cộng với VLM tìm sơ hở (ngón tay, chữ, vật lý, nhấp nháy texture) | Trung bình khi chỉ dùng phân tích tất định, cao khi cộng VLM |
| Siêu dữ liệu | Hãng/model thiết bị quay; nhãn ẩn AIGC theo GB 45438 (Label 1/2/3 và mã của bên cung cấp dịch vụ); C2PA; chữ ký của phần mềm dựng/render | Rất mạnh khi có; thường bị nền tảng xóa |
| Lớp chồng | Cụm cạnh nền đang chuyển động nhưng điểm ảnh đứng yên, cộng với luồng chữ OCR (vị trí, có đổi theo thời gian không, có nằm ngang không) | Trung bình đến cao |
| Âm thanh | Điểm bắt đầu nốt (onset)/nhịp, tỉ lệ điểm cắt rơi đúng vào onset (cắt theo nhịp nhạc), đặc trưng điều chế giọng nói | Trung bình |

Các đoạn được nối bằng jump cut là cùng một đoạn tư liệu bị cắt ra (cùng góc máy, cùng nền). Khi bật VLM thì ghép các đoạn đó thành một clip và hỏi một lần (tối đa 12 giây, tối đa 8 đoạn): cách làm và cách quay được đưa ra một lần cho cả đoạn, còn mô tả nội dung và prompt phục dựng của từng đoạn thì đưa riêng. Khi số lượt gọi VLM có giới hạn, ưu tiên cho các cảnh mà công cụ kém chắc nhất và dài nhất. Chữ trên cảnh lấy trực tiếp từ kết quả mà lượt OCR cả video đã đọc được trong khoảng thời gian đó; khi lượt OCR cả video quá thưa (video dài) hoặc đã tắt lớp đồ họa hậu kỳ thì mới tự đọc 1–4 khung theo độ dài cảnh.

## 2.1 Tư liệu thật của người dùng

Nguồn tư liệu chia làm bốn loại: AI tạo, render của bên sản xuất, tư liệu thật của người dùng, và hỗn hợp.

- **Toàn khung**: suy ra từ nhãn của hình ảnh nền. Quay thật = tư liệu thật; quay màn hình = ghi hình/chụp giao diện; nguồn của khung tĩnh là ảnh chụp hoặc ảnh chụp màn hình = tư liệu thật.
- **Nhúng** (chỉ phát hiện trong hình render):
  - Trong một panel màu nhạt, ít bão hòa, một khung hình có ≥6 chỗ chữ cỡ nhỏ → ảnh chụp giao diện (chắc chắn là tư liệu thật).
  - Vùng có entropy mức xám cao, không có mảng màu phẳng → ảnh hoặc đoạn video (thật hay AI **chờ xác nhận**).
  - Dải phụ đề không tham gia phát hiện.
- Trong kế hoạch phục dựng, tư liệu thật được liệt kê hết ở `user_assets`; khi phục dựng, người dùng phải cung cấp, không được để mô hình sinh ra.

## 2.2 Âm thanh

Thực hiện HPSS (dùng lọc trung vị tách thành phần hài âm và thành phần gõ) trên STFT:

- **Giọng người**: điều chế âm tiết ở dải 3–8Hz của giọng người, cộng với khoảng nghỉ giữa các câu; dùng tần số cơ bản để gợi ý giọng nam/nữ. Khi có nhiều người nói, phân người nói theo chất giọng trên phần giọng khô (dry vocal), mỗi người một track.
- **Nhạc**: lớp nhạc lót vẫn to và có cao độ trong các khoảng nghỉ giọng, hoặc chu kỳ nhịp rõ rệt; ước lượng BPM bằng tự tương quan của onset; ước lượng tông bằng profile Krumhansl; tìm điểm chuyển đoạn nhạc bằng độ mới (novelty) của chroma.
- **Dựng**: tỉ lệ điểm cắt rơi vào nhịp hoặc onset.
- **Hiệu ứng âm thanh (SFX)**: lớp tất định chỉ đưa ra các transient nổi bật ngoài giọng nói làm ứng viên độ tin cậy thấp; danh sách đầy đủ do VLM nghe ra (xem kết quả đo thực tế trong eval/RESULTS.md).
- **Sản phẩm**: `audio` (giá trị đo), `audio_plan` (track âm thanh sau khi gộp VLM và phương án phục dựng), `audio.png` (timeline).

## 3. Hợp nhất

Xác suất cuối ∝ (xác suất tất định)^(0.6×trọng số tin cậy) × xác suất VLM, cộng thêm hai ràng buộc cứng:

- Cảnh có hình đứng yên không được phân loại vào bất kỳ nhóm "sinh video" nào.
- Cảnh cả ảnh pan/zoom theo biến đổi cứng không được phân loại là quay thật hoặc người ảo.

Trọng số tin cậy: khung tĩnh 1.6, ảnh tĩnh pan/zoom 1.4, render từ code 1.0; quay thật, AI và 3D chỉ 0.6, nên ba loại này chủ yếu do VLM quyết định.

Khi có nguồn xem ảnh (VLM hoặc agent review) tham gia, việc phán đoán chia hai bước: trước hết xét hình được tạo ra thế nào (sinh: video AI + người ảo; render: 3D + code; quay thật; quay màn hình; ảnh tĩnh), rồi mới xét loại chi tiết trong nhóm đó, độ tin cậy là tổng xác suất của nhóm. Nhờ vậy khi "công cụ phán video AI, agent phán người ảo, VLM phán quay thật" thì hai phiếu đầu được gộp thành "sinh", không bị một phiếu "quay thật" mạnh hơn làm phân tán. Chỉ dùng công cụ thì vẫn lấy loại chi tiết có điểm cao nhất: điểm người ảo mà công cụ đưa ra được tách ra từ video AI, nếu gộp sẽ lấn át quay thật (trên bộ đánh giá video nói trước camera, đo thực tế điểm giảm từ 0.51 xuống 0.33).

Quy tắc đa số: khi lựa chọn đầu của công cụ khớp với đúng một trong hai nguồn xem ảnh (cùng loại chi tiết, hoặc cùng nhóm), kết luận bắt buộc phải nằm trong nhóm đó.

Các chốt chặn khác:
- Nếu công cụ và VLM, một bên phán quay thật, một bên phán không phải quay thật, và chưa có agent review, thì đánh dấu "có bất đồng" và đưa vào danh sách bắt buộc xem của `review_tasks.json`: VLM có thể bịa ra bằng chứng không có thật (ví dụ "đồng hồ treo tường hiển thị số lỗi" trong video gốc về máy ép trái cây).
- Tốc độ khung chỉ cho biết tư liệu gốc là 24fps: nếu phán là video AI, không có nhãn AIGC, và một bên xem ảnh cho là quay thật, thì đánh dấu "AI hay quay thật bằng máy quay 24p chờ xác nhận" và giới hạn độ tin cậy ở 0.7.
- Chữ OCR đọc được mà danh sách chữ hậu kỳ của VLM không có (hoặc cùng một đoạn chữ di chuyển theo vật thể trong hình) thì tính là chữ trên vật thể, không phải lớp chồng.

## 4. Sản phẩm

```
out/<name>/
  breakdown.json   Video IR (rea_video.breakdown.v1): đặc trưng từng cảnh, bằng chứng, xác suất, lớp chồng, phương án phục dựng
  report.html/md   Báo cáo đọc cho người (cùng một nội dung, HTML được render từ Markdown): kết luận → nội dung và cấu trúc (tóm tắt, hook, timeline cấu trúc, kịch bản) → nhân vật, bối cảnh và đạo cụ →
                   âm thanh (giọng người / nhạc nền / hiệu ứng / âm môi trường, mỗi loại một thẻ) → cách quay, đánh sáng và dựng → lớp đồ họa hậu kỳ → phương án phục dựng (kèm danh sách tư liệu thật và tư liệu tham chiếu) →
                   bảng phân cảnh → điểm chưa chắc chắn → phụ lục (bằng chứng từng cảnh gấp lại, siêu dữ liệu). Nhân vật, bối cảnh, đạo cụ và kịch bản lấy từ phân tích VLM trên cả video hoặc từ agent xem ảnh (cast ở cấp cao nhất của review_answers.json)
  storyboard.jpg   Tổng quan phân cảnh (tô màu theo cách làm)
  shots/           Contact sheet từng cảnh, khung đầu, khung cuối (khung đầu và khung cuối cũng là đầu vào để phục dựng)
  clips/, vlm_cache/  Clip đầu vào VLM và cache (chỉ khi --vlm)
```

`finalize()` có thể phân loại lại chỉ bằng đặc trưng đã lưu và câu trả lời VLM đã có: khi cập nhật luật thì không cần giải mã lại video, `rea-video eval` sẽ tự làm như vậy.
