# Bố cục dọc 1080×1920: vùng an toàn, phụ đề, avatar và bộ mẫu infographic

> **Kết luận:** mỗi khung là một **infographic dọc**: các điểm có liên kết, đọc theo mạch câu chuyện, phủ đều vùng hoạt họa. Không dồn một bên, không có trên mà thiếu dưới, không khung trống. Chọn mẫu V0–V9 theo **quan hệ giữa các ý trong câu**, không theo thói quen.

Số pixel dưới đây đo trên một đợt dựng ba short đã được duyệt (font đậm không chân, tiếng Việt). Kênh có chuẩn riêng thì chuẩn kênh thắng; nền tảng đổi giao diện thì đo lại bằng ảnh tĩnh.

## Contents
- Khung và các vùng
- Phụ đề
- Avatar
- Luật bố cục
- Bộ mẫu V0–V9
- Chọn mẫu theo quan hệ ý
- Chuyển giữa các mẫu

## Khung và các vùng

```text
 x: 0        60                               960   1080
 y=0    ┌─────────────────────────────────────────────┐
        │  vùng tránh trên (0–230): không đặt gì quan  │
 y=230  │  trọng; tên nền tảng, nút tìm kiếm đè lên    │
        ├───────────────────────────────────────┬─────┤
        │                                       │ cột │
        │   VÙNG HOẠT HỌA                       │ nút │
        │   không avatar: y 200–1500            │ nền │
        │   có avatar:    y 200–1080            │ tảng│
        │                                       │ 120 │
 y=1100 │  ┌──────┐                             │ px  │
        │  │avatar│ · · hàng icon phụ           │     │
 y=1500 │  └──────┘  (tâm y ≈ 1300)             │     │
        ├───────────────────────────────────────┤     │
 y=1590 │   DẢI PHỤ ĐỀ  y 1590–1730, x 60–960   │     │
 y=1730 ├───────────────────────────────────────┴─────┤
        │  mô tả, tên kênh của nền tảng (đè lên hình)  │
 y=1920 └─────────────────────────────────────────────┘
```

- Nội dung phải đọc nằm trong x 60–960. Cột 120 px bên phải dành cho nút của nền tảng: chỉ để nền và quầng sáng.
- 18 % dưới (từ y ≈ 1574) là vùng giao diện nền tảng. Phụ đề sát đáy nằm **trong** vùng này theo lựa chọn của chủ kênh, nên **bắt buộc xem trên điện thoại thật** trước khi đăng; nếu bị che, lùi dải phụ đề lên y 1320–1480 và thu vùng hoạt họa tương ứng.
- Nền: một nền tối đồng nhất + quầng mờ; không lưới dày, không hoạ tiết tranh chỗ với icon.

## Phụ đề

| Thuộc tính | Chuẩn |
|---|---|
| Đơn vị | cụm 3–5 từ, ngắt theo dấu câu; một dòng |
| Cỡ chữ | 64 px đậm (sàn 48 px) |
| Bề rộng | cụm rộng nhất đã đo ≈ 830 px; trần 880 px; tuyệt đối ≤ 960 px. Đo bằng font thật, không ước theo số ký tự |
| Vị trí | dải y 1590–1730, tâm ≈ 1650, căn giữa trong x 60–960 |
| Nền chữ | viên bo tối, độ đục ≈ 85 % |
| Tô từ | từ đang đọc màu nhấn của kênh, còn lại màu chữ sáng; mốc từ theo nhận dạng giọng |
| Chuyển cụm | hiện 0,14 s, tắt 0,12 s; hai cụm không chồng nhau |

Phụ đề là chữ duy nhất chạy suốt short. Không lặp nội dung phụ đề bằng chip chữ ở vùng hoạt họa.

## Avatar

- **Nhỏ, tròn, có viền sáng:** đường kính ≈ 400 px (≈ 37 % bề ngang). Bản đầu để avatar bán thân lớn đã bị trả về vì chiếm hết chỗ của hình.
- **Vị trí theo bố cục:** mặc định **góc dưới trái** (tâm ≈ x 250, y 1300), bên phải nó là hàng icon phụ nối bằng đường chấm. Bố cục đối xứng quanh trục dọc (hub-spoke, tam giác) thì đặt avatar **giữa** hàng dưới (tâm x 540) hoặc bỏ avatar ở cảnh đó.
- Avatar chỉ xuất hiện ở beat mà nguồn có take phủ; cắt giữa take bằng `data-media-start` ([audio-cut-and-sync](audio-cut-and-sync.md)). Vào/ra và đổi vị trí chỉ ở ranh câu.
- Phụ đề không đè mặt avatar; vòng avatar không chạm icon chính (cách ≥ 40 px).
- `<video>` avatar không nằm trong `<section data-start>`; đặt ở lớp gốc, điều khiển hiện/ẩn bằng timeline.

## Luật bố cục

1. **Phủ đều:** nội dung chiếm ≥ 45 % chiều cao vùng hoạt họa tại mọi thời điểm ngoài hook và thẻ kết; có phần tử ở cả nửa trên và nửa dưới của vùng.
2. **Cân trục:** tâm khối nội dung lệch trục dọc ≤ 140 px khi không có avatar. Có avatar bên trái thì khối icon chính bù sang phải hoặc phủ toàn bề ngang phía trên.
3. **Không khung trống:** không quá 1 s mà vùng hoạt họa không có icon rộng ≥ 300 px. Icon nhỏ ở góc không tính là đã lấp.
4. **Liên kết đi theo mạch:** hai điểm có quan hệ trong câu thì có đường nối chạy theo đúng hướng nghĩa (nguồn → đích, tâm → nhánh).
5. **Vào lớn, thu về lưới:** icon của ý đang nói vào ở cỡ lớn giữa vùng (420–600 px), khi ý sau tới thì thu nhỏ về ô lưới của nó (200–300 px) và ở lại tới hết cảnh. Các mục liệt kê cùng tồn tại; mục chưa nhắc là **ô chờ nét đứt**.
6. **Không lặp:** một asset không xuất hiện hai lần trong cùng khung (ví dụ logo một nền tảng vừa ở hàng trên vừa ở hàng phụ). Cần nhắc lại thì di chuyển chính phần tử đó.
7. **Khung media:** có video hoặc ảnh lồng thì media chiếm vùng hoạt họa (mẫu V8); gỡ mọi icon/logo khác, chỉ còn phụ đề và avatar nhỏ.
8. **Chữ:** ngoài phụ đề chỉ có hook (0–2 s) và thẻ kết. Nhãn dưới icon chỉ dùng khi icon không tự nói được và nhãn là từ có trong lời; cỡ ≥ 40 px.

`scripts/gap_scan.py` đo luật 1, 2, 3, 6, 7 và việc lặp kiểu chuyển động từ `layout.json`. Ngưỡng 300 px và 1 s của luật 3 rút từ đợt dựng đã duyệt; 45 % (luật 1) và 140 px (luật 2) là điểm khởi đầu chưa hiệu chỉnh trên nhiều short, nên máy chỉ cảnh báo và người nhìn ảnh tĩnh quyết.

## Bộ mẫu V0–V9

Ký hiệu: `[A]` icon lớn · `(a)` icon nhỏ · `(·)` ô chờ nét đứt · `╎` `┄` đường chấm chạy · `(@)` avatar · `▬▬` phụ đề.

### V0 — Hook (0–2 s)

```text
      [logo kênh]
   CÂU HỎI HAI DÒNG
     dòng nhấn màu
        ▬▬▬▬
```
Câu hỏi ≤ 7 từ, cỡ ≈ 120 px, dòng hai màu nhấn. Lời vào trong 0,5 s đầu; hook mờ dần khi icon đầu tiên vào. Dùng: mọi short.

### V1 — Dọc nhân quả (trên → dưới)

```text
        [A]
         ╎  ↓ chấm chạy xuống
        [B]
         ╎
        (c)
        ▬▬▬▬
```
Dùng khi câu có «từ … sinh ra …», «ngoài A còn B», «A dẫn tới B». A vào trước, đường chạy vẽ sau khi B đã hiện. 2–3 tầng; tầng cuối có thể là logo đích.

### V2 — Hub-spoke quanh tâm

```text
   (·)   (b)   (·)
      ╲   ╎   ╱
   (a) ┄ [TÂM] ┄ (c)
      ╱   ╎   ╲
   (·)   (d)   (e)
        ▬▬▬▬
```
Dùng khi một chủ thể điều phối nhiều thứ: «một người có nhiều đội», «một nền tảng nhiều tính năng». 5–7 nhánh. **Ô chờ hiện trước** đủ số nhánh, mỗi lần lời nhắc tới thì icon lắp vào ô và đường chấm cong chạy từ tâm ra. Tâm ≈ 420 px, nhánh ≈ 240 px.

### V3 — Lưới 2×2 (rồi thu thành hàng)

```text
   [A]    [B]            (a)(b)(c)(d)   ← thu lên hàng trên
                    →         ╎
   [C]    [D]               [ĐÍCH]
        ▬▬▬▬                 ▬▬▬▬
```
Dùng cho 4 mục ngang hàng («bài viết, video, blog và phát trực tiếp»). Mỗi mục vào đúng lúc được đọc; khi câu chuyển sang «tất cả ở một nơi», bốn mục thu thành hàng trên nhường giữa khung cho đích. 3 mục thì dùng V4.

### V4 — Tam giác

```text
          [A]
        ╱     ╲
     [B] ┄┄┄┄ [C]
     (b1)(b2)(b3)    ← hàng dưới: thứ mà cả ba cùng nhận
        ▬▬▬▬
```
Dùng cho 3 vai/3 lựa chọn ngang hàng («chủ doanh nghiệp, quản lý hay nhân viên») dẫn về một kết luận chung ở hàng dưới hoặc ở tâm. Phân biệt ba vai bằng màu bệ/quầng trong bảng màu và đạo cụ riêng.

### V5 — Lộ trình bậc

```text
                 [4]★
            [3]
       [2]            đốm sáng chạy
  [1]                 từ bậc 1 lên bậc đích
        ▬▬▬▬
```
Dùng cho trình tự, cấp độ, «chuỗi bài học có thứ tự», «không dành cho người mới». Bậc đã qua sáng, bậc chưa tới mờ; đốm sáng nhảy theo lời.

### V6 — Trước / sau

```text
   ┌── TRƯỚC ──┐
   │   [A]     │  mờ dần, xám
   └─────╎─────┘
         ▼  thanh quét
   ┌─── SAU ───┐
   │   [B]     │  sáng, có quầng
   └───────────┘
        ▬▬▬▬
```
Dùng cho đối lập «không phải … mà là …», «rời rạc → thành chuỗi». Nửa trên hiện trước; thanh quét hoặc mũi tên chạy xuống đúng từ «mà». Không viết chữ «trước/sau» nếu lời không nói.

### V7 — Hero đơn + hàng phụ

```text
        [  A  ]        một icon 500–600 px,
                       các thành phần bên trong
                       đang tương tác
  (@) ┄┄ (a) ┄ (b)
        ▬▬▬▬
```
Dùng khi câu chỉ có một ý đang được giải thích và có avatar. Hàng phụ bên phải avatar là 1–2 icon nhỏ **của chính beat đó** (nơi diễn ra, thứ được nhắc lại), nối bằng đường chấm chạy từ avatar ra.

### V8 — Media lồng

```text
   ┌─────────────────┐
   │                 │   video hoặc ảnh thật,
   │     MEDIA       │   bo góc, viền sáng,
   │                 │   rộng 900–960 px
   └─────────────────┘
  (@)
        ▬▬▬▬
```
Dùng khi beat nói về một màn hình, bản demo, ảnh thật. **Chỉ có media**, phụ đề và avatar nhỏ; không icon, không logo khác. Media là khung thật cắt từ nguồn, không dựng khung giả.

### V9 — Thẻ kết

```text
      [logo kênh]
   Xem tập đầy đủ
     trên kênh
```
1,5–2,5 s sau chữ cuối của lời. Chữ là lời mời chung, không thêm khẳng định; tên kênh/cộng đồng là thứ đã có trong lời.

## Chọn mẫu theo quan hệ ý

| Quan hệ trong câu | Mẫu | Biến thể có avatar |
|---|---|---|
| nguồn → kết quả, cũ → mới | V1 | cột lệch phải, avatar dưới trái |
| một tâm, nhiều nhánh | V2 | bỏ avatar hoặc avatar làm tâm |
| 4 mục ngang hàng | V3 | lưới ở nửa trên, avatar dưới trái |
| 3 mục ngang hàng → một kết luận | V4 | avatar giữa hàng dưới |
| thứ tự, cấp độ | V5 | bậc thang nửa trên |
| đối lập | V6 | chỉ nửa «sau» ở lại khi avatar vào |
| một ý được giải thích | V7 | mặc định |
| màn hình, ảnh thật | V8 | avatar nhỏ dưới trái |

Một beat dài (> 8 s) có thể đi qua hai mẫu (V3 → V1 khi bốn mục gom về một đích).

## Chuyển giữa các mẫu

- Phần tử dùng tiếp thì **di chuyển**, không tắt rồi hiện lại (icon chính thu về hàng phụ; tâm của V2 thành đỉnh của V4).
- Không lặp một kiểu chuyển động quá 2 cảnh liền; ghi `motion` của từng cảnh vào `layout.json` để máy bắt.
- Khoảng giữa hai beat (0,25–0,35 s im) là lúc đổi bố cục; không đổi bố cục giữa một cụm phụ đề.
