"""Optional browser check against a locally supplied, hash-pinned GSAP core."""
import hashlib
import json
import os
from pathlib import Path

import pytest


def test_core_draw_seek():
    supplied = os.environ.get("GSAP_TEST_FILE")
    if not supplied:
        pytest.skip("not_run: GSAP_TEST_FILE not provided")
    core = Path(supplied)
    root = Path(__file__).resolve().parents[1]
    lock = json.loads((root / "video_studio/locks/runtime-libs.json").read_text(encoding="utf-8"))
    member = lock["libs"]["gsap"]["members"][0]
    with core.open("rb") as stream:
        core_bytes = stream.read(member["max_bytes"] + 1)
    assert len(core_bytes) <= member["max_bytes"]
    assert hashlib.sha256(core_bytes).hexdigest() == member["file_sha256"]
    browser_api = pytest.importorskip("playwright.sync_api")
    recipe = root / "skills/video-theme-library/assets/gsap-recipes/core-draw.js"
    with browser_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_content('<svg><path id="p" pathLength="1" d="M0 0 L100 0" stroke="black"/></svg>')
            page.add_script_tag(content=core_bytes.decode("utf-8"))
            page.add_script_tag(path=str(recipe))
            page.evaluate('()=>{window.tl=gsap.timeline({paused:true});addCoreDraw(tl,document.querySelector("#p"),{duration:2});}')
            def sample(t):
                return page.evaluate('(t)=>{tl.totalTime(t,true);const s=getComputedStyle(document.querySelector("#p"));return [parseFloat(s.strokeDashoffset),s.strokeDasharray]}', t)
            times = [0, 0.5, 1, 1.5, 2]
            forward = {t: sample(t) for t in times}
            assert forward == {t: sample(t) for t in reversed(times)}
            assert forward == {t: sample(t) for t in [1.5, 0, 2, 0.5, 1]}
            for t, expected in zip(times, [1, .75, .5, .25, 0]):
                assert forward[t][0] == pytest.approx(expected)
                assert forward[t][1] == "1px, 1px"
        finally:
            browser.close()
