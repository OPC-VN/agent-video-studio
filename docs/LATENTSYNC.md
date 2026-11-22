# LatentSync 1.5 + GFPGAN vùng miệng trên Windows (thử nghiệm)

Đường lip-sync chất lượng cao hơn [MuseTalk](MUSETALK.md): LatentSync 1.5 tạo khẩu hình theo WAV, sau đó GFPGAN v1.4 làm nét **chỉ vùng miệng** để bỏ vệt tối trong miệng do LatentSync dựng mặt ở 256 px.

> **Trạng thái:** chạy qua `video-studio avatar` (`render` mặc định LatentSync, `optimize --task mouth`, `qa`). Quy trình từ quay clip tới hồ sơ dùng lại: skill `avatar-create`. Engine và model nằm ngoài Git, ở `runtime/`; chưa có receipt `opcos-runtime`, cài theo các bước dưới.

## Khi nào dùng engine nào

Kết quả đo ngày 22/11/2026 trên RTX 4070 12 GB, clip 720×720 25 fps, 10 giây giọng tiếng Việt. Điểm SyncNet càng cao càng khớp; video thật thường khoảng 7–9.

| | MuseTalk 1.5 (`--bbox-shift -15`) | LatentSync 1.5 (guidance 2.5, 30 bước) | + GFPGAN vùng miệng |
|---|---|---|---|
| SyncNet (độ tin cậy / lệch khung) | 4,79 / 1 | **7,94 / 0** | 7,80 / 0 |
| Miệng khi im lặng | vẫn hé, lộ răng | khép | khép |
| Trong miệng | răng rõ | khe tối, răng nhoè | sáng, thấy răng |
| Thời gian cho 10 giây video | 104–158 s | 939 s | + 83 s |
| VRAM | ~3,5 GiB | vừa 12 GB | — |

- **MuseTalk:** bản nháp nhanh, xem thử bố cục và nhịp.
- **LatentSync + GFPGAN:** bản dùng thật cho đoạn có avatar xuất hiện.
- Ở cùng clip, guidance 1.5 cho điểm 7,23 (miệng mở ít) và 3.0 cho 7,74. Dời tiếng thêm 40 ms làm điểm tụt xuống 7,60 nên không dời.
- Đoạn đọc nhanh vẫn hơi "chậm" vì model làm mượt theo nhóm 16 khung. **Giả thuyết, chưa đo:** đọc chậm hơn giúp môi theo kịp. Hồ sơ giọng vẫn giữ `speed` 1.0. Chỉ khi SyncNet < 7 hoặc thấy trễ ở đoạn nhanh: thử sắc thái đọc chậm của profile giọng trước, rồi mới thử `speed` 0,95 → 0,9 có ghim seed. Giữ mức mới khi SyncNet tăng ≥ 0,3 và ASR vẫn nghe đúng.

## Bố trí

| Nơi | Thành phần |
|---|---|
| Repo Agent Video Studio | Tài liệu này, `scripts/requirements-latentsync-windows.txt`, `video_studio/avatar/` (lệnh và worker làm nét miệng) |
| `runtime/venvs/agent-video-studio/latentsync-1-5` | CPython 3.10, PyTorch 2.4.1 CUDA 12.1, thư viện LatentSync + GFPGAN |
| `runtime/engines/agent-video-studio/latentsync-1-5` | `src/` (mã LatentSync ghim commit), `src/checkpoints/`, `torch-home/`, `hf-home/` |
| `runtime/engines/agent-video-studio/gfpgan` | `gfpgan/weights/` (GFPGAN v1.4 + bộ dò và phân vùng mặt) |
| Trạm video đã chọn | Footage, WAV, MP4 xuất ra |

## Cài engine

Cần Windows x86-64, GPU NVIDIA ≥ 8 GB VRAM, `uv`, Git, FFmpeg. **Không cần** Visual C++ Build Tools. Dung lượng khoảng 10 GB: model ~5,2 GB, thư viện Python ~3–4 GB, GFPGAN ~0,55 GB. Chạy PowerShell bằng tài khoản thường, từ gốc checkout Agent Video Studio.

**Vì sao ghim commit `b5ee2a5` (10/04/2025):** từ 12/04/2025 LatentSync chuyển sang insightface, gói này phải biên dịch C++ trên Windows. Commit `b5ee2a5` là bản cuối còn dùng face-alignment + mediapipe (có wheel sẵn) và vẫn tương thích checkpoint 1.5.

```powershell
$repo    = (Get-Location).Path
$engines = Join-Path $env:OPCOS_ROOT 'runtime/engines/agent-video-studio'
$venv    = Join-Path $env:OPCOS_ROOT 'runtime/venvs/agent-video-studio/latentsync-1-5'
$ls      = Join-Path $engines 'latentsync-1-5'
$py      = Join-Path $venv 'Scripts/python.exe'

# 1. Mã nguồn, ghim commit
git clone https://github.com/bytedance/LatentSync.git (Join-Path $ls 'src')
git -C (Join-Path $ls 'src') checkout b5ee2a5

# 2. Môi trường Python 3.10 + thư viện đã ghim
uv venv --python 3.10 $venv
uv pip install --python $py --index-strategy unsafe-best-match -r (Join-Path $repo 'scripts/requirements-latentsync-windows.txt')

# 3. Checkpoint từ Hugging Face ByteDance/LatentSync-1.5 (~5,2 GB)
Push-Location (Join-Path $ls 'src')
& $py -c "from huggingface_hub import hf_hub_download as d; [print(d('ByteDance/LatentSync-1.5', f, local_dir='checkpoints')) for f in ['latentsync_unet.pt','whisper/tiny.pt','auxiliary/2DFAN4-cd938726ad.zip','auxiliary/s3fd-619a316812.pth','auxiliary/syncnet_v2.model','auxiliary/sfd_face.pth']]"
Pop-Location

# 4. Model dò mặt cho face-alignment: đặt trong engine, không ghi ~/.cache
New-Item -ItemType Directory -Force (Join-Path $ls 'torch-home/hub/checkpoints'), (Join-Path $ls 'hf-home') | Out-Null
Copy-Item (Join-Path $ls 'src/checkpoints/auxiliary/2DFAN4-cd938726ad.zip'), (Join-Path $ls 'src/checkpoints/auxiliary/s3fd-619a316812.pth') (Join-Path $ls 'torch-home/hub/checkpoints')

# 5. GFPGAN vào cùng venv, không đổi torch/numpy
uv pip install --python $py --no-deps gfpgan==1.3.8 basicsr==1.4.2 facexlib==0.3.0
uv pip install --python $py filterpy addict yapf lmdb future scikit-image scipy numba
$sp = & $py -c "import site; print(site.getsitepackages()[-1])"
$deg = Join-Path $sp 'basicsr/data/degradations.py'
(Get-Content $deg -Raw) -replace 'torchvision\.transforms\.functional_tensor', 'torchvision.transforms.functional' | Set-Content $deg -Encoding utf8 -NoNewline

# 6. Weights GFPGAN từ trang phát hành chính thức
$gw = Join-Path $engines 'gfpgan/gfpgan/weights'
New-Item -ItemType Directory -Force $gw | Out-Null
curl.exe -L -o (Join-Path $gw 'GFPGANv1.4.pth') https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
curl.exe -L -o (Join-Path $gw 'detection_Resnet50_Final.pth') https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth
curl.exe -L -o (Join-Path $gw 'parsing_parsenet.pth') https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/parsing_parsenet.pth

# Kiểm
& $py -c "import torch, face_alignment, gfpgan; print(torch.__version__, torch.cuda.is_available())"
```

SHA-256 của `GFPGANv1.4.pth` bắt đầu bằng `e2cd4703ab14f4d0`. Bước 5 sửa một dòng import trong `basicsr` 1.4.2: dòng đó gọi `torchvision.transforms.functional_tensor`, module đã bị gỡ khỏi torchvision mới.

## Chạy

Đầu vào:
- Footage một người, gần chính diện, miệng khép. Nên cắt khung gần (đầu tới ngực, ví dụ 720×720) để mặt đủ lớn.
- WAV PCM, tối đa 60 giây mỗi lần.
- Mọi đường dẫn nằm trong trạm video. Lệnh tự chép vào thư mục tạm không dấu cách trong engine (script upstream gọi FFmpeg qua shell, không bọc đường dẫn), rồi dọn khi xong.

```powershell
python -m video_studio avatar doctor --engine latentsync --json

# 1. Chuẩn hoá clip nền: bỏ tiếng, 25 fps, cắt W:H:X:Y, thu vào giới hạn 1280x720
python -m video_studio avatar optimize --task normalize --input <clip-gốc.mp4> --crop 720:720:0:180 --out <clip-sẵn.mp4> --json

# 2. Lip-sync (mặc định guidance 2.5, 30 bước, seed 1247)
python -m video_studio avatar render --source <clip-sẵn.mp4> --audio <giọng.wav> --out <ls.mp4> --json

# 3. Làm nét vùng miệng, giữ nguyên tiếng
python -m video_studio avatar optimize --task mouth --input <ls.mp4> --out <ls-nét.mp4> --strength 0.85 --json
```

- Lệnh lip-sync mất 224–939 giây cho clip 10 giây (hai lần đo trên RTX 4070): chạy nền. Trần thời gian tự giãn theo độ dài WAV.
- Engine chạy ngoại tuyến (`HF_HUB_OFFLINE=1`). Lần cài đầu phải có VAE `sd-vae-ft-mse` trong `hf-home`: chạy một lần lệnh inference của upstream khi có mạng.
- Độ mạnh làm nét mặc định 0,85. Nếu khẩu hình tròn (chữ "o", "u") bị khép bớt, hạ xuống khoảng 0,6.
- Hồ sơ dùng lại: `avatar profile new|list|update|revoke`, rồi `render --profile <id>` (skill `avatar-create`).

## Nghiệm thu

1. Chấm SyncNet:
   ```powershell
   python -m video_studio avatar qa --video <ls-nét.mp4> --json
   ```
   Mức đạt: độ lệch (AV offset) = 0 và độ tin cậy ≥ 7. Thêm `--profile <id>` để ghi vào lịch sử QA của hồ sơ.
2. Soi vùng miệng ở mốc im lặng và mốc đang nói: khi nghỉ miệng phải khép, khi nói không có khe tối.
3. Xem ở tốc độ thật để kiểm nhấp nháy vùng miệng sau làm nét (`face_missed` trong kết quả bước 3 phải bằng 0).

Đo lại qua CLI ngày 22/11/2026, cùng clip ở bảng trên: `render` cho 7,89 / 0 trong 224 giây; `qa` trên bản chạy tay cho 7,94 / 0 (khớp lần đo tay); `optimize --task mouth` cho 7,73 / 0 (lần chạy tay 7,80; khác ở chỗ CLI giữ tiếng AAC của bản LatentSync thay vì ghép lại WAV gốc).

## Nguồn và quyền sử dụng

- **LatentSync:**
  - Mã nguồn [bytedance/LatentSync](https://github.com/bytedance/LatentSync) theo Apache-2.0, ghim commit `b5ee2a5`.
  - Trọng số [ByteDance/LatentSync-1.5](https://huggingface.co/ByteDance/LatentSync-1.5) theo **openrail++**: cho dùng thương mại kèm điều khoản giới hạn mục đích sử dụng. Đọc file license của repo model trước khi phát hành sản phẩm bán.
  - Báo cáo upstream có nhắc đánh giá trên VoxCeleb2 và HDTF.
- **GFPGAN:** mã [TencentARC/GFPGAN](https://github.com/TencentARC/GFPGAN) theo Apache-2.0. Bộ dò mặt và phân vùng mặt lấy từ trang phát hành của facexlib và CodeFormer; quyền thương mại của từng tệp weights chưa được xác minh.
- **Chỉ dựng khuôn mặt và giọng của chính người dùng**, hoặc của người đã đồng ý bằng văn bản. Model, footage và kết quả giữ ngoài Git.
- Gỡ: xoá `runtime/engines/agent-video-studio/latentsync-1-5`, `.../gfpgan` và venv `latentsync-1-5`. Không ảnh hưởng MuseTalk.
