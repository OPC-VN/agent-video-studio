# Nhiệm vụ cho agent kiểm tra mù (tách video {V})
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · eval/agent_test/JOB.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Bạn đang ở trong một bản sao của kho rea-video (thư mục hiện tại). Trước hết đọc AGENTS.md, skills/rea-video/SKILL.md, và các tệp mà nó tham chiếu trong skills/rea-video/references/ (taxonomy, audio, materials, output-template). Làm việc đúng theo quy trình trong SKILL.md.

Nhiệm vụ: phân rã video videos/{V}.mp4. Đây là bản chuyển mã tải từ bài viết WeChat Official Account (30fps, nén lại lần hai). Bạn không biết nó được làm như thế nào; bạn cần tự phán đoán.

1. Nếu môi trường chưa cài đặt đầy đủ, trước hết cài theo mục 0 của SKILL.md (cần ffmpeg; có thể dùng trực tiếp `python3 -m rea_video.cli` thay cho `rea-video`).
2. Chạy decompose, xuất ra runs/{V}/. Khi cấu hình VLM dùng được (ví dụ `--env-file ~/code/github/capsule-cinema/.env`), bật `--vlm` theo khuyến nghị của SKILL.md; không dùng được thì không bật, và ghi rõ trong báo cáo.
3. Tự review theo SKILL.md. Trước hết xác định bạn có xem được ảnh hay không: nếu xem được thì xem storyboard.jpg, shots/, các cảnh có độ tin cậy thấp; nếu không xem được thì tuân thủ mục "Quy tắc khi không xem được ảnh" trong SKILL.md.
4. Viết runs/{V}/AGENT_REPORT.md (tiếng Việt) theo cấu trúc của references/output-template.md, bắt buộc có:
   - Kết luận một câu: cách làm (quay thật / video AI / người ảo / 3D / render từ code / quay màn hình hoặc ảnh chụp màn hình / ảnh tĩnh pan/zoom / khung tĩnh) và tỷ lệ từng loại
   - Bảng phân cảnh, tư liệu thật, âm thanh (giọng người / BGM / hiệu ứng và nguồn), điểm chưa chắc chắn
   - Dòng cuối cùng theo đúng định dạng cố định: `FINAL: <cách làm chính> | <độ tin cậy 0-1> | <xem được ảnh: yes/no> | <VLM có hiệu lực: yes/partial/no>` (lấy theo dòng `VLM:` của `rea-video summary`; yêu cầu nhưng gọi thất bại thì ghi no)
5. Không sửa mã, không tìm kiếm trên mạng về video này, không đọc file ngoài thư mục hiện tại.
