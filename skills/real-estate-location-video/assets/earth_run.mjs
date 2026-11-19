// Quay Google Earth web hàng loạt: shot tĩnh + chuyển động liên tục (screencast), khung dọc 1080x1920.
// Dùng: node earth_run.mjs job.json
// job = { out, basemap: {type:"satellite"|"map", details:"clean"|"exploration"|"everything"}, shots:[{id, url, wait, kind:"still"|"move", steps:[...]}] }
// steps: {wait:ms} | {wheel:deltaY, n, gap} | {drag:[dx,dy], n, gap, button:"left"|"right"} | {key, hold}
// Toạ độ UI (khung 1080x2150, cắt 90 px trên): tip1 Dismiss (637,183); tip2 Dismiss (45,148); ô nền góc dưới-trái (47,2073);
// trong Basemap settings: Satellite (100,800) Map (100,863) · Clean (288,984) Exploration (288,1064) Everything (288,1144) · đóng X (296,720).
import { chromePath, loadPuppeteer, LAUNCH_ARGS } from "./_paths.mjs";
import fs from "node:fs";
import path from "node:path";
const puppeteer = loadPuppeteer();
const job = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const W = 1080, H = 2150, CLIP = { x: 0, y: 90, width: 1080, height: 1920 };
fs.mkdirSync(job.out, { recursive: true });
const browser = await puppeteer.launch({
  executablePath: chromePath(),
  headless: "new", defaultViewport: { width: W, height: H, deviceScaleFactor: 1 },
  args: LAUNCH_ARGS,
});
const page = await browser.newPage();
const first = job.shots[0];
await page.goto(first.url, { waitUntil: "domcontentloaded", timeout: 90000 });
await sleep(18000);
await page.keyboard.press("Escape"); await sleep(500);
await page.mouse.click(637, 183); await sleep(700);
await page.mouse.click(45, 148); await sleep(700);
// nền
const bm = job.basemap ?? {};
if (bm.type || bm.details) {
  await page.mouse.click(47, 2073); await sleep(3500);
  if (bm.type === "map") { await page.mouse.click(100, 863); await sleep(2500); }
  if (bm.type === "satellite") { await page.mouse.click(100, 800); await sleep(2500); }
  const dy = { clean: 984, exploration: 1064, everything: 1144 }[bm.details];
  if (dy) { await page.mouse.click(288, dy); await sleep(1500); }
  await page.mouse.click(296, 720); await sleep(1500);   // đóng bảng
}
async function doSteps(steps) {
  for (const s of steps ?? []) {
    if (s.wheel) { await page.mouse.move(W / 2, 1100); for (let i = 0; i < s.n; i++) { await page.mouse.wheel({ deltaY: s.wheel }); await sleep(s.gap ?? 90); } }
    else if (s.drag) {
      const [dx, dy] = s.drag; await page.mouse.move(W / 2, 1100);
      await page.mouse.down({ button: s.button ?? "left" });
      for (let i = 1; i <= s.n; i++) { await page.mouse.move(W / 2 + dx * i / s.n, 1100 + dy * i / s.n); await sleep(s.gap ?? 30); }
      await page.mouse.up({ button: s.button ?? "left" });
    } else if (s.key) { await page.keyboard.down(s.key); await sleep(s.hold); await page.keyboard.up(s.key); }
    else if (s.wait) await sleep(s.wait);
  }
}
for (const s of job.shots) {
  const t0 = Date.now();
  await page.goto(s.url, { waitUntil: "domcontentloaded", timeout: 90000 }); // tải lại URL: kiểm cài đặt nền có còn không
  await sleep(s.wait ?? 16000);
  await page.keyboard.press("Escape"); await sleep(400);
  await page.mouse.move(W / 2, 1100);
  if (s.kind === "move") {
    const file = path.join(job.out, `${s.id}.mp4`);
    const rec = await page.screencast({ path: file, crop: CLIP, speed: 1 });
    await sleep(400); await doSteps(s.steps); await sleep(600); await rec.stop();
    console.log(JSON.stringify({ id: s.id, kind: "move", file, ms: Date.now() - t0, url: page.url().slice(0, 120) }));
  } else {
    const file = path.join(job.out, `${s.id}.png`);
    await page.screenshot({ path: file, clip: CLIP });
    console.log(JSON.stringify({ id: s.id, kind: "still", file, ms: Date.now() - t0, url: page.url().slice(0, 120) }));
  }
}
await browser.close();
