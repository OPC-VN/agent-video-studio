export const meta = {id: "VE-gsap-motionpath", plugin: "MotionPathPlugin", needs: ["gsap-motionpath"]};
export function register(gsap, libs) { gsap.registerPlugin(libs.MotionPathPlugin); }
export function build(tl, {target, path, at=0, duration=2, align=path, alignOrigin=[0.5,0.5], autoRotate=false, start=0, end=1, ease="none"}) {
  return tl.fromTo(target, {motionPath: {path, align, alignOrigin, autoRotate, start, end: start}}, {motionPath: {path, align, alignOrigin, autoRotate, start, end}, duration, ease}, at);
}
