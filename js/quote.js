/* Prime Hub Trading — quote list (RFQ basket)
   Persists in localStorage (falls back to memory when storage is unavailable). No prices anywhere.
   Public API: window.PHQuote { add, remove, setQty, clear, items, count, has, text, waUrl, open, close, onChange } */
(function () {
  'use strict';
  var KEY = 'ph.quote.v1';
  var WA = '201090009508';
  var memory = [];
  var listeners = [];
  var storageOk = (function () {
    try { var k = '__ph'; localStorage.setItem(k, '1'); localStorage.removeItem(k); return true; } catch (e) { return false; }
  })();

  function read() {
    if (!storageOk) return memory.slice();
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || '[]');
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }
  function write(items) {
    memory = items.slice();
    if (storageOk) { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) { storageOk = false; } }
    emit();
  }
  function emit() { var it = read(); listeners.forEach(function (fn) { try { fn(it); } catch (e) {} }); }

  var Q = {
    items: read,
    count: function () { return read().reduce(function (n, i) { return n + (i.qty || 1); }, 0); },
    has: function (id) { return read().some(function (i) { return i.id === id; }); },
    add: function (p, qty) {
      var items = read(), found = items.filter(function (i) { return i.id === p.id; })[0];
      if (found) found.qty = Math.min(999, (found.qty || 1) + (qty || 1));
      else items.push({ id: p.id, qty: qty || 1, name: p.name, model: p.model || '', brand: p.brandName || p.brand || '', thumb: p.thumb || '' });
      write(items);
    },
    remove: function (id) { write(read().filter(function (i) { return i.id !== id; })); },
    setQty: function (id, qty) {
      qty = Math.max(1, Math.min(999, parseInt(qty, 10) || 1));
      write(read().map(function (i) { if (i.id === id) i.qty = qty; return i; }));
    },
    clear: function () { write([]); },
    onChange: function (fn) { listeners.push(fn); },
    text: function () {
      var items = read();
      if (!items.length) return '';
      return items.map(function (i, n) {
        return (n + 1) + '. ' + (i.brand ? i.brand + ' - ' : '') + i.name + (i.model ? ' (' + i.model + ')' : '') + ' x ' + i.qty;
      }).join('\n');
    },
    waUrl: function () {
      var t = Q.text();
      var msg = t ? 'Hello Prime Hub Trading, I would like a quote for:\n' + t : 'Hello Prime Hub Trading, I would like some information about your products.';
      return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
    },
    storageOk: function () { return storageOk; }
  };
  window.PHQuote = Q;
  window.addEventListener('storage', function (e) { if (e.key === KEY) emit(); });

  /* ---- drawer UI ---- */
  var drawer, overlay, body, lastFocus;
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function render() {
    var items = read(), n = Q.count();
    document.querySelectorAll('[data-quote-count]').forEach(function (el) {
      var prev = el.getAttribute('data-n');
      el.textContent = n > 99 ? '99+' : n;
      el.setAttribute('data-n', n);
      if (prev !== null && String(prev) !== String(n)) {
        var btn = el.closest('.quote-btn');
        if (btn) { btn.classList.add('bump'); setTimeout(function () { btn.classList.remove('bump'); }, 350); }
      }
    });
    if (!body) return;
    var foot = drawer.querySelector('.drawer__foot');
    if (!items.length) {
      body.innerHTML = '<div class="q-empty"><i class="fa-solid fa-clipboard-list" aria-hidden="true"></i>' +
        '<p><strong>Your list is empty.</strong><br>Add products to request one quote for several items.</p>' +
        '<a class="btn btn--primary btn--sm" href="products.html">Browse products</a></div>';
      foot.querySelectorAll('#quoteSend,#quoteWa,#quoteClear').forEach(function (b) { b.style.display = 'none'; });
      return;
    }
    foot.querySelectorAll('#quoteSend,#quoteWa,#quoteClear').forEach(function (b) { b.style.display = ''; });
    body.innerHTML = items.map(function (i) {
      return '<div class="q-item" data-id="' + esc(i.id) + '">' +
        '<div class="q-item__img">' + (i.thumb ? '<img src="' + esc(i.thumb) + '" alt="" width="64" height="64" loading="lazy">' : '<i class="fa-solid fa-box-open" aria-hidden="true"></i>') + '</div>' +
        '<div><h3 class="h4">' + esc(i.name) + '</h3><small>' + esc(i.brand) + (i.model ? ' · ' + esc(i.model) : '') + '</small>' +
        '<div class="qty" role="group" aria-label="Quantity for ' + esc(i.name) + '">' +
        '<button type="button" data-q="-1" aria-label="Decrease quantity">&minus;</button>' +
        '<input type="number" min="1" max="999" value="' + i.qty + '" inputmode="numeric" aria-label="Quantity">' +
        '<button type="button" data-q="1" aria-label="Increase quantity">+</button></div></div>' +
        '<button class="q-remove" type="button" data-remove aria-label="Remove ' + esc(i.name) + '"><i class="fa-solid fa-trash-can" aria-hidden="true"></i></button></div>';
    }).join('');
    var wa = document.getElementById('quoteWa'); if (wa) wa.href = Q.waUrl();
  }

  function focusables() {
    return Array.prototype.slice.call(drawer.querySelectorAll('a[href],button:not([disabled]),input,[tabindex]:not([tabindex="-1"])')).filter(function (el) { return el.offsetParent !== null; });
  }
  function open() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    var tr = document.getElementById('toasts'); if (tr) tr.innerHTML = '';
    drawer.classList.add('is-open'); overlay.classList.add('is-on');
    drawer.setAttribute('aria-hidden', 'false'); document.body.classList.add('no-scroll');
    render();
    var f = focusables(); (f[0] || drawer).focus();
  }
  function close() {
    if (!drawer || !drawer.classList.contains('is-open')) return;
    drawer.classList.remove('is-open'); overlay.classList.remove('is-on');
    drawer.setAttribute('aria-hidden', 'true'); document.body.classList.remove('no-scroll');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  Q.open = open; Q.close = close;

  document.addEventListener('DOMContentLoaded', function () {
    drawer = document.getElementById('quoteDrawer'); overlay = document.getElementById('quoteOverlay'); body = document.getElementById('quoteItems');
    render();
    Q.onChange(render);
    if (!drawer) return;
    var openBtn = document.getElementById('quoteOpen');
    if (openBtn) openBtn.addEventListener('click', open);
    overlay.addEventListener('click', close);
    document.getElementById('quoteClose').addEventListener('click', close);
    document.getElementById('quoteClear').addEventListener('click', function () { Q.clear(); });
    document.addEventListener('keydown', function (e) {
      if (!drawer.classList.contains('is-open')) return;
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      if (e.key === 'Tab') {
        var f = focusables(); if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    body.addEventListener('click', function (e) {
      var row = e.target.closest('.q-item'); if (!row) return;
      var id = row.getAttribute('data-id');
      if (e.target.closest('[data-remove]')) { Q.remove(id); return; }
      var q = e.target.closest('[data-q]');
      if (q) { var cur = (Q.items().filter(function (i) { return i.id === id; })[0] || {}).qty || 1; Q.setQty(id, cur + parseInt(q.getAttribute('data-q'), 10)); }
    });
    body.addEventListener('change', function (e) {
      var row = e.target.closest('.q-item'); if (row && e.target.tagName === 'INPUT') Q.setQty(row.getAttribute('data-id'), e.target.value);
    });
  });
})();
