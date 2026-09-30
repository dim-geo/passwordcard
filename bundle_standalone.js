#!/usr/bin/env node
import * as fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function generateStandalone() {
  const assetDirs = [
    path.join(__dirname, "docs", "assets"),
    path.join(__dirname, "dist", "assets")
  ];

  let assetsDir = null;
  for (const d of assetDirs) {
    try {
      const stat = await fs.stat(d);
      if (stat.isDirectory()) {
        assetsDir = d;
        break;
      }
    } catch {}
  }

  if (!assetsDir) {
    console.error("[!] Could not find docs/assets or dist/assets directory.");
    process.exit(1);
  }

  const files = await fs.readdir(assetsDir);
  const cssFile = files.find(f => f.endsWith(".css"));
  const jsFile = files.find(f => f.endsWith(".js"));

  if (!cssFile || !jsFile) {
    console.error("[!] Could not find compiled CSS or JS in " + assetsDir);
    process.exit(1);
  }

  const css = await fs.readFile(path.join(assetsDir, cssFile), "utf8");
  const js = await fs.readFile(path.join(assetsDir, jsFile), "utf8");

  let iconB64 = "";
  try {
    const iconBuf = await fs.readFile(path.join(__dirname, "icon.png"));
    iconB64 = iconBuf.toString("base64");
  } catch {}

  const iconTag = iconB64
    ? `<link rel="icon" type="image/png" href="data:image/png;base64,${iconB64}" />`
    : "";

  const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    ${iconTag}
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Password Card Generator</title>
    <style>
${css}
    </style>
  </head>
  <body>
    <div id="app"></div>
    <script>
${js}
    </script>
  </body>
</html>
`;

  const outputPath = path.join(__dirname, "standalone.html");
  await fs.writeFile(outputPath, html, "utf8");
  console.log(`[✓] Successfully generated: ${outputPath}`);
}

generateStandalone();
