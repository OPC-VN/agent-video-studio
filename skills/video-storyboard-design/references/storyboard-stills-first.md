# Storyboard ảnh tĩnh trước, motion sau

Quy trình làm một tập explainer có avatar khi chủ kênh chỉ đưa **transcript và vài ý chỉnh**. Chủ duyệt hình bằng ảnh tĩnh rẻ tiền trước; máy chỉ chạy phần đắt (giọng, avatar, render) sau khi hình đã chốt. Số đo lấy từ một tập ≈ 9 phút đã dựng xong trên một máy có GPU tầm trung; máy khác thì đo lại. Luật dựng ở [motion-layout-standard](motion-layout-standard.md), cách nghĩ hình ở [creative-icon-brainstorm](creative-icon-brainstorm.md).

## Mục lục

- [Đầu vào và đầu ra](#đầu-vào-và-đầu-ra)
- [Bảy bước và bốn điểm dừng](#bảy-bước-và-bốn-điểm-dừng)
- [Khung tĩnh phải có gì](#khung-tĩnh-phải-có-gì)
- [Thời lượng máy ước từng bước](#thời-lượng-máy-ước-từng-bước)
- [Bẫy đã trả giá](#bẫy-đã-trả-giá)

## Đầu vào và đầu ra

| Chủ kênh đưa | Agent tự lo | Chủ kênh duyệt |
|---|---|---|
| transcript (lời nguyên văn), vài ý chỉnh storyboard, tên chương nếu có | tách cảnh, brainstorm hình, chọn icon, bố cục, giọng, avatar, motion, mix, kiểm | storyboard tĩnh · giọng · từng đoạn S · bản ghép |

Lời của chủ giữ nguyên văn trên màn hình và karaoke; bản đưa cho máy đọc được viết lại cách đọc, không đổi câu chữ.

## Bảy bước và bốn điểm dừng

| # | Bước | Agent làm | Đầu ra | Dừng duyệt |
|---|---|---|---|---|
| 1 | Đọc và tách cảnh | chia transcript thành chương và cảnh ở ranh câu; ước thời lượng từ tốc độ đọc đã đo của giọng (chưa đo thì ≈ 3,6 chữ/s); đánh dấu tên hãng, số liệu, từ ngoại ngữ | bảng cảnh: mã, lời, giây ước | — |
| 2 | Brainstorm hình | bảng sáu cột cho từng ý, chọn ẩn dụ, phân loại nguồn icon, đặc tả animation | `brainstorm.md` | — |
| 3 | **Storyboard tĩnh** | mỗi cảnh một khung dựng thật đúng bố cục, icon, chữ, vị trí avatar và karaoke; ghép bảng thumbnail đánh số; icon chưa có thì ô giữ chỗ ghi rõ «sẽ tạo» | bảng thumbnail + khung cỡ đầy đủ + danh sách icon cần tạo/tải | **Dừng 1:** chủ duyệt hình. Chưa gật thì không sinh giọng, không tạo icon mới, không dựng motion |
| 4 | Giọng | bản đọc cho TTS (từ ngoại ngữ, viết tắt, số), sinh theo đoạn, ASR nghe lại khớp chữ, cân mức | file giọng + bảng giờ chữ + số đo âm | **Dừng 2:** chủ nghe thử. Chưa gật thì không dựng avatar |
| 5 | Tài sản và motion | tạo/tải icon theo danh sách đã duyệt; avatar từ giọng đã duyệt; dựng motion, mốc lấy từ giờ chữ; slide điều hướng | project dựng + `segments.json` (S1…Sn, ranh ở mép cảnh) | — |
| 6 | Render đoạn | render nháp từng đoạn, tự xem và kiểm trước khi gửi; sửa theo đoạn, chỉ render lại đoạn bị chạm | S1…Sn bản nháp + bảng kiểm từng đoạn | **Dừng 3:** chủ duyệt từng đoạn S |
| 7 | Ghép và final | ghép khi mọi đoạn đạt: hình nối, **một** bản mix âm liên tục, kiểm mối nối ≤ 1 khung; bản nháp ghép trước, bản chất lượng giao sau | bản ghép nháp → bản final + hồ sơ kiểm | **Dừng 4:** chủ duyệt bản ghép rồi mới render final |

Giữa các điểm dừng, agent làm thẳng. Câu hỏi nhỏ luôn kèm mặc định để không chờ; bốn điểm dừng trên thì chờ thật, vì bước sau đắt và khó quay lại. Trong lúc chờ một điểm dừng, chỉ làm việc không phụ thuộc quyết định đó (ví dụ chờ giọng thì dựng trước các cảnh không có avatar).

Chủ góp ý ở điểm dừng 1 thì sửa khung tĩnh và gửi lại bảng thumbnail của các cảnh đã đổi, không dựng motion để «cho dễ hình dung».

## Khung tĩnh phải có gì

- Dựng từ **cùng DOM và kit** sẽ dùng cho motion (chụp ở trạng thái cuối cảnh, khi mọi mục đã hiện), không vẽ mockup ở công cụ khác: thứ chủ duyệt là thứ sẽ render.
- Mỗi khung: tiêu đề cảnh, icon thật hoặc ô giữ chỗ có tên, chữ đúng nguyên văn, vị trí và cỡ avatar, vùng karaoke với dòng dài nhất của cảnh, nhãn chương và brand.
- Cảnh có nhiều trạng thái khác hẳn nhau (trước/sau, đổi bố cục avatar) thì 2 khung.
- Dưới mỗi thumbnail một dòng: mã cảnh · giây ước · lời rút gọn · mũi tên chỉ thứ sẽ chuyển động («cột tăng giảm», «chấm chạy A → B»). Chuyển động mô tả bằng chữ, chưa dựng.
- Bảng thumbnail đọc được trên điện thoại: 3–4 cột, số cảnh in trên ảnh.
- Kiểm tĩnh trước khi gửi: chữ không chạm nhau, không chạm header, avatar, karaoke; nội dung phủ vùng an toàn; cỡ chữ đạt. Lỗi bố cục bắt ở đây rẻ hơn sau render.

## Thời lượng máy ước từng bước

Một lần đo trên một tập, một máy; dùng để lập kế hoạch và báo trước cho chủ, không phải cam kết.

| Bước | Số đo | Ghi chú |
|---|---|---|
| Tấm icon 12 ô bằng công cụ sinh ảnh | ≈ 7,5–9 phút mỗi tấm | chạy lần lượt từng tấm |
| Viết tương tác bên trong cho một icon có sẵn | ≈ 20–30 phút mỗi icon | ước lượng, chưa đo |
| Khung tĩnh + bảng thumbnail | chưa đo | đo bằng thời gian chụp N mốc của công cụ snapshot; trang nặng cần nới timeout nạp trang (đã dùng 300 s) |
| Giọng TTS clone | nạp model ≈ 52 s + ≈ 0,43 s máy cho 1 s giọng | sửa từ thì sinh lại đúng đoạn đó |
| Avatar lip-sync (khuếch tán, 30 bước) | ≈ 19,6 s máy cho 1 s hình | 103 s hình ≈ 33 phút, chia 6 take; một lượt trước đó đo 30,5 s/s; cộng thêm tách nền |
| Render nháp một đoạn | ≈ 2–3,5 lần thời lượng đoạn | phụ thuộc số lớp canvas và số video trong đoạn |
| Render chất lượng giao | chưa đo riêng | đo ở tập kế, ghi vào hồ sơ tập |

Ví dụ lập kế hoạch cho tập 9 phút có 5 phút avatar: avatar ≈ 100 phút máy, render nháp toàn bộ ≈ 20–30 phút, giọng < 10 phút. Avatar là bước đắt nhất, vì vậy giọng phải chốt trước.

## Bẫy đã trả giá

| Bẫy | Dấu hiệu | Cách tránh |
|---|---|---|
| Kế hoạch render vượt trần bộ nhớ (`PLAN_TOO_LARGE`, 2 GiB) | render một khoảng ngắn vẫn lỗi | công cụ rút khung của **mọi** `<video>` bất kể khoảng render; render từng đoạn từ bản sao chỉ giữ video giao với đoạn đó |
| Nối đoạn bằng concat làm hình trễ dần so với tiếng | càng về cuối càng lệch môi | concat xếp theo độ dài lớn nhất của tiếng/hình từng đoạn; bỏ tiếng khỏi từng đoạn trước khi nối hình, rồi ghép một bản mix âm liên tục; in số khung từng đoạn và lệch từng mối |
| Tween `stagger + yoyo + repeat` trên cùng phần tử | tua lùi ra khung khác, hai lượt chụp băm lệch | mỗi đợt một tween `fromTo` có giá trị đầu tường minh, `immediateRender:false`; không `to` chồng cùng thuộc tính |
| Video nằm trong phần tử có giờ | lint báo, runtime không nhận | đặt video làm phần tử anh em ngoài section |
| Video alpha (WebM) của avatar bị tua giữa chừng | khung đầu đoạn sai tư thế, viền bẩn | mỗi take bắt đầu ở khung 0; đoạn render chỉ giữ take giao với nó; soi khung đầu, giữa, cuối từng đoạn trên nền thật |
| Khung trắng hoặc đen ở đầu một đoạn | thẻ chương không thấy trong đoạn dù bản nguồn đúng | tự xem khung đầu mỗi đoạn sau render; không suy từ đoạn khác |
| Giọng đọc cả tiêu đề thẻ chương | đổi tên chương thì lời cũ sai nội dung | quyết ngay ở bước 1: thẻ chương có lời hay im; có lời thì tiêu đề là một phần transcript, đổi tiêu đề là đổi giọng |
| TTS đọc sai từ ngoại ngữ, viết tắt | ASR nghe lại không khớp chữ | bản đọc riêng cho máy; dùng lại cách viết đã qua ASR; thử trước rồi mới phiên âm; karaoke hiện chữ gốc |
| Karaoke tắt trước chữ cuối, hoặc chạm avatar | dòng cuối cụt, chữ đè khung người | sinh karaoke từ bảng giờ chữ; vùng chữ tính theo vị trí avatar; dòng dài ngắt 2 hàng |
| Hình hiện trễ hơn lời, đầu cảnh trống | 3–8 s đầu cảnh chỉ có avatar | mốc lấy từ giờ chữ, không gõ số; đầu cảnh hiện sẵn khung và ô rỗng |
| GIF dùng làm icon động | không tua được theo khung | GIF chỉ để xem trước; trong video là lớp rời + tween |
| Cắt lớp icon để dời thành phần | bóng ma ở chỗ cũ, mép vá lộ khi phóng | lớp xoá bằng màu nền tại chỗ cũ; soi ở cỡ phóng lớn |
| Âm lượng lệch giữa các bản, đỉnh vượt | bản mới nhỏ hơn bản đã duyệt | đo bản đã duyệt làm mốc; nâng bằng gain + limiter có oversample; không chuẩn hoá động |
| Sửa tay file dựng lớn | không tái lập được, lượt sau ghi đè | mọi thay đổi qua script vá chạy lại được; phần dùng lại vào kit |
| Sinh lại giọng hoặc avatar đã duyệt | mất bản đã duyệt, tốn hàng chục phút máy | sổ băm cho giọng và avatar; chỉ làm take mới cho lời mới |
| Xoá thư mục tạm dùng chung | phiên render khác đang chạy chết giữa chừng | chỉ xoá thư mục con do chính lượt mình tạo; không xoá cả `.tmp` |
| Xoá liên kết thư mục (junction) bằng lệnh xoá đệ quy | xoá luôn dữ liệu ở đích | gỡ junction bằng lệnh gỡ thư mục rỗng (`rmdir`), không xoá đệ quy |
| Hai phiên cùng ghi một project | file dựng bị ghi đè giữa lượt render | khi một phiên đang render, phiên khác chỉ đọc thư mục đó |
