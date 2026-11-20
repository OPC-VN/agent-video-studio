"""Private worker for an offline MuseTalk render; called by runner only."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import time

# -I deliberately ignores the checkout. Add only this package's trusted parent.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def _command(argv):
    result = subprocess.run(argv, capture_output=True, check=False, timeout=600)
    if result.returncode:
        raise RuntimeError("FFmpeg failed while processing local media")
    return result.stdout


def render(source, audio, output, models, ffmpeg, ffprobe, expected_frames, source_kind):
    started = time.monotonic()
    print("Avatar: loading the engine", file=sys.stderr, flush=True)
    def deny_network(event, args):
        if event in ("socket.connect", "socket.getaddrinfo"):
            raise PermissionError("Network access is disabled in the avatar worker")
    sys.addaudithook(deny_network)
    import cv2
    import numpy as np
    import torch
    from transformers import WhisperModel

    from video_studio.musetalk.pose import PoseEstimator
    from video_studio.musetalk._vendor.audio_processor import AudioProcessor
    from video_studio.musetalk._vendor.blending import get_image
    from video_studio.musetalk._vendor.face_parsing import FaceParsing
    from video_studio.musetalk._vendor.unet import UNet, PositionalEncoding
    from video_studio.musetalk._vendor.vae import VAE

    models, output = Path(models), Path(output)
    if not torch.cuda.is_available():
        raise RuntimeError("A CUDA-capable NVIDIA GPU is required")
    device = torch.device("cuda")
    torch.cuda.reset_peak_memory_stats(device)
    dtype = torch.float16
    with tempfile.TemporaryDirectory(prefix=".avatar-", dir=output.parent) as work:
        work = Path(work)
        inputs, images = work / "input", work / "frames"
        inputs.mkdir()
        images.mkdir()
        decoder = (["-f", "mov", "-enable_drefs", "0"] if source_kind == "mov" else
                   ["-f", "image2", "-pattern_type", "none", "-c:v", source_kind])
        output_args = (["-t", "30", "-vf", "fps=25"] if source_kind == "mov" else ["-frames:v", "1"])
        _command([ffmpeg, "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe", *decoder,
                  "-i", str(source), "-map", "0:v:0", *output_args,
                  "-start_number", "0", str(inputs / "%08d.png")])
        paths = sorted(inputs.glob("*.png"))
        if not paths or len(paths) > 750:
            raise RuntimeError("Source video has no decodable frames")
        frames = [cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR) for path in paths]
        if any(frame is None for frame in frames):
            raise RuntimeError("Could not read an extracted video frame")
        shape = frames[0].shape
        if any(frame.shape != shape for frame in frames):
            raise RuntimeError("Source frame dimensions change during the video")

        vae = VAE(model_path=str(models / "sd-vae"))
        unet = UNet(unet_config=str(models / "musetalkV15" / "musetalk.json"),
                    model_path=str(models / "musetalkV15" / "unet.pth"), device=device)
        vae.vae = vae.vae.to(device=device, dtype=dtype).eval()
        unet.model = unet.model.to(device=device, dtype=dtype).eval()
        pe = PositionalEncoding(d_model=384).to(device=device, dtype=dtype).eval()
        whisper = WhisperModel.from_pretrained(str(models / "whisper"), local_files_only=True,
                                               use_safetensors=True).to(device=device, dtype=dtype).eval()
        whisper.requires_grad_(False)
        audio_processor = AudioProcessor(feature_extractor_path=str(models / "whisper"))
        parser = FaceParsing(model_path=str(models / "face-parse-bisent" / "79999_iter.pth"),
                             left_cheek_width=90, right_cheek_width=90)
        estimator = PoseEstimator(models)
        with torch.no_grad():
            features, length = audio_processor.get_audio_feature(str(audio), weight_dtype=dtype)
            chunks = audio_processor.get_whisper_chunk(features, device, dtype, whisper, length, fps=25)
            boxes = []
            for index, frame in enumerate(frames):
                if index % 25 == 0:
                    print(f"Avatar: locating face {index + 1}/{len(frames)}", file=sys.stderr, flush=True)
                boxes.append(estimator.crop(frame))
            latents = []
            for frame, (x1, y1, x2, y2) in zip(frames, boxes):
                crop = cv2.resize(frame[y1:y2, x1:x2], (256, 256), interpolation=cv2.INTER_LANCZOS4)
                latents.append(vae.get_latents_for_unet(crop))
            cycle = list(range(len(frames))) + list(range(len(frames) - 1, -1, -1))
            timestep = torch.tensor([0], device=device)
            count = len(chunks)
            if count != int(expected_frames):
                raise RuntimeError("Audio feature frame count does not match input WAV")
            for start in range(0, count, 8):
                if start % 64 == 0:
                    print(f"Avatar: generating frame {start + 1}/{count}", file=sys.stderr, flush=True)
                indices = [cycle[i % len(cycle)] for i in range(start, min(start + 8, count))]
                latent_batch = torch.cat([latents[i] for i in indices]).to(device=device, dtype=dtype)
                generated = unet.model(latent_batch, timestep,
                                       encoder_hidden_states=pe(chunks[start:start + len(indices)])).sample
                for offset, (idx, image) in enumerate(zip(indices, vae.decode_latents(generated))):
                    x1, y1, x2, y2 = boxes[idx]
                    face = cv2.resize(image.astype(np.uint8), (x2 - x1, y2 - y1))
                    frame = get_image(frames[idx], face, [x1, y1, x2, y2], mode="jaw", fp=parser)
                    ok, encoded = cv2.imencode(".png", frame)
                    if not ok:
                        raise RuntimeError("Could not write an intermediate frame")
                    encoded.tofile(str(images / f"{start + offset:08d}.png"))
        if len(list(images.glob("*.png"))) != count or not 0 < count <= 750:
            raise RuntimeError("Generated frame count does not match audio")
        print("Avatar: muxing output", file=sys.stderr, flush=True)
        candidate = work / "result.mp4"
        _command([ffmpeg, "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe", "-framerate", "25",
                  "-start_number", "0", "-i", str(images / "%08d.png"), "-protocol_whitelist", "file,pipe",
                  "-f", "wav", "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-crf", "18",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(candidate)])
        if not candidate.is_file() or candidate.stat().st_size == 0:
            raise RuntimeError("FFmpeg did not produce a video")
        probe = _command([ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe", "-f", "mov",
                          "-enable_drefs", "0", "-count_frames", "-show_entries",
                          "stream=codec_type,nb_read_frames,channels:format=duration", "-of", "json", str(candidate)])
        media = json.loads(probe)
        videos = [stream for stream in media["streams"] if stream.get("codec_type") == "video"]
        audio_streams = [stream for stream in media["streams"] if stream.get("codec_type") == "audio"]
        if (len(videos) != 1 or len(audio_streams) != 1 or audio_streams[0].get("channels") != 1
                or int(videos[0]["nb_read_frames"]) != count
                or abs(float(media["format"]["duration"]) - count / 25) > 0.15):
            raise RuntimeError("Rendered stream or duration verification failed")
        os.link(candidate, output)
    return {"frames": count, "fps": 25, "device": device.type,
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "peak_vram_bytes": torch.cuda.max_memory_allocated(device)}


if __name__ == "__main__":
    try:
        print(json.dumps(render(*sys.argv[1:]), ensure_ascii=False))
    except Exception as exc:
        print(f"Avatar engine failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
