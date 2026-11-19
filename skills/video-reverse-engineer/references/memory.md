# Ghi nhớ sửa lỗi và tùy chọn của người dùng

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/memory.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

- Khi người dùng chỉ ra một cảnh bị phán sai ("đây là stop-motion chứ không phải AI", "đoạn này là tôi tự quay"): chạy
  `rea-video correct out/ref --shots 3,5 --label stop_motion --note "<lời nguyên văn của người dùng>"` (`--label` điền đúng loại người dùng nói; tên loại xem trong `taxonomy.md`: stop-motion là `stop_motion`, ảnh tĩnh pan/zoom là `still_motion`; cũng có thể dùng `--start/--end` để chỉ khoảng thời gian, `--shots all` nghĩa là toàn bộ; tư liệu quay thật dùng `--real yes|no`).
  Lệnh này cập nhật ngay kết luận và báo cáo, đồng thời ghi vào `~/.rea-video/corrections.jsonl`; các lần phân rã cùng một tệp về sau sẽ tự áp dụng, và các cảnh cùng loại sẽ được nhắc trong tác vụ review.
- Khi người dùng nói ra một sở thích lâu dài: nếu ứng với tham số thì dùng `rea-video prefs engine kling2.1`, `prefs vlm on`, `prefs env_file <đường dẫn>`, `prefs reviewer <tên>`, `prefs capsule_root <đường dẫn capsule-cinema>`; còn lại thì ghi bằng `rea-video prefs --note "báo cáo nên ngắn, trọng tâm là phương án phục dựng"`. Lần `rea-video memory` sau sẽ hiển thị các ghi chú này, và bạn điều chỉnh cách trả lời theo đó.
- Chỉ ghi những gì người dùng nói rõ, đừng ghi phỏng đoán của bạn thành một lần sửa. Việc sửa lỗi không tự động thay đổi trọng số phân loại; khi tích lũy vài mục, dùng `rea-video memory --export-labels eval/user_labels.yaml` để xuất thành mẫu đánh giá, rồi đánh giá và chỉnh quy tắc theo quy ước phát triển (repo `docs/dev/evaluation.md`).
