# Tư liệu thật của người dùng

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/materials.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

> **Ghi chú dịch:** `@<ảnh>N` và `@<video>N` là token tham chiếu trong prompt gửi Seedance/Jimeng. Ở bản gốc chúng viết bằng chữ Hán: `@` + hai ký tự U+56FE U+7247 + số cho ảnh, `@` + hai ký tự U+89C6 U+9891 + số cho video. Model chỉ nhận đúng ký tự gốc, nên khi ghép prompt thật phải dùng đúng mã này (xem chuỗi mẫu trong `rea_video/dance.py`).

**Định nghĩa**: trên khung hình, các điểm ảnh không do bên sản xuất sinh ra hay render, mà được đưa vào từ thực tế: video quay thật, ảnh chụp thật, ảnh chụp màn hình web/App, quay màn hình, đoạn video phát trong bố cục, logo hoặc ảnh sản phẩm được dán vào. Khi phục dựng, các thứ này phải do người dùng cung cấp file gốc, **không được ghi là "dùng AI tạo"**.

**Tách khỏi "tư liệu tham chiếu"**: sản phẩm, logo, nhân vật xuất hiện trong video AI, người ảo, hay hình 3D là điểm ảnh do mô hình hoặc trình render tạo ra, nên không tính là tư liệu thật; chúng được ghi vào `material.references`, và trong báo cáo là "tư liệu tham chiếu cần chuẩn bị để phục dựng", khi phục dựng được nạp vào mô hình như ảnh tham chiếu (`@<ảnh>N`). Sản phẩm xuất hiện trong cảnh quay thật là đạo cụ, cũng ghi là tham chiếu.

## Cách công cụ đánh dấu

- **Toàn khung**:
  - Quay thật → tư liệu video quay thật
  - Quay màn hình / ảnh chụp màn hình → tư liệu quay màn hình hoặc ảnh giao diện (ảnh tĩnh tính là ảnh chụp màn hình)
  - Khung tĩnh / ảnh tĩnh pan/zoom mà nguồn là ảnh chụp hoặc ảnh màn hình → ảnh chụp thật hoặc ảnh màn hình
  - Khung tĩnh, nguồn không rõ (chưa bật VLM) → "tư liệu ảnh (thật/AI chờ xác nhận)", không tính là tư liệu thật
- **Nhúng** (chỉ dò trong hình render: render từ code, quay màn hình, 3D, thẻ render):
  - Vùng có texture ảnh chụp: entropy độ xám cao, không có mảng phẳng, và không nằm trong dải phụ đề → tư liệu ảnh/hình, **đánh dấu "thật hay AI chờ xác nhận"** (ảnh dán trong mẫu cũng có thể là ảnh AI). Hoặc VLM xác nhận, hoặc bạn tự xem ảnh và phán đoán
  - Panel màu nhạt + trong một khung hình có ≥6 chỗ chữ nhỏ → ảnh chụp giao diện (tính luôn là tư liệu thật)
  - Trong vùng có chuyển động, còn xung quanh đứng yên → đoạn video nhúng hoặc quay màn hình
- **VLM**: các mục có `is_real_material=true` trong `embedded_assets`. Nếu lớp nền là bố cục render (code, quay màn hình, ảnh tĩnh) thì tính là tư liệu nhúng, và `real_footage` mà VLM trả về được ghi là "đoạn video nhúng" (bản thân nó có thể là video AI); nếu lớp nền là video AI / người ảo / quay thật, hoặc sản phẩm, logo, nhân vật trong 3D, thì ghi là tư liệu tham chiếu.

## Điểm bỏ sót đã biết

- Ảnh tối, bán trong suốt, làm nền tạo không khí (ví dụ ảnh nền NASA của mediank): độ tương phản texture quá thấp nên phép dò tất định không thấy. Gặp template tông tối thì phải tự nhìn kỹ phần nền.
- Ảnh chụp màn hình web chủ đề tối: không phải panel màu nhạt, không phát hiện được; phải xem trong khung hình có khung trình duyệt hay khung giao diện không.
- Logo nhỏ, ảnh sản phẩm chồng lên quay thật hoặc video AI: lớp tất định không dò phần nhúng trên nền là ảnh chụp (dễ báo nhầm), phụ thuộc vào VLM.

## Cảnh chèn (B-roll) từ kho stock

Các cảnh quay thật không liên quan trực tiếp đến chủ thể video như flycam thành phố, timelapse, phong cảnh, người mẫu công sở, cận cảnh bàn tay thường được mua từ trang stock chứ không phải tác giả tự quay. Công cụ đánh dấu chúng là "tư liệu video quay thật". Khi xem ảnh, ghi trong `description` là "nghi là B-roll từ kho stock", và khi bàn giao thì liệt kê tách riêng khỏi tư liệu tác giả tự quay: khi phục dựng chỉ cần tìm cảnh cùng loại trên trang stock, không cần xin người dùng file gốc.

Đoạn phim (`film_footage`) cũng vậy: tư liệu thuộc về hãng phim; khi bàn giao ghi "cần tìm đoạn tương ứng trong phim gốc, dùng thương mại phải xin phép", không ghi thành tư liệu của chính người dùng.

## Cách ghi khi bàn giao

Liệt kê từng mục: số cảnh, thời gian, loại tư liệu, vị trí trên khung hình, mô tả nội dung, và "khi phục dựng cần bạn cung cấp: ……".
