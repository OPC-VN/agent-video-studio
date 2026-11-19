# HyperFrames

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/hyperframes.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

[HyperFrames](https://github.com/heygen-com/hyperframes) là framework video HTML mã nguồn mở: trợ lý lập trình AI viết HTML / CSS animation, render thành MP4. Các cảnh render bằng code, motion graphics (MG) và cảnh hoạt hình minh họa vốn được làm theo cách này. Giao cho nó làm lại thành một dự án có thể sửa sẽ gần với gốc hơn bản nháp `code-remake` có sẵn của rea-video.

## Chi phí

- Framework mã nguồn mở, miễn phí (Apache-2.0), render cục bộ.
- Ứng dụng Studio của nó có gói trả phí riêng (kết nối mô hình sinh của HeyGen); việc làm lại các cảnh code không cần đến gói này.

> Trong agent-video-studio, HyperFrames đã có sẵn và ghim bản cụ thể; dùng skill `hyperframes-core`, `hyperframes-animation` và lệnh `video-studio render`; không cài hay cập nhật skill từ ngoài.

## Đưa gì cho nó

Giao các thứ sau cho trợ lý đang viết dự án HyperFrames, và nói rõ «làm lại theo nhịp và hình ảnh này, không dùng pixel của video gốc»:

1. `video/rhythm.md`: thời điểm và loại chuyển cảnh, thời lượng chuyển, keyframe từng cảnh (thời điểm + loại: bắt đầu / đến vị trí động tác, chuyển hướng, phần tử vào/ra, thay đổi bố cục…). Mỗi thời điểm có số `@` phía sau là số khung hình của video gốc; hãy sắp xếp theo số khung hình, không theo số giây đã làm tròn (HyperFrames dùng cùng tốc độ khung hình). Keyframe của animation đặt đúng theo đây, phần chuyển tiếp giữa các keyframe để easing xử lý.
2. Ảnh keyframe từng cảnh `shots/shot_XXX.jpg`, cùng mục «Dựng hình bằng code» của báo cáo: bố cục, bảng màu (mã màu), phần tử là gì, và cách chúng xuất hiện.
3. Âm thanh: dùng `stems/music.wav` làm nhạc nền, hoặc đổi sang bài khác theo BPM và cảm xúc trong `video/sound.md`; mốc thời gian hiệu ứng nằm trong `video/sound.md`.
4. Phụ đề và chữ nhấn: `packaging/timeline.json` (thời gian, vị trí, kiểu).

Nếu chỉ muốn làm lại một vài cảnh thì nói rõ số cảnh và khoảng thời gian; các cảnh còn lại có thể dùng video gốc làm chỗ giữ chỗ, và các đoạn đã làm xong ghi vào `remake/mine.json`, rồi dùng `rea-video remake out/ref` để ghép lại timeline gốc (xem `diy.md`).
