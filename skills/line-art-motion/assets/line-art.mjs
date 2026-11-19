// Clean-room: viết từ mô tả toán trong PLAN SPR-18; không sao chép mã nguồn ngoài.
const finite = (...v) => { if (v.some(x => !Number.isFinite(x))) throw new RangeError('finite number required'); };
const time = t => { finite(t); return Math.max(0, t); };
const unit = x => Math.max(0, Math.min(1, x));
export function hash01(seed, ...keys) {
  if (![seed, ...keys].every(Number.isSafeInteger)) throw new TypeError('integer required');
  let h = seed >>> 0;
  for (const k of keys) { h = Math.imul(h ^ (k >>> 0), 0x9e3779b1); h ^= h >>> 16; }
  h = Math.imul(h ^ (h >>> 16), 0x7feb352d); h = Math.imul(h ^ (h >>> 15), 0x846ca68b);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
export function mulberry(seed) {
  if (!Number.isSafeInteger(seed)) throw new TypeError('integer required');
  let state = seed >>> 0;
  return () => { state = (state + 0x6d2b79f5) >>> 0; let z = state; z = Math.imul(z ^ (z >>> 15), z | 1); z ^= z + Math.imul(z ^ (z >>> 7), z | 61); return ((z ^ (z >>> 14)) >>> 0) / 4294967296; };
}
export function spring({stiffness, damping, mass = 1, from = 0, to = 1, v0 = 0}) {
  finite(stiffness, damping, mass, from, to, v0);
  if (stiffness <= 0 || mass <= 0 || damping < 0) throw new RangeError('invalid spring');
  const w = Math.sqrt(stiffness / mass), z = damping / (2 * Math.sqrt(stiffness * mass)), a = from - to;
  if (!Number.isFinite(w) || !Number.isFinite(z) || !Number.isFinite(z*z) || !Number.isFinite(a)) throw new RangeError('spring coefficients out of range');
  return t => { t = time(t); if (z < 1 - 1e-9) { const d = w * Math.sqrt(1-z*z); return to + Math.exp(-z*w*t)*(a*Math.cos(d*t)+(v0+z*w*a)/d*Math.sin(d*t)); }
    if (Math.abs(z-1)<1e-9) { const e = Math.exp(-w*t); return e === 0 ? to : to + e*(a+(v0+w*a)*t); }
    const q = Math.sqrt(z*z-1), r1 = -w/(z+q), r2 = -w*(z+q), c1 = (v0-r2*a)/(r1-r2); return to+c1*Math.exp(r1*t)+(a-c1)*Math.exp(r2*t); };
}
export const SMALL_ANGLE = 0.35;
export function pendulum({length, gravity, theta0, omega0 = 0, damping}) {
  finite(length, gravity, theta0, omega0, damping);
  if (length <= 0 || gravity <= 0 || damping < 0) throw new RangeError('invalid pendulum');
  if (Math.abs(theta0) > SMALL_ANGLE) throw new RangeError('dùng bakePendulum');
  return spring({stiffness: gravity / length, damping, from: theta0, to: 0, v0: omega0});
}
export function bakePendulum({length, gravity, theta0, omega0 = 0, damping, duration, dt = 1/240}) {
  finite(length, gravity, theta0, omega0, damping, duration, dt);
  if (length <= 0 || gravity <= 0 || damping < 0 || duration <= 0 || dt <= 0 || duration/dt > 1e6) throw new RangeError('invalid bake');
  const n = Math.ceil(duration/dt), step = duration/n, samples = [theta0]; let a = theta0, v = omega0;
  const acc = (x,y) => -gravity/length*Math.sin(x)-damping*y;
  for (let i=0;i<n;i++) { const k1a=v,k1v=acc(a,v), k2a=v+step*k1v/2,k2v=acc(a+step*k1a/2,v+step*k1v/2), k3a=v+step*k2v/2,k3v=acc(a+step*k2a/2,v+step*k2v/2), k4a=v+step*k3v,k4v=acc(a+step*k3a,v+step*k3v); a+=step*(k1a+2*k2a+2*k3a+k4a)/6; v+=step*(k1v+2*k2v+2*k3v+k4v)/6; samples.push(a); }
  return t => { const x = Math.min(duration,time(t))/step, i = Math.floor(x); return i >= n ? samples[n] : samples[i]+(samples[i+1]-samples[i])*(x-i); };
}
export function wind({seed, strength, period}) { finite(strength,period); if (period <= 0) throw new RangeError('invalid period'); const phase=[0,1,2].map(i=>hash01(seed,i)*2*Math.PI), freq=[0,1,2].map(i=>0.7+hash01(seed,i,1)); return t => { t=time(t); return strength*phase.reduce((s,p,i)=>s+Math.sin(p+2*Math.PI*freq[i]*t/period)/3,0); }; }
export function solveTwoBone(hip, target, l1, l2, bend = 1) {
  finite(hip.x,hip.y,target.x,target.y,l1,l2,bend); if(l1<=0||l2<=0||Math.abs(bend)!==1) throw new RangeError('invalid limb');
  const dx=target.x-hip.x,dy=target.y-hip.y,raw=Math.hypot(dx,dy), lo=Math.abs(l1-l2)+1e-6,hi=l1+l2-1e-6, d=Math.max(lo,Math.min(hi,raw)), ux=raw?dx/raw:1,uy=raw?dy/raw:0, along=(l1*l1-l2*l2+d*d)/(2*d), side=Math.sqrt(Math.max(0,l1*l1-along*along))*bend;
  return {knee:{x:hip.x+along*ux-side*uy,y:hip.y+along*uy+side*ux},reached:raw>=lo&&raw<=hi};
}
export function gait(kind='walk', overrides={}) {
  const presets={walk:{period:1.1,duty:.6,stride:26,lift:3,hipRatio:.96},shuffle:{period:.9,duty:.7,stride:12,lift:1,hipRatio:.97},run:{period:.55,duty:.35,stride:36,lift:7,hipRatio:.9}};
  if(!Object.hasOwn(presets,kind)) throw new RangeError('unknown gait'); const base={...presets[kind],ground:120,l1:32,l2:32,bob:0}; for(const key of Object.keys(overrides)) if(!Object.hasOwn(base,key)) throw new TypeError('unknown parameter'); const p={...base,...overrides}; finite(...Object.values(p)); if(p.period<=0||p.duty<=0||p.duty>=1||p.l1<=0||p.l2<=0||p.stride<0||p.stride>=2*(p.l1+p.l2-0.01)||p.lift<0||p.hipRatio<0||p.hipRatio>1||(Math.abs(p.bob)>p.hipRatio*(p.l1+p.l2)||2*Math.abs(p.bob)>Math.sqrt(Math.max(0,(p.l1+p.l2-0.01)**2-(p.stride/2)**2)))||!Number.isFinite(p.stride/(p.duty*p.period))) throw new RangeError('invalid gait');
  return {params:p,groundSpeed:p.stride/(p.duty*p.period),pose(phase){ finite(phase); const ph=((phase%1)+1)%1, hip={x:0,y:p.ground-Math.min(p.hipRatio*(p.l1+p.l2), Math.sqrt(Math.max(0,(p.l1+p.l2-0.01)**2-(p.stride/2)**2))-Math.abs(p.bob))+p.bob*Math.cos(4*Math.PI*ph)}, spine={x:0,y:hip.y-34},head={x:0,y:hip.y-43}; const legs=[0,.5].map(off=>{ const q=(ph+off)%1,u=q<p.duty?0:(q-p.duty)/(1-p.duty), x=q<p.duty?p.stride/2-p.stride*q/p.duty:-p.stride/2+p.stride*(u*u*(3-2*u)-(1-p.duty)/p.duty*(u*u*u-2*u*u+u+u*u*u-u*u)), target={x,y:p.ground-(q<p.duty?0:p.lift*Math.sin(Math.PI*u)**2)}, ik=solveTwoBone(hip,target,p.l1,p.l2,1); const d=Math.hypot(target.x-hip.x,target.y-hip.y), reach=Math.max(Math.abs(p.l1-p.l2)+1e-6,Math.min(d,p.l1+p.l2-1e-6)), ankle={x:hip.x+(d?(target.x-hip.x)/d:1)*reach,y:hip.y+(d?(target.y-hip.y)/d:0)*reach}; return {knee:ik.knee,ankle,toe:{x:ankle.x+8*Math.cos(q<p.duty?0:.32*Math.sin(2*Math.PI*u)),y:ankle.y-(q<p.duty?0:3*Math.sin(Math.PI*u)**2)},reached:ik.reached}; }); const arms=[0,.5].map(off=>{const a=Math.sin(2*Math.PI*(ph+off));return {elbow:{x:-8*a,y:spine.y+13},hand:{x:-15*a,y:spine.y+26}};}); return {hip,spine,head,legs,arms}; }};
}
export function limbPath(a,b,c,width,gap) { finite(a.x,a.y,b.x,b.y,c.x,c.y,width,gap); const dx=c.x-a.x,dy=c.y-a.y,n=Math.hypot(dx,dy)||1, x=-dy/n*gap/2,y=dx/n*gap/2; return `M ${a.x+x} ${a.y+y} L ${b.x+x} ${b.y+y} L ${c.x+x} ${c.y+y} M ${a.x-x} ${a.y-y} L ${b.x-x} ${b.y-y} L ${c.x-x} ${c.y-y}`; }
const hiddenDraws = new WeakMap();
export function drawOn(el,p){
  finite(p); if(!el||typeof el.setAttribute!=='function'||!el.style) throw new TypeError('element required');
  const style=el.style, css=typeof style.getPropertyValue==='function', value=()=>css?style.getPropertyValue('visibility'):(style.visibility||''), priority=()=>css?style.getPropertyPriority('visibility'):'', owned=()=>value()==='hidden'&&(!css||priority()==='important');
  el.setAttribute('pathLength','1'); style.strokeDasharray='1'; style.strokeDashoffset=String(1-unit(p));
  if(p<=0){
    if(!hiddenDraws.has(el)||!owned()) hiddenDraws.set(el,{value:value(),priority:priority()});
    if(css)style.setProperty('visibility','hidden','important');else style.visibility='hidden';
  }else if(hiddenDraws.has(el)){
    const previous=hiddenDraws.get(el); hiddenDraws.delete(el);
    if(owned()){if(css){if(previous.value)style.setProperty('visibility',previous.value,previous.priority);else style.removeProperty('visibility');}else if(previous.value)style.visibility=previous.value;else delete style.visibility;}
  }
}
export function inkFilter(id,{scale=.45,blur=.12,baseFrequency=.04,seed=3,octaves=2}={}) { if(!/^[A-Za-z][A-Za-z0-9_-]*$/.test(id)||!Number.isInteger(seed)||!Number.isInteger(octaves)) throw new TypeError('invalid filter'); finite(scale,blur,baseFrequency); if(blur<0||baseFrequency<=0||octaves<1) throw new RangeError('invalid filter'); return `<filter id="${id}" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="${baseFrequency}" numOctaves="${octaves}" seed="${seed}" result="noise"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="${scale}"/><feGaussianBlur stdDeviation="${blur}"/></filter>`; }
export const PALETTE_KEYS=[{tau:0,bg:'#182333',ink:'#d3d5cf',paper:'#344052',lamp:'#ffd58a'},{tau:.16,bg:'#8c9fa2',ink:'#34404a',paper:'#d5d5be',lamp:'#f4d69b'},{tau:.3,bg:'#dce2d5',ink:'#303c41',paper:'#f5efda',lamp:'#f4e5b9'},{tau:.55,bg:'#e6ddca',ink:'#383932',paper:'#f8eed9',lamp:'#f6e7ba'},{tau:.72,bg:'#d19d7f',ink:'#493e43',paper:'#e9c9aa',lamp:'#ffe0a2'},{tau:.86,bg:'#485367',ink:'#e2d5bb',paper:'#777887',lamp:'#ffca76'}];
export function palette(tau){ finite(tau); const t=((tau%1)+1)%1; let i=PALETTE_KEYS.length-1; for(let j=0;j<PALETTE_KEYS.length;j++) if(PALETTE_KEYS[j].tau<=t) i=j; const a=PALETTE_KEYS[i],b=PALETTE_KEYS[(i+1)%PALETTE_KEYS.length], end=i===PALETTE_KEYS.length-1?1:b.tau, q=(t-a.tau)/(end-a.tau); return Object.fromEntries(['bg','ink','paper','lamp'].map(k=>[k,'#'+[1,3,5].map(n=>Math.round(parseInt(a[k].slice(n,n+2),16)*(1-q)+parseInt(b[k].slice(n,n+2),16)*q).toString(16).padStart(2,'0')).join('')])); }
