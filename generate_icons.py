"""Generate PNG icons from SVG for PWA and Capacitor."""

from pathlib import Path

ROOT = Path(__file__).parent
SVG = ROOT / "static" / "icons" / "icon.svg"
OUT = ROOT / "static" / "icons"

def main():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow required: pip install Pillow")
        return

    for size in (192, 512):
        img = Image.new("RGBA", (size, size), (45, 80, 22, 255))
        draw = ImageDraw.Draw(img)
        margin = size // 8
        draw.ellipse([margin, margin, size - margin, size - margin], fill=(74, 124, 35, 255))
        try:
            font = ImageFont.truetype("arial.ttf", size // 4)
        except OSError:
            font = ImageFont.load_default()
        text = "NC"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size - tw) // 2, (size - th) // 2 - size // 16), text, fill=(200, 149, 46, 255), font=font)
        img.save(OUT / f"icon-{size}.png")
        print(f"Created icon-{size}.png")

    app_icons = ROOT / "app" / "icons"
    app_icons.mkdir(parents=True, exist_ok=True)
    for size in (192, 512):
        src = OUT / f"icon-{size}.png"
        if src.exists():
            import shutil
            shutil.copy2(src, app_icons / f"icon-{size}.png")

if __name__ == "__main__":
    main()
