# Quy trình «copy → dựng giống» (video mẫu → video mới)

Giống **cấu trúc, nhịp, hiệu ứng, bố cục chữ, bảng màu**; khác mọi tư liệu (ảnh, người, giọng, nhạc, logo).
Nhân bản người/giọng/khuôn mặt/logo của mẫu bị cấm kể cả khi «đã có phép» (`video-remix-brief`).

```
video mẫu (tệp cục bộ, đã rõ quyền)
  → reference init --file                       hồ sơ quyền + provenance.json
  → cleanup inspect                             thời lượng, khung hình, có tiếng không
  → reference transcribe --language vi          lời (rea-video không có ASR tiếng Việt)
  → reference decompose --no-VLM (mặc định)     VIDEO.md, video/{timeline,rhythm,look,packaging,sound}.md, shots/
  → reference videomd --check                   gói hợp lệ
  → agent nhìn ảnh: reference tiles/frames + review → apply-review
  → reference-map.md                            bảng beat: mốc, lời, hình, chữ, màu, hiệu ứng, bằng chứng @khung
  ↘ (học để làm loạt video) reference-patterns.md → gộp vào thư viện vlog-design: references/library-merge.md
  → video-remix-brief                           brief, treatment, storyboard (nội dung và tư liệu CỦA NGƯỜI DÙNG)
  → engine sẵn có                               land-plot-map-video (bản đồ), HyperFrames, narrate, edit, theme library
  → video-studio render                         bản dựng
  → reference decompose bản dựng + compare      bảng lệch so với mẫu → sửa → lặp
```

## Ánh xạ «máy thấy → mình làm»

| rea-video cho | Dùng làm gì | Engine/skill nhận |
|---|---|---|
| `video/rhythm.md`: mốc `change`/`cut` theo khung (`@N`) | ứng viên ranh beat; độ dài từng beat | `reference-map.md` cột «Thời điểm» |
| `video/timeline.md`: camera, chuyển cảnh, nhãn «made~» | loại chuyển động mỗi cảnh (tĩnh/lướt/zoom) | thẻ cảnh: trường «Chuyển cảnh» (mẫu chung) hoặc mã TR (storyboard `vlog-design`) |
| `video/look.md` | khung hình, ánh sáng, màu (cảnh quay thật) | brief; cảnh quay thật → `video-edit` |
| `video/packaging.md` + `packaging/timeline.json` | chữ phủ, nhãn, sticker, âm nhấn: thời điểm, kiểu | lớp chữ HyperFrames; mẫu `land-plot-map-video` |
| `video/sound.md` | giọng/nhạc/âm nhấn, có bắt nhịp | `narrate`, nhạc có quyền; gói mẫu mục 6 → nhóm AU của thư viện `vlog-design` |
| `video/remake.md` | kế hoạch **dùng model sinh** (Seedance…) | **bỏ**: dựng bằng engine của repo này |

## Tiêu chí «giống» (đo được; ngưỡng là ASSUMPTION, người dùng chốt)

1. Số beat và thứ tự khớp bản đồ mẫu.
2. ≥ 7/9 ranh beat có mốc `change` của bản dựng trong ±0,7 s (≈ 21 khung) so với mẫu (mốc tay từ lưới 1 s sai số ±1 s).
3. Thời lượng ±0,5 s; độ dài từng beat lệch ≤ 10 %.
4. Chữ phủ: cụm nào, hiện lúc nào (±0,5 s), cỡ/màu/viền cùng kiểu (nhìn ảnh, không chấm chính tả có dấu).
5. Bảng màu chủ đạo cùng nhóm; chuyển động cùng loại (zoom/pan/nhòe).
Không đòi giống từng điểm ảnh: ảnh nền, người dẫn, giọng, nhạc khác. Ghi rõ điều chưa kiểm.

## Phần phải có người xem

Cảm giác chuyển động nhòe, glow, độ đọc chữ, quyền ảnh nền và người dẫn, và «đúng vị trí» khi là cảnh bản đồ.
