/* =============================================
   Prime Hub Trading — Inner-page scroll animations
   Loaded only on inner pages (about/products/training/
   downloads/service/contact) — the home page is untouched.
   ============================================= */
document.addEventListener('DOMContentLoaded', () => {

  if (typeof gsap === 'undefined') return;
  gsap.registerPlugin(ScrollTrigger);

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  /* Page hero: gentle zoom-out on the background photo as the page loads */
  gsap.utils.toArray('[data-hero-zoom]').forEach(el => {
    gsap.fromTo(el, { scale: 1.12 }, { scale: 1, duration: 1.8, ease: 'power2.out' });
  });

  gsap.utils.toArray('[data-hero-in]').forEach(el => {
    gsap.from(el.children, {
      opacity: 0,
      y: 24,
      duration: 0.8,
      stagger: 0.12,
      ease: 'power2.out',
      delay: 0.15
    });
  });

  /* Generic single-element reveal on scroll */
  gsap.utils.toArray('[data-reveal]').forEach(el => {
    gsap.from(el, {
      opacity: 0,
      y: 36,
      duration: 0.7,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 88%',
        toggleActions: 'play none none none'
      }
    });
  });

  /* Grouped reveal: animates direct children with a stagger */
  gsap.utils.toArray('[data-reveal-group]').forEach(group => {
    gsap.from(group.children, {
      opacity: 0,
      y: 30,
      duration: 0.6,
      stagger: 0.1,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: group,
        start: 'top 88%',
        toggleActions: 'play none none none'
      }
    });
  });

  /* Slide in from left/right for two-column media+text sections */
  gsap.utils.toArray('[data-reveal-left]').forEach(el => {
    gsap.from(el, {
      opacity: 0, x: -40, duration: 0.8, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 85%' }
    });
  });
  gsap.utils.toArray('[data-reveal-right]').forEach(el => {
    gsap.from(el, {
      opacity: 0, x: 40, duration: 0.8, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 85%' }
    });
  });

  /* Animated count-up for stat numbers, e.g. data-counter="1000" data-counter-suffix="+" */
  gsap.utils.toArray('[data-counter]').forEach(el => {
    const target = parseFloat(el.dataset.counter);
    const suffix = el.dataset.counterSuffix || '';
    if (Number.isNaN(target)) return;
    const counterObj = { val: 0 };
    ScrollTrigger.create({
      trigger: el,
      start: 'top 90%',
      once: true,
      onEnter: () => {
        gsap.to(counterObj, {
          val: target,
          duration: 1.5,
          ease: 'power1.out',
          onUpdate: () => { el.textContent = Math.round(counterObj.val) + suffix; }
        });
      }
    });
  });

  /* Timeline items alternate in from either side on About page */
  gsap.utils.toArray('[data-timeline-item]').forEach((el, i) => {
    gsap.from(el, {
      opacity: 0,
      x: -30,
      duration: 0.6,
      ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 88%' }
    });
  });

  /* Sticky sidebar active-state on Products page (visual only — no layout logic) */
  gsap.utils.toArray('[data-cat-section]').forEach(section => {
    ScrollTrigger.create({
      trigger: section,
      start: 'top 40%',
      end: 'bottom 40%',
      onToggle: self => {
        if (!self.isActive) return;
        const id = section.getAttribute('id');
        document.querySelectorAll('.cat-sidebar__link').forEach(link => {
          link.classList.toggle('is-active', link.getAttribute('href') === '#' + id);
        });
      }
    });
  });

});
