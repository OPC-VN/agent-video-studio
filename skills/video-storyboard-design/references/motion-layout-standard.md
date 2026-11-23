# Chuẩn chuyển động và bố cục cho explainer có avatar

Luật dựng cảnh rút từ năm vòng phản hồi của chủ kênh khi dựng một tập explainer có người dẫn. **MUST** = bắt buộc, vi phạm là không giao; **SHOULD** = mặc định, lệch phải ghi lý do. Đây là bản tổng quát: kênh có `channels/<kênh>/STYLE-GUIDE.md` thì luật kênh (màu, nền, logo, nhạc riêng) thắng phần chung ở đây.

Hai reference đi kèm: [creative-icon-brainstorm](creative-icon-brainstorm.md) (từ transcript chủ đề mới ra ẩn dụ hình, icon có tương tác bên trong, thư viện motion liên kết, bảng mẫu) và [storyboard-stills-first](storyboard-stills-first.md) (trình tự làm việc với chủ: storyboard ảnh tĩnh → giọng → đoạn S → ghép, thời lượng máy, bẫy).

## Mục lục

- [Quy trình duyệt theo đoạn](#quy-trình-duyệt-theo-đoạn)
- [Icon và liên kết](#icon-và-liên-kết)
- [Bố cục và nhấn mạnh](#bố-cục-và-nhấn-mạnh)
- [Nền, nhạc và âm lượng](#nền-nhạc-và-âm-lượng)
- [Tất định kỹ thuật](#tất-định-kỹ-thuật)
- [Kiểm tự động nên có](#kiểm-tự-động-nên-có)
- [Sáu câu soi trước khi gửi duyệt](#sáu-câu-soi-trước-khi-gửi-duyệt)

## Quy trình duyệt theo đoạn

0. **MUST** hình duyệt bằng ảnh tĩnh trước khi dựng motion: mỗi cảnh một khung dựng thật (đúng bố cục, icon, chữ), ghép bảng thumbnail cho chủ duyệt; bốn điểm dừng theo thứ tự storyboard tĩnh → giọng → từng đoạn S → bản ghép. Chi tiết ở [storyboard-stills-first](storyboard-stills-first.md).
1. **MUST** chia video thành các đoạn duyệt S1…Sn, ranh ở mép cảnh, ghi vào `segments.json`. Chủ xem từng đoạn, sửa theo từng đoạn.
2. **MUST** chỉ gộp khi mọi đoạn đạt. Bản gộp có MỘT bản mix âm liên tục; lệch mối nối ≤ 1 khung, kiểm ở mỗi mối.
3. **MUST** có bản slide điều hướng (bấm tới/lùi theo bước, sinh từ cùng DOM, tắt tiếng, ẩn karaoke mặc định) để chủ soi từng bước.
4. **MUST** không sửa tay file dựng lớn: mọi thay đổi qua script vá chạy lại được; phần dùng lại nằm trong kit của kênh.
5. **MUST** giọng đã duyệt thì không tạo lại. Giọng mới (lời mới) dừng cho chủ nghe thử trước khi dựng avatar; avatar chỉ nhận WAV đã duyệt.
6. **MUST** đoạn nối thêm vào video đã duyệt chỉ làm take mới cho phần lời mới, không render lại take cũ; kiểm mối nối.
7. **SHOULD** cảnh chuyển sang tập sau thì cất vào `videoN-parked`, không xoá.
8. **SHOULD** câu hỏi cho chủ luôn kèm mặc định để làm tiếp, không chờ.

## Icon và liên kết

- **MUST** icon luôn động, không có icon đứng yên. Giữ đúng hình icon đã duyệt: PNG gốc không đổi một pixel, chuyển động là lớp phủ cộng tween. GIF chỉ để xem trước. Sàn cho icon phụ là quầng thở cộng vệt sáng (`idle`).
- **MUST** icon là chủ thể của câu đang nói có **tương tác giữa các thành phần bên trong** (≥ 2 thành phần chuyển động theo nghĩa của vật: ô lịch dời chỗ, chấm chạy trong ống, cột tăng giảm, thẻ đổi cột, luồng sáng đi qua từng khối); lắc, trôi, phát sáng cả khối không tính. Icon chính còn ở mức sàn thì ghi vào danh sách nợ khi gửi duyệt. Bảng đạt/chưa đạt theo loại icon và cách đo ở [creative-icon-brainstorm](creative-icon-brainstorm.md).
- **MUST** icon và ẩn dụ hình sinh từ lời thoại của chính tập đó (bảng brainstorm: lời · ý chính · 2–3 ẩn dụ · tương tác bên trong · motion liên kết · bố cục); không dùng lại icon tập trước chỉ vì có sẵn.
- **MUST** icon và đối tượng hiện theo thứ tự lời nói; mốc lấy từ giờ chữ karaoke, không gõ cứng.
- **MUST** icon đang dim thì đứng yên thật; sáng lên mới chạy hoạt hoạ theo vai.
- **MUST** khi các icon nối nhau, hiệu ứng liên kết (dải chấm chạy, mũi tên chạy, vòng nét đứt quay, đốm sáng chạy vòng, photon trên dây, ribbon) chạy liên tục suốt thời gian cùng hiện; chọn công thức theo nghĩa quan hệ trong câu, hướng chạy đúng nghĩa (thư viện công thức ở [creative-icon-brainstorm](creative-icon-brainstorm.md)). Chấm chạy màu vàng nhạt `#FFE08A` trên nền chấm trắng alpha .35; không dùng amber đậm.
- **MUST** nhắc hãng hay sản phẩm nào thì hiện logo hãng đó đúng lúc nói, kèm highlight. Tải bản chính thức vào `brands/`, ghi `SOURCES.md` (URL nguồn, URL file, ngày, điều khoản, SHA-256); SVG kiểm sạch, giữ màu và tỉ lệ. Tải không được thì dùng ô chữ và báo rõ.
- **MUST** không lặp một kiểu chuyển động quá 2 cảnh liền.
- **SHOULD** minh hoạ sản phẩm của chính mình bằng giao diện thật.

## Bố cục và nhấn mạnh

- **MUST** bố cục cân đối, không chỗ trống: nội dung phủ đều vùng an toàn, chữ và hoạt hoạ cân hai bên; chuỗi icon giãn đủ thoáng.
- **MUST** chữ không chạm nhau và không chạm header/brand: tiêu đề cảnh cách nhãn chương ≥ 60 px; nhãn không đè icon hay đường nối.
- **MUST** karaoke không chạm avatar: vùng chữ tính theo vị trí avatar, cách khung avatar ≥ 48 px, không tràn khung, dòng dài ngắt 2 hàng thay vì thu chữ. Đổi bố cục avatar chỉ ở ranh câu.
- **MUST** các mục liệt kê cùng tồn tại tới hết cảnh. Mục chưa nhắc là ô nét đứt rỗng; tới lời thì thẻ lắp vào ô.
- **MUST** nhấn mạnh bằng viền vàng nhấp nháy dim (1 ↔ .3, êm, đúng cửa lời, tắt hẳn sau cửa); không chớp một phát, không gắt.
- **MUST** phần tử cùng nhóm cùng trục (lệch ≤ 1 px); phần tử chuyển tiếp (bánh răng, mũi tên) nằm giữa hai trạng thái.
- **MUST** đường hoặc vạch gắn với vật chuyển động phải bám vật đó (mép vạch trùng playhead ≤ 2 px). Nét vẽ chỉ xuất hiện khi chữ cũ đã rời; đốm sáng chạy dưới icon, không đè.
- **MUST** biểu đồ đúng nghĩa: pie chia theo tỉ lệ thật, mỗi dây chạm đúng lát; cột chồng có ribbon nối, vẽ sau khi cột mọc; legend đặt ngay dưới icon.
- **MUST** minh hoạ «video» dùng khung video thật cắt từ chính bản đang dựng cộng nút play, không khung giả.
- **MUST** chữ thông tin ≥ 28 px, nhãn phụ ≥ 24 px đậm 700, không chữ alpha < .8; đọc được ở 360p.
- **SHOULD** không màn nào đứng yên quá 6 s: luôn có một chuyển động có nghĩa (không tính nền).

## Nền, nhạc và âm lượng

- **MUST** nền tối đồng nhất toàn tập. Dải neuron (plexus) chỉ ở thẻ chương và outro; màn nội dung chỉ có hạt nhạt cộng nối mảnh quanh viền, giữa màn để trống cho nội dung.
- **MUST** âm lượng bản mới bằng bản đã duyệt đầu tiên: tích hợp −14,4 ±0,3 LUFS, true peak ≤ −1,0 dBTP, LRA lệch ≤ 1 LU. Nâng bằng gain cộng limiter ở hậu kỳ, không loudnorm động; giọng mới cân bằng MỘT hệ số gain về đúng mức giọng cũ.
- **MUST** nhạc intro tắt hẳn trước khi giọng vào (không duck), cú đập trùng mốc hit của hình. Nhạc outro (**SHOULD**) cùng motif, cú đập trùng lúc logo đáp, vào sau chữ cuối ≥ 0,4 s.
- **MUST** lời mới đi qua hồ sơ giọng của kênh: chuẩn hoá từ ngoại ngữ/viết tắt trong bản TTS (không đổi câu chữ), ASR nghe lại khớp 100 %. Xem `voice-routing`.

## Tất định kỹ thuật

- **MUST** không CSS animation, SMIL, `repeat:-1`, `Math.random`, `Date`, `requestAnimationFrame`; vòng lặp dùng `repeat` hữu hạn và gắn `data:'loop'`.
- **MUST** vẽ canvas bằng hàm thuần theo `t`, chung MỘT tween proxy; vòng lặp kín.
- **MUST** `fromTo` + `immediateRender:false` với giá trị đầu tường minh; không `stagger+yoyo+repeat` trên cùng phần tử; mỗi đợt một tween.
- **MUST** `<video>` không là con của `<section data-start>`; render đoạn qua bản sao rút gọn để tránh `PLAN_TOO_LARGE`.
- **MUST** tua ngược ra cùng khung; hai lượt snapshot đảo thứ tự băm trùng.

## Kiểm tự động nên có

Một script kiểm của kênh (ví dụ `check_standard.py <index.html>`, exit 0/1, dòng JSON cuối) gom các kiểm sau; MUST thì lỗi là không giao.

| Mã | Kiểm gì | Mức |
|---|---|---|
| CK-ICON-MOTION | Mọi icon có ≥ 1 tween `data:'loop'` trong thời gian cảnh | MUST |
| CK-ICON-PARTS | Icon chính của câu: ≥ 2 tween trên phần tử con khác pha; vùng pixel đổi nằm ở thành phần, không phủ cả icon; hộp bao icon trôi ≤ 6 px | MUST |
| CK-ICON-BASE | `img` gốc của icon trùng SHA-256 với bộ icon đã duyệt | MUST |
| CK-CUE | Tween «vào» nằm trong ±0,4 s một giờ chữ karaoke; không số gõ cứng | SHOULD |
| CK-LINK | Cảnh ≥ 2 icon có nối → tween lặp phủ ≥ 80 % thời gian cùng hiện | MUST |
| CK-OVERLAP | Hộp chữ không giao; cách header ≥ 60/24 px, cách avatar ≥ 48 px, trong khung | MUST |
| CK-FILL | Nội dung phủ ≥ 60 % vùng an toàn; lệch tâm ngang ≤ 60 px khi không avatar | SHOULD |
| CK-FONT | Không chữ < 24 px; chữ thông tin ≥ 28 px; không alpha < .8 | MUST |
| CK-COLOR | Không màu ngoài bảng màu kênh; chấm chạy `#FFE08A` | MUST |
| CK-KARAOKE | Bảng vùng karaoke 0 vi phạm | MUST |
| CK-DET | Không `@keyframes`, `animation:`, `<animate`, `repeat:-1`, `Math.random`, `Date.now`, `requestAnimationFrame` | MUST |
| CK-BRANDS | Mỗi file logo có mục `SOURCES.md` với SHA khớp; SVG không script/`on*=`/href ngoài/`foreignObject` | MUST |
| CK-BG | Dải neuron chỉ bật ở thẻ chương và outro | MUST |
| CK-AUDIO | Đo LUFS/true peak đúng mức; không nhạc khi giọng đang nói | MUST |
| CK-HASH | Giọng và avatar đã duyệt: băm không đổi so với sổ băm của tập | MUST |
| CK-SEG | `segments.json` phủ kín 0 → tổng, ranh trùng mép cảnh | MUST |
| CK-STILL | Không khoảng > 6 s mà cảnh không có tween nội dung (bỏ vòng nền) | SHOULD |

Chưa có script thì ghi `CHƯA KIỂM` cho từng mã, không tính là đạt.

## Sáu câu soi trước khi gửi duyệt

1. Icon nào còn đứng yên, hoặc chỉ lắc/phát sáng cả khối mà các thành phần bên trong không tương tác?
2. Mỗi đối tượng hiện đúng lúc lời nhắc tới nó chưa (theo giờ chữ, không gõ cứng)?
3. Các icon nối nhau có hiệu ứng liên kết chạy liên tục không?
4. Có chỗ trống lệch một bên, hay nội dung chưa phủ vùng an toàn?
5. Có chữ chạm chữ, chạm header, chạm avatar không?
6. Có khoảng nào màn đứng yên quá 6 s?

Gửi kèm: số đo âm của đoạn, băm giọng và avatar cũ không đổi, danh sách icon còn `idle` và logo còn là ô chữ, và nêu rõ thứ chưa làm hoặc chưa đo.
