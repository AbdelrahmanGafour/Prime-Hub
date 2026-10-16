# Performance Baseline — Prime Hub

Date: 2026-10-17 · Commit: 54927ce · No site files were modified to produce this baseline.

## Method and limits
- Lighthouse 12.x CLI, headless Chrome, one run per page/profile (single runs are noisy: expect ±5 points).
- Served by `python3 -m http.server` on localhost. **No compression, no cache headers, no CDN, ~0 ms TTFB.** Transfer sizes are therefore uncompressed (Vercel serves Brotli) and TTFB/cache findings are not representative of production.
- Mobile = Lighthouse default (Moto G Power, slow 4G throttle). Desktop = desktop preset.
- **Not measured:** PageSpeed Insights, GTmetrix, field data (CrUX), INP (needs real interaction; TBT is the lab proxy), production TTFB. These need the live URL (https://www.primehubeg.com) and must be run by hand or via the PSI API; nothing is invented here.
- Fonts column includes Font Awesome webfonts from cdnjs.

## Project inventory
- Static site, deployed on Vercel (`vercel.json`, `.vercel/`). No bundler, no build step for runtime. `package.json` lists `gsap` but it is not used; GSAP is loaded from cdnjs (3.12.5).
- `scripts/*.py` generate product pages, assets and shell partials (`apply-shell.py`, `build-product-pages.py`, ...).
- Pages: 327 HTML — 8 root (`index`, `about`, `products`, `training`, `service`, `downloads`, `contact`, `404`) + 316 product pages in `products/` + 3 partials. Avg product page ≈ 22 KB.
- CSS: `css/theme.css` 50.8 KB (gz 11.5), `css/products.css` 29.6 KB (gz 6.4), `css/style.css` 40.3 KB (gz 7.9, **used only by index.html**). None minified.
- JS (unminified, all local): `products.js` 27.4 KB, `motion.js` 9.0, `forms.js` 8.4, `quote.js` 8.0, `downloads.js` 7.1, `script.js` 6.4, `shell.js` 5.8, `animations.js` 3.7, `product.js` 2.7, `subnav.js` 1.4. Third party: GSAP + ScrollTrigger (cdnjs), Font Awesome CSS (cdnjs, 649 page refs).
- Data: `data/products.json` 555 KB (fetched by products page), plus smaller JSON.
- Images: 597 product WebPs (none >100 KB), brand/partner logos small. `assets/img/Slide1.png` (2.5 MB) and `Slide2.png` (2.7 MB) are unreferenced originals next to the used WebPs (98/143 KB). Page banners have responsive variants.
- Fonts: 8 self-hosted WOFF2 (Inter 400–700, Poppins 500–800) with size-adjusted fallbacks in `theme.css`. Note the four `inter-*.woff2` are all 48,432 bytes, i.e. likely the same file — verify weights actually differ.
- Downloads: 180 MB of PDFs under `assets/downloads/` (on-demand, not on critical path). No video, one SVG (favicon).
- Third-party/analytics: none (no GA/GTM/Pixel/chat). WhatsApp links are plain `wa.me` anchors.
- Headers (`vercel.json`): security headers present; assets cached 7 d, css/js only 1 h (not fingerprinted), data 10 min. No CSP.
- SEO: `robots.txt` allows all, sitemap present (45 KB), canonicals + Product/Breadcrumb JSON-LD on product pages. `404.html` has noindex (expected).

## Lab results (localhost, single run)

| Page | Profile | Perf | A11y | BP | SEO | FCP ms | LCP ms | TBT ms | CLS | SI ms | Req | KB | Img KB | JS KB | CSS KB | Font KB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| index | mobile | **64** | 90 | 100 | 100 | 4441 | 4911 | 1 | 0 | 10253 | 33 | 891 | 390 | 52 | 60 | 358 |
| index | desktop | **61** | 90 | 100 | 100 | 3559 | 3708 | 0 | 0 | 4352 | 35 | 932 | 430 | 51 | 60 | 358 |
| products | mobile | 75 | 100 | 100 | 100 | 2254 | **6153** | 0 | 0 | 2736 | 60 | 1740 | 448 | 91 | 98 | 499 |
| products | desktop | 95 | 100 | 100 | 100 | 523 | 1202 | 0 | 0 | 1563 | 65 | 1885 | 594 | 91 | 98 | 499 |
| product (renfert-silent-ec2) | mobile | 90 | 100 | 100 | 100 | 2253 | 3303 | 0 | 0 | 2253 | 27 | 772 | 82 | 68 | 98 | 499 |
| product | desktop | 100 | 100 | 100 | 100 | 524 | 685 | 0 | 0 | 524 | 30 | 796 | 106 | 68 | 98 | 499 |
| downloads | mobile | 91 | 100 | 100 | 100 | 1953 | 3228 | 0 | 0 | 2010 | 29 | 783 | 72 | 71 | 98 | 499 |
| downloads | desktop | 96 | 100 | 100 | 100 | 524 | 803 | 0 | 0.008 | 1831 | 32 | 889 | 177 | 71 | 98 | 499 |
| contact | mobile | 95 | 100 | 100 | 100 | 1803 | 2778 | 0 | 0 | 2212 | 41 | 820 | 36 | 239 | 69 | 452 |
| contact | desktop | 99 | 100 | 100 | 100 | 484 | 644 | 0 | 0 | 1050 | 41 | 897 | 66 | 239 | 68 | 499 |

Not yet run: about, training, service, 404 (same template as contact/downloads).

## Findings (ranked by impact)

1. **index.html is on the old stack** (`style.css` + `script.js` + `animations.js`), unlike the other 7 pages (`theme.css`, `shell.js`, `motion.js`). It loads Google Fonts (render-blocking, extra origin; Lighthouse "font-display" est. 3,000 ms) in addition to Font Awesome, and its hero is a CSS `background-image` on a div: LCP is not discoverable by the preload scanner, not preloaded, no fetchpriority. Mobile LCP 4.9 s, Speed Index 10.3 s, FCP 4.4 s.
2. **Index a11y 90:** color-contrast, heading-order, select-name failures; also unsized images and 21 uncached resources (cache audit is localhost-skewed).
3. **products.html mobile LCP 6.15 s** (banner `<img>` in `.ph-hero`, 800 w variant). Lab breakdown shows the delay is not network (TTFB/load ≈ 1–4 ms) — likely render delay from the render-blocked Font Awesome/CSS chain or JS-dependent rendering; needs a trace to confirm before changing anything. 65 requests / 1.7 MB incl. the 555 KB `products.json`.
4. **Font Awesome 6.5.1 full CSS + 3 webfonts (~275 KB) on every page**, from a third-party origin, for a handful of icons. Biggest single third-party cost; candidate for an inline SVG sprite or a subset.
5. **GSAP + ScrollTrigger from cdnjs on every page** (2 extra requests + origin). Verify how much of `motion.js` actually needs it.
6. **No minification** of 3 CSS + 10 JS files (est. ~6 KB CSS saving on index alone); `style.css`/`theme.css`/`products.css` contain unused rules (index: ~41 KB unused).
7. **Caching:** css/js only 1 h and not fingerprinted; HTML cache not set. Safe fix is hashed filenames (needs the Python generators updated across 327 pages) or longer TTL with versioned query.
8. **Cleanup:** 5.2 MB unreferenced `Slide*.png`; `gsap` dependency unused; `inter-*` fonts possibly identical; footer/CTA social links are `href="#"` (index).

## Next step proposed
Fix #1 first (migrate index to the shared shell or at minimum: self-hosted fonts, preload + `<img fetchpriority=high>` hero, drop Google Fonts), then re-measure; then #3 after a trace; then #4/#5 and minification. Each step re-measured against this table.
