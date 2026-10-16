/* Sticky mini-nav: scroll-spy + correct anchor offset (header + subnav height). */
(function () {
  'use strict';
  var nav = document.querySelector('.subnav'); if (!nav) return;
  var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
  var map = links.map(function (a) { return { a: a, el: document.querySelector(a.getAttribute('href')) }; }).filter(function (m) { return m.el; });
  function pad() {
    var h = document.getElementById('siteHeader');
    document.documentElement.style.scrollPaddingTop = ((h ? h.offsetHeight : 64) + nav.offsetHeight + 12) + 'px';
  }
  pad(); window.addEventListener('resize', pad);
  function set(a) { links.forEach(function (l) { l.classList.toggle('is-active', l === a); if (l === a) l.setAttribute('aria-current', 'true'); else l.removeAttribute('aria-current'); }); if (a && a.scrollIntoView && nav.scrollWidth > nav.clientWidth) a.scrollIntoView({ block: 'nearest', inline: 'center' }); }
  var ticking = false;
  function spy() {
    var y = window.scrollY + nav.getBoundingClientRect().bottom + 24, cur = map[0];
    map.forEach(function (m) { if (m.el.getBoundingClientRect().top + window.scrollY <= y) cur = m; });
    if (cur) set(cur.a); ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(spy); } }, { passive: true });
  spy();
})();
