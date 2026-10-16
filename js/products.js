/* Prime Hub Trading — products page
   Everything is client-side from data/products.json (+ brands, taxonomy, documents).
   URL state: ?category=equipment|material &brand=a,b &sub=x,y &tag=t1,t2 &q=text &sort=featured|az|brand &product=<id>
   Legacy anchors #materials / #cadcam / #consumables are mapped to the new categories. */
(function () {
  'use strict';
  var d = document, PAGE_SIZE = 24;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };

  var DATA = { products: [], brands: [], brandMap: {}, subLabel: {}, subCat: {}, subOrder: [], docByFile: {}, docsByBrand: {} };
  var state = { category: '', brands: [], subs: [], tags: [], q: '', sort: 'featured', product: '', shown: PAGE_SIZE };
  var built = false, lastOpener = null;

  var el = {};
  var SITE_TITLE = 'Prime Hub Trading';
  var BASE_DESC = d.querySelector('meta[name="description"]').getAttribute('content');
  var CAT_LABEL = { equipment: 'Dental Equipment', material: 'Dental Material' };
  var LEGACY = { '#materials': { category: 'material' }, '#cadcam': { category: 'equipment' }, '#consumables': { category: 'material', subs: ['tools-finishing'] } };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function norm(s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
  function uniq(a) { return a.filter(function (v, i) { return a.indexOf(v) === i; }); }
  function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }

  /* ------------------------------------------------------------------ data */
  function load() {
    var f = function (u) { return fetch(u).then(function (r) { if (!r.ok) throw new Error(u); return r.json(); }); };
    return Promise.all([f('data/products.json'), f('data/brands.json'), f('data/taxonomy.json'), f('data/documents.json')]).then(function (r) {
      DATA.products = r[0]; DATA.brands = r[1];
      DATA.brands.forEach(function (b) { DATA.brandMap[b.slug] = b; });
      Object.keys(r[2]).forEach(function (cat) { r[2][cat].sub.forEach(function (s) { DATA.subLabel[s.slug] = s.label; DATA.subCat[s.slug] = cat; DATA.subOrder.push(s.slug); }); });
      r[3].forEach(function (doc) {
        DATA.docByFile[doc.file] = doc;
        (DATA.docsByBrand[doc.brand] = DATA.docsByBrand[doc.brand] || []).push(doc);
      });
      DATA.products.forEach(function (p, i) {
        p._i = i; p._b = DATA.brandMap[p.brand]; p._n = norm(p.name);
        p._tags = (p.tags || []).map(norm);
        p._idx = norm([p.name, p.model, p._b.name, (p.tags || []).join(' '), DATA.subLabel[p.subcategory]].join(' '));
      });
    });
  }

  /* ------------------------------------------------------------------ url state */
  function parse() {
    var qs = new URLSearchParams(location.search), s = { category: '', brands: [], subs: [], tags: [], q: '', sort: 'featured', product: '', shown: PAGE_SIZE };
    var c = qs.get('category'); if (c === 'equipment' || c === 'material') s.category = c;
    if (qs.get('brand')) s.brands = qs.get('brand').split(',').filter(function (b) { return DATA.brandMap[b]; });
    if (qs.get('sub')) s.subs = qs.get('sub').split(',').filter(function (b) { return DATA.subLabel[b]; });
    if (qs.get('tag')) s.tags = qs.get('tag').split(',').map(norm).filter(Boolean);
    s.q = (qs.get('q') || '').slice(0, 80);
    var so = qs.get('sort'); if (so === 'az' || so === 'brand') s.sort = so;
    var pr = qs.get('product'); if (pr && DATA.products.some(function (p) { return p.id === pr; })) s.product = pr;
    return s;
  }
  function serialize(s) {
    var qs = new URLSearchParams();
    if (s.category) qs.set('category', s.category);
    if (s.brands.length) qs.set('brand', s.brands.join(','));
    if (s.subs.length) qs.set('sub', s.subs.join(','));
    if (s.tags.length) qs.set('tag', s.tags.join(','));
    if (s.q) qs.set('q', s.q);
    if (s.sort !== 'featured') qs.set('sort', s.sort);
    if (s.product) qs.set('product', s.product);
    var str = qs.toString();
    return location.pathname + (str ? '?' + str : '') + (location.hash === '#brands' && !str ? '' : '');
  }
  function commit(replace) {
    var url = serialize(state);
    try { history[replace ? 'replaceState' : 'pushState']({ ph: 1 }, '', url); } catch (e) {}
    seo();
  }

  /* ------------------------------------------------------------------ SEO (title, description, canonical per view) */
  function setMeta(sel, attr, val) { var m = $(sel); if (m) m.setAttribute(attr, val); }
  function seo() {
    var title = 'Products', desc = BASE_DESC, p = state.product && DATA.products.filter(function (x) { return x.id === state.product; })[0];
    if (p) { title = p.name + ' - ' + p._b.name; desc = p.summary; }
    else {
      var parts = [];
      if (state.brands.length === 1) parts.push(DATA.brandMap[state.brands[0]].name);
      if (state.category) parts.push(CAT_LABEL[state.category]);
      if (state.subs.length === 1) parts.push(DATA.subLabel[state.subs[0]]);
      if (state.q) parts.push('Search: ' + state.q);
      if (parts.length) {
        title = parts.join(' · ') + ' Products';
        desc = 'Browse ' + parts.join(', ') + ' from Prime Hub Trading, authorized distributor of dental laboratory equipment and materials in Egypt. Request a quote online.';
      }
    }
    var full = title + ' | ' + SITE_TITLE;
    d.title = full;
    setMeta('meta[name="description"]', 'content', desc);
    setMeta('meta[property="og:title"]', 'content', full);
    setMeta('meta[property="og:description"]', 'content', desc);
    var can = $('link[rel="canonical"]'), base = can ? can.getAttribute('href').split('?')[0] : '';
    if (can) can.setAttribute('href', base + (p ? '?product=' + p.id : ''));
    setMeta('meta[property="og:url"]', 'content', base + (p ? '?product=' + p.id : ''));
  }

  /* ------------------------------------------------------------------ filtering */
  function matches(p, ex) {
    if (state.category && ex !== 'category' && p.category !== state.category) return false;
    if (state.subs.length && ex !== 'sub' && state.subs.indexOf(p.subcategory) < 0) return false;
    if (state.brands.length && ex !== 'brand' && state.brands.indexOf(p.brand) < 0) return false;
    if (state.tags.length && ex !== 'tag') { for (var i = 0; i < state.tags.length; i++) if (p._tags.indexOf(state.tags[i]) < 0) return false; }
    if (state.q) { var terms = norm(state.q).split(/\s+/).filter(Boolean); for (var j = 0; j < terms.length; j++) if (p._idx.indexOf(terms[j]) < 0) return false; }
    return true;
  }
  function facet(ex, key) {
    var out = {};
    DATA.products.forEach(function (p) { if (matches(p, ex)) { var k = key(p); out[k] = (out[k] || 0) + 1; } });
    return out;
  }
  function sortList(list) {
    var mode = state.sort;
    if (mode === 'az') return list.slice().sort(function (a, b) { return a._n.localeCompare(b._n); });
    if (mode === 'brand') return list.slice().sort(function (a, b) { return a._b.name.localeCompare(b._b.name) || a._n.localeCompare(b._n); });
    var feat = list.filter(function (p) { return p.featured; });
    var rest = list.filter(function (p) { return !p.featured; });
    var byBrand = {}; rest.forEach(function (p) { (byBrand[p.brand] = byBrand[p.brand] || []).push(p); });
    var order = Object.keys(byBrand).sort(function (a, b) { return byBrand[b].length - byBrand[a].length; });
    order.forEach(function (b) { byBrand[b].sort(function (x, y) { return (y.image ? 1 : 0) - (x.image ? 1 : 0) || x._i - y._i; }); });
    var out = feat.slice(), i = 0, more = true;
    while (more) { more = false; order.forEach(function (b) { if (byBrand[b][i]) { out.push(byBrand[b][i]); more = true; } }); i++; }
    return out;
  }

  /* ------------------------------------------------------------------ renderers */
  function brandChip(p) {
    var b = p._b;
    return b.logo ? '<img src="' + esc(b.logo) + '" alt="' + esc(b.name) + '" height="20" loading="lazy" decoding="async">' : '<span>' + esc(b.name) + '</span>';
  }
  function mediaHtml(p) {
    if (p.thumb) return '<img src="' + esc(p.thumb) + '" alt="' + esc(p._b.name + ' ' + p.name) + '" width="480" height="360" loading="lazy" decoding="async">';
    var b = p._b;
    return '<span class="p-card__placeholder">' + (b.logo ? '<img src="' + esc(b.logo) + '" alt="" loading="lazy">' : '<span>' + esc(b.name) + '</span>') + '</span>';
  }
  function cardHtml(p) {
    var inQ = window.PHQuote && PHQuote.has(p.id);
    var sub = DATA.subLabel[p.subcategory];
    return '<article class="p-card" data-id="' + esc(p.id) + '" data-tilt>' +
      '<button class="p-card__media" type="button" data-open tabindex="-1" aria-hidden="true">' + mediaHtml(p) +
      '</button>' +
      '<span class="p-card__cat"><span class="cat-badge cat-badge--' + (p.category === 'equipment' ? 'eq' : 'mat') + '">' + (p.category === 'equipment' ? 'Equipment' : 'Material') + '</span></span>' +
      (p.new ? '<span class="p-card__new badge-sq">New</span>' : '') +
      '<div class="p-card__body">' +
      '<div class="p-card__brand">' + brandChip(p) + '</div>' +
      '<h3><button type="button" data-open>' + esc(p.name) + '</button></h3>' +
      '<p class="p-card__sub">' + esc(p.model ? 'Model ' + p.model : sub) + '</p>' +
      '<p class="p-card__sum">' + esc(p.summary) + '</p>' +
      (p.chips && p.chips.length ? '<ul class="p-card__chips">' + p.chips.map(function (c) { return '<li>' + esc(c) + '</li>'; }).join('') + '</ul>' : '') +
      '<div class="p-card__actions"><button class="btn btn--ghost btn--sm" type="button" data-open aria-label="Details: ' + esc(p.name) + '">Details</button>' +
      '<button class="btn btn--primary btn--sm" type="button" data-add aria-pressed="' + (inQ ? 'true' : 'false') + '" aria-label="' + (inQ ? 'Remove from quote: ' : 'Add to quote: ') + esc(p.name) + '">' + (inQ ? '<i class="fa-solid fa-check" aria-hidden="true"></i> Added' : '<i class="fa-solid fa-plus" aria-hidden="true"></i> Add to quote') + '</button></div>' +
      '</div></article>';
  }

  var list = [];           // current filtered + sorted list
  function renderGrid(reset) {
    list = sortList(DATA.products.filter(function (p) { return matches(p); }));
    var grid = el.grid;
    grid.setAttribute('aria-busy', 'false');
    if (reset) state.shown = Math.max(PAGE_SIZE, Math.min(state.shown, list.length));
    var slice = list.slice(0, state.shown);
    grid.innerHTML = slice.map(cardHtml).join('');
    var nodes = $$('.p-card', grid);
    if (window.PHMotion && PHMotion.swap && !reduce) PHMotion.swap(nodes);
    el.empty.hidden = list.length > 0; grid.hidden = list.length === 0;
    var rest = list.length - slice.length;
    el.more.hidden = rest <= 0;
    el.moreCount.textContent = 'Showing ' + slice.length + ' of ' + list.length;
    el.loadMore.innerHTML = 'Load ' + Math.min(PAGE_SIZE, rest) + ' more <i class="fa-solid fa-arrow-down" aria-hidden="true"></i>';
    var ctx = [];
    if (state.category) ctx.push(CAT_LABEL[state.category]);
    if (state.brands.length) ctx.push(state.brands.map(function (b) { return DATA.brandMap[b].name; }).join(', '));
    el.count.innerHTML = list.length ? 'Showing <strong>' + slice.length + '</strong> of <strong>' + list.length + '</strong> ' + (list.length === 1 ? 'product' : 'products') + (ctx.length ? ' <span>· ' + esc(ctx.join(' · ')) + '</span>' : '') : 'No products found';
    if (window.PHMotion) setTimeout(PHMotion.refresh, 350);
  }
  function appendMore() {
    var from = state.shown; state.shown += PAGE_SIZE;
    var slice = list.slice(from, state.shown);
    var tmp = d.createElement('div'); tmp.innerHTML = slice.map(cardHtml).join('');
    var nodes = $$('.p-card', tmp); nodes.forEach(function (n) { el.grid.appendChild(n); });
    if (window.PHMotion && PHMotion.swap && !reduce) PHMotion.swap(nodes);
    var rest = list.length - Math.min(state.shown, list.length);
    el.more.hidden = rest <= 0;
    el.moreCount.textContent = 'Showing ' + Math.min(state.shown, list.length) + ' of ' + list.length;
    el.loadMore.innerHTML = 'Load ' + Math.min(PAGE_SIZE, rest) + ' more <i class="fa-solid fa-arrow-down" aria-hidden="true"></i>';
    el.count.innerHTML = 'Showing <strong>' + Math.min(state.shown, list.length) + '</strong> of <strong>' + list.length + '</strong> products';
    var first = nodes[0]; if (first) { var b = $('h3 button', first); if (b) b.focus({ preventScroll: true }); }
  }

  function renderCats() {
    var c = facet('category', function (p) { return p.category; });
    var all = (c.equipment || 0) + (c.material || 0);
    $$('.cat-tile', el.catSwitch).forEach(function (t) {
      var v = t.getAttribute('data-cat');
      t.setAttribute('aria-checked', String(v === state.category));
      t.tabIndex = (v === state.category) ? 0 : -1;
      $('.cat-tile__count', t).textContent = v ? (c[v] || 0) : all;
    });
  }

  function buildBrandRail() {
    var items = DATA.brands.slice().sort(function (a, b) { return b.productCount - a.productCount || a.name.localeCompare(b.name); });
    el.rail.innerHTML = items.map(function (b) {
      return '<li><button class="brand-card" type="button" data-brand="' + esc(b.slug) + '" aria-pressed="false">' +
        '<span class="brand-card__logo">' + (b.logo ? '<img src="' + esc(b.logo) + '" alt="" loading="lazy" height="36">' : '<span class="wordmark">' + esc(b.name) + '</span>') + '</span>' +
        '<span class="brand-card__meta"><span class="brand-card__n"><b class="tnum" data-n>0</b> <span>products</span></span>' +
        '<span class="brand-card__badges">' + b.categories.map(function (c) { return '<span class="mini-badge mini-badge--' + (c === 'equipment' ? 'eq' : 'mat') + '">' + (c === 'equipment' ? 'Equipment' : 'Material') + '</span>'; }).join('') + '</span></span></button></li>';
    }).join('');
  }
  function renderBrandRail() {
    var c = facet('brand', function (p) { return p.brand; });
    $$('.brand-card', el.rail).forEach(function (b) {
      var slug = b.getAttribute('data-brand');
      b.setAttribute('aria-pressed', String(state.brands.indexOf(slug) >= 0));
      $('[data-n]', b).textContent = c[slug] || 0;
      b.classList.toggle('is-empty', (c[slug] || 0) === 0 && state.brands.indexOf(slug) < 0);
    });
    var h = el.brandHead;
    if (state.brands.length === 1) {
      var b = DATA.brandMap[state.brands[0]], docs = DATA.docsByBrand[b.slug] || [];
      h.hidden = false;
      h.innerHTML = '<div class="brand-head__logo">' + (b.logo ? '<img src="' + esc(b.logo) + '" alt="' + esc(b.name) + '">' : '<span class="wordmark">' + esc(b.name) + '</span>') + '</div>' +
        '<div><h3>' + esc(b.name) + '</h3><p>' + esc(b.about) + '</p>' +
        '<div class="brand-head__meta">' + b.categories.map(function (c) { return '<span class="mini-badge mini-badge--' + (c === 'equipment' ? 'eq' : 'mat') + '">' + (c === 'equipment' ? 'Equipment' : 'Material') + '</span>'; }).join('') +
        '<span class="chip chip--ghost">' + plural(b.productCount, 'product') + '</span>' + (b.country ? '<span class="chip chip--ghost"><i class="fa-solid fa-location-dot" aria-hidden="true"></i>' + esc(b.country) + '</span>' : '') + '</div>' +
        (docs.length ? '<div class="brand-head__docs">' + docs.slice(0, 4).map(function (dc) { return '<a href="' + esc(dc.file) + '" target="_blank" rel="noopener"><i class="fa-regular fa-file-pdf" aria-hidden="true"></i>' + esc(dc.title) + ' <small>' + (dc.sizeMB ? dc.sizeMB + ' MB' : '') + '</small></a>'; }).join('') + (docs.length > 4 ? '<a href="downloads.html?brand=' + esc(b.slug) + '">All ' + docs.length + ' documents</a>' : '') + '</div>' : '') + '</div>' +
        '<div class="brand-head__cta"><a class="btn btn--accent" href="contact.html?brand=' + esc(b.slug) + '#quote">Request quote for ' + esc(b.name) + '</a><button class="btn btn--ghost btn--sm" type="button" data-clear-brand>Show all brands</button></div>';
    } else { h.hidden = true; h.innerHTML = ''; }
  }

  function buildFilters() {
    var body = el.filtersBody, html = '';
    // sub-categories
    html += '<details class="fgroup" open data-group="sub"><summary>Sub-category</summary><div class="fgroup__list">';
    ['equipment', 'material'].forEach(function (cat) {
      html += '<div class="fgroup__sub" data-subhead="' + cat + '">' + CAT_LABEL[cat] + '</div>';
      DATA.subOrder.filter(function (s) { return DATA.subCat[s] === cat; }).forEach(function (s) {
        html += '<label class="fcheck" data-sub-row="' + cat + '"><input type="checkbox" data-f="sub" value="' + s + '"><span class="fcheck__label">' + esc(DATA.subLabel[s]) + '</span><span class="fcheck__n tnum" data-n>0</span></label>';
      });
    });
    html += '</div></details>';
    // brands
    html += '<details class="fgroup" open data-group="brand"><summary>Brand</summary>' +
      '<div class="fsearch"><label class="sr-only" for="brandFilter">Filter brands</label><input class="input" id="brandFilter" type="search" placeholder="Find a brand" autocomplete="off"></div><div class="fgroup__list">';
    DATA.brands.slice().sort(function (a, b) { return b.productCount - a.productCount || a.name.localeCompare(b.name); }).forEach(function (b) {
      html += '<label class="fcheck" data-brand-row="' + esc(norm(b.name)) + '"><input type="checkbox" data-f="brand" value="' + esc(b.slug) + '"><span class="fcheck__label">' + esc(b.name) + '</span><span class="fcheck__n tnum" data-n>0</span></label>';
    });
    html += '</div></details>';
    // tags
    var freq = {}, label = {};
    DATA.products.forEach(function (p) { (p.tags || []).forEach(function (t) { var k = norm(t); if (k.length < 3) return; freq[k] = (freq[k] || 0) + 1; label[k] = label[k] || t; }); });
    var top = Object.keys(freq).sort(function (a, b) { return freq[b] - freq[a]; }).slice(0, 20);
    html += '<details class="fgroup" data-group="tag"><summary>Popular tags</summary><div class="tagcloud">' +
      top.map(function (k) { return '<button type="button" data-tag="' + esc(k) + '" aria-pressed="false">' + esc(label[k]) + '</button>'; }).join('') + '</div></details>';
    body.innerHTML = html;
    var bf = $('#brandFilter', body);
    bf.addEventListener('input', function () {
      var t = norm(bf.value);
      $$('[data-brand-row]', body).forEach(function (r) { r.style.display = !t || r.getAttribute('data-brand-row').indexOf(t) >= 0 ? '' : 'none'; });
    });
  }
  function renderFilters() {
    var cs = facet('sub', function (p) { return p.subcategory; }), cb = facet('brand', function (p) { return p.brand; });
    $$('[data-f="sub"]', el.filtersBody).forEach(function (i) {
      i.checked = state.subs.indexOf(i.value) >= 0;
      var n = cs[i.value] || 0, row = i.closest('.fcheck'); $('[data-n]', row).textContent = n; row.classList.toggle('is-zero', n === 0 && !i.checked);
      var cat = DATA.subCat[i.value]; row.style.display = (state.category && state.category !== cat) ? 'none' : '';
    });
    $$('[data-subhead]', el.filtersBody).forEach(function (h) { h.style.display = (state.category && state.category !== h.getAttribute('data-subhead')) ? 'none' : ''; });
    $$('[data-f="brand"]', el.filtersBody).forEach(function (i) {
      i.checked = state.brands.indexOf(i.value) >= 0;
      var n = cb[i.value] || 0, row = i.closest('.fcheck'); $('[data-n]', row).textContent = n; row.classList.toggle('is-zero', n === 0 && !i.checked);
    });
    $$('[data-tag]', el.filtersBody).forEach(function (b) { b.setAttribute('aria-pressed', String(state.tags.indexOf(b.getAttribute('data-tag')) >= 0)); });
    var n = state.subs.length + state.brands.length + state.tags.length + (state.category ? 1 : 0);
    el.filtersN.textContent = n; el.filtersN.hidden = n === 0;
  }
  function renderActive() {
    var chips = [];
    if (state.category) chips.push(['category', state.category, CAT_LABEL[state.category]]);
    state.brands.forEach(function (b) { chips.push(['brand', b, DATA.brandMap[b].name]); });
    state.subs.forEach(function (s) { chips.push(['sub', s, DATA.subLabel[s]]); });
    state.tags.forEach(function (t) { chips.push(['tag', t, '#' + t]); });
    if (state.q) chips.push(['q', '', '“' + state.q + '”']);
    el.active.innerHTML = chips.map(function (c) { return '<li><button type="button" data-rm="' + c[0] + '" data-val="' + esc(c[1]) + '" aria-label="Remove filter ' + esc(c[2]) + '">' + esc(c[2]) + ' <i class="fa-solid fa-xmark" aria-hidden="true"></i></button></li>'; }).join('');
    el.clearAll.hidden = chips.length === 0;
    el.qClear.hidden = !state.q;
    if (el.q.value !== state.q) el.q.value = state.q;
    el.sort.value = state.sort;
  }

  function renderAll(opts) {
    opts = opts || {};
    renderCats(); renderBrandRail(); renderFilters(); renderActive(); renderGrid(opts.reset !== false);
  }

  /* ------------------------------------------------------------------ state mutations */
  function change(mut, replace) {
    mut(state); state.shown = PAGE_SIZE; state.product = '';
    // keep sub-categories consistent with the chosen category
    if (state.category) state.subs = state.subs.filter(function (s) { return DATA.subCat[s] === state.category; });
    commit(replace); renderAll({ reset: true });
  }
  function resetAll() { change(function (s) { s.category = ''; s.brands = []; s.subs = []; s.tags = []; s.q = ''; }); }

  /* ------------------------------------------------------------------ product modal */
  var modal, panel, content;
  function focusables() { return $$('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])', panel).filter(function (e) { return e.offsetParent !== null; }); }

  function modalHtml(p) {
    var imgs = [p.image].concat(p.gallery || []).filter(Boolean);
    var doc = p.datasheet && DATA.docByFile[p.datasheet.split('#')[0]];
    var dsLabel = '';
    if (doc) {
      var cat = doc.type === 'catalog';
      dsLabel = (cat && p.sourcePage ? 'Catalog page ' + p.sourcePage : (cat ? 'Catalog' : 'Datasheet')) + ' (PDF' + (doc.sizeMB ? ', ' + doc.sizeMB + ' MB' : '') + ')';
    }
    var inQ = window.PHQuote && PHQuote.has(p.id);
    var related = DATA.products.filter(function (x) { return x.id !== p.id && x.subcategory === p.subcategory; })
      .sort(function (a, b) { return (b.brand === p.brand) - (a.brand === p.brand) || (b.image ? 1 : 0) - (a.image ? 1 : 0); }).slice(0, 4);
    var wa = 'Hello Prime Hub Trading, I would like information about ' + p._b.name + ' ' + p.name + (p.model ? ' (' + p.model + ')' : '') + '. ' + location.origin + location.pathname + '?product=' + p.id;
    var h = '<div class="pm">' +
      '<div class="pm__gallery"><div class="pm__main" id="pmMain">' + (imgs.length ? '<img src="' + esc(imgs[0]) + '" alt="' + esc(p._b.name + ' ' + p.name) + '" width="900" height="900">' : '<span class="p-card__placeholder" style="aspect-ratio:1">' + (p._b.logo ? '<img src="' + esc(p._b.logo) + '" alt="">' : '<span>' + esc(p._b.name) + '</span>') + '</span>') + '</div>' +
      (imgs.length > 1 ? '<div class="pm__thumbs" role="group" aria-label="Product images">' + imgs.map(function (s, i) { return '<button type="button" data-img="' + esc(s) + '" aria-label="Image ' + (i + 1) + '" aria-current="' + (i === 0) + '"><img src="' + esc(s) + '" alt="" loading="lazy"></button>'; }).join('') + '</div>' : '') + '</div>' +
      '<div class="pm__info"><div class="pm__top">' + (p._b.logo ? '<img src="' + esc(p._b.logo) + '" alt="' + esc(p._b.name) + '">' : '<span class="wordmark">' + esc(p._b.name) + '</span>') +
      '<span class="cat-badge cat-badge--' + (p.category === 'equipment' ? 'eq' : 'mat') + '">' + CAT_LABEL[p.category] + '</span><span class="chip chip--ghost">' + esc(DATA.subLabel[p.subcategory]) + '</span>' + (p.new ? '<span class="badge-sq">New</span>' : '') + '</div>' +
      '<h2 id="pmTitle">' + esc(p.name) + '</h2>' + (p.model ? '<p class="pm__model">Model ' + esc(p.model) + '</p>' : '') +
      '<p class="pm__desc">' + esc(p.description || p.summary) + '</p>' +
      '<div class="pm__cta"><button class="btn btn--accent" type="button" data-add aria-pressed="' + (inQ ? 'true' : 'false') + '">' + (inQ ? '<i class="fa-solid fa-check" aria-hidden="true"></i> In your quote list' : '<i class="fa-solid fa-plus" aria-hidden="true"></i> Add to quote') + '</button>' +
      '<a class="btn btn--wa" href="' + PH.waLink(wa) + '" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Ask on WhatsApp</a>' +
      (p.datasheet ? '<a class="btn btn--ghost" href="' + esc(p.datasheet) + '" target="_blank" rel="noopener"><i class="fa-regular fa-file-pdf" aria-hidden="true"></i> ' + esc(dsLabel || 'Datasheet') + '</a>' : '') + '</div>' +
      '<p class="pm__note">No prices online. We reply with pricing and availability.</p></div>';
    if (p.specs && p.specs.length) h += '<section class="pm__section"><h3>Specifications</h3><table class="spec-table"><tbody>' + p.specs.map(function (s) { return '<tr><th scope="row">' + esc(s.label) + '</th><td>' + esc(s.value) + '</td></tr>'; }).join('') + '</tbody></table></section>';
    if ((p.features && p.features.length) || (p.applications && p.applications.length)) {
      h += '<section class="pm__section pm__lists">' +
        (p.features && p.features.length ? '<div><h3>Features</h3><ul class="bul">' + p.features.map(function (f) { return '<li>' + esc(f) + '</li>'; }).join('') + '</ul></div>' : '') +
        (p.applications && p.applications.length ? '<div><h3>Applications</h3><div class="pm__chips">' + p.applications.map(function (a) { return '<span class="chip">' + esc(a) + '</span>'; }).join('') + '</div></div>' : '') + '</section>';
    }
    if (p.orderNumbers && p.orderNumbers.length) h += '<section class="pm__section"><h3>Order numbers</h3><table class="spec-table"><tbody>' + p.orderNumbers.slice(0, 12).map(function (o) { return '<tr><th scope="row">' + esc(o.label) + '</th><td>No. ' + esc(o.no) + '</td></tr>'; }).join('') + '</tbody></table></section>';
    if (related.length) h += '<section class="pm__section"><h3>Related products</h3><div class="related">' + related.map(function (r) {
      return '<button type="button" data-rel="' + esc(r.id) + '"><span class="r-img">' + (r.thumb ? '<img src="' + esc(r.thumb) + '" alt="" loading="lazy">' : '') + '</span><span class="r-txt">' + esc(r.name) + '<small>' + esc(r._b.name) + '</small></span></button>';
    }).join('') + '</div></section>';
    return h + '</div>';
  }

  function openProduct(id, opts) {
    opts = opts || {};
    var p = DATA.products.filter(function (x) { return x.id === id; })[0]; if (!p) return;
    var wasOpen = !modal.hidden;
    if (!wasOpen) lastOpener = d.activeElement;
    state.product = id;
    content.innerHTML = modalHtml(p);
    modal.hidden = false; modal.setAttribute('aria-hidden', 'false'); d.body.classList.add('no-scroll');
    panel.scrollTop = 0; panel.focus({ preventScroll: true });
    if (!opts.fromPop) { try { history[wasOpen ? 'replaceState' : 'pushState']({ ph: 1, modal: 1 }, '', serialize(state)); } catch (e) {} }
    seo();
  }
  function closeProduct(opts) {
    opts = opts || {};
    if (modal.hidden) return;
    modal.hidden = true; modal.setAttribute('aria-hidden', 'true'); d.body.classList.remove('no-scroll');
    state.product = '';
    if (!opts.fromPop) {
      if (history.state && history.state.modal) { history.back(); } else { try { history.replaceState({ ph: 1 }, '', serialize(state)); } catch (e) {} seo(); }
    } else seo();
    var o = lastOpener; lastOpener = null;
    if (o && d.contains(o) && o.focus) o.focus({ preventScroll: true });
  }

  function toggleQuote(id) {
    if (!window.PHQuote) return;
    var p = DATA.products.filter(function (x) { return x.id === id; })[0]; if (!p) return;
    if (PHQuote.has(id)) { PHQuote.remove(id); if (window.PH) PH.toast('Removed from your quote list'); }
    else {
      PHQuote.add({ id: p.id, name: p.name, model: p.model, brandName: p._b.name, thumb: p.thumb });
      if (window.PH) PH.toast('Added to your quote list', 'View list', function () { PHQuote.open(); });
    }
  }
  function syncAdd() {
    $$('.p-card[data-id]').forEach(function (c) {
      var id = c.getAttribute('data-id'), inQ = PHQuote.has(id), b = $('[data-add]', c); if (!b) return;
      var p = DATA.products.filter(function (x) { return x.id === id; })[0];
      b.setAttribute('aria-pressed', String(inQ));
      b.setAttribute('aria-label', (inQ ? 'Remove from quote: ' : 'Add to quote: ') + (p ? p.name : ''));
      b.innerHTML = inQ ? '<i class="fa-solid fa-check" aria-hidden="true"></i> Added' : '<i class="fa-solid fa-plus" aria-hidden="true"></i> Add to quote';
    });
    if (!modal.hidden && state.product) {
      var mb = $('[data-add]', content), inM = PHQuote.has(state.product);
      if (mb) { mb.setAttribute('aria-pressed', String(inM)); mb.innerHTML = inM ? '<i class="fa-solid fa-check" aria-hidden="true"></i> In your quote list' : '<i class="fa-solid fa-plus" aria-hidden="true"></i> Add to quote'; }
    }
  }

  /* ------------------------------------------------------------------ filters sheet (mobile) */
  var sheetOpen = false;
  function setSheet(v) {
    sheetOpen = v; el.filters.classList.toggle('is-open', v); el.filtersOverlay.classList.toggle('is-on', v);
    el.filtersOpen.setAttribute('aria-expanded', String(v)); d.body.classList.toggle('no-scroll', v || !modal.hidden);
    if (v) { var f = $('input,button', el.filtersBody); if (f) f.focus({ preventScroll: true }); } else if (window.matchMedia('(max-width:1000px)').matches) el.filtersOpen.focus({ preventScroll: true });
  }

  /* ------------------------------------------------------------------ events */
  function bind() {
    // category radiogroup
    el.catSwitch.addEventListener('click', function (e) { var t = e.target.closest('.cat-tile'); if (t) change(function (s) { s.category = t.getAttribute('data-cat'); }); });
    el.catSwitch.addEventListener('keydown', function (e) {
      var tiles = $$('.cat-tile', el.catSwitch), i = tiles.indexOf(d.activeElement);
      if (i < 0) return;
      var n = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? (i + 1) % tiles.length : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? (i - 1 + tiles.length) % tiles.length : -1;
      if (n >= 0) { e.preventDefault(); tiles[n].focus(); tiles[n].click(); }
    });
    // brand rail
    el.rail.addEventListener('click', function (e) {
      var b = e.target.closest('.brand-card'); if (!b) return;
      var slug = b.getAttribute('data-brand'), on = state.brands.length === 1 && state.brands[0] === slug;
      change(function (s) { s.brands = on ? [] : [slug]; });
      if (!on) { var c = $('#catalog'); if (c && c.getBoundingClientRect().top > window.innerHeight * .75) c.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }
    });
    el.brandHead.addEventListener('click', function (e) { if (e.target.closest('[data-clear-brand]')) change(function (s) { s.brands = []; }); });
    // sidebar
    el.filtersBody.addEventListener('change', function (e) {
      var i = e.target.closest('[data-f]'); if (!i) return;
      var key = i.getAttribute('data-f') === 'sub' ? 'subs' : 'brands';
      change(function (s) { var a = s[key].slice(); var k = a.indexOf(i.value); if (i.checked && k < 0) a.push(i.value); if (!i.checked && k >= 0) a.splice(k, 1); s[key] = a; });
    });
    el.filtersBody.addEventListener('click', function (e) {
      var t = e.target.closest('[data-tag]'); if (!t) return;
      var v = t.getAttribute('data-tag'); change(function (s) { var a = s.tags.slice(), k = a.indexOf(v); if (k >= 0) a.splice(k, 1); else a.push(v); s.tags = a; });
    });
    // search (debounced) + sort
    var timer;
    el.q.addEventListener('input', function () {
      clearTimeout(timer); var v = el.q.value.trim();
      timer = setTimeout(function () { if (v === state.q) return; change(function (s) { s.q = v; }, true); }, 170);
      el.qClear.hidden = !el.q.value;
    });
    el.q.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); clearTimeout(timer); change(function (s) { s.q = el.q.value.trim(); }, true); } });
    el.qClear.addEventListener('click', function () { el.q.value = ''; change(function (s) { s.q = ''; }); el.q.focus(); });
    el.sort.addEventListener('change', function () { change(function (s) { s.sort = el.sort.value; }); });
    // active chips + clear
    el.active.addEventListener('click', function (e) {
      var b = e.target.closest('[data-rm]'); if (!b) return; var k = b.getAttribute('data-rm'), v = b.getAttribute('data-val');
      change(function (s) {
        if (k === 'category') s.category = ''; else if (k === 'q') s.q = '';
        else { var key = k === 'brand' ? 'brands' : k === 'sub' ? 'subs' : 'tags'; s[key] = s[key].filter(function (x) { return x !== v; }); }
      });
    });
    el.clearAll.addEventListener('click', resetAll); el.filtersReset.addEventListener('click', resetAll); $('#emptyReset').addEventListener('click', resetAll);
    el.loadMore.addEventListener('click', appendMore);
    // sheet
    el.filtersOpen.addEventListener('click', function () { setSheet(true); });
    el.filtersClose.addEventListener('click', function () { setSheet(false); });
    el.filtersApply.addEventListener('click', function () { setSheet(false); });
    el.filtersOverlay.addEventListener('click', function () { setSheet(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheetOpen) setSheet(false); });
    // cards
    el.grid.addEventListener('click', function (e) {
      var card = e.target.closest('.p-card[data-id]'); if (!card) return;
      if (e.target.closest('[data-add]')) { toggleQuote(card.getAttribute('data-id')); return; }
      if (e.target.closest('[data-open]')) openProduct(card.getAttribute('data-id'));
    });
    el.grid.addEventListener('error', function (e) {
      var img = e.target; if (img.tagName !== 'IMG') return;
      var holder = img.closest('.p-card__media'); if (holder) holder.innerHTML = '<span class="p-card__placeholder"><span>Image unavailable</span></span>';
    }, true);
    // modal
    modal.addEventListener('click', function (e) {
      if (e.target.closest('[data-close]')) { closeProduct(); return; }
      var add = e.target.closest('[data-add]'); if (add) { toggleQuote(state.product); return; }
      var th = e.target.closest('[data-img]');
      if (th) { var m = $('#pmMain img'); if (m) m.src = th.getAttribute('data-img'); $$('.pm__thumbs button').forEach(function (b) { b.setAttribute('aria-current', String(b === th)); }); return; }
      var rel = e.target.closest('[data-rel]'); if (rel) openProduct(rel.getAttribute('data-rel'));
    });
    d.addEventListener('keydown', function (e) {
      if (modal.hidden) return;
      if (e.key === 'Escape' && !(window.PHQuote && $('#quoteDrawer').classList.contains('is-open'))) { e.preventDefault(); closeProduct(); }
      if (e.key === 'Tab') {
        var f = focusables(); if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && (d.activeElement === first || d.activeElement === panel)) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    // history
    window.addEventListener('popstate', function () {
      var s = parse(); var wantProduct = s.product; s.product = '';
      state = s; renderAll({ reset: true }); seo();
      if (wantProduct) openProduct(wantProduct, { fromPop: true }); else if (!modal.hidden) closeProduct({ fromPop: true });
    });
    if (window.PHQuote) PHQuote.onChange(syncAdd);
  }

  /* ------------------------------------------------------------------ init */
  function init() {
    el = { grid: $('#grid'), empty: $('#empty'), more: $('#more'), moreCount: $('#moreCount'), loadMore: $('#loadMore'), count: $('#resultCount'), active: $('#activeFilters'),
      clearAll: $('#clearAll'), q: $('#q'), qClear: $('#qClear'), sort: $('#sort'), catSwitch: $('#catSwitch'), rail: $('#brandRail'), brandHead: $('#brandHead'),
      filters: $('#filters'), filtersBody: $('#filtersBody'), filtersOpen: $('#filtersOpen'), filtersClose: $('#filtersClose'), filtersApply: $('#filtersApply'),
      filtersReset: $('#filtersReset'), filtersOverlay: $('#filtersOverlay'), filtersN: $('#filtersN') };
    modal = $('#pModal'); panel = $('.modal__panel', modal); content = $('#pmContent');

    state = parse();
    var hash = location.hash;
    if (LEGACY[hash] && !location.search) { var m = LEGACY[hash]; state.category = m.category; state.subs = m.subs || []; }
    buildBrandRail(); buildFilters(); bind();
    renderAll({ reset: true });
    var wantProduct = state.product; state.product = '';
    try { history.replaceState({ ph: 1 }, '', serialize(Object.assign({}, state, { product: wantProduct }))); } catch (e) {}
    if (LEGACY[hash]) { /* hash replaced by query string above */ }
    seo();
    if (wantProduct) openProduct(wantProduct, { fromPop: true });
    if (hash === '#brands') setTimeout(function () { var b = $('#brands'); if (b) b.scrollIntoView(); }, 60);
    built = true;
  }

  function fail() {
    var g = $('#grid'); if (g) { g.setAttribute('aria-busy', 'false'); g.innerHTML = '<div class="empty-state" style="grid-column:1/-1"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i><h3>We couldn\'t load the catalog</h3><p>Please check your connection and try again, or send us your list directly.</p><p class="empty-actions"><button class="btn btn--primary btn--sm" onclick="location.reload()">Try again</button> <a class="btn btn--accent btn--sm" href="contact.html#quote">Contact us</a></p></div>'; }
    var c = $('#resultCount'); if (c) c.textContent = 'Catalog unavailable';
  }

  load().then(function () {
    var go = function () { init(); }; if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', go); else go();
  }).catch(fail);
})();
