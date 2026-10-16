#!/usr/bin/env python3
"""
Generate one static page per product: products/<id>.html  (layout modelled on renfert.com product pages:
breadcrumb, gallery, title + short description, badges, advantages, jump tabs, details, technical data,
variants / order numbers, downloads with PDF preview, related products).

    python3 scripts/build-product-pages.py && python3 scripts/apply-shell.py
Requires data/products.json with `downloads` (scripts/build-product-downloads.py).
"""
import html, json, os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.environ.get("SITE_URL", "https://www.primehubeg.com").rstrip("/")
P = json.load(open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8"))
B = {b["slug"]: b for b in json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))}
T = json.load(open(os.path.join(ROOT, "data", "taxonomy.json"), encoding="utf-8"))
SUB = {s["slug"]: s["label"] for c in T.values() for s in c["sub"]}
CATL = {"equipment": "Dental Equipment", "material": "Dental Material"}
e = html.escape
os.makedirs(os.path.join(ROOT, "products"), exist_ok=True)


def chip_html(p):
    out = [f'<span class="cat-badge cat-badge--{"eq" if p["category"] == "equipment" else "mat"}">{CATL[p["category"]]}</span>',
           f'<span class="chip chip--ghost">{e(SUB[p["subcategory"]])}</span>']
    if p.get("new"):
        out.append('<span class="badge-sq">New</span>')
    for t in p["tags"][:3]:
        if t.lower() != (p["tags"][0] if p["tags"] else "").lower() or True:
            out.append(f'<span class="chip">{e(t)}</span>')
    return "".join(out[:7])


def page(p):
    b = B[p["brand"]]
    imgs = [p["image"]] + (p["gallery"] or []) if p["image"] else []
    sub = p["tags"][0] if (p["brand"] == "renfert" and p["tags"]) else SUB[p["subcategory"]]
    url = f"{SITE}/products/{p['id']}.html"
    logo = (f'<img src="{b["logo"]}" alt="{e(b["name"])}" height="28">' if b.get("logo") else f'<span class="wordmark">{e(b["name"])}</span>')
    # gallery
    if imgs:
        gal = (f'<button class="pd-main" type="button" data-zoom aria-label="Enlarge image"><img id="pdMain" src="{imgs[0]}" alt="{e(b["name"] + " " + p["name"])}" width="900" height="900" fetchpriority="high"><span class="pd-main__zoom"><i class="fa-solid fa-magnifying-glass-plus" aria-hidden="true"></i></span></button>')
        if len(imgs) > 1:
            gal += '<div class="pm__thumbs" role="group" aria-label="Product images">' + "".join(
                f'<button type="button" data-img="{s}" aria-label="Image {i + 1}" aria-current="{str(i == 0).lower()}"><img src="{s}" alt="" loading="lazy"></button>' for i, s in enumerate(imgs)) + "</div>"
    else:
        gal = f'<div class="pd-main pd-main--empty"><span class="p-card__placeholder" style="position:absolute;inset:0">{logo}</span></div>'
    feats = "".join(f"<li>{e(f)}</li>" for f in p["features"][:5])
    dls = p.get("downloads") or []
    primary_dl = dls[0] if dls else None
    tabs = [("details", "Details")]
    if p["specs"]:
        tabs.append(("technical", "Technical data"))
    if p.get("orderNumbers"):
        tabs.append(("variants", "Variants"))
    if dls:
        tabs.append(("downloads", "Downloads"))
    tabs.append(("related", "Related products"))
    tabs_html = "".join(f'<a href="#{i}"{" class=\"is-active\"" if n == 0 else ""}>{l}</a>' for n, (i, l) in enumerate(tabs))
    # details
    det = f'<p class="pd-lead">{e(p["description"] or p["summary"])}</p>'
    if p["features"]:
        det += '<h3 class="h4">Advantages</h3><ul class="bul pd-list">' + "".join(f"<li>{e(f)}</li>" for f in p["features"]) + "</ul>"
    if p["applications"]:
        det += '<h3 class="h4" style="margin-top:22px">Applications</h3><div class="pm__chips">' + "".join(f'<span class="chip">{e(a)}</span>' for a in p["applications"]) + "</div>"
    sections = f'<section class="pd-sec" id="details"><h2 class="pd-h2">Details</h2>{det}</section>'
    if p["specs"]:
        sections += ('<section class="pd-sec" id="technical"><h2 class="pd-h2">Technical data</h2><div class="pd-table"><table class="spec-table"><tbody>'
                     + "".join(f'<tr><th scope="row">{e(s["label"])}</th><td>{e(s["value"])}</td></tr>' for s in p["specs"]) + "</tbody></table></div></section>")
    if p.get("orderNumbers"):
        sections += ('<section class="pd-sec" id="variants"><h2 class="pd-h2">Variants and item numbers</h2><div class="pd-table"><table class="spec-table"><thead><tr><th>Variant</th><th>Item no.</th></tr></thead><tbody>'
                     + "".join(f'<tr><td>{e(o["label"])}</td><td class="tnum">{e(o["no"])}</td></tr>' for o in p["orderNumbers"]) + "</tbody></table></div></section>")
    if dls:
        rows = ""
        for d in dls:
            href = d["file"] + (f'#page={d["page"]}' if d.get("page") else "")
            meta = f'<span class="chip">{e(d["type"])}</span>' + (f'<span>{d["pages"]} page{"s" if d["pages"] != 1 else ""}</span>' if d.get("pages") else "") + \
                (f'<span class="tnum">{d["sizeMB"]} MB</span>' if d.get("sizeMB") else "") + (f'<span>{e(d["lang"])}</span>' if d.get("lang") else "")
            note = f'<span class="pd-dl__note">{e(d["note"])}</span>' if d.get("note") else (f'<span class="pd-dl__note">Product appears on page {d["page"]}</span>' if d.get("page") else "")
            rows += (f'<article class="doc"><span class="doc__icon"><i class="fa-regular fa-file-pdf" aria-hidden="true"></i></span>'
                     f'<div><h3 class="doc__title">{e(d["title"])}</h3><div class="doc__meta">{meta}</div>{note}</div>'
                     f'<div class="doc__actions"><a class="btn btn--primary btn--sm" href="{e(d["file"])}" download="{os.path.basename(d["file"])}"><i class="fa-solid fa-download" aria-hidden="true"></i> Download</a>'
                     f'<button class="btn btn--ghost btn--sm" type="button" data-view="{e(href)}" data-title="{e(d["title"])}"><i class="fa-regular fa-eye" aria-hidden="true"></i> View</button></div></article>')
        sections += (f'<section class="pd-sec" id="downloads"><h2 class="pd-h2">Downloads</h2><div class="doc-list">{rows}</div>'
                     '<div class="pd-viewer" id="pdViewer" hidden><div class="pd-viewer__bar"><strong id="pdViewerTitle"></strong><span><a class="link-arrow" id="pdViewerOpen" href="#" target="_blank" rel="noopener">Open in new tab <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>'
                     '<button class="icon-btn" type="button" id="pdViewerClose" aria-label="Close preview"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></span></div>'
                     '<iframe id="pdFrame" title="PDF preview" loading="lazy"></iframe></div></section>')
    rel = [x for x in P if x["id"] != p["id"] and x["subcategory"] == p["subcategory"]]
    rel.sort(key=lambda x: (x["brand"] != p["brand"], not x["image"], x["name"]))
    cards = ""
    for r in rel[:4]:
        im = (f'<img src="{r["thumb"]}" alt="" loading="lazy" width="480" height="360">' if r["thumb"] else "")
        cards += f'<a class="related-card card" href="products/{r["id"]}.html"><span class="r-img">{im}</span><span class="r-txt">{e(r["name"])}<small>{e(B[r["brand"]]["name"])}</small></span></a>'
    sections += (f'<section class="pd-sec" id="related"><h2 class="pd-h2">Related products</h2>' + (f'<div class="related">{cards}</div>' if cards else "") +
                 f'<p style="margin-top:22px"><a class="link-arrow" href="products.html?category={p["category"]}&amp;sub={p["subcategory"]}">All {e(SUB[p["subcategory"]])} <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p></section>')
    wa = f"Hello Prime Hub Trading, I would like information about {b['name']} {p['name']}" + (f" ({p['model']})" if p["model"] else "") + f". {url}"
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["summary"], "brand": {"@type": "Brand", "name": b["name"]},
          "category": CATL[p["category"]], "url": url, **({"sku": p["model"]} if p["model"] else {}), **({"image": [f"{SITE}/{i}" for i in imgs]} if imgs else {})}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "item": {"@id": SITE + "/", "name": "Home"}},
        {"@type": "ListItem", "position": 2, "item": {"@id": SITE + "/products.html", "name": "Products"}},
        {"@type": "ListItem", "position": 3, "item": {"@id": f"{SITE}/products.html?category={p['category']}", "name": CATL[p["category"]]}},
        {"@type": "ListItem", "position": 4, "item": {"@id": url, "name": p["name"]}}]}
    pdata = {"id": p["id"], "name": p["name"], "model": p["model"], "brandName": b["name"], "thumb": p["thumb"] or "", "wa": wa}
    title = f'{p["name"]} | {b["name"]} | Prime Hub Trading'
    desc = p["summary"]
    dl_btn = ""
    if primary_dl:
        dl_btn = f'<a class="btn btn--primary" href="{e(primary_dl["file"])}" download="{os.path.basename(primary_dl["file"])}"><i class="fa-solid fa-download" aria-hidden="true"></i> Download datasheet</a>'
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<base href="../">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{f'<link rel="preload" as="image" href="{imgs[0]}" fetchpriority="high">' if imgs else ''}
<!--SHELL:HEAD-->
<!--/SHELL:HEAD-->
<link rel="stylesheet" href="css/products.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body class="ph" data-page="products">
<!--SHELL:HEADER-->
<!--/SHELL:HEADER-->
<main id="main">
  <div class="pd-top"><div class="container">
    <nav class="crumbs crumbs--light" aria-label="Breadcrumb"><a href="index.html">Home</a><i class="fa-solid fa-chevron-right" aria-hidden="true"></i><a href="products.html">Products</a><i class="fa-solid fa-chevron-right" aria-hidden="true"></i><a href="products.html?category={p["category"]}">{CATL[p["category"]]}</a><i class="fa-solid fa-chevron-right" aria-hidden="true"></i><a href="products.html?category={p["category"]}&amp;sub={p["subcategory"]}">{e(SUB[p["subcategory"]])}</a><i class="fa-solid fa-chevron-right" aria-hidden="true"></i><span aria-current="page">{e(p["name"])}</span></nav>
  </div></div>
  <section class="pd">
    <div class="container pd__grid">
      <div class="pd__gallery">{gal}</div>
      <div class="pd__info">
        <div class="pd__brand"><a href="products.html?brand={p["brand"]}" aria-label="All {e(b["name"])} products">{logo}</a></div>
        <h1>{e(p["name"])}</h1>
        <p class="pd__sub">{e(sub)}{(" · Model " + e(p["model"])) if p["model"] else ""}</p>
        <p class="pd__short">{e(p["summary"])}</p>
        <div class="pd__badges">{chip_html(p)}</div>
        {f'<ul class="bul pd-list pd__adv">{feats}</ul>' if feats else ''}
        <div class="pd__cta">
          <button class="btn btn--accent btn--lg" type="button" data-add aria-pressed="false"><i class="fa-solid fa-plus" aria-hidden="true"></i> Add to quote</button>
          <a class="btn btn--wa btn--lg" href="https://wa.me/201090009508?text={html.escape(__import__("urllib.parse").parse.quote(wa))}" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Ask on WhatsApp</a>
          {dl_btn}
        </div>
        <p class="pm__note">No prices online. We reply with pricing and availability.</p>
      </div>
    </div>
  </section>
  <nav class="subnav" aria-label="On this page"><div class="container subnav__inner">{tabs_html}</div></nav>
  <div class="ph-section ph-section--surface pd-body"><div class="container pd-body__inner">{sections}</div></div>
  <section class="ph-section ph-section--tight"><div class="container"><div class="cta-band"><div><h2>Interested in {e(p["name"])}?</h2><p>Add it to your quote list or message us. We reply with pricing and availability.</p></div><div class="cta-band__actions"><a class="btn btn--dark btn--lg" href="contact.html?brand={p["brand"]}#quote">Request a quote <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a><a class="btn btn--ghost btn--lg" href="products.html">All products</a></div></div></div></section>
</main>
<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Enlarged product image"><button class="icon-btn lightbox__close" type="button" id="lbClose" aria-label="Close"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button><img id="lbImg" alt=""></div>
<script type="application/json" id="pdata">{json.dumps(pdata, ensure_ascii=False)}</script>
<!--SHELL:FOOTER-->
<!--/SHELL:FOOTER-->
<script src="js/subnav.js" defer></script>
<script src="js/product.js" defer></script>
</body>
</html>
'''
    return out


n = 0
for p in P:
    open(os.path.join(ROOT, "products", p["id"] + ".html"), "w", encoding="utf-8").write(page(p)); n += 1
print(n, "product pages written")
