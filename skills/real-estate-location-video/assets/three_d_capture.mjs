// Hiệu ứng «vệ tinh -> nhà 3D mọc lên -> kiểu Map»: MapLibre + OpenFreeMap (nhà 3D OSM) + Esri vệ tinh, quay từng khung.
// Dùng: node three_d_capture.mjs outDir [seconds=5] [fps=30] [lat lon zGoogle pitch bearing0 bearing1]
import { chromePath, loadPuppeteer, LAUNCH_ARGS } from "./_paths.mjs";
import fs from "node:fs";
import path from "node:path";
const puppeteer = loadPuppeteer();
const [OUT, SECS = "5", FPS = "30", LAT = "20.95374525", LON = "105.93237025", Z = "17", PITCH = "55", B0 = "40", B1 = "85"] = process.argv.slice(2);
fs.mkdirSync(OUT, { recursive: true });
const N = Math.round(+SECS * +FPS);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const browser = await puppeteer.launch({
  executablePath: chromePath(),
  headless: "new", defaultViewport: { width: 1080, height: 1920, deviceScaleFactor: 1 },
  args: LAUNCH_ARGS,
});
const page = await browser.newPage();
await page.setContent(`<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<style>html,body,#m{margin:0;width:1080px;height:1920px;overflow:hidden}.maplibregl-ctrl-bottom-right,.maplibregl-ctrl-bottom-left{display:none}</style>
</head><body><div id="m"></div></body></html>`);
await page.waitForFunction("window.maplibregl");
await page.evaluate((lat, lon, z, pitch, b0) => new Promise(res => {
  window.map = new maplibregl.Map({ container: "m", style: "https://tiles.openfreemap.org/styles/liberty", center: [+lon, +lat], zoom: +z - 1, pitch: +pitch, bearing: +b0,
    interactive: false, attributionControl: false, fadeDuration: 0, canvasContextAttributes: { preserveDrawingBuffer: true } });
  const map = window.map;
  map.on("load", () => {
    map.getStyle().layers.forEach(l => { if (l.type === "symbol") map.setLayoutProperty(l.id, "visibility", "none"); });
    map.addSource("esri", { type: "raster", tiles: ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"], tileSize: 256, maxzoom: 19 });
    map.addLayer({ id: "esri", type: "raster", source: "esri", paint: { "raster-opacity": 1, "raster-fade-duration": 0 } }, "building");
    map.setPaintProperty("building-3d", "fill-extrusion-color", ["interpolate", ["linear"], ["coalesce", ["get", "render_height"], 6],
      0, "#e8ecf1", 30, "#cfe3f7", 60, "#8fd3ff", 100, "#4fc3ff", 140, "#ffd34d"]);
    map.setPaintProperty("building-3d", "fill-extrusion-opacity", 0.96);
    res(true);
  });
}), LAT, LON, Z, PITCH, B0);
const ease = t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
const out3 = t => 1 - Math.pow(1 - Math.min(1, Math.max(0, t)), 3);
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
async function setT(sec) {
  const u = sec / +SECS;
  const K = out3((sec - 0.7) / 1.6);                 // nhà mọc 0,7–2,3 s
  const op = 1 - clamp((sec - 2.7) / 1.3, 0, 1);     // vệ tinh mờ 2,7–4,0 s
  const bearing = +B0 + (+B1 - +B0) * ease(u);
  const zoom = +Z - 1 + 0.35 * ease(u);
  await page.evaluate((K, op, bearing, zoom) => new Promise(res => {
    const map = window.map;
    map.jumpTo({ bearing, zoom });
    map.setPaintProperty("esri", "raster-opacity", op);
    map.setPaintProperty("building-3d", "fill-extrusion-height", ["*", ["coalesce", ["get", "render_height"], 6], K]);
    map.setPaintProperty("building", "fill-opacity", K > 0.02 ? 0 : 1);
    let done = false; const fin = () => { if (!done) { done = true; res(true); } };
    map.once("idle", fin); map.triggerRepaint(); setTimeout(fin, 2500);
  }), K, op, bearing, zoom);
}
// làm nóng ô bản đồ dọc đường camera
for (const s of [0, 1.5, 3, 4.5, +SECS]) { await setT(s); await sleep(1200); }
for (let f = 0; f < N; f++) {
  await setT(f / +FPS);
  await page.screenshot({ path: path.join(OUT, `f${String(f).padStart(4, "0")}.png`) });
  if (f % 30 === 0) console.log("frame", f, "/", N);
}
await browser.close();
console.log("done", N);
