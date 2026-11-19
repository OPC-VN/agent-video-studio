# Nguyên thủy rea-video (primitives)
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/primitives.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

> Nguyên thủy = một năng lực không phụ thuộc nhà cung cấp. Mục mô hình khai báo qua trường `primitives` các nguyên thủy mà mình hỗ trợ; quy tắc định tuyến (routing.yaml) chỉ tham chiếu nguyên thủy, rồi từ nguyên thủy tìm ra mô hình ứng viên.
> Mỗi nguyên thủy khai báo: đầu vào, đầu ra, lúc nào dùng, dùng chỉ số nào để kiểm chứng (metrics), và probe kiểm tra điều gì.

Phiên bản: 0.1.0 · Cập nhật: 2026-10-29

## Chỉ số kiểm chứng (metrics)

| Khoá | Tên | Mô tả |
|---|---|---|
| `cut_alignment` | Căn điểm cắt | Sai số khung giữa điểm cắt của đoạn phục dựng và điểm cắt gốc / F1 (dung sai ±1 khung) |
| `shot_count_match` | Khớp số cảnh | Mức độ nhất quán về số lượng cảnh và phân bố thời lượng |
| `ocr_text_match` | Khớp chữ | Tỷ lệ khớp ở mức ký tự (CER) giữa văn bản OCR nhận được và văn bản mục tiêu |
| `layout_iou` | IoU bố cục | IoU giữa khung bao chữ/phần tử và bố cục mục tiêu (theo từng khung) |
| `timing_curve_error` | Sai số đường cong hoạt ảnh | Sai số giữa đường cong vị trí/tỷ lệ/độ trong suốt theo thời gian của phần tử và tham chiếu |
| `pixel_similarity` | Độ tương đồng pixel | SSIM / LPIPS; chỉ dùng cho khung hình có thể phục dựng chính xác, như lớp code |
| `perceptual_similarity` | Độ tương đồng cảm nhận | Độ tương đồng DreamSim / CLIP; dùng cho lớp sinh |
| `identity_consistency` | Nhất quán chủ thể | Nhúng khuôn mặt/sản phẩm/nhân vật nhất quán trong một cảnh và giữa các cảnh |
| `motion_trajectory_error` | Sai số quỹ đạo chuyển động | Sai số quỹ đạo điểm khoá/tư thế so với chuyển động tham chiếu |
| `camera_path_error` | Sai số máy quay | Chênh lệch giữa quỹ đạo máy quay ước lượng và chuyển động máy quay tham chiếu |
| `beat_alignment` | Căn nhịp | Sai số giữa điểm cắt/sự kiện hoạt ảnh và nhịp nhạc |
| `lip_sync` | Đồng bộ khẩu hình | Điểm kiểu SyncNet (LSE) |
| `audio_duration_match` | Khớp thời lượng âm thanh | Sai số thời lượng giọng nói sinh ra so với khung thời gian mục tiêu |
| `speech_wer` | Độ rõ lời nói | Tỷ lệ lỗi từ (WER) sau khi nhận dạng giọng nói đầu ra so với kịch bản |
| `text_render_accuracy` | Độ chính xác chữ trong khung | Tỷ lệ đúng của chữ trong ảnh/video sinh ra (đặc biệt chữ Trung) |
| `human_ab` | Thử A/B người thật | Thử mù về độ ưa thích: giống, đẹp, hoặc có thể đưa ra quảng cáo |

## Nguyên thủy

### Nhóm analyze (phân tích ngược)

**`analyze.video_understanding`**: Hiểu ngữ nghĩa video
- Đầu vào: video, audio, text · Đầu ra: structured_text
- Dùng khi: hiểu ý đồ cảnh, diễn xuất, phong cách, cấu trúc kể chuyện; sinh bản nháp mô tả và prompt
- Probe: trên tập cảnh có gán nhãn tay, đo độ chính xác mô tả cảnh, sai số định vị thời gian, tỷ lệ trả lời đúng câu hỏi đếm

**`analyze.shot_boundary`**: Phát hiện chuyển cảnh
- Đầu vào: video · Đầu ra: timestamps
- Dùng khi: bước đầu tiên của mọi video
- Chỉ số: cut_alignment
- Probe: F1 điểm cắt trên mẫu lẫn cắt cứng, chuyển cảnh mờ dần và chuyển cảnh bằng vật che

**`analyze.asr_word_align`**: Nhận dạng giọng nói + căn chỉnh theo từ
- Đầu vào: audio · Đầu ra: transcript_with_word_times
- Dùng khi: video có giọng người; cung cấp mốc từ cho phụ đề, lời thuyết minh, và khớp nhịp
- Probe: CER và sai số ranh giới từ trên mẫu trộn Trung–Anh và mẫu phương ngữ

**`analyze.ocr_text_track`**: Nhận dạng chữ trên khung hình và quỹ đạo
- Đầu vào: video · Đầu ra: text_tracks
- Dùng khi: nhận dạng phụ đề, tiêu đề, chữ UI và thời điểm chữ xuất hiện / biến mất / di chuyển, để dựng lại bằng code
- Probe: tỷ lệ nhận dạng và độ chính xác khung của chữ chuyển động, chữ có viền, chữ tiếng Trung trên nền phức tạp

**`analyze.segmentation`**: Phân đoạn và theo dõi
- Đầu vào: video, text · Đầu ra: masks
- Dùng khi: tách chủ thể / sản phẩm / nền, đo quỹ đạo phần tử

**`analyze.matting`**: Tách nền video (alpha)
- Đầu vào: video · Đầu ra: video_with_alpha
- Dùng khi: cần tiền cảnh trong suốt (đặt người lên nền mới, chữ chèn sau người)

**`analyze.camera_motion`**: Giải mã chuyển động máy quay
- Đầu vào: video · Đầu ra: camera_trajectory
- Dùng khi: xác định đẩy/kéo/lia/dịch, cảm giác cầm tay, máy quay 3D; làm cơ sở cho việc sinh máy quay hoặc render 3D

**`analyze.audio_separation`**: Tách âm thanh theo track
- Đầu vào: audio · Đầu ra: stems
- Dùng khi: tách giọng người / nhạc nền / hiệu ứng để phân tích và thay thế riêng

**`analyze.beat_tempo`**: Phân tích nhịp và đoạn nhạc
- Đầu vào: audio · Đầu ra: beat_grid
- Dùng khi: video cắt theo nhạc; cung cấp mốc nhịp cho nhịp cắt

**`analyze.depth_video`**: Ước lượng độ sâu video
- Đầu vào: video · Đầu ra: video
- Dùng khi: phục dựng cảnh nhảy, đánh nhau: chuyển video gốc thành video độ sâu thang xám làm tín hiệu dẫn; giữ được động tác, vị trí, không gian và máy quay, bỏ đi hình dáng và trang phục của người gốc
- Chỉ số: motion_trajectory_error
- Probe: nhấp nháy từng khung và thiếu chi trong các đoạn xoay người nhanh, tay đan nhau, nhiều người che khuất nhau

**`analyze.pose_track`**: Theo dõi khung xương người
- Đầu vào: video · Đầu ra: keypoints
- Dùng khi: khi thể hình nhân vật đích khác xa diễn viên gốc (chibi, động vật, hoạt hình), dùng khung xương thay vì độ sâu làm tín hiệu dẫn, để thể hình không bị kéo sang
- Chỉ số: motion_trajectory_error

**`analyze.body_mocap`**: Motion capture từ video một camera
- Đầu vào: video · Đầu ra: animation
- Dùng khi: cần đổi góc máy, tái sử dụng hoặc chỉnh trong 3D; chuyển động gốc thành FBX / BVH, gắn lên mô hình trắng (white model) rồi render lại
- Chỉ số: motion_trajectory_error

**`analyze.image_layer_decompose`**: Phân rã lớp của một khung hình
- Đầu vào: image · Đầu ra: layered_images
- Dùng khi: tách một khung thành nền + các lớp phần tử trong suốt, để hiểu hoặc thay bố cục

### Nhóm image (hình ảnh)

**`image.t2i`**: Văn bản sang ảnh
- Đầu vào: text · Đầu ra: image
- Dùng khi: sinh keyframe, thiết lập nhân vật, ảnh tĩnh B-roll
- Chỉ số: perceptual_similarity

**`image.edit_multi_ref`**: Chỉnh sửa/ghép ảnh nhiều tham chiếu
- Đầu vào: image, text · Đầu ra: image
- Dùng khi: ghép tham chiếu sản phẩm / người / cảnh thành khung đầu; thay đồ, thay vật; giữ nhất quán chủ thể
- Chỉ số: identity_consistency, perceptual_similarity
- Probe: độ nhất quán ngoại hình của cùng một sản phẩm trong 5 cảnh

**`image.text_render`**: Vẽ chữ trong khung hình
- Đầu vào: text, image · Đầu ra: image
- Dùng khi: trong khung có biển hiệu, bao bì, poster và các chữ vật lý khác (đặc biệt chữ Trung)
- Chỉ số: text_render_accuracy
- Probe: tỷ lệ đúng trên 20 cụm từ tiếng Trung (gồm chữ hiếm, dọc, trộn lẫn)

**`image.storyboard_series`**: Bộ ảnh phân cảnh
- Đầu vào: text, image · Đầu ra: images
- Dùng khi: sinh một lần nhiều ảnh keyframe phân cảnh có phong cách nhất quán để xác nhận

**`image.tryon`**: Thử đồ ảo
- Đầu vào: image · Đầu ra: image
- Dùng khi: thay đồ cho thương mại điện tử: ảnh người + ảnh trang phục → ảnh mặc đồ, rồi đưa vào sinh video từ ảnh
- Chỉ số: identity_consistency

### Nhóm video (sinh và chỉnh sửa)

**`video.t2v`**: Văn bản sang video
- Đầu vào: text · Đầu ra: video
- Dùng khi: cảnh không khí, B-roll không có chủ thể cụ thể
- Chỉ số: perceptual_similarity

**`video.i2v_first_frame`**: Ảnh sang video (khung đầu)
- Đầu vào: image, text · Đầu ra: video
- Dùng khi: bố cục / sản phẩm / người phải chính xác; định khung đầu trước rồi mới cho chuyển động
- Chỉ số: perceptual_similarity, identity_consistency

**`video.i2v_first_last`**: Sinh từ khung đầu và khung cuối
- Đầu vào: image, image, text · Đầu ra: video
- Dùng khi: cảnh đã xác định trạng thái đầu và cuối; biến đổi trang phục / chuyển cảnh; nối với khung cuối của đoạn trước
- Chỉ số: perceptual_similarity, identity_consistency

**`video.keyframes`**: Điều khiển nhiều keyframe
- Đầu vào: images, text · Đầu ra: video
- Dùng khi: máy quay phức tạp hoặc nhiều trạng thái trung gian phải đúng
- Chỉ số: perceptual_similarity, camera_path_error

**`video.multi_reference`**: Sinh video từ nhiều tham chiếu (giữ nhất quán chủ thể)
- Đầu vào: images, text · Đầu ra: video
- Dùng khi: cùng một nhân vật / sản phẩm nhất quán qua nhiều cảnh; nhiều chủ thể cùng khung
- Chỉ số: identity_consistency
- Probe: tỷ lệ giữ được nhận dạng của 3 nhân vật tham chiếu × 4 cảnh

**`video.reference_video`**: Sinh video từ video tham chiếu (chuyển động / máy quay / hiệu ứng)
- Đầu vào: video, images, text · Đầu ra: video
- Dùng khi: hành vi theo thời gian của cảnh gốc (nhịp chuyển động, máy quay, tiến hoá hiệu ứng) không thể mô tả bằng chữ và khung tĩnh
- Chỉ số: motion_trajectory_error, camera_path_error

**`video.reference_audio`**: Sinh video từ âm thanh tham chiếu
- Đầu vào: audio, images, text · Đầu ra: video
- Dùng khi: để hình ảnh bám theo âm thanh cho trước (nhịp nhạc, giọng nói chỉ định)
- Chỉ số: beat_alignment

**`video.multi_shot`**: Nhiều cảnh trong một lần sinh
- Đầu vào: text, images · Đầu ra: video
- Dùng khi: nhiều cảnh liên tiếp cùng nhân vật và bối cảnh; sinh một lần để có nhất quán và chuyển cảnh tự nhiên
- Chỉ số: cut_alignment, identity_consistency

**`video.extend`**: Nối dài (extend)
- Đầu vào: video, text · Đầu ra: video
- Dùng khi: cảnh liên tiếp vượt giới hạn thời lượng của một lần sinh

**`video.edit_v2v`**: Chỉnh sửa video (giữ chuyển động)
- Đầu vào: video, images, text · Đầu ra: video
- Dùng khi: trên video có sẵn thay người / vật, thay phong cách / nền, chỉnh lại ánh sáng; giữ nguyên chuyển động và thứ tự thời gian
- Chỉ số: motion_trajectory_error, identity_consistency

**`video.camera_control`**: Điều khiển máy quay và tham số ống kính
- Đầu vào: text, image, video · Đầu ra: video
- Dùng khi: cần chỉ định đẩy/kéo/lia/dịch, tiêu cự, độ sâu trường ảnh, hoặc đổi vị trí máy của cảnh có sẵn
- Chỉ số: camera_path_error

**`video.native_audio`**: Âm thanh và hình ảnh cùng sinh
- Đầu vào: text, images, audio · Đầu ra: video_with_audio
- Dùng khi: cảnh có lời thoại / âm thanh môi trường gắn chặt với hình ảnh
- Chỉ số: lip_sync, speech_wer

### Nhóm video điều khiển bởi nhân vật

**`video.control_video`**: Sinh theo video điều khiển
- Đầu vào: video, image, text · Đầu ra: video
- Dùng khi: khoá chuyển động và cấu trúc theo từng khung bằng video độ sâu, khung xương hoặc phác thảo; ảnh tham chiếu cho ngoại hình nhân vật (quy trình mã nguồn mở chạy cục bộ cho nhảy múa, đánh nhau)
- Chỉ số: motion_trajectory_error, identity_consistency

**`motion.transfer`**: Chuyển động
- Đầu vào: video, image · Đầu ra: video
- Dùng khi: nhảy múa, thay trang phục, cử chỉ riêng, động tác đúng nhịp cần tái hiện chính xác trên nhân vật mới
- Chỉ số: motion_trajectory_error, identity_consistency

**`avatar.audio_driven`**: Người ảo điều khiển bằng âm thanh
- Đầu vào: image, audio, text · Đầu ra: video
- Dùng khi: nói trực diện, giảng giải dài
- Chỉ số: lip_sync, identity_consistency

**`lipsync.redub`**: Dub lại khẩu hình
- Đầu vào: video, audio · Đầu ra: video
- Dùng khi: diễn xuất có sẵn cần đổi lời thoại / ngôn ngữ, chỉ đổi khẩu hình
- Chỉ số: lip_sync

### Nhóm 3D

**`threed.image_to_3d`**: Ảnh sang 3D
- Đầu vào: images · Đầu ra: mesh
- Dùng khi: sản phẩm cần nhất quán nhiều góc, trưng bày trên bàn xoay, hoặc làm tham chiếu mô hình trắng cho mô hình video
- Chỉ số: identity_consistency

### Nhóm audio (âm thanh)

**`audio.tts`**: Tổng hợp giọng nói
- Đầu vào: text · Đầu ra: audio
- Chỉ số: speech_wer

**`audio.voice_clone`**: Nhân bản giọng
- Đầu vào: audio, text · Đầu ra: audio
- Dùng khi: dùng giọng của chính mình / giọng đã được cấp phép để dẫn hoặc lời nói
- Chỉ số: speech_wer

**`audio.tts_duration_control`**: Lồng tiếng kiểm soát thời lượng
- Đầu vào: text, audio · Đầu ra: audio
- Dùng khi: lời mới phải nhét vừa khung thời gian gốc (khớp khẩu hình, khớp hình)
- Chỉ số: audio_duration_match, speech_wer

**`audio.music_gen`**: Sinh nhạc
- Đầu vào: text, audio · Đầu ra: audio
- Dùng khi: cần nhạc mới có BPM / cảm xúc / cấu trúc gần với gốc nhưng được phép thương mại
- Chỉ số: beat_alignment

**`audio.sfx_gen`**: Văn bản sang hiệu ứng âm
- Đầu vào: text · Đầu ra: audio

**`audio.v2a_foley`**: Sinh hiệu ứng âm từ video (Foley)
- Đầu vào: video, text · Đầu ra: audio
- Dùng khi: tự động thêm hiệu ứng âm thanh đồng bộ với chuyển động cho hình được sinh

### Nhóm render (code)

**`render.code_graphics`**: Hoạt ảnh render bằng code
- Đầu vào: code, data · Đầu ra: video_with_alpha
- Dùng khi: chữ, UI, biểu đồ, MG, phụ đề, cần chính xác 100% và dễ sửa
- Chỉ số: ocr_text_match, layout_iou, timing_curve_error, pixel_similarity

**`render.web_capture`**: Quay màn hình web/giao diện
- Đầu vào: url, script · Đầu ra: video
- Dùng khi: demo giao diện sản phẩm: điều khiển trực tiếp màn hình thật hoặc giao diện dựng lại để quay

**`render.3d_scene`**: Render cảnh 3D
- Đầu vào: mesh, camera_trajectory · Đầu ra: video
- Dùng khi: sản phẩm trên bàn xoay, máy quay chính xác, tham chiếu mô hình trắng

**`render.compose`**: Ghép và mã hoá
- Đầu vào: video, audio, video_with_alpha · Đầu ra: video
- Dùng khi: chồng nhiều lớp, chuyển cảnh, trộn âm thanh, mã hoá cuối cùng

### Nhóm post (hậu kỳ)

**`post.upscale`**: Siêu phân giải video
- Đầu vào: video · Đầu ra: video
- Dùng khi: bản nháp độ phân giải thấp (ví dụ 480p) đã duyệt, cần phóng lên 1080p/4K

**`post.frame_interp`**: Nội suy khung hình
- Đầu vào: video · Đầu ra: video
- Dùng khi: tốc độ khung hình không đủ hoặc cần slow motion
