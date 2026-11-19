"""Strict S4 data reads and reference validation, without publication."""
import pytest
from video_studio.contract import ContractError
from video_studio.reference._scan import read_json_strict, validate_ref


@pytest.mark.parametrize('payload', ['{"x": 1, "x": 2}', '{"x": NaN}', '{"x": Infinity}', '{bad'])
def test_invalid_json_is_rejected(tmp_path, payload):
    path = tmp_path / 'data.json'
    path.write_text(payload, encoding='utf8')
    with pytest.raises(ContractError):
        read_json_strict(path)


def test_read_json_valid_and_bounded(tmp_path):
    path = tmp_path / 'data.json'
    path.write_text('{"x": 1}', encoding='utf8')
    assert read_json_strict(path) == {'x': 1}
    with pytest.raises(ContractError):
        read_json_strict(path, max_bytes=4)


@pytest.mark.parametrize('ref', ['frame:../x.png', 'frame:/etc/x', 'frame:C:/x.png',
                                 'frame:\\\\h\\s\\x.png', 'tile:', 'cue:evidence/a.json',
                                 'frame:evidence/a\x00.png'])
def test_invalid_ref_rejected(tmp_path, ref):
    assert validate_ref(tmp_path, ref) is not None


def test_valid_ref_must_exist_and_links_are_rejected(tmp_path):
    root = tmp_path / 'evidence' / 'shots'
    root.mkdir(parents=True)
    target = root / 'SH001_mid.png'
    target.write_bytes(b'test')
    assert validate_ref(tmp_path, 'frame:evidence/shots/SH001_mid.png') is None
    assert validate_ref(tmp_path, 'frame:evidence/shots/missing.png') is not None


def test_hardlinked_evidence_and_json_are_rejected(tmp_path):
    import os
    root = tmp_path / 'evidence'
    root.mkdir()
    original = root / 'original.png'
    original.write_bytes(b'x')
    alias = root / 'alias.png'
    json_file = tmp_path / 'source.json'
    json_file.write_text('{"ok":true}', encoding='utf8')
    json_alias = tmp_path / 'alias.json'
    try:
        os.link(original, alias)
        os.link(json_file, json_alias)
    except OSError:
        pytest.skip('filesystem does not support hardlinks')
    assert validate_ref(tmp_path, 'frame:evidence/alias.png') is not None
    with pytest.raises(ContractError):
        read_json_strict(json_alias)


def test_symlink_leaf_and_parent_are_rejected(tmp_path):
    import os
    outside = tmp_path / 'outside'
    outside.mkdir()
    (outside / 'image.png').write_bytes(b'x')
    evidence = tmp_path / 'evidence'
    evidence.mkdir()
    try:
        os.symlink(outside / 'image.png', evidence / 'leaf.png')
        os.symlink(outside, evidence / 'parent', target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip('symlink creation unavailable')
    assert validate_ref(tmp_path, 'frame:evidence/leaf.png') is not None
    assert validate_ref(tmp_path, 'frame:evidence/parent/image.png') is not None


@pytest.mark.parametrize('payload', ['{"a":{"x":1,"x":2}}', '{"x":1e999}'])
def test_nested_duplicate_and_overflow_are_rejected(tmp_path, payload):
    path = tmp_path / 'data.json'
    path.write_text(payload, encoding='utf8')
    with pytest.raises(ContractError):
        read_json_strict(path)
