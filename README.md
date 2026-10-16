# Prime Hub Trading website

Static multipage site (HTML, CSS, vanilla JS + GSAP from a CDN). No framework, no build step needed to deploy.

```
index.html                  home page: original layout (css/style.css, js/script.js, js/animations.js) with the new logo and brand colors
about / products / training / service / downloads / contact / 404 .html   new design system (css/theme.css)
css/theme.css               design tokens + shared components (inner pages)
css/products.css            products + downloads UI
js/shell.js                 header, mobile menu, scroll progress, back-to-top, toasts
js/quote.js                 quote list (localStorage) + drawer
js/motion.js                GSAP reveal / counters / magnetic / tilt (honours prefers-reduced-motion)
js/products.js, downloads.js, forms.js, subnav.js
data/                       products.json, brands.json, documents.json, taxonomy.json (+ asset-map.json for the build script)
partials/                   head / header / footer shared by the inner pages
assets/products|brands|downloads|img/{brand,favicon,pages}
scripts/                    asset pipeline and generators (see below)
```

## Local preview

Any static server works. Do not open the files with `file://`, because the catalog loads JSON with `fetch`.

```bash
python3 -m http.server 8000      # then open http://localhost:8000
```

## How to add or change a product

All product data lives in **`data/products.json`**.

1. Add an object (copy an existing one):

```json
{
  "id": "renfert-new-mixer",              // brand slug + kebab-case name, must be unique
  "brand": "renfert",                      // slug from data/brands.json
  "name": "New Mixer", "model": "NM-1",
  "category": "equipment",                 // equipment | material
  "subcategory": "model-prep",             // slug from data/taxonomy.json (max 8 per category)
  "summary": "One line, 140 characters at most.",
  "description": "Two or three sentences.",
  "specs": [{ "label": "Power", "value": "850 W" }],
  "features": ["..."], "applications": ["..."],
  "image": "assets/products/renfert/new-mixer.webp",
  "thumb": "assets/products/renfert/new-mixer-sm.webp",
  "gallery": [],
  "datasheet": "assets/downloads/renfert/renfert-catalog-2023.pdf#page=41",
  "tags": ["mixer"], "chips": ["850 W"], "featured": false
}
```

2. Put the photo in `assets/products/<brand>/` as WebP (about 1200 px wide, plus a 480 px `-sm` copy), **or** let the script export it from the supplier PDF/JPG: add an entry to `data/asset-map.json` (`"<id>": [{"src": "Brand/file.pdf", "page": 12, "xref": 345}]`; other forms: `index`, `nth`, `crop`) and run

```bash
pip install pymupdf pillow
MATERIALS_DIR=/path/to/Materials python3 scripts/build-assets.py
```

3. Reload the site. Counts, filters, brand cards and the "N brands / N products" numbers all update from the JSON (the static footer numbers are refreshed by `scripts/apply-shell.py`, see below).

## How to add a brand

1. Add an object to `data/brands.json` (`slug`, `name`, `country` or `null`, `logo`, `about`, `categories`, `productCount`, `catalogs`). Without a logo file the site shows a text wordmark. Logo files go in `assets/brands/<slug>.webp`.
2. Add its PDFs to `data/documents.json` (`brand`, `title`, `type`: catalog | datasheet | brochure | manual, `lang`, `file`, `pages`, `sizeMB`, `categories`), and copy the PDF into `assets/downloads/<slug>/`.
3. Add products as above, then run `python3 scripts/apply-shell.py` to refresh the generated parts of the pages (brand marquee, brand count, sitemap).

`scripts/provenance/` contains the code that produced the first dataset from the Materials folder (`extract_renfert.py`, `curated.py`, `build_dataset.py`, `audit_materials.py`); run it only if you want to regenerate everything from scratch, because it overwrites hand edits.

## Shared header / footer

`partials/head.html`, `header.html` and `footer.html` are injected into the inner pages between the `<!--SHELL:...-->` markers by

```bash
python3 scripts/apply-shell.py          # SITE_URL=https://your-domain python3 scripts/apply-shell.py
```

The script also sets the active nav link, canonical / Open Graph tags, the brand marquee and brand `<option>` lists, and regenerates `sitemap.xml` and `robots.txt`. Change the domain with `SITE_URL` (default `https://www.primehubeg.com`, please confirm).

## Brand assets

`python3 scripts/make-brand-assets.py` rebuilds the logo sizes, the white logo, the favicon set and the Open Graph image from `assets/img/PrimeHub_Logo.png`.
Brand colours: orange `#FF5506`, blue `#00409C` (tokens in `css/theme.css`).

## Deploy on Vercel

The project is a plain static site (`vercel.json` only adds headers and caching).

- **Git:** push the repo, then in Vercel choose *Add New → Project → Import*, Framework preset **Other**, leave Build Command and Output Directory empty, Root Directory `./`. Every push to `main` deploys.
- **CLI:** `npm i -g vercel && vercel --prod` from the project folder.

`assets/downloads/` holds ~143 MB of PDFs (the JJ Tools catalogue alone is 47 MB). If Vercel rejects the deployment or it gets slow, host the biggest files elsewhere and set `"externalUrl"` on their entry in `data/documents.json`.

## Accessibility and motion

Skip link, landmarks, visible orange focus rings, `aria-current` on the active nav link, keyboard-operable filters, drawer, modal and menu (focus trap, Esc to close), live result counts. All animation honours `prefers-reduced-motion`.
