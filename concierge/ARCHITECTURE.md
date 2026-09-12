# Baton Rouge Home Concierge — build plan

How to build this without an app store, and how far you can get before you
build anything at all.

---

## 1. The recommendation

**The web, plus SMS. No native apps, no app stores.**

Everything a person touches is either a web page or a text message:

| Who | What they use | Built as |
| --- | --- | --- |
| Prospective member | Marketing site, Stripe checkout | Static site |
| Member, day to day | **Texts a phone number** | Twilio / OpenPhone |
| Member, occasionally | Their home file and job history | Logged-in web page |
| Member, billing | Stripe Customer Portal | Off the shelf |
| **Contractor** | **Texts** — job offers, accept/pass, close-out | Twilio |
| Concierge / dispatcher | Dispatch console | Web app, desktop |

No App Store review. No Play Store. No universal binary. No two codebases.
One deploy, everyone sees it immediately.

### Why SMS is the right channel, not a fallback

This is the decision that makes everything else simpler, and it is worth being
clear that it is not a budget compromise.

**Contractors will not open an app.** A plumber is in a truck, hands dirty,
three jobs behind. An app he has to install, remember, and unlock is friction
he will route around by calling you instead — which puts the work back on your
dispatcher. A text he answers at a red light:

```
BR-2431 · Electrical · No power to half the kitchen
3312 Kenilworth Pkwy · 6.2 mi · wants it today
Est. $200–450 · 3 photos: <link>
Reply Y to accept, N to pass. Expires 4:15p.
```

Zero install, works on every phone he has ever owned, answered in forty
seconds. The countdown-offer screen in the prototype is a prettier version of
something SMS already does better in the field.

**Members in a panic will not hunt for an icon.** Water is coming out from
under the water heater. They want to tell somebody. The thing they already
have open is their messages app. "Text us" has no learning curve and no
install step, and it is the entire product promise.

**Notifications are the one thing a plain website genuinely cannot do.** Web
push on iOS requires the user to add the site to their home screen first and
remains fragile. But every notification this business needs — "your pro is 30
minutes out", "your quote is ready", "your HVAC service is due" — is a text
message, delivered by the same channel the member already uses to reach you.
The notification budget is Twilio, not an app build.

### When to revisit native

One trigger, and it is further out than it feels: **when the member experience
becomes the product.** Browsing the home file, tapping through maintenance
history, an icon on the home screen that keeps the membership visible on a day
nothing is broken. That is a retention play at roughly **500+ members**, and
by then you will know exactly what it needs to do.

Until then, a native app buys you an icon and costs you App Store review, a
subscription-billing fight with Apple (see the appendix), two release cycles,
and roughly double the build. Do not pay that for an icon.

### Why not the other options

**Expo / React Native.** This was the earlier recommendation here, made against
the brief "ship to iPhone, iPad, Android and web." It is the right answer to
that brief. The brief was the problem — this business does not need the app
stores, and dropping them removes more cost and risk than any framework choice
could.

**No-code (Glide, Bubble, Softr).** Genuinely viable for the ops console at
small scale, and worth pricing if the goal is 25 founding members rather than
a sellable asset. The dispatch board will get weird and specific fast, though,
and you cannot sell a company whose core system you cannot export.

**Nothing at all.** The correct answer for the first six months. See §2.

---

## 2. Build nothing first

The first hundred members do not need custom software, and building it before
them is the most expensive mistake available here.

- **Days 1–30.** Marketing site (already built, in `site/`) + Stripe Payment
  Links + one business number on OpenPhone + Jobber for dispatch + a
  spreadsheet for the contractor bench. **Roughly $150–300/month, no custom
  code.**
- **Days 31–90.** Stay on it. Log every request in a spreadsheet shaped like
  the schema in §5. You are not being lazy, you are buying product
  requirements at the lowest price they will ever be available.
- **Around 100–150 members.** Build the dispatch console. This is where the
  operator's hours go and where the 10% fee leaks.
- **Around 250–350 members.** Add the member portal — home file, job history,
  quote approval.
- **500+ members.** Consider native, if and only if retention data says the
  member experience needs to live on a home screen.

---

## 3. Stack

```
apps/
  site/        Static marketing site + signup            (already built)
  ops/         Next.js — dispatch console (desktop web)
  portal/      Next.js — member home file & history      (later)
packages/
  db/          Prisma schema + migrations
  sms/         Message templates, inbound parser, consent handling
```

| Layer | Choice | Why |
| --- | --- | --- |
| Marketing site | Static HTML on Cloudflare Pages | Already built, $0, fast, SEO-friendly |
| Ops console | Next.js on Vercel | Dense desktop tables; server components keep it simple |
| Member portal | Next.js, same deploy | Shares auth and the database |
| Database | Postgres (Neon or Supabase) | Relational from day one; this is a scheduling app |
| Auth | Clerk, phone-number sign-in | This audience thinks in phone numbers, not passwords |
| Payments | Stripe Billing + Customer Portal | Subscriptions, dunning, self-serve cancellation |
| **Messaging** | **Twilio** | Two-way SMS, MMS for job photos, delivery receipts |
| Files | Cloudflare R2 or S3 | Job photos, certificates of insurance, inspection reports |
| Background jobs | Inngest or Trigger.dev | Maintenance reminders, SLA escalation, fee invoicing, COI expiry |
| Error tracking | Sentry | |
| Analytics | PostHog | Signup → first request is the funnel that matters |

### Running cost at ~350 members

Roughly **$250–$400/month** of infrastructure, plus Stripe's 2.9% + $0.30 and
Twilio per message. SMS is the only line that scales meaningfully with member
count, and it is cents per message.

---

## 4. SMS is infrastructure, treat it that way

The channel carrying your entire product deserves more thought than "we'll
send texts."

### Register before you launch

US carriers require **A2P 10DLC registration** — a brand and a campaign — for
application-to-person messaging on a normal 10-digit number. Unregistered
traffic gets filtered or blocked, quietly, which looks exactly like your
business not working. Fees are modest; the delay is the issue, so budget a
couple of weeks and start it early. A toll-free number is a separate
verification path with different tradeoffs. Your messaging provider walks you
through both.

### Consent and compliance, in the product not the policy

- Collect explicit SMS consent at signup. The Stripe checkout already collects
  a phone number — add the consent language there and store the timestamp.
- Handle `STOP`, `UNSUBSCRIBE` and `HELP`. Twilio does this automatically; do
  not defeat it.
- Contractors consent separately, in the vendor agreement.
- Respect quiet hours for anything not a genuine emergency.
- **Store consent as a row, not a checkbox in someone's memory.** See §5.

### Message design

Two-way SMS means parsing replies. Keep the vocabulary tiny and forgiving:

| Inbound | Means |
| --- | --- |
| `Y`, `YES`, `1`, `accept` | Contractor accepts the offer |
| `N`, `NO`, `2`, `pass` | Contractor passes |
| `DONE 385` | Job complete, invoiced $385 — accrues the fee |
| anything else | Route to a human in the console |

That last row is the important one. **Never make a person guess the magic
word.** Anything unparsed becomes a message in the dispatch console for the
coordinator to read, which is the same place member texts already land.

### Offers expire, and expiry is a state change

An offer that times out re-routes to the next contractor on the bench
automatically. This is the single biggest operational win over calling
around, and it is a background job plus a status field — cheap to build,
large effect on fill rate.

---

## 5. Data model

```
Member ──< Property ──< Asset          (HVAC, roof, water heater — the moat)
                    └──< ServiceRequest ──< Quote ──< Job ──< NetworkFee
Contractor ──< ContractorDoc           (COI, W-9, license — with expiry dates)
            └──< Offer                 (sent, accepted, passed, expired)
Message                                (every inbound and outbound SMS)
ConsentRecord                          (who agreed to be texted, and when)
Membership                             (Stripe subscription mirror)
```

Five things to get right on day one, because retrofitting them hurts:

1. **`Asset` is a first-class table, not JSON on Property.** Every asset
   carries install year, expected life, last service date. The maintenance
   reminder engine is a nightly job over this table, and those reminders are
   how you get from 3 jobs per member per year to 4.

2. **`NetworkFee` has its own lifecycle** (accrued → invoiced → paid → written
   off) and records **collected** separately from **invoiced**. A fee you
   cannot age and chase is a 0% fee, and a fee charged on money the contractor
   never received is how you lose a good vendor over $40.

3. **`ContractorDoc.expiresAt` is a date column** that drives automatic
   suspension. A vendor whose certificate of insurance lapses stops receiving
   offers without anyone remembering to check.

4. **`Message` stores every text, both directions, linked to the request.**
   This is your audit trail, your dispute evidence, and the thread the
   coordinator reads in the console. It is also what makes the member portal
   possible later without re-architecting.

5. **`ConsentRecord` is a row with a timestamp and the exact language shown.**
   Carrier complaints and TCPA questions are answered with records, not
   recollections.

---

## 6. Build sequence and cost

| Phase | Scope | Contract build | Timeline |
| --- | --- | --- | --- |
| 0 | No custom software — site, phone, Jobber, spreadsheet | $3–6k | 2 weeks |
| 1 | Dispatch console + SMS pipeline + contractor bench | $25–40k | 8–10 weeks |
| 2 | Member portal — home file, history, quote approval | $10–18k | 4–6 weeks |
| 3 | Property-manager accounts — multi-property, per-property billing | $12–20k | 5–6 weeks |

Phases 1–2 together land near **$35–58k** at agency rates, or roughly
**$25–40k** with one strong senior contractor working with AI tooling.

That is **roughly half** what the native route in this document's earlier
version would have cost, and the difference is almost entirely app-store
overhead that bought nothing this business needs.

Do not read those figures against the $35–50k launch budget in the business
plan and conclude the software is unaffordable. That budget funds Phase 0 —
entity, legal, insurance, branding, the marketing site, working capital —
where software is a rounding error. Phase 1 is a year-two decision funded out
of membership revenue. On the plan's own model year two throws off roughly
$183k of EBITDA, which is what pays for the console.

**Phase 0 is what you should actually be paying for in the next 90 days.**

---

## 7. Notes that outrank the technology

- **The legal structure is a product requirement, not a footnote.** The
  homeowner contracts with and pays the contractor; the platform invoices the
  contractor a network fee. Build it that way in the schema — a `Quote`
  belongs to a Contractor and is addressed to a Member; the platform is never
  a party. If the software ever lets the platform quote work, the licensing
  exposure described in the business plan becomes real. Have a Louisiana
  construction attorney read the actual agreements before the first paid job.
- **Nothing should ever block texting.** SMS is the interface. Every web
  surface is a nicer window onto the same conversation. If the portal ever
  becomes the only way to reach you, the product got worse.
- **Own your own accounts.** Domain, Stripe, Twilio, database, repository —
  in the client's name, with the developer invited. A vendor holding the keys
  is the most common way these projects go wrong.

---

## Appendix — if you ever do go native

Keep this filed. It stops being theoretical only if §1's 500-member trigger
fires.

**The route** would be Expo (React Native + React Native Web), TypeScript, one
repository, shipping iPhone/iPad/Android from one codebase while the web build
serves the same code. The ops console stays a separate desktop web app
regardless; React Native Web fights dense keyboard-driven tables.

**Apple guideline 3.1.1** is the problem to plan for. Apple takes 15–30% of
digital subscriptions sold inside an iOS app, and a $39/month membership sold
through Stripe in-app will be rejected. The way through: sell membership on
the website only, and let the app sign existing members in without mentioning
price, upgrades, or a purchase path anywhere — the Netflix/Spotify pattern.
This membership also has a real argument for the physical-services exemption
under 3.1.3(e), since a human coordinates a physical repair at a physical
house. Budget for one rejection regardless; the fix is usually deleting one
"Upgrade" button.

**Guideline 4.2** — an app that is mostly a contact form gets rejected as not
enough to be an app. The home file, the job timeline and notifications are
what clear that bar, which is another reason this only makes sense once the
member experience is substantial.

Also plan for a demo account in App Store Connect review notes (reviewers
cannot get past phone-OTP login without one), a privacy manifest, and a real
privacy policy URL. On iPad, ship a universal binary with a split view —
request list left, detail right — behind a width breakpoint. That is a day of
work, not a second app, and it matters for the landlord segment.
