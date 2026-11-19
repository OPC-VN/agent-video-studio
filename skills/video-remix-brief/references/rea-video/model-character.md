# Nhân vật: chuyển động, người ảo, đồng bộ khẩu hình, thử đồ ảo
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/models/character.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Chú thích: `motion.transfer` = chuyển động từ video tham chiếu sang ảnh nhân vật; `avatar.audio_driven` = người ảo điều khiển bằng âm thanh; `lipsync.redub` = lồng tiếng và đồng bộ khẩu hình cho video có sẵn; `image.tryon` = thử đồ ảo trên ảnh.

Tổng số mục: 22 mô hình.

| # | id | Tên | Nhà cung cấp | Nhóm năng lực | Trạng thái |
|---|---|---|---|---|---|
| 1 | `kling-motion-control` | Kling Motion Control (2.6 / 3.0) | Kuaishou | motion.transfer | ga |
| 2 | `wan-2.2-animate` | Wan 2.2 Animate (gồm animate-mix đổi người) | Alibaba | motion.transfer, video.edit_v2v | ga |
| 3 | `wan-animate-2` | Wan-Animate-2 | Alibaba | motion.transfer | ga |
| 4 | `omnihuman-2.0` | OmniHuman 2.0 | ByteDance | avatar.audio_driven | ga |
| 5 | `kling-avatar-v2` | Kling Avatar v2 | Kuaishou | avatar.audio_driven | ga |
| 6 | `ltx-2.3-lipsync` | LTX 2.3 Lipsync | Lightricks | avatar.audio_driven | ga |
| 7 | `sync-3` | Sync 3 (Sync Labs) | Sync Labs | lipsync.redub, avatar.audio_driven, audio.tts | ga |
| 8 | `sync-react-1` | sync react-1 | Sync Labs | lipsync.redub | ga |
| 9 | `fashn-v1.6` | FASHN Virtual Try-On v1.6 | FASHN | image.tryon | ga |
| 10 | `fashn-tryon-max` | FASHN Try-On Max | FASHN | image.tryon | ga |
| 11 | `kling-kolors-tryon` | Kling Kolors Virtual Try-On v1.5 | Kuaishou | image.tryon | ga |
| 12 | `kling-virtual-tryon-3` | Kling Virtual Try-On 3.0 | Kuaishou | image.tryon | ga |
| 13 | `heygen-avatar-v` | HeyGen Avatar V | HeyGen | avatar.audio_driven, lipsync.redub, audio.tts, audio.voice_clone | ga |
| 14 | `synthesia-express-3` | Synthesia Express-3 | Synthesia | avatar.audio_driven, audio.tts | ga |
| 15 | `mirage-avatar-x` | Mirage Avatar X (trước đây là Captions) | Mirage | avatar.audio_driven, audio.tts, audio.voice_clone | ga |
| 16 | `longcat-video-avatar-1.5` | LongCat-Video-Avatar-1.5 | Meituan LongCat | avatar.audio_driven | ga |
| 17 | `creatify-aurora` | Creatify Aurora | Creatify | avatar.audio_driven | ga |
| 18 | `veed-fabric-1.0` | VEED Fabric 1.0 (gồm Fast) | VEED | avatar.audio_driven | ga |
| 19 | `hedra-omnia` | Hedra Omnia (Alpha) | Hedra | avatar.audio_driven | preview |
| 20 | `viggle-animate` | Viggle-Animate | Viggle | motion.transfer, video.edit_v2v | ga |
| 21 | `viggle-v4` | Viggle V4 | Viggle | motion.transfer | ga |
| 22 | `dreamactor-m2.0` | DreamActor M2.0 | ByteDance | motion.transfer | ga |

---

## Chi tiết từng mô hình

### 1. `kling-motion-control` — Kling Motion Control (2.6 / 3.0)
- **Nhà cung cấp / loại:** Kuaishou · character · phát hành 2025-12 · `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `motion.transfer`
- **Điểm mạnh:**
  - Chuyển động từ video tham chiếu sang ảnh nhân vật; bên thứ ba đánh giá đây là chuẩn chất lượng cho điều khiển chuyển động.
  - Có báo cáo kỹ thuật (arXiv 2603.03160).
  - Bản 3.0 cho phép gắn chủ thể để giữ khuôn mặt nhất quán (chỉ giữ khuôn mặt, không giữ trang phục hay kiểu tóc; chỉ dùng được ở chế độ theo hướng video).
- **Điểm yếu:** khi dùng video của người khác để điều khiển, cần chú ý quyền chân dung và bản quyền.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://arxiv.org/html/2603.03160v1
  - https://templix.app/blogs/best-ai-motion-control-and-animation-models-in-2026
  - https://kling.ai/quickstart/motion-control-user-guide
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** bản 3.0 lên API ngày 2026-03-04; video tham chiếu dài 3–30 giây, một cảnh liền mạch, thấy toàn thân và đầu; nếu chuyển động quá nhanh, đầu ra có thể ngắn hơn tham chiếu.

### 2. `wan-2.2-animate` — Wan 2.2 Animate (gồm animate-mix đổi người)
- **Loại:** character · phát hành 2025-09 · `ga`
- **Truy cập:** open-weights, api
- **Năng lực:** `motion.transfer`, `video.edit_v2v`
- **Điểm mạnh:** mã nguồn mở; vừa làm chuyển động vừa đổi người ngay trong video gốc. video-replicate-studio dùng `wan2.2-animate-mix` để đổi người.
- **Điểm yếu:** cần card đồ họa cục bộ hoặc API trả phí.
- **Giấy phép:** cho phép thương mại (Apache 2.0, trọng số mở).
- **Nguồn:**
  - https://wanvideogenerator.com/blog/ai-motion-control-kling26-vs-wan22-animate
  - https://github.com/derek-zhuolin/video-replicate-studio
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** phiên bản kế tiếp Wan-Animate-2 (2026-08, mã nguồn mở) có mục riêng.

### 3. `wan-animate-2` — Wan-Animate-2
- **Loại:** character · phát hành 2026-08 · `ga`
- **Truy cập:** open-weights
- **Năng lực:** `motion.transfer`
- **Giới hạn:** 480p, 720p
- **Điểm mạnh:**
  - Dùng trực tiếp video điều khiển, không cần trích xương trước; có thể dùng văn bản để đổi góc nhìn.
  - Apache 2.0, mã nguồn mở.
- **Điểm yếu:**
  - Yêu cầu phần cứng cao (cấu hình tham chiếu 720p là 8 card A800); không có API lưu trữ.
  - Hỗ trợ ComfyUI chưa phát hành chính thức.
- **Giấy phép:** cho phép thương mại (Apache 2.0).
- **Nguồn:** https://github.com/Wan-Video/Wan-Animate-2
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 4. `omnihuman-2.0` — OmniHuman 2.0
- **Loại:** character · phát hành 2026-10 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `avatar.audio_driven`
- **Giới hạn:** âm thanh 4–300 giây; 720p
- **Điểm mạnh:**
  - Một ảnh cộng một đoạn âm thanh là có thể tạo buổi biểu diễn một cảnh dài.
  - Động tác thay đổi theo ngữ nghĩa và nhịp; hỗ trợ nhiều người, nhân vật phi người và hát.
  - Có thể dùng prompt để điều khiển tư thế, góc máy và tương tác.
- **Điểm yếu:** chất lượng biểu diễn phụ thuộc chủ yếu vào độ biểu cảm của âm thanh.
- **Chi phí:** `usd_per_s` 0.07 (BytePlus 0.07 USD/giây, trước đây 0.12; fal 0.105).
- **Giấy phép:** cho phép thương mại (điều khoản BytePlus).
- **Nguồn:**
  - https://www.eachlabs.ai/blog/best-ai-lip-sync-models-2026
  - https://docs.byteplus.com/en/docs/byteplus-vision/omnihuman-2-0-video-generation
  - https://fal.ai/models/fal-ai/bytedance/omnihuman/v2/llms.txt
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** BytePlus mở 2026-10-15; cạnh ảnh 300–6000 px, tỷ lệ 0.4–2.5; người, động vật, anime, nhân vật 3D đều điều khiển được; chưa xác nhận Jimeng digital human đã dùng bản 2.0.

### 5. `kling-avatar-v2` — Kling Avatar v2
- **Loại:** character · phát hành 2025-12 · `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `avatar.audio_driven`
- **Điểm mạnh:** thiết lập đơn giản; bản Standard dùng để lặp, bản Pro dùng cho thành phẩm.
- **Điểm yếu:** tài liệu không nêu rõ thời lượng.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:** https://www.eachlabs.ai/blog/best-ai-lip-sync-models-2026
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** mở toàn bộ 2025-12-04, tối đa 5 phút; hiện chưa có phiên bản mới hơn.

### 6. `ltx-2.3-lipsync` — LTX 2.3 Lipsync
- **Loại:** character · phát hành 2026-03 · `ga`
- **Truy cập:** api, open-weights
- **Năng lực:** `avatar.audio_driven`
- **Giới hạn:** âm thanh 5–20 giây; 480p, 1080p
- **Điểm mạnh:** có thể cố định seed: dùng 480p để làm bản nháp, rồi dùng cùng seed để ra 1080p thành phẩm.
- **Điểm yếu:** chỉ phù hợp đoạn ngắn.
- **Giấy phép:** commercial: conditional — LTX Community License.
- **Nguồn:** https://www.eachlabs.ai/blog/best-ai-lip-sync-models-2026
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** tháng phát hành là ước tính.

### 7. `sync-3` — Sync 3 (Sync Labs)
- **Loại:** character · phát hành 2026-04 · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `lipsync.redub`, `avatar.audio_driven`, `audio.tts`
- **Giới hạn:** 4K
- **Điểm mạnh:**
  - Phân tích toàn cảnh trước rồi mới đồng bộ khẩu hình; xử lý được quay đầu, bóng đổ, máy cầm tay và cảnh hai người.
  - Giữ nguyên diễn xuất gốc; tối đa 4K 60fps.
- **Điểm yếu:**
  - Không chỉ định được mặt nạ hoặc khung mặt; không có prompt hình ảnh.
  - Lipsync v2 Pro cũ có `sync_mode` (cách xử lý khi thời lượng không khớp); v3 không có.
- **Chi phí:** `usd_per_s` 0.133 (0.107–0.133 USD/giây).
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://www.eachlabs.ai/blog/best-ai-lip-sync-models-2026
  - https://sync.so/docs/models/sync-3
  - https://sync.so/changelog/
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-04-06; mở cho mọi người 2026-05-05; 2026-07-14 thêm chức năng ảnh tĩnh cộng âm thanh; tháng 8 thêm lồng tiếng 92 ngôn ngữ; có thể đưa thẳng văn bản cho TTS.

### 8. `sync-react-1` — sync react-1
- **Loại:** character · phát hành 2025-12 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `lipsync.redub`
- **Giới hạn:** âm thanh tối đa 15 giây
- **Điểm mạnh:** không chỉ đồng bộ khẩu hình mà còn tái hiện biểu cảm và động tác đầu; có thể chỉ định một từ chỉ cảm xúc.
- **Điểm yếu:** tối đa 15 giây; trong khung hình chỉ được có một người nói rõ ràng, không có nhận diện người nói và phát hiện che khuất.
- **Chi phí:** `usd_per_s` 0.167 (0.133–0.167 USD/giây).
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://sync.so/docs/models/react
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 9. `fashn-v1.6` — FASHN Virtual Try-On v1.6
- **Loại:** character · phát hành 2026-03 · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `image.tryon`
- **Giới hạn:** 864x1296
- **Điểm mạnh:** họa tiết và chữ in trên trang phục giữ rõ; đầu vào có thể là ảnh người mẫu hoặc ảnh trải phẳng, tự nhận diện loại trang phục.
- **Điểm yếu:** chỉ thử đồ trên ảnh; video phải qua thêm bước ảnh sang video hoặc chuyển động.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://fal.ai/learn/tools/best-virtual-try-on-apis-2026
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** tháng phát hành chưa xác minh; API riêng của FASHN đã có tryon-max (mục riêng).

### 10. `fashn-tryon-max` — FASHN Try-On Max
- **Loại:** character · phát hành 2026-01 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `image.tryon`
- **Giới hạn:** 1K, 2K, 4K
- **Điểm mạnh:** tối đa 4K (thêm nấc độ phân giải tháng 3/2026).
- **Điểm yếu:** giá tính bằng tín dụng, các nguồn nói khác nhau.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://fashn.ai/changelog/api-try-on-max-endpoint-now-available
  - https://fashn.ai/changelog/new-resolution-tiers-and-generation-mode-controls
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** trong API ghi `model_name: tryon-max`.

### 11. `kling-kolors-tryon` — Kling Kolors Virtual Try-On v1.5
- **Loại:** character · phát hành 2025-06 · `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `image.tryon`
- **Điểm mạnh:** giữ được tư thế, màu da và vóc dáng người mẫu; có giấy phép thương mại.
- **Điểm yếu:** cho kết quả tốt nhất khi ảnh người mẫu chính diện và ảnh trang phục trải phẳng sạch.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://fal.ai/learn/tools/best-virtual-try-on-apis-2026
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** tháng phát hành là ước tính; 2026-09-15 ra thử đồ 3.0 (`kling-virtual-tryon-3`), tham số cũ vẫn dùng được.

### 12. `kling-virtual-tryon-3` — Kling Virtual Try-On 3.0
- **Loại:** character · phát hành 2026-09 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `image.tryon`
- **Điểm mạnh:**
  - Khuôn mặt nhất quán và chất lượng hình ảnh tốt hơn bản cũ; ảnh trải phẳng, ảnh mannequin, ảnh mặc sẵn đều dùng làm đầu vào trang phục được.
  - Có thể khóa tư thế, giữ mặt, giữ hoặc bỏ phông nền gốc.
- **Điểm yếu:** giá và độ phân giải chưa được nhà cung cấp công bố.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:** https://kling.ai/document-api/updates/api.md
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** cùng đợt còn có hai API: sao chép trang phục (sinh video người mẫu cho quần áo của mình theo video viral, 2026-08-18) và video quảng cáo bán hàng có lời thoại (2026-09-07).

### 13. `heygen-avatar-v` — HeyGen Avatar V
- **Loại:** character · phát hành 2026-04 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `avatar.audio_driven`, `lipsync.redub`, `audio.tts`, `audio.voice_clone`
- **Giới hạn:** âm thanh tối đa 600 giây; 720p
- **Điểm mạnh:**
  - Tạo người ảo từ một video tham chiếu; đổi cảnh, đổi trang phục vẫn giữ ngoại hình; một cảnh tối đa 30 phút.
  - Có thể chỉ đạo động tác bằng ngôn ngữ đời thường (Custom Motion / motion_prompt); nền tảng hỗ trợ hơn 177 ngôn ngữ.
- **Điểm yếu:**
  - Độ phân giải đầu ra chưa được nêu rõ (API mặc định 720p).
  - Người dùng phản ánh tác vụ thất bại vẫn bị trừ điểm.
- **Chi phí:** `usd_per_s` 0.05 (giá API của Avatar V).
- **Giấy phép:** cho phép thương mại; người ảo tự tạo cần xác thực ủy quyền của chính chủ.
- **Nguồn:**
  - https://www.heygen.com/research/avatar-v-model
  - https://developers.heygen.com/changelog
  - https://developers.heygen.com/docs/usage-limits.md
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 14. `synthesia-express-3` — Synthesia Express-3
- **Loại:** character · phát hành 2026-07 · `ga`
- **Truy cập:** app
- **Năng lực:** `avatar.audio_driven`, `audio.tts`
- **Điểm mạnh:** cử chỉ đi theo kịch bản; render nhanh khoảng 2 lần; nền tảng hỗ trợ hơn 140 ngôn ngữ.
- **Điểm yếu:**
  - Cảm xúc tự suy từ kịch bản, không chỉnh tay được.
  - Chỉ mở cho thư viện người ảo mới; chưa rõ có API hay không.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://www.synthesia.io/post/synthesia-launches-new-ai-assistant-for-faster-video-creation-and-express-3-avatar-model
  - https://www.synthesia.io/updates/express-3
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 15. `mirage-avatar-x` — Mirage Avatar X (trước đây là Captions)
- **Loại:** character · phát hành 2026-07 · `ga`
- **Truy cập:** app, api-aggregator
- **Năng lực:** `avatar.audio_driven`, `audio.tts`, `audio.voice_clone`
- **Giới hạn:** âm thanh 3–180 giây
- **Điểm mạnh:** nhà cung cấp cho biết chi tiết biểu cảm và giao tiếp bằng mắt tốt; giọng nói, biểu cảm, động tác được tạo cùng một lúc; hỗ trợ cả ngang và dọc.
- **Điểm yếu:**
  - Trên fal là 0.30 USD/giây, đắt nhất trong nhóm.
  - Không có prompt động tác; danh sách ngôn ngữ chưa công bố.
- **Chi phí:** `usd_per_s` 0.3 (giá niêm yết fal).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:**
  - https://captions.ai/blog/mirage-avatar-x
  - https://fal.ai/mirage-avatar-x
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 16. `longcat-video-avatar-1.5` — LongCat-Video-Avatar-1.5
- **Loại:** character · phát hành 2026-05 · `ga`
- **Truy cập:** open-weights
- **Năng lực:** `avatar.audio_driven`
- **Giới hạn:** 480p, 720p
- **Điểm mạnh:** giấy phép MIT mã nguồn mở; đối thoại nhiều người (nhiều luồng âm thanh); có thể điều khiển nhân vật anime và động vật; là phiên bản kế tiếp của InfiniteTalk / MultiTalk.
- **Điểm yếu:** video dài có động tác lặp lại; hiệu quả khác nhau giữa các ngôn ngữ; không có API lưu trữ chính thức.
- **Giấy phép:** cho phép thương mại (MIT).
- **Nguồn:**
  - https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5
  - https://github.com/MeiGen-AI/InfiniteTalk
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 17. `creatify-aurora` — Creatify Aurora
- **Loại:** character · `ga`
- **Truy cập:** app, api-aggregator
- **Năng lực:** `avatar.audio_driven`
- **Giới hạn:** 480p, 720p
- **Điểm mạnh:** một ảnh cộng âm thanh ra video người dẫn; prompt điều khiển được khung hình, phông nền, ánh sáng, ánh nhìn và việc cơ thể có giữ yên hay không.
- **Điểm yếu:** tối đa 720p.
- **Chi phí:** `usd_per_s` 0.07 (fal: 480p 0.07; 720p 0.14 USD/giây).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:** https://fal.ai/models/fal-ai/creatify/aurora/llms.txt
- **Xác minh:** 2026-11-12 (bên thứ ba) · **Độ tin cậy:** low

### 18. `veed-fabric-1.0` — VEED Fabric 1.0 (gồm Fast)
- **Loại:** character · phát hành 2025-09 · `ga`
- **Truy cập:** app, api-aggregator
- **Năng lực:** `avatar.audio_driven`
- **Giới hạn:** âm thanh tối đa 300 giây; 480p, 720p
- **Điểm mạnh:** một ảnh cộng âm thanh, tối đa 5 phút.
- **Điểm yếu:** tối đa 720p; năm 2026 chưa có phiên bản mới.
- **Chi phí:** `usd_per_s` 0.08 (fal 0.08–0.15 USD/giây).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:** https://fal.ai/veed-fabric-1.0
- **Xác minh:** 2026-11-12 (bên thứ ba) · **Độ tin cậy:** low

### 19. `hedra-omnia` — Hedra Omnia (Alpha)
- **Loại:** character · phát hành 2026-02 · `preview`
- **Truy cập:** app
- **Năng lực:** `avatar.audio_driven`
- **Giới hạn:** tối đa 8 giây; 540p, 720p, 1080p
- **Điểm mạnh:** khung đầu cộng âm thanh ra được diễn xuất; prompt có thể ghi chuyển động máy.
- **Điểm yếu:** hiện tối đa 8 giây, một lần khoảng 6 phút.
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:** https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** low
- **Ghi chú:** video nói dài của Hedra vẫn là Character-3 (2025-03).

### 20. `viggle-animate` — Viggle-Animate
- **Loại:** character · phát hành 2026-09 · `ga`
- **Truy cập:** app, open-weights
- **Năng lực:** `motion.transfer`, `video.edit_v2v`
- **Giới hạn:** 480x832
- **Điểm mạnh:** vẽ lại một khung của video điều khiển thành nhân vật mới, rồi cả đoạn đổi sang nhân vật đó.
- **Điểm yếu:**
  - Khẩu hình cận cảnh kém; nhiều người, tương tác gần hoặc khi cắt cảnh thì chất lượng giảm.
  - Khoảng 5 giây (124 khung).
- **Giấy phép:** commercial: conditional — trọng số theo MiniMax H3 Community License, mã nguồn Apache 2.0.
- **Nguồn:** https://viggle.ai/blog/viggle-animate-character-replacement-from-a-repainted-frame
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 21. `viggle-v4` — Viggle V4
- **Loại:** character · phát hành 2026-02 · `ga`
- **Truy cập:** app
- **Năng lực:** `motion.transfer`
- **Điểm mạnh:** cảnh nhiều người có thể đổi người theo từng track, tối đa 1 phút; Character Refine tạo 5 góc nhìn từ một ảnh.
- **Điểm yếu:** chưa công bố độ phân giải và giá.
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:** https://viggle.ai/blog/everything-you-need-is-in-viggle-v4
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 22. `dreamactor-m2.0` — DreamActor M2.0
- **Loại:** character · phát hành 2026-01 · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `motion.transfer`
- **Điểm mạnh:** một ảnh cộng video điều khiển để chuyển động, biểu cảm và khẩu hình.
- **Điểm yếu:** chưa tìm thấy thời điểm mở API và yêu cầu đầu vào.
- **Chi phí:** `usd_per_s` 0.05 (giá niêm yết BytePlus).
- **Giấy phép:** cho phép thương mại (điều khoản BytePlus).
- **Nguồn:**
  - https://www.byteplus.com/en/product/DreamActor/M20
  - https://docs.budgetpixel.com/api-reference/motion-control/motion-control-with-dreamactor-m20
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** low
- **Ghi chú:** tháng phát hành theo bài báo (arXiv 2601.21716).
