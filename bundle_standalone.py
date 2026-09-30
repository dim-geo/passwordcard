#!/usr/bin/env python3
"""
bundle_standalone.py

Converts the project's index.html and compiled assets into a 100% self-contained,
offline standalone.html file that can be opened directly via file:// in any browser
without requiring any web server, Python, or Node.js runtime.
"""

import sys
import os
import glob
import base64
from pathlib import Path

def generate_standalone(project_dir: Path, output_file: Path):
    print(f"[*] Packaging standalone HTML in: {project_dir}")

    # 1. Locate assets in docs/assets or dist/assets
    asset_dirs = [project_dir / "docs" / "assets", project_dir / "dist" / "assets"]
    assets_dir = None
    for d in asset_dirs:
        if d.is_dir():
            assets_dir = d
            break

    if not assets_dir:
        print("[!] Error: Could not find 'docs/assets' or 'dist/assets' directory.")
        print("    Please run build first or ensure compiled assets exist.")
        sys.exit(1)

    # 2. Find compiled CSS
    css_files = sorted(glob.glob(str(assets_dir / "*.css")), key=os.path.getmtime, reverse=True)
    if not css_files:
        print(f"[!] Error: No CSS files found in {assets_dir}")
        sys.exit(1)
    css_path = Path(css_files[0])
    print(f"[+] Found CSS: {css_path.name}")
    css_content = css_path.read_text(encoding="utf-8")

    # 3. Find compiled JS
    js_files = sorted(glob.glob(str(assets_dir / "*.js")), key=os.path.getmtime, reverse=True)
    if not js_files:
        print(f"[!] Error: No JS files found in {assets_dir}")
        sys.exit(1)
    js_path = Path(js_files[0])
    print(f"[+] Found JS: {js_path.name}")
    js_content = js_path.read_text(encoding="utf-8")

    # 4. Find icon and encode as base64
    icon_candidates = [
        project_dir / "icon.png",
        *glob.glob(str(assets_dir / "icon-*.png")),
        *glob.glob(str(assets_dir / "*.png"))
    ]
    icon_b64 = ""
    for ic in icon_candidates:
        p = Path(ic)
        if p.is_file():
            print(f"[+] Found icon: {p.name}")
            icon_b64 = base64.b64encode(p.read_bytes()).decode("ascii")
            break

    # 5. Build standalone HTML
    # We remove type="module" from <script> so browsers load it over file:// without CORS errors
    icon_tag = f'<link rel="icon" type="image/png" href="data:image/png;base64,{icon_b64}" />' if icon_b64 else ''

    standalone_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    {icon_tag}
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Password Card Generator</title>
    <style>
{css_content}
    </style>
  </head>
  <body>
    <div id="app"></div>
    <script>
{js_content}
    </script>
  </body>
</html>
"""

    output_file.write_text(standalone_html, encoding="utf-8")
    print(f"[✓] Successfully generated: {output_file} ({output_file.stat().st_size:,} bytes)")
    print("    You can now open this file directly by double-clicking it or via file://.")

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    out = current_dir / "standalone.html"
    if len(sys.argv) > 1:
        out = Path(sys.argv[1]).resolve()
    generate_standalone(current_dir, out)
