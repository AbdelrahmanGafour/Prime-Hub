#!/usr/bin/env python3
"""
Extract structured product records from the Renfert "Catalog 2023" PDF.

Every record keeps the PDF page number it came from, so each product on the
site is traceable to a source page.

    MATERIALS_DIR=/path/to/Materials python3 scripts/provenance/extract_renfert.py

Output: data/_source/renfert_extract.json  (consumed by build_dataset.py)
Requires: pip install pymupdf
"""
import json, os, re, sys
import pymupdf

MATERIALS = os.environ.get("MATERIALS_DIR", os.path.expanduser("~/Documents/Materials"))
CATALOG = os.path.join(MATERIALS, "RENFERT", "RENFERT_CATALOG_EN (3).PDF")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "data", "_source", "renfert_extract.json")

# Pages that are chapter openers, overviews, accessory lists or imprint pages.
SKIP_PAGES = {9, 13, 17, 18, 22, 23, 33, 34, 35, 36, 45, 46, 50, 51, 55, 56, 58, 63, 68, 69, 70, 71, 78, 79,
              85, 86, 87, 88, 89, 93, 94, 99, 100, 106, 107, 112, 113, 119, 123, 127, 134, 135, 136, 147,
              153, 154, 155, 156}
ICON = re.compile(r"^(tool in-?|cluded|easy use|silent|compact|perfect view|smart control|NEW|tool included)$", re.I)
DROP_NAMES = {"Overview", "3D Filament printing"}


def clean(t):
    return t.replace("\xa0", " ").strip()


def read_pages(doc):
    raw = {}
    for i in range(9, 153):
        p = doc[i]
        lines = []
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"]).strip()
                if not t:
                    continue
                lines.append({"t": t, "sz": round(max(s["size"] for s in l["spans"])),
                              "x0": round(l["bbox"][0]), "y0": round(l["bbox"][1]),
                              "x1": round(l["bbox"][2]), "y1": round(l["bbox"][3])})
        imgs = [{"k": k, "x0": round(im["bbox"][0]), "y0": round(im["bbox"][1]), "x1": round(im["bbox"][2]),
                 "y1": round(im["bbox"][3]), "w": im["width"], "h": im["height"], "xref": im.get("xref")}
                for k, im in enumerate(p.get_image_info(xrefs=True))]
        raw[i + 1] = {"lines": lines, "imgs": imgs}
    return raw


def regions(raw, pg):
    """Split a page into one region per product (columns or stacked rows)."""
    L = [l for l in raw[pg]["lines"] if l["y0"] < 760]
    heads = [l for l in L if l["sz"] == 22]
    if not heads:
        return []
    ys = sorted({h["y0"] for h in heads})
    xs = sorted({h["x0"] for h in heads})
    rows = len(ys) > 1 and max(ys) - min(ys) > 150
    cols = len(xs) > 1 and max(xs) - min(xs) > 150
    if rows:
        bands = []
        for y in ys:
            if not bands or y - bands[-1] > 150:
                bands.append(y)
        res = []
        for k, b in enumerate(bands):
            lo = b - 20
            hi = bands[k + 1] - 5 if k + 1 < len(bands) else 800
            res.append({"box": (0, lo, 596, hi), "lines": [l for l in L if lo <= l["y0"] < hi]})
        return res
    if cols:
        return [{"box": (0, 0, 299, 800), "lines": [l for l in L if l["x0"] < 310]},
                {"box": (299, 0, 596, 800), "lines": [l for l in L if l["x0"] >= 310]}]
    return [{"box": (0, 0, 596, 800), "lines": L}]


def join_hyph(lines):
    s = ""
    for t in lines:
        s = s[:-1] + t if s.endswith("-") and not s.endswith(" -") else (s + " " + t if s else t)
    return s


def bullets(lines):
    items = []
    for t in lines:
        if t.startswith("■"):
            items.append(t[1:].strip())
        elif items:
            items[-1] = (items[-1][:-1] + t) if items[-1].endswith("-") else items[-1] + " " + t
        else:
            items.append(t)
    return items


def rows_of(lines):
    by = {}
    for l in lines:
        by.setdefault(l["y0"], []).append(l)
    out = []
    for y, ls in sorted(by.items()):
        ls = sorted(ls, key=lambda l: l["x0"])
        if len(ls) >= 2:
            out.append((clean(ls[0]["t"]), clean(" ".join(l["t"] for l in ls[1:]))))
    return out


def record(raw, pg, reg):
    seg = reg["lines"]
    name, typ, intro, secs, cur = [], [], [], {}, None
    small = [l for l in seg if l["sz"] == 7 and not ICON.match(clean(l["t"]))]
    th = next((l for l in seg if clean(l["t"]) == "Technical data"), None)
    oh = next((l for l in seg if clean(l["t"]) == "Ordering information"), None)
    side = th and oh and abs(th["x0"] - oh["x0"]) > 14
    for l in small:
        c = None
        if th and oh:
            if side:
                c = "ord" if (oh["x0"] > th["x0"] and l["x0"] >= oh["x0"] - 3) or (oh["x0"] < th["x0"] and l["x0"] < th["x0"] - 3) else "tech"
                if l["y0"] <= (oh["y0"] if c == "ord" else th["y0"]):
                    c = None
            else:
                c = "ord" if l["y0"] > oh["y0"] else ("tech" if l["y0"] > th["y0"] else None)
        elif th:
            c = "tech" if l["y0"] > th["y0"] else None
        elif oh:
            c = "ord" if l["y0"] > oh["y0"] else None
        l["_c"] = c
    specs = rows_of([l for l in small if l["_c"] == "tech"])
    orders, refs = [], []
    for lab, val in rows_of([l for l in small if l["_c"] == "ord"]):
        if val.startswith("Page"):
            refs.append((lab, val))
        else:
            orders.append((lab, re.sub(r"^.*?No\. ", "", val) if "No." in val else val))
    heads = ("Advantages", "Details", "Features", "Technical data", "Ordering information", "Further details",
             "Use", "Note", "Areas of application", "Making work easy", "Workflow guarantee")
    for l in seg:
        t = clean(l["t"])
        if l["sz"] == 22:
            name.append(t)
        elif l["sz"] == 15:
            typ.append(t)
        elif l["sz"] in (17, 7):
            continue
        elif l["sz"] == 11 and t in heads:
            cur = t
            secs.setdefault(cur, [])
        elif l["sz"] in (10, 11, 12):
            if cur is None and l["sz"] == 12:
                if not ICON.match(t):
                    intro.append(t)
            elif cur in secs and cur not in ("Technical data", "Ordering information"):
                secs[cur].append(t)
    nm = re.sub(r"^NEW\s*", "", join_hyph(name)).strip()
    new = any(l["t"].startswith("NEW") for l in seg if l["sz"] in (17, 22))
    best = None
    for im in raw[pg]["imgs"]:
        if not im["xref"]:
            continue
        ar = im["w"] / im["h"]
        if not (0.6 <= ar <= 1.8) or im["w"] < 250 or im["w"] == 1259 or (im["w"] == 544 and im["h"] in (319, 324)) \
                or (im["w"] == 596 and im["h"] == 305):
            continue
        if im["x0"] < -8 or im["y0"] < -4 or im["x1"] > 600:      # full-bleed background panels
            continue
        cx, cy = (im["x0"] + im["x1"]) / 2, (im["y0"] + im["y1"]) / 2
        b = reg["box"]
        if b[0] <= cx <= b[2] and b[1] <= cy <= b[3]:
            if best is None or im["w"] * im["h"] > best["w"] * best["h"]:
                best = im
    return {
        "page": pg, "name": nm, "type": join_hyph(typ), "new": new, "intro": join_hyph(intro),
        "advantages": bullets(secs.get("Advantages", [])),
        "details": bullets(secs.get("Details", []) + secs.get("Features", []) + secs.get("Use", []) + secs.get("Further details", [])),
        "areas": bullets(secs.get("Areas of application", [])),
        "specs": specs, "orders": orders, "refs": refs,
        "image": {"xref": best["xref"], "w": best["w"], "h": best["h"]} if best else None,
    }


def main():
    doc = pymupdf.open(CATALOG)
    raw = read_pages(doc)
    recs = []
    for pg in range(10, 154):
        if pg in SKIP_PAGES:
            continue
        for reg in regions(raw, pg):
            r = record(raw, pg, reg)
            if r["name"] and r["name"] not in DROP_NAMES and not (pg == 152 and r["name"] == "help:ex"):
                recs.append(r)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(recs, f, ensure_ascii=False, indent=1)
    print(f"{len(recs)} records -> {os.path.normpath(OUT)}")


if __name__ == "__main__":
    sys.exit(main())
