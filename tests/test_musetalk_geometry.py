import importlib

import pytest


def test_full_frame_affine_preserves_center_and_padding():
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    matrix = geometry.full_frame_affine(1280, 720)
    assert matrix[0][0] == pytest.approx(0.18)
    assert matrix[1][1] == pytest.approx(0.18)
    assert matrix[0][2] == pytest.approx(28.8)
    assert matrix[1][2] == pytest.approx(127.2)


@pytest.mark.parametrize("width,height", [(0, 20), (20, 0), (-1, 20)])
def test_full_frame_affine_rejects_invalid_dimensions(width, height):
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    with pytest.raises(ValueError):
        geometry.full_frame_affine(width, height)


def test_simcc_coordinates_are_mapped_back_to_the_source_frame():
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    x = [0.0] * 576
    y = [0.0] * 768
    x[288] = 1.0
    y[384] = 1.0
    assert geometry.decode_simcc([x], [y], 1280, 720)[0] == pytest.approx((640, 360))


def test_simcc_rejects_unmatched_keypoint_counts():
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    with pytest.raises(ValueError):
        geometry.decode_simcc([[1.0]], [], 10, 10)


def test_face_box_uses_landmark_midpoint_and_v15_margin():
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    points = [(20, 30)] * 68
    points[29] = (40, 50)
    points[67] = (80, 90)
    assert geometry.face_box(points, (10, 10, 90, 95), 100, 100) == (20, 10, 80, 100)


def test_face_box_bbox_shift_moves_upper_bound_like_upstream():
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    points = [(20, 30)] * 68
    points[29] = (40, 50)
    points[67] = (80, 90)
    # midpoint 50-5=45, upper = 45-(90-45) = 0; midpoint 50+5=55, upper = 55-35 = 20
    assert geometry.face_box(points, (10, 10, 90, 95), 100, 100, -5) == (20, 0, 80, 100)
    assert geometry.face_box(points, (10, 10, 90, 95), 100, 100, 5) == (20, 20, 80, 100)


def test_face_box_uses_detector_for_invalid_landmarks():
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    assert geometry.face_box([(10, 10)] * 68, (5, 5, 40, 40), 100, 100) == (5, 5, 40, 50)


def test_detector_requires_one_face_and_returns_box():
    geometry = importlib.import_module("video_studio.musetalk.geometry")
    face = [5, 10, 20, 30] + [0] * 10 + [0.9]
    assert geometry.select_face([face]) == (5, 10, 25, 40)
    with pytest.raises(ValueError):
        geometry.select_face([])
    with pytest.raises(ValueError):
        geometry.select_face([face, face])
