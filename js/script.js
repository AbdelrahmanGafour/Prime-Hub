document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Mobile nav toggle ---------- */
  const navToggle = document.getElementById('navToggle');
  const nav = document.getElementById('nav');

  navToggle.addEventListener('click', () => {
    nav.classList.toggle('is-open');
    const icon = navToggle.querySelector('i');
    icon.classList.toggle('fa-bars');
    icon.classList.toggle('fa-xmark');
  });

  // Toggle dropdowns on tap for mobile
  document.querySelectorAll('.has-dropdown > a').forEach(link => {
    link.addEventListener('click', (e) => {
      if (window.innerWidth <= 960) {
        e.preventDefault();
        link.parentElement.classList.toggle('is-open');
      }
    });
  });

  // Close mobile nav when a link is clicked
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 960 && !link.parentElement.classList.contains('has-dropdown')) {
        nav.classList.remove('is-open');
        navToggle.querySelector('i').classList.add('fa-bars');
        navToggle.querySelector('i').classList.remove('fa-xmark');
      }
    });
  });

  /* ---------- Active nav link on scroll ---------- */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav > ul > li > a');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const top = section.offsetTop - 120;
      if (window.scrollY >= top) current = section.getAttribute('id');
    });
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) link.classList.add('active');
    });
  });

  /* ---------- Hero slider ---------- */
  const slides = document.querySelectorAll('.hero__slide');
  const slideCurrentEl = document.getElementById('slideCurrent');
  const progressEl = document.getElementById('heroProgress');
  const prevBtn = document.getElementById('heroPrev');
  const nextBtn = document.getElementById('heroNext');
  let heroIndex = 0;
  let heroTimer;

  function showSlide(i) {
    slides.forEach(s => s.classList.remove('is-active'));
    heroIndex = (i + slides.length) % slides.length;
    slides[heroIndex].classList.add('is-active');
    slideCurrentEl.textContent = '0' + (heroIndex + 1);
    progressEl.style.width = ((heroIndex + 1) / slides.length * 100) + '%';
  }

  function startHeroTimer() {
    clearInterval(heroTimer);
    heroTimer = setInterval(() => showSlide(heroIndex + 1), 5000);
  }

  prevBtn.addEventListener('click', () => { showSlide(heroIndex - 1); startHeroTimer(); });
  nextBtn.addEventListener('click', () => { showSlide(heroIndex + 1); startHeroTimer(); });

  showSlide(0);
  startHeroTimer();

  /* ---------- Product carousel ---------- */
  const track = document.getElementById('prodTrack');
  const cards = track.querySelectorAll('.product-card');
  const dotsWrap = document.getElementById('prodDots');
  const prodPrev = document.getElementById('prodPrev');
  const prodNext = document.getElementById('prodNext');

  function getVisibleCount() {
    if (window.innerWidth <= 600) return 1;
    if (window.innerWidth <= 960) return 2;
    return 3;
  }

  let prodIndex = 0;
  let visibleCount = getVisibleCount();
  const maxIndex = () => Math.max(cards.length - visibleCount, 0);

  function buildDots() {
    dotsWrap.innerHTML = '';
    const dotCount = maxIndex() + 1;
    for (let i = 0; i < dotCount; i++) {
      const dot = document.createElement('span');
      if (i === prodIndex) dot.classList.add('is-active');
      dot.addEventListener('click', () => goToSlide(i));
      dotsWrap.appendChild(dot);
    }
  }

  function updateCarousel() {
    const cardWidth = cards[0].getBoundingClientRect().width;
    const gap = 24;
    track.style.transform = `translateX(-${prodIndex * (cardWidth + gap)}px)`;
    [...dotsWrap.children].forEach((dot, i) => dot.classList.toggle('is-active', i === prodIndex));
  }

  function goToSlide(i) {
    prodIndex = Math.min(Math.max(i, 0), maxIndex());
    updateCarousel();
  }

  prodPrev.addEventListener('click', () => goToSlide(prodIndex - 1));
  prodNext.addEventListener('click', () => goToSlide(prodIndex + 1));

  window.addEventListener('resize', () => {
    visibleCount = getVisibleCount();
    prodIndex = Math.min(prodIndex, maxIndex());
    buildDots();
    updateCarousel();
  });

  buildDots();
  updateCarousel();

  /* ---------- Quote form ---------- */
  const quoteForm = document.getElementById('quoteForm');
  quoteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const submitBtn = quoteForm.querySelector('.quote__submit');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Request Sent ✓';
    submitBtn.style.background = '#1fa855';
    quoteForm.reset();
    setTimeout(() => {
      submitBtn.textContent = originalText;
      submitBtn.style.background = '';
    }, 2800);
  });

  /* ---------- Watch video placeholder ---------- */
  const watchVideoBtn = document.getElementById('watchVideoBtn');
  watchVideoBtn.addEventListener('click', (e) => {
    e.preventDefault();
    alert('Company introduction video coming soon.');
  });

  /* ---------- Back to top ---------- */
  const backToTop = document.getElementById('backToTop');
  window.addEventListener('scroll', () => {
    backToTop.classList.toggle('is-visible', window.scrollY > 500);
  });
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

});
