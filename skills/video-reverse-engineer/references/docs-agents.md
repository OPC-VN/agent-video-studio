# rea-video: hướng dẫn cho Agent

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · AGENTS.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

- Lần đầu sử dụng: chạy `bash scripts/install_skill.sh` (cài CLI và liên kết skill vào các thư mục agent thông dụng; cần ffmpeg, Python ≥ 3.10), rồi chạy `rea-video --help` để xác nhận.
- Khi người dùng muốn phân rã video, xác định cách làm, đánh dấu tư liệu thật, tách nhạc và hiệu ứng âm thanh, hoặc phục dựng: **đọc `skills/rea-video/SKILL.md` trước**, làm theo quy trình trong đó, và review các cảnh có độ tin cậy thấp.
- Phân công trong repo:
  - `skills/rea-video/`: skill dành cho agent (quy trình + references), chỉ viết cách dùng, không đặt tài liệu phát triển ở đây
  - `rea_video/`: CLI và logic phân rã; bản đồ năng lực mô hình nằm ở `rea_video/capabilities/`, script tích hợp capsule-cinema nằm ở `rea_video/integrations/`
  - `docs/`: tài liệu cho người đọc; `docs/dev/` là tài liệu phát triển (mở rộng bộ đánh giá, thêm chiều phân tích kỹ thuật quay)
  - `eval/`: bộ đánh giá; `tests/`: kiểm thử cục bộ, đã nằm trong .gitignore, không đưa vào repo
- Quy ước phát triển:
  - Môi trường phát triển: `pip install -e ".[ocr,dev]"` (dev gồm pytest và jsonschema, dùng cho kiểm thử và kiểm tra bản đồ năng lực)
  - Sau khi đổi luật, chạy `python3 -m pytest -q` và `rea-video eval eval/labels.yaml` / `eval/holdout*.yaml`, cập nhật kết quả vào `eval/RESULTS.md`
  - Sau khi sửa bản đồ năng lực, chạy `python3 scripts/validate_capabilities.py --matrix`
- Không commit bất kỳ khóa bí mật nào; cấu hình VLM đọc qua `--env-file`.
