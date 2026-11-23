---
name: video-storyboard-design
description: Design or revise an executable video storyboard from a brief, source documents or footage, selecting scene visuals and motion references and describing cues and transitions for a video production pipeline.
---

# Thiết kế storyboard video

> Video **trộn** người dẫn/avatar + quay màn hình + hoạt họa (giảng dạy, vlog kiến thức, kể chuyện) có thư viện bố cục, chuyển chế độ và kiểm nhịp riêng: dùng skill `vlog-design`; skill này cho storyboard chung và một chế độ.

Tạo file storyboard từ [mẫu chung](../video-routing/assets/storyboard.md) trong project/trạm được chọn. Đây là thiết kế để người hoặc agent dựng tiếp; không tự coi là spec, EDL, code hay video đã chạy. Nếu chỉ giao storyboard, dừng ở storyboard.

Khi người dùng cần storyboard để dựng, dùng **toàn bộ mẫu chi tiết**: brief, treatment, thiết kế chung, bản đồ cảnh, thẻ từng cảnh, nguồn/quyền và handoff. Mỗi cảnh cần lời nguyên văn, bố cục có vị trí, hình/icon cụ thể, lựa chọn motion có nguồn và lý do, bảng cue theo thời gian (trước → hành động → sau), âm, nối cảnh, chỉ dẫn dựng và mốc kiểm. Không thay thẻ chi tiết bằng một đoạn tóm tắt. Nếu chỉ được giao phác thảo ngắn, ghi rõ các phần chưa thiết kế.

Khi mở rộng storyboard sẵn có, lấy bản đó làm baseline: giữ các cảnh và quyết định dựng còn hiệu lực (lời, bố cục, cue, caption, âm, asset, nguồn, kiểm); nếu thay/gộp thì ghi rõ nội dung chuyển đi đâu và lý do. Bản tóm tắt là file riêng trỏ tới bản đầy đủ khi người dùng yêu cầu. Trước khi giao, đối chiếu nội dung thực của từng trường trong từng cảnh với mẫu, không chỉ kiểm có tiêu đề; kiểm cue liên tục, nguồn/quyền, sự khớp lời–hình–âm và chỉ dẫn thực thi; ô thiếu hoặc chưa kiểm phải ghi rõ, không tuyên bố đã chứng minh video.

## Phân tích và chọn cách kể

1. Đọc brief, tài liệu, treatment, transcript, footage/ghi chú đã được phép cung cấp. Tổng hợp người xem, mục tiêu, thông điệp, sự thật có nguồn, giả định, độ dài, định dạng, nguồn/quyền và các quyết định còn thiếu. Không bịa số liệu hay nhận minh họa là bản quay thật.
2. Xây 2–3 hướng kể khi có lựa chọn thực chất; so sánh phù hợp người xem, nội dung, tài nguyên và công sức, chọn một hướng có lý do. Chia nhịp theo ý, tránh cùng bố cục lặp lại. Người dùng đã chốt thì giữ hướng đó.
3. Xác định hệ hình: tỷ lệ, màu, font có glyph phù hợp, thứ bậc chữ, vùng phụ đề, cách dùng hình, ảnh, icon, biểu đồ, footage, demo và âm. Chỉ chọn thứ giúp hiểu hoặc cảm nhận; không dùng motion là lựa chọn hợp lệ, thời gian giữ đủ đọc.

## Tra thư viện và thiết kế từng cảnh

4. Dùng `video-theme-library` tra catalog và chỉ mục motion theo vai trò, tỷ lệ, vùng hiển thị; ghi từ khóa, ID/link, phương án cân nhắc, lý do chọn, quyền và bằng chứng. Phân biệt mẫu chạy được, cần tự dựng, và reference chưa kiểm; link không cấp quyền chép/tải. Nếu không tìm thấy, thiết kế mới, nêu giới hạn và cách kiểm, không bịa mã. Không tự tải hoặc cài nguồn chưa được phép.
5. Với mỗi cảnh điền mẫu: ý cần hiểu; thời gian và cue lời; bố cục/vị trí; hình, icon, chữ, màu; trạng thái **trước → hành động → sau** với đối tượng, thứ tự, thời lượng; âm/nhạc/SFX; cách nối cảnh; hướng dẫn dựng và nguồn asset; điểm kiểm đầu–giữa–cuối, trước/sau cue và tua ngược. Ví dụ quy trình: ô xuất hiện trước, connector dẫn đến ô đó sau; mũi tên của bước tương lai ẩn. Đối chiếu hình và lời, tránh panel trống, callout sai hoặc phụ đề chồng lên phụ đề nguồn.
6. Chuyển hướng dẫn thành đầu việc khả thi cho `video-edit`/EDL hoặc `hyperframes`/composition và `video-studio render` theo routing. Ghi phụ thuộc, giới hạn runtime và cảnh cần thử; không hứa template tin có thể nhận motion tùy biến nếu engine chưa hỗ trợ.

Trước khi duyệt storyboard explainer/vlog có avatar, đọc [chuẩn chuyển động và bố cục](references/motion-layout-standard.md): icon luôn động, hiện theo lời, liên kết chạy liên tục, không chỗ trống, không chữ chạm nhau, không màn đứng yên quá 6 s. Chủ chỉ đưa transcript cho tập chủ đề mới: đọc [sáng tạo icon theo lời thoại](references/creative-icon-brainstorm.md) để brainstorm ẩn dụ, icon có tương tác bên trong và motion liên kết. Rồi theo [storyboard ảnh tĩnh trước](references/storyboard-stills-first.md): chủ duyệt khung tĩnh trước khi dựng motion, bốn điểm dừng, thời lượng máy, bẫy.

Khi yêu cầu ba draft nâng cấp hoặc phản biện sáng tạo, đọc [review sáng tạo](references/creative-review.md): tổ chức các góc nhìn chuyên môn, review toàn bài theo bằng chứng và lập kế hoạch sửa cụ thể từng cảnh trước mỗi lượt; không tự nhận đã có chuyên gia độc lập.

## Giao tiếp và review

Giao file storyboard, tóm tắt ý tưởng, lựa chọn motion, nguồn/quyền, chi phí và điểm cần người dùng quyết. Nếu được giao dựng video đầy đủ, theo [workflow chung](../video-routing/references/video-workflow.md): draft 1 → agent xem/nghe trực tiếp, đề xuất và sửa → draft 2 → xem/nghe, đề xuất sáng tạo phù hợp và sửa → draft 3; kiểm và bàn giao cả ba để người dùng chọn. Pilot ngắn không tính draft. Nếu không thể xem hoặc nghe trực tiếp, ghi rõ chưa kiểm, không tự nhận đã review và báo phần phụ thuộc chưa hoàn thành. Không tự mở thêm vòng sau draft 3 nếu chưa được giao.
