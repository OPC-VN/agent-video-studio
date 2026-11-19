# Ma trận năng lực (tự sinh, không sửa tay)
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/MATRIX.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Bản gốc do `python3 scripts/validate_capabilities.py --matrix` sinh từ `rea_video/capabilities/`. Bản tiếng Việt này là bản chép dịch tại một thời điểm, không tự cập nhật theo lần sinh sau.

Độ tin cậy: ● high ◐ medium ○ low. Mô hình đã ngừng hoạt động không được liệt kê.

## 1. Nguyên thủy → mô hình khả dụng

| Nguyên thủy | Tên | Mô hình khả dụng |
|---|---|---|
| `analyze.video_understanding` | Hiểu ngữ nghĩa video | ◐ `doubao-seed-2.0-pro`, ◐ `gemini-3.1-pro`, ◐ `gemini-3.5-flash`, ◐ `pegasus-1.5`, ◐ `qwen3.5-397b-a17b` |
| `analyze.shot_boundary` | Phát hiện chuyển cảnh | ● `pyscenedetect`, ● `transnetv2` |
| `analyze.asr_word_align` | Nhận dạng giọng nói + căn chỉnh theo từ | ◐ `funasr-sensevoice`, ● `whisperx` |
| `analyze.ocr_text_track` | Nhận dạng chữ trên khung hình và quỹ đạo | ● `paddleocr` |
| `analyze.segmentation` | Phân đoạn và theo dõi | ◐ `sam-video` |
| `analyze.matting` | Tách nền video (alpha) | ◐ `matanyone-2`, ◐ `robust-video-matting`, ◐ `volcengine-matting` |
| `analyze.camera_motion` | Giải mã chuyển động máy quay | ◐ `megasam` |
| `analyze.audio_separation` | Tách âm thanh theo track | ● `demucs` |
| `analyze.beat_tempo` | Phân tích nhịp và đoạn nhạc | ◐ `librosa-madmom` |
| `analyze.depth_video` | Ước lượng độ sâu video | ◐ `video-depth-anything` |
| `analyze.pose_track` | Theo dõi khung xương người | ◐ `dwpose` |
| `analyze.body_mocap` | Motion capture từ video một camera | ◐ `rokoko-vision` |
| `analyze.image_layer_decompose` | Phân rã lớp của một khung hình | ◐ `seedream-5.0`, ◐ `seedream-5.5` |
| `image.t2i` | Văn bản sang ảnh | ◐ `flux-3`, ◐ `flux-3-klein`, ● `gpt-image-2.5`, ◐ `gpt-image-2.6`, ◐ `grok-imagine-image-2.0`, ○ `ideogram-4.5`, ◐ `kling-o3-image`, ◐ `mai-image-2.6`, ○ `midjourney-v8.2`, ◐ `minimax-h3-image`, ◐ `nano-banana-2-lite`, ◐ `nano-banana-2.1`, ◐ `qwen-image-2.1`, ◐ `qwen-image-3.0`, ◐ `qwen-image-3.0-pro`, ◐ `seedream-5.0`, ◐ `seedream-5.5` |
| `image.edit_multi_ref` | Chỉnh sửa/ghép ảnh nhiều tham chiếu | ◐ `flux-3`, ◐ `flux-3-klein`, ● `gpt-image-2.5`, ◐ `gpt-image-2.6`, ◐ `grok-imagine-image-2.0`, ○ `ideogram-4.5`, ◐ `kling-o3-image`, ◐ `mai-image-2.6`, ○ `midjourney-v8.2`, ◐ `minimax-h3-image`, ◐ `nano-banana-2.1`, ◐ `qwen-image-2.1`, ◐ `qwen-image-3.0`, ◐ `qwen-image-3.0-pro`, ◐ `seedream-5.0`, ◐ `seedream-5.5` |
| `image.text_render` | Vẽ chữ trong khung hình | ◐ `flux-3`, ● `gpt-image-2.5`, ◐ `gpt-image-2.6`, ○ `ideogram-4.5`, ◐ `mai-image-2.6`, ◐ `minimax-h3-image`, ◐ `nano-banana-2.1`, ◐ `qwen-image-2.1`, ◐ `qwen-image-3.0`, ◐ `qwen-image-3.0-pro`, ◐ `seedream-5.0`, ◐ `seedream-5.5` |
| `image.storyboard_series` | Bộ ảnh phân cảnh | ◐ `kling-o3-image`, ◐ `seedream-5.0` |
| `image.tryon` | Thử đồ ảo | ◐ `fashn-tryon-max`, ◐ `fashn-v1.6`, ◐ `kling-kolors-tryon`, ◐ `kling-virtual-tryon-3`, ◐ `qwen-image-2.1` |
| `video.t2v` | Văn bản sang video | ◐ `flux-3-video`, ○ `flux-3-video-max`, ◐ `gemini-omni-flash`, ◐ `grok-imagine-video-1.5`, ○ `grok-imagine-video-1.5-lite`, ◐ `hailuo-2.3`, ○ `happyhorse-1.0`, ◐ `heygen-video-1`, ◐ `hunyuanvideo-1.5`, ◐ `kling-3.0`, ◐ `kling-4.0`, ◐ `kling-4.0-flash`, ◐ `kling-o3`, ◐ `ltx-2.5`, ○ `luma-ray3.2`, ◐ `minimax-h3`, ◐ `minimax-h3-max`, ○ `p-video-2-pro`, ◐ `pika-h3-flex`, ◐ `pixverse-v6`, ◐ `runway-gen-4.5`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `seedance-2.5-flash`, ○ `skyreels-v4`, ○ `utopai-x`, ◐ `veo-3.1`, ◐ `vidu-q3`, ● `wan-2.2`, ◐ `wan-3.0` |
| `video.i2v_first_frame` | Ảnh sang video (khung đầu) | ◐ `flux-3-video`, ○ `flux-3-video-max`, ◐ `gemini-omni-flash`, ◐ `grok-imagine-video-1.5`, ○ `grok-imagine-video-1.5-lite`, ◐ `hailuo-2.3`, ○ `happyhorse-1.0`, ◐ `heygen-video-1`, ◐ `hunyuanvideo-1.5`, ◐ `kling-3.0`, ◐ `kling-4.0`, ◐ `kling-4.0-flash`, ◐ `kling-o3`, ◐ `ltx-2.5`, ○ `luma-ray3.2`, ◐ `minimax-h3`, ◐ `minimax-h3-max`, ○ `p-video-2-pro`, ◐ `pika-h3-flex`, ◐ `pixverse-v6`, ◐ `runway-gen-4.5`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `seedance-2.5-flash`, ○ `skyreels-v4`, ◐ `veo-3.1`, ◐ `vidu-q3`, ◐ `vidu-q4-preview`, ● `wan-2.2`, ◐ `wan-3.0`, ◐ `wan-vace` |
| `video.i2v_first_last` | Sinh từ khung đầu và khung cuối | ◐ `flux-3-video`, ○ `flux-3-video-max`, ◐ `gemini-omni-flash`, ◐ `grok-imagine-video-1.5`, ◐ `heygen-video-1`, ◐ `kling-3.0`, ◐ `kling-4.0`, ◐ `kling-o3`, ◐ `minimax-h3`, ◐ `minimax-h3-max`, ○ `p-video-2-pro`, ◐ `pika-h3-flex`, ◐ `pixverse-v6`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `seedance-2.5-flash`, ◐ `veo-3.1`, ◐ `wan-3.0` |
| `video.keyframes` | Điều khiển nhiều keyframe | ◐ `flux-3-video`, ○ `flux-3-video-max`, ◐ `grok-imagine-video-1.5`, ◐ `kling-4.0`, ◐ `runway-gen-4.5` |
| `video.multi_reference` | Sinh video từ nhiều tham chiếu (giữ nhất quán chủ thể) | ◐ `gemini-omni-flash`, ◐ `grok-imagine-video-1.5`, ○ `happyhorse-1.0`, ◐ `heygen-video-1`, ◐ `kling-3.0`, ◐ `kling-4.0`, ◐ `kling-4.0-flash`, ◐ `kling-o3`, ◐ `minimax-h3`, ◐ `minimax-h3-max`, ◐ `pika-h3-flex`, ◐ `pixverse-v6`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `seedance-2.5-flash`, ◐ `veo-3.1`, ◐ `vidu-q3`, ◐ `vidu-q4-preview`, ◐ `wan-3.0` |
| `video.reference_video` | Sinh video từ video tham chiếu (chuyển động / máy quay / hiệu ứng) | ◐ `gemini-omni-flash`, ◐ `heygen-video-1`, ◐ `kling-4.0`, ◐ `kling-4.0-flash`, ◐ `kling-o3`, ◐ `minimax-h3-max`, ◐ `pika-h3-flex`, ◐ `pixverse-v6`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `seedance-2.5-flash`, ○ `skyreels-v4`, ◐ `wan-3.0` |
| `video.reference_audio` | Sinh video từ âm thanh tham chiếu | ◐ `grok-imagine-video-1.5`, ◐ `heygen-video-1`, ◐ `kling-4.0-flash`, ◐ `ltx-2.5`, ◐ `minimax-h3-max`, ◐ `pika-h3-flex`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `seedance-2.5-flash`, ◐ `vidu-q4-preview`, ◐ `wan-3.0` |
| `video.multi_shot` | Nhiều cảnh trong một lần sinh | ◐ `flux-3-video`, ◐ `gemini-omni-flash`, ◐ `kling-3.0`, ◐ `kling-4.0`, ◐ `kling-4.0-flash`, ◐ `kling-o3`, ◐ `ltx-2.5`, ◐ `minimax-h3`, ◐ `pika-h3-flex`, ◐ `pixverse-v6`, ◐ `seedance-2.0`, ● `seedance-2.5`, ◐ `veo-3.1`, ◐ `vidu-q4-preview`, ◐ `wan-3.0` |
| `video.extend` | Nối dài (extend) | ◐ `flux-3-video`, ◐ `gemini-omni-flash`, ● `seedance-2.5`, ◐ `veo-3.1` |
| `video.edit_v2v` | Chỉnh sửa video (giữ chuyển động) | ◐ `flux-3-video`, ◐ `gemini-omni-flash`, ○ `happyhorse-1.0`, ○ `higgsfield-genjutsu`, ◐ `kling-4.0`, ◐ `kling-o3`, ◐ `ltx-2.5`, ○ `luma-ray3.2`, ◐ `pika-h3-flex`, ○ `runway-aleph-2`, ◐ `runway-gen-4.5`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `skyreels-v4`, ◐ `viggle-animate`, ◐ `wan-2.2-animate`, ○ `wan-2.7-edit`, ◐ `wan-vace` |
| `video.camera_control` | Điều khiển máy quay và tham số ống kính | ◐ `gemini-omni-flash`, ◐ `kling-3.0`, ◐ `kling-4.0`, ◐ `pixverse-v6`, ○ `runway-aleph-2`, ◐ `runway-gen-4.5`, ● `seedance-2.5` |
| `video.native_audio` | Âm thanh và hình ảnh cùng sinh | ◐ `flux-3-video`, ○ `flux-3-video-max`, ◐ `gemini-omni-flash`, ◐ `grok-imagine-video-1.5`, ○ `grok-imagine-video-1.5-lite`, ◐ `heygen-video-1`, ◐ `kling-3.0`, ◐ `kling-4.0`, ◐ `kling-4.0-flash`, ◐ `ltx-2.5`, ○ `luma-ray3.2`, ◐ `minimax-h3`, ◐ `minimax-h3-max`, ○ `p-video-2-pro`, ◐ `pika-h3-flex`, ◐ `pixverse-v6`, ◐ `runway-gen-4.5`, ◐ `seedance-2.0`, ● `seedance-2.5`, ○ `seedance-2.5-flash`, ○ `skyreels-v4`, ○ `utopai-x`, ◐ `veo-3.1`, ◐ `vidu-q3`, ◐ `vidu-q4-preview`, ◐ `wan-3.0` |
| `video.control_video` | Sinh theo video điều khiển | ◐ `wan-vace` |
| `motion.transfer` | Chuyển động | ○ `dreamactor-m2.0`, ○ `higgsfield-genjutsu`, ◐ `kling-motion-control`, ◐ `runway-gen-4.5`, ◐ `viggle-animate`, ◐ `viggle-v4`, ◐ `wan-2.2-animate`, ◐ `wan-animate-2` |
| `avatar.audio_driven` | Người ảo điều khiển bằng âm thanh | ○ `creatify-aurora`, ○ `hedra-omnia`, ◐ `heygen-avatar-v`, ◐ `kling-avatar-v2`, ◐ `longcat-video-avatar-1.5`, ◐ `ltx-2.3-lipsync`, ◐ `ltx-2.5`, ◐ `mirage-avatar-x`, ◐ `omnihuman-2.0`, ◐ `sync-3`, ◐ `synthesia-express-3`, ○ `veed-fabric-1.0` |
| `lipsync.redub` | Dub lại khẩu hình | ◐ `heygen-avatar-v`, ◐ `sync-3`, ◐ `sync-react-1` |
| `threed.image_to_3d` | Ảnh sang 3D | ◐ `hunyuan-3d`, ◐ `rodin-gen-2.5`, ◐ `tripo-p1` |
| `audio.tts` | Tổng hợp giọng nói | ◐ `cosyvoice-3`, ○ `doubao-tts`, ● `elevenlabs-v3`, ◐ `heygen-avatar-v`, ● `indextts-2`, ● `minimax-speech-2.8`, ◐ `mirage-avatar-x`, ◐ `qwen3-tts`, ◐ `sync-3`, ◐ `synthesia-express-3` |
| `audio.voice_clone` | Nhân bản giọng | ◐ `cosyvoice-3`, ○ `doubao-tts`, ● `elevenlabs-v3`, ◐ `heygen-avatar-v`, ● `indextts-2`, ● `minimax-speech-2.8`, ◐ `mirage-avatar-x`, ◐ `qwen3-tts` |
| `audio.tts_duration_control` | Lồng tiếng kiểm soát thời lượng | ● `indextts-2` |
| `audio.music_gen` | Sinh nhạc | ◐ `lyria-3-pro`, ◐ `minimax-music-2.5`, ◐ `suno-v5.5` |
| `audio.sfx_gen` | Văn bản sang hiệu ứng âm | ◐ `elevenlabs-sfx` |
| `audio.v2a_foley` | Sinh hiệu ứng âm từ video (Foley) | ● `hunyuanvideo-foley`, ● `mmaudio` |
| `render.code_graphics` | Hoạt ảnh render bằng code | ◐ `html-gsap-playwright`, ● `motion-canvas`, ● `remotion` |
| `render.web_capture` | Quay màn hình web/giao diện | ◐ `html-gsap-playwright` |
| `render.3d_scene` | Render cảnh 3D | ● `blender` |
| `render.compose` | Ghép và mã hoá | ● `ffmpeg`, ● `remotion` |
| `post.upscale` | Siêu phân giải video | ◐ `flashvsr`, ◐ `real-esrgan`, ◐ `seedvr2`, ◐ `topaz-video` |
| `post.frame_interp` | Nội suy khung hình | ● `rife`, ◐ `topaz-video` |

## 2. Danh sách mô hình

| Mô hình | Nhà phát hành | Loại | Trạng thái | Thời lượng tối đa (s) | Âm thanh gốc | Thương mại | Căn cứ xác minh |
|---|---|---|---|---|---|---|---|
| Demucs (htdemucs) | Meta (mã nguồn mở) | analysis | ga |  |  | Có | knowledge 2026-10-29 |
| Doubao Seed 2.0 Pro (Doubao) | ByteDance | analysis | ga |  |  | Có | third-party 2026-10-29 |
| DWPose | IDEA Research (mã nguồn mở) | analysis | ga |  |  | Có | knowledge 2026-11-14 |
| FunASR / SenseVoice | Alibaba (mã nguồn mở) | analysis | ga |  |  | Có điều kiện | knowledge 2026-10-29 |
| Gemini 3.1 Pro | Google | analysis | ga | 10800 |  | Có | third-party 2026-10-29 |
| Gemini 3.5 Flash | Google | analysis | ga | 10800 |  | Có | third-party 2026-10-29 |
| librosa / madmom | Mã nguồn mở | analysis | ga |  |  | Có | knowledge 2026-10-29 |
| MatAnyone 2 | Học thuật, mã nguồn mở | analysis | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| MegaSaM | Học thuật, mã nguồn mở (CVPR 2025) | analysis | ga |  |  | Có điều kiện | vendor 2026-10-29 |
| PaddleOCR | Baidu (mã nguồn mở) | analysis | ga |  |  | Có | knowledge 2026-10-29 |
| Twelve Labs Pegasus 1.5 | Twelve Labs | analysis | ga | 7200 |  | Có | third-party 2026-10-29 |
| PySceneDetect | Mã nguồn mở | analysis | ga |  |  | Có | knowledge 2026-10-29 |
| Qwen3.5 397B-A17B (mã nguồn mở) | Alibaba | analysis | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| RobustVideoMatting (RVM) | Mã nguồn mở | analysis | ga |  |  | Có điều kiện | knowledge 2026-10-29 |
| Rokoko Vision 3.0 | Rokoko | analysis | ga |  |  | Có điều kiện | vendor 2026-11-14 |
| SAM (SAM 2 / SAM 3) | Meta (mã nguồn mở) | analysis | ga |  |  | Có điều kiện | knowledge 2026-10-29 |
| TransNetV2 | Mã nguồn mở | analysis | ga |  |  | Có | knowledge 2026-10-29 |
| Video Depth Anything | ByteDance (mã nguồn mở) | analysis | ga |  |  | Có điều kiện | third-party 2026-11-14 |
| Volcengine portrait video matting | ByteDance | analysis | ga |  |  | Có | third-party 2026-10-29 |
| WhisperX | Mã nguồn mở | analysis | ga |  |  | Có | knowledge 2026-10-29 |
| CosyVoice 3 (mã nguồn mở) / Bailian CosyVoice v3.5 | Alibaba | audio | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| Doubao speech synthesis / voice cloning (Volcengine) | ByteDance | audio | ga |  |  | Có | third-party 2026-10-29 |
| ElevenLabs Sound Effects | ElevenLabs | audio | ga | 30 |  | Có | third-party 2026-10-29 |
| ElevenLabs Eleven v3 | ElevenLabs | audio | ga |  |  | Có | third-party 2026-10-29 |
| HunyuanVideo-Foley | Tencent | audio | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| IndexTTS2 / IndexTTS 2.5 (mã nguồn mở, Bilibili) | Bilibili | audio | ga |  |  | Có điều kiện | vendor 2026-10-29 |
| Lyria 3 Pro | Google | audio | ga | 180 |  | Có | third-party 2026-10-29 |
| MiniMax Music 2.5 | MiniMax | audio | ga | 240 |  | Có | third-party 2026-10-29 |
| MiniMax Speech 2.8 (Turbo / HD) | MiniMax | audio | ga |  |  | Có | user 2026-10-29 |
| MMAudio | Học thuật, mã nguồn mở | audio | ga | 8 |  | Không | third-party 2026-10-29 |
| Qwen3-TTS (mã nguồn mở 1.7B / 0.6B) | Alibaba | audio | ga |  |  | Có | third-party 2026-10-29 |
| Suno v5.5 | Suno | audio | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| Creatify Aurora | Creatify | character | ga |  |  | Có điều kiện | third-party 2026-11-12 |
| DreamActor M2.0 | ByteDance | character | ga |  |  | Có | vendor 2026-11-12 |
| FASHN Try-On Max | FASHN | character | ga |  |  | Có | vendor 2026-11-12 |
| FASHN Virtual Try-On v1.6 | FASHN | character | ga |  |  | Có | third-party 2026-10-29 |
| Hedra Omnia (Alpha) | Hedra | character | preview | 8 |  | Có điều kiện | vendor 2026-11-12 |
| HeyGen Avatar V | HeyGen | character | ga |  |  | Có | vendor 2026-11-12 |
| Kling Avatar v2 | Kuaishou | character | ga |  |  | Có | third-party 2026-10-29 |
| Kling Kolors Virtual Try-On v1.5 | Kuaishou | character | ga |  |  | Có | third-party 2026-10-29 |
| Kling Motion Control (2.6 / 3.0) | Kuaishou | character | ga |  |  | Có | third-party 2026-10-29 |
| Kling Virtual Try-On 3.0 | Kuaishou | character | ga |  |  | Có | vendor 2026-11-12 |
| LongCat-Video-Avatar-1.5 | Meituan LongCat | character | ga |  |  | Có | vendor 2026-11-12 |
| LTX 2.3 Lipsync | Lightricks | character | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| Mirage Avatar X (trước là Captions) | Mirage | character | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| OmniHuman 2.0 | ByteDance | character | ga |  |  | Có | vendor 2026-11-12 |
| Sync 3 (Sync Labs) | Sync Labs | character | ga |  |  | Có | vendor 2026-11-12 |
| sync react-1 | Sync Labs | character | ga |  |  | Có | vendor 2026-11-12 |
| Synthesia Express-3 | Synthesia | character | ga |  |  | Có | vendor 2026-11-12 |
| VEED Fabric 1.0 (gồm Fast) | VEED | character | ga |  |  | Có điều kiện | third-party 2026-11-12 |
| Viggle-Animate | Viggle | character | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| Viggle V4 | Viggle | character | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| Wan 2.2 Animate (gồm animate-mix đổi người) | Alibaba | character | ga |  |  | Có | third-party 2026-10-29 |
| Wan-Animate-2 | Alibaba | character | ga |  |  | Có | vendor 2026-11-12 |
| FLUX 3 Image | Black Forest Labs | image | ga |  |  | Có | vendor 2026-11-12 |
| FLUX 3 Image Klein | Black Forest Labs | image | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| GPT Image 2.5 | OpenAI | image | ga |  |  | Có | user 2026-10-29 |
| GPT Image 2.6 (Sunburst / Flare) | OpenAI | image | ga |  |  | Có | vendor 2026-11-12 |
| Grok Imagine Image 2.0 | xAI | image | ga |  |  | Có | vendor 2026-11-12 |
| Ideogram 4.5 | Ideogram | image | ga |  |  | Có điều kiện | third-party 2026-11-12 |
| Kling Image 3.0 / 3.0 Omni (O3 Image) | Kuaishou | image | ga |  |  | Có | vendor 2026-11-12 |
| MAI-Image-2.6 (gồm Flash) | Microsoft AI | image | ga |  |  | Có | vendor 2026-11-12 |
| Midjourney V8.2 | Midjourney | image | ga |  |  | Có điều kiện | third-party 2026-11-12 |
| MiniMax H3 Image (gồm Highspeed) | MiniMax | image | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image) | Google | image | ga |  |  | Có | vendor 2026-11-12 |
| Nano Banana 2.1 | Google | image | ga |  |  | Có | vendor 2026-11-12 |
| Qwen Image 2.1 (mã nguồn mở 7B, gồm Pro / Turbo API) | Alibaba | image | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| Qwen Image 3.0 | Alibaba | image | ga |  |  | Có | vendor 2026-11-12 |
| Qwen Image 3.0 Pro | Alibaba | image | ga |  |  | Có | third-party 2026-10-29 |
| Seedream 5.0 (Lite / Pro / Flash) | ByteDance Seed | image | ga |  |  | Có | vendor 2026-11-12 |
| Seedream 5.5 | ByteDance Seed | image | ga |  |  | Có | vendor 2026-11-12 |
| FlashVSR | Học thuật, mã nguồn mở | post | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| Real-ESRGAN | Mã nguồn mở | post | ga |  |  | Có | third-party 2026-10-29 |
| RIFE | Mã nguồn mở | post | ga |  |  | Có | knowledge 2026-10-29 |
| SeedVR2 | ByteDance Seed (mã nguồn mở) | post | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| Topaz Video (gồm dòng Starlight) | Topaz Labs | post | ga |  |  | Có | third-party 2026-10-29 |
| Blender | Mã nguồn mở | render | ga |  |  | Có | knowledge 2026-10-29 |
| FFmpeg | Mã nguồn mở | render | ga |  |  | Có | knowledge 2026-10-29 |
| HTML + GSAP + Playwright capture | Tổ hợp mã nguồn mở | render | ga |  |  | Có | knowledge 2026-10-29 |
| Motion Canvas | Mã nguồn mở | render | ga |  |  | Có | knowledge 2026-10-29 |
| Remotion | Remotion (mã nguồn mở, thương mại cần giấy phép) | render | ga |  |  | Có điều kiện | knowledge 2026-10-29 |
| Hunyuan 3D (3.x) | Tencent | threed | ga |  |  | Có | third-party 2026-10-29 |
| Rodin Gen-2.5 | Hyper3D / Deemos | threed | ga |  |  | Có | third-party 2026-10-29 |
| Tripo P1 | Tripo | threed | ga |  |  | Có | third-party 2026-10-29 |
| FLUX 3 Video | Black Forest Labs | video | ga | 20 | Có | Có điều kiện | vendor 2026-11-12 |
| FLUX 3 Max (video) | Black Forest Labs | video | ga | 20 | Có | Có điều kiện | vendor 2026-11-12 |
| Gemini Omni Flash | Google | video | ga | 15 | Có | Có | vendor 2026-11-12 |
| Grok Imagine Video 1.5 | xAI | video | ga | 15 | Có | Có điều kiện | vendor 2026-11-12 |
| Grok Imagine Video 1.5 Lite | xAI | video | ga | 15 | Có | Có điều kiện | vendor 2026-11-12 |
| Hailuo 2.3 / 2.3 Fast (Hailuo) | MiniMax | video | ga | 10 | Có | Có | third-party 2026-10-29 |
| HappyHorse 1.0 | Alibaba | video | ga |  |  | Có điều kiện | third-party 2026-11-12 |
| HeyGen Video 1 | HeyGen | video | ga | 30 | Có | Có điều kiện | vendor 2026-11-12 |
| Higgsfield Genjutsu (gồm Lite) | Higgsfield | video | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| HunyuanVideo 1.5 (mã nguồn mở) | Tencent | video | ga |  |  | Có điều kiện | third-party 2026-10-29 |
| Kling 3.0 (gồm Turbo) | Kuaishou | video | ga | 15 | Có | Có | third-party 2026-10-29 |
| Kling 4.0 (Kling 4.0) | Kuaishou | video | ga | 30 | Có | Có | vendor 2026-11-12 |
| Kling 4.0 Flash (Kling 4.0 Flash) | Kuaishou | video | ga | 20 | Có | Có | vendor 2026-11-12 |
| Kling O3 (Omni) | Kuaishou | video | ga | 15 | Không | Có | third-party 2026-10-29 |
| LTX-2.5 (mã nguồn mở) | Lightricks | video | ga |  | Có | Có điều kiện | third-party 2026-11-12 |
| Luma Ray3.2 / Modify | Luma AI | video | ga | 10 | Có | Có | vendor 2026-11-12 |
| MiniMax H3 / H3 Max | MiniMax | video | ga | 15 | Có | Có điều kiện | third-party 2026-10-29 |
| MiniMax H3 Max | MiniMax | video | ga | 15 | Có | Có điều kiện | vendor 2026-11-12 |
| P-Video-2-Pro | Pruna AI | video | ga | 15 | Có | Có điều kiện | third-party 2026-11-12 |
| Pika H3 Flex | Pika | video | ga | 15 | Có | Có điều kiện | vendor 2026-11-12 |
| PixVerse V6 | PixVerse | video | ga | 15 | Có | Có | third-party 2026-10-29 |
| Runway Aleph 2 | Runway | video | ga |  |  | Có | vendor 2026-11-12 |
| Runway Gen-4.5 (gồm Act-Two) | Runway | video | ga | 10 | Có | Có | third-party 2026-10-29 |
| Seedance 2.0 (gồm Mini / Fast) | ByteDance Seed | video | ga | 15 | Có | Có | third-party 2026-11-11 |
| Seedance 2.5 | ByteDance Seed | video | ga | 30 | Có | Có | vendor 2026-11-11 |
| Seedance 2.5 Flash | ByteDance Seed | video | preview |  | Có | Có điều kiện | third-party 2026-11-12 |
| SkyReels V4 | Kunlun Skywork | video | ga |  |  | Có điều kiện | third-party 2026-11-12 |
| Sora 2 / Sora 2 Pro | OpenAI | video | shutdown | 20 |  | Không | third-party 2026-10-29 |
| Utopai X | Utopai Studios | video | ga |  |  | Có điều kiện | vendor 2026-11-12 |
| Veo 3.1 (gồm Lite) | Google | video | ga | 8 | Có | Có | third-party 2026-10-29 |
| Vidu Q3 | Shengshu | video | ga | 16 | Có | Có | vendor 2026-10-29 |
| Vidu Q4 Preview | Shengshu | video | preview | 16 | Có | Có điều kiện | vendor 2026-11-12 |
| Wan 2.2 (mã nguồn mở, gồm TI2V-5B) | Alibaba | video | ga |  | Không | Có | third-party 2026-10-29 |
| Wan 2.7 video editing | Alibaba | video | ga |  |  | Có | third-party 2026-10-29 |
| Wan 3.0 (Wanxiang) | Alibaba | video | ga | 30 | Có | Có | vendor 2026-11-12 |
| Wan VACE (Wan 2.1 VACE / Wan2.2-VACE-Fun) | Alibaba | video | ga |  | Không | Có | third-party 2026-11-14 |
