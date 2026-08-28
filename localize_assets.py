#!/usr/bin/env python3
"""
One-time migration script: downloads every asset the site's HTML still
references directly from Webflow's CDN (images, the shared CSS file, and
a handful of leftover JS chunks) into the local images/ css/ js/ folders,
then rewrites every .html file to point at the local copy instead.

Run this from a normal Terminal window (NOT through Claude/Cowork) so it
has full internet access:

    cd ~/Documents/GitHub/idobendori.github.io
    python3 localize_assets.py

Safe to re-run: already-downloaded files are skipped, and the first time
it edits an .html file it saves a `<name>.html.bak` backup next to it.
"""

import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOSTS = ("cdn.prod.website-files.com", "d3e54v103j8qbb.cloudfront.net")

EXT_FOLDER = {
    ".css": "css",
    ".js": "js",
    ".png": "images", ".jpg": "images", ".jpeg": "images",
    ".svg": "images", ".gif": "images", ".webp": "images",
    ".json": "images", ".mp4": "images", ".webm": "images",
}

# Known URL -> already-present local file, so we don't create a redundant duplicate.
SPECIAL_CASES = {
    "https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=60acf1e0d28b3f733c3be205": "js/jquery.js",
}

url_pattern = re.compile(r'(?:src|href)="(https://(?:%s)[^"]*)"' % "|".join(re.escape(h) for h in HOSTS))


def local_name_for(url):
    parsed = urllib.parse.urlparse(url)
    name = urllib.parse.unquote(os.path.basename(parsed.path))
    ext = os.path.splitext(name)[1].lower()
    folder = EXT_FOLDER.get(ext)
    if not folder:
        print(f"  ! unknown file type, skipping: {url}")
        return None, None
    return folder, name


def download(url, dest):
    if dest.exists():
        print(f"  already have {dest.relative_to(ROOT)}")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        print(f"  downloaded {dest.relative_to(ROOT)}")
        return True
    except Exception as e:
        print(f"  ! failed {url}: {e}")
        return False


def main():
    html_files = sorted(ROOT.glob("*.html"))
    all_urls = set()
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        all_urls.update(url_pattern.findall(text))

    print(f"Found {len(all_urls)} unique external asset URLs across {len(html_files)} pages.\n")

    url_to_local = {}
    for url in sorted(all_urls):
        if url in SPECIAL_CASES:
            url_to_local[url] = SPECIAL_CASES[url]
            print(f"  mapping {url} -> {SPECIAL_CASES[url]} (already local)")
            continue
        folder, name = local_name_for(url)
        if not folder:
            continue
        dest = ROOT / folder / name
        if download(url, dest):
            url_to_local[url] = f"{folder}/{name}"

    print(f"\nRewriting {len(html_files)} HTML files...")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        original = text
        for url, local in url_to_local.items():
            text = text.replace(f'"{url}"', f'"{local}"')
        if text != original:
            backup = f.with_suffix(f.suffix + ".bak")
            if not backup.exists():
                backup.write_text(original, encoding="utf-8")
            f.write_text(text, encoding="utf-8")
            print(f"  updated {f.name}")

    print("\nDone. Everything is now local. Come back to the chat and let Claude know so it can finish the cleanup, wire up Formspree, and commit.")


if __name__ == "__main__":
    main()
