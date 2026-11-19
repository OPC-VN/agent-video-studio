# Mô hình ảnh: keyframe, khung đầu, phân cảnh, chữ trong ảnh
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/models/image.yaml · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Chú thích: `image.t2i` = văn bản sang ảnh; `image.edit_multi_ref` = chỉnh sửa nhiều ảnh tham chiếu; `image.text_render` = render chữ trong ảnh; `image.storyboard_series` = sinh bộ nhiều ảnh phân cảnh; `analyze.image_layer_decompose` = tách ảnh thành nhiều lớp.

Tổng số mục: 21 mô hình.

---

## Danh mục

| # | id | Tên | Nhà cung cấp | Trạng thái |
|---|---|---|---|---|
| 1 | `gpt-image-2.5` | GPT Image 2.5 | OpenAI | ga |
| 2 | `gpt-image-2.6` | GPT Image 2.6 (Sunburst / Flare) | OpenAI | ga |
| 3 | `nano-banana-2.1` | Nano Banana 2.1 | Google | ga |
| 4 | `nano-banana-2-lite` | Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image) | Google | ga |
| 5 | `seedream-5.0` | Seedream 5.0 (Lite / Pro / Flash) | ByteDance Seed | ga |
| 6 | `seedream-5.5` | Seedream 5.5 | ByteDance Seed | ga |
| 7 | `qwen-image-3.0-pro` | Qwen Image 3.0 Pro | Alibaba | ga |
| 8 | `qwen-image-3.0` | Qwen Image 3.0 | Alibaba | ga |
| 9 | `qwen-image-2.1` | Qwen Image 2.1 (mã nguồn mở 7B, gồm Pro / Turbo API) | Alibaba | ga |
| 10 | `flux-3` | FLUX 3 Image | Black Forest Labs | ga |
| 11 | `flux-3-klein` | FLUX 3 Image Klein | Black Forest Labs | ga |
| 12 | `kling-o3-image` | Kling Image 3.0 / 3.0 Omni (O3 Image) | Kuaishou | ga |
| 13 | `minimax-h3-image` | MiniMax H3 Image (gồm Highspeed) | MiniMax | ga |
| 14 | `grok-imagine-image-2.0` | Grok Imagine Image 2.0 | xAI | ga |
| 15 | `mai-image-2.6` | MAI-Image-2.6 (gồm Flash) | Microsoft AI | ga |
| 16 | `ideogram-4.5` | Ideogram 4.5 | Ideogram | ga |
| 17 | `midjourney-v8.2` | Midjourney V8.2 | Midjourney | ga |

Lưu ý: file nguồn có 17 mục mô hình; bảng trên liệt kê đủ 17 mục.

---

## Chi tiết từng mô hình

### 1. `gpt-image-2.5` — GPT Image 2.5
- **Nhà cung cấp / loại:** OpenAI · image · phát hành 2026-09 · `ga`
- **Truy cập:** api, app, api-aggregator
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Điểm mạnh:**
  - **[Người dùng thử thực tế]** chữ tiếng Trung trong ảnh hiển thị tốt nhất và độ chân thực cao nhất; là lựa chọn hàng đầu cho chữ trong ảnh tiếng Trung và khung đầu thực tế.
  - Tuân thủ chỉ dẫn ổn định; xuất được nền trong suốt (PNG/WebP); các mức chất lượng lên tới xhigh và max.
- **Điểm yếu:** giá và tốc độ phụ thuộc mức chất lượng.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://www.eachlabs.ai/blog/best-ai-image-generation-models-2026
  - https://developers.openai.com/api/docs/models
- **Xác minh:** 2026-10-29 (căn cứ: người dùng) · **Độ tin cậy:** high
- **Ghi chú:** có hai bản: sunburst (chất lượng) và flare (nhanh), đã bị gpt-image-2.6 thay thế; ngày phát hành là tháng 9 hoặc 10, nguồn không thống nhất. Hypit hiện đang dùng GPT Image 2 (qua HypiHub; một số tỷ lệ 2K/4K không dùng được).

### 2. `gpt-image-2.6` — GPT Image 2.6 (Sunburst / Flare)
- **Loại:** image · phát hành 2026-11 · `ga`
- **Truy cập:** api, app, api-aggregator
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Điểm mạnh:**
  - Đứng đầu bảng Artificial Analysis cho văn bản sang ảnh (mức chất lượng Sunburst cao nhất).
  - Có thể khoanh vùng cần sửa trên ảnh (chỉnh sửa markup); xuất được nền trong suốt, SVG và ảnh động.
- **Điểm yếu:**
  - Mức chất lượng cao nhất mỗi ảnh tối đa khoảng 2 phút và giá cao; chỉnh sửa liên tiếp nhiều lần sẽ trôi.
  - Vị trí chính xác của chữ vẫn có thể lệch; hiệu quả chữ tiếng Trung chưa được nhà cung cấp nêu.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://developers.openai.com/api/docs/guides/image-generation
  - https://developers.openai.com/api/docs/guides/image-prompting
  - https://kingy.ai/ai-launch-tracker/chatgpt-images-2-6-2026-11-04/
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-11-04; ID mô hình `gpt-image-2.6-sunburst` (chất lượng) / `gpt-image-2.6-flare` (nhanh); cạnh tối đa 3840 và chia hết cho 16, tỷ lệ 1:3–3:1.

### 3. `nano-banana-2.1` — Nano Banana 2.1
- **Loại:** image · phát hành 2026-10 · `ga`
- **Truy cập:** api, app, api-aggregator
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Giới hạn:** 4K
- **Điểm mạnh:** nhanh; chữ trong ảnh rõ; hỗ trợ khổ rộng và toàn cảnh.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://www.eachlabs.ai/blog/best-ai-image-generation-models-2026
  - https://aistudio.google.com/docs/models/gemini-nano-banana-2.1
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-10-06; ID mô hình `gemini-nano-banana-2.1`; tối đa 14 ảnh tham chiếu (10 vật thể + 4 nhân vật); độ phân giải ghi 1K / 2K / 4K (phải viết hoa); mọi đầu ra đều có watermark SynthID.

### 4. `nano-banana-2-lite` — Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image)
- **Loại:** image · phát hành 2026-06 · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `image.t2i`
- **Điểm mạnh:** nhanh nhất và rẻ nhất trong họ; phù hợp để sinh bản nháp hàng loạt.
- **Điểm yếu:** nhà cung cấp nói không tối ưu cho nhiều ảnh tham chiếu và chỉnh sửa nhiều lượt; không phù hợp để giữ nhân vật hoặc ra bộ keyframe.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://aistudio.google.com/docs/image-generation
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** ID mô hình `gemini-3.1-flash-lite-image`.

### 5. `seedream-5.0` — Seedream 5.0 (Lite / Pro / Flash)
- **Loại:** image · phát hành 2026-02 · `ga`
- **Truy cập:** app, api, api-aggregator
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`, `image.storyboard_series`, `analyze.image_layer_decompose`
- **Điểm mạnh:**
  - Tách lớp: xuất nền và nhiều lớp PNG trong suốt; có thể dùng để suy ngược bố cục của một khung.
  - Giỏi infographic, chỉnh sửa tương tác, ảnh chân thực và chữ đa ngôn ngữ.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://www.eachlabs.ai/blog/best-ai-image-generation-models-2026
  - https://docs.volcengine.com/docs/82379/1824121
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** Lite phát hành 2026-02 (`doubao-seedream-5-0-260128`); Pro phát hành 2026-06, lên API 07-08 (`doubao-seedream-5-0-pro-260628`); Flash phát hành 2026-09 (`doubao-seedream-5-0-flash-260915`); chỉ Lite hỗ trợ bộ nhiều ảnh; tham chiếu Lite tối đa 14 ảnh, Pro / Flash tối đa 10 ảnh; Hypit dùng Lite; đã có bản 5.5 mới hơn.

### 6. `seedream-5.5` — Seedream 5.5
- **Loại:** image · phát hành 2026-11 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`, `analyze.image_layer_decompose`
- **Giới hạn:** tham chiếu ảnh 10
- **Điểm mạnh:**
  - Chỉnh sửa nhiều lượt ổn định: nhà cung cấp nói có thể sửa liên tiếp 100 lượt, vùng không sửa được giữ nguyên.
  - Chữ nhỏ dày đặc và chữ phức tạp chính xác hơn; xuất trực tiếp nền trong suốt và tách lớp.
- **Điểm yếu:**
  - Không hỗ trợ bộ nhiều ảnh; bộ keyframe phải sinh từng ảnh.
  - Bài kiểm tra bên thứ ba cho thấy chữ nhỏ trên poster phức tạp vẫn sai.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://seed.bytedance.com/zh/blog/ (bài "Seedream 5.5: tạo chân thực hơn, chỉnh sửa trăm lượt ổn định"; đường dẫn gốc chứa chữ Hán nên đã rút gọn)
  - https://docs.volcengine.com/docs/82379/1824121
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-11-09, ID mô hình `doubao-seedream-5-5-261028`; dùng được trên Jimeng, Doubao, Volcano Ark; bản Pro chưa phát hành.

### 7. `qwen-image-3.0-pro` — Qwen Image 3.0 Pro
- **Loại:** image · phát hành 2026-07 · `ga`
- **Truy cập:** api
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Điểm mạnh:** giỏi đoạn chữ dày đặc và bố cục dài; prompt tối đa 4500 token; mỗi lần tối đa 6 ảnh.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://www.eachlabs.ai/blog/best-ai-image-generation-models-2026
  - https://help.aliyun.com/zh/document_detail/2713156.html
- **Xác minh:** 2026-10-29 (bên thứ ba) · **Độ tin cậy:** medium
- **Ghi chú:** mời thử 2026-07-21, mở toàn bộ 2026-08-05; sinh và chỉnh sửa cùng một mô hình; có bản không Pro nhanh và rẻ hơn là `qwen-image-3.0`.

### 8. `qwen-image-3.0` — Qwen Image 3.0
- **Loại:** image · phát hành 2026-07 · `ga`
- **Truy cập:** api, app
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Giới hạn:** 2048x2048
- **Điểm mạnh:** năng lực tương đương 3.0 Pro (sinh và chỉnh sửa trong cùng một mô hình), nhanh hơn và rẻ hơn; mỗi lần tối đa 6 ảnh.
- **Điểm yếu:** không mã nguồn mở.
- **Giấy phép:** cho phép thương mại.
- **Nguồn:** https://help.aliyun.com/zh/document_detail/2713156.html
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 9. `qwen-image-2.1` — Qwen Image 2.1 (mã nguồn mở 7B, gồm Pro / Turbo API)
- **Loại:** image · phát hành 2026-09 · `ga`
- **Truy cập:** api, open-weights
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`, `image.tryon`
- **Giới hạn:** 2K; tham chiếu ảnh 10
- **Điểm mạnh:**
  - Mô hình 7B nhỏ, chạy cục bộ được; Turbo khoảng 0.016 USD mỗi ảnh.
  - Sinh, chỉnh sửa, tách nền trong cùng một mô hình; xuất trực tiếp nền trong suốt; có thể khoanh, tô hoặc chỉnh cục bộ bằng mặt nạ.
- **Điểm yếu:**
  - Trọng số mã nguồn mở chỉ dùng nghiên cứu; thương mại phải qua API hoặc giấy phép riêng.
  - Thứ hạng bảng xếp hạng thấp hơn 3.0.
- **Giấy phép:** commercial: conditional — trọng số theo Qwen Research License (chỉ nghiên cứu); API được thương mại.
- **Nguồn:**
  - https://www.alibabacloud.com/blog/qwen-image-2-1-pro-and-turbo-apis-are-live-one-7b-model-to-generate-edit-and-cut-out_603679
  - https://huggingface.co/Qwen/Qwen-Image-2.1
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** trọng số mở 2026-09-20; API Pro / Turbo ra mắt 2026-10-09.

### 10. `flux-3` — FLUX 3 Image
- **Loại:** image · phát hành 2026-10 · `ga`
- **Truy cập:** api, api-aggregator
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Giới hạn:** 768p, 1K, 2K, 4K; tham chiếu ảnh 10
- **Điểm mạnh:** đặt phần tử chính xác theo khung bao (bounding box), phù hợp để phục dựng bố cục theo ảnh gốc; chữ đa ngôn ngữ.
- **Điểm yếu:** mặc định bật tìm kiếm web và ảnh (grounding).
- **Giấy phép:** cho phép thương mại.
- **Nguồn:**
  - https://www.eachlabs.ai/blog/best-ai-image-generation-models-2026
  - https://docs.bfl.ai/release-notes
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** 2026-07-23 công bố họ mô hình, FLUX 3 Image lên API 2026-10-01; khi dùng ảnh tham chiếu đầu ra tối đa 4MP; từ 10-22 hỗ trợ kích thước tùy chỉnh từ 256px đến 16.8MP.

### 11. `flux-3-klein` — FLUX 3 Image Klein
- **Loại:** image · phát hành 2026-10 · `ga`
- **Truy cập:** api, api-aggregator, open-weights
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`
- **Giới hạn:** 768p, 1K, 2K, 4K; tham chiếu ảnh 10
- **Điểm mạnh:** 5.6B tham số, chạy được trên card tiêu dùng (RTX 3090); mỗi ảnh 0.008–0.036 USD.
- **Điểm yếu:** tên giấy phép mã nguồn mở và điều khoản thương mại chưa được kiểm chứng.
- **Giấy phép:** commercial: conditional — điều khoản thương mại của trọng số mở chưa kiểm chứng.
- **Nguồn:** https://docs.bfl.ai/release-notes
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-10-15; có bản chưng cất (16 bước) và bản cơ bản (50 bước).

### 12. `kling-o3-image` — Kling Image 3.0 / 3.0 Omni (O3 Image)
- **Loại:** image · phát hành 2026-02 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.storyboard_series`
- **Giới hạn:** 1K, 2K, 4K
- **Điểm mạnh:**
  - Hỗ trợ ảnh tham chiếu và element để khóa danh tính và phong cách.
  - Chế độ bộ phân cảnh phù hợp để xuất một bộ keyframe trong một lần.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://help.artlist.io/hc/en-us/articles/37026869403933-Kling-3-Model-Family
  - https://kling.ai/document-api/api/image/3-0-omni/image-omni.md
  - https://kling.ai/blog/kling-image-3-vs-omni
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** mở cho thành viên cao cấp từ 2026-02-05; tên API `kling-v3-omni`; prompt tối đa 2500 ký tự; ảnh cộng chủ thể tối đa 10; bộ 2–9 ảnh (chỉ bản Omni có).

### 13. `minimax-h3-image` — MiniMax H3 Image (gồm Highspeed)
- **Loại:** image · phát hành 2026-11 · `ga`
- **Truy cập:** api, app, open-weights
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Giới hạn:** 1K, 2K, 4K; tham chiếu ảnh 16
- **Điểm mạnh:** ra 4K nhanh (nhà cung cấp nói khoảng 10 giây); prompt rất dài (tối đa 32000 ký tự); trọng số mở.
- **Điểm yếu:**
  - Chạy cục bộ cần khoảng 135 GB; giấy phép nhiều hạn chế (theo báo cáo loại trừ EU, Anh, Hàn Quốc, Mỹ; doanh thu trên 1 triệu USD phải xin phép).
  - Bằng chứng chất lượng chủ yếu từ nhà cung cấp; chữ tiếng Trung chưa được kiểm tra.
- **Giấy phép:** commercial: conditional — MiniMax-H3-Image Community License.
- **Nguồn:**
  - https://platform.minimax.io/docs/api-reference/image-generation-h3-generations.md
  - https://www.orcarouter.ai/blog/minimax-h3-image-launch
  - https://www.ifanr.com/1688790
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-11-10; yêu cầu không idempotent, thử lại sẽ bị tính phí lại.

### 14. `grok-imagine-image-2.0` — Grok Imagine Image 2.0
- **Loại:** image · phát hành 2026-08 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`
- **Giới hạn:** 1K, 2K; tham chiếu ảnh 5
- **Điểm mạnh:** mỗi lần tối đa 10 ảnh; 16 tỷ lệ khung.
- **Điểm yếu:** chưa có thông tin chính thức về render chữ và tiếng Trung.
- **Giấy phép:** cho phép thương mại (theo điều khoản nền tảng).
- **Nguồn:**
  - https://docs.x.ai/docs/models/grok-imagine-image-2.0
  - https://docs.x.ai/docs/guides/image-generations
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium

### 15. `mai-image-2.6` — MAI-Image-2.6 (gồm Flash)
- **Loại:** image · phát hành 2026-08 · `ga`
- **Truy cập:** api
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Giới hạn:** 1.5K; tham chiếu ảnh 5
- **Điểm mạnh:** có tìm kiếm web (grounding); nhà cung cấp nói render chữ chính xác.
- **Điểm yếu:** tối đa 1.5K; đứng giữa bảng xếp hạng.
- **Giấy phép:** cho phép thương mại (theo điều khoản Azure).
- **Nguồn:** https://techcommunity.microsoft.com/t5/microsoft-foundry-blog/mai-image-2-6-and-mai-image-2-6-flash-quality-and-speed-at/ba-p/4550970
- **Xác minh:** 2026-11-12 (nhà cung cấp) · **Độ tin cậy:** medium
- **Ghi chú:** phát hành 2026-08-10, vào Foundry công khai thử nghiệm 2026-09-04; 2026-10-27 có thêm MAI-Image-2.7 Preview chỉ chỉnh sửa.

### 16. `ideogram-4.5` — Ideogram 4.5
- **Loại:** image · phát hành 2026-09 · `ga`
- **Truy cập:** app, api
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`, `image.text_render`
- **Giới hạn:** 2K; tham chiếu ảnh 4
- **Điểm mạnh:** chuyên chỉnh sửa chính xác: sửa lặp lại không trôi; có thể thêm mặt nạ.
- **Điểm yếu:** chữ tiếng Trung chưa kiểm chứng; giá các nguồn nói khác nhau.
- **Giấy phép:** commercial: conditional — theo điều khoản Ideogram; trọng số mở của 4.0 là giấy phép không thương mại.
- **Nguồn:** https://ideogram.ai/licensing/
- **Xác minh:** 2026-11-12 (bên thứ ba) · **Độ tin cậy:** low
- **Ghi chú:** phát hành 2026-09-30; 4.0 phát hành 2026-06.

### 17. `midjourney-v8.2` — Midjourney V8.2
- **Loại:** image · phát hành 2026-07 · `ga`
- **Truy cập:** app
- **Năng lực:** `image.t2i`, `image.edit_multi_ref`
- **Giới hạn:** 2K
- **Điểm mạnh:** thẩm mỹ hình ảnh và phong cách hóa mạnh; nhiều người sáng tạo dùng để ra khung đầu; tham chiếu phong cách `--sref` giữ phong cách thống nhất.
- **Điểm yếu:**
  - Chỉ có app, không có API chính thức.
  - Tham chiếu nhân vật `--oref` trên V8 được hỗ trợ khác nhau tùy nguồn; `--cref` không hỗ trợ.
- **Giấy phép:** commercial: conditional — theo điều khoản gói đăng ký Midjourney.
- **Nguồn:**
  - https://vidmuse.ai/blog/midjourney-8-2
  - https://evolink.ai/docs/en/api-manual/image-series/midjourney/midjourney-v8-1-prompt-guide.md
  - https://blakecrosley.com/en/guides/midjourney
- **Xác minh:** 2026-11-12 (bên thứ ba) · **Độ tin cậy:** low
- **Ghi chú:** 2026-07-24 trở thành phiên bản mặc định; V8.1 ra tháng 4/2026 với độ phân giải gốc 2K.
