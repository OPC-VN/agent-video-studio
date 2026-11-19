"""Breakdown transformations preserve measurements without copying transcript text."""
import json
import pytest
from video_studio.contract import ContractError
from video_studio.reference.breakdown import link_speech, merge_audio, rhythm


def test_link_speech_counts_overlap_without_copying_transcript():
    shot = {'start_s': 0, 'end_s': 2}
    transcript = {'reference': {'words': [{'type': 'cue', 'text': 'xin chao cac ban', 'start': .2, 'end': 1.8},
                                        {'type': 'cue', 'text': 'sau do', 'start': 2, 'end': 3}]}}
    result = link_speech(shot, transcript)
    assert result == {'cue_ids': ['reference#0'], 'word_count': 4}
    assert 'xin chao' not in json.dumps(result)


def test_invalid_transcript_stem_is_not_written_into_output():
    with pytest.raises(ContractError):
        link_speech({'start_s': 0, 'end_s': 2}, {'../private': {'words': []}})


def test_audio_intervals_are_clipped_and_missing_stays_unknown():
    shot = {'start_s': 1, 'end_s': 3}
    assert merge_audio(shot, None) == {'loudness_lufs_mean': None, 'silence_spans': [], 'onsets': []}
    audio = {'loudness': [{'t_s': 1, 'momentary_lufs': -20}, {'t_s': 2, 'momentary_lufs': None}],
             'silence_spans': [{'start_s': .5, 'end_s': 1.5}], 'onsets': [{'t_s': 2, 'rise_lu': 7}]}
    assert merge_audio(shot, audio) == {'loudness_lufs_mean': -20, 'silence_spans': [{'start_s': 1, 'end_s': 1.5}], 'onsets': [{'t_s': 2, 'rise_lu': 7}]}


def test_rhythm_only_reports_measured_cut_counts():
    shots = [{'start_s': 0, 'end_s': 2}, {'start_s': 2, 'end_s': 5}, {'start_s': 5, 'end_s': 7}]
    assert rhythm(shots) == {'shot_count': 3, 'median_shot_s': 2, 'cuts_per_10s': [2], 'tempo_shifts': []}


def test_transcript_mixed_key_types_fail_as_contract_error():
    with pytest.raises(ContractError):
        link_speech({'start_s': 0, 'end_s': 2}, {'ok': {'words': []}, 1: {'words': []}})


def test_word_granularity_does_not_claim_cue_ids():
    result = link_speech({'start_s': 0, 'end_s': 2}, {'asr': {'granularity': 'word', 'words': [
        {'type': 'word', 'text': 'Hello', 'start': .1, 'end': .4}]}})
    assert result['word_count'] == 1 and result['cue_ids'] == []
    assert result['unverified']


@pytest.mark.parametrize('bad_audio', [
    {'loudness': [{'t_s': 99, 'momentary_lufs': float('nan')}], 'silence_spans': [], 'onsets': []},
    {'loudness': [{'t_s': 1, 'momentary_lufs': -20}, {'t_s': 1, 'momentary_lufs': -30}], 'silence_spans': [], 'onsets': []},
    {'loudness': [], 'silence_spans': [], 'onsets': [{'t_s': 20, 'rise_lu': -4}]},
])
def test_invalid_measurement_outside_shot_is_not_ignored(bad_audio):
    with pytest.raises(ContractError):
        merge_audio({'start_s': 0, 'end_s': 2}, bad_audio)


def test_machine_fields_cannot_be_silently_modified():
    from video_studio.reference.breakdown import check_machine_fields
    source = [{'id': 'SH001', 'start_s': 0, 'end_s': 2, 'duration_s': 2,
               'basis': 'measured', 'cut_in': 'unknown',
               'frames': {'first': 'frame:evidence/shots/SH001_first.png'}}]
    modified = [dict(source[0], end_s=3)]
    with pytest.raises(ContractError):
        check_machine_fields(modified, source)
    changed_type = [dict(source[0], start_s=False)]
    with pytest.raises(ContractError):
        check_machine_fields(changed_type, source)
    check_machine_fields([dict(source[0], viewer_job='intro')], source)


def test_machine_checks_reject_unbacked_speech_or_audio():
    from video_studio.reference.breakdown import check_machine_fields
    source = [{'id': 'SH001', 'start_s': 0, 'end_s': 2, 'duration_s': 2,
               'basis': 'measured', 'cut_in': 'unknown', 'frames': {'mid': {'pts_time': 1.0}}}]
    for extra in ({'speech': {'word_count': 7}}, {'audio': {'loudness_lufs_mean': -20}}):
        with pytest.raises(ContractError):
            check_machine_fields([dict(source[0], **extra)], source)
    with pytest.raises(ContractError):
        check_machine_fields([dict(source[0], frames={'mid': {'pts_time': 1.5}})], source)


def test_machine_checks_reject_speech_audio_tamper_missing_and_reorder():
    from video_studio.reference.breakdown import check_machine_fields
    first = {'id':'SH001','start_s':0,'end_s':1,'duration_s':1,'basis':'measured','cut_in':'unknown',
             'frames':{},'speech':{'cue_ids':['a#0'],'word_count':2},'audio':{'loudness_lufs_mean':-20.0}}
    second = dict(first,id='SH002',start_s=1,end_s=2,cut_in='hard')
    for changed in ([dict(first,speech={'cue_ids':['a#1'],'word_count':2}), second],
                    [dict(first,speech={'cue_ids':['a#0'],'word_count':3}), second],
                    [dict(first,audio={'loudness_lufs_mean':-19.0}), second],
                    [first], [second, first]):
        with pytest.raises(ContractError):
            check_machine_fields(changed, [first, second])
