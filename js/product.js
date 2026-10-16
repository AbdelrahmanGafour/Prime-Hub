/* Prime Hub Trading — product detail page: gallery, zoom, add to quote, inline PDF viewer */
(function () {
  'use strict';
  var d = document, $ = function (s, r) { return (r || d).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var data = {}; try { data = JSON.parse($('#pdata').textContent); } catch (e) {}

  /* gallery */
  var main = $('#pdMain');
  $$('[data-img]').forEach(function (b) {
    b.addEventListener('click', function () { if (main) main.src = b.getAttribute('data-img'); $$('[data-img]').forEach(function (x) { x.setAttribute('aria-current', String(x === b)); }); });
  });
  var lb = $('#lightbox'), lbImg = $('#lbImg'), opener = null;
  function openLb() { if (!main) return; opener = d.activeElement; lbImg.src = main.src; lbImg.alt = main.alt; lb.hidden = false; d.body.classList.add('no-scroll'); $('#lbClose').focus(); }
  function closeLb() { lb.hidden = true; d.body.classList.remove('no-scroll'); if (opener) opener.focus(); }
  var z = $('[data-zoom]'); if (z) z.addEventListener('click', openLb);
  if (lb) { $('#lbClose').addEventListener('click', closeLb); lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); }); d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) closeLb(); }); }

  /* quote */
  var add = $('[data-add]');
  function sync() {
    if (!add || !window.PHQuote) return; var on = PHQuote.has(data.id);
    add.setAttribute('aria-pressed', String(on));
    add.innerHTML = on ? '<i class="fa-solid fa-check" aria-hidden="true"></i> In your quote list' : '<i class="fa-solid fa-plus" aria-hidden="true"></i> Add to quote';
  }
  if (add) {
    add.addEventListener('click', function () {
      if (PHQuote.has(data.id)) { PHQuote.remove(data.id); PH.toast('Removed from your quote list'); }
      else { PHQuote.add(data); PH.toast('Added to your quote list', 'View list', function () { PHQuote.open(); }); }
    });
    var wait = setInterval(function () { if (window.PHQuote) { clearInterval(wait); sync(); PHQuote.onChange(sync); } }, 50);
  }

  /* inline PDF viewer */
  var v = $('#pdViewer'), f = $('#pdFrame');
  $$('[data-view]').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = b.getAttribute('data-view');
      f.src = url; v.hidden = false; $('#pdViewerTitle').textContent = b.getAttribute('data-title');
      var o = $('#pdViewerOpen'); o.href = url; v.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    });
  });
  var c = $('#pdViewerClose'); if (c) c.addEventListener('click', function () { v.hidden = true; f.removeAttribute('src'); });
})();
