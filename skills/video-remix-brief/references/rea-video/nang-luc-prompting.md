# Cách viết prompt và yêu cầu khung hình của từng mô hình
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/prompting.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

> **Ghi chú dịch:** `@<ảnh>N` và `@<video>N` là token tham chiếu trong prompt gửi Seedance/Jimeng. Ở bản gốc chúng viết bằng chữ Hán: `@` + hai ký tự U+56FE U+7247 + số cho ảnh, `@` + hai ký tự U+89C6 U+9891 + số cho video. Model chỉ nhận đúng ký tự gốc, nên khi ghép prompt thật phải dùng đúng mã này (xem chuỗi mẫu trong `rea_video/dance.py`).

> Đánh chỉ mục theo id mô hình (id xem trong `models/*.yaml`). Khi viết prompt phục dựng cho một mô hình, hãy sửa theo cách viết ở đây: `rea-video models <id>`.
> Nội dung lấy từ hướng dẫn prompt của nhà cung cấp và hướng dẫn bên thứ ba; chưa được kiểm thử từng mục. `basis` ghi nguồn chính; `unverified` liệt kê những chỗ chưa xác minh hoặc nguồn mâu thuẫn.

**Các trường:** structure (cấu trúc) · language (ngôn ngữ) · length (độ dài) · multi_shot (nhiều cảnh và thời gian) · references (cách chỉ tham chiếu) · dialogue (lời thoại và âm thanh) · negatives (viết nội dung không muốn có) · camera (máy quay) · frame_mode (nội dung viết ở chế độ khung đầu / đầu–cuối) · frames (yêu cầu với ảnh khung và ảnh tham chiếu) · rewriter (công tắc tự viết lại) · pitfalls (vấn đề đã biết) · unverified (chưa kiểm chứng) · sources (nguồn)

---

## Kỹ thuật keyframe chung (keyframes)

- Chế độ khung đầu: phần chữ chỉ viết chuyển động và máy quay; không lặp lại mô tả những thứ đã có trong khung. Lặp lại sẽ làm yếu chuyển động (hướng dẫn của Runway, Google, Wan, Hunyuan, Kling, Hailuo đều thống nhất; Wan 3.0 là ngoại lệ, được viết cả cốt truyện và lời thoại).
- Mô hình quyết định khung hình đầu ra (Seedance 2.5, Wan): cắt ảnh khung đầu theo tỷ lệ đích trước; khung đầu và khung cuối phải cùng kích thước, nếu không khung cuối sẽ bị kéo giãn hoặc cắt.
- Độ phân giải ảnh khung không thấp hơn độ phân giải đầu ra; tránh khung đang mờ dần, chuyển cảnh và khung bị mờ chuyển động; tay và mặt mờ sẽ bị phóng đại khi sinh.
- Xoá phụ đề, chữ nhấn, logo, watermark trong khung trước khi dùng, chữ và logo thêm lại ở hậu kỳ; chữ nhỏ sẽ biến dạng khi chuyển động.
- Chọn khung đầu ở một tư thế có thể tiếp tục chuyển động; khung ở đỉnh động tác không còn chỗ để đi tiếp. Máy muốn đẩy vào thì lấy khung đầu rộng hơn; chủ thể sắp đi về phía nào thì chừa khoảng trống ở phía đó.
- Khung đầu–cuối giữ cùng bố cục và chủ thể, chỉ thay đổi một điểm; khác quá nhiều sẽ bị coi là cắt cảnh hoặc biến dạng (Kling chính thức: hai khung nên giống nhau nhất có thể). Khác biệt lớn thì tách thành hai đoạn.
- Nối khung cuối đoạn trước làm khung đầu đoạn sau sẽ mờ dần qua từng lần; mặt người thấy rõ nhất: giảm số lần nối, nếu được thì quay về khung rõ gốc; tại mối nối, đoạn trước bỏ khoảng 6 khung cuối, đoạn sau bỏ khung đầu tiên (Seedance chính thức).
- Tham chiếu nhân vật: một ảnh cận mặt chính diện cộng một ảnh toàn thân; Seedance chính thức không khuyến nghị ảnh ba mặt / nhiều góc.
- Mặt người thật: Seedance 2.x không nhận ảnh tham chiếu và video có mặt người thật; khung người thật lấy từ video gốc không dùng trực tiếp được; Google Omni không nhận một số người có thể nhận diện. Đi theo đường người mẫu đã được cấp phép, người ảo, hoặc nhân vật phong cách hoá theo từng nền tảng.
- Lưới phân cảnh (storyboard 9 ô): ra một ảnh lưới trước, rồi cắt từng ô phóng to và sinh từ ảnh từng ô; dùng cả lưới làm khung đầu thì không ổn định, dùng làm ảnh tham chiếu thì được (Seedance có ví dụ chính thức về tham chiếu toàn năng).

---

## Mô hình video

### seedance-2.5
- **basis:** vendor
- **structure:** bốn khối: chỉ định tư liệu → một câu tóm tắt (chủ thể + địa điểm + sự kiện + đề tài / phong cách + máy quay đặc biệt) → tình tiết cụ thể (chia theo mốc thời gian hoặc "cảnh N", mỗi đoạn viết hình, máy, động tác, lời thoại, âm thanh) → kết thúc bằng những thứ không đổi suốt (máy, môi trường, âm thanh, không khí)
- **language:** tiếng Trung và tiếng Anh đều hỗ trợ; chính thức chưa nói cái nào tốt hơn; ngôn ngữ lời thoại phải thống nhất
- **length:** tiếng Trung tối đa 500 chữ, tiếng Anh tối đa 1000 từ; vượt quá sẽ mất chi tiết
- **multi_shot:** dùng "cảnh N" hoặc mốc thời gian nguyên giây đều được: "0-3 giây… 3-7 giây…", nối liền không để trống; cũng nhận "giây thứ 2…", "sau 3 giây…". Không dùng mốc thời gian để viết tần suất ("lắc đầu 3 lần mỗi giây"). Chuyển cảnh viết rõ điểm kích hoạt và kiểu chuyển. Mốc thời gian là tham chiếu nhịp, không chính xác từng khung.
- **references:** tư liệu đánh số theo loại và thứ tự tải lên: API Ark viết "hình ảnh1 / video1 / âm thanh1", ứng dụng Jimeng dùng @<ảnh>1, fal dùng @Image1. Mỗi tư liệu phải có dòng mô tả nó phụ trách gì; đông người thì liệt kê; có thể ghi rõ không lấy gì (ví dụ "không dùng nền của ảnh"). Tư liệu từ thư viện tài sản vẫn viết "hình ảnh1" trong prompt, không viết mã tài sản. Ổn định nhất với 1–5 chủ thể.
- **dialogue:** "vai diễn (cảm xúc): "nội dung"", ví dụ nam MC: "…"; nhạc nền viết "nhạc nền: …". Sau lời thoại không thêm mô tả giọng điệu, biểu cảm, động tác, cũng không lặp lại lời thoại, nếu không dễ bị sinh ra phụ đề. Lời thoại ngoài tiếng Trung và tiếng Anh thì ghi ngôn ngữ trước ("cô gái nói tiếng Nhật nhỏ nhẹ: …"). Nhiều người thì ghi rõ ai nói, ai im.
- **negatives:** không có trường prompt phủ định. Viết tích cực càng nhiều càng tốt; phụ đề và âm thanh có thể viết trực tiếp "không phụ đề", "không nhạc nền, chỉ sinh âm môi trường và âm động tác", "không có âm thanh nào". Lệnh cấm nhạc nền hay bị lọt: viết ở đầu và cuối, kèm các từ đồng nghĩa (BGM, nhạc đệm, âm nền).
- **camera:** dùng thuật ngữ chuẩn: toàn cảnh rộng đến cận cảnh; đẩy, kéo, lia, dịch, bám, quay quanh, lao xuống, cầm tay lắc; góc thấp, góc cao, góc nhìn thứ nhất; một cảnh quay liền, zoom kiểu Hitchcock, FPV, slow motion kiểu bullet time. Ghi rõ máy cố định hay chuyển động; cố định thì viết "máy cố định". Tách chuyển động máy và động tác chủ thể thành hai câu.
- **frame_mode:** muốn khung giữ nguyên thì dùng chế độ khung đầu / đầu–cuối (role=first_frame / last_frame). Lúc đó ratio chỉ được là adaptive, tỷ lệ đầu ra theo khung đầu, và không được truyền thêm ảnh tham chiếu, video, âm thanh. Muốn đồng thời dùng tư liệu tham chiếu thì đi theo chế độ tham chiếu toàn năng, viết "hình 3 làm khung đầu, hình 5 làm khung cuối"; kết quả chỉ gần đúng. Nhiều keyframe thì mở đầu viết "theo thứ tự hình 1 đến hình 7 làm keyframe". Phần chữ viết chuyển động tiếp theo, máy quay và âm thanh.
- **frames:** tỷ lệ khung 0.4–2.5; cạnh 300–6000 px; dưới 30 MB; ảnh tham chiếu không có độ phân giải cao hơn đầu ra; ảnh phân cảnh dùng nét đơn giản, ít chữ trên ảnh.
- **rewriter:** API không có công tắc viết lại.
- **pitfalls:**
  - Ở chế độ tham chiếu toàn năng, nếu prompt chứa các từ "chỉnh sửa video, thêm, thêm vào, xoá, bỏ đi, sửa, thay thế, đổi thành, kéo dài, tiếp tục" thì bị xếp thành tác vụ chỉnh sửa hoặc nối tiếp; khi sao chép bình thường nên tránh các từ này, hoặc đặt omni_reference_task_type=reference.
  - Video tham chiếu có phụ đề thì kết quả dễ có phụ đề.
  - Từ tiếng Anh trong hình hay bị sai chính tả; viết từng chữ cái cách nhau. Chữ Trung sai thì đưa chữ đó vào dưới dạng ảnh tham chiếu.
  - Từ cảm xúc quá mạnh làm mắt phát sáng; đổi sang từ ôn hoà.
  - Tư liệu tham chiếu tải lên theo thứ tự xuất hiện của nhân vật, nếu không nhân vật sẽ bị gán sai.
  - Cảnh dài 30 giây: đặc điểm nói ở đầu không giữ được; nhắc lại ở các đoạn chính. Đoạn để trống trên dòng thời gian thì không được kiểm soát.
  - Từ về nước, sóng (như "nước", "tiếng vang") làm âm thanh có tiếng sóng nước.
- **unverified:**
  - 2.5 có còn nhận bốn ký hiệu âm thanh của 2.0 không, các nguồn nói khác nhau.
  - Số cảnh tối đa viết được chưa có thông tin.
- **sources:** ark.volcengine.com (hướng dẫn prompt Seedance 2.5); docs.volcengine.com (82379/2607689; ark/seedance-2-5; create-video-generation-task-api; seedance-portrait-asset-guide); fal.ai (seedance-2-5-prompting-guide); runway.com (seedance-2-5-prompt-guide)
- **lint:** tối đa 500 chữ CJK

### seedance-2.5-flash
- **basis:** vendor
- **structure:** chính thức chỉ nói: viết ngắn gọn, cụ thể: chủ thể, động tác, máy quay, phong cách hình ảnh; mỗi lần chỉ một động tác. Không có hướng dẫn riêng, theo cách viết của Seedance 2.5 (rea-video models seedance-2.5).
- **frame_mode:** như 2.5, chia chế độ khung đầu / đầu–cuối và chế độ tham chiếu toàn năng, hai chế độ không trộn được.
- **frames:** tối đa 720p; giới hạn thời lượng và số tư liệu tham chiếu chưa công bố.
- **unverified:** Flash có nhận mốc thời gian nguyên giây và bốn ký hiệu âm thanh như 2.5 hay không chưa rõ.
- **sources:** dreamina.capcut.com (seedance-2-5-flash); cellcog.ai (blog seedance-2-5-flash)

### seedance-2.0
- **basis:** vendor
- **structure:** chủ thể chính xác + chi tiết động tác + môi trường cảnh + ánh sáng và màu + máy quay + phong cách hình ảnh + chất lượng + ràng buộc
- **language:** tiếng Trung, tiếng Anh; lời thoại thống nhất một ngôn ngữ, không trộn Trung–Anh; không dán nguyên kịch bản
- **length:** tiếng Trung tối đa 500 chữ, tiếng Anh tối đa 1000 từ
- **multi_shot:** dùng "cảnh 1 / cảnh 2 / cảnh 3", mỗi cảnh ghi máy, động tác, địa điểm, âm thanh. Không ghi số giây cho cảnh: chính thức nói hỗ trợ thời gian chính xác không ổn định, ép thời lượng có thể gây bất thường. Cảnh hội thoại hợp với một cảnh quay liền; động tác nhanh thì tách thành vài đoạn rồi ghép.
- **references:** định nghĩa trước rồi tái sử dụng: "đặt hình ảnh1 trong … là chủ thể 1", hoặc viết tắt "Nhân vật A@<ảnh>1", mỗi chủ thể có 2–3 đặc điểm ổn định; tư liệu quan trọng nhất đặt trước. Mẫu: "tham chiếu hình ảnh N trong chủ thể N, sinh…", "tham chiếu động tác / máy / phong cách / hiệu ứng âm trong video N, sinh…", "tham chiếu âm sắc trong âm thanh N, sinh…". Jimeng toàn năng có thể viết "@<ảnh>1 làm khung đầu, @<video>1 tham chiếu ngôn ngữ hình, @âm thanh1 dùng cho nhạc nền". Khuyến nghị 1–2 ảnh người, 1 ảnh cảnh, 1 đoạn video máy, 1 âm thanh; không nhồi quá nhiều.
- **dialogue:** bốn ký hiệu: nhạc (đang phát … trong nền), hiệu ứng âm <tiếng chó sủa từ xa>, lời thoại {xin chào, thế giới}, phụ đề[chương một: khởi hành]. Ngôn ngữ khác thì viết "nói bằng tiếng Nhật {…}". Chỉ định giọng thì viết "dùng giọng của @âm thanh1… để nói", giọng sẽ có sai lệch.
- **negatives:** không có trường phủ định; ràng buộc viết ở cuối: "giữ không phụ đề", "tránh sinh bất kỳ chữ hoặc phụ đề nào", "không sinh logo", "không sinh watermark". Chính thức thừa nhận không thể hoàn toàn không có phụ đề; khung ngang ra ít hơn khung dọc.
- **camera:** dùng thuật ngữ chuẩn (trung cảnh, cận cảnh, toàn cảnh, đẩy chậm, lia ngang êm, cố định); mỗi cảnh chỉ một kiểu máy.
- **frame_mode:** muốn giữ chắc khung đầu–cuối thì dùng chế độ khung đầu–cuối (role=first_frame / last_frame), không truyền cùng tư liệu tham chiếu; viết "hình 1 làm khung đầu" là cách thay thế lỏng hơn. Chỉnh sửa hoặc kéo dài video thì viết trực tiếp "video N", không viết "video tham chiếu N", nếu không sẽ bị coi là tác vụ tham chiếu.
- **frames:** ảnh người dùng ảnh chân dung cận mặt cộng ảnh toàn thân, không khuyến nghị nhiều góc; mặt quá nhỏ trong ảnh sẽ bị rớt mặt.
- **rewriter:** API không có công tắc viết lại.
- **pitfalls:**
  - Dễ ra bản sao / sinh đôi: thêm một câu cấm toàn cục ở cuối.
  - Chữ đa âm, chữ hiếm, chữ gần giống dễ đọc sai.
  - Ảnh tham chiếu thực tế làm cảnh phong cách hoá bị kéo về thực tế.
  - Trên 4 người tham chiếu thì độ ổn định giảm.
  - Kéo dài nhiều lần thì khuôn mặt suy giảm.
- **sources:** docs.volcengine.com (82379/2222480; ark/seedance-2-0; create-video-generation-task-api)
- **lint:** tối đa 500 chữ CJK; cấm viết số giây cho cảnh (khớp mẫu "cảnh N (số" hoặc "từ số giây…", lý do: chính thức nói hỗ trợ thời gian chính xác không ổn định)

### kling-4.0
- **basis:** vendor
- **structure:** bốn khối: [Asset Roles] mỗi tư liệu phụ trách gì → [Overall Settings] thiết lập chung → [Sequence of Events] sự kiện theo thời gian, rồi máy quay → [Audio] âm thanh. Trước hết dùng một câu nói rõ chủ thể, cảnh, động tác, cảm xúc; sau đó chỉ bổ sung máy, thời gian, âm thanh, và những thứ phải giữ nguyên.
- **language:** không chỉ định ngôn ngữ prompt; lời thoại và chữ trong hình hỗ trợ tiếng Trung, Anh, Nhật, Hàn, Tây Ban Nha, Bồ Đào Nha, tiếng German (Germany), Pháp, Hindi, phương ngữ Trung và giọng Anh
- **length:** tối đa 8000 token
- **multi_shot:** mặc định tự chia cảnh, không có công tắc. Viết cảnh trực tiếp trong prompt: "Shot 1 (5s): …" hoặc "0–3 seconds: …". Muốn một cảnh quay liền phải ghi rõ No cuts. Không dùng trường phân cảnh có cấu trúc như 3.0.
- **references:** tư liệu đánh số theo thứ tự tải lên: @Image1, @Video1, @Element1. Mỗi tư liệu kèm một câu phụ trách (ví dụ "@Image1 defines the scene. Preserve its spatial layout, furnishings, and lighting."); chỉ ghi số mà không ghi vai trò thì kết quả không ổn định. Học máy và nhịp cảnh thì viết "Use @Video1 as the reference for camera movements and shot pacing." Muốn sửa video gốc thì viết "Edit @Video1", và thêm "Keep everything else unchanged".
- **dialogue:** lời thoại đặt trong dấu ngoặc kép, viết nguyên văn theo ngôn ngữ đích, và mô tả tuổi, giọng, tốc độ, cảm xúc của người nói; âm thanh đặt trong khối [Audio], chia thành lời thoại / lời thuyết minh, âm môi trường, nhạc, hiệu ứng. Phụ đề chỉ xuất hiện khi được yêu cầu rõ.
- **negatives:** chính thức nói lệnh phủ định làm tăng lỗi; chỉ giữ hai điều cần thiết: không phụ đề, không nhạc nền (và khi cần một cảnh thì thêm không cắt cảnh).
- **camera:** mô tả bằng ngôn ngữ tự nhiên (push-in, pull-out, pan, tracking, orbit, handheld); không có tham số máy riêng; có thể lấy chuyển động máy từ video tham chiếu.
- **frame_mode:** chế độ keyframe tối đa 10 ảnh (đầu, cuối, hoặc ở bất kỳ thời điểm nào giữa): "Use @Image1 as the first frame and @Image2 as the last frame.", khung giữa viết "X–Y sec | Keyframe 1: chuyện gì xảy ra". Phần chữ chỉ viết chuyển động giữa các khung. Chế độ keyframe không được thêm tư liệu tham chiếu, và không dùng chung với Omni Reference. Thay đổi lớn như ngày sang đêm thì tách thành hai đoạn.
- **frames:** khung hình theo keyframe đầu tiên; ảnh dưới 30 MB, tỷ lệ 2:5–5:2
- **rewriter:** không có công tắc; prompt quá ngắn sẽ được mô hình tự mở rộng.
- **pitfalls:**
  - Từ trừu tượng (premium look) không có tác dụng.
  - Không viết mục giữ nguyên thì các phần tử khác sẽ đổi theo.
  - Ảnh khung có chữ thì thêm câu "Do not redraw the letters."
- **unverified:** tên trường API chính thức và độ phân giải tối thiểu của keyframe chưa kiểm chứng.
- **sources:** kling.ai (kling-4-model-user-guide); krea.ai (kling-4 prompt-guide); fal.ai (what-is-kling-4-0)

### kling-4.0-flash
- **basis:** vendor
- **structure:** cùng cách viết với Kling 4.0 (rea-video models kling-4.0): phụ trách tư liệu → thiết lập chung → sự kiện theo thời gian → âm thanh
- **length:** tối đa 8000 token
- **multi_shot:** mặc định tự chia cảnh; viết cảnh trong prompt ("Shot 1 (5s): …"); trên fal dùng danh sách multi_prompt, tổng thời lượng bằng tổng các cảnh.
- **references:** @Image1, @Video1, @Element1, đánh số theo thứ tự tải lên, mỗi tư liệu kèm một câu phụ trách; fal còn có @Voice1.
- **negatives:** chỉ giữ hai điều: không phụ đề, không nhạc nền.
- **frame_mode:** chỉ nhận khung đầu, không hỗ trợ khung đầu–cuối và nhiều keyframe; bố cục giữ bằng khung đầu hoặc ảnh tham chiếu.
- **sources:** kling.ai (kling-4-model-user-guide)

### kling-3.0
- **basis:** third-party
- **structure:** không có công thức cố định; viết theo chủ thể, động tác, cảnh, máy quay, ánh sáng, cảm xúc. Ví dụ thứ tự: cảnh → chủ thể → máy quay → động tác → lời thoại.
- **language:** tiếng Trung và tiếng Anh đều được; lời thoại hỗ trợ tiếng Trung, Anh, Nhật, Hàn, Tây Ban Nha và phương ngữ, giọng địa phương
- **length:** tổng dưới 2500 ký tự; mỗi cảnh trong phân cảnh tự định nghĩa tối đa 512 ký tự, vượt quá sẽ bị cắt
- **multi_shot:** API dùng phân cảnh có cấu trúc: shot_type=customize, multi_prompt có mỗi cảnh một mục {index, prompt, duration}, 1–6 cảnh, tổng thời lượng bằng tổng thời lượng (3–15 giây), lúc này prompt ở đầu không có tác dụng. shot_type=intelligence là mô hình tự phân cảnh, có thể chỉ ra một cảnh. Viết trong prompt thì dùng "[Shot 1: Wide shot] …", mở đầu tả cảnh rồi liệt kê cảnh theo thứ tự.
- **references:** chủ thể (Element) gắn trên giao diện vào khung đầu, trong chế độ khung đầu và khung đầu–cuối tối đa 3; chủ thể đã có giọng thì không chỉ định âm sắc trong prompt nữa.
- **dialogue:** "tên (giọng điệu, ngôn ngữ): "lời thoại"", ví dụ Mom (softly, in a surprised tone): "…"; lời thuyết minh viết Voiceover (…):; phương ngữ viết said in Cantonese:. Mỗi nhân vật dùng một tên cố định, không dùng đại từ; động tác viết trước lời thoại; dùng các từ nối như Immediately để tránh hai câu thoại dính vào nhau. Âm môi trường viết vào câu cảnh.
- **negatives:** có trường negative_prompt riêng (tối đa 2500 ký tự); bản Turbo không nhận, phải viết vào prompt.
- **camera:** ngôn ngữ tự nhiên (slow push-in, pan, tilt, tracking, dolly-in, handheld), mỗi cảnh một kiểu máy.
- **frame_mode:** coi ảnh là neo, chỉ viết hình thay đổi thế nào; danh tính, bố cục, chữ trong ảnh được giữ lại.
- **frames:** JPEG / PNG không có kênh trong suốt, cạnh 300–8000 px, tỷ lệ 1:2.5–2.5:1, dưới 10 MB; khung ra theo khung vào. Bản Turbo không nhận khung cuối và chủ thể.
- **rewriter:** không có công tắc; cfg_scale (mặc định 0.5) là núm điều khiển mức tuân theo duy nhất.
- **pitfalls:**
  - Động tác không gắn với nhân vật có tên thì sẽ nói sai người.
  - Phân cảnh tự động có thể gộp thành một cảnh.
- **unverified:**
  - Cách viết tham chiếu giọng (<<<voice_1>>>) chỉ thấy ở bản gương không chính thức.
  - Phân cảnh tự định nghĩa có dùng chung được với khung cuối không.
- **sources:** kling.ai (blog kling-ai-prompt-guide; klingai-video-3-model-user-guide); blog.fal.ai (kling-3-0-prompting-guide); help.aliyun.com (kling-video-generation-api-reference)

### kling-o3
- **basis:** vendor
- **structure:** sinh theo tham chiếu: [mô tả chi tiết chủ thể] + [tương tác / động tác giữa các chủ thể] + [môi trường hoặc nền] + [hướng thị giác về ánh sáng, phong cách]
- **language:** tiếng Trung và tiếng Anh đều được
- **length:** tối đa 2500 ký tự
- **multi_shot:** "Shot 1 (2s): Wide shot, @Boxer A and @Boxer B face off…" hoặc "[00:00 - 00:02] Medium shot: … Audio: …", tổng dài dưới 15 giây. Khi có video tham chiếu chỉ dùng được phân cảnh tự động; chỉnh sửa video không hỗ trợ nhiều cảnh.
- **references:** trên app dùng @Image1 hoặc @tên chủ thể ("@Alan walks in holding @Samoyed"); API chính thức dùng <<<image_1>>>, <<<element_1>>>, <<<video_1>>>, đánh số theo thứ tự mảng; fal dùng @Image1 / @Element1. Mẫu: "Take @Image1 as the start frame, take @Image2 as the end frame, mô tả thay đổi giữa hai khung"; "Take @Image as the start frame. Generate a new video following the camera movement of the @Video"; "Based on @Video, generate the next shot: …". Trong cùng một prompt giữ một kiểu ký hiệu.
- **dialogue:** lời thoại viết "@nhân vật says with a barely contained smile, "…"" hoặc "Goro: "…""; hiệu ứng âm viết một dòng riêng Audio:. Chủ thể đã gắn giọng thì không chỉ định thêm.
- **negatives:** API có trường negative_prompt.
- **camera:** ngôn ngữ tự nhiên; có thể lấy chuyển động máy từ video tham chiếu.
- **frame_mode:** dùng mẫu khung đầu–cuối ở trên, phần chữ viết thay đổi giữa hai khung; chỉ có khung cuối thì không hỗ trợ; quá 2 ảnh thì không hỗ trợ khung cuối.
- **frames:** ảnh từ 300 px trở lên, dưới 10 MB; không có video thì ảnh cộng chủ thể tối đa 7, có video thì tối đa 4; video 1 đoạn, 3–10 giây.
- **rewriter:** chưa tìm thấy công tắc.
- **pitfalls:**
  - Đã truyền video tham chiếu thì không bật âm thanh gốc được.
  - Mẫu chỉnh sửa: "Add @Element to @Video" "Remove … from @Video" "Change @Video to … style", là cách viết khác với prompt sinh.
- **sources:** kling.ai (klingai-video-3-omni-model-user-guide; klingai-video-o1-user-guide); help.aliyun.com (kling-video-generation-api-reference)

### veo-3.1
- **basis:** vendor
- **structure:** [Cinematography: máy quay] + [Subject: chủ thể] + [Action: động tác] + [Context: bối cảnh] + [Style & Ambiance: phong cách và không khí]; một đoạn ngắn chỉ viết một khoảnh khắc tập trung.
- **language:** prompt viết tiếng Anh
- **length:** chính thức không giới hạn; gọi qua Runway API thì 1000 ký tự
- **multi_shot:** mỗi cảnh một dòng mốc thời gian: "[00:00-00:02] …", ví dụ chính thức là 4 cảnh 2 giây trong 8 giây, trong dòng có thể kèm SFX: và Emotion:. Mỗi đoạn chỉ 4 / 6 / 8 giây.
- **references:** không có cú pháp đánh dấu, dùng câu mô tả: "Using the provided images for the detective, the woman, and the office setting, create a medium shot of…". Tối đa 3 ảnh, cùng một người / nhân vật / sản phẩm; dùng ảnh tham chiếu thì chỉ ra 8 giây. Trong Flow dùng @ để chỉ.
- **dialogue:** "A woman says: My name is Clara." — sau động từ nói thêm dấu hai chấm, không thêm ngoặc kép; chính thức gắn cách viết này với việc tránh chữ xuất hiện trên hình. Âm thanh viết thành câu riêng: "SFX: thunder cracks in the distance", "Ambient noise: …". Mỗi cảnh một người nói, lời ngắn, người nói hướng về máy; đối thoại nhiều người tách thành nhiều đoạn.
- **negatives:** có trường negativePrompt riêng: chỉ liệt kê danh từ (subtitles, captions, on-screen text), không viết no / don't.
- **camera:** static, pan, tilt, dolly, truck, pedestal, zoom, crane, aerial / drone, handheld, whip pan, arc; ngôn ngữ ống kính wide-angle, telephoto, shallow depth of field, rack focus.
- **frame_mode:** hình đã cho chủ thể, bối cảnh, phong cách, nên chữ chỉ viết chuyển động; chế độ khung đầu–cuối viết quá trình chuyển giữa hai khung và âm thanh.
- **frames:** JPEG / PNG, dưới 20 MB; tỷ lệ 16:9 hoặc 9:16.
- **rewriter:** có enhancePrompt, mặc định bật; chưa kiểm chứng có tắt được ở 3.1 không.
- **pitfalls:**
  - Có lời thoại thì dễ in ra phụ đề loạn chữ: dùng cách viết dấu hai chấm, và đưa subtitles, captions vào negativePrompt.
  - Lời thoại tiếng Trung có khẩu hình thành công thấp (thử nghiệm cộng đồng): nên lồng tiếng hoặc đổi khẩu hình ở hậu kỳ.
- **unverified:**
  - Hai tài liệu chính thức nói ngược nhau về việc lời thoại dùng dấu hai chấm hay ngoặc kép; ở đây lấy dấu hai chấm.
  - Bản xem trước đã ngừng trên Gemini API, chỉ còn bản chính thức trên Vertex.
- **sources:** cloud.google.com (ultimate-prompting-guide-for-veo-3-1); docs.cloud.google.com (video-gen-prompt-guide; best-practice; 3-1-generate)

### grok-imagine-video-1.5
- **basis:** vendor
- **references:** đánh số theo vị trí: <IMAGE_0>, <IMAGE_1>…, không phải @image; nếu khoá khung đầu bằng trường image thì đó là <IMAGE_0>. Âm thanh là <AUDIO_0> đến <AUDIO_2> (giọng cài sẵn). Mỗi ảnh tham chiếu chỉ một vai trò, ở một vị trí cố định trong hình; nhiều ảnh tham chiếu thì hạn chế người, đạo cụ đừng di chuyển.
- **frame_mode:** khi đã khoá khung đầu, prompt có thể để trống; nếu viết thì chỉ viết chuyển động và máy quay; muốn lặp lại thì dùng cùng một ảnh làm cả khung đầu và khung cuối.
- **dialogue:** âm thanh mặc định bật; generate_audio=false để tắt; cách viết lời thoại chính thức chưa nêu.
- **frames:** tối đa 4 keyframe, căn theo 1/3 giây, phải nằm bên trong đoạn; sinh từ ảnh thì tỷ lệ khung theo ảnh vào.
- **sources:** docs.x.ai (reference-to-video; generation)

### gemini-omni-flash
- **basis:** vendor
- **structure:** không có công thức; viết tự nhiên về bối cảnh, máy quay, ánh sáng, không khí.
- **language:** tiếng Anh (các ngôn ngữ khác chính thức chưa đánh giá)
- **length:** chính thức không giới hạn
- **multi_shot:** mặc định tự cắt cảnh; muốn một cảnh quay liền phải viết "In a single continuous shot" hoặc "No scene cuts". Mốc thời gian viết "[0-5s] … [5-10s] …", hoặc câu tự nhiên "After 3 seconds, …". Mỗi đoạn 3–15 giây. Khi nối tiếp, giây 0 tính từ phần nối.
- **references:** giải thích công dụng từng ảnh bằng ngôn ngữ tự nhiên: "The person shown in the reference image enters the scene", "Use the image as the first frame". Không viết chuỗi điều khiển như <FIRST_FRAME> (Google đã bỏ; fal vẫn dùng <IMAGE_REF_0>, tuỳ nền tảng). Tối đa 6 ảnh tham chiếu (mỗi nhân vật 3 ảnh, tối đa 2 nhân vật); video tham chiếu mỗi đoạn dưới 3 giây; không nhận âm thanh tham chiếu.
- **dialogue:** lời thoại giống Veo, dùng dấu hai chấm không ngoặc kép; âm thanh viết bằng câu: "Sound design: gentle breeze… No dialogue.", "Include calm background music". Chữ trên hình đặt trong ngoặc kép.
- **negatives:** không có trường phủ định, viết câu ngắn trong prompt: "No dialogue", "No extra sound effects", "No scene cuts".
- **camera:** ngôn ngữ tự nhiên.
- **frame_mode:** hai ảnh là nội suy (3–10 giây), chữ viết quá trình chuyển; chế độ khung đầu chỉ viết chuyển động. Khi chỉnh sửa thì prompt càng ngắn càng tốt, thêm "Keep everything else the same."
- **frames:** dùng ảnh độ phân giải cao; đầu ra 16:9 hoặc 9:16.
- **rewriter:** chưa tìm thấy công tắc.
- **pitfalls:**
  - Không nhận ảnh có người có thể nhận diện một phần.
  - Prompt chỉnh sửa mô tả quá chi tiết sẽ gây thay đổi thừa.
- **sources:** aistudio.google.com (docs/omni); docs.cloud.google.com (best-practice)

### vidu-q3
- **basis:** third-party
- **structure:** chủ thể / cảnh + mô tả cảnh + mô tả môi trường + phong cách / chất liệu; câu tự nhiên, ít chủ thể, từ khoá phong cách quan trọng có thể lặp lại.
- **language:** không chỉ định; giọng nói đầu ra hỗ trợ tiếng Trung, Anh, Nhật
- **length:** văn bản sinh, ảnh sinh, khung đầu–cuối dưới 20000 ký tự (Turbo văn bản sinh 5000); tham chiếu sinh video 5000
- **multi_shot:** hỗ trợ tự cắt cảnh thông minh, không có trường phân cảnh cũng không có cách viết chính thức; dùng câu nói rõ chỗ cắt.
- **references:** chế độ chủ thể: mỗi chủ thể có tên và tối đa 3 ảnh, trong prompt dùng @tên chủ thể để chỉ, tối đa 7 chủ thể. Truyền ảnh trực tiếp thì nói theo thứ tự: "Image 1 is [scene]; Image 2 is [character]; Image 3 is [prop]".
- **dialogue:** chính thức không có định dạng; bên thứ ba khuyến nghị: mỗi câu thoại 5–9 từ, dấu câu gọn; hiệu ứng âm viết "SFX: …"; nhạc nền viết nhịp hoặc phong cách.
- **negatives:** không có trường phủ định.
- **camera:** pan, tilt, zoom, static, orbit, FPV, aerial; mỗi cảnh một kiểu máy.
- **frame_mode:** chỉ viết chuyển động và máy quay.
- **frames:** tỷ lệ độ phân giải khung đầu so với khung cuối trong khoảng 0.8–1.25; ảnh dưới 50 MB, tỷ lệ không vượt 1:4 / 4:1; ảnh tham chiếu từ 128×128 trở lên.
- **rewriter:** sinh video từ ảnh có is_rec giữ false; bật lên thì mô hình sẽ bỏ prompt của bạn và tự viết.
- **pitfalls:**
  - Lời thoại dài một hơi hoặc miệng bị che thì khẩu hình bị trôi.
- **unverified:**
  - Chưa có hướng dẫn prompt chính thức cho Q3; cấu trúc và khuyến nghị lời thoại lấy từ bên thứ ba.
- **sources:** platform.vidu.com (vidu-q3 reference-to-video; image-to-video; start-end-to-video); help.aliyun.com (vidu-video-generation-prompt-guide)

### vidu-q4-preview
- **basis:** vendor
- **structure:** chính thức không có hướng dẫn prompt. Bên thứ ba khuyến nghị chia theo thời gian: 0–4 giây dựng cảnh, 4–10 giây động tác, 10–16 giây phản ứng; mỗi đoạn ghi cỡ cảnh, máy quay, lời thoại và âm thanh.
- **length:** dưới 20000 ký tự
- **multi_shot:** tự cắt cảnh, không có trường phân cảnh và cách viết chính thức.
- **references:** sinh theo tham chiếu: 1–15 ảnh cộng 0–3 đoạn âm thanh (mp3, 3–12 giây). Tài liệu viết [@tên chủ thể], ví dụ dùng @1 / @2, nhưng đồng thời nói tạm chưa hỗ trợ gọi chủ thể; cách viết chính xác chưa xác minh.
- **frame_mode:** sinh từ ảnh chỉ nhận một ảnh; prompt có thể để trống.
- **frames:** png / jpeg / webp, dưới 50 MB (thân yêu cầu dưới 20 MB); chế độ tham chiếu có tỷ lệ 1:1, 9:16, 16:9, 3:4, 4:3.
- **rewriter:** sinh từ ảnh có is_rec mặc định là true, sẽ thay prompt của bạn bằng prompt hệ thống đề xuất; muốn dùng prompt riêng phải đặt false.
- **sources:** platform.vidu.com (vidu-q4-preview image-to-video; reference-to-video); pollo.ai (how-to-use-vidu-q4)

### pixverse-v6
- **basis:** vendor
- **structure:** ba câu: câu 1 chủ thể + động tác + địa điểm; câu 2 máy quay + phong cách; câu 3 ràng buộc. Động tác chính đặt lên đầu.
- **language:** nhận mọi ngôn ngữ, khuyến nghị tiếng Anh
- **length:** bắt đầu từ 50–80 từ; trên fal giới hạn 2048 byte (mỗi chữ Trung 3 byte)
- **multi_shot:** nhiều cảnh là một công tắc (generate_multi_clip_switch), không có trường cảnh; prompt chia đoạn bằng "Start with… Cut to… Shift to… End with…", cuối cùng thêm một câu ràng buộc nhất quán ("Preserve the same warm color grade across all shots"). Chuyển khung đầu–cuối, nối tiếp, chế độ hợp nhất không bật được.
- **references:** chế độ hợp nhất dùng @Subject1–8, @Background1–2, @Video1–2; mỗi đánh dấu phải tương ứng với một tham chiếu đã truyền, nếu không yêu cầu bị từ chối. Đầu vào có video tham chiếu thì độ dài đầu ra theo video.
- **dialogue:** không có định dạng lời thoại chính thức; âm thanh và âm môi trường viết thành dòng ngắn "Audio: …". Bên thứ ba cho rằng âm thanh của nó chủ yếu là âm môi trường, lời thoại nên để hậu kỳ.
- **negatives:** trong app mọi chữ đều được coi là chỉ thị tích cực, viết no X chỉ làm tăng X; đổi thành ràng buộc tích cực ("camera stays steady"); một số nền tảng API có trường negative_prompt.
- **camera:** ngôn ngữ tự nhiên, một chuyển động chính cộng một từ về chất cảm; xếp nhiều chuyển động sẽ rung.
- **frame_mode:** không mô tả lại ảnh, chỉ viết chuyển động, máy và một quy tắc nhất quán; chuyển khung đầu–cuối thêm một câu nói gì giữ nguyên, hai khung phải là cùng một chủ thể liên tục.
- **rewriter:** thinking_type (enabled / disabled / auto) là công tắc tối ưu prompt, chọn tường minh theo nhu cầu.
- **pitfalls:**
  - cinematic, fast, epic là những từ không kiểm soát được gì.
  - Prompt dài thì chi tiết về sau bị mất.
- **unverified:** trang tài liệu chính thức của nền tảng không mở được; tham số lấy từ bên thứ ba.
- **sources:** pixverse.ai (ai-video-prompt-guide-7-tested-fixes); runware.ai (pixverse-v6 multi-shot-storytelling); docs.comfy.org (PixverseV6FusionVideoNode)

### minimax-h3
- **basis:** vendor
- **structure:** viết theo trường: integrated_multimodal_description: (hình và động tác) → overall_soundscape: (âm môi trường và hiệu ứng, 1–4 câu) → non_diegetic_music: (nhạc đệm: nhạc cụ và tốc độ, 1–3 câu, không có thì viết N/A). Hai trường âm thanh không để trống, để trống dễ sinh tiếng người thừa.
- **language:** prompt viết tiếng Anh; lời thoại và chữ trong hình giữ nguyên ngôn ngữ gốc
- **length:** dưới 7000 ký tự
- **multi_shot:** "[Shot 1] …" không kèm thời gian; cảnh sau viết "[Shot 2] At 00:03.500, the camera cuts to...", dùng một mốc thời gian tăng dần, không dùng khoảng thời gian. Chuyển mờ và mờ dần chỉ viết khi cần.
- **references:** đánh dấu <Subject N>, <Picture N>, <Video N>, <Audio N>; prompt sinh theo tham chiếu chia sáu đoạn: subject_definitions, summary, retention_analysis, detailed_description, overall_soundscape, non_diegetic_music, và ghi mức giữ lại (fully_preserved / partially_preserved / attribute_transfer / weak_reference). API hosted cũng nhận cách viết đời thường ("following the motion in reference video 1").
- **dialogue:** mã người nói (S1), (S2); lời thoại đặt trong <d>[English] I get off at the next station.</d>, giọng điệu và động tác viết ngoài thẻ; lời thuyết minh viết "says in an off-screen voiceover" và nói rõ miệng đang khép. Ngoặc kép tiếng Anh ở đây nghĩa là chữ trên hình, không phải lời thoại. Không dùng dấu ba chấm trong lời thoại.
- **negatives:** không có trường phủ định; liệt kê điều cấm sẽ đưa chính khái niệm đó vào hình, nên mô tả tích cực.
- **camera:** ngôn ngữ tự nhiên.
- **frame_mode:** dòng đầu viết câu căn chỉnh, rồi một dòng trống: sinh từ ảnh "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced."; khung đầu–cuối gắn <Picture N> với giây cụ thể. Chế độ khung và chế độ tham chiếu không được trộn.
- **frames:** cạnh ảnh 256–5760 px, tỷ lệ 0.4–2.5, dưới 30 MB; tham chiếu tối đa 9 ảnh, 3 đoạn video (tổng 15 giây), 3 đoạn âm thanh.
- **rewriter:** chỉ H3 Max có prompt_expansion_mode (disabled / balanced / quality); muốn kiểm soát chính xác thì đặt disabled.
- **pitfalls:**
  - Có âm thanh tham chiếu thì dễ nói sai người; buộc lời thoại vào động tác nhìn thấy được.
- **unverified:**
  - API hosted có bắt buộc dùng định dạng theo trường không (ví dụ của fal là đoạn văn thường).
- **sources:** huggingface.co (MiniMax-H3 VIDEO_PROMPT_WRITING_GUIDE base và ref); platform.minimax.io (video-generation-v2-create); docs.comfy.org (minimax-h3-prompt-guide)
- **lint:** ngôn ngữ en; tối đa 7000 ký tự; bắt buộc có "overall_soundscape:" và "non_diegetic_music:"; cấm khoảng thời gian dạng "số–số giây" (lý do: mốc cảnh phải là một thời điểm, ví dụ At 00:03.500, không dùng khoảng thời gian)

### minimax-h3-max
- **basis:** vendor
- **structure:** cùng cách viết với MiniMax H3 (rea-video models minimax-h3)
- **length:** dưới 7000 ký tự
- **references:** không có cú pháp đánh dấu, viết đời thường: Video 1, Image 2, Audio 3, "Voice timbre follows reference audio 1"
- **frame_mode:** khung đầu / khung cuối và tư liệu tham chiếu không truyền cùng lúc; video và âm thanh chỉ dùng được ở chế độ tham chiếu.
- **frames:** ảnh tham chiếu 256–5760 px, tỷ lệ 0.4–2.5, dưới 30 MB; video tham chiếu 2–15 giây (tổng dưới 15 giây); âm thanh tham chiếu 2–15 giây; t2v phải chỉ định tỷ lệ khung, i2v theo khung đầu.
- **rewriter:** extra.prompt_expansion_mode: disabled / balanced (mặc định) / quality; muốn kiểm soát chính xác thì đặt disabled.
- **pitfalls:**
  - Thời lượng chỉ 5–15 giây, 4 giây sẽ báo lỗi.
  - Chỉ có khung cuối có được không, tài liệu trước sau nói mâu thuẫn; đưa khung cuối cùng với khung đầu.
- **sources:** platform.minimax.io (video-generation-v2-create)
- **lint:** ngôn ngữ en; tối đa 7000 ký tự; bắt buộc có "overall_soundscape:" và "non_diegetic_music:"; cấm khoảng thời gian dạng "số–số giây" (xem minimax-h3)

### pika-h3-flex
- **basis:** vendor
- **structure:** viết theo thứ tự phát: hình và bối cảnh → ai ở đâu → mỗi động tác và cách nó kết thúc
- **language:** mô tả bối cảnh viết tiếng Anh; lời thoại và chữ trong hình giữ ngôn ngữ đích
- **length:** dưới 8000 ký tự
- **multi_shot:** đánh số cảnh kèm thời gian bắt đầu: "[Shot 2] at 00:04"; chỉ chuyển cảnh khi có nội dung mới; mỗi nhịp một chuyển động, một động tác.
- **references:** @Image1, @Video1, @Audio1, mỗi cái ghi rõ vai trò và mức bám theo; không được chỉ đưa âm thanh tham chiếu.
- **dialogue:** lời thoại đặt trong ngoặc kép, ghi rõ ai nói và nói thế nào; lời thuyết minh ngoài hình ghi rõ đến từ ngoài khung, người trong hình khép miệng; chữ trên hình viết nguyên văn trong ngoặc kép và thêm "No other text"; âm thanh và nhạc mỗi thứ một dòng, hoặc ghi "No music" / "No speech".
- **negatives:** dùng câu cấm rõ ràng, ví dụ "NO slow motion".
- **camera:** mỗi chuyển động ghi khoảng cách và tốc độ; đẩy (push-in) không giống zoom.
- **frame_mode:** để mô hình giữ những gì có trong khung đầu, rồi viết điều gì xảy ra tiếp theo; có khung cuối thì viết một động tác liền mạch, kết đúng ở khung cuối.
- **rewriter:** tuỳ chọn, do Pika lưu trữ.
- **sources:** pika.art (pika-h3-flex-prompt-guide)

### heygen-video-1
- **basis:** vendor
- **structure:** chính thức không có hướng dẫn prompt; dựa trên MiniMax H3, có thể tham khảo cách viết H3 (rea-video models minimax-h3).
- **length:** dưới 16000 ký tự
- **dialogue:** khi viết lời thoại trong ngoặc kép trong prompt, đặt duration là auto để thời lượng theo độ dài lời thoại.
- **rewriter:** prompt_enhancement: turbo / quality / ultraquality / disabled; muốn kiểm soát chính xác thì đặt disabled, nhưng quá 15 giây bắt buộc bật.
- **sources:** developers.heygen.com (create-heygen-video)

### hailuo-2.3
- **basis:** vendor
- **structure:** chính thức không có công thức; thứ tự thường dùng là cỡ cảnh / máy quay → chủ thể → động tác → cảnh / ánh sáng; một đoạn 6 giây chỉ viết một nhịp động tác.
- **language:** chưa nêu
- **length:** dưới 2000 ký tự
- **multi_shot:** không hỗ trợ, một lần một cảnh, nhiều cảnh tách thành nhiều lần sinh.
- **references:** không hỗ trợ tư liệu tham chiếu.
- **dialogue:** không có âm thanh; lời thoại và hiệu ứng âm không viết vào prompt.
- **negatives:** không có trường phủ định.
- **camera:** dùng lệnh trong ngoặc vuông, viết đúng chính tả cố định: [Truck left] [Truck right] [Pan left] [Pan right] [Push in] [Pull out] [Pedestal up] [Pedestal down] [Tilt up] [Tilt down] [Zoom in] [Zoom out] [Shake] [Tracking shot] [Static shot]. Các lệnh trong cùng một ngoặc có hiệu lực đồng thời ([Pan left,Pedestal up], tối đa 3); các ngoặc khác nhau thực hiện theo thứ tự.
- **frame_mode:** không mô tả lại ảnh, chỉ viết chuyển động và máy, và ghi rõ cái gì giữ yên.
- **frames:** chỉ nhận khung đầu, không có khung cuối; JPG / PNG / WebP, dưới 20 MB, cạnh ngắn từ 300 px, tỷ lệ 2:5–5:2.
- **rewriter:** prompt_optimizer mặc định bật; khi dùng lệnh ngoặc vuông hoặc muốn kiểm soát chính xác thì đặt false.
- **pitfalls:**
  - Thời lượng chỉ 6 hoặc 10 giây (1080P chỉ 6 giây).
- **sources:** platform.minimax.io (video-generation-t2v; video-generation-i2v); eachlabs.ai (how-to-write-better-hailuo-2-3-prompts)

### wan-3.0
- **basis:** vendor
- **structure:** [mô tả tổng thể] + [tham chiếu tư liệu: hình N / video N / âm thanh N] + [cảnh N (giây bắt đầu-kết thúc): chủ thể + bối cảnh + chuyển động + kiểm soát thẩm mỹ] + [lời thoại: xx nói: "xxxx"] + [hiệu ứng âm / BGM] + [phong cách / cảm xúc] + [danh sách phủ định]; phần không viết thì bỏ qua.
- **language:** tiếng Trung, tiếng Anh
- **length:** dưới 20000 ký tự
- **multi_shot:** "Cảnh 1 [0-3 giây]… Cảnh 2 [4-6 giây] chuyển cắt cứng, máy cố định, …"; dùng [bắt đầu-kết thúc] hoặc (bắt đầu-kết thúc) đều được, cả bài dùng một kiểu; các cảnh nối liền nhau, mỗi đoạn 2–5 giây. Cuối đoạn viết "chuyển cắt cứng", "chuyển mờ chéo", hoặc đầu đoạn sau viết "nối liền không đứt từ khung cuối của đoạn trước". Muốn một cảnh quay liền thì viết "sinh một cảnh quay đơn". Không viết động tác tần số cao mà mô hình không kiểm soát được.
- **references:** "hình 1 / video 1 / âm thanh 1" (tiếng Anh Image 1 / Video 1, có khoảng trắng giữa chữ và số), hình và video đánh số riêng. Nói rõ mỗi tư liệu phụ trách gì: "hình tướng quân tham chiếu, nét mặt tham chiếu hình 2… giọng tham chiếu âm thanh 1", "tham chiếu cách lia máy của video", "chỉ tham chiếu bảng màu và ánh sáng của hình 2, không tham chiếu người". Tối đa 10 ảnh, 5 video, 5 âm thanh.
- **dialogue:** "nhân vật + động từ nói + dấu hai chấm + nội dung trong ngoặc kép": hình 1 nói: "…"; hình 2 đáp: "…"; lời thuyết minh ngoài hình: "…". Có thể thêm cảm xúc, ngữ điệu, tốc độ, âm sắc, giọng vùng miền. Không viết lời thoại thì mô hình tự thêm; không muốn thì viết "không lời thoại", "không nhạc nền". Tham chiếu giọng viết một lần thì áp dụng cho toàn bộ lời thoại của nhân vật đó; muốn khớp khẩu hình thì viết "khẩu hình đồng bộ".
- **negatives:** viết ở cuối prompt thành "danh sách phủ định: không phụ đề, không watermark…", chỉ viết những thứ không muốn xuất hiện, không có thì để trống, không lặp lại những gì đã viết tích cực.
- **camera:** nói đời thường: đẩy gần, kéo xa, quay quanh, cầm tay theo sát; cố định thì viết "cố định, máy đứng yên, vị trí không đổi"; ống kính viết "tiêu cự 85mm, độ sâu trường ảnh nông", "góc rộng 24mm, độ sâu trường ảnh sâu"; chuyển động chậm viết "quay tốc độ cao (slow motion 1000fps)".
- **frame_mode:** ở chế độ khung đầu / đầu–cuối có thể viết quá trình động, cốt truyện, lời thoại và chuyển máy, cũng có thể chia theo khoảng thời gian; hai khung khác nhiều thì viết rõ quá trình chuyển. Khung đầu–cuối và tư liệu tham chiếu không truyền cùng lúc; chế độ khung đầu–cuối không nhận âm thanh.
- **frames:** khung đầu ra theo khung vào; muốn 3:4 thì truyền khung đầu 3:4.
- **rewriter:** prompt_extend mặc định bật; prompt đã viết theo cấu trúc trên thì nên tắt; khi đầu vào có file hoặc liên kết thì bắt buộc bật.
- **pitfalls:**
  - Chỉnh sửa video là một cách viết khác: "chỉnh sửa video, trong video 1 đổi xxx thành yyy, phần còn lại giữ nguyên"; mỗi lần đổi một thứ là ổn định nhất.
- **unverified:**
  - Cắt cảnh có chính xác rơi đúng thời điểm đã viết không chưa được nói rõ.
- **sources:** help.aliyun.com (wan3-video-generation-prompt-guide; wan3-video-generation-guide; text-to-video-prompt)

### wan-2.7-edit
- **basis:** vendor
- **structure:** chỉ thị chỉnh sửa: nói rõ đổi cái gì, đổi thành gì, phần còn lại giữ nguyên; mỗi lần một thứ.
- **language:** tiếng Trung, tiếng Anh
- **length:** dưới 5000 ký tự; negative_prompt dưới 500 ký tự
- **references:** "video 1", "hình 1" (tiếng Anh Video 1 / Image 1); 1 video (2–10 giây) cộng tối đa 4 ảnh tham chiếu.
- **dialogue:** audio_setting chọn origin để giữ âm thanh gốc, auto để mô hình xử lý.
- **negatives:** có trường negative_prompt riêng.
- **rewriter:** prompt_extend mặc định bật; khi chỉ thị đã rõ thì tắt.
- **sources:** help.aliyun.com (wan-video-editing-api-reference; text-to-video-prompt)

### wan-2.2
- **basis:** vendor
- **structure:** chủ thể + cảnh + chuyển động + kiểm soát thẩm mỹ (nguồn sáng, ánh sáng, cỡ cảnh, góc nhìn, ống kính, chuyển máy) + phong cách hoá. Nếu có phong cách thì đặt đầu; từ thẩm mỹ dùng dạng nhãn; sau đó là chủ thể, quá trình động tác, nền. Không viết mô tả văn chương về không khí, cảm giác.
- **language:** tiếng Trung, tiếng Anh đều được (từ phủ định và viết lại mặc định của chính thức là tiếng Trung)
- **length:** sinh văn bản thành video 60–200 chữ, sinh từ ảnh dưới 100 chữ; giới hạn Bailian 800 ký tự
- **multi_shot:** không hỗ trợ, một lần một cảnh.
- **references:** sinh văn bản / sinh từ ảnh không hỗ trợ đánh dấu tham chiếu.
- **dialogue:** không có âm thanh, không viết lời thoại và hiệu ứng âm.
- **negatives:** trường riêng; danh sách phủ định chuẩn chính thức: màu sắc quá rực, phơi sáng quá, tĩnh, chi tiết mờ không rõ, chữ phụ đề, phong cách, tác phẩm, bức vẽ, khung hình, đứng yên, xám tổng thể, chất lượng tệ nhất, chất lượng thấp, vết nén JPEG, xấu xí, khuyết tật, ngón tay thừa, tay vẽ không tốt, mặt vẽ không tốt, dị dạng, biến dạng mặt, cơ thể dị dạng, ngón tay dính nhau, khung hình đứng yên, nền lộn xộn, ba chân, nhiều người ở nền, đi ngược. Dùng LoRA tăng tốc (CFG=1) thì phủ định không có tác dụng.
- **camera:** từ vựng chính thức — cỡ cảnh: cận cảnh, cận trung, trung cảnh, trung toàn, toàn cảnh, cực toàn; góc máy: qua vai, góc thấp, góc cao, từ trên xuống, flycam, ngang tầm mắt, nhìn từ dưới lên; bố cục: trung tâm, nhấn trái / phải, đối xứng; ánh sáng: mềm, cứng, bên, trên, viền, ngược; chuyển máy: đẩy vào, kéo ra, dịch trái, lia lên, quay quanh, cố định. Đã viết chuyển máy trong prompt thì không thêm nhãn góc máy nữa.
- **frame_mode:** prompt = chuyển động + chuyển máy; những thứ đã có trong hình thì xoá khỏi prompt; muốn máy không động thì viết "cố định".
- **frames:** đầu ra theo khung đầu; khung đầu và khung cuối có độ phân giải khác nhau cũng được.
- **rewriter:** bản mã nguồn mở mặc định tắt (chính thức khuyến nghị bật); prompt_extend trên Bailian mặc định bật, đã viết theo cấu trúc thì tắt.
- **pitfalls:**
  - LoRA tăng tốc làm mất chuyển động, hình như hình nền động; cộng đồng xử lý bằng cách giảm cường độ LoRA ở giai đoạn nhiễu cao và đưa CFG lên 2–3.5.
- **sources:** help.aliyun.com (text-to-video-prompt); github.com/Wan-Video/Wan2.2 (system_prompt.py; shared_config.py)

### ltx-2.5
- **basis:** vendor
- **structure:** một đoạn tiếng Anh liền, theo thứ tự thời gian, thì hiện tại: động tác chính → động tác chi tiết → ngoại hình → môi trường → máy quay → ánh sáng → biến đổi. Không dùng nhãn kiểu "Audio:" "Visual:"; cỡ cảnh, máy, góc viết trong câu, không viết thành tiền tố kiểu "medium shot, static camera —"; không viết cảm xúc suy đoán, viết động tác nhìn thấy được.
- **language:** tiếng Anh; lời thoại giữ ngôn ngữ gốc, để nguyên trong ngoặc kép
- **length:** 150–220 từ; video càng dài prompt càng dài
- **multi_shot:** vẫn là một đoạn văn, không dùng danh sách cảnh, đánh số hay định dạng kịch bản; chỉ rõ cắt cảnh trong câu ("A hard cut transitions to…"), sau cắt thì giới thiệu lại cỡ cảnh, dùng cùng cách gọi, nói âm thanh có tiếp nối không. Khuyến nghị 2–4 cảnh.
- **references:** không có ký hiệu tham chiếu.
- **dialogue:** lời thoại đặt trong ngoặc kép, ghi rõ ngôn ngữ hoặc giọng; lời thoại dài chia thành câu ngắn, giữa các câu chèn một chỉ dẫn diễn (ánh mắt, dừng, giọng, động tác). Có đầu vào âm thanh thì âm thanh quyết định cấu trúc thời gian, prompt chỉ viết hình.
- **negatives:** có sẵn danh sách phủ định tiếng Anh mặc định; bản chưng cất (CFG=1) không có đầu vào phủ định.
- **camera:** follows, tracks, pans across, circles around, tilts upward, pushes in, pulls back, overhead view, handheld movement, over-the-shoulder, static frame; "slow dolly in" và "handheld tracking" là ổn định nhất. Máy đứng yên phải nói rõ "the camera remains static"; viết chuyển máy rồi mô tả chủ thể trông như thế nào sau đó. Thông số bằng số (2 độ mỗi giây) không có tác dụng.
- **frame_mode:** mở đầu nói đúng với hình khung đầu, viết thành một cảnh quay liền ("Single continuous take"); mô tả không khớp hình sẽ gây cắt cảnh.
- **frames:** chiều rộng và chiều cao đều chia hết cho 32, số khung là 8k+1.
- **rewriter:** enhance_prompt mặc định tắt.
- **pitfalls:**
  - Chữ đọc được trong hình và logo, vật lý lộn xộn, nhiều nhân vật, ánh sáng mâu thuẫn đều dễ có vấn đề.
- **unverified:**
  - Mô tả âm thanh đặt giữa câu hay cuối câu: các phiên bản chính thức nói khác nhau.
- **sources:** ltx.io (ltx-2-5-prompt-guide; prompting-guide-for-ltx-2; directing-dialogue-and-acting); github.com/Lightricks/LTX-2 (README)

### hunyuanvideo-1.5
- **basis:** vendor
- **structure:** sinh từ văn bản: chủ thể + động tác + cảnh + [cỡ cảnh] + [máy] + [ánh sáng] + [phong cách] + [không khí]. Động tác phức tạp: thiết lập cảnh + tách động tác theo thứ tự (đầu tiên… rồi… tiếp… đồng thời… cuối cùng…) + chi tiết then chốt. Thay từ cảm xúc bằng chi tiết động tác; phương hướng dùng toạ độ hình (bên trái / phải khung, tiền cảnh / hậu cảnh); nhiều nhân vật phân biệt bằng thuộc tính hoặc vị trí.
- **language:** tiếng Trung, tiếng Anh đều được
- **length:** viết dài được (sau khi viết lại khoảng 350 từ)
- **multi_shot:** không có cách viết nhiều cảnh, một lần một cảnh.
- **references:** không có ký hiệu tham chiếu.
- **dialogue:** không có âm thanh. Dấu ngoặc ở đây nghĩa là chữ trên hình: prompt tiếng Trung dùng “”, tiếng Anh dùng "".
- **negatives:** negative_prompt mặc định trống, không có phủ định chính thức; bản chưng cất CFG=1.
- **camera:** The camera moves upward / downward, moves to the left / right, moves forward, moves back, tilts up / down, pans to the left / right, circles around, follows, remains static; bản tiếng Trung của chính thức dùng các cụm: đẩy máy tiến lên, kéo máy xa chậm, máy bám theo, máy quay quanh, máy đứng yên, máy cầm tay.
  - Lưu ý: đây là bản dịch nghĩa của các cụm tiếng Trung trong file gốc; nếu cần đối chiếu chữ nguyên văn thì xem file gốc.
- **frame_mode:** sinh từ ảnh: chuyển động chủ thể + chuyển động cảnh + [máy]; không thêm chuyển máy người dùng không yêu cầu.
- **rewriter:** rewrite mặc định bật; đã viết theo cấu trúc trên thì có thể tắt.
- **sources:** github.com/Tencent-Hunyuan/HunyuanVideo-1.5 (HunyuanVideo_1_5_Prompt_Handbook_EN.md; README.md)

### flux-3-video
- **basis:** vendor
- **structure:** chủ thể và động tác → máy quay → cảnh và không khí → chất cảm chuyển động → ràng buộc liên tục
- **multi_shot:** "SHOT ONE: … HARD CUT. SHOT TWO: …", khuyến nghị 2–3 cảnh, tổng dưới 20 giây; nối tiếp thì viết như cùng một cảnh quay liền, không cắt.
- **dialogue:** lời thoại đặt trong ngoặc kép viết nguyên văn, và gọi tên người nói nhìn thấy được trong hình; lời thuyết minh ngoài hình ghi voiceover; lời không ghi người nói có thể bị vẽ thành chữ trên hình, nên thêm "no on-screen text or subtitles"; nhiều ngôn ngữ thì ghi ngôn ngữ cạnh từng câu; không muốn nhạc thì viết "no music"; mỗi hiệu ứng âm gắn với một động tác nhìn thấy được.
- **camera:** có danh sách thuật ngữ máy chính thức (xem nguồn).
- **frame_mode:** sinh từ ảnh viết chuyển động, không mô tả ảnh; khung đầu–cuối viết quá trình chuyển, hai khung phải liên quan; nhiều keyframe viết quá trình biến đổi, thứ tự có ý nghĩa, phong cách hình phải nhất quán, nếu không sẽ bị coi là cắt cảnh.
- **frames:** tối đa 10 keyframe, có thể ghi giây; từ 3 khung trở lên phải chỉ định thời lượng; keyframe, nối tiếp và bản nháp là ba chế độ loại trừ nhau.
- **sources:** docs.bfl.ml (prompting_video_overview; prompting_video_image_to_video; video_multishot_films; prompting_video_audio; prompting_video_camera_terms)

### flux-3-video-max
- **basis:** vendor
- **structure:** không có hướng dẫn riêng, theo cách viết của FLUX 3 Video (rea-video models flux-3-video)
- **frames:** tối đa 10 keyframe, chỉ định theo số thứ tự khung ở 24fps; khung cuối dùng end_image_url.
- **unverified:** cách viết của FLUX 3 Video có áp dụng đầy đủ cho Max không.
- **sources:** docs.bfl.ml (api-reference generate-a-video-with-flux-3-max)

### runway-gen-4.5
- **basis:** vendor
- **structure:** sinh từ văn bản: "[Camera] shot of [subject] [action] in [environment]. [mô tả bổ sung]"; sinh từ ảnh: "The camera [chuyển máy] as the subject [động tác]. [mô tả bổ sung]". Không nhận định dạng JSON.
- **language:** nhận mọi ngôn ngữ, tiếng Anh ổn định nhất
- **length:** dưới 1000 ký tự, không viết nhiều đoạn dài
- **multi_shot:** coi là một cảnh; mốc thời gian chỉ dùng để sắp thứ tự động tác: sinh từ văn bản "[00:00 through 00:02] …", sinh từ ảnh "[00:01] X occurs. [00:03] Y occurs." hoặc "X occurs, then Y occurs. Finally, Z occurs."; không đảm bảo chính xác. Có cắt thừa thì tăng thời lượng hoặc viết "Continuous, seamless shot".
- **references:** Gen-4.5 không nhận ảnh tham chiếu để sinh video; muốn giữ nhất quán nhân vật thì dùng Gen-4 References sinh khung đầu trước (trong prompt dùng @tên để gọi tham chiếu đã lưu), rồi mới sinh video từ khung đầu.
- **dialogue:** không có âm thanh gốc; bỏ lời thoại và hiệu ứng âm trong prompt; muốn khẩu hình thì dùng Act-Two (nhập một video diễn, không dùng chữ).
- **negatives:** không hỗ trợ phủ định, có thể ra kết quả ngược lại; viết lại tích cực ("sharp focus" thay vì "not blurry", "The locked-off camera remains perfectly still.").
- **camera:** các thuật ngữ máy chuẩn đều nhận; máy đứng yên viết "Locked camera. The camera remains still."
- **frame_mode:** chủ yếu viết chuyển động, không mô tả thứ đã có trong ảnh; chủ thể dùng "the subject" hoặc vị trí ("The subject on the left") để gọi; chỉ mô tả khi đưa vào yếu tố mới, thay đổi rõ rệt hoặc tương tác.
- **frames:** chỉ nhận khung đầu, không có khung cuối; khung có mờ chuyển động hoặc đang giữa động tác sẽ xung đột với prompt, nên xử lý sạch trước; tỷ lệ ảnh sinh 1280:720, 720:1280, 1104:832, 960:960, 832:1104, 1584:672.
- **rewriter:** Enhance Prompt là nút tuỳ chọn trên giao diện, API không có tính năng viết lại.
- **sources:** help.runwayml.com (47313737321107; 48324313115155; 47313698911891); docs.dev.runwayml.com (api)

### runway-aleph-2
- **basis:** vendor
- **structure:** động từ + thay đổi mong muốn, ngắn và cụ thể: add, remove, change, replace, re-light, re-style ("Change the outfit and bag to soft yellow"). Không phải mô tả cảnh.
- **language:** tiếng Anh ổn định nhất
- **references:** sửa một khung, mô hình mang thay đổi đó đi cả đoạn; Extra motion chỉ viết chuyển động không có trong video gốc.
- **frames:** video gốc 2–30 giây, 480p–1080p, 24–30 fps
- **sources:** help.runwayml.com (52150503729171; 51683104370451)

### luma-ray3.2
- **basis:** vendor
- **structure:** đặt chuyển máy lên đầu, rồi đến bối cảnh, việc gì xảy ra, ánh sáng và phong cách; thêm một từ về tốc độ (slowly, smoothly). Dùng động từ tiến hành (running, không dùng begins to run), thì hiện tại.
- **language:** tiếng Anh
- **length:** khoảng 100 từ (giới hạn 6000 ký tự)
- **multi_shot:** không có mốc thời gian và cách viết nhiều cảnh, một lần một cảnh; một prompt một kiểu máy.
- **references:** không có cú pháp đánh dấu; có tham chiếu nhân vật thì prompt chỉ viết bối cảnh và động tác, nhận dạng giao cho ảnh tham chiếu.
- **dialogue:** không có âm thanh; không viết lời thoại và hiệu ứng âm.
- **negatives:** chỉ viết tích cực, không có trường phủ định; tránh các từ vibrant, whimsical, hyper-realistic.
- **camera:** pan, tilt, dolly, zoom, tracking, crane, orbit, drone, whip pan; xếp nhiều chuyển máy thì kết quả rối.
- **frame_mode:** dùng keyframe thì chỉ viết phần thay đổi, không viết phần đứng yên.
- **frames:** khung đầu–cuối chỉ ra được 5 giây; 10 giây phải dùng keyframe có số thứ tự khung, không được dùng chung với khung đầu–cuối; ảnh dưới 50 MB, cạnh dưới 8000 px.
- **pitfalls:**
  - Hành động dày đặc nhiều chủ thể còn yếu.
  - Khung cuối khớp rồi nhưng chuyển động giữa không chắc liền mạch.
- **sources:** lumalabs.ai (ai-camera-movement-prompts; luma-video-models-guide-ray3.14-veo-sora-kling-compared); docs.agents.lumalabs.ai (video-generation)

---

## Mô hình ảnh (sinh khung đầu / keyframe)

### minimax-h3-image
- **basis:** vendor
- **length:** tối đa 32000 ký tự; khi tắt viết lại thì chỉ khoảng 4096 token đầu có tác dụng
- **references:** <Picture 1> đến <Picture 16> (cách nói của bên thứ ba)
- **negatives:** không có prompt phủ định, API sẽ từ chối
- **frames:** kích thước 655360–20000000 pixel, tỷ lệ 1:3–3:1, hoặc dùng area chọn 1K / 2K / 4K; mỗi lần 1–10 ảnh.
- **rewriter:** disable_prompt_enhanced mặc định false (mở rộng prompt đang bật); muốn kiểm soát chính xác thì đặt true.
- **pitfalls:**
  - Yêu cầu không có tính lũy đẳng, thử lại sẽ bị tính tiền lần nữa.
- **sources:** platform.minimax.io (image-generation-h3-generations); orcarouter.ai (minimax-h3-image-launch)

### midjourney-v8.2
- **basis:** third-party
- **structure:** câu tự nhiên, chủ thể đặt trước, tham số đặt cuối; không xếp chồng nhãn như 8k, masterpiece.
- **references:** --sref tham chiếu phong cách (tối đa 20 ảnh) để khoá hoạ phong; --oref tham chiếu nhân vật 1 ảnh, --ow khuyến nghị dưới 400, nhưng V8 có hỗ trợ hay không các nguồn nói khác nhau; --cref không hỗ trợ.
- **negatives:** --no (một số giao diện V8 bên thứ ba không hỗ trợ)
- **frames:** tỷ lệ khung dùng --ar; --raw giảm tạo kiểu; chữ trong hình đặt trong ngoặc kép, 2–4 từ là ổn định nhất.
- **unverified:** trang chính thức không mở được; mức hỗ trợ tham số lấy từ bên thứ ba.
- **sources:** evolink.ai (midjourney-v8-1-prompt-guide); blakecrosley.com (midjourney guide)

### gpt-image-2.5
- **basis:** vendor
- **structure:** bối cảnh / cảnh → chủ thể → chi tiết then chốt → ràng buộc, và ghi rõ mục đích; prompt phức tạp chia thành các đoạn ngắn có nhãn hoặc xuống dòng. Tham số máy ảnh chỉ là tham chiếu cảm quan, không mô phỏng chính xác.
- **language:** chủ yếu tiếng Anh; chính thức không nói việc hiển thị chữ Trung
- **references:** đánh số và ghi vai trò cho ảnh đầu vào: "Image 1: product photo… Image 2: style reference…", rồi viết cách kết hợp ("apply Image 2's style to Image 1"). Sửa ảnh viết "chỉ sửa X, còn lại giữ nguyên", danh sách giữ nguyên lặp lại ở mỗi vòng ("Do not change her face, facial features, skin tone, body shape, pose, or identity in any way.").
- **negatives:** không có trường phủ định, viết trực tiếp "no watermark", "no extra text"
- **frames:** chữ trong hình đặt trong ngoặc kép hoặc viết hoa toàn bộ, ghi rõ kiểu chữ; tên thương hiệu khó đọc viết từng chữ cái; cạnh là bội số của 16, tỷ lệ không quá 3:1.
- **pitfalls:**
  - Ra một bộ keyframe: làm trước một ảnh định hình nhân vật, rồi sửa dựa trên ảnh đó, chỉ đổi cảnh và động tác, mỗi lần kèm "Same facial features, proportions, and color palette" "Do not redesign the character".
  - Sinh liên tiếp nhiều ảnh trong cùng một phiên sẽ tích nhiễu, nên đổi phiên mới.
- **sources:** developers.openai.com (guides/image-prompting; cookbook image-gen-models-prompting-guide)

### gpt-image-2.6
- **basis:** vendor
- **structure:** cảnh → chủ thể → chi tiết → ràng buộc, có thể chia đoạn có nhãn; không có cú pháp đặc biệt. Kích thước và chất lượng đặt bằng tham số API, không viết vào prompt.
- **references:** đánh số và ghi vai trò: image 1 là chủ thể, image 2 là phong cách / trang phục / nền. Sửa ảnh viết "chỉ sửa X", liệt kê những thứ cần giữ (danh tính, hình học, bố cục, ánh sáng, nhãn), cuối cùng thêm "Do not change anything else"; có thể khoanh vùng cần sửa trên ảnh 1.
- **negatives:** không có trường phủ định, viết trong prompt ("no extra text")
- **frames:** chữ đặt trong ngoặc kép, ghi rõ vị trí và kiểu chữ, từ hiếm viết từng chữ cái; cạnh tối đa 3840, bội số của 16, tỷ lệ 1:3–3:1.
- **pitfalls:**
  - Ra bộ keyframe: làm một ảnh tham chiếu nhân vật trước, sau đó mỗi ảnh đều kèm theo nó, lặp lại chi tiết ngoại hình và viết "Do not redesign the character".
  - Khi cần một vùng không đổi đến từng pixel: sau khi sinh thì ghép lại vùng gốc, đừng trông vào prompt.
  - Khi sửa không truyền input_fidelity.
- **sources:** developers.openai.com (guides/image-prompting; guides/image-generation)

### nano-banana-2.1
- **basis:** vendor
- **structure:** [chủ thể] + [động tác] + [địa điểm / môi trường] + [bố cục] + [phong cách], viết thành câu tường thuật hoàn chỉnh, mở đầu bằng một động từ rõ ràng, không xếp từ khoá. Có ảnh tham chiếu: [ảnh tham chiếu] + [quan hệ] + [cảnh mới].
- **language:** chủ yếu tiếng Anh; chữ trong hình đặt trong ngoặc kép và ghi kiểu chữ
- **references:** nói đời thường vai trò của từng ảnh; khoá nhận dạng viết "Keep the person's facial features exactly the same as Image 1."; nhiều người viết "Make sure to only have one of each character in each image.". Tối đa 14 ảnh (10 vật thể, 4 nhân vật). Sửa ảnh phải ghi rõ cái gì giữ nguyên hoàn toàn, không cần mặt nạ.
- **negatives:** không viết phủ định, đổi thành mô tả tích cực ("empty street" thay vì "no cars").
- **frames:** độ phân giải 1K / 2K / 4K; không chỉ định thì đầu ra cùng kích thước ảnh vào; keyframe sinh từng ảnh một, đưa ảnh trước vào prompt sau và ghi rõ nhân vật và trang phục không đổi.
- **pitfalls:**
  - Ảnh đã đúng khoảng 80% thì nêu chỉnh sửa cụ thể, đừng sinh lại toàn bộ.
  - Sửa nhiều vòng thì chất lượng giảm.
  - Đôi khi không ra đúng tỷ lệ yêu cầu.
- **sources:** cloud.google.com (ultimate-prompting-guide-for-nano-banana); aistudio.google.com (image-generation); dev.to (nano-banana-pro-prompting-guide-strategies)

### seedream-5.0
- **basis:** vendor
- **structure:** câu tự nhiên ngắn gọn, mạch lạc: chủ thể + hành vi + môi trường, phong cách, màu, ánh sáng, bố cục bổ sung bằng cụm ngắn; ngắn gọn chính xác tốt hơn xếp tính từ; có thể nói rõ mục đích.
- **language:** tiếng Trung, tiếng Anh
- **length:** tiếng Trung dưới 300 chữ, tiếng Anh dưới 600 từ
- **references:** chỉ bằng "hình một / hình hai" và nói rõ vai trò: "thay chủ thể hình một bằng chủ thể hình hai", "cho người trong hình một mặc trang phục của hình hai", "tham chiếu phong cách hình hai, chuyển đổi phong cách hình một". Phần cần giữ nguyên phải nói rõ ("và giữ nguyên động tác"), không dùng đại từ như "nó". Bản 5.0 pro / flash có thể dùng toạ độ <bbox> để chỉ vùng.
- **negatives:** hướng dẫn chính thức không đề cập prompt phủ định.
- **frames:** chữ trong hình đặt trong ngoặc kép; ra bộ keyframe: 5.0 lite / 4.x dùng "một loạt", "một bộ", "bộ ảnh" hoặc ghi số lượng để kích hoạt bộ ảnh (tối đa 15 ảnh); 5.0 pro / flash không hỗ trợ bộ ảnh, đưa cùng bộ ảnh tham chiếu và sinh từng ảnh. Giữ nhân vật nhất quán: tải ảnh tham chiếu lên và viết "hình tượng nhân vật trong ảnh tham chiếu" cộng cảnh mới.
- **rewriter:** optimize_prompt_options.mode chỉ có standard (mặc định) và fast, không có tắt.
- **pitfalls:**
  - Chữ nhỏ hiển thị yếu: chữ phải ngắn, ghi rõ vị trí.
  - Da quá mịn, có thể viết mô tả khuyết điểm như "không có bộ lọc làm đẹp".
- **sources:** docs.volcengine.com (seedream-4-0-5-0-prompt-guide; image-generation-api; seedream-5-0-pro)

### seedream-5.5
- **basis:** vendor
- **structure:** cùng cách viết với Seedream 5.0 (rea-video models seedream-5.0): câu tự nhiên ngắn gọn viết chủ thể + hành vi + môi trường
- **length:** tiếng Trung dưới 300 chữ, tiếng Anh dưới 600 từ
- **references:** dùng "hình 1 / hình 2": "thay trang phục hình 1 bằng trang phục hình 2"; phần giữ nguyên ghi rõ ("giữ nguyên bố cục"); tối đa 10 ảnh.
- **frames:** chữ đặt trong ngoặc kép (tiêu đề là “…”); kích thước điều khiển bằng tham số size; không hỗ trợ bộ ảnh, bộ keyframe phải đưa cùng bộ ảnh tham chiếu và sinh từng ảnh.
- **pitfalls:**
  - Chính thức nói có thể liên tục sửa 100 vòng, vùng không sửa thì không đổi; phù hợp để ra một ảnh rồi sửa dần.
- **sources:** docs.volcengine.com (82379/1824121)

### qwen-image-3.0-pro
- **basis:** vendor
- **language:** chỉ hỗ trợ tiếng Trung và tiếng Anh
- **length:** prompt 800–1300 token; negative_prompt dưới 500 ký tự
- **references:** dùng "hình 1 / hình 2" theo thứ tự mảng: "hình 1 nữ sinh mặc váy đen hình 2 ngồi xuống theo tư thế hình 3"; 3.0 nhận 1–3 ảnh đầu vào. Phần cần giữ nói rõ (giữ trang phục, kiểu tóc, biểu cảm không đổi).
- **negatives:** 3.0 có trường negative_prompt. Ví dụ chính thức: độ phân giải thấp, chất lượng thấp, chi tiết cơ thể dị dạng, ngón tay dị dạng, màu quá bão hoà, cảm giác tượng sáp, khuôn mặt không có chi tiết, quá mịn, cảm giác AI. Bố cục lộn xộn. Chữ mờ, biến dạng.
- **frames:** chữ nhiều dòng và đoạn văn trong tiếng Trung rất mạnh, chữ đặt trong dấu ngoặc kép tiếng Trung “”; kích thước viết dạng rộng*cao, 16:9 khuyến nghị 2688*1536, 9:16 khuyến nghị 1536*2688; cạnh ảnh đầu vào 384–3072 px, dưới 10 MB.
- **rewriter:** prompt_extend mặc định bật, sẽ viết lại prompt; muốn kiểm soát chính xác thì tắt.
- **sources:** help.aliyun.com (qwen-image-edit-guide; qwen-image-api)

### qwen-image-2.1
- **basis:** vendor
- **language:** tiếng Trung, tiếng Anh
- **references:** tối đa 10 ảnh đầu vào; sửa cục bộ có thể khoanh, tô, hoặc đưa mặt nạ.
- **frames:** muốn nền trong suốt thì kẹp mô tả chủ thể giữa "This is an RGBA image with transparency." và "The image has alpha channel and the background is transparent."; gốc 2K, kích thước khuyến nghị 2048x2048, 2752x1536 và các bản dọc tương ứng.
- **rewriter:** có mô hình viết lại riêng Qwen-Image-2.1-PE-T2I / -PE-I2I, dùng để mở rộng prompt ngắn.
- **sources:** huggingface.co (Qwen-Image-2.1); alibabacloud.com (qwen-image-2-1-pro-and-turbo-apis)

### flux-3
- **basis:** vendor
- **structure:** chủ thể + động tác + phong cách + môi trường, cái quan trọng đặt trước (đứng trước có trọng số cao hơn); 30–80 từ.
- **language:** tiếng Anh chính xác nhất; tiếng Trung chưa nói rõ
- **references:** chỉ vị trí và ghi vai trò: "subject from image 1, style from image 2, background from image 3"; 1–10 ảnh. Sửa ảnh chỉ nói phần cần đổi, phần giữ nguyên nói rõ ("while maintaining the same facial features and hairstyle"), dùng động từ cụ thể.
- **negatives:** không hỗ trợ prompt phủ định, cũng không có các trường seed, guidance, prompt_upsampling (truyền thừa sẽ báo lỗi); viết lại tích cực ("sharp focus throughout").
- **frames:** chữ đặt trong ngoặc kép, đặt phía trước, phải ngắn; mã màu viết kèm color hoặc hex và gắn với vật cụ thể ("in color #0047AB"); chế độ auto thì khung đầu ra theo ảnh đầu vào thứ nhất.
- **rewriter:** mở rộng prompt luôn bật, không tắt được (cách nói của bên thứ ba).
- **pitfalls:**
  - Một bộ phân cảnh thì mỗi ô đều phải lặp lại đầy đủ mô tả nhân vật.
  - Ra một bộ ảnh: giữ cố định chủ thể, phong cách, ánh sáng, bảng màu, chỉ đổi một câu về máy; muốn chỉnh tinh thì lấy một ảnh được chọn làm tham chiếu và sửa, viết lại prompt tức là làm lại từ đầu.
- **unverified:**
  - Prompt có cấu trúc dạng JSON là tài liệu của FLUX.2, FLUX 3 không nêu.
- **sources:** docs.bfl.ai (prompting_guide_flux2); docs.bfl.ml (prompting_unified_reference; prompting_editing_overview); runware.ai (bfl-flux-3-image guides/prompting)

### kling-o3-image
- **basis:** vendor
- **structure:** câu tự nhiên; viết rõ giữ gì, đổi gì, ảnh tham chiếu nào quản yếu tố nào.
- **length:** dưới 2500 ký tự, không có trường phủ định riêng
- **references:** trên app dùng Image 1 / Image 2; API viết <<<image_1>>>; ảnh cộng chủ thể tối đa 10. Mẫu: "Use Image 1 as the base. Dress the person in Image 1 with the dress from Image 2 and the handbag from Image 3."; mục giữ nguyên viết "keeping all facial features, poses, and lighting the same", "leaving everything else untouched"; mỗi lần chỉ sửa một yếu tố.
- **frames:** có chế độ bộ ảnh (chỉ có bản Omni; API viết result_type: series, series_amount 2–9), có thể tiếp tục bộ phân cảnh từ một ảnh ("Predict the next part of the story based on this image and generate six storyboard frames."); 1K / 2K / 4K.
- **sources:** kling.ai (klingai-image-3-omni-user-guide; image-omni; kling-image-3-vs-omni)

---

## Mô hình điều khiển nhân vật (ít có thể điều khiển bằng chữ)

### kling-motion-control
- **basis:** third-party
- **structure:** prompt không bắt buộc: viết danh tính, môi trường, ánh sáng, phong cách; không mô tả động tác, động tác do video tham chiếu quyết định.
- **length:** dưới 2500 ký tự
- **frames:** ảnh từ 300 px trở lên, dưới 10 MB, chủ thể chiếm trên 5% khung, không bị che, lộ đầu; video tham chiếu là một cảnh liền, chỉ có một người, không cắt cảnh và không chuyển máy; ảnh và video phải cùng cỡ toàn thân / nửa thân. character_orientation=image giữ hướng của ảnh (video 3–10 giây), =video theo hướng và máy của video (3–30 giây).
- **camera:** theo hướng ảnh thì có thể viết chuyển máy trong prompt; theo hướng video thì chuyển máy theo video tham chiếu.
- **pitfalls:**
  - Gắn chủ thể 3.0 chỉ dùng khuôn mặt (không quan tâm quần áo, kiểu tóc, trang điểm), và chỉ dùng được ở chế độ theo hướng video; nếu nhiều người trong khung có kích thước gần bằng nhau thì việc gắn sẽ thất bại.
  - Động tác quá nhanh và phức tạp thì đầu ra có thể ngắn hơn video tham chiếu, và tín dụng không hoàn lại.
- **sources:** kling.ai (motion-control-user-guide); apidoc.cometapi.com (kling motion-control); fal.ai (kling-video-2-6-motion-control-prompt-guide)

### kling-avatar-v2
- **basis:** vendor
- **structure:** prompt không bắt buộc, chỉ viết biểu cảm, động tác và máy quay, không viết ngoại hình ("Smiling warmly at the camera, she gently touches her necklace… stationary shot.").
- **length:** dưới 2500 ký tự
- **dialogue:** trong văn bản lời thoại dùng dấu phẩy để kiểm soát ngắt nghỉ.
- **frames:** ảnh từ 300×300 trở lên, tỷ lệ 1:2.5–2.5:1; âm thanh 2–300 giây.
- **sources:** kling.ai (kling-ai-avatar-2-user-guide; avatar.md)

### wan-2.2-animate
- **basis:** vendor
- **structure:** API bằng Bailian không có tham số prompt, chỉ nhận ảnh, video và chế độ; bản mã nguồn mở dùng một prompt mặc định ("người trong video đang làm động tác") là đủ.
- **sources:** help.aliyun.com (wan-animate-move-api); github.com/Wan-Video/Wan2.2 (generate.py)

### wan-animate-2
- **basis:** vendor
- **structure:** prompt viết ngoại hình nhân vật (không viết động tác) cộng mô tả nền khách quan; mẫu chính thức là tiếng Trung, do mô hình lớn xem hình sinh; góc nhìn cũng chỉ bằng chữ.
- **sources:** github.com/Wan-Video/Wan-Animate-2

### viggle-animate
- **basis:** vendor
- **structure:** bước sinh video không có prompt chữ; prompt được dùng ở bước trước: dùng mô hình ảnh đổi một khung của video dẫn thành nhân vật mới.
- **sources:** viggle.ai (viggle-animate-character-replacement-from-a-repainted-frame)

### omnihuman-2.0
- **basis:** vendor
- **structure:** prompt không bắt buộc: viết cảnh, động tác và máy quay, cũng có thể thêm vật hoặc hiệu ứng không có trong ảnh; không mô tả ngoại hình.
- **language:** tiếng Trung, Anh, Nhật, Hàn, Tây Ban Nha, Indonesia
- **frames:** cạnh ảnh 300–6000 px, tỷ lệ 0.4–2.5, dưới 30 MB; âm thanh 4–300 giây, wav / mp3.
- **unverified:**
  - Nội dung tài liệu BytePlus chưa đọc được, tham số lấy từ fal.
- **sources:** fal.ai (omnihuman v2 llms.txt); docs.byteplus.com (omnihuman-2-0-video-generation)

### sync-3
- **basis:** vendor
- **structure:** không có prompt hình ảnh; đầu vào là video hoặc ảnh tĩnh, cộng âm thanh hoặc văn bản TTS.
- **language:** trên 95 ngôn ngữ; lồng tiếng tích hợp 92 ngôn ngữ
- **frames:** gói miễn phí mỗi lần tối đa 15 giây.
- **sources:** sync.so (models/sync-3)

### sync-react-1
- **basis:** vendor
- **structure:** options.prompt chỉ nhận một từ cảm xúc: happy, angry, sad, neutral, disgusted, surprised; không viết thì giữ cảm xúc của video gốc. model_mode chọn lips (chỉ đổi miệng), face (mặc định) hoặc head (đổi cả chuyển động đầu).
- **frames:** tối đa 15 giây; trong hình chỉ được có một người nói rõ ràng.
- **sources:** sync.so (models/react)

### ltx-2.3-lipsync
- **basis:** vendor
- **structure:** mẫu khẩu hình lồng tiếng: [Speaker] is speaking [Language/Accent], saying: "[Dialogue]". Lời thoại viết nguyên văn toàn bộ, chỉ một người nói, số âm tiết gần với câu gốc.
- **language:** các ngôn ngữ đã kiểm chứng: Anh, Pháp, Tây Ban Nha, tiếng German (Germany), Nga
- **sources:** ltx.io (ltx-2-5-prompt-guide)

### heygen-avatar-v
- **basis:** vendor
- **structure:** Custom Motion dùng ngôn ngữ đời thường chỉ đạo khuôn mặt, tay, tư thế, ánh mắt và trạng thái tinh thần ("Look at the camera, lean in, stay serious", "Thumbs up at the end"); trường API là motion_prompt, chỉ có tác dụng với video người ảo Avatar V; expressiveness chỉ có ở Avatar IV, Avatar V sẽ từ chối.
- **language:** nền tảng hỗ trợ hơn 177 ngôn ngữ và phương ngữ
- **length:** kịch bản tối đa 5000 ký tự; âm thanh tối đa 10 phút.
- **dialogue:** chưa tìm thấy cách viết chính thức cho dừng và đánh dấu cảm xúc trong kịch bản; more_blinking có thể làm người ảo chớp mắt nhiều hơn.
- **sources:** developers.heygen.com (changelog; usage-limits)

### synthesia-express-3
- **basis:** vendor
- **structure:** không có prompt động tác; cảm xúc (vui, nghiêm túc, trung tính, thân thiện) được tự xác định theo kịch bản, cử chỉ đi theo kịch bản.
- **language:** nền tảng hỗ trợ trên 140 ngôn ngữ
- **sources:** synthesia.io (updates/express-3)

### mirage-avatar-x
- **basis:** vendor
- **structure:** không có prompt động tác; biểu cảm, nhịp và động tác đi theo âm thanh hoặc kịch bản.
- **length:** kịch bản 50–1500 ký tự (tối đa 180 giây)
- **frames:** video tham chiếu 1–120 giây hoặc ảnh (cạnh ngắn từ 512 px trở lên); âm thanh tham chiếu 10–180 giây, chỉ dùng 60 giây đầu; chỉ có tỷ lệ 9:16 và 16:9.
- **sources:** fal.ai (mirage-avatar-x)

### longcat-video-avatar-1.5
- **basis:** vendor
- **structure:** viết prompt dài hơn; khác với đa số mô hình người ảo, phải viết ngoại hình, động tác và cảnh.
- **language:** tiếng Trung, tiếng Anh
- **pitfalls:**
  - CFG âm thanh đặt 3–5; khẩu hình chưa chuẩn thì tăng lên.
  - Video dài dễ lặp động tác, chỉnh --ref_img_index và --mask_frame_range.
- **sources:** huggingface.co (meituan-longcat/LongCat-Video-Avatar-1.5)

### creatify-aurora
- **basis:** third-party
- **structure:** prompt viết cách lấy khung hình, nền, ánh sáng, ánh mắt, và cơ thể có giữ yên hay không; guidance_scale và audio_guidance_scale đều trong khoảng 0–5.
- **sources:** fal.ai (creatify aurora llms.txt)
