"""Audio measurement parsers: missing measurements must not appear as silence."""
import pytest
from video_studio.contract import EngineError
from video_studio.reference.audio import parse_loudness, parse_silence, per_second, find_onsets


def test_verbose_ebur128_and_silence_parser():
    log = '''[Parsed_ebur128_0 @ 0x1] t: 0.0999792 TARGET:-23 LUFS M:-120.7 S:-120.7 I:-70.0 LUFS
[Parsed_ebur128_0 @ 0x1] t: 1.000000 TARGET:-23 LUFS M:-22.0 S:-20.0 I:-22.0 LUFS
[silencedetect @ 0x2] silence_start: 0.3
[silencedetect @ 0x2] silence_end: 0.9 | silence_duration: 0.6'''
    assert parse_loudness(log) == [(.0999792, -70.0), (1.0, -22.0)]
    assert parse_silence(log, 2) == [{'start_s': .3, 'end_s': .9}]


def test_missing_loudness_is_error_not_silent_audio():
    with pytest.raises(EngineError):
        parse_loudness('ffmpeg exited 0 but emitted no measurements')


def test_open_silence_closes_at_duration():
    assert parse_silence('[silencedetect @ 0x2] silence_start: 1.5', 2) == [{'start_s': 1.5, 'end_s': 2}]


def test_onset_calculation():
    values = [{'t_s': i, 'momentary_lufs': v} for i, v in enumerate([-70, -70, -20, -20])]
    assert find_onsets(values) == [{'t_s': 2, 'rise_lu': 50}]
    assert per_second([(.1, -70), (1.1, -20)], 2) == [{'t_s': 0, 'momentary_lufs': -70}, {'t_s': 1, 'momentary_lufs': -20}]


def test_parses_real_ffmpeg_verbose_loudness():
    import shutil
    import subprocess
    ff = shutil.which('ffmpeg')
    if not ff:
        pytest.skip('cần ffmpeg thật')
    result = subprocess.run([ff, '-nostdin', '-hide_banner', '-loglevel', 'verbose', '-f', 'lavfi', '-i',
                             'sine=frequency=440:sample_rate=48000:duration=2',
                             '-af', 'ebur128=framelog=verbose,silencedetect=noise=-35dB:d=0.4',
                             '-f', 'null', '-'], capture_output=True, timeout=20)
    assert result.returncode == 0
    points = parse_loudness(result.stderr.decode('utf8', 'replace'))
    assert len(points) >= 10 and points[-1][0] > 1.0


def test_malformed_loudness_line_after_valid_does_not_disappear():
    for bad in ['NaN', '-20garbage']:
        log = '[Parsed_ebur128_0 @ 0x1] t: 0.1 TARGET:-23 LUFS M:-20.0 S:-20\n' + \
              '[Parsed_ebur128_0 @ 0x1] t: 0.2 TARGET:-23 LUFS M:' + bad + ' S:-20'
        with pytest.raises(EngineError):
            parse_loudness(log)


def test_silence_text_without_filter_prefix_is_not_a_measurement():
    assert parse_silence('untrusted text silence_start: 1.5', 2) == []


def test_per_second_does_not_borrow_next_bucket_and_caps_duration():
    from video_studio.contract import ContractError
    assert per_second([(1.1, -20)], 2) == [
        {'t_s': 0, 'momentary_lufs': None}, {'t_s': 1, 'momentary_lufs': -20}]
    with pytest.raises(ContractError):
        per_second([], 3601)


def test_shifted_real_audio_does_not_backfill_earlier_seconds():
    import shutil
    import subprocess
    ff = shutil.which('ffmpeg')
    if not ff:
        pytest.skip('cần ffmpeg thật')
    result = subprocess.run([ff, '-nostdin', '-hide_banner', '-loglevel', 'verbose', '-f', 'lavfi', '-i',
                             'sine=frequency=440:sample_rate=48000:duration=1',
                             '-af', 'asetpts=PTS+2/TB,ebur128=framelog=verbose', '-f', 'null', '-'],
                            capture_output=True, timeout=20)
    assert result.returncode == 0
    points = parse_loudness(result.stderr.decode('utf8', 'replace'))
    assert points[0][0] >= 2
    values = per_second(points, 3)
    assert [values[0]['momentary_lufs'], values[1]['momentary_lufs']] == [None, None]
    assert values[2]['momentary_lufs'] is not None


def test_short_final_bucket_is_explicitly_missing():
    assert per_second([(.1, -30), (1.0, -20)], 2.05)[2]['momentary_lufs'] is None


def test_silence_malformed_and_case_are_handled():
    assert parse_silence('[silencedetect @ x] SILENCE_START: 0.5\n[silencedetect @ x] SILENCE_END: 1.0', 2) == [{'start_s': .5, 'end_s': 1.0}]
    with pytest.raises(EngineError):
        parse_silence('[silencedetect @ x] silence_start: 0.5\n[silencedetect @ x] silence_end: NaN', 2)


def test_numeric_overflow_not_treated_as_negative_infinity():
    with pytest.raises(EngineError):
        parse_loudness('[Parsed_ebur128_0 @ x] t: 0.1 TARGET:-23 M:-1e999 S:-20')
    assert parse_loudness('[Parsed_ebur128_0 @ x] t: 0.1 TARGET:-23 M:-inf S:-20') == [(0.1, -70.0)]


def test_last_bucket_cannot_use_sample_beyond_duration():
    assert per_second([(2.9, -20)], 2.05)[2]['momentary_lufs'] is None
