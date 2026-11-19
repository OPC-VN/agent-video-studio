"""Metrics for scene-cut calibration: one detection cannot match two truth cuts."""
import pytest
from video_studio.contract import ContractError
from video_studio.reference._calibration import score_cuts


def test_matches_one_to_one_and_counts_extra_detections():
    result = score_cuts([2.0, 2.1, 5.0], [2.05, 5.05, 5.1], tolerance=.11)
    assert result['matched'] == 2
    assert result['missed'] == result['extra'] == 1


def test_one_detection_cannot_explain_two_ground_truths():
    result = score_cuts([2.0, 2.2], [2.1], tolerance=.15)
    assert (result['matched'], result['missed'], result['extra']) == (1, 1, 0)
    assert result['precision'] == 1.0 and result['recall'] == .5


def test_empty_sets_are_reported_without_inventing_scores():
    result = score_cuts([], [], tolerance=.25)
    assert result['precision'] is None and result['recall'] is None


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -1])
def test_invalid_input_rejected(value):
    with pytest.raises(ContractError):
        score_cuts([value], [], tolerance=.25)


def test_nominal_tolerance_boundary_survives_float_rounding():
    assert score_cuts([.3], [.4], tolerance=.1)['matched'] == 1
