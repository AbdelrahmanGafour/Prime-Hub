#!/usr/bin/env python3
"""
Assemble data/brands.json, data/products.json, data/documents.json and data/asset-map.json
from the curated entries (curated.py) and the extracted Renfert catalogue
(data/_source/renfert_extract.json).

    python3 scripts/provenance/build_dataset.py

Then run `python3 scripts/build-assets.py` to export the images and PDFs these files point to.
Day-to-day, you can also simply edit data/products.json by hand (see README).
"""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import curated as C  # noqa: E402

DATA = os.path.join(ROOT, "data")
RCAT = "RENFERT/RENFERT_CATALOG_EN (3).PDF"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.replace("α", "a").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def first_sentence(text, limit):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^\d{1,3}\s+(?=[A-Z])", "", text)           # stray page numbers
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    s = m.group(1) if m else text
    if len(s) <= limit:
        return s
    cut = s[:limit - 1].rsplit(" ", 1)[0].rstrip(",;:- ")
    return cut + "…"


def sentences(text, limit):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^\d{1,3}\s+(?=[A-Z])", "", text)
    out = ""
    for s in re.findall(r".+?(?:[.!?](?:\s|$)|$)", text):
        if len(out) + len(s) > limit and out:
            break
        out += s
    return out.strip()


# --------------------------------------------------------------------------------------
# Renfert classification
# --------------------------------------------------------------------------------------
def ren_class(r):
    pg, nm = r["page"], r["name"]
    E, M = "equipment", "material"
    if pg == 11: return E, "milling-printing"
    if pg == 12: return M, "resins"
    if pg == 14: return M, "lab-supplies"
    if pg in (15, 16): return E, "scanners-imaging"
    if pg in (19, 20, 21) or 24 <= pg <= 32: return E, "extraction"
    if 37 <= pg <= 44: return E, "sandblasting"
    if pg in (47, 48): return E, "cleaning"
    if pg == 49: return (M, "lab-supplies") if "descaler" in nm else (E, "cleaning")
    if pg in (52, 53, 54, 57, 59, 60, 61, 62, 64, 65, 67): return E, "model-prep"
    if pg == 66: return M, "lab-supplies"
    if pg in (72, 73, 74, 75, 76, 77, 81): return E, "wax-casting"
    if pg == 80: return E, "furnaces"
    if pg in (82, 84): return E, "cleaning"
    if pg == 83: return M, "lab-supplies"
    if 90 <= pg <= 92 or 95 <= pg <= 98 or 101 <= pg <= 105: return M, "lab-supplies"
    if 108 <= pg <= 111 or 114 <= pg <= 117: return M, "tools-finishing"
    if pg == 118: return (M, "lab-supplies") if nm == "Remberti" else (M, "tools-finishing")
    if pg == 121 or 137 <= pg <= 145: return M, "pmma-wax"
    if pg == 146: return (M, "lab-supplies") if "Mesh" in nm else (M, "pmma-wax")
    if pg in (148, 149, 150): return M, "tools-finishing"
    return M, "lab-supplies"          # 120, 122, 124-126, 128-133, 151


LEAFLET = {
    "Basic eco": "renfert-basic-eco", "Millo": "renfert-millo", "Millo pro": "renfert-millo", "MT3": "renfert-mt3",
    "POWER steamer 1": "renfert-power-steamer", "SILENT compact": "renfert-silent-compact",
    "SILENT compactCAM": "renfert-silent-compactcam", "Top spin": "renfert-top-spin", "Twister": "renfert-twister",
    "Twister venturi": "renfert-twister", "Vario E": "renfert-vario-e", "Waxlectric I": "renfert-waxlectric",
    "Waxlectric II": "renfert-waxlectric",
}
FEATURED_REN = {"Twister evolution", "Basic quattro IS", "MT premium", "POWER steamer 2", "SILENT EC2", "GEO Expert A. Bruguera"}


def metric(v):
    return v.split(" // ")[0].strip()


def ren_products():
    recs = json.load(open(os.path.join(DATA, "_source", "renfert_extract.json"), encoding="utf-8"))
    out = []
    for r in recs:
        cat, sub = ren_class(r)
        nm = r["name"]
        intro = re.sub(r"\s+Tip\b.*$", "", r["intro"])
        summ = first_sentence(intro, 140) if intro else (r["type"] or nm)
        desc = sentences(intro, 300)
        specs = [[a, metric(b)] for a, b in r["specs"] if a and b]
        feats = [re.sub(r"\s+Tip\b.*$", "", a)[:180] for a in r["advantages"]][:5]
        apps = [a[:120] for a in r["areas"]][:6]
        if not feats:
            feats = [re.sub(r"\s+Tip\b.*$", "", d)[:180] for d in r["details"]][:4]
        leaflet = LEAFLET.get(nm)
        out.append(dict(brand="renfert", name=nm, category=cat, subcategory=sub, summary=summ, description=desc,
                        model="", specs=specs, features=feats, applications=apps,
                        tags=[t for t in [r["type"]] if t], doc=leaflet or "renfert-catalog",
                        page=None if leaflet else r["page"], catalogPage=r["page"],
                        img={"src": RCAT, "page": r["page"], "xref": r["image"]["xref"]} if r["image"] else None,
                        gallery=[], featured=nm in FEATURED_REN, isNew=bool(r["new"]), pid=None,
                        orders=[[a, b] for a, b in r["orders"] if re.fullmatch(r"\d{5,8}", b or "")][:12]))
    # New products published as stand-alone leaflets (not in the 2023 catalogue)
    xs = "RENFERT/20250821_B_SILENT-XS_2pages_en (1).pdf"
    out.append(dict(
        brand="renfert", name="SILENT XS", category="equipment", subcategory="extraction",
        summary="Cordless mobile suction unit with H13/HEPA filter (99.99%) for precise touch-ups on temporaries, splints and dentures.",
        description="A fully mobile, battery-powered suction unit designed for dental offices and in-house laboratories, "
                    "collecting debris at the source during minor, small-scale finishing work.",
        model="", specs=[["Volume flow (max.)", "510 l/min"], ["Filter", "HEPA / H13 fine filter"],
                         ["Sound pressure level", "52.7 dB(A)"], ["Weight (without battery)", "1.12 kg"],
                         ["Dimensions (W x H x D)", "223 x 248 x 193 mm"], ["Battery (not included)", "8 x AA NiMH"],
                         ["Power supply", "100-240 V, 50-60 Hz"]],
        features=["Cordless and battery-powered for maximum freedom of movement", "One-handed operation with LED lighting",
                  "Bag-free, H13/HEPA filter with 99.99% collector efficiency"],
        applications=["Temporary restorations", "Splints", "Dentures"], tags=["Mobile suction unit"],
        doc="renfert-silent-xs", page=None, catalogPage=None, img={"src": xs, "page": 2, "index": 2}, gallery=[],
        featured=False, isNew=True, pid=None, orders=[["SILENT XS", "29220000"]]))
    lt = "RENFERT/LIGHT-1_2pages_en.pdf"
    out.append(dict(
        brand="renfert", name="LIGHT 1", category="equipment", subcategory="scanners-imaging",
        summary="Dental worklight with CRI 97 colour rendering, uniform glare-free illumination and 100% flicker-free light.",
        description="A dental worklight with ray-tracing optics for uniform, rectangular illumination of the bench, "
                    "with daylight and blue-light-elimination modes and a composite mode at the touch of a button.",
        model="", specs=[["Colour rendering index (Ra / CRI)", "97.5"], ["Extended CRI (Re)", "96"], ["Glare value UGR", "19"],
                         ["Intensity tolerance (calibrated)", "± 5 %"], ["Colour temperature tolerance", "± 50 K"],
                         ["Power supply", "100-240 V, 50-60 Hz"], ["Weight", "3.7 kg"]],
        features=["Colour rendering quality CRI 97", "Uniform, glare-free rectangular illumination",
                  "Light modes for daylight and blue-light elimination", "100% flicker-free"],
        applications=[], tags=["Dental worklight"], doc="renfert-light-1", page=None, catalogPage=None,
        img={"src": lt, "page": 2, "index": 2}, gallery=[], featured=False, isNew=True, pid=None,
        orders=[["LIGHT 1, tabletop mounting", "25000600"], ["LIGHT 1, wall mounting", "25000700"]]))
    return out


# --------------------------------------------------------------------------------------
CHIP_PRIORITY = [r"^accuracy", r"^axes$", r"^spindle", r"^power consumption", r"^rated power", r"^volume flow",
                 r"^working temperature", r"^target temperature", r"^working pressure", r"^tank capacity", r"^capacity",
                 r"^cusp angle", r"^layers", r"^flexural strength", r"^dimensions", r"^weight", r"^packing", r"^thickness",
                 r"^size", r"^shades"]
LABEL_SHOWN = {"layers", "cusp angle", "packing", "thickness", "size", "shades", "axes", "capacity"}


def chips_for(p):
    chips = []
    for pat in CHIP_PRIORITY:
        for lab, val in p["specs"]:
            if re.search(pat, lab, re.I):
                v = val if len(val) <= 22 else ""
                if not v:
                    continue
                chips.append((lab + " " + v) if lab.lower() in LABEL_SHOWN else v)
                break
        if len(chips) == 3:
            break
    if len(chips) < 2:
        for t in p["tags"]:
            if len(t) <= 22 and t not in chips:
                chips.append(t)
            if len(chips) == 2:
                break
    return chips[:3]


def main():
    brands = {b["slug"]: dict(b) for b in C.BRANDS}
    folder_to_slug = {b["folder"]: b["slug"] for b in C.BRANDS}

    prods = [dict(p) for p in C.PRODUCTS] + ren_products()
    seen, final, amap = set(), [], {}
    doc_pages = C.DOCS
    for p in prods:
        pid = p.get("pid") or f"{p['brand']}-{slug(p['name'])}"
        base, n = pid, 2
        while pid in seen:
            pid, n = f"{base}-{n}", n + 1
        seen.add(pid)
        short = pid[len(p["brand"]) + 1:]
        d = doc_pages.get(p["doc"]) if p["doc"] else None
        datasheet = None
        if d:
            datasheet = f"assets/downloads/{d['brand']}/{d['out']}" + (f"#page={p['page']}" if p.get("page") else "")
        entry = dict(id=pid, brand=p["brand"], name=p["name"], model=p["model"], category=p["category"],
                     subcategory=p["subcategory"], summary=p["summary"], description=p["description"],
                     specs=[{"label": a, "value": b} for a, b in p["specs"]], features=p["features"],
                     applications=p["applications"], image=None, thumb=None, gallery=[], datasheet=datasheet,
                     tags=p["tags"], chips=[], featured=bool(p["featured"]), new=bool(p["isNew"]))
        if p.get("orders"):
            entry["orderNumbers"] = [{"label": a, "no": b} for a, b in p["orders"]]
        if p.get("catalogPage") and p["brand"] == "renfert":
            entry["sourcePage"] = p["catalogPage"]
        entry["chips"] = chips_for({"specs": p["specs"], "tags": p["tags"]})
        imgs = ([p["img"]] if p["img"] else []) + list(p.get("gallery") or [])
        if imgs:
            entry["image"] = f"assets/products/{p['brand']}/{short}.webp"
            entry["thumb"] = f"assets/products/{p['brand']}/{short}-sm.webp"
            entry["gallery"] = [f"assets/products/{p['brand']}/{short}-{i + 1}.webp" for i in range(1, len(imgs))]
            amap[pid] = imgs
        final.append(entry)

    # brand derived fields ---------------------------------------------------------------
    for b in brands.values():
        mine = [e for e in final if e["brand"] == b["slug"]]
        b["categories"] = sorted({e["category"] for e in mine})
        b["productCount"] = len(mine)
        b["catalogs"] = []
        b["logo"] = b["logo"]
        b.pop("folder", None)
    docs_out = []
    for key, d in C.DOCS.items():
        cats = sorted({e["category"] for e in final if e["datasheet"] and e["datasheet"].split("#")[0].endswith("/" + d["out"])})
        rec = dict(id=key, brand=d["brand"], title=d["title"], type=d["type"], lang=d["lang"],
                   file=f"assets/downloads/{d['brand']}/{d['out']}", pages=None, sizeMB=None, categories=cats,
                   source=d["src"])
        docs_out.append(rec)
        brands[d["brand"]]["catalogs"].append({"title": d["title"], "file": rec["file"], "pages": None, "sizeMB": None})
    # documents that list no product (brand-level docs) still carry the brand categories
    for rec in docs_out:
        if not rec["categories"]:
            rec["categories"] = brands[rec["brand"]]["categories"]

    final.sort(key=lambda e: (e["brand"], e["category"], e["subcategory"], e["name"].lower()))
    json.dump(final, open(os.path.join(DATA, "products.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(list(brands.values()), open(os.path.join(DATA, "brands.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(docs_out, open(os.path.join(DATA, "documents.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    taxonomy = {k: {"label": v["label"], "sub": [{"slug": s, "label": l} for s, l in v["sub"]]} for k, v in C.TAXONOMY.items()}
    json.dump(taxonomy, open(os.path.join(DATA, "taxonomy.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for slug_, spec in C.LOGO_SOURCES.items():
        amap["_logo:" + slug_] = [spec]
    json.dump(amap, open(os.path.join(DATA, "asset-map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    from collections import Counter
    print(len(final), "products;", len(brands), "brands;", len(docs_out), "documents")
    print(Counter(e["category"] for e in final))
    print("with image:", sum(1 for e in final if e["image"]), "without:", sum(1 for e in final if not e["image"]))


if __name__ == "__main__":
    main()
