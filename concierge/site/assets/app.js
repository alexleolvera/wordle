/* Baton Rouge Home Concierge — site behavior. No dependencies. */
(function () {
  'use strict';
  var C = window.BRHC || {};
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- fill in configured text ---------- */
  function fill(sel, fn) {
    Array.prototype.forEach.call(document.querySelectorAll(sel), fn);
  }
  fill('[data-fill]', function (el) {
    var key = el.dataset.fill, v;
    if (key === 'phone') v = C.phone;
    else if (key === 'email') v = C.email;
    else if (key === 'monthly') v = '$' + C.price.monthly;
    else if (key === 'annual') v = '$' + C.price.annual;
    else if (key === 'founding') v = '$' + C.price.founding;
    else if (key === 'foundingLeft') v = String(C.founding.total - C.founding.claimed);
    else if (key === 'foundingTotal') v = String(C.founding.total);
    else if (key === 'year') v = String(new Date().getFullYear());
    if (v != null) el.textContent = v;
  });
  fill('[data-href="phone"]', function (el) { el.href = 'tel:' + C.phoneE164; });
  fill('[data-href="sms"]', function (el) { el.href = 'sms:' + C.phoneE164; });
  fill('[data-href="email"]', function (el) { el.href = 'mailto:' + C.email; });

  /* ---------- preview ribbon ---------- */
  if (C.PREVIEW) {
    var r = document.getElementById('preview');
    if (r) r.hidden = false;
  }

  /* ---------- founding counter ---------- */
  var meter = document.getElementById('meter');
  if (meter && C.founding) {
    var pct = Math.min(100, Math.round((C.founding.claimed / C.founding.total) * 100));
    meter.style.width = pct + '%';
  }

  /* ---------- checkout buttons ---------- */
  fill('[data-buy]', function (el) {
    var url = (C.checkout || {})[el.dataset.buy];
    if (url) {
      el.href = url;
      el.removeAttribute('data-nolink');
    } else {
      el.href = '#pricing';
      el.setAttribute('data-nolink', '1');
    }
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-nolink]');
    if (!b) return;
    e.preventDefault();
    var note = document.getElementById('buynote');
    if (note) {
      note.textContent = 'Checkout is not connected yet. Add your Stripe Payment Links in assets/config.js to take payments.';
      note.className = 'formmsg formmsg--err';
      note.setAttribute('data-on', '1');
      note.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
    }
  });

  /* ---------- hero thread stagger ---------- */
  var msgs = document.querySelectorAll('.thread .msg');
  if (!reduce) {
    Array.prototype.forEach.call(msgs, function (m, i) {
      m.style.animationDelay = (i * 0.34) + 's';
    });
  }

  /* ---------- lists from config ---------- */
  var tradeBox = document.getElementById('trades');
  if (tradeBox && C.trades) {
    tradeBox.innerHTML = C.trades.map(function (t) {
      return '<li class="trade">' + t + '</li>';
    }).join('');
  }
  var areaBox = document.getElementById('areas');
  if (areaBox && C.areas) {
    areaBox.innerHTML = C.areas.map(function (a) {
      return '<li class="area">' + a + '</li>';
    }).join('');
  }

  /* ---------- contractor application ---------- */
  var form = document.getElementById('proform');
  if (form) {
    if (C.contractorFormAction) form.action = C.contractorFormAction;
    form.addEventListener('submit', function (e) {
      var msg = document.getElementById('formmsg');
      if (C.contractorFormAction) return; // let it post normally
      e.preventDefault();
      var data = new FormData(form);
      var trades = data.getAll('trades').join(', ') || 'not specified';
      msg.className = 'formmsg formmsg--ok';
      msg.setAttribute('data-on', '1');
      msg.textContent = 'Thanks, ' + (data.get('company') || 'there') + '. This form is not connected to an inbox yet — '
        + 'email ' + C.email + ' with your company, trades (' + trades + '), license and insurance, and we will set up a call.';
      msg.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
    });
  }
})();
