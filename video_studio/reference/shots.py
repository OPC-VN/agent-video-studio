"""Pure shot boundary calculations for reference analysis.

No media I/O occurs here. Frame marks are requests, not measured presentation times.
"""
import math

from ..contract import ContractError

MAX_SHOTS = 40
DEFAULT_THRESHOLD = 0.30
DEFAULT_MIN_SHOT = 0.5
SCHEMA = 'video_studio.shots.v1'


def _positive(value, label):
    if isinstance(value, bool):
        raise ContractError(f'{label} phải là số hữu hạn dương')
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ContractError(f'{label} phải là số hữu hạn dương') from None
    if not math.isfinite(result) or result <= 0:
        raise ContractError(f'{label} phải là số hữu hạn dương')
    return result


def build_shots(cuts, duration, min_shot):
    """Build contiguous intervals from finite detector cuts in timeline seconds."""
    duration = _positive(duration, 'duration')
    minimum = _positive(min_shot, '--min-shot')
    try:
        cuts = list(cuts)
        if any(isinstance(value, bool) for value in cuts):
            raise ValueError('boolean cut')
        positions = [float(value) for value in cuts]
    except (TypeError, ValueError, OverflowError):
        raise ContractError('mốc cắt phải là số hữu hạn') from None
    if any(not math.isfinite(value) for value in positions):
        raise ContractError('mốc cắt phải là số hữu hạn')
    bounds = [0.0]
    for cut in sorted(positions):
        gap_before, gap_after = cut - bounds[-1], duration - cut
        if (cut > bounds[-1] and cut < duration
                and (gap_before >= minimum or math.isclose(gap_before, minimum, rel_tol=1e-12, abs_tol=1e-12))
                and (gap_after >= minimum or math.isclose(gap_after, minimum, rel_tol=1e-12, abs_tol=1e-12))):
            bounds.append(cut)
    bounds.append(duration)
    if len(bounds) - 1 > MAX_SHOTS:
        raise ContractError(f'quá {MAX_SHOTS} cảnh: tăng --threshold hoặc --min-shot')
    return [{'id': f'SH{index:03d}', 'start_s': start, 'end_s': end,
             'duration_s': end - start, 'basis': 'measured',
             'cut_in': 'unknown' if index == 1 else 'hard'}
            for index, (start, end) in enumerate(zip(bounds, bounds[1:]), 1)]


def frame_marks(shot, fps):
    """Return three requested times; extractors must report actual frame PTS."""
    rate = _positive(fps, 'fps')
    try:
        if isinstance(shot['start_s'], bool) or isinstance(shot['end_s'], bool):
            raise ValueError('boolean endpoint')
        start, end = float(shot['start_s']), float(shot['end_s'])
    except (KeyError, TypeError, ValueError, OverflowError):
        raise ContractError('cảnh cần start_s và end_s hữu hạn') from None
    if not math.isfinite(start) or not math.isfinite(end) or start < 0 or end <= start:
        raise ContractError('cảnh cần 0 <= start_s < end_s hữu hạn')
    midpoint = start + (end - start) / 2
    return start, midpoint, max(midpoint, end - 1.5 / rate)


def select_frame_pts(frame_pts, start, end):
    """Choose measured presentation times within a scene, reusing frames if needed."""
    try:
        if isinstance(start, bool) or isinstance(end, bool):
            raise ValueError('boolean boundary')
        start, end = float(start), float(end)
        source = list(frame_pts)
        if any(isinstance(value, bool) for value in source):
            raise ValueError('boolean frame')
        times = sorted(float(value) for value in source)
    except (TypeError, ValueError, OverflowError):
        raise ContractError('mốc PTS và biên phải là số hữu hạn') from None
    if not math.isfinite(start) or not math.isfinite(end) or start < 0 or start >= end:
        raise ContractError('biên cảnh không hợp lệ')
    if any(not math.isfinite(value) or value < 0 for value in times):
        raise ContractError('mốc PTS không hợp lệ')
    inside = [value for value in times if start <= value < end]
    if not inside:
        raise ContractError('cảnh không chứa frame PTS; không thể trích khung')
    middle = start + (end - start) / 2
    return inside[0], min(inside, key=lambda value: (abs(value - middle), value)), inside[-1]
