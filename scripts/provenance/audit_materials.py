#!/usr/bin/env python3
"""
Inventory of the supplier "Materials" folder -> products-audit.md

    MATERIALS_DIR=/path/to/Materials python3 scripts/provenance/audit_materials.py
Requires: pip install pymupdf pillow
"""
import hashlib, json, os, sys
import pymupdf
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MATERIALS = os.environ.get("MATERIALS_DIR", os.path.expanduser("~/Documents/Materials"))
DOCS = {d["source"]: d for d in json.load(open(os.path.join(ROOT, "data", "documents.json"), encoding="utf-8"))}
PRODUCTS = json.load(open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8"))

# Manual review notes (what the file is, and what was decided)
NOTES = {
    "TCS/tcsكتالوج.pdf": "Scanned TCS catalogue pages with hand-drawn circles and Arabic notes (internal marked-up copy). Product facts read from it; NOT published for download.",
    "BSM/DENTAL EQUIPMENTS/BSM_Milling_520D_Flyer_EN 20260127-old version.pdf": "File name says 'old version' (flyer V1.2.1). Used; a newer flyer should be requested.",
    "JJ TOOLS/1785379371038992.pdf": "533-page general carbide end-mill / drill / thread-mill catalogue (Korean/English). Not dental-specific; used for series-level entries only.",
    "PMMA & WAX.pdf": "",
    "Yamahachi/PMMA & WAX.pdf": "Two-page extract that duplicates catalogue pages 16-19; kept as a handy leaflet.",
    "ERAYLAR/erayturkce_2022-01-25_20-59-30.pdf": "Turkish-only mould chart for the standard ERAY line.",
    "ERAYLAR/eraydeluxetureng_2022-01-25_21-14-12.pdf": "Turkish/English mould chart for ERAY DELUXE.",
    "RENFERT/RENFERT_CATALOG_EN (3).PDF": "Renfert Catalog 2023 (156 pages). Source of ~150 products. Dated 3/2023.",
    "BSM/DENTAL MATERIALS/BSM_CL _Artist V1_Flyer(vertical)_2024.pdf": "Image-only flyer (no text layer); read visually.",
}
PROMO = ("Facebook-style promotional post (shows a phone number and QR code that differ from the site's contact details). "
         "Used only as a cropped product image; contact details not reused.")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    rows, by_hash = {}, {}
    for d, _, fs in os.walk(MATERIALS):
        for f in sorted(fs):
            if f.startswith("."):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, MATERIALS)
            brand = rel.split(os.sep)[0]
            e = {"rel": rel, "size": os.path.getsize(p), "ext": f.rsplit(".", 1)[-1].lower(), "flags": [], "info": ""}
            try:
                if e["ext"] == "pdf":
                    doc = pymupdf.open(p)
                    chars = sum(len(pg.get_text()) for pg in doc)
                    e["info"] = f"{len(doc)} p" + ("" if chars > 50 else ", image-only")
                    if chars <= 50:
                        e["flags"].append("no text layer")
                    if len(doc) <= 2 and e["size"] > 20_000_000:
                        e["flags"].append("oversized for page count (carries a whole catalogue's resources)")
                else:
                    im = Image.open(p)
                    e["info"] = f"{im.size[0]}x{im.size[1]} px"
            except Exception as ex:
                e["flags"].append(f"unreadable: {ex}")
            if e["size"] == 0:
                e["flags"].append("empty")
            if e["size"] > 5_000_000:
                e["flags"].append("> 5 MB")
            h = md5(p)
            by_hash.setdefault(h, []).append(rel)
            e["hash"] = h
            rows.setdefault(brand, []).append(e)
    dup_groups = [v for v in by_hash.values() if len(v) > 1]
    for brand in rows:
        for e in rows[brand]:
            if any(e["rel"] in g for g in dup_groups):
                e["flags"].append("byte-identical duplicate")
            if e["ext"] in ("jpg", "jpeg", "png"):
                e["note"] = PROMO
            elif e["ext"] == "pdf" and e["rel"] in DOCS:
                e["note"] = "Published: " + DOCS[e["rel"]]["title"]
            else:
                e["note"] = ""
            e["note"] = (NOTES.get(e["rel"]) or e["note"]).strip()
    # social post image / PDF wrapper pairs
    twin = {}
    for brand, items in rows.items():
        stems = {}
        for e in items:
            stems.setdefault(os.path.splitext(os.path.basename(e["rel"]))[0], []).append(e)
        for stem, es in stems.items():
            if len(es) > 1:
                for e in es:
                    if e["ext"] == "pdf":
                        e["flags"].append("duplicate of the same-named image (PDF wrapper)")
                        e["note"] = "PDF wrapper around the image of the same name; not published."
    total = sum(e["size"] for items in rows.values() for e in items)
    out = ["# Materials audit", "",
           f"Source: `{MATERIALS}`  ·  {sum(len(v) for v in rows.values())} files in {len(rows)} brand folders  ·  {total / 1e6:.0f} MB", ""]
    out += ["## Summary of findings", "",
            "- **Brands found: 15** (the old site claimed 8). Seven brands have no logo file in the project and are shown with a text wordmark until official logos are supplied.",
            "- **Duplicates:** social-post JPGs are also saved as same-named PDF wrappers (Audent, FDT Resin, IMT, LUSTRA, PHT, TCS); IMT's PDF is the two JPGs combined. The PDF wrappers are not published.",
            "- **Oversized:** every single-page Renfert leaflet is ~29.5 MB because it carries the whole 156-page catalogue's resources; rebuilding each from its own page (text verified identical) brings them to 0.2-0.4 MB. JJ Tools (51 MB), the Renfert catalogue (29.5 MB), Profeta C150 (14.6 MB), BSM Aconia Family (11 MB) and Teknik MP100 (10 MB) remain large.",
            "- **Not product-related / unsuitable to publish:** TCS Arabic-annotated scan (hand-drawn marks); JJ Tools is a general CNC cutting-tool catalogue; the 520D flyer is marked 'old version'.",
            "- **Wrong logo on the old site:** `assets/partners/AUDent.webp` shows *Audent Capital Partners* (a dragon mark), not the dental-ceramics company AUDent AG; `AUDents.webp` is the correct one.",
            ""]
    for brand in sorted(rows, key=str.lower):
        out += [f"## {brand}", "", "| File | Type | Size | Details | Flags | Decision / note |", "|---|---|---|---|---|---|"]
        for e in sorted(rows[brand], key=lambda x: x["rel"].lower()):
            nm = e["rel"].split(os.sep, 1)[-1].replace("|", "\\|")
            out.append(f"| {nm} | {e['ext'].upper()} | {e['size'] / 1e6:.2f} MB | {e['info']} | {'; '.join(e['flags'])} | {e['note']} |")
        n = sum(1 for p in PRODUCTS if p["brand"].replace("-", " ").lower() == brand.lower().replace("-", " ")
                or p["brand"] == brand.lower().replace(" ", "-"))
        out += ["", f"Products on the site from this folder: **{n}**", ""]
    out += ["## Byte-identical groups", ""]
    out += [f"- {', '.join(g)}" for g in dup_groups] or ["- none"]
    with open(os.path.join(ROOT, "products-audit.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("wrote products-audit.md")


if __name__ == "__main__":
    sys.exit(main())
