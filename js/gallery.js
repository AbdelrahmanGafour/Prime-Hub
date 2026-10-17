/* Training Center galleries: tabbed Events/Courses post grid (training.html) and
   the media detail page with lightbox (training-gallery.html?type=event|course&id=slug). */
(function () {
  'use strict';
  var d = document, DATA_URL = 'data/training-gallery.json';
  var fmt = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
  function esc(s) { var e = d.createElement('div'); e.textContent = s == null ? '' : s; return e.innerHTML; }
  function date(s) { return fmt.format(new Date(s)); }
  function counts(it) {
    var p = it.media.filter(function (m) { return m.type === 'image'; }).length, v = it.media.length - p;
    return { p: p, v: v };
  }
  function load() { return fetch(DATA_URL).then(function (r) { return r.json(); }); }
  var KINDS = { event: 'events', course: 'courses' };

  /* ---------- list page ---------- */
  function card(it, kind) {
    var c = counts(it), href = 'training-gallery.html?type=' + kind + '&id=' + encodeURIComponent(it.slug);
    return '<article class="post">' +
      '<div class="post__media"><img src="' + esc(it.cover) + '" alt="" loading="lazy" decoding="async">' +
      '<span class="chip chip--solid post__badge">' + esc(it.category) + '</span>' +
      '<div class="post__counts"><span><i class="fa-regular fa-image" aria-hidden="true"></i>' + c.p + '</span>' +
      (c.v ? '<span><i class="fa-solid fa-play" aria-hidden="true"></i>' + c.v + '</span>' : '') + '</div></div>' +
      '<div class="post__body"><div class="post__meta"><span><i class="fa-regular fa-calendar" aria-hidden="true"></i>' + date(it.date) + '</span>' +
      '<span><i class="fa-solid fa-location-dot" aria-hidden="true"></i>' + esc(it.location) + '</span></div>' +
      '<h3>' + esc(it.title) + '</h3><p>' + esc(it.summary) + '</p>' +
      '<a class="link-arrow stretched" href="' + href + '">View gallery <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></div></article>';
  }
  function initList(root) {
    load().then(function (data) {
      var tabs = root.querySelectorAll('.gtab');
      Array.prototype.forEach.call(tabs, function (t) {
        var kind = t.dataset.kind, panel = d.getElementById(t.getAttribute('aria-controls')), list = data[KINDS[kind]] || [];
        t.querySelector('.count').textContent = list.length;
        panel.innerHTML = list.length ? '<div class="ggrid">' + list.map(function (i) { return card(i, kind); }).join('') + '</div>' : '<p class="gempty">Nothing here yet. Check back soon.</p>';
      });
      function show(t, focus) {
        Array.prototype.forEach.call(tabs, function (x) {
          var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
          d.getElementById(x.getAttribute('aria-controls')).hidden = !on;
        });
        if (focus) t.focus();
        try { history.replaceState(null, '', '#gallery-' + t.dataset.kind + 's'); } catch (e) {}
      }
      Array.prototype.forEach.call(tabs, function (t, i) {
        t.addEventListener('click', function () { show(t); });
        t.addEventListener('keydown', function (e) {
          var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!n) return;
          e.preventDefault(); show(tabs[(i + n + tabs.length) % tabs.length], true);
        });
      });
      if (/gallery-courses/.test(location.hash)) show(tabs[1]);
    }).catch(function () { root.querySelector('.gpanel').innerHTML = '<p class="gempty">Gallery could not be loaded.</p>'; });
  }

  /* ---------- detail page ---------- */
  function initDetail(root) {
    var qs = new URLSearchParams(location.search), kind = qs.get('type') === 'course' ? 'course' : 'event', id = qs.get('id');
    load().then(function (data) {
      var list = data[KINDS[kind]] || [], it = list.filter(function (x) { return x.slug === id; })[0];
      if (!it) { root.innerHTML = '<div class="container ph-section"><p class="gempty">This gallery was not found. <a href="training.html#gallery">Back to the Training Center</a></p></div>'; return; }
      d.title = it.title + ' | Prime Hub Training Center';
      var c = counts(it), back = 'training.html#gallery-' + KINDS[kind];
      d.getElementById('gdBack').href = back;
      d.getElementById('gdBackLabel').textContent = 'Back to ' + KINDS[kind];
      d.getElementById('gdType').textContent = kind === 'event' ? 'Event' : 'Course';
      d.getElementById('gdTitle').textContent = it.title;
      d.getElementById('gdLead').textContent = it.description;
      var meta = '<span class="chip chip--orange"><i class="fa-regular fa-calendar" aria-hidden="true"></i>' + date(it.date) + '</span>' +
        '<span class="chip"><i class="fa-solid fa-location-dot" aria-hidden="true"></i>' + esc(it.location) + '</span>' +
        '<span class="chip">' + esc(it.category) + '</span>' +
        '<span class="chip"><i class="fa-regular fa-image" aria-hidden="true"></i>' + c.p + ' photos</span>' +
        (c.v ? '<span class="chip"><i class="fa-solid fa-play" aria-hidden="true"></i>' + c.v + ' videos</span>' : '');
      d.getElementById('gdMeta').innerHTML = meta;
      var cta = d.getElementById('gdCta');
      if (kind === 'course' && it.courseId) { cta.href = 'training.html?course=' + it.courseId + '#book'; cta.hidden = false; }
      var grid = d.getElementById('gdGrid'), filter = d.getElementById('gdFilter'), shown = it.media;
      if (!c.v) filter.hidden = true;
      function render() {
        grid.innerHTML = shown.map(function (m, i) {
          return '<button type="button" class="mitem' + (m.type === 'video' ? ' mitem--video' : '') + '" data-i="' + i + '" aria-label="' + (m.type === 'video' ? 'Play video: ' : 'Open photo: ') + esc(m.caption || it.title) + '">' +
            '<img src="' + esc(m.type === 'video' ? m.poster : m.src) + '" alt="" loading="lazy" decoding="async">' +
            (m.caption ? '<span class="mitem__cap">' + esc(m.caption) + '</span>' : '') + '</button>';
        }).join('');
      }
      render();
      filter.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        Array.prototype.forEach.call(filter.children, function (x) { x.setAttribute('aria-pressed', x === b); });
        var f = b.dataset.f; shown = f === 'all' ? it.media : it.media.filter(function (m) { return m.type === f; }); render();
      });
      lightbox(grid, function () { return shown; });
      // more from same kind
      var more = list.filter(function (x) { return x.slug !== it.slug; }).slice(0, 3);
      var mw = d.getElementById('gdMore');
      if (more.length) mw.querySelector('.ggrid').innerHTML = more.map(function (x) { return card(x, kind); }).join(''); else mw.hidden = true;
    });
  }

  function lightbox(grid, getList) {
    var lb = d.createElement('div'); lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Media viewer');
    lb.innerHTML = '<div class="lb__bar"><span class="lb__n" aria-live="polite"></span><button type="button" class="lb__btn lb__x" aria-label="Close"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div>' +
      '<div class="lb__stage"><button type="button" class="lb__btn lb__prev" aria-label="Previous"><i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button><div class="lb__media"></div><button type="button" class="lb__btn lb__next" aria-label="Next"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button></div><p class="lb__cap"></p>';
    d.body.appendChild(lb);
    var cur = 0, opener = null, media = lb.querySelector('.lb__media');
    function show(i) {
      var l = getList(); cur = (i + l.length) % l.length; var m = l[cur];
      if (m.type === 'video' && m.src) media.innerHTML = '<video controls autoplay playsinline poster="' + esc(m.poster || '') + '" src="' + esc(m.src) + '"></video>';
      else if (m.type === 'video') media.innerHTML = '<div class="lb__soon"><img src="' + esc(m.poster) + '" alt=""><span><i class="fa-solid fa-film" aria-hidden="true"></i> Video coming soon</span></div>';
      else media.innerHTML = '<img src="' + esc(m.src) + '" alt="' + esc(m.caption) + '">';
      lb.querySelector('.lb__n').textContent = (cur + 1) + ' / ' + l.length;
      lb.querySelector('.lb__cap').textContent = m.caption || '';
    }
    function open(i, from) { opener = from; show(i); lb.classList.add('is-on'); d.body.classList.add('no-scroll'); lb.querySelector('.lb__x').focus(); }
    function close() { lb.classList.remove('is-on'); d.body.classList.remove('no-scroll'); media.innerHTML = ''; if (opener) opener.focus(); }
    grid.addEventListener('click', function (e) { var b = e.target.closest('.mitem'); if (b) open(+b.dataset.i, b); });
    lb.querySelector('.lb__x').addEventListener('click', close);
    lb.querySelector('.lb__prev').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.lb__next').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb__stage')) close(); });
    d.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-on')) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') show(cur - 1); else if (e.key === 'ArrowRight') show(cur + 1);
      else if (e.key === 'Tab') { var f = lb.querySelectorAll('button'); var a = f[0], z = f[f.length - 1]; if (e.shiftKey && d.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && d.activeElement === z) { e.preventDefault(); a.focus(); } }
    });
  }

  var list = d.getElementById('galleryTabs'); if (list) initList(list);
  var det = d.getElementById('galleryDetail'); if (det) initDetail(det);
})();
