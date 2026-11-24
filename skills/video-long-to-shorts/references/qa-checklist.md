# Kiểm chất lượng short: cổng tự động và mắt, tai người

> **Kết luận:** ba lớp kiểm theo thứ tự rẻ → đắt: (1) `gap_scan.py` trên `layout.json` trước khi chụp ảnh, (2) tự soi bảng ảnh tĩnh trước khi gửi Cổng 2, (3) `qa_short.py` + người nghe, người xem sau render. Lớp máy không thay lớp người; mục chưa làm ghi «chưa kiểm».

## Contents
- Hợp đồng `layout.json`
- Lớp 1 — rà bố cục bằng máy
- Lớp 2 — tự soi ảnh tĩnh trước Cổng 2
- Lớp 3 — sau render
- Mắt và tai người
- Mẫu báo kết quả

## Hợp đồng `layout.json`

Script dựng của short ghi file này **cùng lúc** sinh HTML, từ chính danh sách phần tử nó đặt lên khung (không gõ tay lần hai).

```json
{
  "frame": {"w": 1080, "h": 1920},
  "duration": 46.5,
  "zone": {"y0": 200, "y1": 1500},
  "skip": [[0, 2.0], [44.0, 46.5]],
  "elements": [
    {"id": "post", "asset": "icons/post.png", "role": "icon",
     "t_in": 8.9, "t_out": 14.6, "cx": 330, "cy": 520, "w": 420, "h": 400}
  ],
  "scenes": [
    {"id": "A1", "t_in": 0.3, "t_out": 8.3, "layout": "V1", "motion": "flow-down"}
  ]
}
```

| Trường | Nghĩa |
|---|---|
| `zone` | vùng hoạt họa theo trục y; short có avatar suốt thì đặt `y1` ≈ 1080 |
| `skip` | khoảng chỉ có hook hoặc thẻ kết, không rà khoảng trống |
| `elements[].role` | `icon` (mặc định) · `logo` · `media` · `avatar` · `link` · `text` |
| `elements[].asset` | đường file hình; dùng để bắt lặp trong một khung |
| `elements[].allow_repeat` | `true` khi lặp là cố ý (dãy ô giống nhau của một icon) |
| `cx`, `cy`, `w`, `h` | tâm và kích thước **ở trạng thái ở lại lâu nhất**; phần tử vào lớn rồi thu về lưới thì khai hai phần tử nối tiếp nhau về thời gian |
| `scenes[].layout` / `motion` | mã mẫu V0–V9 và tên kiểu chuyển động chính của cảnh |

## Lớp 1 — rà bố cục bằng máy

```text
python <skill>/scripts/gap_scan.py <short>/layout.json --json
```

| Kiểm | Mức | Ngưỡng mặc định |
|---|---|---|
| Vùng hoạt họa trống (không icon/logo/media rộng ≥ 300 px) | lỗi | liên tục > 1,0 s, bước rà 0,5 s |
| Cùng một `asset` hai lần trong một khung | lỗi | bất kỳ bước nào |
| Khung có `media` mà còn icon/logo khác | lỗi | bất kỳ bước nào |
| Quá 2 cảnh liền cùng `motion` | lỗi | `--max-run 2` |
| Nội dung phủ < 45 % chiều cao vùng (có trên thiếu dưới) | cảnh báo | liên tục > 1,0 s |
| Tâm nội dung lệch ngang > 140 px khi không avatar | cảnh báo | liên tục > 1,0 s |
| Quá 2 cảnh liền cùng `layout` | cảnh báo | `--max-run 2` |

Ngưỡng 300 px và 1,0 s rút từ đợt dựng đã duyệt. Hai ngưỡng 45 % và 140 px là **điểm khởi đầu chưa hiệu chỉnh** trên nhiều short: cảnh báo thì nhìn ảnh tĩnh rồi quyết, và ghi lý do nếu giữ nguyên.

Một cách đo bổ sung trên ảnh thật (chưa có script trong skill): chụp mỗi 0,5 s, tính tỉ lệ điểm sáng trong vùng hoạt họa; dưới 2,5 % kéo dài hơn 1 s là khung trống.

## Lớp 2 — tự soi ảnh tĩnh trước Cổng 2

Chụp một khung cho **mỗi cụm phụ đề đổi ý** (thường 20–30 khung cho 40–70 s), ghép bảng có nhãn giây. Soi từng khung theo mười câu:

1. Vùng hoạt họa có phủ đều trên–dưới, trái–phải không? Có khung nào trống hoặc chỉ có icon nhỏ ở góc?
2. Icon đang hiện có đúng là thứ **câu phụ đề của khung đó** đang nói không?
3. Có chip chữ, nhãn nào ngoài phụ đề, hook, thẻ kết không?
4. Có asset nào xuất hiện hai lần trong khung không?
5. Logo hãng: chỉ hãng được nhắc tên, đúng beat?
6. Các icon có quan hệ đã có đường nối chưa; hướng đúng nghĩa chưa (so hai khung cách 0,2 s)?
7. Avatar nhỏ, đúng vị trí theo bố cục, không chạm icon chính, phụ đề không đè mặt?
8. Phụ đề một dòng, trong x 60–960, sát đáy, từ đang đọc được tô?
9. Khung có video/ảnh lồng: chỉ còn media, phụ đề, avatar?
10. Màu: có màu nào ngoài bảng màu kênh không? Icon phóng lớn có bị mềm?

Kèm bảng ảnh khi gửi: danh sách icon chính còn ở mức sàn, icon tạm, cảnh báo `gap_scan` giữ lại và lý do. Ảnh tĩnh không cho thấy chuyển động: mô tả một dòng cho mỗi icon chính «thành phần nào làm gì».

Giữ bảng ảnh của mọi vòng (`contact-v1.png`, `contact-v2.png`…) để người duyệt so.

## Lớp 3 — sau render

```text
python <skill>/scripts/qa_short.py <short>/out/<mã>.mp4 --json
```

| Kiểm | Mặc định | Đổi khi |
|---|---|---|
| Khung | 1080×1920 | nền tảng khác tỉ lệ |
| Tốc độ khung | 30 fps | — |
| Thời lượng | 15–90 s | lời gốc dài: nới `--max-dur`, ghi lý do |
| Âm lượng tích hợp | −14 ± 1 LUFS | kênh có mức riêng: `--lufs`, `--lufs-tol` |
| True peak | ≤ −1,0 dBTP | — |
| Lời vào | tiếng đầu ≤ 0,5 s | có nhạc vào từ 0 s thì kiểm này đo nhạc; kiểm lời bằng `beats.json` (`lead` ≤ 0,5) |

Cùng lượt: lint composition 0 lỗi; tua ngược ra cùng khung (hai lượt chụp đảo thứ tự trùng nhau); băm file giọng và take avatar nguồn không đổi.

## Mắt và tai người

| Việc | Ai | Ghi lại |
|---|---|---|
| Nghe mọi điểm cắt giữa lời liền và mối nối rút khoảng lặng | người | mốc giây + đạt/vấp |
| Xem khớp môi avatar ở đoạn cắt giữa take | người | mốc giây |
| Xem trên điện thoại thật: phụ đề có bị giao diện nền tảng che, chữ đọc được | người | ảnh chụp màn hình |
| Chuyển động icon có «sống», có gắt, có lặp nhàm | người duyệt | góp ý theo mốc giây |
| Mức nhạc so với giọng trên loa điện thoại | người | đạt/giảm |
| Giấy phép nhạc, điều khoản logo | người dùng | nguồn + ngày |

Agent tự xem ảnh tĩnh và tự đọc số đo được; agent không tự nhận đã nghe hay đã xem trên điện thoại.

## Mẫu báo kết quả

```text
SH-A · 46,5 s · vòng v4
Máy:   gap_scan 0 lỗi, 1 cảnh báo (lệch ngang 12–14 s: có chủ ý, cột icon bù avatar)
       qa_short đạt: 1080×1920 · 30 fps · −14,1 LUFS · TP −1,4 · tiếng đầu 0,00 s (nhạc), lời 0,30 s
Người: duyệt ảnh tĩnh — «…» (nguyên văn, ngày)
Chưa kiểm: nghe điểm cắt 0,3 s và 37,7 s · xem trên điện thoại · giấy phép nhạc
```
