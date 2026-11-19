"""Compare DrawSVG cold and reverse pixels with a local pinned tarball."""
import hashlib
import io
import json
import os
from pathlib import Path
import tarfile

import pytest


def test_drawsvg_initial_pixels_against_reverse():
    supplied = os.environ.get('GSAP_TEST_TARBALL')
    if not supplied:
        pytest.skip('not_run: GSAP_TEST_TARBALL not supplied')
    root = Path(__file__).resolve().parents[1]
    lock = json.loads((root / 'video_studio/locks/runtime-libs.json').read_text(encoding='utf8'))
    blob = Path(supplied).read_bytes()
    assert hashlib.sha256(blob).hexdigest() == lock['packages']['gsap']['tarball_sha256']
    with tarfile.open(fileobj=io.BytesIO(blob), mode='r:gz') as tar:
        scripts = []
        for name in ['gsap', 'gsap-drawsvg']:
            member = lock['libs'][name]['members'][0]
            data = tar.extractfile(member['member']).read()
            assert hashlib.sha256(data).hexdigest() == member['file_sha256']
            scripts.append(data.decode('utf8'))
    api = pytest.importorskip('playwright.sync_api')
    with api.sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_default_timeout(5000)
            page.set_content('<svg xmlns="http://www.w3.org/2000/svg" width="500" height="180"><path id="p" d="M10 30 L200 30" stroke="black" /></svg>')
            for script in scripts:
                page.add_script_tag(content=script)
            import base64
            recipe = base64.b64encode((root / 'skills/video-theme-library/assets/gsap-recipes/draw-svg.mjs').read_bytes()).decode()
            result = page.evaluate('''async RECIPE => {
                gsap.registerPlugin(DrawSVGPlugin);
                const path=document.querySelector('#p');
                const recipe=await import('data:text/javascript;base64,'+RECIPE); const tl=gsap.timeline({paused:true}); recipe.build(tl,{targets:path,ease:'none'});
                const pixels=async()=>{
                    const svg=document.querySelector('svg').cloneNode(true),p=svg.querySelector('path'),s=getComputedStyle(path);
                    p.style.strokeDasharray=s.strokeDasharray;p.style.strokeDashoffset=s.strokeDashoffset;
                    const image=new Image(); image.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(svg));
                    await Promise.race([image.decode(),new Promise((_,reject)=>setTimeout(()=>reject(Error('decode timeout')),3000))]);
                    const canvas=document.createElement('canvas'); canvas.width=500;canvas.height=180;
                    const ctx=canvas.getContext('2d');ctx.drawImage(image,0,0);return [...ctx.getImageData(0,0,500,180).data];
                };
                tl.totalTime(0,true);const initial=await pixels();tl.totalTime(1,true);tl.totalTime(0,true);const reverse=await pixels();
                tl.totalTime(.5,true);const middle=await pixels();
                return {same:initial.every((v,i)=>v===reverse[i]), changed:initial.some((v,i)=>v!==middle[i])};
            }''', recipe)
            assert result == {'same': True, 'changed': True}
        finally:
            browser.close()
