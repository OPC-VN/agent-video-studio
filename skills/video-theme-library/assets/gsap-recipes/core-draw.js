/* Draw a normalized SVG path using GSAP core; caller owns the paused timeline. */
function addCoreDraw(timeline, target, options = {}) {
  const { at = 0, duration = 1, ease = "none" } = options;
  if (!target || target.getAttribute("pathLength") !== "1") {
    throw new Error("target must have pathLength=1");
  }
  timeline.fromTo(target,
    { strokeDasharray: "1 1", strokeDashoffset: 1 },
    { strokeDasharray: "1 1", strokeDashoffset: 0, duration, ease, autoRound: false }, at);
  return timeline;
}
if (typeof window !== "undefined") window.addCoreDraw = addCoreDraw;
if (typeof module !== "undefined") module.exports = { addCoreDraw };
