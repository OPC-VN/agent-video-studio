export const meta = {id: "VE-gsap-drawsvg", plugin: "DrawSVGPlugin", needs: ["gsap-drawsvg"]};
export function register(gsap, libs) { gsap.registerPlugin(libs.DrawSVGPlugin); }
export function build(tl, {targets, at=0, duration=1, from="0% 0%", to="0% 100%", ease="power2.out"}) {
  return tl.fromTo(targets, {drawSVG: from}, {drawSVG: to, duration, ease}, at);
}
