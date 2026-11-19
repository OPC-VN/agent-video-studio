const {test} = require("node:test");
const assert = require("node:assert/strict");
const {pathToFileURL} = require("node:url");
const path = require("node:path");
const url = pathToFileURL(path.resolve(__dirname, "../skills/video-theme-library/assets/gsap-recipes/seek-check.mjs")).href;
test("fresh fixture checks order and catches history dependence", async () => {
  const {runSeekCheck} = await import(url);
  const stable = () => { let t=0; return {timeline:{totalTime(x){t=x;}}, probes:{value:()=>String(t)}}; };
  const bad = () => { let t=0, visitedEnd=false; return {timeline:{totalTime(x){t=x; if(x===1) visitedEnd=true;}}, probes:{value:()=>`${t}:${t===.5 && visitedEnd}`}}; };
  const times=[0,.25,.5,.75,1];
  assert.equal(runSeekCheck({makeFixture:stable,times}).ok,true);
  assert.equal(runSeekCheck({makeFixture:bad,times}).ok,false);
  assert.throws(()=>runSeekCheck({makeFixture:stable,times:[0,1]}),/times/);
  assert.throws(()=>runSeekCheck({times}),/makeFixture/);
});

test("three independent instances see each time exactly once and catch cold reverse", async () => {
 const {runSeekCheck} = await import(url);
 const instances=[];
 const makeFixture=()=>{let first=null,t=0; const calls=[]; instances.push(calls); return {
   timeline:{totalTime(x){calls.push(x);t=x;if(first===null) first=x;}},
   probes:{value:()=>String(t===.5 && first===1 ? 999 : t)}
 };};
 const result=runSeekCheck({makeFixture,times:[0,.25,.5,.75,1]});
 assert.equal(instances.length,3);
 for(const calls of instances) { assert.equal(calls.length,5); assert.deepEqual([...calls].sort((a,b)=>a-b),[0,.25,.5,.75,1]); }
 assert.equal(result.ok,false);
 assert.ok(result.results.value.mismatches.some(m=>m.order==='reverse' && m.t===.5));
});
