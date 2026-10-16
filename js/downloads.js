/* Prime Hub Trading — Download Center
   Renders data/documents.json grouped by brand. URL state: ?brand=&type=&cat=&q= */
(function () {
  'use strict';
  var d = document;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var TYPE = { catalog: 'Catalog', datasheet: 'Datasheet', brochure: 'Brochure', manual: 'Manual / IFU' };
  var ICON = { catalog: 'fa-book', datasheet: 'fa-file-lines', brochure: 'fa-newspaper', manual: 'fa-book-open' };
  var docs = [], brands = [], bmap = {};
  var st = { q: '', cat: '', type: '', brand: '' };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function norm(s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }

  function readUrl() {
    var q = new URLSearchParams(location.search);
    st.q = (q.get('q') || '').slice(0, 80); st.cat = q.get('cat') === 'equipment' || q.get('cat') === 'material' ? q.get('cat') : '';
    st.type = TYPE[q.get('type')] ? q.get('type') : ''; st.brand = bmap[q.get('brand')] ? q.get('brand') : '';
  }
  function writeUrl() {
    var q = new URLSearchParams();
    Object.keys(st).forEach(function (k) { if (st[k]) q.set(k, st[k]); });
    var s = q.toString();
    try { history.replaceState(null, '', location.pathname + (s ? '?' + s : '')); } catch (e) {}
  }

  function filtered() {
    var terms = norm(st.q).split(/\s+/).filter(Boolean);
    return docs.filter(function (x) {
      if (st.cat && x.categories.indexOf(st.cat) < 0) return false;
      if (st.type && x.type !== st.type) return false;
      if (st.brand && x.brand !== st.brand) return false;
      var hay = norm(x.title + ' ' + bmap[x.brand].name + ' ' + TYPE[x.type]);
      return terms.every(function (t) { return hay.indexOf(t) >= 0; });
    });
  }

  function docHtml(x) {
    var url = x.externalUrl || x.file, ext = !!x.externalUrl;
    var name = x.file.split('/').pop();
    return '<article class="doc">' +
      '<span class="doc__icon"><i class="fa-regular fa-file-pdf" aria-hidden="true"></i></span>' +
      '<div><h3 class="doc__title">' + esc(x.title) + '</h3><div class="doc__meta">' +
      '<span class="chip"><i class="fa-solid ' + ICON[x.type] + '" aria-hidden="true"></i>' + TYPE[x.type] + '</span>' +
      (x.pages ? '<span>' + x.pages + (x.pages === 1 ? ' page' : ' pages') + '</span>' : '') +
      (x.sizeMB ? '<span class="tnum">' + x.sizeMB + ' MB</span>' : '') +
      (x.lang ? '<span>' + esc(x.lang) + '</span>' : '') +
      x.categories.map(function (c) { return '<span class="mini-badge mini-badge--' + (c === 'equipment' ? 'eq' : 'mat') + '">' + (c === 'equipment' ? 'Equipment' : 'Material') + '</span>'; }).join('') +
      (x.large ? '<span class="chip chip--orange" title="Large file, it may take a while on a slow connection">Large file</span>' : '') +
      '</div></div>' +
      '<div class="doc__actions"><a class="btn btn--primary btn--sm" href="' + esc(url) + '"' + (ext ? ' target="_blank" rel="noopener"' : ' download="' + esc(name) + '"') + '><i class="fa-solid fa-download" aria-hidden="true"></i> Download</a>' +
      '<a class="btn btn--ghost btn--sm" href="' + esc(url) + '" target="_blank" rel="noopener" aria-label="Preview ' + esc(x.title) + ' in a new tab"><i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i> Preview</a></div></article>';
  }

  function render() {
    var list = filtered(), host = $('#docs');
    host.setAttribute('aria-busy', 'false');
    var groups = {}; list.forEach(function (x) { (groups[x.brand] = groups[x.brand] || []).push(x); });
    var order = brands.filter(function (b) { return groups[b.slug]; }).sort(function (a, b) { return groups[b.slug].length - groups[a.slug].length || a.name.localeCompare(b.name); });
    host.innerHTML = order.map(function (b) {
      var g = groups[b.slug];
      return '<section class="doc-group" aria-labelledby="g-' + b.slug + '"><div class="doc-group__head">' +
        '<span class="doc-group__logo">' + (b.logo ? '<img src="' + esc(b.logo) + '" alt="" loading="lazy" height="34">' : '<span class="wordmark">' + esc(b.name) + '</span>') + '</span>' +
        '<h2 class="sr-only" id="g-' + b.slug + '">' + esc(b.name) + '</h2><span class="doc-group__n">' + g.length + (g.length === 1 ? ' document' : ' documents') + '</span></div>' +
        '<div class="doc-list">' + g.map(docHtml).join('') + '</div></section>';
    }).join('');
    $('#dlEmpty').hidden = list.length > 0;
    $('#dlCount').innerHTML = list.length ? 'Showing <strong>' + list.length + '</strong> of ' + docs.length + ' documents' : 'No documents found';
    $$('#dlCat button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-cat') === st.cat)); });
    $('#dtype').value = st.type; $('#dbrand').value = st.brand; if ($('#dq').value !== st.q) $('#dq').value = st.q;
    if (window.PHMotion && PHMotion.swap) PHMotion.swap($$('.doc', host));
  }

  function bind() {
    var t; $('#dq').addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { st.q = $('#dq').value.trim(); writeUrl(); render(); }, 160); });
    $('#dlCat').addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; st.cat = b.getAttribute('data-cat'); writeUrl(); render(); });
    $('#dtype').addEventListener('change', function () { st.type = this.value; writeUrl(); render(); });
    $('#dbrand').addEventListener('change', function () { st.brand = this.value; writeUrl(); render(); });
    $('#dlReset').addEventListener('click', function () { st = { q: '', cat: '', type: '', brand: '' }; writeUrl(); render(); });
  }

  Promise.all([fetch('data/documents.json').then(function (r) { return r.json(); }), fetch('data/brands.json').then(function (r) { return r.json(); })]).then(function (r) {
    docs = r[0]; brands = r[1]; brands.forEach(function (b) { bmap[b.slug] = b; });
    var sel = $('#dbrand');
    brands.filter(function (b) { return docs.some(function (x) { return x.brand === b.slug; }); }).sort(function (a, b) { return a.name.localeCompare(b.name); })
      .forEach(function (b) { var o = d.createElement('option'); o.value = b.slug; o.textContent = b.name; sel.appendChild(o); });
    $$('#dtype option').forEach(function (o) { if (o.value && !docs.some(function (x) { return x.type === o.value; })) o.remove(); });
    $$('[data-doc-count]').forEach(function (e) { e.textContent = docs.length; });
    readUrl(); bind(); render();
  }).catch(function () {
    $('#docs').innerHTML = '<div class="empty-state"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i><h3>We couldn\'t load the documents</h3><p>Please try again, or contact us and we\'ll send the catalog directly.</p><p class="empty-actions"><a class="btn btn--accent btn--sm" href="contact.html">Contact us</a></p></div>';
    $('#dlCount').textContent = 'Documents unavailable';
  });
})();
