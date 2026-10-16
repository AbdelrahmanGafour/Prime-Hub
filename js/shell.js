/* Prime Hub Trading — inner-page shell behaviour: sticky/shrinking glass header, scroll progress,
   mobile menu (focus trap, ESC), dropdowns, back-to-top, toasts. */
(function () {
  'use strict';
  var d = document, body = d.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var WA = '201090009508';

  /* ---------- toasts ---------- */
  window.PH = window.PH || {};
  PH.toast = function (msg, actionLabel, actionFn, ms) {
    var region = d.getElementById('toasts'); if (!region) return;
    var t = d.createElement('div'); t.className = 'toast';
    t.innerHTML = '<i class="fa-solid fa-circle-check" aria-hidden="true"></i><span></span>';
    t.querySelector('span').textContent = msg;
    if (actionLabel) {
      var b = d.createElement('button'); b.type = 'button'; b.textContent = actionLabel;
      b.addEventListener('click', function () { if (actionFn) actionFn(); t.remove(); });
      t.appendChild(b);
    }
    region.appendChild(t);
    setTimeout(function () { if (t.parentNode) t.remove(); }, ms || 3800);
  };
  PH.waLink = function (text) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text); };

  /* ---------- scroll state: header shrink, progress bar, back-to-top ---------- */
  var bar = d.querySelector('.scroll-progress span'), top = d.getElementById('toTop'), ticking = false;
  function onScroll() {
    var y = window.scrollY || d.documentElement.scrollTop;
    body.classList.toggle('is-scrolled', y > 40);
    if (bar) { var h = d.documentElement.scrollHeight - window.innerHeight; bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')'; }
    if (top) top.classList.toggle('is-on', y > 640);
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* ---------- mobile menu ---------- */
  var nav = d.getElementById('nav'), toggle = d.getElementById('navToggle'), overlay = d.getElementById('navOverlay');
  var mq = window.matchMedia('(max-width: 1120px)'), lastFocus = null;
  function navFocusables() {
    return Array.prototype.slice.call(nav.querySelectorAll('a[href],button')).filter(function (el) { return el.offsetParent !== null; }).concat([toggle]);
  }
  function openNav() {
    lastFocus = d.activeElement;
    nav.classList.add('is-open'); overlay.classList.add('is-on'); body.classList.add('no-scroll', 'nav-open');
    toggle.setAttribute('aria-expanded', 'true'); toggle.setAttribute('aria-label', 'Close menu');
    var f = nav.querySelector('a[href]'); if (f) f.focus();
  }
  function closeNav(restore) {
    nav.classList.remove('is-open'); overlay.classList.remove('is-on'); body.classList.remove('no-scroll', 'nav-open');
    toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Open menu');
    if (restore !== false && lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (nav && toggle) {
    toggle.addEventListener('click', function () { nav.classList.contains('is-open') ? closeNav() : openNav(); });
    overlay.addEventListener('click', function () { closeNav(); });
    nav.addEventListener('click', function (e) { if (mq.matches && e.target.closest('a[href]') && !e.target.closest('.dd-toggle')) closeNav(false); });
    d.addEventListener('keydown', function (e) {
      if (!nav.classList.contains('is-open') || !mq.matches) return;
      if (e.key === 'Escape') { e.preventDefault(); closeNav(); return; }
      if (e.key === 'Tab') {
        var f = navFocusables(), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    (mq.addEventListener ? mq.addEventListener('change', function () { closeNav(false); }) : mq.addListener(function () { closeNav(false); }));
  }

  /* ---------- dropdown (keyboard + touch) ---------- */
  d.querySelectorAll('.has-dropdown').forEach(function (li) {
    var btn = li.querySelector('.dd-toggle');
    function set(v) { li.classList.toggle('is-open', v); btn.setAttribute('aria-expanded', v ? 'true' : 'false'); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); set(!li.classList.contains('is-open')); });
    li.addEventListener('keydown', function (e) { if (e.key === 'Escape' && li.classList.contains('is-open')) { set(false); btn.focus(); } });
    li.addEventListener('mouseenter', function () { if (!mq.matches) btn.setAttribute('aria-expanded', 'true'); });
    li.addEventListener('mouseleave', function () { if (!mq.matches) btn.setAttribute('aria-expanded', 'false'); });
  });
  d.addEventListener('click', function (e) { d.querySelectorAll('.has-dropdown.is-open').forEach(function (li) { if (!li.contains(e.target) && !mq.matches) { li.classList.remove('is-open'); li.querySelector('.dd-toggle').setAttribute('aria-expanded', 'false'); } }); });

  /* ---------- placeholder links (social, legal): keep them inert until real URLs exist ---------- */
  d.querySelectorAll('a[data-placeholder]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); }); });

  /* ---------- WhatsApp links: add the current page to the greeting ---------- */
  d.querySelectorAll('a[data-wa]').forEach(function (a) {
    var page = (d.title || '').split('|')[0].trim();
    if (page && body.dataset.page && body.dataset.page !== 'products') {
      a.href = PH.waLink('Hello Prime Hub Trading, I have a question (from your "' + page + '" page).');
    }
  });

})();
