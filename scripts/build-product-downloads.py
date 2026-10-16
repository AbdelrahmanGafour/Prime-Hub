#!/usr/bin/env python3
"""
Attach a `downloads` list to every product in data/products.json.

  * Renfert catalogue products get their own one-page product sheet, cut from the Catalog 2023 PDF
    (assets/downloads/renfert/datasheets/<product>.pdf), plus the stand-alone leaflet (if any) and the full catalogue.
  * All other products link to their brand document (with the page number where the product appears).

    MATERIALS_DIR is not needed (works from assets/downloads). Requires: pip install pymupdf
    Run after build_dataset.py / build-assets.py.
"""
import json, os
import pymupdf

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DATA = os.path.join(ROOT, "data")
products = json.load(open(os.path.join(DATA, "products.json"), encoding="utf-8"))
docs = {d["file"]: d for d in json.load(open(os.path.join(DATA, "documents.json"), encoding="utf-8"))}
CAT = "assets/downloads/renfert/renfert-catalog-2023.pdf"
outdir = os.path.join(ROOT, "assets", "downloads", "renfert", "datasheets")
os.makedirs(outdir, exist_ok=True)
cat_doc = pymupdf.open(os.path.join(ROOT, CAT))
mb = lambda p: round(os.path.getsize(p) / 1_048_576, 2)


def entry(doc, title=None, page=None):
    e = {"title": title or doc["title"], "type": doc["type"].capitalize(), "lang": doc["lang"], "file": doc["file"],
         "pages": doc["pages"], "sizeMB": doc["sizeMB"]}
    if page:
        e["page"] = page
    return e


for p in products:
    dl = []
    ds = p.get("datasheet") or ""
    base, _, frag = ds.partition("#page=")
    page = int(frag) if frag.isdigit() else None
    if p["brand"] == "renfert":
        sp = p.get("sourcePage")
        if sp:
            rel = f"assets/downloads/renfert/datasheets/{p['id']}.pdf"
            out = os.path.join(ROOT, rel)
            if not os.path.exists(out):
                n = pymupdf.open(); n.insert_pdf(cat_doc, from_page=sp - 1, to_page=sp - 1)
                n.save(out, garbage=4, deflate=True, clean=True)
            dl.append({"title": f"{p['name']} product sheet", "type": "Datasheet", "lang": "EN", "file": rel, "pages": 1,
                       "sizeMB": mb(out), "note": f"Page {sp} of the Renfert Catalog 2023"})
        if base and base in docs and base != CAT:
            dl.append(entry(docs[base]))
        dl.append(entry(docs[CAT], "Renfert Catalog 2023 (complete)"))
    elif base and base in docs:
        dl.append(entry(docs[base], page=page))
    p["downloads"] = dl
json.dump(products, open(os.path.join(DATA, "products.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(sum(1 for p in products if p["downloads"]), "products with downloads;",
      round(sum(os.path.getsize(os.path.join(outdir, f)) for f in os.listdir(outdir)) / 1_048_576, 1), "MB of product sheets")
