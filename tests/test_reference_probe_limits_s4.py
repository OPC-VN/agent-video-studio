"""Input metadata must be bounded before decode."""
import pytest
from video_studio.contract import ContractError
from video_studio.reference._scan_media import validate_probe_metadata


def sample():
    return {'format': {'duration':'2.0'}, 'streams': [
        {'index':0, 'codec_type':'video', 'width':640, 'height':360, 'avg_frame_rate':'30/1'},
        {'index':1, 'codec_type':'audio', 'channels':2, 'sample_rate':'48000'}]}


def test_accepts_bounded_video_and_audio():
    assert validate_probe_metadata(sample()) == {'duration_s':2.0,'width':640,'height':360,'fps':30.0,'has_audio':True}


@pytest.mark.parametrize('change', ['pixels', 'streams', 'fps', 'duration', 'audio_channels', 'audio_rate'])
def test_resource_limits_reject_unsafe_metadata(change):
    data=sample()
    if change=='pixels': data['streams'][0]['width']=10000
    if change=='streams': data['streams'] *= 3
    if change=='fps': data['streams'][0]['avg_frame_rate']='1000/1'
    if change=='duration': data['format']['duration']='999999'
    if change=='audio_channels': data['streams'][1]['channels']=64
    if change=='audio_rate': data['streams'][1]['sample_rate']='1000000'
    with pytest.raises(ContractError): validate_probe_metadata(data)


@pytest.mark.parametrize('bad', [48000.9, True, float('nan'), float('inf'), 10**1000, '48000.5', '-48000'])
def test_audio_rate_cannot_be_coerced_from_invalid_values(bad):
    data=sample(); data['streams'][1]['sample_rate']=bad
    with pytest.raises(ContractError):
        validate_probe_metadata(data)


def test_multiple_video_streams_are_rejected():
    data=sample();data['streams'].append(dict(data['streams'][0],index=2))
    with pytest.raises(ContractError):
        validate_probe_metadata(data)
