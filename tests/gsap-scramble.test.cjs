const {test} = require('node:test');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const path = require('node:path');
const url=pathToFileURL(path.resolve(__dirname,'../skills/video-theme-library/assets/gsap-recipes/seeded-scramble.mjs')).href;
test('seeded scramble rejects invalid delay and handles Unicode code points', async ()=>{
 const {build}=await import(url); let state;
 const timeline={fromTo(target){state=target;return this;}};
 const element={textContent:''};
 assert.throws(()=>build(timeline,{target:element,text:'abc',revealDelay:1}),/revealDelay/);
 build(timeline,{target:element,text:'A😀B',chars:'😀🚀',seed:3});
 state.progress=.5; assert.equal(Array.from(element.textContent).length,3);
 assert.doesNotMatch(element.textContent,/\uFFFD/);
 state.progress=1; assert.equal(element.textContent,'A😀B');
});
