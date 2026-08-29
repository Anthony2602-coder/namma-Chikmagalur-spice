"""Verify APK is a valid Android package."""

import sys
import zipfile
from pathlib import Path


def verify(path: Path) -> bool:
    if not path.exists():
        print(f"APK not found: {path}")
        return False
    if path.stat().st_size < 10000:
        print(f"APK too small: {path.stat().st_size} bytes")
        return False
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            if not any("AndroidManifest.xml" in n for n in names):
                print("Invalid APK: missing AndroidManifest.xml")
                return False
            if not any(n.endswith(".dex") for n in names):
                print("Invalid APK: missing classes.dex")
                return False
    except zipfile.BadZipFile:
        print("Invalid APK: not a valid zip file")
        return False
    print(f"APK verified: {path} ({path.stat().st_size // 1024} KB)")
    return True


if __name__ == "__main__":
    apk = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("release-assets/namma-chikmagaluru.apk")
    sys.exit(0 if verify(apk) else 1)
