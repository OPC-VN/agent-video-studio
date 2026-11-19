export const meta = {id: "VE-gsap-seededscramble", plugin: null, needs: ["gsap"]};
export function register() {}
export function build(tl, {target, text, chars="ABCDEFGHJKLMNPQRSTUVWXYZ0123456789", seed=1, at=0, duration=1, revealDelay=0.2}) {
  if (!Number.isInteger(seed)) throw new Error("seed");
  if (!text) return tl;
  const alphabet = Array.from(chars), letters = Array.from(text);
  if (!alphabet.length) throw new Error("chars");
  if (!(revealDelay >= 0 && revealDelay < 1)) throw new Error("revealDelay");
  let progress = 0;
  const state = {get progress() { return progress; }, set progress(value) {
    progress = value;
    const step = Math.floor(progress * 24), reveal = Math.max(0, Math.min(1, (progress-revealDelay)/(1-revealDelay)));
    target.textContent = letters.map((c,i) => {
      if (i < Math.floor(reveal * letters.length) || c === " ") return c;
      let x = (seed ^ Math.imul(i+1, 0x9e3779b1) ^ Math.imul(step+1, 0x85ebca6b)) >>> 0;
      x ^= x >>> 16; x = Math.imul(x, 0x7feb352d); x ^= x >>> 15;
      return alphabet[(x >>> 0) % alphabet.length];
    }).join("");
  }};
  return tl.fromTo(state, {progress:0}, {progress:1,duration,ease:"none"}, at);
}
