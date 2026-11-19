"""Pure breakdown transformations; no user transcript text appears in output."""
import math
import re
import statistics

from ..contract import ContractError

SCHEMA = 'video_studio.breakdown.v1'
UNTRUSTED_FIELDS = ['shots[].text_layers[].text_summary', 'beats[].hypothesis']
OBSERVED_FIELDS = ('method', 'framing', 'layout', 'motion', 'viewer_job')
SCENE_ROLES = ('hook', 'explain', 'proof', 'emphasis', 'transition', 'closing', 'cta', 'ambient')
_STEM = re.compile(r'[A-Za-z0-9_-][A-Za-z0-9._-]{0,99}\Z')
_MAX_CUES = 100000
_MAX_TEXT = 1000000


def _number(value):
    try:
        if isinstance(value, bool):
            raise ValueError
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ContractError('thời điểm phải là số hữu hạn') from None
    if not math.isfinite(result):
        raise ContractError('thời điểm phải là số hữu hạn')
    return result


def _bounds(shot):
    try:
        start, end = _number(shot['start_s']), _number(shot['end_s'])
    except (KeyError, TypeError):
        raise ContractError('cảnh thiếu biên') from None
    if start < 0 or end <= start:
        raise ContractError('biên cảnh không hợp lệ')
    return start, end


def link_speech(shot, transcripts):
    start, end = _bounds(shot)
    if not isinstance(transcripts, dict):
        raise ContractError('transcripts phải là object')
    if any(not isinstance(stem, str) or not _STEM.fullmatch(stem) or '..' in stem for stem in transcripts):
        raise ContractError('tên transcript không an toàn')
    cue_ids, count, seen, word_level = [], 0, 0, False
    for stem, transcript in sorted(transcripts.items()):
        if not isinstance(transcript, dict) or not isinstance(transcript.get('words'), list):
            raise ContractError('transcript.words phải là danh sách')
        for index, cue in enumerate(transcript['words']):
            seen += 1
            if seen > _MAX_CUES or not isinstance(cue, dict):
                raise ContractError('cue không hợp lệ hoặc quá nhiều')
            kind = cue.get('type')
            if kind not in ('cue', 'word'):
                raise ContractError('loại cue không hợp lệ')
            word_level = word_level or kind == 'word'
            text = cue.get('text')
            if not isinstance(text, str) or len(text) > _MAX_TEXT:
                raise ContractError('nội dung cue không hợp lệ hoặc quá lớn')
            cue_start, cue_end = _number(cue.get('start')), _number(cue.get('end'))
            if cue_start < 0 or cue_end <= cue_start:
                raise ContractError('biên cue không hợp lệ')
            if cue_start < end and cue_end > start:
                if kind == 'cue':
                    cue_ids.append(f'{stem}#{index}')
                count += len(text.split())
    result = {'cue_ids': cue_ids, 'word_count': count}
    if word_level:
        result['unverified'] = ['các từ ASR không có cue ID']
    return result


def merge_audio(shot, audio):
    start, end = _bounds(shot)
    if audio is None:
        return {'loudness_lufs_mean': None, 'silence_spans': [], 'onsets': []}
    if not isinstance(audio, dict):
        raise ContractError('audio phải là object')
    samples = audio.get('loudness')
    spans = audio.get('silence_spans')
    onsets = audio.get('onsets')
    if not all(isinstance(items, list) and len(items) <= 3600 for items in (samples, spans, onsets)):
        raise ContractError('audio thiếu danh sách số đo hoặc vượt trần')
    values = []
    last_timestamp = -1
    for item in samples:
        try:
            timestamp = _number(item['t_s'])
            volume = item['momentary_lufs']
        except (KeyError, TypeError):
            raise ContractError('số đo loudness không hợp lệ') from None
        if timestamp < 0 or timestamp <= last_timestamp:
            raise ContractError('mốc loudness trùng, âm hoặc không tăng')
        last_timestamp = timestamp
        if volume is not None:
            volume = _number(volume)
            if start <= timestamp < end:
                values.append(volume)
    clipped = []
    last_end = -1
    for item in spans:
        left, right = _bounds(item)
        if left < last_end:
            raise ContractError('khoảng lặng chồng hoặc không tăng')
        last_end = right
        if left < end and right > start:
            clipped.append({'start_s': max(start, left), 'end_s': min(end, right)})
    hits = []
    last_onset = -1
    for item in onsets:
        try:
            timestamp, rise = _number(item['t_s']), _number(item['rise_lu'])
        except (KeyError, TypeError):
            raise ContractError('mốc onset không hợp lệ') from None
        if timestamp < 0 or timestamp <= last_onset or rise < 0:
            raise ContractError('mốc onset hoặc độ tăng không hợp lệ')
        last_onset = timestamp
        if start <= timestamp < end:
            hits.append({'t_s': timestamp, 'rise_lu': rise})
    return {'loudness_lufs_mean': statistics.mean(values) if values else None,
            'silence_spans': clipped, 'onsets': hits}


def rhythm(shots):
    if not isinstance(shots, list) or not shots or len(shots) > 40:
        raise ContractError('cần từ 1 đến 40 cảnh')
    intervals = [_bounds(shot) for shot in shots]
    if intervals[0][0] != 0 or any(a[1] != b[0] for a, b in zip(intervals, intervals[1:])):
        raise ContractError('biên cảnh phải liền nhau từ 0')
    end = intervals[-1][1]
    if end > 3600:
        raise ContractError('video vượt trần thời lượng')
    counts = [0] * math.ceil(end / 10)
    for start, _ in intervals[1:]:
        counts[int(start // 10)] += 1
    return {'shot_count': len(shots), 'median_shot_s': statistics.median(end - start for start, end in intervals),
            'cuts_per_10s': counts, 'tempo_shifts': []}


def _strict_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_strict_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def check_machine_fields(observed, authoritative):
    """Reject edits to measurements; caller supplies freshly validated authoritative records."""
    if (not isinstance(observed, list) or not isinstance(authoritative, list)
            or not 1 <= len(authoritative) <= 40 or len(observed) != len(authoritative)):
        raise ContractError('số cảnh không khớp bằng chứng')
    required = ('id', 'start_s', 'end_s', 'duration_s', 'basis', 'cut_in', 'frames')
    for actual, expected in zip(observed, authoritative):
        if not isinstance(actual, dict) or not isinstance(expected, dict):
            raise ContractError('cảnh không phải object')
        for key in required:
            if key not in actual or key not in expected or not _strict_equal(actual[key], expected[key]):
                raise ContractError(f'trường đo {key} không khớp bằng chứng')
        for key in ('speech', 'audio'):
            if (key in expected) != (key in actual) or (key in expected and not _strict_equal(actual[key], expected[key])):
                raise ContractError(f'trường đo {key} không khớp bằng chứng')


_AUDIO_ABSENT = object()


def build_breakdown(shots_doc, provenance, snapshot_sha, *, audio=_AUDIO_ABSENT, transcripts=None):
    """Create a pending breakdown from validated measured inputs; does not read or publish files."""
    from .. import _paths
    from ._identity import require_same_source

    if not isinstance(shots_doc, dict) or shots_doc.get('schema') != 'video_studio.shots.v1':
        raise ContractError('shots schema không hợp lệ')
    if not isinstance(provenance, dict) or provenance.get('rights_status') not in ('approved', 'rights_pending'):
        raise ContractError('hồ sơ quyền không hợp lệ hoặc bị chặn')
    source = shots_doc.get('source')
    if not isinstance(source, dict):
        raise ContractError('thiếu nguồn shots')
    fields = ('name', 'sha256', 'duration_s', 'width', 'height', 'fps', 'has_audio')
    if any(key not in source for key in fields):
        raise ContractError('nguồn shots thiếu trường')
    try:
        if not isinstance(source['name'], str):
            raise ValueError('name is not text')
        safe_name = _paths.plain_name(source['name'], 'source.name')
    except (ContractError, TypeError, ValueError) as exc:
        raise ContractError('source.name không hợp lệ') from exc
    def measured_number(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ContractError('trường đo phải là số hữu hạn')
        return _number(value)
    duration = measured_number(source['duration_s'])
    if duration <= 0 or duration > 3600:
        raise ContractError('duration ngoài giới hạn')
    if any(not isinstance(source[key], int) or isinstance(source[key], bool) or not 0 < source[key] <= 4096
           for key in ('width', 'height')):
        raise ContractError('kích thước nguồn không hợp lệ')
    if not isinstance(source['has_audio'], bool):
        raise ContractError('has_audio không hợp lệ')
    if source['fps'] is not None and not 0 < measured_number(source['fps']) <= 240:
        raise ContractError('fps không hợp lệ')
    if audio is not _AUDIO_ABSENT and (not isinstance(audio, dict) or audio.get('schema') != 'video_studio.audio.v1'):
        raise ContractError('audio schema không hợp lệ')
    if audio is not _AUDIO_ABSENT and audio.get('has_audio') is not source['has_audio']:
        raise ContractError('has_audio không khớp nguồn')
    if audio is not _AUDIO_ABSENT and (not isinstance(audio.get('source'), dict) or
            not _strict_equal(audio['source'], source)):
        raise ContractError('nguồn audio không khớp nguồn shots')
    if audio is not _AUDIO_ABSENT and not audio['has_audio']:
        if any(audio.get(key) != [] for key in ('loudness', 'silence_spans', 'onsets')):
            raise ContractError('audio không có tiếng nhưng số đo không rỗng')
    reference = provenance.get('reference', {})
    if not isinstance(reference, dict):
        raise ContractError('hồ sơ reference không hợp lệ')
    require_same_source(snapshot_sha, source,
                        None if audio is _AUDIO_ABSENT else audio.get('source'), reference.get('sha256'))
    shots = shots_doc.get('shots')
    measured_rhythm = rhythm(shots)
    if measured_number(shots[-1]['end_s']) != duration:
        raise ContractError('cảnh không phủ hết thời lượng nguồn')
    output_shots = []
    for number, shot in enumerate(shots, 1):
        start, end = _bounds(shot)
        measured_number(shot.get('start_s'))
        measured_number(shot.get('end_s'))
        if (shot.get('id') != f'SH{number:03d}' or shot.get('basis') != 'measured'
                or shot.get('cut_in') != ('unknown' if number == 1 else 'hard')
                or not math.isclose(measured_number(shot.get('duration_s')), end - start, rel_tol=1e-12, abs_tol=1e-12)):
            raise ContractError('cảnh đo không hợp lệ')
        frames = shot.get('frames')
        if not isinstance(frames, dict) or set(frames) != {'first', 'mid', 'last'}:
            raise ContractError('cảnh thiếu ba khung đo')
        previous = None
        for label in ('first', 'mid', 'last'):
            frame = frames[label]
            if not isinstance(frame, dict) or set(frame) != {'file', 'pts_time'}:
                raise ContractError('khung đo không hợp lệ')
            if frame['file'] != f'evidence/shots/SH{number:03d}_{label}.png':
                raise ContractError('đường khung đo không hợp lệ')
            timestamp = measured_number(frame['pts_time'])
            if not start <= timestamp < end or (previous is not None and timestamp < previous):
                raise ContractError('PTS không thuộc cảnh hoặc không tăng')
            previous = timestamp
        speech = link_speech(shot, {} if transcripts is None else transcripts)
        observation = {'method': None, 'method_evidence': [], 'framing': None, 'layout': None,
                       'text_layers': [], 'motion': None, 'audio_obs': None, 'viewer_job': None,
                       'scene_role': None, 'unknown': []}
        output_shots.append({'id': shot['id'], 'beat_id': None, 'start_s': shot['start_s'],
                             'end_s': shot['end_s'], 'duration_s': shot['duration_s'], 'basis': 'measured',
                             'cut_in': shot['cut_in'], 'frames': {key: dict(value) for key, value in frames.items()},
                             'speech': speech, 'audio': merge_audio(shot, None if audio is _AUDIO_ABSENT else audio),
                             **observation})
    detector = shots_doc.get('detector')
    if not isinstance(detector, dict) or detector.get('tool') != 'ffmpeg-select-scene':
        raise ContractError('detector shots không hợp lệ')
    allowed_detector = ('tool', 'threshold', 'min_shot_s', 'ffmpeg_version', 'note')
    if set(detector) - set(allowed_detector):
        raise ContractError('detector có trường không hợp lệ')
    if 'threshold' in detector and not 0 < measured_number(detector['threshold']) < 1:
        raise ContractError('threshold không hợp lệ')
    if 'min_shot_s' in detector and not 0 < measured_number(detector['min_shot_s']) <= 3600:
        raise ContractError('min_shot_s không hợp lệ')
    for key in ('ffmpeg_version', 'note'):
        if key in detector:
            value = detector[key]
            if (not isinstance(value, str) or len(value) > 500 or
                    any(ord(c) < 32 or c in '/\\:' for c in value)):
                raise ContractError('detector chứa dữ liệu không hợp lệ')
    canonical_note = ('Chỉ phát hiện cắt cứng bằng độ đổi khung (ffmpeg scene); '
                      'chuyển cảnh mờ hoặc trượt có thể bị sót. Ngưỡng chưa hiệu chỉnh trên video thật.')
    if 'note' in detector and detector['note'] != canonical_note:
        raise ContractError('detector.note không khớp ghi chú chuẩn')
    detector = {key: detector[key] for key in allowed_detector if key in detector}
    rights = {'rights_status': provenance['rights_status'], 'rights_basis': provenance.get('rights_basis'),
              'publish_intent': provenance.get('publish_intent', 'public')}
    if rights['rights_basis'] not in (None, 'own_content', 'written_permission', 'license') or rights['publish_intent'] not in ('public', 'private'):
        raise ContractError('hồ sơ quyền không hợp lệ')
    safe_source = {key: source[key] for key in fields}
    safe_source['name'] = safe_name
    notes = ['chưa đo âm'] if audio is _AUDIO_ABSENT else []
    if audio is not _AUDIO_ABSENT and audio['has_audio']:
        measurements = audio['loudness']
        observed = {item['t_s'] for item in measurements if item['momentary_lufs'] is not None}
        if not set(range(math.ceil(duration))).issubset(observed):
            notes.append('thiếu số đo âm ở một hoặc nhiều giây')
    if any(shot['speech'].get('unverified') for shot in output_shots):
        notes.append('các từ ASR không có cue ID')
    return {'schema': SCHEMA, 'source': safe_source, 'rights': rights, 'detector': detector,
            'summary': {**measured_rhythm, 'ratio': None, 'hook_note': None, 'narration': None, 'music': None},
            'rhythm': measured_rhythm, 'shots': output_shots, 'beats': [], 'flags': [],
            'unverified': notes,
            'untrusted_fields': list(UNTRUSTED_FIELDS)}
