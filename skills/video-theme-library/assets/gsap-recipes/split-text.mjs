export const meta = {id: "VE-gsap-splittext", plugin: "SplitText", needs: ["gsap-splittext"]};
export function register(gsap, libs) { gsap.registerPlugin(libs.SplitText); }
export function prepare(SplitText, el, {type="chars,words,lines"}={}) { return SplitText.create(el, {type}); }
export function build(tl, {split, part="chars", from={opacity:0,y:24}, at=0, duration=0.6, stagger=0.04, ease="power3.out"}) {
  if (!Array.isArray(split[part])) throw new Error("part");
  return tl.fromTo(split[part], from, {opacity:1,y:0,duration,stagger,ease}, at);
}
