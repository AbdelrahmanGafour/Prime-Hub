#!/usr/bin/env python3
"""
Generate the Prime Hub brand asset set from the master logo assets/img/PrimeHub_Logo.png (500 x 239, transparent).

  assets/img/brand/primehub-logo.webp        (+@2x)   full-colour logo for light backgrounds
  assets/img/brand/primehub-logo-white.webp  (+@2x)   PRIME in brand orange, HUB in white, for dark backgrounds
  assets/img/brand/og-image.png                       1200 x 630 social card (white logo on brand blue)
  assets/img/favicon/                                 favicon.ico, 16/32/48 png, apple-touch-icon (180), 192/512 png, favicon.svg
  favicon.ico                                         copy in the site root

    python3 scripts/make-brand-assets.py            (requires: pip install pillow)
"""
import os, shutil
from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "assets", "img", "PrimeHub_Logo.png")
OUT = os.path.join(ROOT, "assets", "img", "brand")
FAV = os.path.join(ROOT, "assets", "img", "favicon")
BLUE, ORANGE = (0, 64, 156), (255, 85, 6)
os.makedirs(OUT, exist_ok=True)
os.makedirs(FAV, exist_ok=True)

logo = Image.open(SRC).convert("RGBA")
W, H = logo.size


def save(img, path, **kw):
    img.save(os.path.join(OUT, path), **kw)


def sized(img, h):
    return img.resize((round(img.width * h / img.height), h), Image.LANCZOS)


# full-colour logo, 1x = 50 px high (header 44-52 px), 2x = 100 px, 3x = 150 px
for name, h in (("primehub-logo", 50), ("primehub-logo@2x", 100), ("primehub-logo@3x", 150)):
    save(sized(logo, h), name + ".webp", quality=92, method=6, alpha_quality=100)

# white version for dark backgrounds: blue pixels -> white, orange pixels stay orange
white = logo.copy()
px = white.load()
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if a and b > r:                    # blue-ish ("HUB")
            px[x, y] = (255, 255, 255, a)
for name, h in (("primehub-logo-white", 50), ("primehub-logo-white@2x", 100), ("primehub-logo-white@3x", 150)):
    save(sized(white, h), name + ".webp", quality=92, method=6, alpha_quality=100)
shutil.copyfile(SRC, os.path.join(OUT, "primehub-logo-master.png"))

# --- favicon mark: orange "P" over white "H" on a brand-blue rounded square ----------------
def letter_boxes(img, y0, y1):
    """Column-wise bounding boxes of glyphs inside the horizontal band y0..y1."""
    a = img.getchannel("A").crop((0, y0, W, y1))
    cols = [any(a.getpixel((x, y)) > 40 for y in range(a.height)) for x in range(W)]
    boxes, start = [], None
    for x, on in enumerate(cols + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            boxes.append((start, x))
            start = None
    return boxes


rows_alpha = logo.getchannel("A")
row_on = [any(rows_alpha.getpixel((x, y)) > 40 for x in range(0, W, 2)) for y in range(H)]
bands, s = [], None
for y, on in enumerate(row_on + [False]):
    if on and s is None:
        s = y
    elif not on and s is not None:
        bands.append((s, y))
        s = None
top, bottom = bands[0], bands[-1]            # PRIME band, HUB band
p0, p1 = letter_boxes(logo, *top)[0]
h0, h1 = letter_boxes(logo, *bottom)[0]
P = logo.crop((p0, top[0], p1, top[1]))
Hh = white.crop((h0, bottom[0], h1, bottom[1]))


def mark(size):
    s = size * 4                                       # draw big, downsample for clean edges
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * 0.22), fill=BLUE + (255,))
    box = int(s * 0.74)                                # glyph column height budget (P + gap + H)
    gap = int(s * 0.07)
    gh = (box - gap) // 2
    def fit(g):
        w = round(g.width * gh / g.height)
        return g.resize((w, gh), Image.LANCZOS)
    gp, gh_ = fit(P), fit(Hh)
    y0 = (s - (gh * 2 + gap)) // 2
    img.alpha_composite(gp, ((s - gp.width) // 2, y0))
    img.alpha_composite(gh_, ((s - gh_.width) // 2, y0 + gh + gap))
    return img.resize((size, size), Image.LANCZOS)


sizes = {16: "favicon-16.png", 32: "favicon-32.png", 48: "favicon-48.png", 180: "apple-touch-icon.png",
         192: "icon-192.png", 512: "icon-512.png"}
for sz, fn in sizes.items():
    mark(sz).save(os.path.join(FAV, fn))
mark(256).save(os.path.join(FAV, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
mark(64).save(os.path.join(FAV, "favicon.webp"), quality=95, method=6)
shutil.copyfile(os.path.join(FAV, "favicon.ico"), os.path.join(ROOT, "favicon.ico"))

# --- Open Graph card ---------------------------------------------------------------------
card = Image.new("RGB", (1200, 630), (4, 19, 46))
g = Image.new("RGB", (1200, 630))
gp = g.load()
for y in range(630):
    for x in range(1200):
        t = min(1, max(0, (x * 0.55 + y * 0.9) / 1300))
        gp[x, y] = (int(4 + (0 - 4) * t), int(19 + (48 - 19) * t), int(46 + (111 - 46) * t))
card = g
lg = white.resize((520, round(520 * H / W)), Image.LANCZOS)
card.paste(lg, (80, 150), lg)
d = ImageDraw.Draw(card)
d.rectangle((80, 150 + lg.height + 36, 140, 150 + lg.height + 42), fill=ORANGE)
card.save(os.path.join(OUT, "og-image.png"), optimize=True)

with open(os.path.join(FAV, "favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#00409C"/>'
            '<text x="32" y="30" text-anchor="middle" font-family="Poppins,Arial,sans-serif" font-weight="800" font-size="24" fill="#FF5506">P</text>'
            '<text x="32" y="54" text-anchor="middle" font-family="Poppins,Arial,sans-serif" font-weight="800" font-size="24" fill="#fff">H</text></svg>')
print("brand assets written")
