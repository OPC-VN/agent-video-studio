# Mô hình sinh / chỉnh sửa video
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/models/video.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

> **Ghi chú dịch:** `@<ảnh>N` và `@<video>N` là token tham chiếu trong prompt gửi Seedance/Jimeng. Ở bản gốc chúng viết bằng chữ Hán: `@` + hai ký tự U+56FE U+7247 + số cho ảnh, `@` + hai ký tự U+89C6 U+9891 + số cho video. Model chỉ nhận đúng ký tự gốc, nên khi ghép prompt thật phải dùng đúng mã này (xem chuỗi mẫu trong `rea_video/dance.py`).

Ghi chú chung của file nguồn: đặc tả đa số lấy từ thông báo nhà cung cấp hoặc tổng hợp bên thứ ba; các trường `status`, `verified`, `confidence` cho biết độ tin cậy. Đơn vị giá `usd_per_s` là giá niêm yết của bên thứ ba quy đổi, chỉ dùng làm mức tương đối khi định tuyến chi phí.

Chú thích viết tắt trong bảng: `t2v` = văn bản sang video; `i2v` = ảnh sang video; `first_frame` = khung đầu; `first_last` = khung đầu và khung cuối; `multi_reference` = nhiều ảnh tham chiếu; `reference_video` / `reference_audio` = video / âm thanh tham chiếu; `edit_v2v` = chỉnh sửa video sang video.

Tổng số mục: 36 mô hình (theo thứ tự trong file nguồn).

---

## Danh mục mô hình

| # | id | Tên | Nhà cung cấp | Trạng thái |
|---|---|---|---|---|
| 1 | `seedance-2.5` | Seedance 2.5 | ByteDance Seed | ga |
| 2 | `seedance-2.5-flash` | Seedance 2.5 Flash | ByteDance Seed | preview |
| 3 | `seedance-2.0` | Seedance 2.0 (gồm Mini / Fast) | ByteDance Seed | ga |
| 4 | `kling-4.0` | Kling 4.0 | Kuaishou | ga |
| 5 | `kling-4.0-flash` | Kling 4.0 Flash | Kuaishou | ga |
| 6 | `kling-3.0` | Kling 3.0 (gồm Turbo) | Kuaishou | ga |
| 7 | `kling-o3` | Kling O3 (Omni) | Kuaishou | ga |
| 8 | `veo-3.1` | Veo 3.1 (gồm Lite) | Google | ga |
| 9 | `grok-imagine-video-1.5` | Grok Imagine Video 1.5 | xAI | ga |
| 10 | `grok-imagine-video-1.5-lite` | Grok Imagine Video 1.5 Lite | xAI | ga |
| 11 | `gemini-omni-flash` | Gemini Omni Flash | Google | ga |
| 12 | `vidu-q3` | Vidu Q3 | Shengshu | ga |
| 13 | `vidu-q4-preview` | Vidu Q4 Preview | Shengshu | preview |
| 14 | `pixverse-v6` | PixVerse V6 | PixVerse | ga |
| 15 | `minimax-h3` | MiniMax H3 / H3 Max | MiniMax | ga |
| 16 | `minimax-h3-max` | MiniMax H3 Max | MiniMax | ga |
| 17 | `pika-h3-flex` | Pika H3 Flex | Pika | ga |
| 18 | `heygen-video-1` | HeyGen Video 1 | HeyGen | ga |
| 19 | `utopai-x` | Utopai X | Utopai Studios | ga |
| 20 | `p-video-2-pro` | P-Video-2-Pro | Pruna AI | ga |
| 21 | `hailuo-2.3` | Hailuo 2.3 / 2.3 Fast | MiniMax | ga |
| 22 | `wan-3.0` | Wan 3.0 | Alibaba | ga |
| 23 | `happyhorse-1.0` | HappyHorse 1.0 | Alibaba | ga |
| 24 | `wan-2.7-edit` | Wan 2.7 chỉnh sửa video | Alibaba | ga |
| 25 | `wan-2.2` | Wan 2.2 (mã nguồn mở, gồm TI2V-5B) | Alibaba | ga |
| 26 | `wan-vace` | Wan VACE (Wan 2.1 VACE / Wan2.2-VACE-Fun) | Alibaba | ga |
| 27 | `ltx-2.5` | LTX-2.5 (mã nguồn mở) | Lightricks | ga |
| 28 | `hunyuanvideo-1.5` | HunyuanVideo 1.5 (mã nguồn mở) | Tencent | ga |
| 29 | `skyreels-v4` | SkyReels V4 | Kunlun Skywork | ga |
| 30 | `runway-gen-4.5` | Runway Gen-4.5 (gồm Act-Two) | Runway | ga |
| 31 | `runway-aleph-2` | Runway Aleph 2 | Runway | ga |
| 32 | `higgsfield-genjutsu` | Higgsfield Genjutsu (gồm Lite) | Higgsfield | ga |
| 33 | `luma-ray3.2` | Luma Ray3.2 / Modify | Luma AI | ga |
| 34 | `flux-3-video` | FLUX 3 Video | Black Forest Labs | ga |
| 35 | `flux-3-video-max` | FLUX 3 Max (video) | Black Forest Labs | ga |
| 36 | `sora-2` | Sora 2 / Sora 2 Pro | OpenAI | shutdown |

---

## Chi tiết từng mô hình

### 1. `seedance-2.5` — Seedance 2.5
- **Nhà cung cấp / loại:** ByteDance Seed · video · phát hành 2026-07 · trạng thái `ga`
- **Truy cập:** app, api-aggregator
- **Năng lực (primitives):** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.multi_shot`, `video.extend`, `video.edit_v2v`, `video.camera_control`, `video.native_audio`
- **Giới hạn:** thời lượng tối đa 30 giây; độ phân giải 480p, 720p, 1080p; tham chiếu: ảnh 30, video 10, âm thanh 10
- **Không được đặt chung trong một yêu cầu (exclusive_inputs):** [khung đầu / khung đầu–cuối] và [nhiều tham chiếu / video tham chiếu / âm thanh tham chiếu]. Nhiều nhà cung cấp ghi nhận điều này; giao diện app Jimeng dùng "toàn năng tham chiếu" có thể dùng `@<ảnh>` làm khung đầu.
- **Âm thanh:** có sẵn (native: true)
- **Điểm mạnh:**
  - Một lần tối đa 30 giây, bên trong có nhiều cảnh quay mạch lạc về logic.
  - Một lần nhận được 30 ảnh + 10 video + 10 âm thanh tham chiếu; hỗ trợ clay render (mô hình 3D trắng không texture), chuyển động và tham chiếu sáng tạo.
  - Chỉnh sửa cục bộ theo mốc thời gian, thay phông xanh lá, đổi góc máy, nối tiếp kéo dài (có thể đến vài phút).
  - Là mô hình chủ lực của thương mại điện tử nội địa Trung Quốc để phục dựng sản phẩm (OiiOii, Hypit).
- **Điểm yếu:**
  - Nhà cung cấp thừa nhận tính hợp lý vật lý của chuyển động phức tạp và độ ổn định của tương tác nhiều chủ thể còn hạn chế.
  - Chưa công bố độ phân giải tối đa chính thức; kênh HypiHub của Hypit cung cấp 480p/720p/1080p.
- **Chi phí:** tham khảo thực tế: OiiOii phục dựng video thương mại điện tử 50 giây khoảng 40 nhân dân tệ (sinh 480p rồi siêu phân giải lên 1080p).
- **Giấy phép:** cho phép thương mại (có điều kiện theo điều khoản nền tảng).
- **Nguồn:**
  - https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
  - https://github.com/hypit-ai/hypit/blob/main/packages/provider-hypihub/README.md
  - https://docs.byteplus.com/docs/en/modelark/seedance-2-5.md
  - https://apiframe.ai/docs/videos/seedance/seedance-2-5
- **Xác minh:** 2026-11-11 (căn cứ: nhà cung cấp) · **Độ tin cậy:** high

### 2. `seedance-2.5-flash` — Seedance 2.5 Flash
- **Loại:** video · phát hành 2026-11 · trạng thái `preview`
- **Truy cập:** app, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.native_audio`
- **Giới hạn:** độ phân giải 480p, 720p
- **Không được đặt chung (exclusive_inputs):** [khung đầu / khung đầu–cuối] và [tư liệu tham chiếu]. Đây là suy luận từ Seedance 2.5; Flash không có mô tả riêng.
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Rẻ hơn Seedance 2.5 khoảng một phần ba, nhanh gấp khoảng hai lần; phù hợp để dựng bản nháp.
  - Giống 2.5, có hai chế độ: khung đầu–cuối và toàn năng tham chiếu.
- **Điểm yếu:**
  - Tối đa 720p.
  - Giới hạn thời lượng và số lượng tham chiếu chưa được nhà cung cấp công bố; không nên áp dụng nguyên con số của 2.5.
- **Chi phí:** khoảng 0.152 USD/giây ở 720p (một nguồn duy nhất).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức; theo điều khoản nền tảng.
- **Nguồn:**
  - https://dreamina.capcut.com/seedance/seedance-2-5-flash
  - https://cellcog.ai/blog/seedance-2-5-flash/
- **Xác minh:** 2026-11-12 (căn cứ: bên thứ ba) · **Độ tin cậy:** low
- **Ghi chú:** Jimeng đã ra mắt; API Ark được cho là mở ngày 2026-11-15 (mã mô hình `dreamina-seedance-2-5-flash-261115`). Ngày API và giá chỉ có một nguồn.

### 3. `seedance-2.0` — Seedance 2.0 (gồm Mini / Fast)
- **Loại:** video · phát hành 2026-02 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.multi_shot`, `video.native_audio`, `video.edit_v2v`
- **Giới hạn:** thời lượng 4–15 giây; độ phân giải 720p, 1080p; tham chiếu: ảnh 9, video 3, âm thanh 3; tổng độ dài video tham chiếu tối đa 15 giây
- **Không được đặt chung (exclusive_inputs):** [khung đầu / khung đầu–cuối] và [tư liệu tham chiếu]. Giao diện app Jimeng "toàn năng tham chiếu" có thể dùng `@<ảnh>` làm khung đầu.
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Chi phí thấp; bản Mini 720p được Hypit dùng làm nguồn chính cho A-roll / B-roll (tổng chi phí một video khoảng 1.1 USD).
  - Một lần có thể ra nhiều cảnh: viết trong prompt theo số thứ tự cảnh (không hỗ trợ mốc thời gian theo từng cảnh).
- **Điểm yếu:**
  - Thời lượng một lần ngắn hơn 2.5; tổng độ dài video tham chiếu và âm thanh tham chiếu mỗi loại không quá 15 giây.
- **Chi phí:** `usd_per_s` 0.15 (giá niêm yết bên thứ ba khoảng 9.07 USD/phút).
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://tech-insider.org/best-ai-video-generator-2026/
  - https://en.wikipedia.org/wiki/Seedance_2.0
  - https://github.com/hypit-ai/hypit
  - https://dev.runwayml.com/learn/seedance-2-0-api
  - https://ofox.ai/docs/develop/models/seedance
  - https://evolink.ai/docs/en/api-manual/video-series/seedance2.0/seedance-2.0-overview
- **Xác minh:** 2026-11-11 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium

### 4. `kling-4.0` — Kling 4.0
- **Loại:** video · phát hành 2026-10 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.keyframes`, `video.multi_reference`, `video.reference_video`, `video.multi_shot`, `video.edit_v2v`, `video.camera_control`, `video.native_audio`
- **Giới hạn:** thời lượng 3–30 giây; độ phân giải 720p, 1080p, 4K; tham chiếu: ảnh 10, video 5, âm thanh 1, tổng 15; prompt tối đa 8000 token; keyframe tối đa 10
- **Âm thanh:** có sẵn; có tham chiếu giọng nói (voice_ref: true)
- **Điểm mạnh:**
  - Khung đầu–cuối cùng tối đa 10 keyframe: kiểm soát được chuyển động máy phức tạp và trạng thái trung gian.
  - Omni Reference tối đa 15 tham chiếu (10 ảnh, 5 đoạn video tổng 30 giây, 7 "element").
  - Chỉnh sửa video: thay biểu cảm, cơ thể, góc máy, phong cách, phông nền, nhân vật (tối đa 5 đoạn đầu vào, tổng 30 giây).
  - Âm thanh nổi, lời thoại đa ngôn ngữ và giọng vùng miền; chữ trên màn hình hỗ trợ đa ngôn ngữ và emoji.
  - Tỷ lệ khung 21:9 / 16:9 / 1:1 / 9:16.
  - Mặc định tự chia cảnh; thời điểm từng cảnh được viết trực tiếp trong prompt.
- **Điểm yếu:**
  - HDR 10-bit và nối tiếp (tối đa 2 phút) chưa ra mắt.
  - Tham chiếu âm thanh chỉ dùng làm tham chiếu giọng nói.
- **Chi phí:** `usd_per_s` 0.235 (giá niêm yết fal: 720p 0.157; 1080p 0.235 USD/giây; giá API chính thức chưa công bố).
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://fal.ai/learn/tools/what-is-kling-4-0
  - https://kling.ai/quickstart/kling-4-model-user-guide
  - https://kling.ai/document-api/updates/api.md
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** ứng dụng chính thức ra mắt 2026-10-15; API chính thức mở toàn bộ 2026-10-28. Nối tiếp (tối đa 2 phút) và HDR 10-bit vẫn ở trạng thái "sắp ra mắt". Bản Flash tách thành mục riêng (`kling-4.0-flash`).

### 5. `kling-4.0-flash` — Kling 4.0 Flash
- **Loại:** video · phát hành 2026-09 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.multi_shot`, `video.native_audio`
- **Giới hạn:** thời lượng 3–20 giây; 720p; prompt tối đa 8000 token
- **Âm thanh:** có sẵn; có tham chiếu giọng nói (voice_ref: true)
- **Điểm mạnh:**
  - Rẻ, ra nhanh, phù hợp để dựng bản nháp; cách dùng ảnh tham chiếu, video tham chiếu và tham chiếu giọng nói giống 4.0.
  - Mặc định tự chia cảnh; âm thanh nổi.
- **Điểm yếu:**
  - Chỉ 720p, 8-bit SDR.
  - Không hỗ trợ khung đầu–cuối và nhiều keyframe; bố cục chỉ khóa được bằng khung đầu hoặc ảnh tham chiếu.
- **Chi phí:** `usd_per_s` 0.094 (giá niêm yết bên thứ ba).
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://kling.ai/quickstart/kling-4-model-user-guide
  - https://kling.ai/document-api/updates/api.md
  - https://www.llmreference.com/model/kling-4.0-flash
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** mở giới hạn số lượng từ 2026-09-28; API chính thức mở 2026-11-04. Chưa xác nhận giới hạn số tài liệu tham chiếu có giống 4.0 không.

### 6. `kling-3.0` — Kling 3.0 (gồm Turbo)
- **Loại:** video · phát hành 2026-02 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.multi_shot`, `video.camera_control`, `video.native_audio`
- **Giới hạn:** thời lượng 3–15 giây; độ phân giải 720p, 1080p, 4K; tối đa 6 cảnh mỗi lần sinh
- **Âm thanh:** có sẵn; có tham chiếu giọng nói (voice_ref: true)
- **Điểm mạnh:**
  - Tối đa 6 cảnh trong một lần; khung bắt đầu cộng ảnh tham chiếu giúp giữ kiểu dáng và đường nét nhân vật.
  - Voice ID giữ giọng nhân vật xuyên các cảnh; xử lý tốt vật lý phức tạp, chuyển động nhanh và chuyển máy.
  - Turbo Pro cải thiện khẩu hình và nhiều cảnh.
- **Điểm yếu:** giá API khá cao.
- **Chi phí:** `usd_per_s` 0.34 (720p khoảng 15.12 USD/phút; 1080p khoảng 20.16 USD/phút; giá niêm yết bên thứ ba).
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://help.artlist.io/hc/en-us/articles/37026869403933-Kling-3-Model-Family
  - https://tech-insider.org/best-ai-video-generator-2026/
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium

### 7. `kling-o3` — Kling O3 (Omni)
- **Loại:** video · phát hành 2026-03 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.multi_shot`, `video.edit_v2v`, `video.reference_video`
- **Giới hạn:** thời lượng 3–15 giây; độ phân giải 720p, 1080p, 4K
- **Âm thanh:** không (native: false)
- **Điểm mạnh:**
  - Chỉnh sửa video sang video: đổi nhân vật hoặc đạo cụ, tạo lại phong cách, chiếu sáng lại, giữ nguyên chuyển động gốc.
  - Nhất quán tham chiếu Element mạnh hơn; Director Mode kết hợp được văn bản, khung đầu–cuối, ảnh tham chiếu và video nhân vật.
- **Điểm yếu:** chỉnh sửa cho kết quả tốt hơn trên đoạn ngắn.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:** https://help.artlist.io/hc/en-us/articles/37026869403933-Kling-3-Model-Family
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** tháng phát hành là ước tính; tài liệu về âm thanh không đề cập.

### 8. `veo-3.1` — Veo 3.1 (gồm Lite)
- **Loại:** video · phát hành 2025-10 · trạng thái `ga`
- **Truy cập:** app, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.multi_shot`, `video.extend`, `video.native_audio`
- **Giới hạn:** thời lượng 4–8 giây; độ phân giải 720p, 1080p, 4K; tham chiếu ảnh 4
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Bám prompt tốt và người thật tự nhiên; hướng doanh nghiệp (GCP, SLA, SynthID).
  - Hỗ trợ khung đầu–cuối; Ingredients to Video hỗ trợ tham chiếu nhân vật, vật thể, phông nền hoặc phong cách (chỉ 8 giây; số lượng ảnh tham chiếu theo bên thứ ba là 3–4 ảnh).
  - Biến thể Extend riêng có thể thêm 7 giây cho video 2–30 giây.
- **Điểm yếu:**
  - Mỗi đoạn chỉ 4/6/8 giây.
  - Giá cao nhất trong nhóm.
- **Chi phí:** `usd_per_s` 0.40 (Lite khoảng 0.08 USD/giây).
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://tech-insider.org/best-ai-video-generator-2026/
  - https://templix.app/blogs/best-ai-motion-control-and-animation-models-in-2026
  - https://help.artlist.io/hc/en-us/articles/33139656414877-Veo-3-1
  - https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate
  - https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
  - https://aistudio.google.com/docs/deprecations
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** bản xem trước của Gemini API (gồm Lite) ngừng hoạt động 2026-10-22; nhà cung cấp khuyến nghị chuyển sang `gemini-omni-1.2-flash`. Bản chính thức `veo-3.1-generate-001` trên Vertex AI chưa có ngày ngừng. Lite ra mắt 2026-03-31, chỉ có văn bản sang video và ảnh sang video, 720p / 1080p; trong một đoạn có thể viết nhiều cảnh theo mốc thời gian.

### 9. `grok-imagine-video-1.5` — Grok Imagine Video 1.5
- **Loại:** video · phát hành 2026-06 · trạng thái `ga`
- **Truy cập:** app, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.keyframes`, `video.multi_reference`, `video.reference_audio`, `video.native_audio`
- **Giới hạn:** thời lượng 1–15 giây; 720p, 1080p; tham chiếu: ảnh 14, âm thanh 3; keyframe 4
- **Âm thanh:** có sẵn; có tham chiếu giọng nói
- **Điểm mạnh:**
  - Khung đầu, khung cuối và keyframe trung gian có thể đặt cùng một yêu cầu với ảnh tham chiếu.
  - Tối đa 14 ảnh tham chiếu; 9 tỷ lệ khung (gồm 21:9, 5:2).
- **Điểm yếu:**
  - Tạo video từ tham chiếu tối đa 720p.
  - Tham chiếu giọng nói chỉ chọn được 3 giọng dựng sẵn; âm thanh tùy chỉnh chỉ mở cho đối tác.
- **Chi phí:** `usd_per_s` 0.08.
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức; theo điều khoản nền tảng.
- **Nguồn:**
  - https://docs.x.ai/developers/model-capabilities/video/generation
  - https://docs.x.ai/developers/model-capabilities/video/reference-to-video
  - https://docs.x.ai/docs/models
  - https://www.techtimes.com/articles/318635/20260618/grok-imagine-video-15-goes-live-xai-tops-ai-video-leaderboard-86-percent-below-sora.htm
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành chính thức 2026-06-16; 2026-07-31 thêm văn bản sang video. Keyframe căn theo 1/3 giây và phải nằm bên trong đoạn; khung của ảnh sang video theo ảnh đầu vào.

### 10. `grok-imagine-video-1.5-lite` — Grok Imagine Video 1.5 Lite
- **Loại:** video · phát hành 2026-10 · trạng thái `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.native_audio`
- **Giới hạn:** thời lượng 1–15 giây; 480p, 720p, 1080p
- **Âm thanh:** có sẵn
- **Điểm mạnh:** là mức rẻ nhất của xAI; theo nhà cung cấp, phù hợp với video đơn giản.
- **Điểm yếu:** chỉ nhận khung đầu; không có khung cuối và ảnh tham chiếu; 1080p là phóng đại từ 720p.
- **Chi phí:** `usd_per_s` 0.02 (giá niêm yết bên thứ ba: 480p 0.02; 720p 0.03; 1080p 0.14 USD/giây).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:**
  - https://docs.x.ai/docs/models
  - https://runware.ai/docs/models/xai-grok-imagine-video-1-5-lite.md
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** low

### 11. `gemini-omni-flash` — Gemini Omni Flash
- **Loại:** video · phát hành 2026-05 · trạng thái `ga`
- **Truy cập:** app, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.multi_shot`, `video.extend`, `video.edit_v2v`, `video.camera_control`, `video.native_audio`
- **Giới hạn:** thời lượng 3–15 giây; 720p, 1080p, 4K; tham chiếu ảnh 6
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Nhận đầu vào tự do là văn bản, ảnh, âm thanh, video; phác thảo có thể làm hướng dẫn chuyển động.
  - Chỉnh sửa nhiều lượt bằng hội thoại; trạng thái cảnh được giữ liên tục, không bị đặt lại.
  - Theo bảng xếp hạng bên thứ ba, đứng đầu về văn bản sang video (có âm thanh) (Elo khoảng 1233).
- **Điểm yếu:**
  - Mỗi đoạn 3–15 giây; khung đầu–cuối và nối tiếp mỗi lần 3–10 giây.
  - Mặc định tự cắt cảnh; muốn một cảnh duy nhất phải nói rõ trong prompt.
  - Không nhận âm thanh tham chiếu.
  - Tính nhất quán vật lý còn khuyết điểm.
  - Đầu ra có nhãn SynthID và C2PA.
- **Chi phí:** `usd_per_s` 0.10.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://www.datacamp.com/blog/gemini-omni
  - https://tech-insider.org/best-ai-video-generator-2026/
  - https://aistudio.google.com/docs/omni
  - https://aistudio.google.com/docs/changelog
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-05-19 (Gemini App, Flow); API phiên bản 1.1 chính thức 2026-08-27 (thêm nối tiếp, khung đầu–cuối, 4K); phiên bản 1.2 ngày 2026-11-05 (tối đa 15 giây, tối đa 6 ảnh tham chiếu, giảm giá 30%); từ 2026-12-03 yêu cầu của 1.1 được chuyển sang 1.2. ID API hiện tại: `gemini-omni-1.2-flash`. Omni Pro chưa phát hành.

### 12. `vidu-q3` — Vidu Q3
- **Loại:** video · phát hành 2026-04 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.multi_reference`, `video.native_audio`
- **Giới hạn:** tối đa 16 giây
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Reference-to-Video tập trung vào nhất quán nhiều chủ thể: chủ thể, môi trường, trang phục, đạo cụ, phong cách đều có thể làm tham chiếu.
  - Âm thanh gốc gồm âm môi trường, âm chuyển động, Foley, âm cảm xúc; tích hợp 6 loại hiệu ứng (hạt, chất lỏng, chuyển cảnh...).
- **Điểm yếu:** số lượng tham chiếu và độ phân giải chưa công khai.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:** https://www.kosmo.com.my/2026/04/13/shengshu-launches-vidu-q3-reference-to-video-with-expanded-visual-and-audio-capabilities/
- **Xác minh:** 2026-10-29 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium

### 13. `vidu-q4-preview` — Vidu Q4 Preview
- **Loại:** video · phát hành 2026-10 · trạng thái `preview`
- **Truy cập:** app, api
- **Năng lực:** `video.i2v_first_frame`, `video.multi_reference`, `video.reference_audio`, `video.multi_shot`, `video.native_audio`
- **Giới hạn:** thời lượng 3–16 giây; 540p, 720p, 1080p, 2K, 4K; tham chiếu: ảnh 15, âm thanh 3
- **Âm thanh:** có sẵn; có tham chiếu giọng nói
- **Điểm mạnh:**
  - Diễn xuất và khẩu hình tự nhiên; lời thoại và âm thanh được tạo cùng lúc; tối đa 4K, 2K/4K là 10-bit.
  - Reference-to-Video tối đa 15 ảnh tham chiếu cộng 3 đoạn tham chiếu giọng nói, giữ ngoại hình nhân vật và giọng.
  - Tự động cắt cảnh.
- **Điểm yếu:**
  - Không có văn bản sang video và khung đầu–cuối: chỉ có ảnh sang video (một ảnh) và tạo từ tham chiếu.
  - Bản xem trước, thông số có thể đổi; chưa hỗ trợ gọi thư viện chủ thể.
- **Chi phí:** `usd_per_s` 0.045 (thông cáo báo 540p từ 0.045 USD/giây, 4K 0.39 USD/giây; trong nước từ 0.09 nhân dân tệ/giây).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:**
  - https://platform.vidu.com/docs/api-reference/video-models/vidu-q4-preview/image-to-video
  - https://platform.vidu.com/docs/api-reference/video-models/vidu-q4-preview/reference-to-video
  - https://www.chinatechnews.com/2026/10/08/130490-shengshu-technology-launches-vidu-q4-preview-a-next-generation-ai-video-model-built-for-lifelike-performances
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** tên mô hình trong API: `viduq4-preview`.

### 14. `pixverse-v6` — PixVerse V6
- **Loại:** video · phát hành 2026-03 · trạng thái `ga`
- **Truy cập:** app, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.multi_shot`, `video.camera_control`, `video.native_audio`
- **Giới hạn:** tối đa 15 giây; 1080p
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Hơn 20 tham số ống kính (tiêu cự, khẩu độ, độ sâu trường ảnh, méo hình, quang sai màu, tối góc), phù hợp để phục dựng cảnh có "cảm giác ống kính" nhất định.
  - Nhiều cảnh; Hypit đã tích hợp (hỗ trợ video tham chiếu và khung đầu–cuối qua HypiHub).
- **Điểm yếu:** qua HypiHub, tham số seed và multi-clip không dùng được.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://wavespeed.ai/blog/posts/pixverse-v6-ai-video-camera-control-vfx-2026/
  - https://github.com/hypit-ai/hypit/blob/main/packages/provider-hypihub/README.md
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium

### 15. `minimax-h3` — MiniMax H3 / H3 Max
- **Loại:** video · phát hành 2026-07 · trạng thái `ga`
- **Truy cập:** api, api-aggregator, open-weights
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.multi_shot`, `video.native_audio`
- **Giới hạn:** thời lượng 4–15 giây; 768p, 1080p, 2K
- **Không được đặt chung (exclusive_inputs):** [khung đầu / khung đầu–cuối] và [tư liệu tham chiếu] — không cùng một yêu cầu.
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Đứng thứ ba trong bảng xếp hạng bên thứ ba (H3 Max Elo khoảng 1227) và có giá niêm yết thấp nhất.
  - Trọng số mở (H3-Base chạy cục bộ được 768p).
  - Hypit và video-replicate-studio đều đã tích hợp.
  - Một lần có thể ra nhiều cảnh: trong prompt viết theo `[Shot N]` kèm thời điểm chuyển cảnh.
- **Điểm yếu:**
  - Hỗ trợ doanh nghiệp yếu; ở 1080p thời lượng bị giới hạn.
  - 2K cần mô-đun lưu trữ.
- **Chi phí:** `usd_per_s` 0.04 (H3 Max khoảng 2.40 USD/phút; H3 khoảng 7.80 USD/phút).
- **Giấy phép:** commercial: conditional — MiniMax H3 Community License.
- **Nguồn:**
  - https://tech-insider.org/best-ai-video-generator-2026/
  - https://www.turingpost.com/p/6-opensource-video-generation-models
  - https://huggingface.co/MiniMaxAI/MiniMax-H3/raw/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md
  - https://platform.minimax.io/docs/api-reference/video-generation-v2-create
  - https://minimax.io/blog/minimax-h3
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** blog chính thức ra mắt 2026-07-31; trọng số mở 2026-08-03, chỉ có bản cơ bản 768p; mô-đun 2K chỉ đi qua API. Cùng một giao diện còn có hai bản H3 Highspeed và H3 Lite; H3 Max tách thành mục riêng.

### 16. `minimax-h3-max` — MiniMax H3 Max
- **Loại:** video · phát hành 2026-08 · trạng thái `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.native_audio`
- **Giới hạn:** thời lượng 5–15 giây; 480p, 768p; tham chiếu: ảnh 9, video 3, âm thanh 3
- **Không được đặt chung (exclusive_inputs):** [khung đầu / khung cuối] và [tư liệu tham chiếu]; video và âm thanh chỉ dùng được ở chế độ tham chiếu.
- **Âm thanh:** có sẵn; có tham chiếu giọng nói
- **Điểm mạnh:**
  - Là bản nhanh của H3 (tên là Max nhưng tài liệu API ghi là chế độ sinh nhanh); nhà cung cấp cho biết đoạn 5 giây ra trong khoảng 3 giây.
  - Dùng được ảnh, video, âm thanh tham chiếu; có thể tắt mở rộng prompt.
- **Điểm yếu:**
  - Tối đa 768p, không có 2K; không tạo được đoạn 4 giây.
  - Liên kết kết quả hết hạn sau 24 giờ.
- **Chi phí:** `usd_per_s` 0.08 (giá niêm yết fal: 768p 0.08; 480p 0.05 USD/giây).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:**
  - https://platform.minimax.io/docs/api-reference/video-generation-v2-create
  - https://www.orcarouter.ai/blog/h3-max-fal-speed-debut
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** hợp tác với fal để huấn luyện; ra mắt trên fal 2026-08-27 (`minimax/h3-max`, còn gọi là H3 Max by fal, lên được 1080p); đầu tháng 9 chuyển sang API riêng của MiniMax. Chưa xác nhận có hỗ trợ nhiều cảnh trong một lần không.

### 17. `pika-h3-flex` — Pika H3 Flex
- **Loại:** video · phát hành 2026-10 · trạng thái `ga`
- **Truy cập:** app, api, open-weights
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.multi_shot`, `video.edit_v2v`, `video.native_audio`
- **Giới hạn:** thời lượng 3–15 giây; 480p, 768p; tham chiếu: ảnh 9, video 3, âm thanh 3, tổng 12
- **Âm thanh:** có sẵn; có tham chiếu giọng nói; có thể xuất riêng âm thanh thành track
- **Điểm mạnh:**
  - Rẻ, nhanh (lấy mẫu 6 bước); có thể xuất riêng track âm thanh.
  - Tài liệu hướng dẫn prompt rất chi tiết; ảnh, video, âm thanh tham chiếu đều dùng được.
- **Điểm yếu:**
  - Gốc chỉ có 480p / 768p; độ phân giải cao hơn nhờ bộ phóng đại do Pika lưu trữ.
  - Phần mở là adapter khoảng 2 GB; mô hình nền khoảng 210 GB.
- **Chi phí:** `usd_per_s` 0.04 (768p 0.04 USD/giây; 480p 0.02; 1080p 0.07; 4K 0.16 — giảm nửa giá khi mới phát hành).
- **Giấy phép:** commercial: conditional — huấn luyện lại dựa trên MiniMax H3; giấy phép theo điều khoản nền tảng và MiniMax H3 Community License.
- **Nguồn:**
  - https://pika.art/blog/pika-h3-flex
  - https://pika.art/pika-h3-flex
  - https://pika.art/learn/pika-h3-flex-prompt-guide
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** huấn luyện lại dựa trên MiniMax H3; phát hành 2026-10-29, vào Pika App 2026-11-02; chỉ có tham chiếu âm thanh là không đủ, phải có ít nhất một ảnh hoặc một đoạn video.

### 18. `heygen-video-1` — HeyGen Video 1
- **Loại:** video · phát hành 2026-09 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.native_audio`
- **Giới hạn:** thời lượng 5–30 giây; 480p, 768p, 1080p, 2K; tham chiếu: ảnh 9, video 3, âm thanh 3, tổng 15
- **Không được đặt chung (exclusive_inputs):** [khung đầu / khung đầu–cuối] và [tư liệu tham chiếu]. Khung cuối chỉ có ở chế độ ảnh sang video; tư liệu tham chiếu chỉ có ở chế độ tham chiếu.
- **Âm thanh:** có sẵn; có tham chiếu giọng nói
- **Điểm mạnh:**
  - Đứng cao trên bảng xếp hạng (Artificial Analysis: ảnh sang video thứ 6, văn bản sang video thứ 7).
  - Prompt tối đa 16000 ký tự; mỗi lần tối đa 30 giây.
- **Điểm yếu:** mặc định 768p; trên 15 giây phải bật tăng cường prompt.
- **Chi phí:** `usd_per_s` 0.03 (768p, giá niêm yết bên thứ ba).
- **Giấy phép:** commercial: conditional — huấn luyện lại dựa trên MiniMax H3; theo điều khoản nền tảng và MiniMax H3 Community License.
- **Nguồn:**
  - https://developers.heygen.com/reference/create-heygen-video.md
  - https://help.heygen.com/en/articles/17272995-introducing-heygen-video-generate-cinematic-clips-from-a-prompt
  - https://openrouter.ai/heygen/heygen-video-1
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** huấn luyện lại dựa trên MiniMax H3; phát hành 2026-09-30; ở 1080p / 2K, chế độ văn bản và tham chiếu chỉ được tỷ lệ 16:9 hoặc 9:16.

### 19. `utopai-x` — Utopai X
- **Loại:** video · phát hành 2026-09 · trạng thái `ga`
- **Truy cập:** app
- **Năng lực:** `video.t2v`, `video.native_audio`
- **Điểm mạnh:** xếp thứ 2 trong Artificial Analysis ở cả văn bản sang video và ảnh sang video.
- **Điểm yếu:** chỉ dùng được trong PAI App, không có API công khai; thông số chưa công bố.
- **Giấy phép:** commercial: conditional — huấn luyện lại dựa trên MiniMax H3; theo điều khoản nền tảng và MiniMax H3 Community License.
- **Nguồn:** https://www.utopaistudios.com/en/pai/utopai-x
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** low
- **Ghi chú:** huấn luyện lại dựa trên MiniMax H3.

### 20. `p-video-2-pro` — P-Video-2-Pro
- **Loại:** video · phát hành 2026-10 · trạng thái `ga`
- **Truy cập:** api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.native_audio`
- **Giới hạn:** thời lượng 5–15 giây; 480p, 768p
- **Âm thanh:** có sẵn
- **Điểm mạnh:** rất rẻ; có hai chế độ tốc độ và chất lượng.
- **Điểm yếu:** tối đa 768p.
- **Chi phí:** `usd_per_s` 0.01 (0.01–0.075 USD/giây tùy độ phân giải và chế độ).
- **Giấy phép:** commercial: conditional — huấn luyện lại dựa trên MiniMax H3; theo điều khoản nền tảng và MiniMax H3 Community License.
- **Nguồn:**
  - https://replicate.com/prunaai/p-video-2-pro
  - https://runware.ai/docs/models/prunaai-p-video-2-pro.md
- **Xác minh:** 2026-11-12 (căn cứ: bên thứ ba) · **Độ tin cậy:** low
- **Ghi chú:** dựa trên MiniMax H3.

### 21. `hailuo-2.3` — Hailuo 2.3 / 2.3 Fast
- **Loại:** video · phát hành 2025-10 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`
- **Giới hạn:** tối đa 10 giây; 768p, 1080p
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Cải thiện vi biểu cảm, phong cách hóa, chuyển động.
  - Rẻ (bản Fast 768p 6 giây khoảng 0.19 USD trở lên).
- **Điểm yếu:**
  - Ở 1080p thời lượng ngắn hơn.
  - Generation thất bại vẫn bị tính phí.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:** https://tech-insider.org/best-ai-video-generator-2026/
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium

### 22. `wan-3.0` — Wan 3.0 (Vạn Tượng)
- **Loại:** video · phát hành 2026-08 · trạng thái `ga`
- **Truy cập:** api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.multi_reference`, `video.reference_video`, `video.reference_audio`, `video.multi_shot`, `video.native_audio`
- **Giới hạn:** thời lượng 2–30 giây; 480p, 720p, 1080p; tham chiếu: ảnh 10, video 5, âm thanh 5
- **Không được đặt chung (exclusive_inputs):** [khung đầu / khung đầu–cuối] và [tư liệu tham chiếu]
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Đứng thứ hai trên bảng xếp hạng bên thứ ba (Elo khoảng 1229).
  - Một lần có thể ra nhiều cảnh: viết theo "cảnh thứ N [giây bắt đầu-kết thúc]", mỗi đoạn 2–5 giây.
  - Dùng được ảnh, video, âm thanh tham chiếu (giọng).
- **Điểm yếu:** chỉ có API, không mã nguồn mở.
- **Chi phí:** `usd_per_s` 0.20 (1080p khoảng 0.20 USD/giây; 720p 0.10; 480p 0.05).
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://tech-insider.org/best-ai-video-generator-2026/
  - https://help.aliyun.com/zh/model-studio/wan3-video-generation-guide
  - https://help.aliyun.com/zh/model-studio/wan3-video-generation-prompt-guide
  - https://help.aliyun.com/zh/model-studio/wan3-video-generation-api-reference
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** công bố thử nghiệm 2026-08-06, mở toàn bộ 2026-08-24; prompt tối đa 20000 ký tự; có thêm bản Prime nhanh hơn và đắt hơn (`wan3.0-video-prime`) với cùng năng lực và tham số; chế độ khung đầu–cuối không nhận âm thanh.

### 23. `happyhorse-1.0` — HappyHorse 1.0
- **Loại:** video · phát hành 2026-04 · trạng thái `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.multi_reference`, `video.edit_v2v`
- **Điểm mạnh:** lúc phát hành đứng đầu bảng Artificial Analysis cho văn bản sang video không âm thanh; có bốn giao diện trên Bailian và fal: văn bản, ảnh, tham chiếu và chỉnh sửa video.
- **Điểm yếu:** các nguồn nói khác nhau về việc có mã nguồn mở hay không; thời lượng, độ phân giải chưa kiểm chứng.
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:** https://datanorth.ai/news/alibaba-launches-happyhorse-video-model
- **Xác minh:** 2026-11-12 (căn cứ: bên thứ ba) · **Độ tin cậy:** low

### 24. `wan-2.7-edit` — Wan 2.7 chỉnh sửa video
- **Loại:** video · phát hành 2026-05 · trạng thái `ga`
- **Truy cập:** api
- **Năng lực:** `video.edit_v2v`
- **Điểm mạnh:** video-replicate-studio dùng để chỉnh sửa góc máy.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://github.com/derek-zhuolin/video-replicate-studio
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** low
- **Ghi chú:** chưa tra cứu chi tiết năng lực cụ thể; cần bổ sung thăm dò (probe).

### 25. `wan-2.2` — Wan 2.2 (mã nguồn mở, gồm TI2V-5B)
- **Loại:** video · phát hành 2025-07 · trạng thái `ga`
- **Truy cập:** open-weights
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`
- **Giới hạn:** 720p
- **Âm thanh:** không (native: false)
- **Điểm mạnh:**
  - Apache 2.0; TI2V-5B chạy được trên một card đồ họa tiêu dùng.
  - Tự triển khai và tinh chỉnh được; phù hợp để sinh hàng loạt với chi phí thấp.
- **Điểm yếu:** không còn là thế hệ mới nhất.
- **Giấy phép:** cho phép thương mại (Apache 2.0).
- **Nguồn:** https://www.turingpost.com/p/6-opensource-video-generation-models
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** high

### 26. `wan-vace` — Wan VACE (Wan 2.1 VACE / Wan2.2-VACE-Fun)
- **Loại:** video · phát hành 2025-05 · trạng thái `ga`
- **Truy cập:** open-weights
- **Năng lực:** `video.control_video`, `video.edit_v2v`, `video.i2v_first_frame`
- **Giới hạn:** 480p, 720p
- **Âm thanh:** không
- **Điểm mạnh:**
  - Video độ sâu, khung xương, nét vẽ đều dùng làm đầu vào điều khiển; thêm một ảnh tham chiếu để quy định ngoại hình nhân vật. ComfyUI có sẵn workflow chuyển động vũ đạo.
  - Mã nguồn mở, chạy cục bộ được; tham số (cường độ điều khiển, chia đoạn) đều chỉnh được.
- **Điểm yếu:** phải tự dựng ComfyUI và có card đồ họa; đoạn dài phải sinh theo từng phân đoạn rồi ghép lại.
- **Giấy phép:** cho phép thương mại (Apache 2.0).
- **Nguồn:**
  - https://github.com/ali-vilab/VACE
  - https://www.runcomfy.com/comfyui-workflows/wan-2-2-vace-in-comfyui-pose-driven-motion-video-workflow
- **Xác minh:** 2026-11-14 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium

### 27. `ltx-2.5` — LTX-2.5 (mã nguồn mở)
- **Loại:** video · phát hành 2026-08 · trạng thái `ga`
- **Truy cập:** open-weights, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.reference_audio`, `video.multi_shot`, `video.edit_v2v`, `video.native_audio`, `avatar.audio_driven`
- **Âm thanh:** có sẵn
- **Điểm mạnh:** hiếm trong nhóm mã nguồn mở có hình và tiếng đồng bộ; hỗ trợ sinh có điều kiện âm thanh, chỉnh sửa, nhiều cảnh và siêu phân giải.
- **Điểm yếu:** tài liệu không nêu rõ thời lượng và độ phân giải.
- **Giấy phép:** commercial: conditional — LTX-2.x Community License: miễn phí thương mại nếu doanh thu năm dưới 10 triệu USD.
- **Nguồn:**
  - https://comfyui-wiki.com/en/news/2026-08-11-ltx-2-5-open-weights-release
  - https://fal.ai/models/lightricks/ltx-2.5/audio-to-video/pro/llms.txt
  - https://www.turingpost.com/p/6-opensource-video-generation-models
- **Xác minh:** 2026-11-12 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** trọng số mã nguồn mở 2026-08-11 (22B, thay thế LTX-2.3); API chia Fast / Pro; trên fal có giao diện video điều khiển bằng âm thanh (âm thanh 2–20 giây, Pro tối đa 10 giây).

### 28. `hunyuanvideo-1.5` — HunyuanVideo 1.5 (mã nguồn mở)
- **Loại:** video · phát hành 2025-11 · trạng thái `ga`
- **Truy cập:** open-weights
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`
- **Giới hạn:** 720p, 1080p
- **Điểm mạnh:** 8.3B tham số, chạy được với khoảng 14GB VRAM (cần offload); có sẵn mô-đun siêu phân giải, có thể nâng đầu ra lên 1080p.
- **Điểm yếu:** giấy phép loại trừ EU, Anh, Hàn Quốc.
- **Giấy phép:** commercial: conditional — Tencent Community License.
- **Vùng loại trừ (regions_excluded):** EU, UK, KR
- **Nguồn:** https://www.turingpost.com/p/6-opensource-video-generation-models
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium

### 29. `skyreels-v4` — SkyReels V4
- **Loại:** video · phát hành 2026-02 · trạng thái `ga`
- **Truy cập:** app, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.reference_video`, `video.edit_v2v`, `video.native_audio`
- **Điểm mạnh:** văn bản, ảnh, video đều làm đầu vào được; âm thanh và hình ảnh cùng được tạo; sinh và chỉnh sửa trong cùng một mô hình.
- **Điểm yếu:** chỉ có nguồn tin tức; thời lượng, độ phân giải chưa kiểm chứng.
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:** https://news.lavx.hu/article/kunlun-tech-s-skyreels-v4-claims-second-place-in-global-video-model-rankings
- **Xác minh:** 2026-11-12 (căn cứ: bên thứ ba) · **Độ tin cậy:** low

### 30. `runway-gen-4.5` — Runway Gen-4.5 (gồm Act-Two)
- **Loại:** video · phát hành 2025-12 · trạng thái `ga`
- **Truy cập:** app, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.keyframes`, `video.edit_v2v`, `video.camera_control`, `motion.transfer`, `video.native_audio`
- **Giới hạn:** tối đa 10 giây; 720p
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Bộ công cụ điều khiển đầy đủ nhất: keyframe, cọ chuyển động, đường đi camera.
  - Act-Two chuyển diễn xuất từ video dẫn sang ảnh nhân vật.
- **Điểm yếu:**
  - Gốc 720p (4K cần siêu phân giải).
  - Tính phí theo tín dụng, chi phí tăng nhanh.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://tech-insider.org/best-ai-video-generator-2026/
  - https://templix.app/blogs/best-ai-motion-control-and-animation-models-in-2026
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium

### 31. `runway-aleph-2` — Runway Aleph 2
- **Loại:** video · phát hành 2026-05 · trạng thái `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `video.edit_v2v`, `video.camera_control`
- **Điểm mạnh:** trên cảnh quay có sẵn, đổi góc máy, thêm bớt vật thể và giữ phong cách xuyên suốt cảnh.
- **Điểm yếu:** chỉnh sửa lặp lại trên dự án dài có chi phí cao.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://runway.com/news/introducing-aleph-2-and-edit-studio
  - https://openrouter.ai/runway/aleph-2/api
  - https://www.seedance.tv/blog/best-ai-video-to-video-models-2026
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** low
- **Ghi chú:** phát hành cùng Edit Studio ngày 2026-05-21.

### 32. `higgsfield-genjutsu` — Higgsfield Genjutsu (gồm Lite)
- **Loại:** video · phát hành 2026-09 · trạng thái `ga`
- **Truy cập:** app
- **Năng lực:** `video.edit_v2v`, `motion.transfer`
- **Giới hạn:** 720p, 1080p; tham chiếu: ảnh 30
- **Điểm mạnh:** đổi phong cách, đổi người hoặc đổi vật cho một đoạn video, tối đa 30 ảnh tham chiếu.
- **Điểm yếu:** không nói rõ là mô hình tự phát triển hay bọc lại mô hình khác; video đầu vào dài 4–30 giây (Lite 4–15 giây, tối đa 10 ảnh tham chiếu).
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:** https://higgsfield.ai/creator-hub/changelog
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** low
- **Ghi chú:** phát hành 2026-09-01, Lite 2026-10-19; cùng thời kỳ còn có Intone (nhân vật nói theo khẩu hình, tối đa 30 giây) và Cinema Studio 4.0 (sinh 30 giây, tối đa 50 ảnh tham chiếu).

### 33. `luma-ray3.2` — Luma Ray3.2 / Modify
- **Loại:** video · phát hành 2026-06 · trạng thái `ga`
- **Truy cập:** app, api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.edit_v2v`, `video.native_audio`
- **Giới hạn:** tối đa 10 giây; 1080p
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Modify thay diễn viên và giữ nguyên động tác, nhịp gốc.
  - Ray có khả năng tự sửa "kiểu suy luận", bám prompt tốt.
- **Điểm yếu:**
  - Chuyển cảnh trong bối cảnh phức tạp, đông người cho kết quả kém.
  - Giá tín dụng cao.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://lumalabs.ai/news/introducing-ray-3-2
  - https://tech-insider.org/best-ai-video-generator-2026/
  - https://www.seedance.tv/blog/best-ai-video-to-video-models-2026
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** low
- **Ghi chú:** phát hành 2026-06-09; là API đầy đủ đầu tiên của Luma; hiện Luma chưa có mô hình mới hơn; tối đa 16 keyframe; Modify tối đa 20 giây ở 1080p.

### 34. `flux-3-video` — FLUX 3 Video
- **Loại:** video · phát hành 2026-08 · trạng thái `ga`
- **Truy cập:** api
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.keyframes`, `video.extend`, `video.multi_shot`, `video.edit_v2v`, `video.native_audio`
- **Giới hạn:** thời lượng 5–20 giây; 720p, 1080p, 2K, 4K; 10 keyframe
- **Âm thanh:** có sẵn
- **Điểm mạnh:**
  - Tối đa 20 giây mỗi lần; lời thoại đa ngôn ngữ có khẩu hình; chữ trong khung hình được viết đúng.
  - Có thể làm bản nháp trước rồi nâng cấp; âm thanh không tính phí thêm.
- **Điểm yếu:**
  - Từ 1080p trở lên có thể là phóng đại; số đánh giá do chính nhà cung cấp chạy.
  - Ảnh, video, âm thanh tham chiếu chưa ra mắt.
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:**
  - https://bfl.ai/blog/flux-3-video
  - https://bfl.ai/models/flux-3-video
  - https://docs.bfl.ml/api-reference/utility/generate-a-video-with-flux-3.md
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** chính thức mở 2026-08-04; ba chế độ keyframe, nối tiếp và bản nháp loại trừ lẫn nhau; từ 3 keyframe trở lên phải chỉ rõ thời lượng; chỉnh sửa video đi qua FLUX Video Edit riêng.

### 35. `flux-3-video-max` — FLUX 3 Max (video)
- **Loại:** video · phát hành 2026-10 · trạng thái `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.i2v_first_last`, `video.keyframes`, `video.native_audio`
- **Giới hạn:** thời lượng 5–20 giây; 720p; 10 keyframe
- **Âm thanh:** có sẵn
- **Điểm mạnh:** nhanh; nhà cung cấp cho biết đoạn 10 giây ra trong khoảng 12 giây.
- **Điểm yếu:** gốc chỉ 720p; độ phân giải cao hơn là phóng đại.
- **Giấy phép:** commercial: conditional — chưa tìm thấy điều khoản thương mại chính thức.
- **Nguồn:**
  - https://docs.bfl.ml/api-reference/utility/generate-a-video-with-flux-3-max.md
  - https://bfl.ai/models/flux-3-video
- **Xác minh:** 2026-11-12 (căn cứ: nhà cung cấp) · **Độ tin cậy:** low
- **Ghi chú:** lên fal trước; keyframe chỉ định theo số thứ tự khung ở 24fps.

### 36. `sora-2` — Sora 2 / Sora 2 Pro
- **Loại:** video · phát hành 2025-09 · trạng thái `shutdown`
- **Truy cập:** không còn (access: [])
- **Năng lực:** `video.t2v`, `video.i2v_first_frame`, `video.native_audio`
- **Giới hạn:** tối đa 20 giây
- **Điểm mạnh:** lúc phát hành có biểu hiện vật lý tốt nhất.
- **Điểm yếu:** ứng dụng ngừng phục vụ 2026-04-26; API đóng 2026-09-24.
- **Giấy phép:** không cho thương mại (đã đóng).
- **Nguồn:** https://tech-insider.org/best-ai-video-generator-2026/
- **Xác minh:** 2026-10-29 (căn cứ: bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** thông báo ngừng hỗ trợ 2026-03-24; ứng dụng và web đóng 2026-04-26; API đóng 2026-09-24; OpenAI không đưa ra mô hình thay thế. Giữ mục này để cho thấy bản đồ năng lực phải được cập nhật liên tục; bộ định tuyến sẽ bỏ qua các mô hình có trạng thái `shutdown`.
