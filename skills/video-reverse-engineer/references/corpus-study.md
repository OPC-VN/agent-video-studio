# Học từ một bộ video mẫu dài → thư viện mẫu tái dùng

> **Kết luận:** muốn **làm ra nhiều video cùng thể loại**, đừng mổ từng video rồi chép: gom 3–6 video mẫu theo loại, trích dữ liệu bằng máy, cho model rẻ ghi nhật ký cảnh, soi dày quanh chỗ đổi cảnh, rồi chưng cất thành **thư viện mẫu có mã** (bố cục, hình, chữ, chuyển cảnh, công thức ý → hình). Thư viện này là đầu vào của skill `vlog-design`.

Quy trình đã chạy thật trên 5 video giảng dạy / kể chuyện (≈ 78 phút): ra 639 dòng nhật ký cảnh, 45 lưới soi dày ở 5–10 khung/giây (24 dòng ghi chép cơ chế), và 137 mẫu có mã. Số đo ở cuối file.

## Contents
- Khi nào dùng, khi nào không
- Cổng quyền và nơi lưu
- Bước 1 — Gom bộ mẫu
- Bước 2 — Trích dữ liệu bằng máy
- Bước 3 — Nhật ký cảnh (model rẻ, song song)
- Bước 4 — Soi dày chỗ đổi cảnh (model mạnh, tự nhìn)
- Bước 5 — Chưng cất thành thư viện có mã
- Bước 6 — Kiểm chứng và tích hợp vào skill
- Lần sau làm gọn hơn
- Phân vai model
- Số đo và chi phí thực tế
- Cạm bẫy đã gặp

## Khi nào dùng, khi nào không

- Dùng: có nhiều video mẫu dài (≥ 5 phút) cùng thể loại; mục tiêu là **ngữ pháp dựng** (bố cục, chuyển cảnh, cách vẽ ý) để làm loạt video của mình.
- Không dùng: chỉ cần phục dựng **một** video ngắn → `decompose` + `review` ở SKILL.md và `copy-pipeline.md`; chỉ cần bản đồ beat một video → skill `video-reference-analysis`.
- `decompose` của rea-video vẫn dùng được cho từng video, nhưng với video dài, giảng dạy, tiếng Việt thì bộ dò cắt cảnh bỏ sót chuyển mờ/co và OCR/ASR không hỗ trợ tiếng Việt; quy trình dưới đây không phụ thuộc nó.

## Cổng quyền và nơi lưu

- Chỉ dùng tệp người dùng đã tải và có quyền xem để học. **Học ngữ pháp, không chép hình**: không đưa khung hình mẫu vào công cụ tạo ảnh, không dùng lại người, giọng, logo.
- **Khung có mặt người thật** (video mẫu có người dẫn) gửi lên model là gửi dữ liệu nhận diện được: hỏi người dùng trước khi giao bước 3–4 cho các video đó.
- Sau khi thư viện được duyệt: đề nghị xoá `frames/` và `sheets/` (phần lớn dung lượng), chỉ giữ nhật ký, ghi chép và lưới chuyển cảnh; xoá chỉ khi người dùng gật.
- Mọi dữ liệu trích (khung, lời, nhật ký) nằm trong **trạm**: `<trạm>/library/<tên-thư-viện>/evidence/<video>/`. Thư viện chưng cất đưa vào repo phải **viết chung**: không tên kênh, tên người, tên sản phẩm của video mẫu, không đường dẫn máy (`tests/test_no_identity_leak.py` bắt); trích lời ≤ 12 chữ.
- Gán mã video A, B, C… và ghi bảng mã ↔ file trong `README.md` của thư viện ở trạm.

## Bước 1 — Gom bộ mẫu

- Chia theo **chế độ hình** người dùng muốn học, ví dụ: chỉ hoạt họa tối giản · hoạt họa + màn hình · hoạt họa kể chuyện · người + hoạt họa · người + màn hình. Mỗi loại 1–2 video là đủ; hơn 6 video thì lợi giảm mà tốn tăng.
- `video-studio cleanup inspect --input <v> --json` lấy thời lượng, fps, độ phân giải.
- Xong khi: bảng mã video có loại, thời lượng, ngôn ngữ lời.

## Bước 2 — Trích dữ liệu bằng máy

Dùng script [`../assets/corpus_extract.py`](../assets/corpus_extract.py) (chỉ cần ffmpeg; mọi lệnh con là argv list):

| Lệnh | Ra | Ghi chú |
|---|---|---|
| `extract --input V --out EVID/<v>` | `frames/f_NNNN.jpg` (1280px, mỗi 2 s), `sheets/s_NNN.jpg` (lưới 4×4 = 32 s), `cuts.txt` (mốc cắt `scene>0.25`), `index.json` | giây của khung = (NNNN−1)×2; ô k của trang N ở giây (N−1)×32 + 2k |
| `strips --input V --out EVID/<v>/transitions --at t1,t2,…` | `tr_<giây>.jpg`: lưới 6×4 = 2.4 s ở 10 khung/giây quanh mỗi mốc | dùng ở bước 4 |
| `switches --log EVID/<v>/scene-log.md [--per-pair 2]` | mốc đổi chế độ kèm mốc gợi ý cho `strips`; `--per-pair` giữ tối đa N mốc mỗi cặp từ → tới để phủ đều | đọc bảng nhật ký bước 3 |
| `stats --log EVID/<v>/scene-log.md --duration <giây>` | tỉ lệ chế độ, số lần đổi, độ dài cảnh, chỗ hở/chồng, mốc vượt thời lượng (mã 1) | **mọi con số đưa vào thư viện lấy từ đây**, không để model cộng |

- **Lời:** `video-studio reference transcribe` (skill `video-reference-analysis`, mục transcript). Video dài nên chạy một lần nạp model cho cả bộ, chạy nền; faster-whisper large-v3 trên GPU ≈ 1 phút xử lý cho 4–5 phút video.
- **Chữ trên màn hình (OCR):** chỉ là phụ. Windows OCR (`Windows.Media.Ocr`) đọc tiếng Anh ổn, **tiếng Việt sai dấu**; để model nhìn khung đọc chữ thay vì tin OCR.
- Xong khi: mỗi video có `frames/`, `sheets/`, `cuts.txt`, lời có mốc.

## Bước 3 — Nhật ký cảnh (model rẻ, song song)

- Mỗi video giao **một** subagent model rẻ (Haiku) với brief chung [`../assets/scene-log-brief.md`](../assets/scene-log-brief.md), chạy song song, chạy nền.
- Brief bắt buộc: đọc **hết** các trang lưới và lời trước khi kết luận; chuyển động suy từ bước 2 s phải ghi «suy từ bước 2 s»; được mở tối đa ~40 khung lớn cho chữ nhỏ; trích lời ≤ 12 chữ.
- Bảng nhật ký: `# | thời gian | chế độ (P/PA/A/S/PS/AS) | bố cục | phần tử | chữ trên hình | chuyển động trong cảnh | chuyển sang cảnh sau | ý nói | ý → ẩn dụ hình`, rồi danh mục mẫu, nhịp, 10 công thức.
- Dặn rõ **60–120 dòng** (gộp nhịp 2 s); không dặn thì model ghi quá vụn (đã gặp 176 dòng).
- Xong khi: mỗi video có `scene-log.md`; `stats --duration` thoát 0 (không mốc vượt thời lượng), chỗ hở/chồng đã xem; đọc lướt bảng kiểm chế độ có hợp lý (xem cạm bẫy).

## Bước 4 — Soi dày chỗ đổi cảnh (model mạnh, tự nhìn)

Nhật ký 2 s **không thấy cơ chế chuyển** (blur 0.1 s, người co thành PIP 0.3 s đều lọt giữa hai khung). Bước này phân biệt thư viện «có tên hiệu ứng» với thư viện «dựng lại được».

1. `switches --per-pair 2` lấy mốc đổi chế độ, **cả hai chiều** của mỗi cặp (ví dụ P → PS và PS → P: hai chiều có thể khác hẳn nhau); video không người thì lấy rải 6–8 mốc trong `cuts.txt` và vài mốc có chuyển động trong cảnh. Mốc nhật ký sai ±2–4 s: nếu lưới không bắt được chuyển, dời mốc ±2 s và cắt lại.
2. `strips` ở 10 khung/giây (video kể chuyện chuyển chậm: 5 khung/giây, cửa sổ 4.8 s).
3. Model mạnh (Opus) **tự nhìn** từng lưới, ghi `transitions/TRANSITIONS.md`: mốc, từ → tới, cơ chế theo 0.1 s (blur bao nhiêu, co về đâu, bo góc, thứ tự lớp), rồi 3–5 điều rút ra.
4. Khi nhật ký nói «cắt cứng» mà lưới dày cho thấy blur/co: **theo lưới dày**.
5. **Mỗi lưới đã cắt phải có một dòng ghi chép** (kể cả «không thấy chuyển»); lưới không ghi là công phí.
- Xong khi: mỗi kiểu đổi chế độ chính có ít nhất một mốc đo **mỗi chiều**; số lưới = số dòng ghi chép.

## Bước 5 — Chưng cất thành thư viện có mã

- **Chốt bảng mã trước khi giao** để nhiều subagent viết song song mà không lệch: LY bố cục · TR chuyển cảnh · VO vật thể/icon/người · MO chuyển động giữa khối · TX hiệu ứng chữ · IG dựng infographic/sơ đồ · ST thiết bị kể chuyện · RC công thức ý → hình. Ghi sẵn danh sách LY và TR (tên + nghĩa); subagent chỉ được thêm mã mới ở cuối dãy.
- Giao 2 subagent model trung (Sonnet) song song bằng brief chung [`../assets/synthesis-brief.md`](../assets/synthesis-brief.md): một bên LY + TR, một bên VO + MO + TX + IG + ST + RC.
- Mỗi mẫu đủ 6 trường: **trông thế nào** (vị trí %, cỡ) · **chuyển động** (trước → sau, giây, easing gợi ý) · **khi dùng** · **tránh** · **bằng chứng** (mã video + mốc, ví dụ «E tr 38.6») · **gợi ý dựng** (CSS/GSAP 1–3 dòng).
- Xong khi: mọi mã được dùng đều có định nghĩa; mọi mẫu có bằng chứng hoặc ghi «suy ra».

## Bước 6 — Kiểm chứng và tích hợp vào skill

- **Thư viện đã có** (học thêm một hay nhiều video): bước 5 ra một gói mẫu mỗi video (`../assets/reference-patterns.md`) rồi gộp theo [`library-merge.md`](library-merge.md); không ghi thẳng thư viện. Khuôn mẫu, độ tin, luật mã: `skills/vlog-design/references/library-contract.md`.

- **Kiểm chứng trước khi tích hợp:** Opus rút ngẫu nhiên ≈ 10% mẫu, mở khung/lưới ở mốc bằng chứng, đối chiếu mô tả; mọi con số phải có nhãn đo / ước / suy ra; mã bố cục gán trong công thức phải khớp loại video làm bằng chứng (ví dụ không gán bố cục «thế giới minh hoạ» cho bằng chứng từ video UI mock).
- **Phản biện độc lập:** một model khác (Fable) review thư viện + skill trước khi dùng thật; lần đầu chạy quy trình này, review bắt được: cổng nhịp mâu thuẫn số đo, một mốc vượt thời lượng video, nhãn chế độ sai làm lệch tỉ lệ, chiều quay về toàn khung chưa đo (đo xong thì ngược với giả định).

- Thư viện vào `skills/<skill-đích>/references/`; skill đích có quy trình dùng thư viện, mẫu điền và script kiểm (ví dụ `vlog-design` có `pace_check.py`).
- Kiểm trước khi giao:
  - mã: mọi `XX-NN` được nhắc đều có định nghĩa (grep tiêu đề hoặc dòng in đậm);
  - danh tính: grep tên kênh/người/sản phẩm của bộ mẫu và đường dẫn máy; chạy `tests/test_no_identity_leak.py`;
  - repo: `python scripts/build_host_adapters.py`, `python scripts/skill_counts.py --check`, `python -m pytest -q`;
  - skill: `studio.py validate <skill> --require-evals` (skill `create-skill` của OpcOS).

## Lần sau làm gọn hơn

| Đổi | Vì sao | Trạng thái |
|---|---|---|
| Lấy khung theo cảnh (mốc cắt + sai khác khung, 1–2 khung đại diện mỗi đoạn) thay vì đều 2 s | video giảng dạy có nhiều đoạn tĩnh dài; giảm ảnh cho model rẻ | chưa đo mức giảm |
| Lưới 3×3 ô 640 px thay 4×4 ô 480 px | model rẻ đọc được chữ nhỏ, bớt phải mở khung lớn | chưa thử |
| `stats` trước khi chưng cất | số tỉ lệ, số đếm do máy tính | đã có |
| `switches --per-pair 2`, soi cả hai chiều | phủ đều kiểu chuyển, tránh suy diễn chiều ngược | đã có |
| Chốt định nghĩa chế độ trong brief (P = người toàn khung kể cả chữ nổi; slide = A; giao diện thật = S) | tránh lệch tỉ lệ giữa các video | đã có trong `scene-log-brief.md` |

## Phân vai model

| Việc | Model | Lý do |
|---|---|---|
| Đọc lưới, ghi nhật ký cảnh | Haiku | nhiều ảnh, việc mô tả; rẻ, song song |
| Soi chỗ đổi cảnh, chốt bảng mã, tích hợp, kiểm | Opus | cần nhìn chính xác và quyết định |
| Chưng cất thư viện | Sonnet | viết dài có cấu trúc từ nhật ký |
| Phản biện thư viện và skill | Fable | góc nhìn độc lập trước khi dùng thật |

## Số đo và chi phí thực tế

Bộ 5 video, ≈ 78 phút, máy có GPU.

| Hạng mục | Đo được |
|---|---|
| Trích khung + lưới (song song 5 video) | 2 346 khung, 148 trang lưới; vài phút |
| Lời (faster-whisper large-v3, GPU, chạy nền) | ≈ 15–20 phút cho cả bộ |
| OCR Windows | vài phút; chữ Việt sai dấu |
| Nhật ký cảnh Haiku (5 subagent) | 5,7–18 phút mỗi video; ≈ 250–330 nghìn token mỗi video |
| Soi dày (Opus tự nhìn) | 45 lưới cắt, 24 dòng ghi chép (8 lưới của B chưa ghi); mỗi lưới ≈ 1 lượt đọc ảnh |
| Chưng cất Sonnet (2 subagent) | ≈ 5 phút mỗi bên; ≈ 175–205 nghìn token |
| Dung lượng bằng chứng trong trạm | ≈ 175 MB |

## Cạm bẫy đã gặp

- **Chế độ bị gán nhầm:** người cột bên + slide bị ghi «PS» (người + màn hình) thay vì «PA». Định nghĩa rõ trong brief: slide/hoạt họa = A, giao diện phần mềm thật = S.
- **Lời và hình lệch thứ tự** ở video quay màn hình: lời nói một thao tác, hình chiếu thao tác đó sau 1–2 phút. Lấy lưới làm trục thời gian.
- **Mốc thời gian từ lưới sai ±2–4 s**; mốc trong ghi chép soi dày chính xác ±0.1–0.2 s. Trích bằng chứng ghi rõ loại.
- **Thư viện cuDNN/cuBLAS** của faster-whisper có thể thiếu trên Windows: thêm thư mục DLL của torch trong một venv có sẵn bằng `os.add_dll_directory` (đặt qua biến môi trường, không hardcode).
- **Chiều quay về khác chiều đi:** người rời toàn khung bằng co có chuyển động, nhưng quay về toàn khung bằng **cắt cứng** (đo ở 3 mốc). Suy chiều ngược «đối xứng» là sai; phải đo.
- **Console Windows cp1252** không in được tiếng Việt: script phải `sys.stdout.reconfigure(encoding="utf-8")`.
- **Hook chặn lệnh shell dài** khi subagent ghi file: dặn subagent ghi bằng công cụ Write.
- Model rẻ đọc ảnh lưới nhỏ **không đọc được chữ nhỏ**: cho phép mở khung lớn có giới hạn số lượng.
