"""GSAP catalog retains core-draw and marks unverified recipes as candidates."""
import hashlib
import json
from pathlib import Path

from video_studio.effect_library.catalog import validate_entry


def test_gsap_entries_have_valid_assets_and_honest_evidence():
    root = Path(__file__).resolve().parents[1]
    entries = json.loads((root / 'skills/video-theme-library/assets/effect-library/entries.json').read_text(encoding='utf8'))
    gsap = [entry for entry in entries if entry['id'].startswith('VE-gsap-')]
    assert len(gsap) == 9
    assert len({entry['id'] for entry in gsap}) == 9
    for entry in gsap:
        validate_entry(entry)
        if entry['asset']:
            assert hashlib.sha256((root / entry['asset']['path']).read_bytes()).hexdigest() == entry['asset']['sha256']
        if entry['id'] not in {'VE-gsap-core-draw', 'VE-gsap-seek-safety'}:
            assert entry['maturity'] == 'candidate'
            assert entry['checks']['render'] == 'pass'
            assert 'HyperFrames 0.8.54' in entry['evidence']['render']
