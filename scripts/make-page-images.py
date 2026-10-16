#!/usr/bin/env python3
"""Export the inner-page banner/photo JPGs as responsive WebP (assets/img/pages/). Requires: pip install pillow"""
import os
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC, OUT = os.path.join(ROOT, "assets", "img"), os.path.join(ROOT, "assets", "img", "pages")
os.makedirs(OUT, exist_ok=True)
JOBS = {  # file -> widths
    "pexels-about-banner.jpg": (1600, 800), "pexels-products-banner.jpg": (1600, 800),
    "pexels-training-banner.jpg": (1600, 800), "pexels-service-banner.jpg": (1600, 800),
    "pexels-downloads-banner.jpg": (1600, 800), "pexels-contact-banner.jpg": (1600, 800),
    "pexels-about-photo.jpg": (1000, 500), "pexels-training-photo.jpg": (1200, 600),
    "pexels-service-photo.jpg": (1200, 600),
}
for f, widths in JOBS.items():
    im = Image.open(os.path.join(SRC, f)).convert("RGB")
    base = f.replace("pexels-", "").rsplit(".", 1)[0]
    for w in widths:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, f"{base}-{w}.webp"), "WEBP", quality=55, method=6)
        print(f"{base}-{w}.webp {w}x{h}")
