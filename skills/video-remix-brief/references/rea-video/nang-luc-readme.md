# Bản đồ năng lực rea-video (Capability Map)
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · rea_video/capabilities/README.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

> Mô hình chính là "bộ lệnh" của rea-video. Đảo ngược một video nghĩa là dịch từng cảnh (shot) thành một tập lệnh sinh hoặc render code kiểm soát được nhất trong năng lực hiện tại của mô hình.
> Đây là sổ tay bộ lệnh đó: có dữ liệu, kiểm chứng được, có ngày xác minh, và sẽ lỗi thời.

Bảng tổng hợp dễ đọc cho người: [MATRIX.md](MATRIX.md), sinh tự động bằng script.

## Cấu trúc ba tầng

```
signals (đặc trưng cảnh quay, phát hiện khi phân tích ngược)
   │  routing.yaml
   ▼
primitives (nguyên thủy năng lực, không phụ thuộc nhà cung cấp)  ◄── primitives.yaml
   │  trường primitives trong models/*.yaml
   ▼
models (mô hình/công cụ cụ thể, kèm giới hạn, giá, giấy phép, nguồn)
```

- **primitives.yaml**: tổng cộng 43 nguyên thủy, bao phủ phân tích, hình ảnh, video, điều khiển nhân vật, 3D, âm thanh, render code và hậu kỳ; ngoài ra có 16 chỉ số kiểm chứng. Bộ định tuyến chỉ nhận nguyên thủy, nên đổi nhà cung cấp thì không cần sửa quy tắc.
- **models/*.yaml**: mỗi mô hình một mục, chia file theo nhóm:
  - `video`: sinh và chỉnh sửa video
  - `character`: chuyển động nhân vật, người ảo (digital human), dub lại khẩu hình, thử đồ
  - `image`: ảnh
  - `audio`: âm thanh
  - `threed`: sinh 3D
  - `analysis`: VLM và công cụ tất định dùng để phân tích ngược
  - `render-post`: render code, ghép cảnh, siêu phân giải, nội suy khung hình
- **prompting.yaml**: cách viết prompt của từng mô hình và yêu cầu về keyframe, đánh chỉ mục theo id mô hình:
  - cách viết cấu trúc, ngôn ngữ, độ dài, nhiều cảnh và thời gian; cách gọi tài liệu tham chiếu; lời thoại và âm thanh; cách viết nội dung không muốn có; chuyển động máy quay; nội dung cần viết ở chế độ khung đầu / khung đầu–cuối; yêu cầu với ảnh khung và ảnh tham chiếu; công tắc tự viết lại prompt; các vấn đề đã biết
  - `basis` ghi nguồn chính; `unverified` liệt kê chỗ chưa kiểm chứng hoặc nguồn mâu thuẫn; `keyframes` ở đầu file là cách làm keyframe chung cho mọi mô hình
  - xem: `rea-video models <id>`; kế hoạch phục dựng dùng mô hình nào thì lấy cách viết của mô hình đó
- **routing.yaml**: gồm các phần:
  - định nghĩa tín hiệu (signals)
  - quy tắc tách hai cấp (cảnh dựng → đơn vị sinh → lớp)
  - định tuyến hình ảnh R01–R16, định tuyến âm thanh A01–A05, định tuyến hậu kỳ
  - chính sách chi phí, nút xác nhận, kỷ luật prompt

## Trường của mục mô hình

| Trường | Ý nghĩa |
|---|---|
| `id` | Duy nhất toàn cục, chữ thường, nối bằng gạch ngang |
| `status` | `ga` (phát hành chính thức) / `preview` (xem trước) / `limited` (giới hạn) / `deprecated` (không khuyến nghị nữa) / `shutdown` (đã ngừng); bộ định tuyến bỏ qua `shutdown` |
| `access` | `app` / `api` / `api-aggregator` (cổng API tổng hợp) / `open-weights` (trọng số mở) |
| `primitives` | Các nguyên thủy mô hình hỗ trợ |
| `limits` | Biên giới như thời lượng, độ phân giải, số tham chiếu, số keyframe. `exclusive_inputs` liệt kê các nhóm đầu vào không được đặt chung trong một yêu cầu (ví dụ khung đầu–cuối và ảnh tham chiếu); kế hoạch phục dựng dựa vào đó để chọn một chế độ cho mỗi đơn vị sinh |
| `cost.usd_per_s` | Chi phí tương đối, dùng để sắp xếp định tuyến và ước tính ngân sách |
| `license` | `commercial: true / false / conditional` kèm ghi chú; `regions_excluded` liệt kê khu vực bị hạn chế |
| `verified.basis` | Độ tin cậy từ cao đến thấp: `probe` (tự kiểm) > `user` (người dùng thực tế) > `vendor` (chính hãng) > `third-party` (bên thứ ba) > `knowledge` (kiến thức chung hoặc kiến thức huấn luyện) |
| `confidence` | `high` / `medium` / `low` |
| `probe_scores` | Điểm bài kiểm tra thăm dò; dành sẵn, do probe tự ghi vào |

## Quy trình bảo trì

1. **Thêm hoặc cập nhật mô hình**: sửa đúng `models/*.yaml`, ghi link nguồn và `verified.date`; với mô hình video, bổ sung thêm cách viết prompt vào `prompting.yaml`.
2. **Kiểm tra**: chạy `python3 scripts/validate_capabilities.py --matrix`. Script kiểm tra schema, tính toàn vẹn tham chiếu, "mô hình ưu tiên có thật sự hỗ trợ nguyên thủy không", các nguyên thủy còn trống và các mục quá hạn (quá 90 ngày).
3. **Kết luận từ người dùng thực tế** (ví dụ "GPT Image 2.5 chữ Trung tốt nhất"): ghi vào `strengths` và đặt `basis` là `user`.
4. **Mô hình ngừng hoạt động**: đổi `status` thành `shutdown`, giữ nguyên mục, đồng thời gỡ khỏi quy tắc định tuyến.
5. **Probe (P1)**: mỗi nguyên thủy có một nhóm bài kiểm tra nhỏ (trường `probe` trong `primitives.yaml`); khi mô hình mới lên sóng, probe tự chạy, ghi điểm vào `probe_scores`, và bộ sắp xếp định tuyến sẽ ưu tiên tham khảo điểm này.

## Việc còn để ngỏ

- Nhiều mục có tháng phát hành và thông số chi tiết lấy từ tổng hợp bên thứ ba, được gắn `medium` hoặc `low`; cần kiểm lại bằng probe hoặc tài liệu chính hãng.
- Một số mô hình là bản huấn luyện lại từ MiniMax H3 (Pika H3 Flex, HeyGen Video 1, Utopai X, P-Video-2-Pro); khi xem giấy phép phải xem cùng giấy phép của H3.
- Các mô hình này chưa có cách viết prompt chính thức, nên `prompting.yaml` tạm thiếu: HappyHorse 1.0, SkyReels V4, Grok Imagine Video 1.5 Lite, Utopai X, P-Video-2-Pro, Higgsfield Genjutsu.
- Chỉ có tin đồn, chưa có trang chính thức nên chưa được đưa vào: Veo 3.2 / 4, Gemini Omni Pro, Runway Gen-5, Luma Ray 4, Hunyuan Video 2.0, Midjourney Video V2.
- Chưa đưa vào: ảnh Jimeng, ảnh Keling, khả năng người ảo và xuất file của Jianying / CapCut, các công cụ người ảo trong nước như Chanchan và Shanjian (chưa tìm thấy thông tin phát hành ở cấp mô hình).
