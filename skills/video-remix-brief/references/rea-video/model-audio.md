# Âm thanh: lồng tiếng, nhân bản giọng, nhạc, hiệu ứng, sinh âm thanh từ video
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/models/audio.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Chú thích: `audio.tts` = đọc văn bản thành tiếng; `audio.voice_clone` = nhân bản giọng; `audio.music_gen` = sinh nhạc; `audio.sfx_gen` = sinh hiệu ứng âm thanh; `audio.v2a_foley` = sinh âm thanh Foley từ video; `audio.tts_duration_control` = kiểm soát thời lượng khi đọc.

Tổng số mục: 12 mô hình.

---

### 1. `minimax-speech-2.8` — MiniMax Speech 2.8 (Turbo / HD)
- **Nhà cung cấp / loại:** MiniMax · audio · phát hành 2026-06 · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `audio.tts`, `audio.voice_clone`
- **Điểm mạnh:**
  - **[Người dùng xác nhận]** hỗ trợ nhân bản giọng.
  - Thuộc nhóm đầu về tiếng Trung, tiếng Trung là thế mạnh gốc; hỗ trợ tiếng Quảng Đông.
- **Chi phí:** Turbo 30–60 USD mỗi triệu ký tự; HD 50–80 USD mỗi triệu ký tự (dữ liệu bên thứ ba tháng 7/2026).
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://peihuachen.github.io/ai-tools-hub/posts/tts-commercial-open-source-comparison-guide-2026.html
- **Xác minh:** 2026-10-29 (căn cứ: người dùng) · **Độ tin cậy:** high
- **Ghi chú:** tháng phát hành là ước tính.

### 2. `indextts-2` — IndexTTS2 / IndexTTS 2.5 (mã nguồn mở, Bilibili)
- **Loại:** audio · phát hành 2025-09 · `ga` · mã nguồn mở
- **Truy cập:** open-weights
- **Năng lực:** `audio.tts`, `audio.voice_clone`, `audio.tts_duration_control`
- **Điểm mạnh:**
  - Kiểm soát thời lượng tường minh, hiếm có ở TTS tự hồi quy; phù hợp để nhét giọng đọc mới vào khoảng thời gian của video gốc.
  - Tách cảm xúc khỏi âm sắc; nhân bản zero-shot; song ngữ Trung–Anh.
- **Điểm yếu:** phải tự triển khai.
- **Giấy phép:** commercial: conditional — theo giấy phép kho mã.
- **Nguồn:**
  - https://arxiv.org/html/2506.21619v2
  - https://arxiv.org/html/2601.03888v3
- **Xác minh:** 2026-10-29 (nhà cung cấp) · **Độ tin cậy:** high

### 3. `qwen3-tts` — Qwen3-TTS (mã nguồn mở 1.7B / 0.6B)
- **Loại:** audio · phát hành 2026-01 · `ga`
- **Truy cập:** open-weights, api
- **Năng lực:** `audio.tts`, `audio.voice_clone`
- **Điểm mạnh:**
  - Nhân bản giọng chỉ với 3 giây âm thanh; hỗ trợ tiếng Quảng Đông, Tứ Xuyên, Bắc Kinh, Thượng Hải.
  - Apache 2.0; bản API trên Bailian hỗ trợ điều khiển giọng điệu bằng chỉ dẫn văn bản.
- **Giấy phép:** cho phép thương mại (Apache 2.0).
- **Nguồn:** https://peihuachen.github.io/ai-tools-hub/posts/tts-commercial-open-source-comparison-guide-2026.html
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** tháng phát hành là ước tính; độ dài âm thanh cần để nhân bản có nhiều nguồn nói khác nhau (3 giây hoặc 10–20 giây).

### 4. `cosyvoice-3` — CosyVoice 3 (mã nguồn mở) / Bailian CosyVoice v3.5
- **Loại:** audio · phát hành 2025-09 · `ga`
- **Truy cập:** open-weights, api
- **Năng lực:** `audio.tts`, `audio.voice_clone`
- **Điểm mạnh:** thuộc nhóm đầu về tiếng Trung; nhân bản zero-shot.
- **Chi phí:** Bailian flash 0.8 nhân dân tệ mỗi vạn ký tự; plus 1.5 nhân dân tệ mỗi vạn ký tự.
- **Giấy phép:** commercial: conditional — theo giấy phép kho mã.
- **Nguồn:** https://peihuachen.github.io/ai-tools-hub/posts/tts-commercial-open-source-comparison-guide-2026.html
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** tháng phát hành là ước tính.

### 5. `elevenlabs-v3` — ElevenLabs Eleven v3
- **Loại:** audio · phát hành 2025-06 · `ga`
- **Truy cập:** api, app
- **Năng lực:** `audio.tts`, `audio.voice_clone`
- **Điểm mạnh:** biểu cảm cảm xúc tốt nhất (nổi bật với tiếng Anh); hơn 70 ngôn ngữ; có quy trình lồng tiếng (dubbing).
- **Điểm yếu:** không có phương ngữ tiếng Trung; nội dung dài tốn nhiều tín dụng.
- **Chi phí:** khoảng 100 USD mỗi triệu ký tự.
- **Giấy phép:** cho phép thương mại; nhân bản cần ủy quyền rõ ràng.
- **Nguồn:** https://peihuachen.github.io/ai-tools-hub/posts/tts-commercial-open-source-comparison-guide-2026.html
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** high
- **Ghi chú:** Hypit đã tích hợp.

### 6. `doubao-tts` — Đọc tổng hợp và nhân bản giọng Doubao (Volcano Engine)
- **Loại:** audio · `ga`
- **Truy cập:** api
- **Năng lực:** `audio.tts`, `audio.voice_clone`
- **Điểm mạnh:** giọng tự nhiên, phương ngữ mở rộng liên tục; cùng hệ sinh thái với Seedance.
- **Chi phí:** khoảng 20–50 nhân dân tệ mỗi triệu ký tự.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://peihuachen.github.io/ai-tools-hub/posts/tts-commercial-open-source-comparison-guide-2026.html
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** low

### 7. `lyria-3-pro` — Lyria 3 Pro
- **Loại:** audio · phát hành 2026-03 · `ga`
- **Truy cập:** api, app
- **Năng lực:** `audio.music_gen`
- **Giới hạn:** tối đa 180 giây
- **Điểm mạnh:** có API; sinh bài hát tối đa 3 phút từ văn bản hoặc hình ảnh.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://aiunpacking.com/guides/ai-audio-music-generation-guide-2026/
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 8. `minimax-music-2.5` — MiniMax Music 2.5
- **Loại:** audio · phát hành 2026-04 · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `audio.music_gen`
- **Giới hạn:** tối đa 240 giây
- **Điểm mạnh:** bài hát 4 phút, hơn 100 loại nhạc cụ, có thể điều khiển cấu trúc theo đoạn; fal.ai cung cấp API.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://aiunpacking.com/guides/ai-audio-music-generation-guide-2026/
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** tháng phát hành là ước tính.

### 9. `suno-v5.5` — Suno v5.5
- **Loại:** audio · phát hành 2026-03 · `ga`
- **Truy cập:** app
- **Năng lực:** `audio.music_gen`
- **Điểm mạnh:** chất lượng nhạc hàng đầu; hỗ trợ mô hình tùy chỉnh và hát bằng giọng của chính mình.
- **Điểm yếu:**
  - Không có API chính thức, không phù hợp cho quy trình tự động.
  - Gói miễn phí không được dùng thương mại.
- **Giấy phép:** commercial: conditional — chỉ gói Pro / Premier mới có quyền thương mại.
- **Nguồn:** https://aiunpacking.com/guides/ai-audio-music-generation-guide-2026/
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 10. `elevenlabs-sfx` — ElevenLabs Sound Effects
- **Loại:** audio · `ga`
- **Truy cập:** api, app
- **Năng lực:** `audio.sfx_gen`
- **Giới hạn:** tối đa 30 giây
- **Điểm mạnh:** sinh hiệu ứng từ văn bản, có thể lặp; đầu ra WAV 48kHz.
- **Điểm yếu:** không xem video, phải tự đặt theo mã thời gian.
- **Giấy phép:** cho phép thương mại (từ gói Starter trở lên).
- **Nguồn:** https://www.creativeainews.com/articles/how-to-add-sound-effects-to-ai-video-2026/
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium

### 11. `hunyuanvideo-foley` — HunyuanVideo-Foley
- **Loại:** audio · phát hành 2025-08 · `ga`
- **Truy cập:** open-weights, api-aggregator
- **Năng lực:** `audio.v2a_foley`
- **Điểm mạnh:** nhìn video sinh âm thanh đồng bộ, 48kHz; chỉ số đồng bộ tốt nhất (DeSync 0.74; MMAudio là 0.80).
- **Điểm yếu:**
  - Cần 8–20 GB VRAM.
  - Giấy phép loại trừ EU, Anh, Hàn Quốc (bên thứ ba cho rằng đầu ra cũng bị hạn chế tương tự).
- **Giấy phép:** commercial: conditional — Tencent Community License.
- **Vùng loại trừ (regions_excluded):** EU, UK, KR
- **Nguồn:**
  - https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley
  - https://www.creativeainews.com/articles/how-to-add-sound-effects-to-ai-video-2026/
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** high

### 12. `mmaudio` — MMAudio
- **Loại:** audio · phát hành 2024-12 · `ga` · mã nguồn mở (học thuật)
- **Truy cập:** open-weights
- **Năng lực:** `audio.v2a_foley`
- **Giới hạn:** tối đa 8 giây
- **Điểm mạnh:** chạy với khoảng 6 GB VRAM.
- **Điểm yếu:**
  - Trọng số CC-BY-NC 4.0, không dùng thương mại.
  - Có thể sinh giọng người mơ hồ kiểu người; xử lý kém các âm thanh lạ.
- **Giấy phép:** không cho thương mại — mã MIT, trọng số CC-BY-NC 4.0.
- **Nguồn:** https://www.creativeainews.com/articles/how-to-add-sound-effects-to-ai-video-2026/
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** high

---

**Ghi chú về số mục:** file nguồn có 12 mục âm thanh, đánh số 1–12 theo đúng thứ tự file.
