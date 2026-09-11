# Launching this site

Static HTML. No build step, no framework, no npm install. Everything
configurable lives in `assets/config.js`.

```
site/
  index.html              homeowner landing page
  pros.html               contractor recruiting + application
  assets/config.js        ← the only file you have to edit
  assets/styles.css
  assets/app.js
  api/create-checkout-session.js   optional, see step 5
```

---

## 1. Put the site online (15 minutes)

Any static host works. In rough order of least friction:

- **Cloudflare Pages** — drag the `site/` folder onto
  [pages.cloudflare.com](https://pages.cloudflare.com). Free, fast, done.
- **Netlify** — drag-and-drop at [app.netlify.com/drop](https://app.netlify.com/drop).
- **Vercel** — `npx vercel --prod` from inside `site/`. Required if you want
  step 5.

Point your domain at it in the host's dashboard. Buy the domain wherever;
Cloudflare is cheapest and does not upsell you.

## 2. Get a phone number (20 minutes)

[OpenPhone](https://openphone.com) — around $15/user/month, gives you a real
Baton Rouge number that rings on your cell, supports texting, and has a shared
inbox so a coordinator can take it over later without changing the number.

Put it in `config.js` as both `phone` (formatted for display) and `phoneE164`
(`+1225...`, for the tap-to-call links).

**Do this before anything else.** The phone number *is* the product. The
website is a brochure for it.

## 3. Create the Stripe products (30 minutes)

In the [Stripe dashboard](https://dashboard.stripe.com), under **Product
catalog**, create one product — "Home Concierge Membership" — with three
prices:

| Price | Amount | Billing |
| --- | --- | --- |
| Monthly | $39.00 | Recurring, monthly |
| Annual | $399.00 | Recurring, yearly |
| Founding annual | $299.00 | Recurring, yearly |

The founding price is a separate price on the same product, so a founding
member stays on $299 at renewal. That is deliberate — you promised them a
locked rate on the site. If you would rather they roll to $399 after year one,
use a coupon on the annual price instead of a separate price, and change the
wording on the pricing section.

## 4. Create Payment Links (15 minutes)

**Payment links → Create link**, one for each of the three prices.

On each link, turn on:

- **Collect customers' addresses → Billing + Shipping.** Label the shipping
  address "Property address" in the custom text. You need the address of the
  house, and it is not always the billing address.
- **Phone number** — required. This is how they will contact you and how you
  will recognize them when they text.
- **Custom fields** (add these three):
  - `Gate code or access notes` — optional text
  - `How did you hear about us?` — dropdown: Neighbor, Facebook/Nextdoor,
    Realtor, Google, Direct mail, Other
  - `Anything already broken?` — optional text. People will tell you, and it
    gives you a reason to text them on day one.
- **After payment → Redirect** to a thank-you page or back to your site.

Copy each `https://buy.stripe.com/...` URL into `config.js`:

```js
checkout: {
  founding: 'https://buy.stripe.com/...',
  annual:   'https://buy.stripe.com/...',
  monthly:  'https://buy.stripe.com/...'
}
```

Then set `PREVIEW: false` and redeploy. You can now take money.

Also turn on, in Stripe **Settings → Billing**:

- **Customer portal** — so members cancel and update cards themselves. You
  promised "cancel any time, without calling anyone" on the FAQ.
- **Smart retries / dunning emails** — failed cards are the quietest source of
  churn there is.

## 5. Optional: your own checkout endpoint

Only worth doing once Payment Links stop fitting — you want to pre-fill the
address from a form, apply referral credits automatically, or write the signup
straight into your own database.

`api/create-checkout-session.js` is a Vercel serverless function that creates a
Checkout Session server-side. To use it:

```bash
cd site
npm init -y
npm install stripe
vercel env add STRIPE_SECRET_KEY    # your sk_live_... key
vercel --prod
```

Then in `config.js` set `checkout.founding` (and the others) to
`/api/create-checkout-session?plan=founding`.

**Never put a secret key in `config.js` or anywhere else in this folder.** It
is a public directory; anything in it is readable by anyone.

## 6. The contractor application form (10 minutes)

`pros.html` posts to whatever you set as `contractorFormAction`. Easiest
options:

- **Formspree** — [formspree.io](https://formspree.io), free tier, emails you
  each submission. Paste the endpoint URL into `config.js`.
- **Tally** or **Google Forms** — if you would rather replace the form
  entirely, link the button out instead.

Until you set it, the form still works: it collects the answers and tells the
applicant to email you.

## 7. Before you run traffic

- [ ] Replace the sample phone number and email everywhere (they only live in
      `config.js`).
- [ ] Set `founding.claimed` to the real count, and keep it honest — update it
      as people sign up.
- [ ] Write a privacy policy and terms page. You are collecting addresses and
      phone numbers; you need one, and Stripe will ask.
- [ ] Have a Louisiana construction attorney read the two footer disclaimers
      and the FAQ answer "Do you do the work yourselves?" against your actual
      contracts. That language is describing your legal structure, so it has to
      match what your agreements actually say.
- [ ] Set up a Google Business Profile. For "handyman baton rouge" type
      searches it matters more than the website.
- [ ] Add analytics — [PostHog](https://posthog.com) free tier is plenty. The
      only number that matters early is: of the people who hit `/#pricing`, how
      many start checkout.

## Running cost

| | |
| --- | --- |
| Hosting | $0 |
| Domain | ~$12/year |
| OpenPhone | ~$15/month |
| Stripe | 2.9% + $0.30 per charge, no monthly fee |
| Formspree | $0 |

Under **$20 a month** to have a website that takes payments.

That figure covers this site and the phone number only — it is not what it
costs to *run* the business. The full Phase 0 operating stack adds Jobber for
dispatch (~$29/mo), QuickBooks, Google Workspace (~$7/user/mo), and Checkr
background screening (~$30 per report, charged per contractor you onboard).
Budget **$150–$300 a month** for all of it before advertising and card
processing, which is the number in the business plan.
