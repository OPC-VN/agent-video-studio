# Phân tích (lật phim): VLM lo ngữ nghĩa, công cụ tất định lo thời gian và vị trí chính xác
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/models/analysis.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

**Nguyên tắc (từ đầu file nguồn):** VLM không giỏi độ chính xác từng khung hình và việc đếm (video-replicate-studio đã thử cho VLM đếm ngón tay: 14 ảnh chỉ đếm đúng 7). Vì vậy mọi phép đo chính xác giao cho công cụ tất định; VLM chỉ làm phần giải thích và bản nháp prompt.

Tổng số mục: 20 mô hình/công cụ, chia hai nhóm: VLM (5) và công cụ tất định (15).

---

## Nhóm A — VLM (phân tích ngữ nghĩa)

### A1. `gemini-3.1-pro` — Gemini 3.1 Pro
- **Nhà cung cấp / loại:** Google · analysis · `ga`
- **Truy cập:** api, app
- **Năng lực:** `analyze.video_understanding`
- **Giới hạn:** thời lượng tối đa 10800 giây (3 giờ)
- **Điểm mạnh:** đứng đầu về hiểu video tổng hợp; hiểu được video dài tới 3 giờ; hiểu âm thanh và hình ảnh cùng lúc.
- **Điểm yếu:** mã đóng; độ chính xác mốc thời gian chưa công bố, cần hiệu chuẩn bằng công cụ tất định.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://usefulai.com/models/video-understanding
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### A2. `gemini-3.5-flash` — Gemini 3.5 Flash
- **Loại:** analysis · `ga`
- **Truy cập:** api, app
- **Năng lực:** `analyze.video_understanding`
- **Giới hạn:** thời lượng tối đa 10800 giây
- **Điểm mạnh:** nhanh và rẻ hơn, phù hợp để lật phim hàng loạt ở bước sàng lọc.
- **Điểm yếu:** suy luận thời gian khó kém hơn 3.1 Pro.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://usefulai.com/models/video-understanding
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### A3. `doubao-seed-2.0-pro` — Doubao Seed 2.0 Pro (Đậu Bao)
- **Loại:** analysis · `ga`
- **Truy cập:** api
- **Năng lực:** `analyze.video_understanding`
- **Điểm mạnh:** phân tích âm thanh-hình ảnh; điểm tổng hợp gần Gemini nhưng giá thấp hơn; gọi trực tiếp được trong nước, phù hợp nội dung tiếng Trung.
- **Điểm yếu:** thời lượng tối đa chưa công bố.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://usefulai.com/models/video-understanding
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### A4. `pegasus-1.5` — Twelve Labs Pegasus 1.5
- **Loại:** analysis · `ga`
- **Truy cập:** api
- **Năng lực:** `analyze.video_understanding`
- **Giới hạn:** thời lượng tối đa 7200 giây (2 giờ)
- **Điểm mạnh:** trả trực tiếp tóm tắt, chương và JSON có cấu trúc kèm mốc thời gian.
- **Điểm yếu:** hỏi đáp mở về nội dung còn yếu.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://usefulai.com/models/video-understanding
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### A5. `qwen3.5-397b-a17b` — Qwen3.5 397B-A17B (mã nguồn mở)
- **Loại:** analysis · `ga`
- **Truy cập:** open-weights
- **Năng lực:** `analyze.video_understanding`
- **Điểm mạnh:** điểm hiểu video cao nhất trong nhóm trọng số mở; có thể triển khai riêng.
- **Điểm yếu:** cần máy chủ cấp cao; âm thanh phải xử lý riêng.
- **Giấy phép:** commercial: conditional — theo giấy phép của mô hình.
- **Nguồn:** https://usefulai.com/models/video-understanding
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

---

## Nhóm B — Công cụ tất định (đo chính xác)

### B1. `pyscenedetect` — PySceneDetect
- **Loại:** analysis · `ga` · mã nguồn mở
- **Năng lực:** `analyze.shot_boundary`
- **Điểm mạnh:** nhẹ; phát hiện theo nội dung hoặc theo ngưỡng đều cho ra điểm cắt cứng nhanh.
- **Điểm yếu:** dễ bỏ sót chuyển cảnh hòa tan và che khuất; điểm cắt bị bỏ sót được định vị về đúng khung bằng SSIM nhị phân.
- **Giấy phép:** cho phép thương mại (BSD-3-Clause).
- **Nguồn:** https://github.com/Breakthrough/PySceneDetect
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### B2. `transnetv2` — TransNetV2
- **Loại:** analysis · `ga` · mã nguồn mở
- **Năng lực:** `analyze.shot_boundary`
- **Điểm mạnh:** phát hiện cắt cảnh bằng học máy; với chuyển cảnh mờ dần ổn định hơn phương pháp ngưỡng.
- **Giấy phép:** cho phép thương mại (MIT).
- **Nguồn:** https://github.com/soCzech/TransNetV2
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### B3. `whisperx` — WhisperX
- **Loại:** analysis · `ga` · mã nguồn mở
- **Năng lực:** `analyze.asr_word_align`
- **Điểm mạnh:** căn thời gian theo từng từ; Hypit dùng làm nền cho thời gian ngữ nghĩa.
- **Điểm yếu:** dễ nhận sai từ mới tự tạo và tên riêng lạ; tiếng Trung cần chuẩn bị tài nguyên căn chỉnh riêng.
- **Giấy phép:** cho phép thương mại (BSD-2-Clause).
- **Nguồn:** https://github.com/m-bain/whisperX
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### B4. `funasr-sensevoice` — FunASR / SenseVoice
- **Loại:** analysis · `ga` · mã nguồn mở (Alibaba)
- **Năng lực:** `analyze.asr_word_align`
- **Điểm mạnh:** nhận dạng và mốc thời gian tiếng Trung mạnh; SenseVoice xuất đồng thời nhãn cảm xúc và nhãn sự kiện âm thanh.
- **Giấy phép:** commercial: conditional — theo giấy phép mô hình.
- **Nguồn:**
  - https://github.com/modelscope/FunASR
  - https://github.com/FunAudioLLM/SenseVoice
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** medium

### B5. `paddleocr` — PaddleOCR
- **Loại:** analysis · `ga` · mã nguồn mở (Baidu)
- **Năng lực:** `analyze.ocr_text_track`
- **Điểm mạnh:**
  - OCR tiếng Trung mạnh, đồng thời cho khung chữ.
  - Nhận dạng từng khung rồi liên kết theo IoU, cho ra quỹ đạo chữ (xuất hiện, di chuyển, biến mất).
- **Giấy phép:** cho phép thương mại (Apache 2.0).
- **Nguồn:** https://github.com/PaddlePaddle/PaddleOCR
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### B6. `sam-video` — SAM (SAM 2 / SAM 3)
- **Loại:** analysis · `ga` · mã nguồn mở (Meta)
- **Năng lực:** `analyze.segmentation`
- **Điểm mạnh:** phân đoạn và theo dõi đối tượng trong video; SAM 3 hỗ trợ prompt bằng văn bản.
- **Giấy phép:** commercial: conditional — theo giấy phép từng phiên bản.
- **Nguồn:** https://github.com/facebookresearch/sam2
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** medium

### B7. `matanyone-2` — MatAnyone 2
- **Loại:** analysis · `ga` · học thuật mã nguồn mở
- **Năng lực:** `analyze.matting`
- **Điểm mạnh:** tách nền video ổn định nhờ lan truyền bộ nhớ, viền tóc tốt; có node cho ComfyUI.
- **Giấy phép:** commercial: conditional — theo giấy phép kho mã.
- **Nguồn:** https://studio.aifilms.ai/blog/matanyone-2-video-matting
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### B8. `robust-video-matting` — RobustVideoMatting (RVM)
- **Loại:** analysis · `ga` · mã nguồn mở
- **Năng lực:** `analyze.matting`
- **Điểm mạnh:** tách nền chân dung nhẹ, chạy thời gian thực; video-replicate-studio đang dùng.
- **Giấy phép:** commercial: conditional — GPL-3.0, cần lưu ý khi tích hợp với sản phẩm đóng.
- **Nguồn:** https://github.com/PeterL1n/RobustVideoMatting
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** medium

### B9. `volcengine-matting` — Tách nền chân dung video Volcano Engine
- **Loại:** analysis · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `analyze.matting`
- **Điểm mạnh:** API lưu trữ, xuất WEBM/MOV có kênh alpha; Hypit đã tích hợp.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://github.com/hypit-ai/hypit/blob/main/packages/provider-hypihub/README.md
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### B10. `video-depth-anything` — Video Depth Anything
- **Loại:** analysis · phát hành 2025-01 · `ga` · mã nguồn mở (ByteDance)
- **Năng lực:** `analyze.depth_video`
- **Điểm mạnh:**
  - Ước lượng độ sâu video dài, ổn định giữa các khung, không nhấp nháy như độ sâu từng khung.
  - Ba cấp Small / Base / Large; Small chạy được trên card tiêu dùng.
- **Điểm yếu:** khi xoay người nhanh, tay đan chéo và che khuất vẫn có thể thiếu chi tiết cơ thể; phải xem toàn bộ đoạn trước khi dùng làm video điều khiển.
- **Giấy phép:** commercial: conditional — Small là Apache 2.0; Base / Large là CC BY-NC 4.0, không dùng thương mại.
- **Nguồn:**
  - https://github.com/DepthAnything/Video-Depth-Anything
  - https://aiidelist.com/blog/remake-viral-video-codex-depth-maps-minimax-h3
- **Xác minh:** 2026-11-14 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** cách sao chép bằng độ sâu theo quy trình của aiidelist: đổi video gốc sang video độ sâu thang xám, rồi đưa cùng ảnh thiết kế nhân vật vào mô hình video.

### B11. `dwpose` — DWPose
- **Loại:** analysis · phát hành 2023-07 · `ga` · mã nguồn mở (IDEA Research)
- **Năng lực:** `analyze.pose_track`
- **Điểm mạnh:** điểm khớp toàn thân gồm ngón tay và khuôn mặt; ComfyUI controlnet_aux có node sẵn, xuất video khung xương để nối với Wan VACE.
- **Điểm yếu:** chỉ có điểm 2D; khi xoay người và che khuất trước/sau, trái phải dễ bị đảo.
- **Giấy phép:** cho phép thương mại (Apache 2.0).
- **Nguồn:** https://github.com/IDEA-Research/DWPose
- **Xác minh:** 2026-11-14 (kiến thức nền) · **Độ tin cậy:** medium

### B12. `rokoko-vision` — Rokoko Vision 3.0
- **Loại:** analysis · `ga`
- **Truy cập:** app
- **Năng lực:** `analyze.body_mocap`
- **Điểm mạnh:** tải lên một video là có chuyển động 3D đã làm sạch, xuất FBX / BVH (khung HIK, Mixamo), nhập thẳng vào Blender.
- **Điểm yếu:** gói miễn phí rất ít; xuất BVH cần gói trả phí.
- **Giấy phép:** commercial: conditional — theo điều khoản nền tảng.
- **Nguồn:** https://rokoko.com/products/video
- **Xác minh:** 2026-11-14 (nhà cung cấp) · **Độ tin cậy:** medium

### B13. `megasam` — MegaSaM
- **Loại:** analysis · `ga` · học thuật mã nguồn mở (CVPR 2025)
- **Năng lực:** `analyze.camera_motion`
- **Điểm mạnh:** từ video quay tay có vật động, suy ngược được tư thế camera và độ sâu; ổn định với cảnh động.
- **Giấy phép:** commercial: conditional — theo giấy phép kho mã.
- **Nguồn:** https://arxiv.org/abs/2412.04463
- **Xác minh:** 2026-10-29 (nhà cung cấp) · **Độ tin cậy:** medium

### B14. `demucs` — Demucs (htdemucs)
- **Loại:** analysis · `ga` · mã nguồn mở (Meta)
- **Năng lực:** `analyze.audio_separation`
- **Điểm mạnh:** tách bốn track: giọng hát, trống, bass, phần còn lại; là chuẩn cơ sở của ngành.
- **Giấy phép:** cho phép thương mại (MIT).
- **Nguồn:** https://github.com/facebookresearch/demucs
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** high

### B15. `librosa-madmom` — librosa / madmom
- **Loại:** analysis · `ga` · mã nguồn mở
- **Năng lực:** `analyze.beat_tempo`
- **Điểm mạnh:** phát hiện nhịp, BPM và onset, tạo điểm neo nhịp cho việc dựng phim.
- **Giấy phép:** cho phép thương mại. librosa là ISC; madmom mã nguồn BSD, mô hình CC-BY-NC-SA.
- **Nguồn:**
  - https://github.com/librosa/librosa
  - https://github.com/CPJKU/madmom
- **Xác minh:** 2026-10-29 (kiến thức nền) · **Độ tin cậy:** medium

---

**Ghi chú về số mục:** file nguồn có 20 mục, gồm 5 VLM (A1–A5) và 15 công cụ tất định (B1–B15); đánh số theo đúng thứ tự file.
