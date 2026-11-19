"""Guard seek-safe GSAP recipe assets against the forbidden FR3.3 patterns."""
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/video-theme-library/assets/gsap-recipes'
FORBIDDEN = {
    'Math.random': r'\bMath\s*\.\s*random\b',
    'Date.now': r'\bDate\s*\.\s*now\b',
    'performance.now': r'\bperformance\s*\.\s*now\b',
    'infinite repeat': r'\brepeat\s*:\s*-\s*1\b',
    'gsap.utils.random': r'\bgsap\s*\.\s*utils\s*\.\s*random\b',
    'ScrollTrigger': r'\bScrollTrigger\b',
    'remote URL': r'https?\s*:\s*//',
    'CDN': r'cdn',
}


def forbidden_patterns(source):
    return [name for name, pattern in FORBIDDEN.items() if re.search(pattern, source, re.IGNORECASE)]


@pytest.mark.parametrize(('name', 'source'), [
    ('Math.random', 'const x = Math . random();'),
    ('Date.now', 'const x = Date.now();'),
    ('performance.now', 'const x = performance.now();'),
    ('infinite repeat', 'const opts = {repeat : - 1};'),
    ('gsap.utils.random', 'gsap . utils . random(0, 1)'),
    ('ScrollTrigger', 'gsap.registerPlugin(ScrollTrigger);'),
    ('remote URL', 'const source = "https://example.invalid/file.js";'),
    ('CDN', 'const name = "cdnjs";'),
])
def test_forbidden_pattern_is_detected(name, source):
    assert name in forbidden_patterns(source)


def test_local_deterministic_code_is_allowed():
    assert not forbidden_patterns('const repeat = 1; const url = "./motion.mjs";')


def test_all_gsap_recipe_assets_pass_static_gate():
    assets = sorted(path for path in ASSETS.rglob('*') if path.is_file() and path.suffix.lower() in {'.js', '.mjs'})
    assert assets, 'no recipe assets found'
    failures = {path.name: found for path in assets if (found := forbidden_patterns(path.read_text(encoding='utf8')))}
    assert not failures, failures
