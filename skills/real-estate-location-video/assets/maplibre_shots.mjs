// Chụp shot MapLibre top-down: node maplibre_shots.mjs outDir  (dùng geo-capture.html; Esri vệ tinh + OpenFreeMap nhà 3D)
import { chromePath, loadPuppeteer, LAUNCH_ARGS } from "./_paths.mjs";
import path from "node:path"; import fs from "node:fs"; import url from "node:url";
const puppeteer = loadPuppeteer();
const sleep = ms => new Promise(r => setTimeout(r, ms));
const OUT = process.argv[2]; fs.mkdirSync(OUT, { recursive: true });
const here = path.dirname(url.fileURLToPath(import.meta.url));
const page_url = url.pathToFileURL(path.join(here, "geo-capture.html")).href;
const P = [20.95374525, 105.93237025];
// Danh sách shot: mặc định là ví dụ dưới; hoặc đưa tệp JSON làm đối số 3: [["N01", lat, lon, zoom256, mode?, pitch?, bearing?], ...]
// mode: esri | osm | esri3d | osm3d | mask-water (đa giác nước trắng trên nền đen, dùng để lấy viền hồ: xem water_outline.py)
const shots = process.argv[3] ? JSON.parse(fs.readFileSync(process.argv[3], "utf8")) : [
  ["M01", 20.62, 106.27, 10.8], ["M02", 20.95655, 105.93502, 14.5], ["M03", 20.9738, 105.9530, 14.4],
  ["M04", P[0], P[1], 15.6], ["M05", 20.9596, 105.9322, 16.8], ["M06", 20.9732, 105.9381, 14.0],
  ["M07", P[0], P[1], 16.5, "esri3d", 55, 40],
];
const browser = await puppeteer.launch({ executablePath: chromePath(),
  headless: "new", defaultViewport: { width: 1080, height: 1920, deviceScaleFactor: 1 }, args: LAUNCH_ARGS });
const page = await browser.newPage();
for (const [id, lat, lon, z, mode = "esri", pitch = 0, b = 0] of shots) {
  await page.goto(`${page_url}?lat=${lat}&lon=${lon}&z=${z}&mode=${mode}&pitch=${pitch}&b=${b}`, { waitUntil: "domcontentloaded" });
  await page.waitForFunction("window.__ready === true", { timeout: 60000 }).catch(() => {});
  await sleep(1500);
  const err = await page.evaluate(() => (window.__err || []).slice(0, 2));
  await page.screenshot({ path: path.join(OUT, id + ".png") });
  console.log(JSON.stringify({ id, lat, lon, z, mode, errs: err }));
}
await browser.close();
