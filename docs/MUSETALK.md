# MuseTalk 1.5 trên Windows

Lệnh `video-studio avatar` nhận footage hoặc ảnh và file giọng thật. MuseTalk chỉnh khẩu hình theo WAV. Footage ngắn có thể chạy xuôi rồi ngược để phủ thời lượng audio. Chọn đoạn ít động tác lớn để điểm đổi chiều ít lộ.

## Bố trí

| Nơi | Thành phần |
|---|---|
| Repo Agent Video Studio | `video_studio/musetalk/`, CLI, skill, công cụ cài, danh mục model và wheel lock |
| `runtime/venvs/agent-video-studio/musetalk-1-5` | CPython 3.12 x86-64, PyTorch CUDA và các wheel đã khóa |
| `runtime/engines/agent-video-studio/musetalk-1-5` | Receipt OpcOS và model đã kiểm SHA-256 trong `models/` |
| Trạm video đã chọn | Tư liệu nói, file WAV và MP4 xuất ra |

## Cài engine

Cần Windows x86-64, NVIDIA CUDA, Python 3.12, `uv`, FFmpeg và FFprobe. Từ gốc checkout Agent Video Studio, chạy PowerShell bằng tài khoản thường. Kho model tải khoảng 4,1 GB, ngoài dung lượng môi trường Python.

```powershell
$runtime = Join-Path $env:OPCOS_ROOT 'system/operations/runtime/opcos-runtime.ps1'
$env:UV_NO_CONFIG = '1'
$env:UV_REQUIRE_HASHES = '1'
& $runtime ensure --repo-dir . --only venvs/musetalk-1-5
if ($LASTEXITCODE -ne 0) { throw 'Không cài được venv MuseTalk.' }
& $runtime ensure --repo-dir . --only engines/musetalk-1-5
if ($LASTEXITCODE -ne 0) { throw 'Không đăng ký được engine MuseTalk.' }
$engine = & $runtime resolve engines agent-video-studio musetalk-1-5
if ($LASTEXITCODE -ne 0) { throw 'Không tìm được engine MuseTalk.' }
python -I -B scripts/install_musetalk_models.py --engine-dir $engine
if ($LASTEXITCODE -ne 0) { throw 'Không xác minh được model MuseTalk.' }
```

Dùng `python -I -B scripts/install_musetalk_models.py --engine-dir $engine --verify-only` để xác minh model cục bộ. Thực hiện lại lệnh cài model khi lần tải trước bị gián đoạn. Tệp đã khớp SHA‑256 được dùng lại. Nếu tệp có sẵn sai hash, xác định nguồn của tệp đó trước khi sửa runtime.

## Chạy và nghiệm thu

```powershell
python -m video_studio avatar doctor --json
python -m video_studio avatar render --source footage.mp4 --audio narration.wav --out avatar.mp4 --json
```

Truyền đường dẫn trong project ở trạm video đã chọn. Dùng video MP4/MOV hoặc ảnh PNG/JPEG có một mặt rõ, tối đa 1280×720, cùng WAV PCM16 mono 16 kHz. Mỗi lần chạy nhận tối đa 30 giây lời thoại và 30 giây footage. Chuẩn hóa footage về 25 fps. Chọn tên MP4 chưa tồn tại. Với audio 30 giây, kiểm đủ 750 khung hình ở 25 fps, tiếng và hình cùng bắt đầu gần mốc 0 và kết thúc gần mốc 30 giây. Soi đoạn mở đầu, giữa, cuối và mép lặp, chú ý môi khi nghỉ, cử chỉ và viền ghép mặt.

`--bbox-shift N` (số nguyên −30..30, mặc định 0) dịch điểm giữa mặt như tham số `bbox_shift` của MuseTalk gốc: số âm cắt khung mặt cao hơn để miệng mở ít, lộ răng ít; số dương làm miệng mở nhiều hơn. Thử 22/11/2026 trên một clip 720×720 có giọng tiếng Việt: −10 đến −15 giảm lộ răng thấy được bằng mắt, nhưng môi vẫn hé khi nghỉ.

Worker có trần tổng thời gian 60 phút và trần 5 phút không thấy tiến độ. Khi quá hạn, lệnh dừng cây tiến trình và báo rõ loại timeout.

## Bản thử trên Windows

Pilot chạy video thật + WAV riêng bằng RTX 4070 và PyTorch CUDA 12.8.
FFprobe đọc được 750 khung hình H.264 1280×720 ở 25 fps và một track AAC mono. Hai
track bắt đầu tại giây 0 và cùng dài 30 giây. Đối chiếu 480.000 mẫu PCM cho hệ số
tương quan 0,999975 với WAV nguồn. Đỉnh bộ nhớ PyTorch cấp phát khoảng 3,50 GiB.
Bản thử PNG chạy được 50 khung hình với WAV 2 giây.

Giới hạn khi xem thử là chuyển động thân và ánh mắt lấy từ footage rồi lặp xuôi/ngược.
Độ tự nhiên khi xem cận mặt cần người duyệt dựa trên tư liệu dùng thật.

## Nguồn và quyền sử dụng

- Model MuseTalk 1.5 và cấu trúc suy luận theo [Tencent Music Lyra Lab](https://github.com/TMElyralab/MuseTalk/tree/2536eaf06b85f775d8e04b7fd81bf6699155a58d). Từng tệp được ghim nguồn, kích thước và băm trong [danh mục](../video_studio/locks/musetalk-models.json).
- Các phần mã được giữ lại ở `video_studio/musetalk/_vendor/` gồm `musetalk/models/{unet,vae}.py`, `musetalk/utils/{audio_processor,blending}.py` và `musetalk/utils/face_parsing/`. Bản chép giữ LICENSE và NOTICE, giới hạn tải trọng số vào đường dẫn đã khóa, dùng `weights_only=True` và bỏ checkpoint ResNet khởi tạo sau khi kiểm nạp nghiêm ngặt toàn bộ parser. Quét riêng mã đưa vào runtime trước khi vá, kèm rà tay sửa các điểm tải, nạp model và gọi tiến trình.
- Bản Windows dùng DWPose ONNX và YuNet để xác định vùng mặt. Bước ONNX khác đường MMPose có lật ảnh, nên đánh giá bằng kết quả trên footage thật.
- Bộ phân vùng mặt do MuseTalk chỉ định là bản đăng lại. Quyền dùng thương mại của thành phần này chưa được xác minh. Tác giả MuseTalk cũng yêu cầu đối chiếu điều khoản của HDTF cho mục đích thương mại. [Thông báo từ upstream](https://github.com/TMElyralab/MuseTalk/blob/2536eaf06b85f775d8e04b7fd81bf6699155a58d/NOTICE) Cấu hình hiện tại dành cho đánh giá kỹ thuật cục bộ. Giữ model và media ngoài Git.
- Để ngừng dùng MuseTalk, dừng lệnh avatar và giữ tài nguyên cho lần gọi sau. `opcos-runtime release --repo agent-video-studio` tác động cả các tài nguyên khác của Video Studio. Tư liệu và kết quả thuộc trạm video.
