#!/usr/bin/env python3
"""
Apply the shared inner-page shell (head tags, header, footer, floating UI, scripts) to the six inner pages
and regenerate sitemap.xml / robots.txt. index.html is never touched.

Each page contains three marker pairs that this script fills from partials/:
    <!--SHELL:HEAD--> ... <!--/SHELL:HEAD-->     (inside <head>)
    <!--SHELL:HEADER--> ... <!--/SHELL:HEADER--> (right after <body>)
    <!--SHELL:FOOTER--> ... <!--/SHELL:FOOTER--> (before </body>)

    SITE_URL=https://www.primehubeg.com python3 scripts/apply-shell.py
"""
import datetime, html, json, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE_URL = os.environ.get("SITE_URL", "https://www.primehubeg.com").rstrip("/")
PAGES = ["about", "products", "training", "service", "downloads", "contact"]
SHELL_PAGES = PAGES + ["404"]          # 404 gets the shell but is not listed in the sitemap
read = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()

brands = json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))
products = json.load(open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8"))
VARS = {"SITE_URL": SITE_URL, "BRAND_COUNT": str(len(brands)), "PRODUCT_COUNT": str(len(products))}


def fill(text):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: VARS.get(m.group(1), m.group(0)), text)


def region(name, content):
    return f"<!--SHELL:{name}-->\n{content.rstrip()}\n<!--/SHELL:{name}-->"


def replace_region(page, name, content):
    pat = re.compile(rf"<!--SHELL:{name}-->.*?<!--/SHELL:{name}-->", re.S)
    if not pat.search(page):
        raise SystemExit(f"marker SHELL:{name} missing")
    return pat.sub(lambda m: region(name, content), page)


def logo_size(path):
    try:
        from PIL import Image
        with Image.open(os.path.join(ROOT, path)) as im:
            return im.size
    except Exception:
        return None


def gen_marquee():
    """Brand logos (grayscale -> colour on hover), duplicated once for a seamless loop."""
    def items(hidden):
        out = []
        for b in sorted(brands, key=lambda b: -b["productCount"]):
            href = f"products.html?brand={b['slug']}"
            attrs = ' tabindex="-1"' if hidden else ""
            if b.get("logo"):
                sz = logo_size(b["logo"])
                wh = f' width="{sz[0]}" height="{sz[1]}"' if sz else ""
                inner = f'<img src="{b["logo"]}" alt="{html.escape(b["name"])}"{wh} loading="lazy">'
            else:
                inner = f'<span class="wordmark">{html.escape(b["name"])}</span>'
            out.append(f'<a class="marquee__item" href="{href}" title="{html.escape(b["name"])} products"{attrs}>{inner}</a>')
        return "".join(out)
    return ('<div class="marquee" role="group" aria-label="Authorized brands"><div class="marquee__track">'
            + items(False) + '<span class="marquee__dup" aria-hidden="true" style="display:contents">' + items(True) + '</span></div></div>')


def gen_brand_options():
    opts = ['<option value="" selected disabled>Equipment brand</option>']
    for b in sorted(brands, key=lambda b: b["name"].lower()):
        if "equipment" in b["categories"]:
            opts.append(f'<option value="{html.escape(b["name"])}">{html.escape(b["name"])}</option>')
    opts.append('<option value="Other">Other brand</option>')
    return "".join(opts)


def gen_all_brand_options():
    opts = ['<option value="" selected disabled>Choose a brand (optional)</option>']
    for b in sorted(brands, key=lambda b: b["name"].lower()):
        opts.append(f'<option value="{html.escape(b["name"])}">{html.escape(b["name"])}</option>')
    return "".join(opts)


def gen_product_jsonld():
    """ItemList of representative products (featured + first per brand). No offers or prices (RFQ model)."""
    bmap = {b["slug"]: b for b in brands}
    pick, seen = [], set()
    for p in products:
        if p["featured"] and p["image"]:
            pick.append(p); seen.add(p["id"])
    for b in brands:
        for p in products:
            if p["brand"] == b["slug"] and p["id"] not in seen and p["image"]:
                pick.append(p); seen.add(p["id"]); break
    items = []
    for i, p in enumerate(pick[:30], 1):
        items.append({"@type": "ListItem", "position": i, "item": {
            "@type": "Product", "name": p["name"], "description": p["summary"],
            "brand": {"@type": "Brand", "name": bmap[p["brand"]]["name"]},
            "category": "Dental Equipment" if p["category"] == "equipment" else "Dental Material",
            "image": f"{SITE_URL}/{p['image']}", "url": f"{SITE_URL}/products.html?product={p['id']}"}})
    data = {"@context": "https://schema.org", "@type": "ItemList", "name": "Prime Hub Trading product catalog",
            "numberOfItems": len(products), "itemListElement": items}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


GEN = {"PRODUCT_JSONLD": gen_product_jsonld, "MARQUEE": gen_marquee, "BRAND_OPTIONS": gen_brand_options, "ALL_BRAND_OPTIONS": gen_all_brand_options}


def apply_gen(page):
    for name, fn in GEN.items():
        pat = re.compile(rf"<!--GEN:{name}-->.*?<!--/GEN:{name}-->", re.S)
        page = pat.sub(lambda m: f"<!--GEN:{name}-->{fn()}<!--/GEN:{name}-->", page)
    return page


def main():
    head, header, footer = (fill(read(f"partials/{n}.html")) for n in ("head", "header", "footer"))
    for name in SHELL_PAGES:
        path = os.path.join(ROOT, f"{name}.html")
        page = read(f"{name}.html")
        if "<!--SHELL:HEAD-->" not in page:
            print("skipped (no markers yet):", name)
            continue
        title = html.unescape(re.search(r"<title>(.*?)</title>", page, re.S).group(1).strip())
        desc = html.unescape(re.search(r'<meta name="description" content="(.*?)"', page, re.S).group(1))
        page_head = head + (
            f'\n<link rel="canonical" href="{SITE_URL}/{name}.html">'
            f'\n<meta property="og:url" content="{SITE_URL}/{name}.html">'
            f'\n<meta property="og:title" content="{html.escape(title)}">'
            f'\n<meta property="og:description" content="{html.escape(desc)}">'
        )
        page = replace_region(page, "HEAD", page_head)
        cur = re.search(r'<body[^>]*data-page="(\w+)"', page).group(1)
        h = re.sub(rf'(<a class="nav__link" href="[^"]+" data-nav="{cur}")', r'\1 aria-current="page"', header)
        page = replace_region(page, "HEADER", h)
        page = replace_region(page, "FOOTER", footer)
        page = apply_gen(page)
        cats = {"all": len(products), "equipment": sum(1 for x in products if x["category"] == "equipment"), "material": sum(1 for x in products if x["category"] == "material")}
        for k, v in cats.items():
            page = re.sub(rf'(data-count="{k}">)[^<]*(<)', lambda m, v=v: m.group(1) + str(v) + m.group(2), page)
        for attr, key in (("data-brand-count", "BRAND_COUNT"), ("data-product-count", "PRODUCT_COUNT")):
            def bump(m, key=key):
                tag = re.sub(r'data-counter="[^"]*"', f'data-counter="{VARS[key]}"', m.group(1))
                return tag + VARS[key] + m.group(2)
            page = re.sub(rf"(<[^>]*{attr}[^>]*>)[^<]*(<)", bump, page)
        open(path, "w", encoding="utf-8").write(page)
        print("shell applied:", name)

    today = datetime.date.today().isoformat()
    urls = ["index"] + PAGES
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = f"{SITE_URL}/" if u == "index" else f"{SITE_URL}/{u}.html"
        pr = "1.0" if u == "index" else ("0.9" if u == "products" else "0.7")
        sm.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("sitemap.xml + robots.txt written")


if __name__ == "__main__":
    main()
