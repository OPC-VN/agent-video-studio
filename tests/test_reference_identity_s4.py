"""Do not merge evidence produced from different source bytes."""
import pytest
from video_studio.contract import ContractError
from video_studio.reference._identity import require_same_source


A = 'a' * 64
B = 'b' * 64


def test_matching_digests_and_absent_optional_provenance():
    assert require_same_source(A, {'sha256': A}, {'sha256': A}, None) == A


def test_mixed_shots_audio_or_reference_are_rejected():
    with pytest.raises(ContractError):
        require_same_source(A, {'sha256': A}, {'sha256': B}, None)
    with pytest.raises(ContractError):
        require_same_source(A, {'sha256': A}, {'sha256': A}, B)


@pytest.mark.parametrize('bad', ['', 'z' * 64, 'a' * 63, None])
def test_missing_or_invalid_machine_source_digest_is_rejected(bad):
    with pytest.raises(ContractError):
        require_same_source(A, {'sha256': bad}, {'sha256': A}, None)


def test_absent_audio_allowed_but_present_invalid_audio_rejected():
    assert require_same_source(A, {'sha256': A}, None, None) == A
    with pytest.raises(ContractError):
        require_same_source(A, {'sha256': A}, {}, None)
    with pytest.raises(ContractError):
        require_same_source(A, {'sha256': A}, {'sha256': B, 'has_audio': False}, None)
