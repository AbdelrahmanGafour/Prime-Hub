/* Prime Hub Trading — unified motion system (GSAP + ScrollTrigger)
   data-reveal[="left|right|scale"]  single element reveal        data-reveal-group  staggered children
   data-counter="1000" [data-counter-suffix="+"] [data-counter-decimals="1"]   count-up
   data-magnetic      magnetic hover on buttons                   data-tilt           card tilt (max 4°, fine pointers only)
   data-hero-zoom / data-hero-in   page-hero entrance             .timeline / .stepper  scroll-linked line, step reveal
   Everything is optional: without GSAP (or with prefers-reduced-motion) content simply shows. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var hasGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  var PHMotion = window.PHMotion = { refresh: function () {}, reveal: function () {}, counters: function () {} };

  function show(el) { el.classList.add('is-revealed'); }
  function formatNum(v, dec) { return dec ? v.toFixed(dec) : String(Math.round(v)); }

  /* ---------- fallback: no GSAP or reduced motion ---------- */
  if (!hasGsap || reduce) {
    var targets = d.querySelectorAll('[data-reveal], [data-reveal-group]');
    if (reduce || !('IntersectionObserver' in window)) {
      targets.forEach(show);
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.querySelectorAll && e.target.hasAttribute('data-reveal-group') && Array.prototype.forEach.call(e.target.children, function (c, i) { c.style.setProperty('--i', i); });
          show(e.target); io.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -8% 0px' });
      targets.forEach(function (t) { io.observe(t); });
      PHMotion.reveal = function (scope) {
        (scope || d).querySelectorAll('[data-reveal],[data-reveal-group]').forEach(function (t) { if (!t.classList.contains('is-revealed')) io.observe(t); });
      };
    }
    d.querySelectorAll('.timeline__item').forEach(function (i) { i.classList.add('is-on'); });
    d.querySelectorAll('.timeline__line span').forEach(function (s) { s.style.transform = 'scaleY(1)'; });
    return;
  }

  /* ---------- GSAP path ---------- */
  gsap.registerPlugin(ScrollTrigger);
  root.classList.add('gsap-on');
  gsap.defaults({ ease: 'power3.out' });
  ScrollTrigger.config({ ignoreMobileResize: true });

  function fromVars(el) {
    var t = el.getAttribute('data-reveal');
    return t === 'left' ? { x: -32, y: 0 } : t === 'right' ? { x: 32, y: 0 } : t === 'scale' ? { scale: .96, y: 12 } : { y: 26 };
  }
  function done(el) { return function () { gsap.set(el, { clearProps: 'transform,opacity' }); show(el); }; }

  function reveal(scope) {
    scope = scope || d;
    var singles = Array.prototype.filter.call(scope.querySelectorAll('[data-reveal]'), function (e) { return !e.__rv; });
    singles.forEach(function (el) { el.__rv = 1; gsap.set(el, Object.assign({ opacity: 0 }, fromVars(el))); });
    if (singles.length) {
      ScrollTrigger.batch(singles, {
        start: 'top 90%', once: true, interval: .08,
        onEnter: function (batch) {
          batch.forEach(function (el, i) {
            gsap.to(el, { opacity: 1, x: 0, y: 0, scale: 1, duration: .8, delay: i * .06, onComplete: done(el) });
          });
        }
      });
    }
    var groups = Array.prototype.filter.call(scope.querySelectorAll('[data-reveal-group]'), function (e) { return !e.__rv; });
    groups.forEach(function (g) {
      g.__rv = 1;
      var kids = Array.prototype.slice.call(g.children);
      gsap.set(kids, { opacity: 0, y: 28 });
      ScrollTrigger.create({
        trigger: g, start: 'top 88%', once: true,
        onEnter: function () {
          gsap.to(kids, { opacity: 1, y: 0, duration: .7, stagger: Math.min(.09, .6 / Math.max(kids.length, 1)),
            onComplete: function () { kids.forEach(function (k) { gsap.set(k, { clearProps: 'transform,opacity' }); }); show(g); } });
        }
      });
    });
  }
  PHMotion.reveal = reveal;
  PHMotion.refresh = function () { ScrollTrigger.refresh(); };

  /* results swap (products grid): quick fade/rise, <= 300 ms total */
  PHMotion.swap = function (nodes) {
    if (!nodes || !nodes.length) return;
    gsap.fromTo(nodes, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .28, stagger: { each: .018, amount: .22 }, clearProps: 'transform,opacity', overwrite: true });
  };

  /* ---------- counters ---------- */
  function counters(scope) {
    (scope || d).querySelectorAll('[data-counter]').forEach(function (el) {
      if (el.__ct) return; el.__ct = 1;
      var end = parseFloat(el.getAttribute('data-counter')); if (isNaN(end)) return;
      var suf = el.getAttribute('data-counter-suffix') || '', pre = el.getAttribute('data-counter-prefix') || '';
      var dec = parseInt(el.getAttribute('data-counter-decimals') || '0', 10);
      var o = { v: 0 }; el.textContent = pre + formatNum(0, dec) + suf;
      ScrollTrigger.create({
        trigger: el, start: 'top 92%', once: true,
        onEnter: function () {
          gsap.to(o, { v: end, duration: 1.6, ease: 'power2.out', onUpdate: function () { el.textContent = pre + formatNum(o.v, dec) + suf; },
            onComplete: function () { el.textContent = pre + formatNum(end, dec) + suf; } });
        }
      });
    });
  }
  PHMotion.counters = counters;

  /* ---------- page hero ---------- */
  d.querySelectorAll('[data-hero-zoom]').forEach(function (el) {
    gsap.fromTo(el, { scale: 1.14 }, { scale: 1.02, duration: 2.2, ease: 'power2.out' });
    gsap.to(el, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: el.parentNode, start: 'top top', end: 'bottom top', scrub: true } });
  });
  d.querySelectorAll('[data-hero-in]').forEach(function (el) {
    gsap.from(el.children, { opacity: 0, y: 28, duration: .9, stagger: .1, delay: .1, clearProps: 'transform,opacity' });
  });
  d.querySelectorAll('.ph-hero__art').forEach(function (el) {
    gsap.fromTo(el, { rotate: -6, opacity: 0 }, { rotate: 0, opacity: .5, duration: 1.8, delay: .2 });
  });

  /* ---------- timeline: scroll-drawn line + active nodes ---------- */
  d.querySelectorAll('.timeline').forEach(function (tl) {
    var line = tl.querySelector('.timeline__line span');
    if (line) gsap.to(line, { scaleY: 1, ease: 'none', scrollTrigger: { trigger: tl, start: 'top 70%', end: 'bottom 60%', scrub: .4 } });
    tl.querySelectorAll('.timeline__item').forEach(function (it) {
      ScrollTrigger.create({ trigger: it, start: 'top 68%', onEnter: function () { it.classList.add('is-on'); }, onLeaveBack: function () { it.classList.remove('is-on'); } });
    });
  });
  d.querySelectorAll('.stepper').forEach(function (st) {
    var steps = st.querySelectorAll('.step');
    ScrollTrigger.create({ trigger: st, start: 'top 75%', once: true, onEnter: function () {
      steps.forEach(function (s, i) { setTimeout(function () { s.classList.add('is-on'); }, 220 * i); });
    } });
  });

  /* ---------- magnetic buttons (fine pointers only) ---------- */
  if (fine) {
    d.querySelectorAll('[data-magnetic]').forEach(function (el) {
      var xTo = gsap.quickTo(el, 'x', { duration: .45, ease: 'power3' }), yTo = gsap.quickTo(el, 'y', { duration: .45, ease: 'power3' });
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        xTo((e.clientX - (r.left + r.width / 2)) * .22); yTo((e.clientY - (r.top + r.height / 2)) * .3);
      });
      el.addEventListener('pointerleave', function () { xTo(0); yTo(0); });
    });

    /* ---------- tilt (max 4 deg) via delegation, so dynamic cards work too ---------- */
    var cur = null, MAX = 4;
    d.addEventListener('pointermove', function (e) {
      if (e.pointerType && e.pointerType !== 'mouse') return;
      var el = e.target.closest && e.target.closest('[data-tilt]');
      if (cur && cur !== el) { gsap.to(cur, { rotationX: 0, rotationY: 0, duration: .5, overwrite: 'auto' }); cur = null; }
      if (!el) return;
      cur = el;
      var r = el.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
      gsap.to(el, { rotationY: px * MAX * 2, rotationX: -py * MAX * 2, transformPerspective: 900, transformOrigin: 'center', duration: .35, overwrite: 'auto' });
    }, { passive: true });
    d.addEventListener('pointerleave', function () { if (cur) { gsap.to(cur, { rotationX: 0, rotationY: 0, duration: .5 }); cur = null; } }, true);
  }

  /* ---------- run + keep triggers fresh ---------- */
  function init() { reveal(d); counters(d); }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init); else init();
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(function () { ScrollTrigger.refresh(); });
})();
