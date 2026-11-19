# Mở rộng bộ đánh giá

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · docs/dev/evaluation.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Cài trước các phụ thuộc phát triển: `pip install -e ".[ocr,dev]"`.

1. Thêm mục vào `eval/labels.yaml` (hoặc tạo một yaml mới):
   - `label`: có thể là danh sách, nghĩa là nhiều nhãn đều được chấp nhận
   - `segments`: nhãn thật theo từng đoạn
   - `real_material`: có dùng tư liệu thật hay không
   - `cuts` / `cut_tolerance`: nhãn thật của các điểm cắt
   - `audio`: `{voice, music, sfx, bpm, key}`
2. Nhãn thật phải có nguồn, ghi trong trường `source`: bản ghi sản xuất (timeline.json, manifest, cues.py) > nhãn AIGC của nền tảng > xem bằng mắt người (xem bằng mắt thì phải ghi "còn nghi ngờ").
3. Chạy `rea-video eval eval/xxx.yaml -o out/eval_xxx`. Khi chỉ sửa luật phân loại thì không cần giải mã lại: đánh giá sẽ phân loại lại bằng đặc trưng đã cache; khi sửa mã đo trên video (giải mã, cắt cảnh, đặc trưng, âm thanh, đồ họa hậu kỳ) thì sẽ tự giải mã lại, không chấm điểm code mới bằng đặc trưng cũ (`--fresh` làm lại tất cả, `--only id` chỉ giải mã lại video được chỉ định). Nếu đường dẫn trong danh sách không tìm thấy thì dùng bản sao lưu trong `eval/media/<id>.<phần mở rộng>`; vẫn thiếu thì liệt kê trong `missing` của bản tóm tắt. Bản tóm tắt có `by_resolution` / `by_camera` tách độ chính xác và hướng nhận sai theo nhóm độ phân giải và kiểu máy quay; trước và sau khi sửa luật, so sánh xem lỗi có tập trung ở loại hình nào không.
4. Tránh overfitting khi chỉnh luật: giữ ít nhất một bộ **hold-out** chỉ được chạy **sau khi** đã sửa luật lần đầu, và ghi kết quả vào `eval/RESULTS.md`.

## Benchmark cho chuyển cảnh và người nói

Hai mục này không có video gán nhãn sẵn, nên dùng mẫu tổng hợp có đáp án đã biết để đo:

```bash
# Chuyển cảnh: lấy các cảnh có hình ổn định từ video cho trước, ghép từng cặp với 47 kiểu chuyển cảnh (ffmpeg xfade cộng với các kiểu tự tổng hợp: whip / xoay / phóng / glitch / rung / làm mờ),
# mỗi kiểu với độ dài 0.3 / 0.6 / 1.0 giây. Tìm thấy = chỉ báo đúng một ranh giới và nằm trong chuyển cảnh; đúng loại = loại được báo thuộc họ của chuyển cảnh đó
python3 scripts/bench_transitions.py a.mp4 b.mp4 c.mp4 --out out/bench_transitions --pairs 5

# Người nói: mỗi đầu vào là video một người đang nói; phần giọng khô được cắt thành các đoạn 2–7 giây và ghép luân phiên thành hội thoại, có thể chèn nhạc nền (--music) và chồng lời (--overlap)
python3 scripts/bench_speakers.py a.mp4 b.mp4 c.mp4 --out out/bench_speakers --music bgm.mp4
```

Sau khi sửa `shots.py` / `transitions.py` phải xem cả hai phía: benchmark tổng hợp xem loại, còn nhãn điểm cắt của `eval/film.yaml`, `koubo.yaml`, `daihuo.yaml` xem có báo thừa / thiếu trên video thật không.
Khi tính điểm cắt, nếu điểm cắt được gán nằm trong khoảng đầu–cuối của một chuyển cảnh thì được tính là đã tìm thấy (người gán và bộ phát hiện có thể đã lấy hai khung khác nhau trong nửa giây của chuyển cảnh lật/quét (wipe)).
