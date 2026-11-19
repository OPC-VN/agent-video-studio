"""Optional real-browser seek test using the locally cached pinned GSAP tarball."""
import base64
import hashlib
import json
import os
from pathlib import Path
import tarfile

import pytest


def test_gsap_recipe_seek_real_browser():
    supplied = os.environ.get('GSAP_TEST_TARBALL')
    if not supplied:
        pytest.skip('not_run: GSAP_TEST_TARBALL not supplied')
    root = Path(__file__).resolve().parents[1]
    lock = json.loads((root / 'video_studio/locks/runtime-libs.json').read_text(encoding='utf8'))
    blob = Path(supplied).read_bytes()
    assert hashlib.sha256(blob).hexdigest() == lock['packages']['gsap']['tarball_sha256']
    import io
    with tarfile.open(fileobj=io.BytesIO(blob), mode='r:gz') as archive:
        scripts = []
        for name in ['gsap', 'gsap-drawsvg', 'gsap-morphsvg', 'gsap-motionpath', 'gsap-splittext', 'gsap-flip', 'gsap-customease']:
            member = lock['libs'][name]['members'][0]
            data = archive.extractfile(member['member']).read()
            assert hashlib.sha256(data).hexdigest() == member['file_sha256']
            scripts.append(data.decode('utf8'))
    browser_api = pytest.importorskip('playwright.sync_api')
    with browser_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_content('''<style>body{font:20px monospace}.box{position:absolute;left:20px;top:200px;width:40px;height:40px;background:red}.moved{left:180px}</style><svg width="500" height="180"><path id="draw" d="M10 30 L200 30" stroke="black"/><path id="morph" d="M10 80 L100 80 L100 120 Z" fill="red"/><path id="shape" d="M10 80 L100 50 L150 120 Z"/><path id="path" d="M10 140 L220 140" fill="none"/><circle id="dot" r="5" fill="blue"/></svg><span id="text">HELLO</span><div id="box" class="box"></div><div id="scramble"></div><div id="ease">ease</div><div id="defaultEase">control</div>''')
            for script in scripts:
                page.add_script_tag(content=script)
            folder = root / 'skills/video-theme-library/assets/gsap-recipes'
            modules = {}
            for name in ['draw-svg','morph-svg','motion-path','split-text','flip','custom-ease','seeded-scramble','seek-check']:
                modules[name] = 'data:text/javascript;base64,' + base64.b64encode((folder / (name + '.mjs')).read_bytes()).decode()
            result = page.evaluate('''async urls => {
              const m = {}; for (const [k,v] of Object.entries(urls)) m[k] = await import(v);
              for (const k of ['draw-svg','morph-svg','motion-path','split-text','flip','custom-ease']) m[k].register(gsap, window);
              const initial=document.body.innerHTML; let tl;
              const makeFixture=()=>{ document.body.innerHTML=initial; tl=gsap.timeline({paused:true});
              m['draw-svg'].build(tl,{gsap,targets:'#draw',ease:'none'});
              m['morph-svg'].build(tl,{target:'#morph',shape:'#shape',shapeIndex:0});
              m['motion-path'].build(tl,{target:'#dot',path:'#path'});
              const split=m['split-text'].prepare(SplitText,document.querySelector('#text'),{});
              m['split-text'].build(tl,{split});
              m.flip.build(tl,{Flip,targets:'#box',change:()=>document.querySelector('#box').classList.add('moved')});
              const eases=m['custom-ease'].registerEases(gsap,CustomEase);
              tl.fromTo('#ease',{opacity:.2},{opacity:1,duration:1,ease:eases.softOvershoot},0);tl.fromTo('#defaultEase',{opacity:.2},{opacity:1,duration:1},0);
              m['seeded-scramble'].build(tl,{target:document.querySelector('#scramble'),text:'HELLO WORLD'});
              const probe=()=>JSON.stringify(['draw','morph','dot','text','box','scramble'].map(id=>{let e=document.getElementById(id);return [e.outerHTML,getComputedStyle(e).transform,getComputedStyle(e).opacity]}));
              const probes={
              draw:()=>{const s=getComputedStyle(document.querySelector('#draw'));const o=parseFloat(s.strokeDashoffset);return JSON.stringify([s.strokeDasharray,Math.abs(o)<=.002 ? 0 : o]);},
              morph:()=>{const e=document.querySelector('#morph'),len=e.getTotalLength();return JSON.stringify([Math.round(len*10)/10,...[0,.25,.5,.75,1].map(t=>{const p=e.getPointAtLength(len*t);return [Math.round(p.x*10)/10,Math.round(p.y*10)/10]})]);},
              dot:()=>getComputedStyle(document.querySelector('#dot')).transform,
              text:()=>JSON.stringify([...document.querySelector('#text').querySelectorAll('*')].map(e=>[getComputedStyle(e).transform,getComputedStyle(e).opacity])),
              box:()=>{let e=document.querySelector('#box'),r=e.getBoundingClientRect();return JSON.stringify([Math.round(r.x*100)/100,Math.round(r.y*100)/100,getComputedStyle(e).opacity]);},
              ease:()=>getComputedStyle(document.querySelector('#ease')).opacity,
              scramble:()=>document.querySelector('#scramble').textContent}; return {timeline:tl,probes}; }; window.makeRecipeFixture=makeFixture; const result=m['seek-check'].runSeekCheck({makeFixture,times:[0,.25,.5,.75,1,2]});
              const snapshot=()=>Object.fromEntries(['draw','morph','dot','text','box','scramble'].map(id=>{const e=document.getElementById(id);return [id,JSON.stringify([e.outerHTML,getComputedStyle(e).transform,getComputedStyle(e).opacity])]}));
              tl.totalTime(0,true); const start=snapshot(), x0=document.querySelector('#box').getBoundingClientRect().x; tl.totalTime(.5,true); const midEase=Number(getComputedStyle(document.querySelector('#ease')).opacity), defaultMid=Number(getComputedStyle(document.querySelector('#defaultEase')).opacity), midX=document.querySelector('#box').getBoundingClientRect().x; tl.totalTime(1,true); const end=snapshot(), x1=document.querySelector('#box').getBoundingClientRect().x;
              const finalText=document.getElementById('scramble').textContent; const path=document.querySelector('#morph'), saved=path.getAttribute('d'), geomProbe=makeFixture().probes.morph, before=geomProbe(), target=document.querySelector('#morph'); target.setAttribute('d','M10 80 L200 80 L200 120 Z'); const geomNegative=before!==geomProbe(); target.setAttribute('d',saved);
              return {result,start,end,x0,midX,x1,midEase,defaultMid,geomNegative,text:finalText};
            }''', modules)
            for key, value in result['result']['results'].items():
                if not value['ok']:
                    print(key, value['mismatches'])
            assert result['x0'] < result['midX'] < result['x1']
            assert .2 < result['midEase'] <= 1
            assert abs(result['midEase'] - .6) > .02
            assert abs(result['midEase'] - result['defaultMid']) > .02
            assert result['geomNegative']
            assert result['result']['ok']
            for name in ['draw', 'morph', 'dot', 'text', 'box', 'scramble']:
                assert result['start'][name] != result['end'][name], name
            assert result['text'] == 'HELLO WORLD'
        finally:
            browser.close()
