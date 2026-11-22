"""Local DWPose and YuNet preprocessing for the avatar engine."""

from pathlib import Path

from .geometry import decode_simcc, face_box, full_frame_affine, select_face


class PoseEstimator:
    def __init__(self, models: Path):
        import cv2
        import onnxruntime

        self.cv2 = cv2
        onnxruntime.disable_telemetry_events()
        self.session = onnxruntime.InferenceSession(
            str(models / "dwpose" / "dw-ll_ucoco_384.onnx"),
            providers=["CPUExecutionProvider"],
        )
        self.detector = cv2.FaceDetectorYN.create(
            str(models / "yunet" / "face_detection_yunet_2023mar.onnx"),
            "", (320, 320), score_threshold=0.9,
        )

    def crop(self, frame, bbox_shift=0):
        import numpy as np

        height, width = frame.shape[:2]
        self.detector.setInputSize((width, height))
        _, faces = self.detector.detect(frame)
        detected = select_face(faces)
        matrix = np.asarray(full_frame_affine(width, height), dtype=np.float32)
        rgb = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
        image = self.cv2.warpAffine(rgb, matrix, (288, 384), flags=self.cv2.INTER_LINEAR)
        image = image.astype(np.float32)
        image = (image - np.asarray([123.675, 116.28, 103.53], dtype=np.float32)) / np.asarray(
            [58.395, 57.12, 57.375], dtype=np.float32
        )
        tensor = np.ascontiguousarray(image.transpose(2, 0, 1)[None])
        x_scores, y_scores = self.session.run(None, {"input": tensor})
        points = decode_simcc(x_scores[0, 23:91], y_scores[0, 23:91], width, height)
        return face_box(points, detected, width, height, bbox_shift)
