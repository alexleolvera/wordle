/* ============================================================
   Baton Rouge Home Concierge — site configuration
   Edit this file. Nothing else needs to change to go live.
   ============================================================ */
window.BRHC = {

  /* Set to false when you are ready for real traffic. While true, the site
     shows a preview ribbon and buttons explain that checkout is not wired up.
     Leave it true until the Stripe links below are real. */
  PREVIEW: true,

  /* --- contact ------------------------------------------------ */
  phone: '(225) 555-0142',        // your OpenPhone / Twilio number
  phoneE164: '+12255550142',      // same number, for tel: and sms: links
  email: 'hello@brhomeconcierge.com',

  /* --- Stripe Payment Links ----------------------------------- */
  /* Create these in the Stripe dashboard (see SETUP.md) and paste the
     https://buy.stripe.com/... URLs here. Empty string = not live yet. */
  checkout: {
    founding: '',   // $299 first year, first 50 members
    annual:   '',   // $399 / year
    monthly:  ''    // $39 / month
  },

  /* --- pricing (display only; Stripe is the source of truth) --- */
  price: { monthly: 39, annual: 399, founding: 299 },

  /* --- founding member counter -------------------------------- */
  /* Keep this honest. It is a real cap, not a fake scarcity widget:
     the $299 rate is only viable on a limited cohort. */
  founding: { total: 50, claimed: 19 },

  /* --- contractor application form ---------------------------- */
  /* Paste a Formspree (https://formspree.io) or Tally endpoint here.
     Empty string = the form collects the answers and tells the applicant
     to email you instead. */
  contractorFormAction: '',

  /* --- service area ------------------------------------------- */
  areas: [
    'Baton Rouge', 'Prairieville', 'Gonzales', 'Denham Springs',
    'Central', 'Zachary', 'Baker', 'Watson', 'St. Gabriel', 'Geismar'
  ],

  /* --- trades covered ----------------------------------------- */
  /* Only list what your bench actually covers. The page promises two vetted
     providers in every major trade — do not advertise a trade you cannot fill.
     These match the ten launch categories in CONTRACTOR-NETWORK.md. Add more
     as you sign vendors for them. */
  trades: [
    'Plumbing', 'Electrical', 'HVAC', 'Handyman & carpentry',
    'Painting & drywall', 'Roofing & gutters', 'Gutter cleaning',
    'Pressure washing', 'Appliance repair', 'Locksmith', 'Flooring & tile'
  ]
};
