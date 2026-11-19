# Gói phân rã VIDEO.md

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · docs/videomd.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Phân rã một video sẽ cho ra hai thứ:

- **Báo cáo cho người đọc** (`report.html` / `report.pdf`): video này nói gì, vì sao nó hot, được làm như thế nào, và làm theo thế nào để phục dựng.
- **Gói phân rã cho mô hình và chương trình đọc** (`VIDEO.md` + `video/`): cùng kết luận, nhưng đặt theo một định dạng cố định trong một thư mục. Agent trả lời câu hỏi và các dự án phía sau (downstream) tạo tác vụ phục dựng đều đọc gói này.

Mỗi skill có một `SKILL.md`, mỗi video có một `VIDEO.md`. VIDEO.md là một định dạng mở; đặc tả, tư duy thiết kế, hướng dẫn tích hợp và sinh, cùng bộ kiểm tra đều nằm ở [videomd/videomd](https://github.com/videomd/videomd) ([tiếng Trung](https://videomd.github.io/videomd/zh/)), lấy bên đó làm chuẩn. Trang này chỉ nói về những gì có trong gói phân rã do rea-video sinh ra.

## Đọc theo từng lớp

1. **Thẻ** (phần front matter của `VIDEO.md`, vài trăm token): video này nói gì, làm như thế nào, và chắc chắn đến mức nào.
2. **Tổng quan và bản đồ** (phần thân `VIDEO.md`, khoảng 1–2k token): kết luận, mạch kể chuyện, tóm tắt phương án phục dựng, điểm chưa chắc chắn. Bản đồ mỗi dòng một file: `đường dẫn | khoảng token | có gì bên trong · khi nào nên đọc`.
3. **Timeline** (`video/timeline.md`): mỗi dòng một cảnh. Khóa có dấu `~` là suy luận; khóa không có dấu là thứ nhìn thấy trên hình hoặc đo được.
4. **File cảnh** (`video/shots/<mã số>.md`) và ảnh chụp khung hình: chỉ mở khi cần kiểm tra một cảnh cụ thể.

Với một video nói trước camera dài 3 phút, đọc đến tổng quan khoảng 2k token, cộng thêm timeline khoảng 4k token; toàn bộ dữ liệu `breakdown.json` khoảng 190 nghìn token.

## Những gì rea-video đưa vào gói

| File | Nội dung |
|---|---|
| `VIDEO.md` | Thẻ có `made_mix` (tỉ lệ cách làm theo thời lượng), `confidence`, `readers` (công cụ / mô hình xem ảnh / agent / người), `source.sha256`; phần thân là kết luận, nội dung nói gì, mạch kể, tóm tắt phục dựng, tư liệu thật cần lấy, điểm chưa chắc chắn, bản đồ |
| `video/timeline.md` | `story` vai trò trong câu chuyện · `seen` hình ảnh · `act` diễn xuất · `camera` chuyển động máy · `overlay` lớp chồng · `made~` cách làm · `material~` nguồn tư liệu · `remake` hướng phục dựng · `flag` cần review |
| `video/content.md` | Nội dung và cấu trúc, mạch kể, lời thoại |
| `video/cast.md` | Nhân vật, bối cảnh, đạo cụ |
| `video/sound.md` | Giọng người, BGM, hiệu ứng âm thanh, nhịp và nguồn |
| `video/rhythm.md` | Nhịp và keyframe: mỗi phút mấy nhát cắt, độ dài cảnh, đường cong biến thiên của hình (mỗi 0.5 giây một chữ số), thời điểm và thời lượng của các điểm cắt và chuyển cảnh (mỗi mốc thời gian kèm số khung của video gốc @N; chỗ nào bước survey đã xem thì phía sau ghi cắt sang cái gì), keyframe của từng cảnh (thời điểm + thuộc loại nào: khung đầu, động tác bắt đầu / tới vị trí, điểm ngoặt, phần tử vào/ra, đổi bố cục, đỉnh biểu cảm, giữa chuyển cảnh…) |
| `video/look.md` | Cỡ cảnh, góc máy, ánh sáng, cách dựng và thiết bị của các cảnh quay thật (khi có cảnh quay thật) |
| `video/packaging.md` | Thời gian và kiểu của phụ đề, chữ nhấn, sticker, hình trong hình (PiP) |
| `video/remake.md` | Phương án phục dựng: đơn vị sinh, buổi quay, dựng hình bằng code, tư liệu thật cần chuẩn bị, diễn xuất và cảm xúc |
| `video/shots/<mã số>.md` | Với mỗi cảnh: `inferred` (cách làm, xác suất, phương án thứ hai, do ai phán định, có tư liệu thật hay không), `flags`, `keyframes` (thời gian và loại), `frames`; phần thân là những gì nhìn thấy, suy luận và căn cứ, prompt |
| `breakdown.json`, `shots/`, `stems/`, `sfx/`, `packaging/`, `frames/` (chỉ khi có cảnh render bằng code), `storyboard.jpg`, `audio.png` | Dữ liệu đầy đủ và file phương tiện, được liệt kê trong bản đồ |

Các file chủ đề không có nội dung thì không được sinh ra.

## Lệnh

```bash
rea-video decompose ref.mp4 -o out/ref      # Sinh gói phân rã cùng lúc khi phân rã
rea-video videomd out/ref                   # Sinh lại gói phân rã từ breakdown.json
rea-video videomd out/ref --check           # Kiểm tra theo đặc tả VIDEO.md (dùng gói videomd)
```

```python
import videomd
pkg = videomd.read("out/ref")   # {"card", "map", "timeline", "shots"}
```
