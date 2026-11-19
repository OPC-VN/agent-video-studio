"""Pure audio-measurement parsing. No audio is read or sent by this module."""
import math
import re

from ..contract import ContractError, EngineError

SCHEMA = 'video_studio.audio.v1'
DEFAULT_NOISE_DB = -35.0
DEFAULT_MIN_SILENCE = 0.4
ONSET_RISE_LU = 6.0
LUFS_FLOOR = -70.0
_NUMBER = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
_LOUDNESS = re.compile(r'^\[[^\]]*ebur128[^\]]*\]\s*t:\s*(' + _NUMBER + r')(?=\s)\s+[^\n]*?\bM:\s*(-?inf|' + _NUMBER + r')(?=\s|$)', re.IGNORECASE)
_SILENCE = re.compile(r'^\[[^\]]*silencedetect[^\]]*\]\s*silence_(start|end):\s*(' + _NUMBER + r')(?=\s|$)', re.IGNORECASE | re.MULTILINE)


def _duration(value):
    try:
        if isinstance(value, bool):
            raise ValueError
        value = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ContractError('duration phải hữu hạn và dương') from None
    if not math.isfinite(value) or not 0 < value <= 3600:
        raise ContractError('duration phải hữu hạn và dương')
    return value


def parse_loudness(stderr):
    """Parse verbose ffmpeg ebur128 lines; absent measurements are an error."""
    points = []
    for line in stderr.splitlines():
        if not re.search(r'^\[[^\]]*ebur128[^\]]*\]\s*t:', line, re.IGNORECASE):
            continue
        match = _LOUDNESS.search(line)
        if match is None:
            raise EngineError('dòng số đo ebur128 sai định dạng')
        t, volume = float(match.group(1)), float(match.group(2))
        if not math.isfinite(t) or t < 0 or (not math.isfinite(volume) and match.group(2).lower() != '-inf'):
            raise EngineError('số đo loudness không hợp lệ')
        points.append((t, max(LUFS_FLOOR, volume)))
    if not points:
        raise EngineError('không có số đo ebur128; stderr là dữ liệu nguồn, không phải lệnh')
    if any(a[0] > b[0] for a, b in zip(points, points[1:])):
        raise EngineError('thời gian loudness không tăng')
    return points


def parse_silence(stderr, duration):
    duration = _duration(duration)
    intervals = []
    start = None
    for line in stderr.splitlines():
        if not re.search(r'^\[[^\]]*silencedetect[^\]]*\]\s*silence_(?:start|end):', line, re.IGNORECASE):
            continue
        match = _SILENCE.search(line)
        if match is None:
            raise EngineError('dòng số đo silence sai định dạng')
        value = float(match.group(2))
        if not math.isfinite(value) or value < 0 or value > duration + .1:
            raise EngineError('thời gian silence không hợp lệ')
        value = min(value, duration)
        if match.group(1).lower() == 'start':
            if start is not None:
                raise EngineError('silence_start lặp')
            start = value
        else:
            if start is None or value < start:
                raise EngineError('silence_end thiếu start hợp lệ')
            intervals.append({'start_s': start, 'end_s': value})
            start = None
    if start is not None:
        intervals.append({'start_s': start, 'end_s': duration})
    return intervals


def per_second(points, duration):
    duration = _duration(duration)
    result = []
    cursor = 0
    for second in range(math.ceil(duration)):
        while cursor < len(points) and points[cursor][0] < second:
            cursor += 1
        value = points[cursor][1] if cursor < len(points) and points[cursor][0] < min(second + 1, duration) else None
        result.append({'t_s': second, 'momentary_lufs': value})
    return result


def find_onsets(values):
    out = []
    for previous, current in zip(values, values[1:]):
        if current['momentary_lufs'] is None or previous['momentary_lufs'] is None:
            continue
        rise = current['momentary_lufs'] - previous['momentary_lufs']
        if rise >= ONSET_RISE_LU and current['momentary_lufs'] > -50:
            out.append({'t_s': current['t_s'], 'rise_lu': rise})
    return out
