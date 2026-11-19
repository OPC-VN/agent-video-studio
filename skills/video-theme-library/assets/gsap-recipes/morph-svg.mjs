export const meta = {id: "VE-gsap-morphsvg", plugin: "MorphSVGPlugin", needs: ["gsap-morphsvg"]};
export function register(gsap, libs) { gsap.registerPlugin(libs.MorphSVGPlugin); }
export function build(tl, {target, shape, shapeIndex="auto", at=0, duration=1, ease="power2.inOut"}) {
  return tl.to(target, {morphSVG: {shape, shapeIndex}, duration, ease}, at);
}
