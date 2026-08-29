"""Build a static snapshot of the Django storefront for Netlify."""

import os
import shutil
import subprocess
import sys
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


def output_path(route: str) -> Path:
    relative_route = route.strip("/")
    if not relative_route:
        return DIST / "index.html"
    return DIST / relative_route / "index.html"


def export_page(client, route: str) -> None:
    response = client.get(route, secure=True, HTTP_HOST="testserver")
    if response.status_code != 200:
        raise RuntimeError(f"Could not export {route}: HTTP {response.status_code}")

    destination = output_path(route)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)
    print(f"Exported {route} -> {destination.relative_to(ROOT)}")


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ.setdefault("DJANGO_DEBUG", "False")
    os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "*")

    import django

    django.setup()

    from django.conf import settings
    from django.core.management import call_command
    from django.test import Client
    from shop.models import Category, Product

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    call_command("migrate", interactive=False, verbosity=0)
    call_command("seed_data", stdout=StringIO(), verbosity=0)

    subprocess.run([sys.executable, str(ROOT / "generate_icons.py")], check=True)
    if "testserver" not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append("testserver")
    settings.STATIC_ROOT = DIST / "static"
    call_command("collectstatic", interactive=False, verbosity=0)

    client = Client()
    routes = [
        "/",
        "/products/",
        "/cart/",
        "/signup/",
        "/login/",
        "/about/",
        "/contact/",
        "/install/",
    ]
    routes.extend(f"/products/category/{slug}/" for slug in Category.objects.values_list("slug", flat=True))
    routes.extend(f"/product/{slug}/" for slug in Product.objects.values_list("slug", flat=True))

    for route in routes:
        export_page(client, route)

    media_root = Path(settings.MEDIA_ROOT)
    if media_root.exists():
        shutil.copytree(media_root, DIST / "media", dirs_exist_ok=True)

    apk = ROOT / "release-assets" / "namma-chikmagaluru.apk"
    if apk.exists():
        shutil.copy2(apk, DIST / "static" / apk.name)

    print(f"Netlify site built at {DIST}")


if __name__ == "__main__":
    main()
