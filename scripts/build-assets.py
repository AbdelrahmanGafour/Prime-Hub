#!/usr/bin/env python3
"""
Export the web assets that data/*.json point to, from the supplier "Materials" folder.

  * product images   -> assets/products/<brand>/<product>.webp (max 1200 px) + <product>-sm.webp (480 px)
  * brand logos      -> assets/brands/<brand>.webp
  * PDFs             -> assets/downloads/<brand>/<name>.pdf (lossless clean-up only; page content is unchanged)
  * documents.json / brands.json are updated with real page counts and file sizes

    MATERIALS_DIR=/path/to/Materials python3 scripts/build-assets.py [--only-docs | --only-images] [--force]

Requires: pip install pymupdf pillow
Each image spec in data/asset-map.json is one of
    {"src","page","xref"}   embedded image by xref           {"src","page","index"} k-th embedded image on the page
    {"src","page","nth"}    n-th square-ish photo, left->right {"src","page","crop":[x0,y0,x1,y1]} fractional page crop
    {"src","crop":[...]}    fractional crop of an image file
"""
import io, json, os, shutil, sys
import pymupdf
from PIL import Image, ImageChops

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DATA = os.path.join(ROOT, "data")
MATERIALS = os.environ.get("MATERIALS_DIR", os.path.expanduser("~/Documents/Materials"))
ARGS = set(sys.argv[1:])
FORCE = "--force" in ARGS
MAX_W, THUMB = 1200, 480
_docs = {}


def doc(src):
    if src not in _docs:
        _docs[src] = pymupdf.open(os.path.join(MATERIALS, src))
    return _docs[src]


def pdf_image(d, xref):
    """Embedded image as RGBA (applies the soft mask so transparent backgrounds stay transparent)."""
    info = d.extract_image(xref)
    img = Image.open(io.BytesIO(info["image"]))
    if info.get("smask"):
        try:
            m = Image.open(io.BytesIO(d.extract_image(info["smask"])["image"])).convert("L")
            img = img.convert("RGB")
            if m.size != img.size:
                m = m.resize(img.size)
            img.putalpha(m)
        except Exception:
            pass
    return img.convert("RGBA")


def fractional_crop(img, box):
    w, h = img.size
    return img.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))


def load(spec):
    src = spec["src"]
    if src.lower().endswith(".pdf"):
        d = doc(src)
        page = d[spec["page"] - 1]
        if "xref" in spec:
            return pdf_image(d, spec["xref"])
        if "index" in spec:
            info = page.get_image_info(xrefs=True)[spec["index"]]
            return pdf_image(d, info["xref"])
        if "nth" in spec:
            cand = [i for i in page.get_image_info(xrefs=True)
                    if i.get("xref") and i["width"] >= 300 and 0.8 <= i["width"] / i["height"] <= 1.25]
            cand.sort(key=lambda i: i["bbox"][0])
            return pdf_image(d, cand[spec["nth"]]["xref"])
        if "crop" in spec:
            z = min(3.2, 2600 / page.rect.width)
            pix = page.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("RGBA")
            return fractional_crop(img, spec["crop"])
    else:
        img = Image.open(os.path.join(MATERIALS, src)).convert("RGBA")
        return fractional_crop(img, spec["crop"]) if "crop" in spec else img
    raise ValueError(spec)


def trim(img, pad=0.04):
    """Crop away transparent / near-white margins so product tiles are consistently filled."""
    a = img.getchannel("A")
    box = a.point(lambda v: 255 if v > 12 else 0).getbbox()
    if box and (box[2] - box[0]) < img.width * 0.98 or (box and (box[3] - box[1]) < img.height * 0.98):
        px, py = int((box[2] - box[0]) * pad), int((box[3] - box[1]) * pad)
        img = img.crop((max(0, box[0] - px), max(0, box[1] - py), min(img.width, box[2] + px), min(img.height, box[3] + py)))
    return img


def save_webp(img, path, max_side):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = img.copy()
    img.thumbnail((max_side, max_side), Image.LANCZOS)
    has_alpha = img.getchannel("A").getextrema()[0] < 250
    if not has_alpha:
        img = img.convert("RGB")
    img.save(path, "WEBP", quality=80, method=6, alpha_quality=90)
    return os.path.getsize(path)


def make_logo(img, name):
    """White-on-white logos: make near-white transparent so they sit on any tile."""
    px = img.load()
    if img.getchannel("A").getextrema()[0] >= 250:
        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = px[x, y]
                m = min(r, g, b)
                if m > 235:
                    px[x, y] = (r, g, b, 0)
                elif m > 190:
                    px[x, y] = (r, g, b, int(255 * (235 - m) / 45))
    return trim(img, 0.02)


def build_images():
    amap = json.load(open(os.path.join(DATA, "asset-map.json"), encoding="utf-8"))
    products = {p["id"]: p for p in json.load(open(os.path.join(DATA, "products.json"), encoding="utf-8"))}
    brands = json.load(open(os.path.join(DATA, "brands.json"), encoding="utf-8"))
    n = fail = 0
    for pid, specs in amap.items():
        if pid.startswith("_logo:"):
            slug = pid.split(":", 1)[1]
            out = os.path.join(ROOT, "assets", "brands", slug + ".webp")
            try:
                save_webp(make_logo(load(specs[0]), slug), out, 420)
                print("logo", slug)
            except Exception as e:
                print("LOGO FAIL", slug, e)
            continue
        p = products.get(pid)
        if not p:
            continue
        for i, spec in enumerate(specs):
            main = os.path.join(ROOT, p["image"]) if i == 0 else os.path.join(ROOT, p["gallery"][i - 1])
            if os.path.exists(main) and not FORCE:
                continue
            try:
                img = trim(load(spec))
                save_webp(img, main, MAX_W)
                if i == 0:
                    save_webp(img, os.path.join(ROOT, p["thumb"]), THUMB)
                n += 1
            except Exception as e:
                fail += 1
                print("IMAGE FAIL", pid, spec, repr(e))
    # normalise partner logos -> assets/brands/<slug>.webp
    for b in brands:
        out = os.path.join(ROOT, "assets", "brands", b["slug"] + ".webp")
        src = b.get("logo")
        if src and not src.startswith("assets/brands/") and os.path.exists(os.path.join(ROOT, src)):
            im = Image.open(os.path.join(ROOT, src)).convert("RGBA")
            save_webp(trim(im, 0.02), out, 420)
        b["logo"] = f"assets/brands/{b['slug']}.webp" if os.path.exists(out) else None
    json.dump(brands, open(os.path.join(DATA, "brands.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"images written: {n}, failed: {fail}")


def build_pdfs():
    docs = json.load(open(os.path.join(DATA, "documents.json"), encoding="utf-8"))
    brands = {b["slug"]: b for b in json.load(open(os.path.join(DATA, "brands.json"), encoding="utf-8"))}
    for b in brands.values():
        b["catalogs"] = []
    for d in docs:
        src = os.path.join(MATERIALS, d["source"])
        out = os.path.join(ROOT, d["file"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        tmp = out + ".tmp"
        pdf = pymupdf.open(src)
        best, kind = os.path.getsize(src), "copy"
        shutil.copyfile(src, out)
        # lossless clean-up: drop unreferenced objects and compress streams
        pdf.save(tmp, garbage=4, deflate=True, clean=True)
        if os.path.getsize(tmp) < best * 0.95:
            shutil.move(tmp, out); best, kind = os.path.getsize(out), "gc"
        elif os.path.exists(tmp):
            os.remove(tmp)
        if len(pdf) <= 8 and best > 2_000_000:
            # single leaflets exported from a large catalogue still carry the whole catalogue's resources:
            # rebuild them from their own pages only (text content is verified identical).
            new = pymupdf.open()
            new.insert_pdf(pdf)
            new.save(tmp, garbage=4, deflate=True, clean=True)
            same = [p.get_text() for p in pymupdf.open(tmp)] == [p.get_text() for p in pdf]
            if same and os.path.getsize(tmp) < best * 0.8:
                shutil.move(tmp, out); best, kind = os.path.getsize(out), "rebuilt"
            elif os.path.exists(tmp):
                os.remove(tmp)
        d["pages"] = len(pdf)
        d["sizeMB"] = round(os.path.getsize(out) / 1_048_576, 2)
        d["large"] = d["sizeMB"] > 8
        d["optimised"] = kind
        brands[d["brand"]]["catalogs"].append({"title": d["title"], "file": d["file"], "pages": d["pages"], "sizeMB": d["sizeMB"]})
        print(f"{d['file']:70s} {d['pages']:>4}p {d['sizeMB']:>7} MB {kind}")
    json.dump(docs, open(os.path.join(DATA, "documents.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(list(brands.values()), open(os.path.join(DATA, "brands.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if "--only-docs" not in ARGS:
        build_images()
    if "--only-images" not in ARGS:
        build_pdfs()
