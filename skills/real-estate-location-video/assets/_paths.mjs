// Tìm Chrome và puppeteer-core không gắn đường dẫn cứng (Windows và macOS).
//   CHROME_BIN            đường tới chrome(.exe); không có thì tìm trong ~/.cache/puppeteer (HyperFrames cài sẵn)
//   PUPPETEER_CORE_DIR    thư mục puppeteer-core; không có thì tìm trong cache npx / thử `require`
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { createRequire } from "node:module";

function firstExisting(list) { return list.find(p => p && fs.existsSync(p)); }
function listDirs(dir) { try { return fs.readdirSync(dir).map(n => path.join(dir, n)); } catch { return []; } }

export function chromePath() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  const root = path.join(os.homedir(), ".cache", "puppeteer", "chrome");
  const cands = [];
  for (const v of listDirs(root).sort().reverse()) {
    cands.push(path.join(v, "chrome-win64", "chrome.exe"), path.join(v, "chrome-linux64", "chrome"),
      path.join(v, "chrome-mac-arm64", "Google Chrome for Testing.app", "Contents", "MacOS", "Google Chrome for Testing"),
      path.join(v, "chrome-mac-x64", "Google Chrome for Testing.app", "Contents", "MacOS", "Google Chrome for Testing"));
  }
  const found = firstExisting(cands);
  if (!found) throw new Error("Không tìm thấy Chrome: đặt CHROME_BIN hoặc chạy `video-studio doctor` để cài Chromium của HyperFrames");
  return found;
}

export function loadPuppeteer() {
  const dirs = [];
  if (process.env.PUPPETEER_CORE_DIR) dirs.push(process.env.PUPPETEER_CORE_DIR);
  const npx = [process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, "npm-cache", "_npx"), path.join(os.homedir(), ".npm", "_npx")];
  for (const n of npx) for (const d of listDirs(n)) dirs.push(path.join(d, "node_modules", "puppeteer-core"));
  const dir = firstExisting(dirs.map(d => d && path.join(d, "package.json")));
  const req = createRequire(import.meta.url);
  if (dir) return req(path.dirname(dir));
  try { return req("puppeteer-core"); } catch { /* chưa cài */ }
  throw new Error("Không tìm thấy puppeteer-core: đặt PUPPETEER_CORE_DIR hoặc `npm i puppeteer-core` ở thư mục chạy");
}

export const LAUNCH_ARGS = ["--no-sandbox", "--enable-webgl", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader", "--hide-scrollbars"];
