# Sáng tạo icon và ẩn dụ hình theo lời thoại

Cách đạo diễn biến một transcript **chủ đề mới** thành danh mục icon, ẩn dụ hình và chuyển động đúng nội dung, trong khi theme và format của kênh giữ nguyên. Rút từ một tập explainer có avatar đã được chủ kênh duyệt. Luật dựng (MUST/SHOULD, mã kiểm) ở [motion-layout-standard](motion-layout-standard.md); trình tự làm việc với chủ ở [storyboard-stills-first](storyboard-stills-first.md). Kênh có `channels/<kênh>/STYLE-GUIDE.md` thì màu, họ icon và kit của kênh thắng.

## Mục lục

- [Nguyên tắc](#nguyên-tắc)
- [Năm bước từ transcript tới đặc tả](#năm-bước-từ-transcript-tới-đặc-tả)
- [Icon động đạt khi các thành phần bên trong tương tác](#icon-động-đạt-khi-các-thành-phần-bên-trong-tương-tác)
- [Thư viện motion liên kết](#thư-viện-motion-liên-kết)
- [Bảng brainstorm mẫu từ một tập đã duyệt](#bảng-brainstorm-mẫu-từ-một-tập-đã-duyệt)
- [Phân loại nguồn icon](#phân-loại-nguồn-icon)
- [Đặc tả animation từng icon](#đặc-tả-animation-từng-icon)
- [Tự soi trước khi trình](#tự-soi-trước-khi-trình)

## Nguyên tắc

- **Giữ khung, đổi hình.** Theme, bố cục, nhịp chương, kiểu liên kết dùng lại; icon và ẩn dụ phải sinh ra từ lời thoại của tập này. Không bê icon tập trước sang chỉ vì đã có bản động.
- **Hình trả lời câu «người xem cần thấy gì để hiểu câu này?»**, không minh hoạ từ khoá. Câu nói về thay đổi thì hình phải thay đổi; câu nói về quan hệ thì hình phải có liên kết.
- **Mỗi icon là một cỗ máy nhỏ:** nghĩa nằm ở thành phần bên trong đang làm việc (cột tăng giảm, thẻ đổi cột), không ở việc cả khối lắc hay phát sáng.
- **Mọi liên kết đều sống:** đã vẽ đường nối thì có thứ chạy trên đường đó suốt thời gian hai đầu cùng hiện.

## Năm bước từ transcript tới đặc tả

1. **Tách ý.** Chia transcript theo câu hoặc cụm ý (một ý ≈ 3–8 s lời). Mỗi ý ghi: lời nguyên văn, ý chính bằng một động từ + một danh từ («dữ liệu chảy vào báo cáo»), loại ý: *vật · hành động · quan hệ · so sánh trước/sau · liệt kê · số liệu · tên hãng/sản phẩm · cảm xúc/lời mời*.
2. **Brainstorm rộng.** Mỗi ý viết **2–3 ẩn dụ khác họ** (vật thật · sơ đồ · nhân vật làm việc · giao diện thật · biểu đồ). Với từng ẩn dụ ghi luôn: thành phần nào bên trong chuyển động, liên kết với hình nào, bố cục. Dùng bảng sáu cột:

   | Lời thoại | Ý chính | 2–3 ẩn dụ icon | Tương tác bên trong icon | Motion liên kết | Bố cục |
   |---|---|---|---|---|---|

3. **Chọn.** Mỗi ý một ẩn dụ, theo thứ tự ưu tiên: đúng nghĩa câu → người xem nhận ra trong 1 s ở 360p → có thành phần bên trong để tương tác → khác kiểu chuyển động với hai cảnh liền trước → rẻ (có sẵn). Ghi một dòng lý do loại cho ẩn dụ bỏ. Icon quen của thư viện chỉ dùng khi thắng ở tiêu chí đầu; không hợp thì tạo mới.
4. **Phân loại nguồn** cho từng icon đã chọn (bảng [Phân loại nguồn icon](#phân-loại-nguồn-icon)), gom icon tạo mới thành lô để sinh một lượt.
5. **Đặc tả animation** từng icon theo [mẫu](#đặc-tả-animation-từng-icon), rồi mới dựng khung tĩnh.

Đầu ra là một file `brainstorm.md` trong project (bảng bước 2 có cột «chọn / loại + lý do», bảng nguồn, bảng đặc tả). Storyboard tĩnh lấy hình từ file này.

## Icon động đạt khi các thành phần bên trong tương tác

**MUST:** icon là chủ thể của câu đang nói phải có **ít nhất hai thành phần bên trong** chuyển động theo nghĩa của vật, tác động lên nhau hoặc lệch pha nhau. Quầng thở, vệt sáng, trôi, lắc, phóng to thu nhỏ cả khối chỉ là sàn (`idle`) cho icon phụ hoặc icon chưa tới lượt; icon chính còn ở mức sàn thì ghi vào danh sách nợ khi gửi duyệt.

| Loại icon | Tương tác bên trong (đạt) | Chỉ là sàn (chưa đạt) |
|---|---|---|
| Lịch | các ô ngày dời chỗ, sắp xếp lại; một ô được đánh dấu rồi nhảy sang tuần sau | cả tờ lịch lắc |
| Cơ sở dữ liệu | chấm chạy trong ống nối; khối sáng trượt lên xuống trong trụ | trụ phát sáng |
| Dashboard | cột tăng giảm so le; đường xu hướng vẽ lại; con trỏ bấm một ô làm ô đó đổi | cả bảng thở |
| Kanban | thẻ rời cột này lắp vào cột kia; hai thẻ đổi chỗ | bảng trôi lên xuống |
| Infographic / sơ đồ | luồng sáng đi qua từng khối theo thứ tự đọc | vệt sáng quét cả hình |
| Checklist | dấu tick vẽ lần lượt, nghỉ, xoá, lặp | tờ giấy nhấp nháy |
| Bánh răng / quy trình | bánh này quay kéo bánh kia; mũi tên chuyển sáng giữa hai trạng thái | quầng sáng quanh cụm |
| Nhân vật / robot | bộ phận làm đúng nghề (lật trang, sập clapper, gõ phím), đèn tín hiệu nháy lần lượt | cả nhân vật nhún |

**Đo được (mã `CK-ICON-PARTS`):** trong một chu kỳ lặp, (a) có ≥ 2 tween trên **phần tử con** của icon, khác selector, khác pha hoặc khác thuộc tính; (b) so khung `t` với `t + nửa chu kỳ` sau khi bỏ dịch chuyển của gốc icon: vùng pixel đổi nằm trong hộp của các thành phần, không phủ cả icon; (c) hộp bao của icon trôi ≤ 6 px. Ngưỡng khởi điểm cho (b): vùng đổi chiếm 3–60 % diện tích alpha của icon; ngưỡng này **chưa hiệu chỉnh trên bộ icon thật**, kênh đo lại rồi ghi số của mình.

Cách làm không đổi hình đã duyệt: ảnh gốc giữ nguyên từng pixel; cắt thành phần ra lớp riêng theo alpha, phủ miếng xoá ở chỗ cũ, tween lớp cắt. Icon mới thì xin luôn ảnh «bung lớp» (nền + từng phần rời) để khỏi phải vá.

## Thư viện motion liên kết

Mọi công thức: vòng lặp hữu hạn tính từ cửa thời gian (`repeat = floor((t1 − t0) / chu kỳ) − 1`), mỗi đợt một tween, gắn `data:'loop'`, giá trị đầu tường minh. Màu vật chạy và nền đường theo kênh. Bản mô tả code ở `video-theme-library` → `references/gsap-recipes.md`.

| Công thức | Hình | Dùng khi lời nói về | Tham số chính |
|---|---|---|---|
| Chấm chạy | dải chấm mờ, từng chấm sáng lần lượt theo hướng | dòng chảy, chuyển giao A → B | số chấm, chu kỳ ≈ 1,2–1,4 s, độ trễ giữa chấm |
| Mũi tên chạy | chấm chạy + chevron ở đầu | thứ tự, bước kế tiếp | như trên; chevron chỉ hiện khi đích đã hiện |
| Đổi chiều dòng | cùng dải chấm, đảo hướng tại một mốc lời | «ngược lại», «quay về», đổi vai nguồn–đích | mốc đổi lấy từ giờ chữ |
| Vòng nét đứt quay | vòng tròn nét đứt xoay quanh ô đang nói | «đang nói tới cái này», trạng thái hoạt động | bán kính, 1 vòng / ≈ 6 s |
| Đốm sáng chạy vòng | đốm chạy trên quỹ đạo quanh cụm icon, nằm **dưới** icon | một trung tâm điều phối nhiều thành viên | chu kỳ vòng, số đốm |
| Photon trên dây cong | hạt sáng chạy dọc dây nối nút với lõi | mạng, tích hợp, gọi qua lại | chu kỳ ≈ 2,4 s lệch pha theo chỉ số; hạt nổi bật khi nhánh được nhắc |
| Ribbon | dải cong nối các lớp của hai cột | cùng thành phần, tỉ lệ khác nhau | vẽ **sau** khi cột mọc xong |
| Dây chạm lát | dây chấm từ icon tới đúng lát biểu đồ | «phần này thuộc về…» | đầu dây chạm đúng lát theo tỉ lệ thật |
| Vòng kín kết cảnh | dải chấm nối thành vòng khép qua mọi mục | tổng kết, «tất cả cùng nhau» | thêm cung về để khép vòng |
| Vạch bám vật | vạch kéo dài theo playhead / vật đang đi | tiến độ theo thời gian | mép vạch trùng vật ≤ 2 px |

Chọn liên kết theo **nghĩa quan hệ** trong câu, rồi mới tới thẩm mỹ. Không lặp một công thức quá hai cảnh liền; cảnh nhiều liên kết thì chỉ một cái nổi (màu ấm), phần còn lại mờ.

## Bảng brainstorm mẫu từ một tập đã duyệt

Tập giới thiệu series của một kênh về AI (≈ 9 phút, 30 cảnh). Cột ẩn dụ ghi cái **đã chọn** trước, cái bị loại trong ngoặc. Dùng làm mẫu cách nghĩ, không làm kho icon cho tập khác.

| # | Lời thoại (rút) | Ý chính | Ẩn dụ (đã chọn · đã loại) | Tương tác bên trong icon | Motion liên kết | Bố cục |
|---|---|---|---|---|---|---|
| 1 | «…chia sẻ về data, Power BI…» | nghề gốc: dữ liệu | trụ CSDL + đường ống · (chip chữ «data») | chấm chạy trong ống; dải vàng trượt lên xuống trong hai trụ, lệch pha | — | avatar to giữa, icon bật cạnh theo từng từ |
| 2 | «…chào mừng đến kênh về AI và cộng đồng mới» | chuyển từ cộng đồng cũ sang mới | logo cũ trên, logo mới dưới · (hai chip ngang) | logo giữ nguyên | chấm chạy dọc xuống + chevron, đúng 3 lượt | cột dọc giữa màn |
| 3 | «Data Engineer… Analytics & BI… Project Manager và Business Analyst» | liệt kê các vai đã làm | ô nét đứt rỗng, thẻ lắp vào · (thẻ hiện rồi mất) | thẻ bay vào ô đúng lúc nói | viền vàng nhấp nháy dim ở thẻ đang nói | ba ô cùng tồn tại tới hết cảnh |
| 4 | «…những góc nhìn khác nhau về AI» | nhiều vai góp vào một cái nhìn | pie 40/30/20/10 + 4 icon vai ở 4 góc · (pie chia đều) | dashboard: cột tăng giảm so le, đường xu hướng vẽ lại; kanban: hai thẻ đổi chỗ; checklist: 3 tick vẽ lần lượt | dây chấm từ mỗi icon chạm đúng lát | pie giữa, icon bốn góc |
| 5 | «…mình còn là giảng viên, đứng lớp cho ngân hàng, viễn thông, sản xuất» | dạy cho nhiều ngành | bục + bảng · (người cầm micro) | cột biểu đồ trên bảng cao lên thấp xuống | — | icon chính + 3 thẻ ngành cùng tồn tại |
| 6 | «…không doanh nghiệp nào giống nhau: dữ liệu, văn hoá, tư duy phân tích» | cùng thành phần, tỉ lệ khác | 3 cột chồng dưới 3 icon ngành · (3 chip chữ) | cột mọc theo lớp | ribbon nối lớp giữa các cột, vẽ sau khi cột mọc | legend ngay dưới icon |
| 7 | «…dùng mô hình local, không cần Gemini, ElevenLabs, Claude» | máy tại nhà so với dịch vụ lớn | PC có GPU + mạng neuron + 3 logo thật · (đám mây bị gạch chéo) | PC: lõi chip thở, chân chip chạy sáng, đèn trạng thái nháy; neuron: photon chạy dọc dây, nút nhấp so le | mỗi ô logo nối nút neuron gần nhất bằng 4 chấm | PC trái, mạng + logo phải; «không cần» = mạng mờ đi, logo không gạch |
| 8 | «…một số khung cảnh chưa được ưng lắm» | tự nhận điểm yếu của chính video | 3 khung video thật cắt từ bản đang dựng · (khung giả có nút play) | clip chạy trong khung | nút play nhảy 1 → 2 → 3, viền vàng khung đang nói | ba khung ngang |
| 9 | «Trước đây chia sẻ…, rồi công việc cuốn mình đi» | thời gian trôi, việc chia sẻ đứt quãng | trục thời gian + playhead · (tờ lịch) | playhead chạy; icon việc rơi xuống trục | vạch gạch bám đúng playhead | trục ngang giữa màn |
| 10 | «…dễ hơn, tiết kiệm thời gian, đóng gói giải pháp» | ba lợi ích | bóng đèn · thanh thời gian · hộp đóng gói | đèn: năm tia nháy lần lượt; thanh co 1 → 1/3; hộp: mũi tên rơi vào miệng hộp | viền vàng theo cột đang nói | ba cột cùng tồn tại |
| 11 | «Quan trọng nhất là thay đổi tư duy» | cũ → mới | chip cũ · bánh răng · chip mới · (mũi tên đơn) | hai bánh răng luân phiên sáng | bánh răng nằm **giữa** hai trạng thái | ba phần tử cùng trục dọc |
| 12 | «…một người tổ chức một đội quân AI» | một người điều phối nhiều agent | người + robot ở tâm, 6 robot quanh vòng · (sơ đồ tổ chức) | ăng-ten các robot nháy lần lượt | vòng tròn vẽ ra, đốm sáng chạy vòng dưới icon | tâm + vòng |
| 13 | «team bài giảng, tiến độ, dữ liệu, lập trình, video, nhạc» | liệt kê đội theo việc | hàng robot, mỗi con một nghề | dim thì đứng yên; sáng lên mới làm đúng nghề (lật trang, sập clapper…) | sáng lần lượt theo lời | một hàng, giãn đều |
| 14 | «…không phải vài video rời rạc mà là chuỗi có thứ tự» | rời rạc → có thứ tự → leo dần | 4 ô video lệch xoay rồi xếp thẳng + bậc thang có người leo · (danh sách đánh số) | ô xoay về thẳng hàng; người nhảy 3 bậc, bậc sáng dần | mũi tên + chấm chạy giữa các ô và tới thang | hàng ô trái, thang phải |
| 15 | «…nền tảng open source tích hợp rất nhiều repo» | sản phẩm của chính mình | giao diện thật của sản phẩm: quả cầu lưới + nhánh + lõi · (hộp mở + chip «repo») | cầu xoay; mỗi lúc một nhánh sáng theo lời | photon chạy trên dây về tâm | sân khấu đối xứng |
| 16 | «…chưa dùng Claude, Codex… thì tìm hiểu thêm trên YouTube» | chỉ đường cho người mới | biển chỉ đường + 4 logo thật lắp vào ô · (kính lúp một mình) | logo lắp vào ô nét đứt đúng tên được nói | chấm chạy biển → ô, rồi **đổi chiều** ô → kính lúp ở «tìm hiểu thêm» | biển giữa, logo hai bên |
| 17 | «…theo dõi qua nhóm, kênh video, website, khoá học» | bốn kênh, mỗi kênh một việc | 4 ô kênh · (4 logo đứng yên) | bong bóng bình luận nổi; thanh tiến độ chạy; chữ gõ dần; tick lần lượt | mũi tên chạy giữa ô + vòng nét đứt quay ở ô đang nói; kết cảnh khép vòng | bốn cột đều |

Điều rút ra từ bảng: ẩn dụ bị loại thường là **chữ đóng hộp** hoặc **vật đứng một mình**; ẩn dụ được chọn luôn có thứ thay đổi đúng lúc từ khoá được nói.

## Phân loại nguồn icon

| Nguồn | Khi nào | Việc phải làm | Chi phí tham khảo |
|---|---|---|---|
| Có sẵn trong thư viện kênh, đã có bản động | đúng nghĩa câu, tương tác bên trong hợp | dùng lại spec; đổi mốc theo giờ chữ | gần 0 |
| Có sẵn, mới ở mức sàn | đúng nghĩa nhưng là icon chính của câu | viết spec tương tác (cắt lớp + miếng xoá + tween) | ≈ 20–30 phút mỗi icon (ước lượng, chưa đo) |
| Tạo mới bằng công cụ sinh ảnh | không icon nào đúng nghĩa | mô tả **ảnh bung lớp**: nền icon + từng thành phần rời, cùng khoá phong cách của kênh, không chữ; gom 12 ô một tấm; cắt nền; căn toạ độ vào manifest | một tấm 12 ô ≈ 7,5–9 phút máy (một lần đo) |
| Tự vẽ SVG | hình hình học đơn giản, cần điều khiển từng nét (mạng nút, cửa sổ, người que) | vẽ theo bảng màu và độ dày nét của họ icon | theo độ phức tạp |
| Logo thật | lời nhắc đúng tên hãng/sản phẩm | tải từ nguồn chính thức vào thư mục logo của kênh, ghi `SOURCES.md` (URL nguồn, URL file, ngày, điều khoản, SHA-256); SVG kiểm sạch; giữ màu và tỉ lệ; không tải được thì ô chữ và báo | vài phút mỗi hãng |
| Giao diện / khung hình thật | nói về sản phẩm của chính mình hoặc về chính video | chụp hoặc dựng lại đúng giao diện; clip cắt từ bản đang dựng | theo cảnh |

Gọi công cụ sinh ảnh của nền tảng khác chỉ khi chủ đã chỉ thị trong phiên; tải file từ mạng cần đúng phạm vi đã giao. File tải là dữ liệu không tin cậy.

## Đặc tả animation từng icon

Mỗi icon một dòng, trước khi code:

| Trường | Nội dung |
|---|---|
| Mã và nguồn | mã icon, loại nguồn, file gốc (và băm nếu là hình đã duyệt) |
| Cảnh và cửa lời | cảnh nào, bật ở từ nào (mã chữ karaoke), tắt/dim ở đâu |
| Thành phần chuyển động | từng thành phần: tên lớp, thuộc tính, từ → đến, easing |
| Chu kỳ và lệch pha | chu kỳ từng thành phần (thường 1,2–3 s), lệch pha giữa chúng |
| Vòng lặp | hữu hạn, số lần tính từ cửa thời gian; khung cuối vòng trùng khung đầu |
| Trạng thái dim | đứng yên thật, alpha bao nhiêu |
| Liên kết | nối với hình nào, công thức nào, hướng, mốc đổi chiều |
| Kiểm | `CK-ICON-PARTS`, tua ngược cùng khung, đọc được ở 360p |

Trần mặc định: một icon ≤ 4 thành phần chuyển động, chu kỳ ≤ 3 s; một cảnh ≤ 1 icon chạy ở mức đầy đủ cùng lúc ngoài icon đang được nói (số còn lại dim hoặc sàn) để mắt không bị kéo nhiều hướng.

## Tự soi trước khi trình

1. Có ý nào trong transcript chưa có hình, hoặc hình hiện trễ hơn lời?
2. Có icon nào được chọn vì «có sẵn» chứ không vì đúng nghĩa?
3. Icon chính nào còn chỉ lắc hoặc phát sáng cả khối?
4. Có đường nối nào đứng yên, hoặc chạy sai hướng so với nghĩa câu?
5. Có ba cảnh liền nào cùng một ẩn dụ hoặc cùng một kiểu chuyển động?
6. Tên hãng nào được nhắc mà chưa có logo thật kèm nguồn?
