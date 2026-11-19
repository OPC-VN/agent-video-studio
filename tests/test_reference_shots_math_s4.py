"""Pure shot-boundary rules; they do not open or process user media."""
import math
import pytest
from video_studio.contract import ContractError
from video_studio.reference.shots import build_shots, frame_marks


def test_boundaries_are_contiguous_and_filter_near_cuts():
    result = build_shots([0.1, 2.0, 2.2, 5.0, 6.9], 7.0, .5)
    assert [(s['start_s'], s['end_s']) for s in result] == [(0, 2), (2, 5), (5, 7)]
    assert [s['id'] for s in result] == ['SH001', 'SH002', 'SH003']
    assert [s['cut_in'] for s in result] == ['unknown', 'hard', 'hard']
    assert all(s['basis'] == 'measured' for s in result)


def test_no_cuts_and_limit():
    assert len(build_shots([], 7, .5)) == 1
    with pytest.raises(ContractError, match='--min-shot'):
        build_shots(list(range(1, 60)), 100, .5)


@pytest.mark.parametrize('bad', [float('nan'), float('inf'), -1, 0])
def test_invalid_duration_rejected(bad):
    with pytest.raises(ContractError):
        build_shots([], bad, .5)


def test_marks_for_constant_rate_are_proposals_not_actual_pts():
    assert frame_marks({'start_s': 0, 'end_s': 2}, 12) == (0, 1, 1.875)
    with pytest.raises(ContractError):
        frame_marks({'start_s': 0, 'end_s': 2}, math.nan)


def test_short_scene_proposals_remain_in_order():
    first, middle, last = frame_marks({'start_s': 0, 'end_s': .25}, 10)
    assert 0 <= first <= middle <= last < .25


def test_minimum_spacing_is_not_lost_to_float_representation():
    result = build_shots([.3, .6], 1, .3)
    assert [shot['start_s'] for shot in result] == [0, .3, .6]


@pytest.mark.parametrize('bad', [True, 10 ** 1000])
def test_invalid_duration_types_and_overflow_raise_contract_error(bad):
    with pytest.raises(ContractError):
        build_shots([], bad, .5)


def test_minimum_spacing_with_floating_boundary():
    result = build_shots([.4, .7], 1.1, .3)
    assert [shot['start_s'] for shot in result] == [0, .4, .7]


def test_generator_cut_input_is_not_consumed_twice():
    result = build_shots((value for value in [2, 5]), 7, .5)
    assert [shot['start_s'] for shot in result] == [0, 2, 5]


@pytest.mark.parametrize('bad', [True, 10 ** 1000])
def test_invalid_frame_endpoints_raise_contract_error(bad):
    with pytest.raises(ContractError):
        frame_marks({'start_s': 0, 'end_s': bad}, 12)
