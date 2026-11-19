// Check each visible probe at the same times in three different seek orders.
export function runSeekCheck({ makeFixture, times, seed = 1 }) {
  if (typeof makeFixture !== "function") throw new Error("makeFixture");
  if (!Array.isArray(times) || times.length < 5 || times[0] !== 0 ||
      times.some((t, i) => !Number.isFinite(t) || (i && t <= times[i - 1]))) throw new Error('times');
  const shuffled = [...times];
  let state = seed >>> 0;
  for (let i = shuffled.length - 1; i > 0; i--) {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    const j = state % (i + 1);
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  let names = null;
  const results = {};
  const baseline = {};
  for (const [order, sequence] of [['forward', times], ['reverse', [...times].reverse()], ['shuffled', shuffled]]) {
    const { timeline, probes } = makeFixture();
    const fixtureNames = Object.keys(probes).sort();
    if (!fixtureNames.length) throw new Error("probes");
    if (names === null) {
      names = fixtureNames;
      for (const name of names) results[name] = {ok: true, mismatches: []};
    } else if (JSON.stringify(names) !== JSON.stringify(fixtureNames)) throw new Error("probes");
    for (const t of sequence) {
      timeline.totalTime(t, true);
      for (const name of names) {
        const value = probes[name]();
        if (typeof value !== 'string') throw new Error('probe');
        const key = `${name}\u0000${t}`;
        if (order === 'forward') baseline[key] = value;
        else if (baseline[key] !== value) {
          results[name].ok = false;
          results[name].mismatches.push({t, order, a: baseline[key], b: value});
        }
      }
    }
  }
  return {ok: names.every(name => results[name].ok), results};
}
