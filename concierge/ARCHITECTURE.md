# Baton Rouge Home Concierge — build plan

How to ship one product to iPhone, iPad, Android, and the web without building
it three times.

---

## 1. The recommendation

**Expo (React Native + React Native Web), TypeScript, one repository.**

One codebase compiles to a native iOS app, a native iPadOS app, a native
Android app, and a real website. Not a wrapper around a web page — genuine
native views on the app stores, and a separately-rendered web build for
`brhomeconcierge.com`.

| Surface | How it ships |
| --- | --- |
| iPhone / iPad | Expo → native build → App Store (one universal binary) |
| Android | Expo → native build → Play Store |
| Website | `expo export --platform web` → static site on Vercel |
| Ops console | Same repo, but a **separate web-only app** (see §3) |

### Why not the alternatives

**Flutter.** Excellent, genuinely fast. Wrong call here because the hiring pool
in Baton Rouge and remote-contract pool for React/React Native is an order of
magnitude deeper than for Dart, and because the rest of this stack (Stripe,
the marketing site, the ops console) is JavaScript either way. Don't run two
languages in a company this size.

**Native iOS + native Android separately.** Two codebases, two engineers, two
release cycles, for an app whose hardest problem is scheduling logic rather
than graphics. Roughly doubles cost to launch for no user-visible gain.

**Web-only PWA, no app stores.** Cheapest, and honestly defensible for year
one — but push notifications are the product. "Your pro is 30 minutes out,"
"your quote is ready," "your HVAC service is due" are the messages that keep a
$39/month membership from feeling invisible. iOS web push exists now but is
fragile and requires the user to add the site to their home screen first. And
a member who cannot find an icon on their phone forgets they are paying you.

**No-code (Glide, Bubble, FlutterFlow).** Legitimate for the pilot, and worth
considering if the goal is 25 founding members by day 30 rather than a
sellable asset. But the dispatch board is the real product, it will get
weird and specific fast, and you cannot sell a company whose core system you
cannot export.

### What to actually do first

Do not build the app first. **The first 100 members do not need one.**

- **Days 1–30:** marketing site + Stripe Checkout + a shared phone number
  (OpenPhone) + Jobber for dispatch. No custom software at all.
- **Days 31–90:** keep running on that. Log every request in a spreadsheet
  shaped like the eventual database. You are buying product requirements.
- **Around 100–150 members:** build the ops console first — it is where your
  time goes and where margin leaks.
- **Around 250–350 members:** build the member app, when notifications and the
  home file are worth more than the build cost.

The demo in `demo/` exists to sell the vision to a customer today. Shipping it
is a separate decision from making it.

---

## 2. Stack

```
apps/
  mobile/      Expo (React Native + RN Web) — member app + contractor app
  web/         Next.js — marketing site, signup, Stripe checkout, member portal
  ops/         Next.js — concierge dispatch console (desktop, internal)
packages/
  api/         tRPC routers — one typed contract for all three clients
  db/          Prisma schema + migrations
  ui/          shared tokens, primitives
```

| Layer | Choice | Why |
| --- | --- | --- |
| Client | Expo SDK, TypeScript | iOS/iPadOS/Android/web from one source |
| Web | Next.js on Vercel | SEO matters — "handyman baton rouge" is a real query |
| API | tRPC on the same Next.js deploy | End-to-end types, no separate backend to run |
| Database | Postgres (Neon or Supabase) + Prisma | Relational from day one; this is a scheduling app |
| Auth | Clerk | Phone-number sign-in, which is how this audience thinks |
| Payments | Stripe Billing + Customer Portal | Subscriptions, dunning, and cancellation you don't write |
| Messaging | Twilio (or OpenPhone API) | One BR number; inbound SMS becomes a request row |
| Push | Expo Notifications | One API across APNs and FCM |
| Files | Cloudflare R2 or S3 | Job photos, COIs, inspection reports |
| Background jobs | Inngest or Trigger.dev | Maintenance reminders, SLA escalation, fee invoicing |
| Error tracking | Sentry | |
| Analytics | PostHog | Funnel from signup → first request is the number that matters |

### Cost at ~350 members

Roughly **$250–$450/month** all-in for infrastructure, plus Stripe's
2.9% + $0.30 and Twilio per-message. The only line that scales meaningfully
with members is Twilio.

---

## 3. Three clients, not one

This is the most important architectural decision in the document.

**Member app** — phone-first. Expo. Ships to both app stores and to the web.

**Contractor app** — phone-first, and it is *not* a mode of the member app.
Different login, different data, different notification behavior (a job offer
must ring through Do Not Disturb; a maintenance reminder must not). Same Expo
project, separate entry point and separate store listing. Two apps on the
stores, one codebase.

**Ops console** — desktop web only. Do not build this in React Native.
Dispatchers live in a keyboard-driven, dense, multi-column, many-tabs-open
interface. React Native Web fights you on every one of those. Plain Next.js +
TanStack Table.

---

## 4. Data model, in brief

```
Member ──< Property ──< Asset          (HVAC, roof, water heater — the moat)
                    └──< ServiceRequest ──< Quote ──< Job ──< NetworkFee
Contractor ──< ContractorDoc           (COI, W-9, license — with expiry dates)
            └──< Offer                 (sent, accepted, passed, expired)
Membership (Stripe subscription mirror)
```

Two things to get right on day one, because retrofitting them is painful:

1. **`Asset` is a first-class table, not a JSON blob on Property.** Every
   asset carries install year, expected life, and last service date. The
   maintenance reminder engine is a nightly job over this table, and those
   reminders are how you get from 3 jobs per member per year to 4.

2. **`NetworkFee` is its own row with its own lifecycle** (accrued → invoiced
   → paid → written off). A 10% fee you cannot age and chase is a 0% fee.
   Ties to `Job.invoiceTotal`, which the contractor reports at close-out.

Also: `ContractorDoc.expiresAt` drives an automatic suspension. A contractor
whose certificate of insurance lapses should stop receiving offers without
anyone remembering to check.

---

## 5. App Store review — the two things that will bite you

**Apple 3.1.1 (in-app purchase).** Apple takes 15–30% of digital subscriptions
sold inside an iOS app. A $39/month membership sold through Stripe in the app
will be rejected.

The way out: this membership is largely a **service consumed outside the app**
(a human coordinates a physical repair at a physical house), which is
"physical goods and services" under 3.1.3(e) and exempt. Two-step approach:

1. Sell the membership **on the website only.** The app signs existing members
   in and does not mention pricing, upgrades, or a purchase path anywhere.
   This is the Netflix/Spotify pattern and reviewers accept it readily.
2. Once you have volume, apply for the **External Purchase Link** entitlement,
   or argue the physical-services exemption directly with a reviewer note.

Budget for one rejection. It is routine, and the fix is usually removing a
single "Upgrade" button from a settings screen.

**Guideline 4.2 (minimum functionality).** An app that is mostly a contact
form gets rejected as "not enough to be an app." The home file, the job
timeline, and push notifications are what clear this bar — which is another
reason not to ship the app until those are real.

Also plan for: a **demo account** in App Store Connect review notes (reviewers
cannot get past a phone-OTP login without one), an ATT-free privacy manifest,
and a real privacy policy URL.

### iPad specifically

Ship it as a **universal app** — same binary, adaptive layout. On iPad the
member app should use a split view (request list on the left, detail on the
right), which in Expo means React Navigation's two-pane layout behind a width
breakpoint. It is a day of work, not a separate app, and it makes the app
usable for the landlord/property-manager segment, who will be on iPads.

---

## 6. Build sequence

**Phase 0 — no code (weeks 1–12).** Squarespace or Framer site, Stripe
Payment Link, OpenPhone number, Jobber for dispatch, Google Sheet for the
contractor bench. Validate that people stay subscribed. Roughly $200/month.

**Phase 1 — ops console (weeks 13–20).** Next.js, Postgres, the data model
above. Twilio inbound SMS creates a request row. Replaces the spreadsheet and
half of Jobber. This is where the operator's hours come back.

**Phase 2 — contractor app (weeks 21–28).** Push-notified job offers with a
countdown, accept/pass, close-out with photos and invoice total. Ship it
before the member app: it is what makes the fee collectible and the response
times fast, and contractors tolerate a rougher v1 than homeowners do.

**Phase 3 — member app (weeks 29–40).** Request composer, job timeline, home
file, membership management. Both stores, plus the web build at
`app.brhomeconcierge.com`.

**Phase 4 — property manager portal.** Multi-property, tenant-initiated
requests, per-property billing. This is the $99–$149/property/month product
and it is mostly a permissions layer over what already exists.

### Rough cost to build

| Phase | Scope | Contract build | Timeline |
| --- | --- | --- | --- |
| 0 | No-code stack | $3–6k | 2 weeks |
| 1 | Ops console | $25–40k | 8 weeks |
| 2 | Contractor app | $20–35k | 8 weeks |
| 3 | Member app (iOS/iPad/Android/web) | $35–55k | 12 weeks |

Phases 1–3 together land near **$80–130k** at agency rates, or roughly
$55–75k with one strong senior contractor working with AI tooling.

Do not read that against the $35–50k launch budget in the business plan and
conclude the software is unaffordable. That budget funds Phase 0 — entity,
legal, insurance, branding, the marketing site, and working capital — where
software is a rounding error. Phases 1–3 are a year-two and year-three
decision, funded out of membership revenue once it exists. On the plan's own
model, year two throws off roughly $183k of EBITDA, which is what pays for the
ops console and the contractor app. **Phase 0 is what you should actually be
paying for in the next 90 days.**

---

## 7. Notes that outrank the technology

- **The legal structure is a product requirement, not a footnote.** The
  homeowner contracts with and pays the contractor; the platform invoices the
  contractor a network fee. Build it that way in the schema — a `Quote` belongs
  to a Contractor and is addressed to a Member; the platform never appears as
  a party. If the app ever lets the platform quote work, the licensing exposure
  described in the business plan becomes real. Have a Louisiana construction
  attorney read the actual agreements before the first paid job.
- **Do not put the membership price in the mobile app.** See §5.
- **Nothing here should block texting.** SMS is the interface; the app is a
  nicer surface over the same inbox. If the app ever becomes the only way in,
  the product got worse.
