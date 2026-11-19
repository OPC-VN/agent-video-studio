"""PTS selection for variable-rate and short scenes."""
import pytest
from video_studio.contract import ContractError
from video_studio.reference.shots import select_frame_pts


def test_pts_selection_never_leaves_scene_and_reuses_when_needed():
    assert select_frame_pts([10.0, 10.1, 10.35, 10.7], 10.0, 10.3) == (10.0, 10.1, 10.1)
    assert select_frame_pts([10.0, 10.1, 10.35], 10.05, 10.2) == (10.1, 10.1, 10.1)


def test_no_frame_in_scene_is_a_failure():
    with pytest.raises(ContractError):
        select_frame_pts([0, 1], .2, .9)


def test_exclusive_end_inclusive_start_unsorted_and_duplicate():
    assert select_frame_pts((value for value in [1.0, .5, .5, 0.0]), .5, 1.0) == (.5, .5, .5)


@pytest.mark.parametrize('bad', [True, 10 ** 1000, float('nan')])
def test_invalid_pts_fail_closed(bad):
    with pytest.raises(ContractError):
        select_frame_pts([bad], 0, 2)
