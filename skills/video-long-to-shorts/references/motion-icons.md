# Icon động và đường liên kết cho short dọc

> **Kết luận:** icon phải «sống» kiểu GIF: **các thành phần bên trong tương tác với nhau** theo nghĩa của vật, không chỉ sáng lên hay lắc cả khối. Icon nối nhau thì đường nối **chạy**. Hình gốc đã duyệt giữ nguyên; chuyển động là lớp phủ và thành phần tách rời, tween bằng GSAP, tua được.

Nền tảng chung (tiêu chí đạt/chưa đạt, mười công thức liên kết, mẫu đặc tả) ở `video-storyboard-design/references/creative-icon-brainstorm.md` và `motion-layout-standard.md`. File này là phần riêng của khung dọc và những gì đợt dựng short đã đo.

## Contents
- Ba mức chuyển động
- Ví dụ theo loại icon
- Cách làm: lớp phủ trên ảnh gốc
- Cách làm: ảnh bung lớp
- Đường liên kết chạy
- Vào, ở lại, ra
- Logo hãng và phân vai bằng màu
- Khi nào xin icon mới
- Tất định

## Ba mức chuyển động

| Mức | Là gì | Dùng cho |
|---|---|---|
| Sàn (`idle`) | quầng thở + trôi nhẹ + vệt sáng quét theo mặt nạ alpha | icon phụ, icon đã thu về lưới |
| Vai (`act`) | ≥ 2 thành phần bên trong chuyển động khác pha, theo nghĩa của vật | **icon chính của câu đang nói — bắt buộc** |
| Liên kết (`link`) | đường/đốm chạy giữa hai icon | mọi cặp icon có quan hệ trong câu |

Icon chính còn ở mức sàn khi gửi Cổng 2 thì ghi vào danh sách nợ; không tính là đạt. Icon đang mờ (chưa tới lượt) thì đứng yên thật.

## Ví dụ theo loại icon

| Icon | Chưa đạt | Đạt (thành phần tương tác) |
|---|---|---|
| Toà nhà / công ty | cả khối phát sáng | các ô cửa sổ bật dần từng tầng, vài ô nhấp nháy lệch pha; đèn mái quét |
| Khung lịch / bảng kế hoạch | lắc nhẹ | các ô di chuyển đổi chỗ rồi xếp thành hàng; một ô được đánh dấu |
| Bot / trợ lý | trôi lên xuống | tay bot đưa khối vào chỗ, mắt chớp theo nhịp, khối được đặt sáng lên |
| Biểu đồ | quầng thở | cột cao thấp thay đổi, đường xu hướng vẽ tiếp, con số chỉ báo đổi vị trí |
| Bài viết / trang giấy | vệt sáng quét | từng dòng chữ giả chạy ra, bút di chuyển theo dòng |
| Phát trực tiếp | phóng to thu nhỏ | chấm «đang phát» nháy, vòng sóng toả ra lần lượt |
| Chuỗi video | sáng cả dãy | từng ô lần lượt sáng, nút phát chạy từ ô này sang ô kế |
| Lộ trình bậc | trôi | đốm sáng nhảy từng bậc, bậc đã qua giữ sáng |
| Cộng đồng / mạng người | xoay cả khối | tín hiệu chạy trên các cạnh nối, từng nút sáng khi tín hiệu tới |
| Hộp công cụ / sản phẩm | bật nảy | nắp mở, từng món bay ra theo thứ tự lời |
| Lõi khái niệm (nguyên tử, mạng) | quầng thở | các nút quay trên quỹ đạo khác tốc độ, lõi phát xung khi nút đi qua |
| Chia sẻ / tương tác | bay cả khối | thẻ bay ra theo đường cong có hạt đuôi; tim, ngón tay, bong bóng nổi lên lệch pha |

Quy tắc đặt tương tác: hỏi «vật này **làm gì** ngoài đời?» rồi cho đúng thành phần đó làm việc ấy. Tương tác khớp động từ của câu thì tốt nhất (lời nói «sắp xếp» → ô lịch tự xếp).

## Cách làm: lớp phủ trên ảnh gốc

Dùng khi chỉ có một PNG phẳng của icon. Ảnh gốc không đổi một pixel.

```text
.ia (hộp icon, vị trí tuyệt đối)
 ├─ .gl    quầng thở (box-shadow, scale 1 ↔ 1.18)
 ├─ .ring  vòng toả (tuỳ chọn)
 └─ .bob   trôi dọc ±12 px
     └─ .in   nhịp phóng 1 ↔ 1.035
         ├─ img        PNG gốc
         ├─ .sh        vệt sáng quét, mask-image = chính PNG (chỉ quét trên phần có hình)
         └─ lớp phủ    các div/SVG nhỏ định vị theo % kích thước icon
```

Lớp phủ tạo tương tác bên trong mà không cắt ảnh:

- **Ô sáng** (cửa sổ, ô lịch, ô video): hình chữ nhật bo góc màu nhấn, đặt trùng ô trong ảnh theo %, tween độ mờ lệch pha.
- **Đốm chạy** (`runner`): một chấm sáng đi qua danh sách điểm `[x%, y%]` (nút mạng, bậc thang, quỹ đạo).
- **Thanh mọc**: thanh có `transform-origin` ở đáy, scaleY theo chuỗi giá trị, phủ lên cột biểu đồ.
- **Dòng chữ giả**: thanh ngang scaleX từ 0, lần lượt từng dòng.
- **Vòng sóng**: vòng tròn viền mảnh scale + mờ dần, 2–3 vòng lệch 0,9 s.

Toạ độ lớp phủ khai theo % của icon để còn đúng khi icon đổi cỡ (vào lớn rồi thu về lưới).

## Cách làm: ảnh bung lớp

Dùng khi thành phần phải **rời chỗ** (ô lịch đổi vị trí, tay bot đưa khối, nắp hộp mở): lớp phủ không che được phần gốc.

1. Có sẵn ảnh phẳng: cắt thành phần ra lớp riêng theo alpha, đặt **miếng che** cùng màu nền icon ở vị trí cũ, tween lớp đã cắt.
2. Icon mới: xin luôn **ảnh bung lớp** — một tấm gồm nền icon (không có các phần sẽ động) và từng thành phần rời đặt cạnh nhau, cùng khoá phong cách, nền phẳng một màu, không chữ. Cắt nền, ghép lại bằng toạ độ %, rồi tween từng lớp.
3. Kiểm: khung đầu của bản ghép phải trùng hình icon phẳng đã duyệt (so bằng mắt ở cỡ dùng).

## Đường liên kết chạy

- **Đường chấm chạy:** `path` SVG phủ cả khung, `stroke-dasharray: 1 20`, đầu tròn, tween `strokeDashoffset` tuyến tính với `repeat` hữu hạn tính từ thời gian cùng hiện. Màu vàng nhạt, không dùng màu nhấn đậm (tranh với từ đang tô).
- **Hướng chạy = hướng nghĩa:** nguồn → đích, tâm → nhánh, người nói → nơi diễn ra. Offset âm hay dương quyết định hướng; kiểm bằng hai ảnh tĩnh cách nhau 0,2 s.
- **Đường cong** cho hub-spoke (điểm điều khiển lệch khỏi đường thẳng tâm–nhánh) để các đường không chồng lên nhau.
- **Thứ tự:** đường chỉ xuất hiện khi icon đích đã hiện; đường tắt cùng lúc với icon đầu tiên trong cặp rời khung.
- Liên kết chạy **liên tục** suốt thời gian hai icon cùng hiện, không chạy một lần rồi đứng.
- Đốm sáng chạy dưới icon, không đè lên icon.

## Vào, ở lại, ra

| Pha | Chuẩn |
|---|---|
| Vào | bật nảy 0,4–0,55 s đúng mốc từ khoá (lấy từ `subs.json`); icon của ý đang nói vào ở cỡ lớn |
| Ở lại | chạy mức `act` khi là chủ thể; khi ý sau tới thì thu về ô lưới, hạ xuống mức `idle` |
| Ra | mờ + thu nhỏ 0,25–0,3 s ở ranh beat; phần tử dùng tiếp thì di chuyển sang vị trí mới |

Trong một short, đổi kiểu vào giữa các cảnh (bật nảy, trượt theo đường nối, lắp vào ô chờ, mọc từ tâm) để không quá 2 cảnh liền cùng một kiểu.

## Logo hãng và phân vai bằng màu

- Chỉ hiện logo của hãng/sản phẩm **được nhắc tên trong beat**, đúng lúc đọc tên, kèm quầng nhấn. «Các công cụ khác», «nền tảng khác» dùng icon chung, không tự chọn thêm logo.
- Logo giữ nguyên màu và tỉ lệ gốc; nguồn và điều khoản ghi trong sổ nguồn của kênh. Kênh có cổng tên nội bộ thì hỏi trước khi đưa tên lên hình.
- Cần phân biệt nhiều nhân vật cùng hình (ba vai, bảy trợ lý): đổi **màu bệ và quầng trong bảng màu kênh** và thêm **đạo cụ** (bảng, biểu đồ, máy quay). Không dùng bộ lọc xoay sắc: đã cho ra đỏ và xanh lá ngoài bảng màu.
- Một logo không xuất hiện hai lần trong một khung.

## Khi nào xin icon mới

Thứ tự: kho icon của kênh → icon của chính bản dài → ghép từ icon sẵn có → **xin tạo mới**. Bước cuối là thao tác ra ngoài: chỉ làm khi người dùng cho phép trong phiên, và gọi công cụ của hãng khác theo đúng luật gọi chéo của máy.

Khi được phép:

- Gom nhu cầu của **cả loạt short** vào một tấm lưới (đã đo: 4×3 = 12 ô, một tấm ≈ 7 phút), thêm 3–4 ô dự phòng cho ý có thể đổi.
- Prompt gồm: nội dung từng ô theo thứ tự; **khoá phong cách** của kênh (kiểu vẽ, bảng màu, độ dày nét, quầng); cấm chữ, số, logo, giao diện thật, mặt người thật; lưu đúng một file, không sửa file khác.
- Icon chính cần tương tác rời chỗ thì xin dạng bung lớp, mỗi icon một hàng.
- Ô lưới ≈ 300 px phóng lên 450–600 px bị mềm: icon sẽ dùng ở cỡ lớn thì xin ít ô hơn mỗi tấm hoặc tấm độ phân giải cao hơn.
- Tự xem tấm gốc trước khi dùng: lệch phong cách, có chữ lạc, icon dính nhau → tạo lại. Cắt nền theo màu nền đo ở mép ảnh, giữ quầng thành bán trong suốt.
- Ghi vào `ICON-GAPS.md`: ý, icon mới, file, lớp phủ đã dùng, điểm chưa lý tưởng.

## Tất định

Composition phải tua tới lui ra cùng một khung: không CSS animation, không SMIL, không `repeat:-1`, không ngẫu nhiên, không đồng hồ thật. Vòng lặp = `repeat` hữu hạn tính từ `(t_out − t_in) ÷ chu kỳ`; mọi tween nằm trên một timeline đã đăng ký với engine. Lệch pha giữa các thành phần đặt bằng hằng số, không sinh ngẫu nhiên.
