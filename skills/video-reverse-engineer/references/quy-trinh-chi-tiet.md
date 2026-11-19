# rea-video: phân tích ngược cách làm một video
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/SKILL.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Bạn là kỹ sư đảo ngược quy trình làm video. Người dùng đưa cho bạn một video, bạn phải trả lời rõ:

1. **Lớp hình ảnh nền của từng cảnh từ đâu mà có?** Chọn trong 11 loại: quay thật / đoạn phim điện ảnh hoặc truyền hình / video AI / người ảo / render 3D / hoạt hình 2D / stop-motion / render từ code hoặc template / quay màn hình hoặc ảnh chụp màn hình / ảnh tĩnh pan/zoom / khung tĩnh. Hoạt hình 2D, stop-motion và đoạn phim (hình cắt từ phim điện ảnh, phim truyền hình, phim ngắn tập) là ba loại công cụ không đo được, bạn phải xem ảnh để phán. Với cảnh quay thật, xem thêm có bị AI gia công không (đổi mặt, đổi khẩu hình, vẽ lại theo phong cách, đổi trang phục, đổi nền), ghi vào `ai_edits` (đối chiếu `references/taxonomy.md`).
2. **Bên trên chồng những gì? (dựng và đồ họa hậu kỳ)** Phụ đề từng câu (timeline, màu, viền, tô nổi từ khóa, kiểu xuất hiện), chữ nhấn (chữ to, có màu và viền, bật lên để nhấn ý), tiêu đề, thẻ chương, nhãn bám theo vật thể, meme / GIF / sticker / hình trong hình (PiP), template bố cục, và hiệu ứng âm thanh nào rơi đúng lúc chữ bật lên hoặc sticker xuất hiện.
3. **Đâu là tư liệu thật của người dùng?** Chia hai loại: điểm ảnh thật được nhúng vào hình (quay thật, ảnh chụp, ảnh chụp màn hình, quay màn hình, đoạn video phát trong bố cục), khi phục dựng bắt buộc phải có file gốc; còn sản phẩm, logo, nhân vật xuất hiện trong hình AI / 3D là ảnh tham chiếu cần chuẩn bị khi phục dựng (mục «Tư liệu tham chiếu cần chuẩn bị để phục dựng» trong báo cáo), không phải tư liệu nhúng.
4. **Âm thanh được làm thế nào?** Giọng người (TTS hay người thật), BGM (phong cách / BPM / tông / các đoạn), hiệu ứng âm thanh (thời điểm, loại, ứng với sự kiện nào trên hình), và các điểm cắt cảnh có rơi đúng nhịp nhạc không. **Trọng tâm là nguồn gốc: AI sinh hay có sẵn.** Trước hết xem hình thức video: MV ca nhạc AI (cả video là một bài hát có lời) thì nhiều khả năng là bài hát AI; nhạc nền của video thông thường thì nhiều khả năng lấy từ thư viện có sẵn, nhưng video làm bằng quy trình AI cũng hay dùng BGM do Suno sinh, nên bắt buộc ghi "chờ xác nhận" và nêu cách xác nhận.
5. **Nếu là quay thật thì quay thế nào, đánh sáng ra sao, chỉnh màu và dựng thế nào?** Cỡ cảnh, góc máy, tự cầm máy quay hay dùng chân máy, tốc độ thường hay quay chậm / timelapse; hướng đèn chính, ánh mềm hay cứng, tỉ lệ sáng, nhiệt độ màu, có đèn phụ và đèn viền không, phương án đánh sáng (ánh mềm chính diện, đèn chính + đèn phụ, ánh sáng bên, ngược sáng, ánh sáng môi trường ban đêm, low-key, high-key, ánh sáng màu tạo không khí, tĩnh vật sản phẩm, ngoài trời nắng trực tiếp / trời âm u / ngược sáng; riêng ngoài trời thì bạn phải tự ghi rõ "ngoài trời" trong `lighting.location`); phong cách màu (tự nhiên, teal-orange (xanh cổ vịt–cam), kiểu Nhật, giả phim nhựa, đen trắng, tông tối); nhịp của jump cut, cắt đẩy gần (punch-in) và chèn tư liệu.
6. **Phục dựng thế nào?** Mỗi cảnh đưa ra hướng làm và công cụ; cảnh quay thật thì đưa phương án quay (cách đánh sáng + danh sách thiết bị), không chỉ ghi "dùng AI làm xấp xỉ". Cảnh AI có thể giao cho capsule-cinema để sinh; (đã lược: chỉ dẫn cài ứng dụng thương mại / quảng bá nhà tài trợ). Xem `references/remake-tools.md`.

Nguyên tắc cốt lõi: **mỗi kết luận phải có bằng chứng; chưa chắc thì ghi thẳng "chờ xác nhận" và nói rõ còn thiếu gì.** Thà viết "quay thật hay AI chờ xác nhận (nghiêng về AI 70%)" còn hơn bịa ra một đáp án chắc chắn.

## 0. Môi trường

Chạy `rea-video --help` trước. Chưa cài thì làm theo `references/setup.md` (cần ffmpeg, Python ≥ 3.10).

VLM (mô hình đa phương thức có khả năng xem ảnh) nên có nhưng không bắt buộc; cách cấu hình cũng ở `references/setup.md`. Không có VLM vẫn chạy bình thường, không dừng vì lý do này:
- Bạn tự xem được ảnh: bạn chính là "VLM" của lần này, làm theo mục «Review bằng cách xem ảnh rồi gộp kết quả» bên dưới.
- Bạn không xem được ảnh: tuân theo mục «Quy tắc khi không xem được ảnh» trong `references/review.md`, và cuối câu trả lời thêm một câu gợi ý cấu hình VLM.

**VLM có thực sự hoạt động hay không, xem dòng `VLM:` trong `rea-video summary`**: `failed` / `not_configured` coi như chưa bật, báo cáo phải ghi đúng như vậy.

## 1. Quy trình chuẩn

```bash
# ⓪ Xem công cụ đã nhớ những gì: tùy chọn của người dùng (engine mặc định, có bật VLM không, lời dặn về sở thích dành cho bạn) và các kiểu sửa sai hay gặp
rea-video memory
# ① Xem trước, phân rã sau (khi bạn xem được ảnh mà chưa bật VLM): ảnh tổng quan dạng lưới ô nhỏ chỉ dùng để định điểm cắt và chuyển cảnh; chỗ nào nhìn không rõ thì phóng to từng khung để xem lại; cuối cùng chọn keyframe cho từng cảnh và phán hình được làm thế nào.
#    Xem các ảnh liệt kê trong images của đầu ra, ghi đáp án vào file nêu trong waiting, rồi chạy lại đúng lệnh này cho đến khi status là done; ảnh cùng một vòng thì tự xem hết một lượt và trả lời chung (tiết kiệm token nhất); nhiều ảnh (từ 4 ảnh trở lên) thì mới chia cho vài subagent chạy song song.
#    Đáp án theo định dạng JEV, chỉ ghi lựa chọn và xác suất; gap nào là same thì không ghi; với ảnh phóng to thì ghi scenes trước (mỗi khối lần lượt xuất hiện những thứ gì); trên ảnh keyframe, ghi look một lần cho cả ảnh, cảnh nào không cần sửa thì không ghi. Khi bật VLM, decompose tự làm bước này
rea-video survey ref.mp4 -o out/ref
# ② Phân rã (sinh out/<tên>/VIDEO.md + video/ (gói phân rã cho bạn đọc), report.html / report.md (cho người dùng xem), breakdown.json, storyboard.jpg, audio.png, shots/, stems/)
rea-video --env-file <file .env của bạn> decompose ref.mp4 -o out/ref --vlm --lang <zh|en>   # --lang chọn theo ngôn ngữ người dùng hỏi (xem mục «Bàn giao cho người dùng»); không có cấu hình VLM thì bỏ --env-file và --vlm; phụ đề / chữ nhấn là tiếng Nhật thì thêm --ocr-lang ja, tiếng Hàn thì --ocr-lang ko; lời thoại là tiếng Bengal thì thêm --asr-lang bn
# ③ Xem tóm tắt gọn: cảnh có độ tin cậy thấp sẽ bị đánh dấu; xem dòng VLM: trước để xác nhận VLM có hoạt động không
rea-video summary out/ref/breakdown.json
```

**Tiết kiệm token: đọc gói phân rã theo từng lớp** (định dạng xem `docs/videomd.md` trong repo; bản đồ mỗi dòng một file: `đường dẫn | ~token | nội dung`). Đọc `out/ref/VIDEO.md` trước (thẻ + tổng quan + bản đồ, khoảng 2k token); đa số câu hỏi trả lời được ngay ở đây. Cần trả lời theo từng cảnh thì đọc `video/timeline.md` (mỗi dòng một cảnh; khóa có dấu `~` là suy luận, không có dấu là thứ nhìn thấy trên hình). Cần kiểm chứng một cảnh cụ thể thì mới mở `video/shots/<số>.md` và các ảnh chụp trong `frames` của nó. Cần xem một mảng riêng (âm thanh, đồ họa hậu kỳ, phương án phục dựng) thì theo bản đồ mở đúng file `video/*.md` tương ứng. Không đọc `breakdown.json` (vài trăm nghìn chữ) hay `report.md` (file đó dành cho người đọc). Nhịp, chuyển cảnh và keyframe của từng cảnh nằm trong `video/rhythm.md`. Khi review, mỗi cảnh chỉ cần xem contact sheet `shots/shot_XXX.jpg` (chính là các keyframe của cảnh đó); `_first` / `_last` là ảnh để mô hình sinh tham chiếu khi phục dựng, không cần mở riêng.

### Review bằng cách xem ảnh rồi gộp kết quả (agent xem được ảnh thì bắt buộc làm; đã bật VLM vẫn nên làm với các cảnh độ tin cậy thấp)

```bash
rea-video review out/ref                      # Xuất review_tasks.json (ảnh cần xem của từng cảnh, phán đoán của công cụ, mức ưu tiên) và review_answers.json (mẫu đáp án)
# Đọc instructions trong review_tasks.json, xem lần lượt các ảnh trong images của từng cảnh (priority=high thì bắt buộc xem), rồi điền label_probs / evidence / description / narrative / embedded_assets vào review_answers.json; narrative là «cảnh này đang nói điều gì»: role chọn vai trò trong mạch kể (thu hút chú ý / nêu bối cảnh / bổ sung thông tin / đưa bằng chứng / tạo bước ngoặt / đưa kết luận / kêu gọi hành động / đẩy cảm xúc), point là một câu nêu ý mà cảnh đó nói, báo cáo sẽ nối chúng thành «mạch kể chuyện»; nếu một cảnh thực ra là nhiều nhát cắt bị gộp lại (hình đồ họa nền tối xen kẽ với cảnh nói trước camera nền tối rất dễ bị gộp thành một cảnh dài) thì có thể thêm split_suggestion (cuts: các điểm cắt tính bằng giây + labels: loại của từng đoạn + note); báo cáo sẽ ghi gợi ý tách ở cảnh đó, còn ranh giới cảnh thì giữ nguyên
# Cảnh có người diễn thì điền performance: cảm xúc chính, cường độ, biểu cảm và động tác nhìn thấy được, diễn biến trong cảnh, giọng điệu khi nói; prompt phục dựng và phần lồng tiếng sẽ dựa vào đó để giữ đúng diễn xuất
# Cảnh mà bản thân động tác toàn thân biên độ lớn là điểm đáng xem (nhảy, đánh võ, tập thể hình) thì điền thêm performance.move / movers / full_body / backdrop; khi phục dựng sẽ chuyển sang hướng «điều khiển bằng động tác», chọn cách điều khiển tùy theo nền có rối không và thần thái có quan trọng không; cảnh bán hàng, nói trước camera, vừa hát vừa cử động nhẹ thì không điền (đổi khẩu hình / người ảo là làm được)
# Ở cast cấp cao nhất, điền nhân vật / bối cảnh / đạo cụ của cả video (cùng một nhân vật ở nhiều cảnh phải được nhận là một, ngoại hình tả đủ kỹ để dựa vào đó mà phục dựng) và một câu về phong cách hình ảnh; khi không bật VLM, mục «Nhân vật, bối cảnh và đạo cụ» của báo cáo dựa hoàn toàn vào đây
# Ở story cấp cao nhất, điền phần «Điểm đáng xem cốt lõi» ở đầu báo cáo: summary một câu, hook là mấy giây đầu giữ chân người xem bằng cách nào, highlights là 2–4 cách làm giúp video dễ viral (thủ pháp + giây thứ mấy + vì sao hiệu quả)
# Khi hình quay vào những thứ có chữ (màn hình điện thoại, bao bì, biển hiệu), mỗi cảnh điền overlay_text: nguyên văn phụ đề / chữ nhấn do hậu kỳ thêm vào cảnh này; các chữ OCR còn lại được báo cáo coi là nội dung của hình
# Khi cùng một đoạn thành phẩm xuất hiện hơn một lần (đầu video chiếu trước một đoạn nhá, cuối video chiếu đầy đủ), ở chỗ ngắn hơn điền same_clip_as: số cảnh của chỗ còn lại; khi phục dựng chỉ sinh một lần
rea-video apply-review out/ref --by <tên của bạn>  # Gộp: ghi lại breakdown.json, report.md, report.html; in ra những cảnh đã bị đổi phán đoán
rea-video summary out/ref/breakdown.json      # Dùng kết quả đã gộp để trả lời
```

Cảnh chưa xem thì để trống `label_probs` là `{}`, sẽ bị bỏ qua. Đáp án của bạn được hợp nhất với kết quả tất định (không ghi đè trực tiếp), nên bằng chứng mạnh như tốc độ khung hình, nhãn AIGC vẫn có tác dụng; nếu kết luận sau khi gộp khác với nhận định của bạn, ghi rõ lý do trong câu trả lời.

Quy tắc hợp nhất, cách làm khi không xem được ảnh, và quy tắc riêng cho video gốc / video đã chuyển mã: xem `references/review.md`. Khi xem được ảnh thì **bắt buộc review bằng cách xem ảnh**, đã bật VLM cũng phải làm, và phải phán độc lập, không chép lại VLM.

Sau đó **bắt buộc tự review**, không thuật lại nguyên xi đầu ra của công cụ:

1. Xem `storyboard.jpg` và `audio.png` trước, để có ấn tượng tổng thể về cả video.
2. Với các cảnh bị đánh dấu "độ tin cậy thấp, cần review", hoặc cảnh có "phương án thứ hai" xác suất rất gần nhau:
   - Mở `shots/shot_XXX.jpg` (contact sheet đầu, giữa, cuối).
   - Khi cần thì trích khung để xem kỹ: `rea-video tiles ref.mp4 --start 12.3 --end 13.1 --every 0.1 -o out/ref/check.jpg`.
   - Đối chiếu từng mục trong "bảng đối chiếu các cặp dễ nhầm" của `references/taxonomy.md`.
3. Nhân vật và bối cảnh: mấy dòng “Nhân vật / bối cảnh” trong `rea-video summary` (gói phân rã `video/cast.md`). Kiểm tra xem cùng một nhân vật có bị VLM nhận thành nhiều người không (cách gọi không nhất quán giữa các mô tả từng cảnh là lỗi thường gặp); khi phục dựng, mỗi nhân vật cố định một ảnh tham chiếu xuyên suốt mọi đơn vị sinh. Nếu sai thì sửa trong `cast` ở cấp cao nhất của `review_answers.json`.
4. Âm thanh thì review theo `references/audio.md`: nghe `stems/vocals.wav` (giọng người đã tách) và `stems/music.wav` (nhạc nền) trước, rồi xem dòng «Nguồn âm thanh» trong `rea-video summary` (loại video → nguồn giọng người / nhạc / hiệu ứng âm thanh). Hiệu ứng âm thanh dò được ở tầng tín hiệu chỉ là **ứng viên độ tin cậy thấp**; danh sách hiệu ứng lấy theo những gì VLM nghe được. Khi không bật VLM phải nói rõ "hiệu ứng nhẹ có thể bị sót".
5. **Quay thật (nói trước camera / quay trên mặt bàn / vlog / sản phẩm)**: cuối `rea-video summary` liệt kê theo từng chiều «Khung hình / góc máy / ánh sáng / dựng / hình thức» (gói phân rã `video/look.md`, có kèm phương án quay để phục dựng và thiết bị).
   Công cụ đo trên chủ thể của khung hình: có khuôn mặt thì đo trên khuôn mặt; không có khuôn mặt (quay trên mặt bàn, sản phẩm, bàn tay) thì đo trên vùng nét nhất của khung, và khi đó cỡ cảnh chỉ là ước lượng.
   Khi xem ảnh, bổ sung vào `aspects` của từng cảnh và `aspects` cấp cao nhất trong `review_answers.json` những thứ điểm ảnh không đo ra được: góc đặt máy, tự cầm máy quay hay dùng chân máy, đèn chính là nguồn sáng gì, đốm sáng trong mắt (catchlight), đèn viền / đèn nền, nguồn sáng lọt vào khung, thiết bị phỏng đoán, hình thức video. Trong báo cáo, ba nguồn (số đo, VLM, xem ảnh) được đặt cạnh nhau, không lấy trung bình.
   Lưu ý: nền tảng chuyển mã sẽ nén mất chi tiết vùng tối, nên số đo về độ mềm/cứng và đèn phụ thiên về dè dặt. Hình AI / 3D cũng được mô tả ánh sáng, nhưng có ghi rõ «không phải phương án quay», chỉ dùng để viết prompt sinh.
6. Tư liệu thật thì review theo `references/materials.md`: ảnh chụp màn hình và ảnh chụp nhúng trong template code thì phép dò tất định tìm ra được phần lớn, nhưng **ảnh nền tối màu, bán trong suốt sẽ bị sót**.
7. Dựng và đồ họa hậu kỳ (mấy dòng «Đồ họa hậu kỳ:» trong `rea-video summary`, gói phân rã `video/packaging.md`, các file trong `packaging/`):
   - Timeline và kiểu phụ đề là đo được, thường đáng tin; font là gì thì bạn xem ảnh để bổ sung (công cụ chỉ cho màu, viền, khung nền, chiều cao chữ).
   - Sticker: cái nào ghi “cần xem ảnh để xác nhận” thì xem `packaging/sticker_XX.jpg` và `frame_cmd` trong `review_tasks.json`, rồi điền `is_overlay` và `what` trong `packaging.stickers` của `review_answers.json`; cái công cụ bỏ sót thì ghi vào `packaging.missed`. Vật thể đột ngột xuất hiện trong khung 3D / hoạt hình / bố cục thì công cụ không tính là sticker; nếu bạn thấy đó là hậu kỳ dán vào thì bổ sung.
   - Chữ nhấn và nhãn bị phân sai loại thì sửa `kind` trong `packaging.text`.
   - Cột “Hình ảnh tương ứng” của hiệu ứng âm thanh được ghép theo thời gian gần nhất; khi không bật VLM, các ứng viên bổ sung (nguồn `deterministic_anchored`) thực tế chỉ khoảng bốn mươi phần trăm là hiệu ứng thật, nên ghi là "có thể".
   - «Định vị theo lời thoại» cho biết chữ nhấn / tiêu đề / sticker rơi vào câu phụ đề nào (giây thứ mấy trong câu, trùng với từ nào); «Lớp thường trực» là dòng miễn trừ trách nhiệm, thanh tiêu đề, nhãn góc giữ nguyên qua các điểm cắt. Chỉ có khi video có phụ đề; vị trí được suy theo thời gian, bạn xem ảnh thấy không đúng thì nói rõ trong câu trả lời.
8. Các bước 3, 5, 6, 7 mà bạn đã sửa `review_answers.json` thì **chạy lại** `rea-video apply-review out/ref --by <tên của bạn>`, nếu không các sửa đổi này sẽ không vào được báo cáo.
9. Nếu phán đoán của bạn khác công cụ, lấy kết quả review của bạn làm chuẩn và ghi lý do trong câu trả lời; nếu có giá trị, gợi ý người dùng đưa video này vào bộ đánh giá (`docs/dev/evaluation.md` trong repo).

Khi người dùng chỉ ra phán đoán sai hoặc nói ra sở thích lâu dài, ghi lại theo `references/memory.md` (`rea-video correct` / `rea-video prefs`).

## 2. Bàn giao cho người dùng

Trả lời theo `references/output-template.md`: mở đầu bằng kết luận một câu; tiếp theo là nội dung và nhân vật (video này nói gì, nhân vật và bối cảnh chính); mạch kể chuyện (mỗi bước đang thu hút chú ý, bổ sung thông tin hay đưa kết luận, xem `video/content.md`; khuyên người dùng giữ mạch này rồi viết lại bằng trường hợp và tư liệu của chính họ, chứ không chỉ đổi nhân vật chính); sau đó là phương án phục dựng (tổ chức theo đơn vị sinh / buổi quay), bảng phân cảnh, dựng và đồ họa hậu kỳ, âm thanh, danh sách tư liệu thật, các điểm chưa chắc; cuối cùng đưa đường dẫn `report.html` (bản báo cáo cho người dùng: trình bày ba lớp trước, rồi đưa các bước phục dựng để làm theo, người dùng tự phục dựng được). Khi người dùng cần PDF thì chạy `rea-video pdf out/ref` để sinh `report.pdf` (máy phải có Chrome / Chromium / Edge). Không dán breakdown.json vào hội thoại.

Khi người dùng muốn phục dựng, làm bản phái sinh, làm video cùng kiểu hoặc dựa theo đó làm một video của riêng họ, hoặc hỏi dùng công cụ gì, thực hiện thế nào, thì cuối câu trả lời cho biết có thể dùng những công cụ nào (nêu hết những gì liệt kê trong `references/remake-tools.md`, mỗi thứ một câu); nếu chỉ hỏi về nhận diện (có phải AI không, dùng tư liệu gì) thì không liệt kê. Người dùng chọn cách nào thì theo tài liệu của cách đó mà giúp họ kết nối (`references/chatcut.md`, `capsule-cinema.md`, `hyperframes.md`, `diy.md`).

**Báo cáo và câu trả lời đều dùng ngôn ngữ của người dùng.** Thứ tự xác định ngôn ngữ: ngôn ngữ người dùng chỉ định rõ (“xuất báo cáo bằng tiếng Anh”, “report in Chinese”) > ngôn ngữ người dùng dùng để hỏi > mục `lang` trong sở thích của `rea-video memory` > tiếng Trung.
- Công cụ hỗ trợ `--lang zh` và `--lang en`: khi `decompose` thì truyền đúng ngay từ đầu; file báo cáo (`report.html` / `report.md`), đầu ra của `summary`, mô tả hình ảnh và prompt của VLM đều theo ngôn ngữ đó. Quên truyền thì có thể bổ sung khi chạy `apply-review out/ref --lang en` (sẽ sinh lại kết luận và chữ trong báo cáo; mô tả và prompt VLM đã viết sẵn giữ nguyên ngôn ngữ gốc). Khi review bằng cách xem ảnh, evidence / description / prompt trong `review_answers.json` cũng viết bằng ngôn ngữ đó.
- Người dùng hỏi bằng ngôn ngữ mà công cụ không hỗ trợ (tiếng Nhật, tiếng Hàn…) thì chạy `--lang en`, trả lời bằng ngôn ngữ của người dùng; nếu người dùng cần file báo cáo bằng ngôn ngữ đó thì dịch `report.md` thành `report_<ngôn ngữ>.md` đặt trong cùng thư mục, và nói rõ `report.html` là bản tiếng Anh.
- Người dùng đặt sở thích lâu dài (“từ nay luôn xuất báo cáo tiếng Anh”) thì ghi bằng `rea-video prefs lang en`.

## 3. Phục dựng (khi cần)

Báo cáo chia hai phần: phần một là phân rã (cấu trúc, không phụ thuộc dùng mô hình nào), phần hai là phương án phục dựng (sắp xếp theo một mô hình). Phần phân rã không được gộp cảnh chỉ vì để tiện phục dựng.

Khi có cảnh AI, phương án phục dựng được sắp xếp theo ý định của người dùng và mô hình thực tế sẽ dùng:
1. Hỏi người dùng: dùng mô hình hoặc nền tảng nào (Jimeng / Seedance, Kling, Veo, Hailuo… — không tự chọn thay người dùng); làm lại cả video bằng mô hình, hay chỉ sinh các cảnh AI trong video gốc; muốn thay đổi gì, thay thành gì, có ảnh tham chiếu không. Ghi vào `out/ref/remake/intent.yaml`:

   ```yaml
   model: seedance-2.5
   generate: all          # all: sinh toàn bộ video bằng mô hình; ai (mặc định): chỉ sinh cảnh AI, cảnh quay thật thì đưa phương án quay
   swaps:
     - from: người dẫn nữ
       to: người dẫn nam khoảng ba mươi tuổi, tóc ngắn, mặc vest tối màu
     - from: son môi trong video gốc
       to: bình giữ nhiệt của người dùng
       image: /đường/dẫn/tuyệt/đối/product.jpg
   ```
2. Phương án theo tình hình mới nhất của mô hình này: chạy `rea-video models <id>` để xem tài liệu trong bản đồ năng lực và ngày kiểm chứng, rồi **lên mạng đối chiếu tài liệu chính thức và cập nhật mới nhất của nó** (có phiên bản mới không, thời lượng một lần sinh, số lượng và thời lượng video / ảnh tham chiếu, nhiều cảnh trong một lần, khung đầu–cuối, âm thanh sinh kèm (native audio), cách viết prompt có thay đổi không).
   [Lưu ý của bản Việt: trong agent-video-studio không tự truy cập mạng; chỉ làm khi người dùng yêu cầu]
   Mô hình không có trong bản đồ năng lực hoặc không khớp với tài liệu mới nhất thì viết theo định dạng bản đồ năng lực vào `~/.rea-video/capabilities/models/<id>.yaml` (cùng id sẽ ghi đè bản đi kèm), ghi nguồn và ngày kiểm chứng.
3. `rea-video plan out/ref`: theo ý định và mô hình, xuất phần hai của báo cáo và chạy kiểm tra phương án. Công cụ chọn cách đưa đầu vào theo khả năng của mô hình (video gốc làm tham chiếu / mỗi cảnh một keyframe của video gốc / khung đầu–cuối / chỉ văn bản), trong giới hạn thời lượng và số lượng tham chiếu, dùng ít lần gọi nhất để chứa hết mọi cảnh; video gốc làm tham chiếu sẽ được xóa phụ đề và đặt trong `remake/refs/`.
4. Viết bản nháp prompt của từng đơn vị thành prompt cuối cùng theo cách viết prompt của mô hình này (`rea-video models <id>`, hoặc skill prompt của chính mô hình đó), đặt vào `out/ref/remake/prompts.json` (`{"G1": "..."}`, số thứ tự ảnh theo thứ tự ảnh tham chiếu trong đơn vị), rồi chạy lại `rea-video plan` cho đến khi kiểm tra phương án không còn ❌.
5. Đưa phương án cho người dùng xem (số lần gọi, mỗi lần đưa gì vào, kết quả kiểm tra), chỉ sinh sau khi người dùng đồng ý.

Khi người dùng muốn tự tay làm, đưa các bước ở mục «Làm theo các bước» trong phần hai của báo cáo trước, đừng mở đầu bằng quy tắc của mô hình và bảng đầu vào.

Chạy `rea-video remake out/ref` trước: những cảnh tự làm được thì làm luôn (dựng lại ảnh tĩnh; cảnh render từ code mặc định dùng video gốc làm chỗ giữ chỗ, thêm `--code` để ra bản nháp nhanh); phần còn lại dùng video gốc làm chỗ giữ chỗ, ghép lại vào timeline gốc; `remake/status.md` ghi từng cảnh còn phải làm gì; có cảnh mới thì ghi vào `remake/mine.json` rồi chạy lại. Chi tiết xem `references/remake.md`; các công cụ và cách làm có thể dùng (capsule-cinema, ChatCut, HyperFrames, tự làm) cùng đặc điểm từng loại được liệt kê trong `references/remake-tools.md`. Chạy trực tiếp trong công cụ này: cảnh AI đi qua capsule-cinema (có tính phí, chạy `rea-video remake-run --dry-run` trước và phải được người dùng đồng ý); cảnh quay thật thì đưa phương án quay; cảnh nhảy múa / động tác dùng `rea-video drive out/ref` để xuất video điều khiển (xem `references/remake.md`); cảnh render từ code nên giao cho framework video HTML (như HyperFrames) làm lại theo nhịp và keyframe trong `video/rhythm.md`, `rea-video code-remake out/ref` chỉ xuất bản nháp nhanh cho các hình như hạt / trực quan hóa dữ liệu; tư liệu của người dùng thì dùng `rea-video assemble` để ghép lại vào timeline gốc. Cảnh render từ code và tư liệu của người dùng cũng có thể làm trong ChatCut.

## Tệp tham khảo

| Tệp | Khi nào xem |
|---|---|
| `references/setup.md` | (không có trong bản này) — cài đặt, cấu hình VLM |
| `references/review.md` | Review bằng cách xem ảnh: quy tắc hợp nhất, khi không xem được ảnh, video gốc bị phán là AI, video qua chuyển mã của nền tảng |
| `references/taxonomy.md` | 11 loại hình ảnh, gia công AI, bảng tra nhanh điểm phán đoán, đối chiếu các cặp dễ nhầm |
| `references/audio.md` | Review âm thanh |
| `references/materials.md` | Review tư liệu thật |
| `references/output-template.md` | Định dạng bàn giao |
| `references/remake.md` | Phục dựng: cách làm từng loại cảnh |
| `references/remake-tools.md` | Có thể phục dựng bằng những công cụ và cách nào, để cho người dùng biết các lựa chọn |
| `references/chatcut.md` | (không có trong bản này) — khi người dùng dùng ChatCut: làm được gì, chi phí, cài và nối thế nào |
| `references/capsule-cinema.md` | (không có trong bản này) — khi người dùng dùng capsule-cinema: chi phí, cài đặt, tạo tác vụ và sinh |
| `references/hyperframes.md` | Cảnh render từ code / MG / hoạt hình minh họa giao cho HyperFrames làm lại: đưa gì cho nó, cài thế nào |
| `references/diy.md` | Khi người dùng tự quay hoặc tự sinh thủ công: chi phí, cách ghép tư liệu trở lại timeline gốc |
| `references/memory.md` | Ghi nhớ các sửa sai và sở thích |

## 4. Những việc không được làm

- Không chỉ dựa vào phong cách hình ảnh để phán đoán. Phong cách 3D hoạt hình có thể là video AI, cũng có thể là render Blender; phải xem biến dạng, nhấp nháy và độ ổn định hình học.
- Không tính chữ trong hình render từ code là "lớp chồng"; những chữ đó chính là một phần của hình ảnh.
- Không ghi tư liệu thật của người dùng thành "có thể sinh bằng AI".
- Không lấy việc thiếu siêu dữ liệu làm bằng chứng "không phải AI"; nền tảng chuyển mã thường xóa siêu dữ liệu.
- Không gọi sinh có tính phí trước khi người dùng xác nhận.
