/**
 * OPTIONAL — you do not need this to launch.
 *
 * Stripe Payment Links (see SETUP.md step 4) cover everything this does, with
 * no server to run. Reach for this only when you need to pre-fill a session
 * from your own form, apply referral credits, or write the signup into your
 * own database at the moment of purchase.
 *
 * Deploys as a Vercel serverless function at /api/create-checkout-session.
 * Requires:  npm install stripe
 * Requires:  STRIPE_SECRET_KEY set as an environment variable (never in a file
 *            inside this folder — everything here is publicly readable).
 */

const Stripe = require('stripe');

/* Price IDs from your Stripe dashboard (price_..., not prod_...). */
const PRICES = {
  founding: process.env.STRIPE_PRICE_FOUNDING,
  annual: process.env.STRIPE_PRICE_ANNUAL,
  monthly: process.env.STRIPE_PRICE_MONTHLY
};

module.exports = async function handler(req, res) {
  const plan = (req.query && req.query.plan) || 'founding';
  const price = PRICES[plan];

  if (!price) {
    res.status(400).json({ error: 'Unknown plan: ' + plan });
    return;
  }
  if (!process.env.STRIPE_SECRET_KEY) {
    res.status(500).json({ error: 'STRIPE_SECRET_KEY is not set' });
    return;
  }

  const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
  const origin =
    req.headers.origin ||
    (req.headers.host ? 'https://' + req.headers.host : '');

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price: price, quantity: 1 }],

      /* The property address is the whole point of collecting anything. */
      billing_address_collection: 'required',
      shipping_address_collection: { allowed_countries: ['US'] },
      phone_number_collection: { enabled: true },

      custom_fields: [
        {
          key: 'access_notes',
          label: { type: 'custom', custom: 'Gate code or access notes' },
          type: 'text',
          optional: true
        },
        {
          key: 'referral',
          label: { type: 'custom', custom: 'How did you hear about us?' },
          type: 'dropdown',
          dropdown: {
            options: [
              { label: 'A neighbor', value: 'neighbor' },
              { label: 'Facebook or Nextdoor', value: 'social' },
              { label: 'My realtor', value: 'realtor' },
              { label: 'Google', value: 'google' },
              { label: 'Mail', value: 'mail' },
              { label: 'Somewhere else', value: 'other' }
            ]
          }
        },
        {
          key: 'existing_issue',
          label: { type: 'custom', custom: 'Anything already broken?' },
          type: 'text',
          optional: true
        }
      ],

      subscription_data: { metadata: { plan: plan } },
      allow_promotion_codes: true,
      success_url: origin + '/?welcome=1',
      cancel_url: origin + '/#pricing'
    });

    res.writeHead(303, { Location: session.url });
    res.end();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
