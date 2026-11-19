// Lấy ranh hành chính (admin_level 4, 6) và đường chính từ OpenFreeMap theo khung nhìn MapLibre. Ra JSON toạ độ lon/lat.
// Dùng: node extract_osm.mjs out.json
import { chromePath, loadPuppeteer, LAUNCH_ARGS } from "./_paths.mjs";
import fs from "node:fs";
const puppeteer = loadPuppeteer();
const sleep = ms => new Promise(r => setTimeout(r, ms));
const VIEWS = {
  M01: { c: [106.27, 20.62], z: 10.8 - 1, want: ["b4"] },
  M02: { c: [105.93502, 20.95655], z: 14.5 - 1, want: ["b6", "b4"] },
  M03: { c: [105.9530, 20.9738], z: 14.4 - 1, want: ["b6"] },
  M04: { c: [105.93237025, 20.95374525], z: 15.6 - 1, want: ["roads", "b6"] },
};
const browser = await puppeteer.launch({ executablePath: chromePath(), headless: "new", defaultViewport: { width: 1080, height: 1920, deviceScaleFactor: 1 }, args: LAUNCH_ARGS });
const page = await browser.newPage();
await page.setContent(`<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"><script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script><div id="m" style="width:1080px;height:1920px"></div>`);
await page.waitForFunction("window.maplibregl");
await page.evaluate(() => new Promise(res => { window.map = new maplibregl.Map({ container: "m", style: "https://tiles.openfreemap.org/styles/liberty", center: [106.27, 20.62], zoom: 9.8, interactive: false, attributionControl: false, fadeDuration: 0 }); map.on("load", () => res(true)); }));
const result = {};
for (const [id, v] of Object.entries(VIEWS)) {
  await page.evaluate((c, z) => new Promise(res => { map.jumpTo({ center: c, zoom: z }); map.once("idle", () => res(true)); setTimeout(() => res(true), 8000); }), v.c, v.z);
  await sleep(1500);
  result[id] = await page.evaluate(() => {
    const src = "openmaptiles";
    const lines = f => { const g = f.geometry; return g.type === "LineString" ? [g.coordinates] : g.type === "MultiLineString" ? g.coordinates : []; };
    const bnd = lvl => map.querySourceFeatures(src, { sourceLayer: "boundary", filter: ["all", ["==", ["get", "admin_level"], lvl], ["!=", ["get", "maritime"], 1]] }).flatMap(lines);
    const roads = map.querySourceFeatures(src, { sourceLayer: "transportation", filter: ["in", ["get", "class"], ["literal", ["motorway", "trunk", "primary", "secondary", "tertiary"]]] })
      .map(f => ({ cls: f.properties.class, name: f.properties["name:vi"] || f.properties.name || "", lines: lines(f) })).filter(r => r.lines.length);
    return { b4: bnd(4), b6: bnd(6), roads };
  });
  const r = result[id];
  console.log(id, "b4:", r.b4.length, "b6:", r.b6.length, "roads:", r.roads.length);
}
fs.writeFileSync(process.argv[2], JSON.stringify(result));
await browser.close();
