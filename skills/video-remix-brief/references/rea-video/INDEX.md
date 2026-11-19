# Tri thức phục dựng từ rea-video (bản dịch tiếng Việt)

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · Apache-2.0. Các file trong thư mục này là bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)) từ tài liệu tiếng Trung của upstream; không phải bản gốc.

**Chỉ để tham khảo khi lập kế hoạch.** Phần này mô tả cách phục dựng bằng model AI sinh video (Seedance, Kling, Veo…) và chuỗi công cụ của upstream. agent-video-studio **không chạy** các bước đó (không có executor sinh video, không gọi dịch vụ trả phí); việc dựng dùng HyperFrames và `video-studio render`. Dùng để: hiểu khả năng từng model, viết brief/treatment có căn cứ, giải thích cho người dùng vì sao một cảnh nên quay thật, dựng bằng code hay sinh bằng AI.

**Lưu ý dịch (quan trọng):** các chuỗi prompt mẫu vốn là tiếng Trung (cho Seedance, Jimeng, Kling…) đã được dịch sang tiếng Việt để đọc hiểu; khi thật sự gửi tới model Trung Quốc phải dùng đúng bản gốc trong checkout rea-video (`rea_video/capabilities/prompting.yaml`). Các token tham chiếu `@<ảnh>N` / `@<video>N` có ghi chú điểm mã Unicode ở đầu file liên quan. Chất lượng bản dịch: Haiku dịch, Fable soát; file lõi khoảng 95 %, model và năng lực khoảng 85–90 % về văn phong (số liệu và id đã đối chiếu tự động với bản gốc).

| File | Nội dung | Gốc (rea-video) |
|---|---|---|
| `diy.md` | Tự làm | `skills/rea-video/references/diy.md` |
| `docs-replicate.md` | Phục dựng theo báo cáo | `docs/replicate.md` |
| `hyperframes.md` | HyperFrames | `skills/rea-video/references/hyperframes.md` |
| `model-analysis.md` | Phân tích (lật phim): VLM lo ngữ nghĩa, công cụ tất định lo thời gian và vị trí chính xác | `rea_video/capabilities/models/analysis.yaml` |
| `model-audio.md` | Âm thanh: lồng tiếng, nhân bản giọng, nhạc, hiệu ứng, sinh âm thanh từ video | `rea_video/capabilities/models/audio.yaml` |
| `model-character.md` | Nhân vật: chuyển động, người ảo, đồng bộ khẩu hình, thử đồ ảo | `rea_video/capabilities/models/character.yaml` |
| `model-image.md` | Mô hình ảnh: keyframe, khung đầu, phân cảnh, chữ trong ảnh | `rea_video/capabilities/models/image.yaml` |
| `model-render-post.md` | Render từ code, ghép và hậu kỳ | `rea_video/capabilities/models/render-post.yaml` |
| `model-threed.md` | Sinh 3D (nhất quán đa góc sản phẩm / bàn xoay / khối trắng tham chiếu) | `rea_video/capabilities/models/threed.yaml` |
| `model-video.md` | Mô hình sinh / chỉnh sửa video | `rea_video/capabilities/models/video.yaml` |
| `nang-luc-matrix.md` | Ma trận năng lực (tự sinh, không sửa tay) | `rea_video/capabilities/MATRIX.md` |
| `nang-luc-primitives.md` | Nguyên thủy rea-video (primitives) | `rea_video/capabilities/primitives.yaml` |
| `nang-luc-prompting.md` | Cách viết prompt và yêu cầu khung hình của từng mô hình | `rea_video/capabilities/prompting.yaml` |
| `nang-luc-readme.md` | Bản đồ năng lực rea-video (Capability Map) | `rea_video/capabilities/README.md` |
| `nang-luc-routing.md` | Quy tắc định tuyến rea-video: đặc trưng cảnh (signals) → chuỗi nguyên thủy (route) → mô hình ứng viên (prefer, theo thứ tự ưu tiên) | `rea_video/capabilities/routing.yaml` |
| `remake-tools.md` | Công cụ và cách làm để phục dựng | `skills/rea-video/references/remake-tools.md` |
| `remake.md` | Phục dựng (remake) | `skills/rea-video/references/remake.md` |
