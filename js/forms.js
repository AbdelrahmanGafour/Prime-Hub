/* Prime Hub Trading — forms (training / service / contact)
   There is no backend: after validation the visitor gets a ready-to-send WhatsApp message and mailto draft.
   Features: inline errors, aria-invalid, honeypot, success state, ?course= preselect, quote-list summary on contact. */
(function () {
  'use strict';
  var d = document;
  var WA = '201090009508', MAIL = 'info@primehubeg.com';
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var NAMES = { training: 'Training course request', service: 'Service request', contact: 'Message' };

  function digits(s) { return (s || '').replace(/\D/g, ''); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function fieldOf(el) { return el.closest('.field'); }
  function validateField(el) {
    var v = (el.value || '').trim(), ok = true;
    if (el.required && !v) ok = false;
    else if (v && el.type === 'email' && !EMAIL_RE.test(v)) ok = false;
    else if (v && el.type === 'tel' && (digits(v).length < 8 || digits(v).length > 15)) ok = false;
    var f = fieldOf(el); if (!f) return ok;
    f.classList.toggle('is-invalid', !ok);
    el.setAttribute('aria-invalid', ok ? 'false' : 'true');
    var err = d.getElementById(el.id + '-e');
    if (err) { if (!ok) el.setAttribute('aria-describedby', err.id); else el.removeAttribute('aria-describedby'); }
    return ok;
  }

  function label(el) {
    var l = el.id && d.querySelector('label[for="' + el.id + '"]');
    return l ? l.childNodes[0].textContent.replace(/\*/g, '').trim() : el.name;
  }
  function valueText(el) {
    if (el.tagName === 'SELECT') return el.options[el.selectedIndex] ? el.options[el.selectedIndex].text : '';
    return (el.value || '').trim();
  }

  function buildMessage(form, type) {
    var lines = ['Hello Prime Hub Trading, ' + NAMES[type].toLowerCase() + ' from the website:', ''];
    Array.prototype.forEach.call(form.querySelectorAll('input,select,textarea'), function (el) {
      if (!el.name || el.name === 'website' || el.type === 'hidden') return;
      var v = valueText(el); if (!v || (el.tagName === 'SELECT' && !el.value)) return;
      if (el.name === 'message' && type === 'contact') return;
      lines.push(label(el) + ': ' + v);
    });
    var msg = form.querySelector('[name="message"]');
    if (type === 'contact' && msg && msg.value.trim()) { lines.push('', msg.value.trim()); }
    return lines.join('\n');
  }

  function showSuccess(form, type, message) {
    var box = d.getElementById(form.id + '-success'); if (!box) return;
    var phone = (form.querySelector('[name="phone"]') || {}).value || '';
    var subject = NAMES[type] + ' - Prime Hub website';
    var wa = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(message);
    var mail = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(message);
    box.innerHTML = '<h3><i class="fa-solid fa-circle-check" aria-hidden="true"></i>Your request is ready</h3>' +
      '<p>Send it to our team with one tap. We reply within 24 hours' + (phone ? ' on ' + esc(phone) : '') + '.</p>' +
      '<p><a class="btn btn--wa" href="' + wa + '" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Send on WhatsApp</a>' +
      '<a class="btn btn--primary" href="' + mail + '"><i class="fa-regular fa-envelope" aria-hidden="true"></i> Send by email</a>' +
      '<button class="btn btn--ghost" type="button" data-copy><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy details</button></p>' +
      '<p><button class="link-arrow" type="button" data-again style="background:none;border:0;cursor:pointer;padding:0">Edit my request</button></p>';
    box.classList.add('is-on'); form.classList.add('is-sent');
    box.querySelector('[data-copy]').addEventListener('click', function (e) {
      var b = e.currentTarget;
      (navigator.clipboard ? navigator.clipboard.writeText(message) : Promise.reject()).then(function () { if (window.PH) PH.toast('Details copied'); b.textContent = 'Copied'; }, function () { if (window.PH) PH.toast('Copy is not available on this browser'); });
    });
    box.querySelector('[data-again]').addEventListener('click', function () { box.classList.remove('is-on'); form.classList.remove('is-sent'); form.querySelector('input,select,textarea').focus(); });
    box.focus(); box.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' });
  }

  function init(form) {
    var type = form.getAttribute('data-form');
    var controls = Array.prototype.slice.call(form.querySelectorAll('.input,.select,.textarea'));
    controls.forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value || el.required) { el.__touched = true; validateField(el); } });
      el.addEventListener('input', function () { if (el.__touched) validateField(el); });
      el.addEventListener('change', function () { el.__touched = true; validateField(el); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var hp = form.querySelector('.hp'); if (hp && hp.value) { form.reset(); return; }   // bot
      var bad = controls.filter(function (el) { el.__touched = true; return !validateField(el); });
      var banner = form.querySelector('.form-banner'); if (banner) banner.classList.toggle('is-on', bad.length > 0);
      if (bad.length) { bad[0].focus(); return; }
      showSuccess(form, type, buildMessage(form, type));
    });

    /* training: ?course=cad-cam preselects the course */
    var qs = new URLSearchParams(location.search);
    if (type === 'training' && qs.get('course')) {
      var sel = form.querySelector('[name="course"]'); if (sel) { sel.value = qs.get('course'); if (sel.value !== qs.get('course')) sel.value = ''; }
    }
    if (type === 'contact' && qs.get('brand')) {
      var slugify = function (t) { return t.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); };
      var bs = form.querySelector('[name="brand"]'), tp = form.querySelector('[name="topic"]'), ms = form.querySelector('[name="message"]');
      if (bs) Array.prototype.forEach.call(bs.options, function (o) { if (o.value && slugify(o.value) === qs.get('brand')) { bs.value = o.value; if (tp && !tp.value) tp.value = 'pricing'; if (ms && !ms.value) ms.value = 'I would like a quote for ' + o.value + ' products.'; } });
    }
    if (type === 'service') {
      ['brand', 'model'].forEach(function (k) { var el = form.querySelector('[name="' + k + '"]'); if (el && qs.get(k)) el.value = qs.get(k); });
    }
  }

  /* contact: quote-list summary + prefilled message */
  function quoteSummary() {
    var box = d.getElementById('quoteSummary'), form = d.querySelector('form[data-form="contact"]');
    if (!box || !window.PHQuote) return;
    var msg = form && form.querySelector('[name="message"]'), topic = form && form.querySelector('[name="topic"]');
    var prefilled = '';
    function render() {
      var items = PHQuote.items();
      if (!items.length) { box.hidden = true; box.innerHTML = ''; if (msg && msg.value === prefilled && prefilled) msg.value = ''; prefilled = ''; return; }
      box.hidden = false;
      box.innerHTML = '<h3 class="h4"><i class="fa-solid fa-clipboard-list" aria-hidden="true"></i>Your quote list (' + PHQuote.count() + ' items)</h3><ul>' +
        items.map(function (i) { return '<li><span>' + esc(i.name) + (i.model ? ' <small>(' + esc(i.model) + ')</small>' : '') + '</span><span>' + esc(i.brand) + ' · x ' + i.qty + '</span></li>'; }).join('') +
        '</ul><p style="margin:12px 0 0"><button class="btn btn--ghost btn--sm" type="button" id="editQuote">Edit list</button></p>';
      box.querySelector('#editQuote').addEventListener('click', function () { PHQuote.open(); });
      if (msg && (!msg.value || msg.value === prefilled)) { prefilled = 'I would like a quote for:\n' + PHQuote.text(); msg.value = prefilled; }
      if (topic && !topic.value) topic.value = topic.querySelector('option[data-quote]') ? topic.querySelector('option[data-quote]').value : topic.value;
    }
    render(); PHQuote.onChange(render);
  }

  d.addEventListener('DOMContentLoaded', function () {
    d.querySelectorAll('form[data-form]').forEach(init);
    quoteSummary();
  });
})();
