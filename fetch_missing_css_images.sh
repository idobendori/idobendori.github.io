#!/bin/bash
# One-time: grabs the 2 images referenced from CSS background-image urls
# that the earlier migration script missed (it only scanned .html files).
# Run from a normal Terminal (not through Claude), from the repo root:
#   cd ~/Documents/GitHub/idobendori.github.io
#   bash fetch_missing_css_images.sh
set -e
cd "$(dirname "$0")"
curl -A "Mozilla/5.0" -o "images/67a8ac79b7b7e3d82b75b055_IMG_9803.JPG" \
  "https://cdn.prod.website-files.com/60acf1e0d28b3f733c3be205/67a8ac79b7b7e3d82b75b055_IMG_9803.JPG"
curl -A "Mozilla/5.0" -o "images/60d06751f9061aac27f3e008_AC957BDA-0D1E-463A-B386-6F50C27E107C.JPG" \
  "https://cdn.prod.website-files.com/60acf1e0d28b3f733c3be205/60d06751f9061aac27f3e008_AC957BDA-0D1E-463A-B386-6F50C27E107C.JPG"
echo "Done. Both files should now be in images/."
