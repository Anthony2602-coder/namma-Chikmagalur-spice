"""Prepare Capacitor app folder for Android/iOS build."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APP = ROOT / "app"
SERVER_URL = os.environ.get("APP_SERVER_URL", "http://10.0.2.2:8000")

INDEX = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#2d5016">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="Namma Chikmagaluru">
    <title>Namma Chikmagaluru</title>
    <link rel="manifest" href="./manifest.json">
    <link rel="icon" href="./icons/icon-192.png">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a3009, #2d5016);
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .splash {{ text-align: center; padding: 2rem; }}
        .splash h1 {{ font-size: 1.8rem; margin: 1rem 0 0.5rem; }}
        .splash p {{ opacity: 0.8; margin-bottom: 1.5rem; }}
        .loader {{
            width: 50px; height: 50px;
            border: 4px solid rgba(255,255,255,0.2);
            border-top-color: #c8952e;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="splash">
        <div style="font-size:4rem">☕</div>
        <h1>Namma Chikmagaluru</h1>
        <p>Loading store…</p>
        <div class="loader"></div>
    </div>
    <script>
        const SERVER = "{SERVER_URL}";
        window.location.replace(SERVER);
    </script>
</body>
</html>"""

INSTALL = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#2d5016">
    <title>Install App</title>
    <style>
        body { font-family: sans-serif; background: #2d5016; color: #fff; padding: 2rem; text-align: center; }
        a { color: #c8952e; }
        .btn { display: inline-block; background: #c8952e; color: #1a3009; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; margin: 1rem; }
    </style>
</head>
<body>
    <h1>☕ Namma Chikmagaluru</h1>
    <p>Install the Android app</p>
    <a class="btn" href="./namma-chikmagaluru.apk" download>Download APK</a>
    <p><a href="./index.html">Open App</a></p>
</body>
</html>"""


def main():
    subprocess.run([sys.executable, str(ROOT / "generate_icons.py")], check=False)

    if APP.exists():
        shutil.rmtree(APP)
    APP.mkdir()

    icons_dir = APP / "icons"
    icons_dir.mkdir()
    static_icons = ROOT / "static" / "icons"
    for name in ("icon-192.png", "icon-512.png"):
        src = static_icons / name
        if src.exists():
            shutil.copy2(src, icons_dir / name)

    manifest = {
        "name": "Namma Chikmagaluru",
        "short_name": "NC Shop",
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#2d5016",
        "theme_color": "#2d5016",
        "icons": [
            {"src": "./icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "./icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    (APP / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (APP / "index.html").write_text(INDEX, encoding="utf-8")
    (APP / "install.html").write_text(INSTALL, encoding="utf-8")

    apk = ROOT / "release-assets" / "namma-chikmagaluru.apk"
    if apk.exists():
        shutil.copy2(apk, APP / "namma-chikmagaluru.apk")

    cap_config = json.loads((ROOT / "capacitor.config.json").read_text())
    cap_config["server"] = {"url": SERVER_URL, "androidScheme": "https", "cleartext": True}
    (ROOT / "capacitor.config.json").write_text(json.dumps(cap_config, indent=2), encoding="utf-8")

    print(f"Built {APP} with server URL: {SERVER_URL}")


if __name__ == "__main__":
    main()
