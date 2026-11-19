export const meta = {id: "VE-gsap-flip", plugin: "Flip", needs: ["gsap-flip"]};
export function register(gsap, libs) { gsap.registerPlugin(libs.Flip); }
export function build(tl, {Flip, targets, change, at=0, duration=0.8, ease="power2.inOut", absolute=false}) {
  if (typeof change !== "function") throw new Error("change");
  const state = Flip.getState(targets); change();
  const animation = Flip.from(state, {duration,ease,absolute,paused:true});
  tl.add(animation, at);
  animation.paused(false);
  return tl;
}
