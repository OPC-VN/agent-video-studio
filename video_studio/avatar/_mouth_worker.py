"""GFPGAN v1.4 on the mouth region only; runs inside the LatentSync venv with cwd = GFPGAN engine dir.

argv: <in.mp4> <out-silent.mp4> <strength 0..1> <GFPGANv1.4.pth>
Prints one JSON line: frames, face_missed, strength.
"""
import json
import sys

import cv2
import numpy as np
from gfpgan import GFPGANer


def main(src, dst, strength, model):
    strength = float(strength)
    restorer = GFPGANer(model_path=model, upscale=1, arch="clean", channel_multiplier=2, bg_upsampler=None)
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    smooth = None  # (cx, cy, half_w, half_h), smoothed over time so the mask does not shake
    missed = frames = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames += 1
        _, _, restored = restorer.enhance(frame, has_aligned=False, only_center_face=True, paste_back=True)
        landmarks = restorer.face_helper.all_landmarks_5
        if restored is None or not landmarks:
            missed += 1
            out.write(frame)
            continue
        lm = np.asarray(landmarks[0])
        left, right = lm[3], lm[4]
        corner = float(np.linalg.norm(right - left))
        cx, cy = (left + right) / 2.0
        box = np.array([cx, cy + 0.10 * corner, 0.85 * corner, 0.55 * corner])
        smooth = box if smooth is None else 0.6 * smooth + 0.4 * box
        mask = np.zeros((h, w), np.float32)
        cv2.ellipse(mask, (int(smooth[0]), int(smooth[1])), (int(smooth[2]), int(smooth[3])), 0, 0, 360, 1.0, -1)
        k = max(3, int(0.35 * corner) | 1)
        mask = cv2.GaussianBlur(mask, (k, k), 0)[..., None] * strength
        blended = frame.astype(np.float32) * (1 - mask) + restored.astype(np.float32) * mask
        out.write(blended.clip(0, 255).astype(np.uint8))
    out.release()
    print(json.dumps({"frames": frames, "face_missed": missed, "strength": strength}))


if __name__ == "__main__":
    main(*sys.argv[1:5])
