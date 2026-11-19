"""Pixel regression for round-capped curves before their draw-on begins."""
import base64
import io
import os
from pathlib import Path

import pytest


def test_round_capped_draw_on_is_invisible_at_zero_and_seek_safe():
    api = pytest.importorskip('playwright.sync_api')
    image = pytest.importorskip('PIL.Image')
    source = Path(__file__).resolve().parents[1] / 'skills/line-art-motion/assets/line-art.mjs'
    module = base64.b64encode(source.read_bytes()).decode('ascii')
    with api.sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(
                headless=True, executable_path=os.environ.get('CHROME_BIN') or None
            )
        except api.Error as exc:
            if 'Executable doesn\'t exist' in str(exc):
                pytest.skip('not_run: no Playwright Chromium; set CHROME_BIN')
            raise
        try:
            page = browser.new_page(viewport={'width': 1280, 'height': 720})
            page.set_content('''<style>body{margin:0} .ink{fill:none;stroke:black;
                stroke-width:1.15;stroke-linecap:round;stroke-linejoin:round}</style>
                <svg id="scene" width="1280" height="720" viewBox="0 0 320 180"
                  xmlns="http://www.w3.org/2000/svg" style="background:white">
                  <defs><filter id="ink"><feTurbulence type="fractalNoise"
                    baseFrequency=".04" numOctaves="2" seed="8" result="noise"/>
                    <feDisplacementMap in="SourceGraphic" in2="noise" scale=".45"/>
                    <feGaussianBlur stdDeviation=".12"/></filter></defs>
                  <g filter="url(#ink)"><path class="ink" d="M224 149 C222 138 224 124 225 104"/>
                    <path class="ink" d="M224 130 C213 128 207 122 207 114 C218 115 224 121 224 130"/>
                    <path class="ink" d="M225 119 C227 109 235 105 243 106 C241 115 234 119 225 119"/>
                    <path class="ink" d="M225 99 v-7 M216 102 l-5 -5 M234 102 l5 -5"/></g></svg>''')
            page.evaluate('''async encoded => {
                const m = await import('data:text/javascript;base64,' + encoded);
                window.fixedDraw = p => document.querySelectorAll('.ink').forEach(el => m.drawOn(el, p));
                window.draw = window.fixedDraw;
            }''', module)

            def pixels(progress):
                page.evaluate('p => window.draw(p)', progress)
                png = page.locator('#scene').screenshot()
                frame = image.open(io.BytesIO(png)).convert('RGB')
                return sum(count for count, (r, g, b) in frame.getcolors(frame.width * frame.height)
                           if max(r, g, b) < 200)

            # The former dash-only implementation shows round-cap dots here.
            page.evaluate('''() => { window.draw = p => {
                document.querySelectorAll('.ink').forEach(el => { el.setAttribute('pathLength', '1');
                el.style.strokeDasharray = '1'; el.style.strokeDashoffset = String(1 - p); });
            }; }''')
            assert pixels(0) > 0
            page.evaluate('() => { window.draw = window.fixedDraw; }')
            assert pixels(0) == 0
            mid = pixels(.5)
            full = pixels(1)
            assert 0 < mid < full
            assert pixels(0) == 0
            assert pixels(.5) == mid
            assert pixels(1) == full
        finally:
            browser.close()
