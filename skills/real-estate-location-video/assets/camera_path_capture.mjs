// Quay MỘT chuyển động camera MƯỢT (zoom liền mạch, orbit, nghiêng, nhà 3D mọc) bằng MapLibre + Esri + OpenFreeMap, TỪNG KHUNG.
//   node camera_path_capture.mjs spec.json        (ra <out>/f0000.png … rồi ghép: ffmpeg -framerate 30 -i f%04d.png -c:v libx264 -crf 17 -pix_fmt yuv420p -g 15 clip.mp4)
// spec: {"out":"dir","secs":5,"fps":30,"buildings":false,
//        "keys":[{"t":0,"lat":..,"lon":..,"z":5,"pitch":0,"bearing":0,"rise":1,"sat":1}, {"t":5,...}]}
//   z = zoom ô 256 px (MapLibre dùng z-1, script tự trừ). rise (0..1) = độ cao nhà 3D; sat (0..1) = độ đậm ảnh vệ tinh (kiểu «vệ tinh → khối 3D»).
// Vì sao không dùng Google Earth cho zoom: Earth web quay ra chỉ ~6 khung/giây thật (đo: 19 khung khác nhau trong 90) nên zoom giật;
// ở đây mỗi khung được dựng xong rồi mới chụp (tất định) nên chuyển động đều. Earth chỉ dùng cho ảnh tĩnh nghiêng điện ảnh.
// Zoom vào theo kiểu «điểm đích đi đều trên màn hình»: tâm nội suy theo tham số s = (2^-z - 2^-z0)/(2^-z1 - 2^-z0).
import { chromePath, loadPuppeteer, LAUNCH_ARGS } from "./_paths.mjs";
import fs from "node:fs";
import path from "node:path";
const puppeteer = loadPuppeteer();
const spec = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const FPS = spec.fps || 30, SECS = spec.secs, N = Math.round(SECS * FPS);
fs.mkdirSync(spec.out, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const k0 = spec.keys[0];
const browser = await puppeteer.launch({ executablePath: chromePath(), headless: "new", defaultViewport: { width: 1080, height: 1920, deviceScaleFactor: 1 }, args: LAUNCH_ARGS });
const page = await browser.newPage();
await page.setContent(`<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<style>html,body,#m{margin:0;width:1080px;height:1920px;overflow:hidden}.maplibregl-ctrl-bottom-right,.maplibregl-ctrl-bottom-left{display:none}</style>
</head><body><div id="m"></div></body></html>`);
await page.waitForFunction("window.maplibregl");
await page.evaluate((k, b3d) => new Promise(res => {
  window.map = new maplibregl.Map({ container: "m", style: "https://tiles.openfreemap.org/styles/liberty", center: [k.lon, k.lat], zoom: k.z - 1, pitch: k.pitch || 0, bearing: k.bearing || 0,
    interactive: false, attributionControl: false, fadeDuration: 0, maxPitch: 75, canvasContextAttributes: { preserveDrawingBuffer: true } });
  const map = window.map;
  map.on("load", () => {
    map.getStyle().layers.forEach(l => { if (l.type === "symbol") map.setLayoutProperty(l.id, "visibility", "none"); });
    map.addSource("esri", { type: "raster", tiles: ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"], tileSize: 256, maxzoom: 19 });
    map.addLayer({ id: "esri", type: "raster", source: "esri", paint: { "raster-opacity": 1, "raster-fade-duration": 0 } }, "building");
    if (b3d) {
      map.setPaintProperty("building-3d", "fill-extrusion-color", ["interpolate", ["linear"], ["coalesce", ["get", "render_height"], 6],
        0, "#e8ecf1", 30, "#cfe3f7", 60, "#8fd3ff", 100, "#4fc3ff", 140, "#ffd34d"]);
      map.setPaintProperty("building-3d", "fill-extrusion-opacity", 0.96);
    } else {
      for (const id of ["building", "building-3d"]) if (map.getLayer(id)) map.setLayoutProperty(id, "visibility", "none");
    }
    res(true);
  });
}), k0, !!spec.buildings);
const ease = u => u * u * u * (u * (u * 6 - 15) + 10);   // smootherstep: vào/ra êm
const lerp = (a, b, u) => a + (b - a) * u;
function camAt(t) {
  const ks = spec.keys; let i = 0;
  while (i < ks.length - 2 && t > ks[i + 1].t) i++;
  const a = ks[i], b = ks[i + 1];
  const u = Math.min(1, Math.max(0, (t - a.t) / (b.t - a.t))), e = spec.linear ? u : ease(u);
  const z = lerp(a.z, b.z, e);
  const d = Math.pow(2, -b.z) - Math.pow(2, -a.z);
  const s = Math.abs(d) < 1e-12 ? e : (Math.pow(2, -z) - Math.pow(2, -a.z)) / d;
  return { lat: lerp(a.lat, b.lat, s), lon: lerp(a.lon, b.lon, s), zoom: z - 1, pitch: lerp(a.pitch || 0, b.pitch || 0, e),
    bearing: lerp(a.bearing || 0, b.bearing || 0, e), rise: lerp(a.rise ?? 1, b.rise ?? 1, e), sat: lerp(a.sat ?? 1, b.sat ?? 1, e) };
}
async function setT(t) {
  const c = camAt(t);
  await page.evaluate((c, b3d) => new Promise(res => {
    const map = window.map;
    map.jumpTo({ center: [c.lon, c.lat], zoom: c.zoom, pitch: c.pitch, bearing: c.bearing });
    map.setPaintProperty("esri", "raster-opacity", c.sat);
    if (b3d) {
      map.setPaintProperty("building-3d", "fill-extrusion-height", ["*", ["coalesce", ["get", "render_height"], 6], c.rise]);
      map.setPaintProperty("building", "fill-opacity", c.rise > 0.02 ? 0 : 1);
    }
    let done = false; const fin = () => { if (!done) { done = true; res(true); } };
    map.once("idle", fin); map.triggerRepaint(); setTimeout(fin, 3000);
  }), c, !!spec.buildings);
}
for (let s = 0; s <= SECS; s += 0.4) { await setT(s); await sleep(700); }   // làm nóng ô bản đồ dọc đường camera
for (let f = 0; f < N; f++) {
  await setT(f / FPS);
  await page.screenshot({ path: path.join(spec.out, `f${String(f).padStart(4, "0")}.png`) });
  if (f % 30 === 0) console.log(spec.out, "frame", f, "/", N);
}
await browser.close();
console.log("done", spec.out, N);
