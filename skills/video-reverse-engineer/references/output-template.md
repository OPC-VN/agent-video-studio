# Bàn giao cho người dùng

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/output-template.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

> **Ghi chú dịch:** `@<ảnh>N` và `@<video>N` là token tham chiếu trong prompt gửi Seedance/Jimeng. Ở bản gốc chúng viết bằng chữ Hán: `@` + hai ký tự U+56FE U+7247 + số cho ảnh, `@` + hai ký tự U+89C6 U+9891 + số cho video. Model chỉ nhận đúng ký tự gốc, nên khi ghép prompt thật phải dùng đúng mã này (xem chuỗi mẫu trong `rea_video/dance.py`).

## Nguyên tắc

- Phản hồi cũng chia hai phần như báo cáo, không trộn lẫn:
  - **Phân rã**: kết luận một câu (video này được làm ra thế nào), hai ba dòng về nội dung và nhân vật (video nói gì, nhân vật / bối cảnh / sản phẩm chính), cấu trúc phân cảnh, dựng và đồ họa hậu kỳ, âm thanh, tư liệu thật, điểm chưa chắc. Viết theo từng cảnh, không gộp các cảnh theo cách sinh.
  - **Phương án phục dựng**: theo mô hình người dùng đã chọn (phần hai của báo cáo, do `rea-video plan` xuất ra). Khi người dùng chưa chọn mà video có cảnh AI, hỏi trước là dùng mô hình nào, đừng tự chọn thay họ rồi lập phương án.
- Phương án phục dựng đưa phần «Làm theo các bước» lên trước: đầu phần hai của báo cáo (mục «Làm theo các bước» trong `video/remake.md` của gói phân rã) đã xếp sẵn các bước theo loại video; thuật lại đúng như vậy và giữ ngắn gọn: mỗi bước một câu, người dùng đọc là bắt tay làm được, còn các số đo để lại trong các mục của báo cáo. Nếu loại video bị phán sai thì nói rõ và đưa các bước theo thứ tự của loại đúng. Ghi rõ phương án được xếp theo những năng lực nào của mô hình nào (câu đầu của phần hai báo cáo).
- Khi có cảnh do AI sinh, nhắc một câu: prompt trong báo cáo là cấu trúc dùng chung, trước khi sinh cần sửa lại một lượt theo hướng dẫn viết prompt chính thức của mô hình đó hoặc theo skill prompt tương ứng.
- Phương án phục dựng viết theo cách tổ chức sản xuất thực tế, không viết lần lượt theo từng cảnh của bản dựng:
  - Cảnh AI → **đơn vị sinh**: mấy cảnh liên tiếp được sinh trong một lần, dùng mô hình nào, tư liệu tham chiếu (`@<ảnh>` sản phẩm / nhân vật, `@<video>` đoạn video gốc), prompt nhiều cảnh đã gộp, và các đơn vị nối với nhau thế nào. Khi engine mặc định không sinh được nhiều cảnh trong một lần, chép nguyên `engine_note` và nói rõ đổi mô hình thì bớt được mấy lần gọi.
  - Cảnh quay thật → **buổi quay**: những cảnh nào cùng bối cảnh, cùng góc máy thì quay chung một lượt; cách đánh sáng của từng bối cảnh; quay cỡ cảnh rộng trước, đặc tả sau. Riêng bảng phân cảnh vẫn viết chi tiết từng cảnh.
  - Cảnh có người diễn → ghi rõ cảm xúc và diễn xuất của từng cảnh được phục dựng thế nào (mục «Diễn xuất và cảm xúc» của báo cáo: biểu cảm, động tác, giọng điệu; và chọn cách nào: chốt biểu cảm bằng khung đầu, lồng tiếng trước rồi dùng tiếng điều khiển hình, chuyển diễn xuất từ video mẫu, hay để diễn viên diễn theo).
  - Render từ code → mấy đoạn dựng hình bằng code, mỗi cảnh ghi rõ phần tử trên hình và hoạt ảnh (timeline hoạt ảnh từng cảnh trong mục «Dựng hình bằng code» của báo cáo: vị trí phần tử, thời điểm xuất hiện, hướng, nhanh chậm, mã màu; ảnh chụp phần tử nằm trong `shots/`); ảnh tĩnh pan/zoom → dựng lại ngay trên máy.
- Khi thiếu prompt (chưa bật VLM), bạn xem ảnh rồi viết bổ sung: trong đáp án của `rea-video review`, mỗi cảnh điền `replication.image_prompt / video_prompt / video_prompt_en`; sau `apply-review`, đơn vị sinh sẽ tự mang theo các prompt này.
- Ghi đường dẫn file báo cáo (`report.html`) cho người dùng. Khi có cảnh render từ code và người dùng muốn phục dựng, nói rõ là phải dùng cả thư mục báo cáo (ảnh chụp phần tử và dải keyframe trong `shots/`, file phụ đề trong `packaging/`); chỉ đưa file HTML hoặc PDF thì thiếu các ảnh chụp rời. Không dán nguyên cả `breakdown.json` vào hội thoại.

## Ngôn ngữ

Ngôn ngữ báo cáo theo `--lang` (zh / en), ngôn ngữ trả lời theo người dùng; thứ tự xét của cả hai xem ở mục "Bàn giao cho người dùng" trong SKILL.md. Khuôn dưới đây ở bản gốc là bản tiếng Trung (zh), ở đây đã dịch sang tiếng Việt; phản hồi bằng tiếng Anh dùng cùng cấu trúc: one-line verdict → content and cast → remake plan → shot list → packaging → audio → material you must supply → open questions → report path.

## Khuôn phản hồi (bản gốc tiếng Trung, đã dịch)

**Kết luận một câu**: sản xuất hỗn hợp — lớp hình nền gồm video AI sinh 62%, template code 30%, quay thật 8%; toàn bộ phụ đề được chồng lên bằng code; có đưa vào 2 ảnh chụp màn hình thật; giọng nữ TTS + BGM pop 110 BPM, các điểm cắt cảnh rơi đúng nhịp nhạc.

**Nội dung và nhân vật**: phim ngắn có cốt truyện, 4 cảnh; nhân vật chính A "Tiểu Hoàng" (hà mã hoạt hình màu vàng, bộ liền thân hồng, đeo túi hồng chéo; xuất hiện suốt video), B bạn trai (cùng bảng màu, #3–#4); bối cảnh S1 đường phố ban ngày. Khi phục dựng, A và B mỗi người cố định một ảnh tham chiếu xuyên suốt mọi đơn vị sinh.

**Bảng phân cảnh**

| # | Thời gian | Thấy được trên khung hình | Lớp chồng (overlay) | Cách làm (suy đoán, độ tin cậy) | Căn cứ suy đoán | Nguồn tư liệu | Hướng phục dựng |
|---|---|---|---|---|---|---|---|
| 1 | 0:00–0:02.5 | Tiểu Hoàng vẫy tay bên đường; ngón tay trái bị méo | Phụ đề, tiêu đề | Video AI (86%) | Khung lặp 24→30 | AI sinh | Khung đầu–cuối bằng capsule-cinema |

"Thấy được trên khung hình" chỉ ghi những gì đối chiếu với ảnh chụp có thể kiểm chứng (nội dung, chuyển động máy, sơ hở); thông số như tốc độ khung, nhiễu, metadata là số đo của công cụ, ghi vào "căn cứ suy đoán", và ghi rõ cách làm là suy đoán. Nếu hai bên không khớp nhau thì ghi ra.

**Cách quay, đánh sáng và dựng** (ghi khi có cảnh quay thật, ứng với mấy dòng khung hình / góc máy / ánh sáng / dựng / hình thức ở cuối `rea-video summary`): hình thức video (nói trước camera / quay trên mặt bàn / vlog), cỡ cảnh và góc máy, cầm tay hay dùng chân máy, số góc máy / bối cảnh; phương án đánh sáng (hướng và độ cao đèn chính, tỉ lệ sáng, ánh mềm hay cứng, nhiệt độ màu, có đèn phụ / đèn viền không, nguồn sáng lọt vào khung); thủ pháp dựng (jump cut để cắt bỏ khoảng lấy hơi, cắt đẩy gần (punch-in), tỉ lệ chèn ảnh chụp màn hình / quay màn hình); kèm một danh sách thiết bị để phục dựng. Khi số đo và kết luận xem ảnh của bạn mâu thuẫn, ghi rõ căn cứ.

**Dựng và đồ họa hậu kỳ**: phụ đề (mấy câu, vị trí, màu / viền / khung nền, tô nổi từ khóa, kiểu xuất hiện, đường dẫn file SRT/ASS); chữ nhấn (chữ to, có màu và viền, bật lên để nhấn ý), tiêu đề, thẻ chương, nhãn bám theo vật thể (thời gian, nội dung chữ, kiểu, hoạt ảnh); sticker / GIF / meme / hình trong hình (PiP) (thời gian, vị trí, dán cái gì, có lặp không); hiệu ứng âm thanh nào rơi đúng lúc chữ bật lên hoặc sticker xuất hiện; chữ nhấn / sticker đi theo câu thoại nào («Định vị theo lời thoại»), cái nào là lớp thường trực. Phần nào công cụ không đo được mà bạn xem ảnh bổ sung thì ghi rõ.

**Âm thanh**: giọng người (TTS hay người thật, chất giọng; lời thoại xem bảng kịch bản trong báo cáo) / BGM (đoán tên bài, phong cách, BPM, tông, nguồn và rủi ro bản quyền, các đoạn) / hiệu ứng âm thanh (thời điểm → sự kiện tương ứng trên hình) / trộn âm (có hạ nhạc xuống khi có giọng không). Trong mục «Âm thanh» của báo cáo, mỗi hạng mục là một thẻ; chép theo là được.

**Tư liệu thật cần bạn cung cấp**: ảnh chụp màn hình trang GitHub ở giữa cảnh #4……

**Phương án phục dựng**: viết theo `production_plan`. Cảnh AI viết theo đơn vị sinh (phạm vi cảnh, mô hình, tư liệu tham chiếu, prompt nhiều cảnh, cách nối); cảnh quay thật viết theo buổi quay (bối cảnh → góc máy → cảnh, cách đánh sáng); render từ code thì ghi mấy đoạn dựng hình bằng code, mỗi đoạn làm theo cách nào, và trỏ tới timeline hoạt ảnh từng cảnh cùng ảnh chụp phần tử; ảnh tĩnh pan/zoom chỉ cần một câu. Thao tác nào tốn phí thì xác nhận trước.

> Ví dụ: 8 cảnh AI → 3 đơn vị sinh, 3 lần gọi Seedance 2.5 (Seedance 2.0 mặc định không sinh được nhiều cảnh trong một lần, làm từng cảnh thì phải gọi 8 lần). G1 #1–#5 (9.0s): @<ảnh>1 ảnh sản phẩm + @<video>1 video gốc 0–9s, sinh một lần ra 5 cảnh……

**Điểm chưa chắc**: #7 quay thật hay AI chờ xác nhận (nghiêng về AI 64%): không có tay và chữ để phán đoán, đề nghị……

**Báo cáo**: out/ref/report.html

**VLM**: chép nguyên dòng `VLM:` của `rea-video summary` (đã có hiệu lực / có hiệu lực một phần / toàn bộ gọi thất bại / chưa cấu hình / chưa bật). Nếu chưa có hiệu lực, và bạn cũng không xem được ảnh, thêm một câu gợi ý: "cấu hình một mô hình đa phương thức bất kỳ (REA_VLM_BASE_URL / REA_VLM_API_KEY / REA_VLM_MODEL) rồi chạy lại với --vlm, phán đoán quay thật / AI / 3D sẽ chính xác hơn." Nếu bạn xem được ảnh thì chỉ cần ghi "agent đã xem ảnh để review".
