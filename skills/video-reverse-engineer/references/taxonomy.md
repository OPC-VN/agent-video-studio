# Phân loại cách làm và bảng đối chiếu các trường hợp dễ nhầm
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/taxonomy.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

## 11 loại hình ảnh nền

| Nhãn | Tên tiếng Việt | Bằng chứng điển hình | Cách phục dựng |
|---|---|---|---|
| live_action | Quay thật | nhiễu cảm biến σ>1, nhiễu theo thời gian >0.8, tỉ lệ pixel không đổi qua các khung <0.55, rung tay cầm, 60fps gốc, siêu dữ liệu thiết bị quay | Footage quay thật (người dùng cung cấp) hoặc AI image-to-video xấp xỉ |
| ai_video | Video AI sinh ra | Texture ảnh không có nhiễu cảm biến, lặp khung 24→30 hoặc chu kỳ nội suy khung hình, chuyển động camera trôi mượt; VLM thấy ngón tay, chữ, vật thể biến dạng hoặc texture nhấp nháy | Sinh theo khung đầu–cuối bằng capsule-cinema |
| avatar | Người ảo nói trước camera | Máy cố định, chính diện khuôn mặt, chỉ miệng và đầu chuyển động, điều khiển bằng âm thanh | TTS/giọng nhân bản + người ảo |
| cg_3d | Render 3D | Vật liệu phẳng/sạch nhưng nền không đứng yên tuyệt đối từng pixel, hình học ổn định, không biến dạng | Blender/C4D, hoặc xấp xỉ bằng AI khung đầu–cuối |
| code_render | Render từ code/template | Khối phẳng >20%, số màu dùng <70, nhiều cạnh ngang/dọc; nền đứng yên tuyệt đối từng pixel, chỉ phần tử cục bộ chuyển động; không có texture vật liệu (gradient màu mượt, khối màu bão hòa đậm, glow trên nền tối, trường màu fractal/shader); trên nền tối, phần sáng toàn điểm sáng nhỏ hoặc nét mảnh (hạt, point cloud, wireframe) | Dựng lại bằng Remotion/HTML; báo cáo đưa cách làm theo loại hình ảnh (hạt → Three.js, trường màu → GLSL, gradient → CSS blur, biểu đồ → SVG/D3) |
| screen_capture | Quay màn hình/ảnh chụp màn hình | Giao diện sáng diện tích lớn, chữ nhỏ dày đặc, độ bão hòa thấp, cuộn toàn trang | Quay giao diện thật (người dùng cung cấp) |
| still_motion | Ảnh tĩnh pan/zoom | Tỉ lệ inlier theo biến đổi cứng >95%, residual <0.3px, sau bù chuyển động không còn phần dư, không có dấu vết tốc độ khung 24fps | Một ảnh + ffmpeg cục bộ dựng lại theo tham số đo được |
| static_hold | Khung tĩnh | Từ 85% trở lên số khung lặp lại đúng từng pixel | Một ảnh |
| anim_2d | Hoạt hình 2D | Công cụ không đo được, chỉ xem ảnh: đường nét và mảng màu phẳng ổn định, nhân vật có khung xương hoặc chuyển động từng khung, thường vẽ kiểu "on twos" (một hình giữ hai khung) | Ảnh thiết kế nhân vật + tạo theo khung đầu–cuối; khi cần khẩu hình hoặc chuyển động chính xác thì làm bằng AE / Live2D / Spine |
| stop_motion | Stop-motion | Công cụ không đo được, chỉ xem ảnh: vật liệu thật (đất sét, nỉ, giấy), chuyển động giật từng nhịp, nhấp nháy nhẹ giữa các khung, cùng vật thể thật với ánh sáng không đổi | Ưu tiên quay thật (máy cố định, khoảng 12 ảnh mỗi giây); AI chỉ xấp xỉ được |
| film_footage | Đoạn phim điện ảnh/truyền hình | Công cụ không đo được, chỉ đưa manh mối: khung hình nằm trong viền đen, nguồn 24/25fps. Xem ảnh để nhận: diễn viên hoặc phim nhận ra được, ánh sáng chuyên nghiệp và cắt luân phiên nhiều máy (shot/reverse shot), nhiều diễn viên quần chúng và bối cảnh dựng trọn bộ, logo kênh hoặc watermark nền tảng | Tìm đoạn gốc tương ứng để cắt (bản quyền thuộc hãng phim, dùng thương mại cần xin phép); không dùng bản gốc thì quay lại theo cùng cỡ cảnh và ánh sáng, hoặc xấp xỉ bằng AI |

`anim_2d` / `stop_motion` / `film_footage` chỉ được xác định từ việc xem ảnh: nếu chỉ một bên xem ảnh thì kết luận ghi "chờ xác nhận"; khi cả VLM và agent đều đã xem thì mới bỏ nhãn này.

`live_action` chỉ dùng cho khung hình do tác giả video hoặc khách hàng tự quay; đoạn cắt từ phim, phim truyền hình, phim ngắn tập có sẵn thì luôn là `film_footage`, dù trông giống quay thật đến đâu.

## Gia công AI trên quay thật (ai_edits)

Khi nền là quay thật hoặc stop-motion, xem thêm có bị gia công AI lần hai không, ghi vào `ai_edits`. Phương án phục dựng sẽ thêm mục "Gia công AI cần làm sau khi quay" vào sau phần các buổi quay.

| kind | Tên tiếng Việt | Nhìn vào đâu | Cách phục dựng |
|---|---|---|---|
| face_swap | Đổi mặt | Viền mặt và chân tóc nhấp nháy, màu da/ánh sáng mặt và cổ không khớp, khi quay nghiêng thì các nét trên mặt trôi lệch | Mô hình chỉnh sửa video R12 để đổi người |
| lip_sync | Đồng bộ khẩu hình/đổi lời thoại | Miệng và cằm không khớp lời, răng mờ, chỉ vùng miệng có chất lượng khác | Lồng tiếng lại và đồng bộ khẩu hình R13 |
| restyle | Vẽ lại cả đoạn theo phong cách | Hành động là người thật nhưng hình ảnh theo phong cách anime/sơn dầu/đất sét, texture trôi giữa các khung | Mô hình chỉnh sửa video R12 |
| outfit_swap | Đổi trang phục bằng AI | Texture áo nhấp nháy, chỗ giao với cánh tay bị nhòe | Ảnh thử đồ R05 + video |
| bg_replace | Tách nền đổi nền | Viền tóc có quầng sáng hoặc răng cưa, hướng sáng người và nền không khớp, phối cảnh nền sai | Keying phông xanh, hoặc R12 |
| object_edit | Thêm/xóa/đổi vật thể | Viền vật thể nhấp nháy, thiếu bóng | R12 |
| beautify | Làm đẹp/thon mặt | Da quá mịn, đường thẳng nền cong quanh mặt | Công cụ làm đẹp như Jianying (CapCut) |

## Bảng tra nhanh điểm phán đoán

| Hiện tượng | Chỉ về |
|---|---|
| Các khung liên tiếp lặp đúng từng pixel, đầu và cuối không đổi | Khung tĩnh; nếu là thẻ render phẳng thì xếp vào render từ code |
| Cả khung thu phóng/tịnh tiến theo một biến đổi cứng, bù chuyển động không còn phần dư, và **không có** dấu vết tốc độ 24fps | Ảnh tĩnh pan/zoom |
| Nhiều khối phẳng, ít màu, nhiều cạnh ngang/dọc | Render (code hoặc 3D); nền đứng yên tuyệt đối từng pixel, chỉ phần cục bộ chuyển động → hoạt ảnh 2D bằng code |
| Khoảng 20% khung lặp, chu kỳ 4–6 (24→30) | Nguồn 24fps: AI sinh / 3D / phim hoặc phim truyền hình, không phải quay gốc bằng điện thoại |
| Trong khung dọc có một khối hình 16:9 hoặc rộng hơn nằm giữa viền đen, trên là tiêu đề, dưới là phụ đề thuyết minh | Bố cục video thuyết minh phim → nghiêng về đoạn phim; phim ngắn AI kiểu điện ảnh cũng có viền đen, phải xem ảnh |
| Trên hình có "năm · «tên phim»", logo kênh, watermark nền tảng, hoặc nhiều đoạn với phong cách và màu sắc khác nhau chuyển nhanh | Video cắt ghép phim (mashup) / tuyển tập cảnh kinh điển → nghiêng về đoạn phim |
| Chỉ độ nét dao động theo chu kỳ, không có khung lặp (nội suy) | Bằng chứng yếu: nội suy và nén lại đều tạo ra hiện tượng này; cần xem ảnh để xác nhận |
| Gốc ≥48fps, không lặp, không có chu kỳ nội suy | Thường là quay thật bằng điện thoại/máy ảnh |
| Nhiễu cảm biến và nhiễu theo thời gian rõ, có rung tay | Quay thật |
| File chuyển mã từ nền tảng: toàn file gốc 30fps, cảnh quay thật không có khung lặp | Nghiêng về quay bằng điện thoại (sau chuyển mã, bằng chứng nhiễu mất hiệu lực, lấy tốc độ khung làm chuẩn) |
| Gần như không màu, chỉ vài màu, hình phẳng | Hoạt ảnh giao diện/tài liệu (render từ code), không phải 3D |
| Nền gần đen, phần sáng gần như toàn điểm sáng nhỏ hoặc nét mảnh, không có bề mặt sáng tối liên tục | Hình hạt/point cloud/wireframe (render từ code), không phải khối 3D, AI hay quay đêm thật |
| Gần như không có texture: gradient mượt, khối màu bão hòa, glow trên nền tối, hoặc trường màu cầu vồng | Gradient/vector/shader vẽ bằng code, không phải render 3D (3D có texture vật liệu như vải, vân gỗ); cả khung đều chuyển động cũng vậy |
| Nhạc phủ kín cả video, có giọng đang hát (nhiều nốt ngân giữ cao độ) | MV ca nhạc → nhiều khả năng bài hát do AI sinh |
| Lời thuyết minh + nhạc nền lót | Nhạc thông thường → nghiêng về thư viện có sẵn (chờ xác nhận; quy trình AI hay dùng Suno) |
| Tiếng ồn nền nhảy ở chỗ cắt | Âm thanh đi theo từng đoạn hình: video AI tự sinh tiếng, hoặc quay thật có tiếng thu trực tiếp |
| File có nhãn ẩn AIGC theo GB 45438, Label=1 | Đã khai báo là AI sinh (chỉ cho biết cả file có khai báo; từng cảnh vẫn phải xét riêng) |
| Trong panel màu nhạt có rất nhiều chữ cỡ nhỏ | Ảnh chụp giao diện được nhúng vào → tư liệu thật |
| Khoảng lặng giữa các câu nói vẫn có âm thanh to và có cao độ | Có nhạc nền lót |
| Nền rất tối nhưng có hạt, vùng sáng không phẳng, có khuôn mặt | Quay đêm/thiếu sáng thật (vùng tối bị làm phẳng do chuyển mã không phải đặc điểm của render) |
| Khuôn mặt chiếm ≥6% khung, có mặt suốt cảnh, đang nói | Cận cảnh người thật hoặc người ảo; khối phẳng trên tường/quần áo không tính là bằng chứng render |

## Đối chiếu các cặp dễ nhầm (xem từng mục khi review)

**Quay thật vs video AI**
- Quay thật: hạt nhiễu thay đổi theo khung; tay, chữ, người xa đều bình thường; đúng vật lý (vải, chất lỏng, va chạm).
- AI: da và ánh sáng quá hoàn hảo; người ở nền hoặc chữ bị rối; cạnh vật thể "sôi"; chuyển động chậm, trôi; cuối cảnh dễ đứng hình.
- Tốc độ khung: nguồn 24fps (AI/phim) so với 60fps gốc (điện thoại). Lưu ý AI nội suy lên 60fps sẽ để lại chu kỳ độ nét, `sharp_period_ac>0.45`.
- Lớp tất định là yếu nhất với cặp này, **bắt buộc kết hợp VLM và tự xem khung hình**.

**Video AI kiểu 3D hoạt hình vs render 3D thật**
- 3D thật: hình học và vật liệu ổn định từng khung; lông và vải chuyển động theo vật lý, lặp chính xác được; nhiều khối phẳng, ít màu.
- AI: vật thể biến dạng nhẹ trong cảnh, texture nhấp nháy, nhiễu giống ảnh chụp hơn (dùng >100 màu).
- Nhiều tài khoản "3D hoạt hình" trên Douyin là AI sinh, nhưng khi không có nhãn thì chỉ ghi "nghiêng về".

**Hình hạt trên nền tối vs render 3D vs video AI / quay đêm thật**
- Hình hạt (render từ code): cơ quan, cơ thể người, Trái Đất, phân tử... được ghép từ hàng nghìn điểm sáng hoặc nét mảnh, không có bề mặt sáng tối liên tục; thường đi kèm thẻ chương ở góc trên trái, chú thích dẫn, số nhảy. Three.js, AE Plexus / Trapcode đều làm được; phục dựng theo quy trình code.
- Render 3D: có bề mặt sáng tối liên tục, vật liệu và bóng đổ.
- Quay đêm thật / AI: vùng sáng là vật thể và đốm sáng có chuyển độ sáng tối, có hạt hoặc biến dạng.
- Khi review, `description` phải ghi rõ mỗi cảnh hạt ghép thành hình gì, màu gì, chuyển động thế nào (hướng hạt chảy, biến hình, đẩy máy/bay vòng quanh), chú thích và số nằm ở đâu. Bảng theo từng cảnh trong mục "Dựng hình bằng code" của báo cáo dùng chính nội dung này. Chỉ ghi "nền hạt" thì phục dựng ra chỉ là một đám đốm sáng.

**Gradient/phát sáng/trường màu vẽ bằng code vs render 3D**
- Cảnh code: gần như không có texture chi tiết, chỉ có gradient mượt, khối màu, glow và chữ; thường gặp: nền gradient đốm sáng, thẻ kính mờ, chữ neon, thẻ 3D CSS lật, phóng to fractal và shader plasma. Dù cả khung đang chuyển động (nền trôi, glow "thở") vẫn là render từ code.
- Render 3D: vật thể có texture vật liệu (vải, vân gỗ, kim loại, nhựa hạt), có bóng đổ và quan hệ sáng tối giữa các vật.
- Poster phẳng có thêm hạt phim: bỏ hạt đi còn lại khối màu phẳng thì tính là render từ code; hạt rất nặng (công cụ đo được nhiễu σ≥3) thì công cụ có thể không nhìn xuyên được, phải xem ảnh để phán đoán.
- Gradient mượt đổi màu chậm dễ bị nhầm thành chồng mờ (cross dissolve); công cụ loại trừ bằng việc "tốc độ biến đổi có ổn định không". Khi review, nếu một nền động liên tục vẫn bị cắt thành nhiều cảnh thì xử lý như một cảnh.

**Render từ code vs quay màn hình/ảnh chụp**
- Render từ code: chữ cỡ lớn, màu thương hiệu, vector sắc nét, phần tử có hoạt ảnh xuất hiện.
- Ảnh chụp: nền sáng, chữ nhỏ dày đặc, điều khiển giao diện (nút, icon, thanh điều hướng), thường bị thu phóng hoặc cuộn.
- Mẫu có nhúng ảnh chụp: lớp nền tính là render từ code, còn ảnh chụp được liệt kê riêng ở mục "tư liệu thật".

**Cách viết `description` cho cảnh render từ code**
- "Bảng thời gian hoạt ảnh từng cảnh" trong mục "Dựng hình bằng code" của báo cáo do công cụ đo: vị trí, thời điểm xuất hiện, hướng, đường cong nhanh chậm, mã màu của từng phần tử; các phần tử xuất hiện lần lượt được gộp thành một dòng "cách nhau X giây". Dải keyframe là `shots/shot_XXX_strip.jpg`, ảnh phần tử và ảnh ghép có đánh số là `shots/shot_XXX_elements.jpg`.
- Đối chiếu với các ảnh này, trong `description` ghi theo số thứ tự từng phần tử là gì (ví dụ "1–12: thẻ icon bo góc, lần lượt bật vào"), không lặp lại các giá trị đo.

**Ảnh tĩnh pan/zoom vs video AI đẩy máy chậm**
- Pan/zoom: phần mềm dựng render theo tốc độ khung của timeline, mỗi khung đều khác nhau, không có quy luật lặp 24→30.
- Đẩy máy của AI: có quy luật khung lặp của nguồn 24fps, chủ thể thường có chuyển động nhỏ (thở, chớp mắt).

**Hoạt hình 2D vs hoạt ảnh code vs video AI kiểu hoạt hình**
- Hoạt hình 2D: có nhân vật và diễn xuất, đường nét ổn định, chính xác theo khung, thường vẽ kiểu "on twos" (mỗi hai khung mới đổi hình).
- Hoạt ảnh code: chữ, hình và UI vào khung và easing, không có diễn xuất nhân vật.
- AI kiểu hoạt hình: đường nét trôi giữa các khung, chi tiết biến dạng, có dấu vết nguồn 24fps.

**Stop-motion vs video AI vs quay thật**
- Stop-motion: cùng một vật thật được dịch chuyển từng khung, ánh sáng không đổi, giữa các khung có nhấp nháy nhẹ và giật, vật liệu có dấu vân tay, mép xù.
- AI giả stop-motion: bản thân vật liệu đổi giữa các khung (vân đất sét trôi), không có nhịp giật thật.
- Công cụ hay đoán stop-motion là AI (quy luật khung tương tự); khi xem ảnh, tập trung kiểm tra vật liệu có ổn định không.

**Đoạn phim điện ảnh/truyền hình vs phim ngắn tập AI vs quay thật tự làm**
- Đoạn phim: diễn viên hoặc phim nhận ra được; ánh sáng đoàn phim chuyên nghiệp (đèn chính, đèn viền, nguồn sáng thực có trong bối cảnh), độ sâu trường ảnh và cắt luân phiên nhiều máy; nhiều diễn viên quần chúng, bối cảnh và đạo cụ dựng trọn bộ; cảnh hành động có diễn viên đóng thế và dây treo; chữ trong khung (biển hiệu, báo, màn hình) đọc rõ; thường có logo kênh, watermark nền tảng, chữ đầu phim và cuối phim (credit), hoặc khung rộng nằm trong viền đen.
- Phim ngắn tập AI: mặt quá hoàn hảo, các nhân vật khác nhau trông rất giống nhau; tay, răng, chữ bị lỗi; người nền ít và mờ; texture vật thể và quần áo trôi giữa các khung; cảnh thường là cận cảnh một người dài 5–10 giây. Tuyên bố miễn trừ kiểu "chỉ mang tính hiệu ứng điện ảnh" hoặc "theo nhu cầu cốt truyện" cũng thường thấy trong video thuyết minh phim ngắn tập AI, không được dùng riêng lẻ làm bằng chứng.
- Quay thật tự làm: nói trước camera, vlog, unboxing do tác giả hoặc khách hàng trực tiếp xuất hiện, quay bằng điện thoại hoặc nhóm nhỏ, không có bối cảnh và quần chúng cỡ đoàn phim.
- Video thuyết minh có chèn cảnh tác giả tự nói trước camera hoặc hình AI thì đánh nhãn riêng theo từng cảnh.
- Khi chỉ bật lớp đo pixel, công cụ sẽ đánh đoạn phim thành "video AI" hoặc "quay thật" kèm nhãn "chờ xác nhận"; khi review phải sửa lại.

**Cảnh game vs render 3D vs quay màn hình**
- Video chơi game, bình luận game, video cắt ghép game: lớp dưới là `screen_capture` (quay cảnh game đang render thời gian thực trên màn hình), không phải `cg_3d`. Nhận diện bằng HUD: thanh máu, minimap, tâm ngắm, icon kỹ năng, số sát thương, khung chat. Cách phục dựng là quay game; `description` ghi rõ tên game (khi nhận ra được), góc nhìn và vị trí HUD.
- CG quảng bá game, cảnh cắt (cutscene): không có HUD, cách dựng cảnh như phim, xếp vào `cg_3d`.
- Công cụ và VLM đều có thể đoán cảnh game có HUD là 3D hoặc giao diện quay màn hình; khi review lấy HUD làm chuẩn.

**Truyện tranh động (motion comic) / phim truyện tranh vs hoạt hình 2D vs video AI**
- Khung truyện tranh tĩnh chỉ đẩy, kéo, lia, trượt máy → `still_motion`; trên khung tranh có hoạt ảnh cục bộ như chớp mắt, tóc bay, miệng cử động → `anim_2d`; đường nét trôi giữa các khung, chi tiết biến dạng → `ai_video`.
- Phim truyện tranh thường là ảnh AI + hiệu ứng cục bộ; `image_source` điền `ai_image` hay vẽ tay thì xem nét vẽ và các chi tiết như ngón tay.

**Ảnh tĩnh: ảnh AI vs ảnh chụp thật vs thẻ render**
- Thẻ render (phẳng, ít màu) → xếp vào render từ code.
- Ảnh AI và ảnh chụp thật không phân biệt được ở lớp tất định, giao cho VLM; chưa phân biệt được thì ghi "tư liệu ảnh (thật/AI chờ xác nhận)".

## Cắt cảnh

- Cắt cứng: đỉnh của khoảng cách histogram và chênh lệch pixel, đồng thời diện tích thay đổi vượt 25%. Hiệu ứng xuất hiện phần tử không tính là cắt cảnh.
- Jump cut / push-in cut: cùng góc máy, cùng nền, vị trí người hoặc cỡ cảnh nhảy trong một khung. Diện tích thay đổi chỉ cần từ 17% trở lên, nhưng cao hơn mức biến thiên của các khung trước/sau ít nhất 2.5 lần; hai khung trước và sau đều ổn định, và hình không quay lại như trước điểm cắt.
- Chớp sáng, lửa đầu nòng súng, đèn nháy (strobe): hình sáng lên rồi trở lại trong một-hai khung, không tính là cắt cảnh; chuyển cảnh chớp trắng tan đi rồi lộ ra hình mới thì vẫn tính là cắt cảnh.
- Cảnh ngắn: cảnh có hình ổn định nằm giữa hai nhát cắt cứng gọn thì được giữ lại nếu dài từ 0.12 giây (cảnh chèn cắt nhanh, khung bìa mở đầu); các ranh giới nằm gần nhau hơn mức đó thuộc cùng một chuyển cảnh, chỉ giữ ranh giới mạnh nhất.
- Chồng mờ (cross dissolve): khung giữa là hỗn hợp tuyến tính của hai khung đầu–cuối (α trong khoảng 0.2–0.8, residual <0.2), và dùng optical flow để loại trừ chuyển động đẩy/kéo máy.
- Fade in/out: độ sáng giảm xuống cực tối hoặc cực sáng rồi trở lại.
- Chuyển cảnh không có cắt cứng: đoạn đầu hình ổn định, đoạn giữa chuyển tiếp, đoạn sau hình ổn định, hai đầu là hai hình khác nhau, và đoạn giữa giải thích được là fade / dissolve / wipe / slide thì mới tính là một ranh giới. Cùng cảnh chỉ sáng lên hoặc tối đi, hay đẩy/lia trong cảnh, không tính.
- Viền đen và banner cố định trên dưới được cắt bỏ trước khi đo; chuyển cảnh nằm trong viền đen không bị viền đen làm loãng.

**Loại chuyển cảnh** (`transition` của mỗi cảnh: `type`, thời điểm đầu `start` / cuối `end`, `duration`; nếu có hướng thì thêm `direction`)

| type | Trên hình là gì | Nhận biết bằng cách nào |
|---|---|---|
| `fade` | Qua khung đen hoặc trắng (`via`) | Giữa có khung đen hoặc trắng thuần; hai đầu là cùng một hình tối dần rồi sáng lên |
| `flash` | Chớp trắng, lóa sáng (light leak) cháy trắng rồi lộ hình mới | Giữa sáng gần trắng nhưng không phải khung phẳng; hoặc khung đầu cảnh mới rất sáng rồi giảm dần |
| `dissolve` | Chồng mờ (dissolve) | Mỗi khung giữa là hỗn hợp tuyến tính của hai đầu |
| `wipe` | Quét (cạnh thẳng, hình tròn, lá sách, kim đồng hồ) | Xem từng khối, mỗi khối hoặc là hình cũ hoặc là hình mới, diện tích hình mới tăng dần. `direction` là hướng cạnh di chuyển; `center_out` / `edges_in` là đóng mở hình tròn |
| `slide` | Trượt (`mode`: `push` hai hình cùng trượt, `cover` hình mới trượt vào, `reveal` hình cũ trượt đi) | Khung giữa ghép được từ hai hình đầu–cuối bằng cách dịch chuyển theo một cạnh thẳng |
| `whip` | Quét nhanh (whip pan): lia nhanh kèm mờ chuyển động, điểm cắt ẩn trong vùng mờ | Trước và sau điểm cắt cứng, hình dịch chuyển mạnh theo một hướng, chi tiết bị xóa |
| `zoom` / `spin` | Phóng to / xoay xông vào cảnh tiếp theo | Lượng zoom hoặc góc xoay ước lượng từng khung quanh điểm cắt cứng rất lớn |
| `blur` | Mờ rồi nét lại | Hai bên điểm cắt cứng, chi tiết ít hơn rõ rệt so với mức bình thường của cảnh |
| `glitch` | Nhiễu tín hiệu: lệch vị trí, hình cũ và mới nhấp nháy xen kẽ | Trong khoảng có nhiều bước nhảy cứng, và hình từng quay lại cảnh cũ |
| `shake` | Rung quanh điểm cắt | Dịch chuyển từng khung lớn nhưng triệt tiêu qua lại |

Whip, zoom, xoay, mờ và rung chỉ nhận diện khi nằm quanh cắt cứng; chuyển động cùng loại không có cắt cứng là chuyển động camera trong cảnh.
- Nhịp MG (motion graphics): trong một cảnh dài, "đứng hình → hoạt ảnh → đứng hình", nếu hai trạng thái đứng hình khác nhau trên 12% thì ghi là nhịp trong cảnh, không tính là cắt cảnh.
