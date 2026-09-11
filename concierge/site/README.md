# Site

The Phase 0 website: a homeowner landing page that takes membership payments
through Stripe, and a contractor recruiting page with an application form.

Static HTML, no build step, no dependencies. Everything you need to change
lives in `assets/config.js` — phone number, email, Stripe Payment Link URLs,
pricing, service areas, trades, and the founding-member counter.

**Start with [SETUP.md](SETUP.md).** It walks through hosting, the phone
number, creating the Stripe products and Payment Links, and the checklist to
clear before running traffic. Under $20/month to be open for business.

```
index.html          homeowner landing page
pros.html           contractor recruiting + application
assets/config.js    ← the only file you have to edit
assets/styles.css   shared styles (same design tokens as the /demo prototype)
assets/app.js       config wiring, checkout buttons, form handling
api/                optional Stripe Checkout endpoint — not needed to launch
tools/              generates a preview build; not part of the deployed site
```

While `PREVIEW: true` in the config, the site shows a ribbon saying checkout
and the phone number are placeholders, and the buy buttons explain that
payments are not connected. Set it to `false` once the Stripe links are real.
