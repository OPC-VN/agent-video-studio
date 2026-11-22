"""Coordinate transforms used by the MuseTalk pose adapter."""


def full_frame_affine(width: int, height: int) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """Map the padded full frame into the 288 by 384 pose input."""
    if width <= 0 or height <= 0:
        raise ValueError("frame dimensions must be positive")
    padded_width = max(width * 1.25, height * 1.25 * 288 / 384)
    factor = 288 / padded_width
    return ((factor, 0.0, 144 - factor * width / 2),
            (0.0, factor, 192 - factor * height / 2))


def decode_simcc(x, y, width: int, height: int) -> list[tuple[float, float]]:
    """Decode per-keypoint SimCC scores and invert the full-frame affine."""
    if len(x) != len(y) or not len(x):
        raise ValueError("pose outputs must contain matching keypoints")
    matrix = full_frame_affine(width, height)
    factor, x_offset, y_offset = matrix[0][0], matrix[0][2], matrix[1][2]
    result = []
    for x_scores, y_scores in zip(x, y):
        if len(x_scores) != 576 or len(y_scores) != 768:
            raise ValueError("unexpected SimCC output dimensions")
        x_index = max(range(len(x_scores)), key=x_scores.__getitem__)
        y_index = max(range(len(y_scores)), key=y_scores.__getitem__)
        if x_scores[x_index] <= 0 or y_scores[y_index] <= 0:
            raise ValueError("pose keypoint has no positive score")
        result.append(((x_index / 2 - x_offset) / factor,
                       (y_index / 2 - y_offset) / factor))
    return result


def face_box(points, detector_box, width, height, bbox_shift=0):
    """Derive the v1.5 crop from 68 face points, falling back to detection.

    bbox_shift moves the nose midpoint like upstream MuseTalk: negative values
    give a taller crop and a less open mouth, positive values open it more.
    """
    if len(points) != 68 or len(detector_box) != 4 or width <= 0 or height <= 0:
        raise ValueError("invalid landmarks, detector box or frame dimensions")
    xs = [int(p[0]) for p in points]
    ys = [int(p[1]) for p in points]
    midpoint = ys[29] + int(bbox_shift)
    x1, y1, x2, y2 = min(xs), max(0, midpoint - (max(ys) - midpoint)), max(xs), max(ys)
    if x1 < 0 or x2 <= x1 or y2 <= y1:
        x1, y1, x2, y2 = map(int, detector_box)
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width, x2), min(height, y2 + 10)
    if x2 <= x1 or y2 <= y1:
        raise ValueError("face crop is outside the frame")
    return x1, y1, x2, y2


def select_face(faces):
    """Require one unambiguous detected face and convert xywh to xyxy."""
    if faces is None or len(faces) != 1 or len(faces[0]) < 4:
        raise ValueError("expected exactly one detected face")
    x, y, width, height = map(float, faces[0][:4])
    if width <= 0 or height <= 0:
        raise ValueError("invalid detected face box")
    return x, y, x + width, y + height
