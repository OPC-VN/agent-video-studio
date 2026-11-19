# Quy tắc định tuyến rea-video: đặc trưng cảnh (signals) → chuỗi nguyên thủy (route) → mô hình ứng viên (prefer, theo thứ tự ưu tiên)
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/routing.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

> Quy tắc chỉ tham chiếu nguyên thủy và id mô hình; script kiểm tra sẽ xác minh tính toàn vẹn tham chiếu và việc "mô hình thật sự hỗ trợ nguyên thủy đó".
> Khi chọn mô hình: bỏ qua `status: shutdown`; lọc theo `regions_excluded` và `license`; với điều kiện ngang nhau thì xếp theo chi phí.

Phiên bản: 0.1.0 · Cập nhật: 2026-10-29

## 1. Chế độ

- **fidelity** (phục dựng trung thực): cấu trúc, nhịp, máy quay, chữ, hiệu ứng được đối chiếu từng mục; đo bằng scorecard.
- **adapt** (cải biên sáng tạo): giữ mối quan hệ khiến video gốc "hiệu quả" (móc câu, hé lộ, nhịp), nội dung viết lại theo chủ đề mới.
- Hai chế độ có thể trộn theo lớp, ví dụ `{rhythm: fidelity, camera: fidelity, people: adapt, copy: adapt}`.

## 2. Tín hiệu (signals)

Đặc trưng cảnh cần phát hiện khi phân tích ngược, cùng các nguyên thủy phân tích cung cấp bằng chứng.

| Tín hiệu | Phát hiện bởi | Mô tả |
|---|---|---|
| `text_or_ui_dominant` | analyze.ocr_text_track, analyze.video_understanding | Chữ / UI / biểu đồ / MG là chủ thể khung; cạnh chữ sắc nét, căn theo pixel, quỹ đạo gọn |
| `screen_ui` | analyze.video_understanding, analyze.ocr_text_track | Thao tác demo giao diện phần mềm hoặc web |
| `talking_head_frontal` | analyze.video_understanding, analyze.asr_word_align, analyze.camera_motion | Người nói trực diện, máy gần như cố định |
| `dialogue_coupled` | analyze.asr_word_align, analyze.video_understanding | Lời thoại gắn chặt với hình ảnh trong cảnh không trực diện (hội thoại nhiều người, vừa làm vừa nói) |
| `precise_motion` | analyze.video_understanding, analyze.segmentation, analyze.beat_tempo | Nhảy múa, đổi trang phục, cử chỉ theo nhịp là điểm nhấn của cảnh |
| `garment_change` | analyze.video_understanding | Thay đồ hoặc trưng bày trang phục trong thương mại điện tử |
| `physical_text_zh` | analyze.ocr_text_track | Chữ vật lý trong khung (biển hiệu, bao bì, màn hình), đặc biệt chữ Trung |
| `product_hero` | analyze.video_understanding, analyze.segmentation | Ngoại hình hoặc bố cục sản phẩm phải chính xác |
| `product_multiview` | analyze.video_understanding, analyze.camera_motion | Sản phẩm xoay, trưng bày nhiều góc |
| `complex_camera` | analyze.camera_motion, analyze.shot_boundary | Máy quay phức tạp, chuyển cảnh bằng vật che, biến đổi tức thời |
| `lens_look` | analyze.video_understanding | Cảm giác ống kính nổi bật: tiêu cự, độ sâu trường, méo hình |
| `recurring_character` | analyze.video_understanding, analyze.segmentation | Cùng một nhân vật hoặc sản phẩm xuất hiện ở nhiều cảnh |
| `owned_footage_edit` | (không có) | Tư liệu có sẵn mà người dùng có quyền dùng, chỉ cần thay người, vật, nền |
| `redub_only` | analyze.asr_word_align | Giữ diễn xuất, chỉ đổi lời thoại hoặc ngôn ngữ |
| `ambient_broll` | analyze.video_understanding | Cảnh không khí (B-roll), không có chủ thể cụ thể |
| `reusable_footage` | (không có) | Tư liệu có sẵn của người dùng có thể dùng lại trực tiếp |
| `still_image_motion` | analyze.camera_motion | Cả khung là một ảnh tĩnh được đẩy/kéo/lia/dịch (Ken Burns), đo được tham số thu phóng / dịch chuyển |
| `static_hold` | analyze.shot_boundary | Khung tĩnh đứng yên (ảnh hoặc thẻ dừng lại) |
| `anim_2d` | analyze.video_understanding | Hoạt hình 2D (vẽ tay từng khung, Live2D, nhân vật AE/Spine); công cụ không đo được, phải nhìn ảnh để xác định |
| `stop_motion` | analyze.video_understanding | Stop-motion (chụp từng khung vật thật / đất sét / con rối giấy); công cụ không đo được, phải nhìn ảnh |
| `film_footage` | analyze.video_understanding | Cảnh phim / truyền hình / phim ngắn đã cắt sẵn (video thuyết minh phim, video cắt ghép, tuyển tập cảnh kinh điển); về pixel không tách được với quay thật hoặc AI; công cụ chỉ cho manh mối (viền đen, nguồn 24/25fps), phải nhìn ảnh |
| `ai_edited_footage` | analyze.video_understanding | Cảnh quay thật bị AI xử lý lại (đổi mặt, đối khẩu hình, phong cách hoá, đổi trang phục, đổi nền) |

## 3. Tách cảnh (segmentation)

**Các cấp:**
- `edit_shot`: cảnh dựng, lấy từ phát hiện chuyển cảnh; là sự thật khách quan.
- `generation_unit`: đơn vị sinh, là sản phẩm của một lần gọi mô hình; không khớp 1-1 với cảnh dựng.
- `layer`: phân lớp theo chiều dọc trong cùng một khung (lớp code / lớp sinh / lớp tư liệu / lớp phụ đề).

**Mặc định:**
- `generation_unit_s`: min 4, max 15 (giây)
- `multishot_hardcut_s`: prefer 8, max 10 (giây). Thời lượng các cắt cứng liên tiếp trong một đơn vị sinh (S06)
- `motion_segment_s`: prefer 10, max 15, min 3 (giây). Độ dài mỗi đoạn video dẫn bằng chuyển động: cắt ở chỗ dừng, đoạn ngắn thì tay chân ổn định hơn
- `same_scene_distance`: 0.5. Khoảng cách phân bố màu ở khung đầu và khung cuối của hai cảnh liền kề (Bhattacharyya) nhỏ hơn mức này thì coi là cùng một cảnh

**Quy tắc:**

- **S01-merge-multishot**: Các cảnh liên tiếp cùng nhân vật, cùng bối cảnh; nếu tổng thời lượng không vượt giới hạn trên của mô hình ứng viên thì gộp thành một đơn vị sinh, dùng `video.multi_shot` sinh một lần.
  - Lý do: nhất quán và chuyển cảnh tự nhiên do mô hình xử lý bên trong.
- **S02-split-duration**: Cảnh vượt giới hạn một lần sinh của mô hình ứng viên thì cắt ở chỗ động tác dừng; đoạn sau lấy khung cuối của đoạn trước làm khung đầu (`video.i2v_first_frame` hoặc `i2v_first_last`).
- **S03-split-transition**: Chuyển cảnh bằng vật che, khoảnh khắc thay đồ, điểm biến đổi động tác mạnh thì cắt riêng, kiểm soát chính xác bằng khung đầu–cuối hoặc keyframe.
  - Lý do: ví dụ thay đồ lúc cánh quạt che, lệch thời điểm một chút là lộ.
- **S04-vertical-layers**: Chữ, UI, hình, phụ đề tách thành lớp code; phần hình bên dưới đi qua lớp sinh hoặc lớp tư liệu; cuối cùng ghép lại.
  - Lý do: mô hình sinh vẽ lại chữ chắc chắn sai; lớp code đúng 100% và dễ sửa.
- **S05-end-state**: Prompt của mỗi đơn vị sinh phải nói rõ "quá trình động tác + trạng thái kết thúc"; trạng thái kết thúc là điều kiện nối sang đơn vị tiếp theo.
- **S06-hardcut-guard**: Trong một đơn vị sinh, cắt cứng liên tiếp không quá khoảng 8 giây (kinh nghiệm thực tế; quá khoảng 10 giây thì thường có lỗi).
- **S07-long-video**: Video dài thì chia trước theo đoạn kể chuyện rồi xử lý riêng, sau đó ghép lại; tại chỗ ghép kiểm tra ngoại hình sản phẩm nhất quán, phụ đề khớp điểm bán hàng, động tác nối liền.

## 4. Định tuyến hình ảnh (rules)

**R01-code-graphics** (lớp phủ)
- Khi: `text_or_ui_dominant`
- Route: render.code_graphics
- Ưu tiên: remotion, html-gsap-playwright, motion-canvas
- Kiểm chứng: ocr_text_match, layout_iou, timing_curve_error, pixel_similarity
- Lý do: chữ và hoạt ảnh đòi hỏi chính xác từng pixel và phải dễ sửa; mô hình sinh không làm được.

**R02-screen-demo** (lớp nền)
- Khi: `screen_ui`
- Route: render.web_capture, render.code_graphics
- Ưu tiên: html-gsap-playwright, remotion
- Kiểm chứng: ocr_text_match, layout_iou
- Lý do: dùng giao diện thật hoặc dựng lại để điều khiển quay màn hình, chính xác hơn sinh.

**R03-talking-head** (lớp nền)
- Khi: `talking_head_frontal`
- Route: audio.voice_clone, avatar.audio_driven
- Ưu tiên: minimax-speech-2.8, omnihuman-2.0, kling-avatar-v2, heygen-avatar-v, ltx-2.3-lipsync
- Phương án khác: cảnh ngắn có thể dùng mô hình âm thanh-hình ảnh cùng sinh kèm tham chiếu giọng (R16)
- Kiểm chứng: lip_sync, identity_consistency, speech_wer

**R04-precise-motion** (lớp nền)
- Khi: `precise_motion`
- Route: motion.transfer, video.reference_video, analyze.depth_video, analyze.pose_track, video.control_video, analyze.body_mocap, render.3d_scene
- Ưu tiên: kling-motion-control, seedance-2.5, wan-2.2-animate, wan-animate-2, video-depth-anything, dwpose, wan-vace, rokoko-vision, blender
- Kiểm chứng: motion_trajectory_error, identity_consistency, beat_alignment
- Lý do: thời gian của chuyển động không mô tả được bằng chữ và khung tĩnh; khung đầu–cuối chỉ khoá hai đầu, phần giữa của đoạn nhảy thì mô hình phải tự đoán.
- Phương án khác: nếu ngoại hình hoặc thể hình của diễn viên gốc bị mang sang, đổi sang video độ sâu (đổi người, đổi cảnh, giữ máy quay) hoặc video khung xương (thể hình khác xa) làm tín hiệu dẫn; muốn đổi góc máy hoặc tái dùng bộ động tác này thì motion capture một camera ra mô hình trắng, dựng lại máy trong Blender, render, rồi dùng làm tham chiếu sinh.
- Bảo vệ (guard): xoá phụ đề và sticker khỏi video dẫn (nếu không sẽ bị học như một phần của hình); cắt video dẫn thành đoạn ngắn ở chỗ dừng (tay chân và xoay người ổn định hơn trong đoạn ngắn); dùng video nhảy của người khác cần chú ý quyền hình ảnh và bản quyền.

**R05-garment** (lớp nền)
- Khi: `garment_change`
- Route: image.tryon, video.i2v_first_frame, motion.transfer
- Ưu tiên: fashn-tryon-max, kling-virtual-tryon-3, fashn-v1.6, seedance-2.5, kling-3.0, kling-motion-control
- Kiểm chứng: identity_consistency, perceptual_similarity
- Lý do: ra ảnh thử đồ, xác nhận rồi mới cho chuyển động, ổn định hơn việc để mô hình video thay đồ trực tiếp.

**R06-physical-text-zh** (lớp nền)
- Khi: `physical_text_zh`
- Route: image.text_render, video.i2v_first_frame
- Ưu tiên: gpt-image-2.5, gpt-image-2.6, qwen-image-3.0-pro, seedream-5.5, seedream-5.0, seedance-2.5, kling-3.0
- Kiểm chứng: text_render_accuracy, ocr_text_match
- Bảo vệ: nếu chữ cần rõ ràng ổn định lâu, hoặc máy quay chuyển động mạnh, chuyển sang R01 (chèn chữ bằng code) vì mô hình video sẽ làm méo chữ khi đang chuyển động.

**R07-product-hero** (lớp nền)
- Khi: `product_hero`
- Route: image.edit_multi_ref, video.i2v_first_frame, video.i2v_first_last
- Ưu tiên: gpt-image-2.5, gpt-image-2.6, nano-banana-2.1, seedream-5.5, seedream-5.0, seedance-2.5, kling-3.0, veo-3.1
- Kiểm chứng: identity_consistency, perceptual_similarity
- Lý do: ghép khung đầu từ ảnh sản phẩm rồi xác nhận, khoá ngoại hình xong mới sinh chuyển động.

**R08-product-multiview** (lớp nền)
- Khi: `product_multiview`
- Route: threed.image_to_3d, render.3d_scene, video.reference_video
- Ưu tiên: hunyuan-3d, rodin-gen-2.5, blender, seedance-2.5
- Kiểm chứng: identity_consistency, camera_path_error
- Lý do: mô hình 3D giữ nhất quán nhiều góc; có thể render trực tiếp, cũng có thể đưa render mô hình trắng làm tham chiếu cho Seedance 2.5.

**R09-complex-camera** (lớp nền)
- Khi: `complex_camera`
- Route: video.keyframes, video.i2v_first_last
- Ưu tiên: kling-4.0, kling-3.0, veo-3.1, runway-gen-4.5, minimax-h3
- Kiểm chứng: camera_path_error, cut_alignment
- Bảo vệ: nếu vẫn không kiểm soát được, cắt tại điểm bị che khuất (xem S03).

**R10-lens-look** (lớp nền)
- Khi: `lens_look`
- Route: video.camera_control
- Ưu tiên: pixverse-v6, kling-4.0, runway-gen-4.5, gemini-omni-flash
- Kiểm chứng: perceptual_similarity

**R11-recurring-character** (lớp nền)
- Khi: `recurring_character`
- Route: video.multi_reference, video.multi_shot
- Ưu tiên: seedance-2.5, kling-3.0, kling-o3, vidu-q3, kling-4.0
- Kiểm chứng: identity_consistency, cut_alignment

**R12-owned-footage-edit** (lớp nền)
- Khi: `owned_footage_edit`
- Route: video.edit_v2v
- Ưu tiên: kling-o3, kling-4.0, runway-aleph-2, luma-ray3.2, wan-2.2-animate, seedance-2.5
- Kiểm chứng: motion_trajectory_error, identity_consistency

**R13-redub** (lớp nền)
- Khi: `redub_only`
- Route: lipsync.redub
- Ưu tiên: sync-3, sync-react-1
- Kiểm chứng: lip_sync, speech_wer

**R14-ambient-broll** (lớp nền)
- Khi: `ambient_broll`
- Route: video.t2v
- Ưu tiên: minimax-h3, hailuo-2.3, seedance-2.0, wan-2.2, seedance-2.5
- Kiểm chứng: perceptual_similarity
- Lý do: đường rẻ nhất, xếp theo chi phí.

**R15-reuse-footage** (lớp nền)
- Khi: `reusable_footage`
- Route: render.compose
- Ưu tiên: ffmpeg
- Kiểm chứng: cut_alignment

**R17-still-motion** (lớp nền)
- Khi: `still_image_motion`
- Route: image.edit_multi_ref, render.compose
- Ưu tiên: gpt-image-2.5, seedream-5.0, ffmpeg
- Kiểm chứng: camera_path_error, perceptual_similarity
- Lý do: bước phân tích đã đo được đường cong thu phóng / dịch chuyển, dùng một ảnh cùng ffmpeg cục bộ là phục dựng chính xác chuyển động, không cần mô hình video.

**R18-static-hold** (lớp nền)
- Khi: `static_hold`
- Route: image.edit_multi_ref, render.compose
- Ưu tiên: gpt-image-2.5, seedream-5.0, ffmpeg
- Kiểm chứng: perceptual_similarity

**R19-2d-animation** (lớp nền)
- Khi: `anim_2d`
- Route: image.t2i, video.i2v_first_last, video.multi_reference
- Ưu tiên: kling-3.0, seedance-2.5, vidu-q3
- Kiểm chứng: identity_consistency, perceptual_similarity
- Lý do: dùng mô hình ảnh để chốt nhân vật và phong cách (một ảnh thiết lập), rồi sinh từ khung đầu–cuối; khi cần khẩu hình và động tác chính xác từng khung thì chuyển sang dự án AE / Live2D / Spine.

**R20-stop-motion** (lớp nền)
- Khi: `stop_motion`
- Route: video.i2v_first_frame
- Ưu tiên: kling-3.0, seedance-2.5, vidu-q3
- Kiểm chứng: perceptual_similarity
- Lý do: tốt nhất là quay thật: điện thoại cố định + app chụp stop-motion 12 khung mỗi giây; AI chỉ giả được cảm giác giật cục gần đúng; prompt ghi rõ stop-motion, 12fps.

**R21-film-footage** (lớp nền)
- Khi: `film_footage`
- Route: render.compose
- Ưu tiên: ffmpeg
- Kiểm chứng: perceptual_similarity
- Lý do: hình đến từ tác phẩm điện ảnh có sẵn; phục dựng là tìm đúng đoạn tương ứng trong bản gốc rồi cắt lại (bản quyền thuộc về hãng phim, dùng thương mại phải có giấy phép). Không dùng bản gốc thì quay lại theo cùng cỡ cảnh, góc máy, ánh sáng, hoặc dùng AI xấp xỉ (R07).

**R16-dialogue-coupled** (lớp nền)
- Khi: `dialogue_coupled`
- Route: video.native_audio, video.multi_reference
- Ưu tiên: seedance-2.5, kling-3.0, veo-3.1, gemini-omni-flash, kling-4.0
- Kiểm chứng: lip_sync, speech_wer, identity_consistency

> Ghi chú của bản dịch: trong file gốc, phần mô tả R01–R16 nhưng thực tế có thêm R17–R21 (đã giữ nguyên như gốc).

## 5. Định tuyến âm thanh (audio_rules)

**A01-narration**
- Khi: có lời thuyết minh hoặc nói trước camera
- Route: analyze.asr_word_align, audio.voice_clone, audio.tts
- Ưu tiên: funasr-sensevoice, whisperx, minimax-speech-2.8, cosyvoice-3, qwen3-tts, elevenlabs-v3
- Kiểm chứng: speech_wer
- Ghi chú: tiếng Trung ưu tiên nhân bản giọng MiniMax; tiếng Anh cần cảm xúc thì ưu tiên ElevenLabs.

**A02-fit-time-window**
- Khi: lời mới phải nhét vừa khung thời gian gốc (khớp khẩu hình, khớp hình)
- Route: audio.tts_duration_control
- Ưu tiên: indextts-2
- Kiểm chứng: audio_duration_match, speech_wer

**A03-music**
- Khi: có nhạc nền
- Route: analyze.audio_separation, analyze.beat_tempo, audio.music_gen
- Ưu tiên: demucs, librosa-madmom, lyria-3-pro, minimax-music-2.5
- Kiểm chứng: beat_alignment
- Ghi chú: không mang nguyên bản nhạc sang; sinh nhạc mới có BPM và cảm xúc gần đúng, hoặc dùng thư viện nhạc đã cấp phép. Suno không có API, chỉ phù hợp thao tác thủ công.

**A04-sfx**
- Khi: có hiệu ứng động tác hoặc âm thanh môi trường
- Route: audio.v2a_foley, audio.sfx_gen
- Ưu tiên: hunyuanvideo-foley, elevenlabs-sfx
- Kiểm chứng: beat_alignment
- Ghi chú: giấy phép của HunyuanVideo-Foley loại trừ EU, Anh, Hàn Quốc; trọng số của MMAudio không được dùng thương mại.

**A05-lip-mismatch**
- Khi: khẩu hình của hình đã sinh không khớp với âm thanh mới
- Route: lipsync.redub
- Ưu tiên: sync-3, sync-react-1
- Kiểm chứng: lip_sync

## 6. Hậu kỳ (post_rules)

**P01-upscale**
- Khi: độ phân giải bản nháp thấp hơn độ phân giải giao hàng
- Route: post.upscale
- Ưu tiên: seedvr2, flashvsr, topaz-video
- Ghi chú: không khuyến nghị Real-ESRGAN cho video sinh ra (có artifact dạng ô vuông).

**P02-interp**
- Khi: tốc độ khung hình không đủ hoặc cần slow motion
- Route: post.frame_interp
- Ưu tiên: rife, topaz-video

## 7. Chi phí và nút xác nhận

**Chính sách chi phí (cost_policy):**
- Mỗi đơn vị sinh phải ước tính chi phí trước (thời lượng × usd_per_s), cộng tổng rồi để người dùng xác nhận ngân sách ở G1.
- Ra keyframe hoặc ảnh thử đồ trước (rẻ), xác nhận rồi mới sinh video (đắt).
- Ra bản nháp 480p hoặc 720p trước, xác nhận rồi mới siêu phân giải lên độ phân giải giao hàng (thực tế giảm chi phí đáng kể).
- Nhiều cảnh của cùng một nhân vật ưu tiên gộp thành một lần sinh nhiều cảnh (S01).
- Các đơn vị sinh đã có được cache theo (hash đầu vào + mô hình + tham số); khi sửa chỉ chạy lại các đơn vị bị ảnh hưởng.

**Nút xác nhận (confirm_gates):**
- G1: yêu cầu, chế độ (fidelity / adapt), ngân sách và tài khoản
- G2: bảng phân cảnh + ảnh keyframe / ảnh thử đồ / khung đầu
- G3: bản nháp thành phẩm độ phân giải thấp
- G4: thành phẩm đã siêu phân giải và scorecard

## 8. Kỷ luật prompt (prompting_rules)

Quy tắc chung; cách viết cụ thể của từng mô hình nằm ở prompting.yaml, nếu hai bên không khớp thì lấy bên prompting.yaml.

- Chỉ viết nội dung muốn có; không viết câu phủ định (viết "no phone" lại vẽ ra điện thoại).
- Viết rõ "quá trình động tác + trạng thái kết thúc".
- Mỗi đầu vào phải ghi rõ vai trò: tham chiếu nhận dạng, sự thật về sản phẩm, tham chiếu động tác hoặc máy quay, tham chiếu giọng, lời thoại.
- Tránh ngôn từ ẩn dụ; mô hình sẽ vẽ ẩn dụ thành vật thể hoặc sự kiện theo nghĩa đen.
- Số lượng chính xác (ví dụ số ngón tay) giao cho phụ đề hoặc MG, đừng để mô hình diễn.
- Diễn xuất thì cho một thái độ có thể thực hiện, đừng liệt kê động tác.
