# Contractor network — data and operating requirements

What to collect from every vendor, what blocks activation, how the 10% fee is
calculated and collected, and what all of it looks like in the database.

**This is an operations and data specification, not legal advice and not a
contract.** The network agreement itself has to be drafted by a Louisiana
attorney. This document tells that attorney — and whoever builds the system —
what the business actually needs the agreement to capture.

---

## 1. Why the file matters more than it looks

Three separate risks all land on the same folder of paperwork:

1. **The member's risk.** Someone is letting a stranger into their house
   because you said it was fine. That is the entire product.
2. **Your workers' compensation exposure.** Louisiana's statutory-employer
   rules mean a business that hires an uninsured subcontractor to do work
   within its trade or business can end up responsible for that person's
   comp benefits. The cheapest defense is never routing a job to a vendor
   whose coverage you have not verified — enforced by software, not memory.
3. **Your structural position.** The whole model depends on the contractor
   being an independent business that contracts with the homeowner directly.
   Every field below should be consistent with that story. The moment your
   records read like you are directing the work, you look like the contractor.

So: **an incomplete or expired file is not a paperwork problem. It is a
routing block.**

---

## 2. Collect at application

Captured by the form on `site/pros.html`. Cheap, self-reported, no
verification yet — the point is to decide whether to spend an hour on a call.

| Field | Type | Why you want it |
| --- | --- | --- |
| Company legal name | text | Must match the W-9 later |
| Doing-business-as name | text | What the member will see |
| Primary contact name | text | |
| Mobile number | phone | Where job offers go — the single most important field |
| Email | email | Documents, fee invoices |
| Trades | multi-select | Drives routing |
| License / registration number | text | Verified later against the state |
| GL insurance carrier | text | Verified later against the certificate |
| Workers' comp status | enum: carried / sole proprietor / none | Decides which path they take |
| Crew size | enum | Capacity planning |
| Service area | text or multi-select | Routing by ZIP |
| Weekly spare capacity | enum | How many jobs you can actually send |
| Pricing structure | long text | Service call fee, hourly, minimum, after-hours |
| Re-service answer | long text | The single best predictor of how they behave |
| Years in business | number | |
| References | text | Two other customers, ideally not friends |

**Read the re-service answer first.** A vendor who describes a concrete
process ("I come back within 48 hours, no second trip charge") behaves
differently from one who writes "we always make it right."

---

## 3. Verify before activation

Nothing on this list is self-reported. Every item is a document you hold a copy
of, with an expiry date recorded as a date field, not as text.

| Document | What you record | Blocks activation? |
| --- | --- | --- |
| **W-9** | Legal name, EIN/SSN-last-4, address, entity type | Yes |
| **Certificate of general liability** | Carrier, policy number, limits, effective date, **expiry date**, whether you are named as certificate holder | Yes |
| **Workers' comp certificate** *or* signed sole-proprietor exemption | Carrier, policy number, expiry — or the signed exemption on file | Yes |
| **Trade license** | Type, number, status, **expiry date**, verified against the Louisiana State Licensing Board for Contractors or the relevant state board | Yes, where the trade requires one |
| **Background screening** | Provider, date run, pass/fail, re-run due date, for each person entering homes | Yes |
| **Signed network agreement** | Version signed, date, signatory | Yes |
| **Auto liability** | Carrier, expiry | No — record it, do not block on it |
| **Bank / payment details** | For fee invoicing | No |

### Insurance limits to require

Ask your insurance broker what to set, and expect something in the range of
**$500k–$1M general liability per occurrence** for the trades you route. That
is higher than the $100k Louisiana requires for a home-improvement
registration, and it is the right kind of expensive.

Get yourself listed as a **certificate holder** on each vendor's GL policy so
the carrier notifies you when a policy changes. Vendors will not volunteer
that their coverage lapsed.

### The automatic behaviors

These are the entire reason the dates are structured fields:

- **60 days before expiry** — automated email, vendor and your ops inbox.
- **30 days before expiry** — second email. Vendor shows amber on the bench.
- **On expiry** — vendor status flips to `paused` automatically. No new job
  offers route to them. Jobs already scheduled proceed; you are not cancelling
  on a member over paperwork, but nothing new goes out.
- **Background screening** — re-run every 24 months, same escalation.

Screening runs roughly **$30 per report** (Checkr's basic tier), charged per
person entering homes. At 15 launch vendors that is a few hundred dollars, and
it is the single cheapest line item standing between you and a bad outcome.

The prototype's contractor bench screen shows this working: Tiger Appliance is
paused for a missing W-9, Cypress Roofing shows amber at 21 days to expiry.

---

## 4. What the agreement has to capture

For your attorney. Each of these exists because the business needs it, and
several exist specifically to protect the structure.

**Fee mechanics**
- 10% of the amount the contractor actually **collects** from the member on a
  job sourced through the platform. Collected, not invoiced — a vendor should
  never owe you a fee on money they never got.
- Invoiced monthly in arrears, net 15.
- The contractor **reports every job** sourced through the platform, including
  the invoice total, at close-out. This is the clause the whole revenue stream
  hangs on.
- Define what "sourced through the platform" covers, and for how long. If a
  member calls the plumber directly six months later for a different job, is
  that yours? The defensible answer is a **tail period** — typically 12 months
  from introduction — on that member, disclosed to the vendor plainly.
- Audit right: you may request invoices for jobs at member addresses.

**Independence** — the clauses that keep you out of prime-contractor territory
- Contractor is an independent business, not an employee, agent, partner or
  subcontractor of the platform.
- Contractor contracts with and invoices the homeowner **directly**; the
  platform is not a party to that agreement and does not guarantee payment.
- Contractor sets their own prices, hours, methods and crew.
- Contractor carries their own insurance and licenses.
- Platform does not supervise, direct or control the means and methods of the
  work.
- No exclusivity in either direction.

**Standards**
- Re-service policy, in writing, with a defined window.
- Response window on job offers.
- The quality thresholds (acceptance rate, rating, rework), and what happens
  when they are missed — a conversation, then removal.
- Close-out requirements: before photo, after photo, invoice total.
- Conduct in a member's home; background screening for every person entering.
- Immediate notice to you of any insurance lapse, license action, injury on a
  member's property, or claim.

**Protection**
- Non-solicitation: the contractor will not market their own services to
  platform members outside the platform for the tail period. Have counsel
  scope this carefully — Louisiana is unusually strict about restrictive
  covenants, and an overbroad clause can be worse than none.
- Indemnification, running the right direction: the contractor indemnifies the
  platform for their own work.
- Member data is confidential and may not be sold, shared or used for the
  contractor's own marketing.
- Termination: either side, 30 days, no cause needed.

**Ask your attorney directly:** does this structure — with these clauses,
these disclaimers on the website, and the homeowner contracting with the
contractor — keep the company outside the Louisiana State Licensing Board's
registration and licensing requirements at every job size you intend to
coordinate? Get the answer in writing before the first paid job. If the answer
is no, the fix is to get registered, not to hope.

---

## 5. Data model

The tables the ops console needs. Field names are suggestions; the shape is
the point.

```
Contractor
  id, legal_name, dba, status              -- prospect | verifying | active | paused | removed
  primary_contact, phone, email
  trades[]                                 -- routing key
  service_zips[]                           -- routing key
  weekly_capacity, crew_size
  pricing_notes, reservice_policy
  fee_rate           decimal               -- 0.10 today; per-vendor so you can test 12.5% on new ones
  tail_months        int                   -- default 12
  onboarded_at, agreement_version, agreement_signed_at
  paused_reason, paused_at                 -- set automatically by the doc expiry job

ContractorDoc
  id, contractor_id
  kind               enum                  -- w9 | gl_insurance | workers_comp | wc_exemption
                                           -- | trade_license | background_check | agreement | auto
  file_url
  issuer                                   -- carrier, state board, screening provider
  reference_number                         -- policy no., license no., report id
  effective_at       date
  expires_at         date                  -- NULL only for documents that never expire (W-9)
  verified_by, verified_at                 -- a person checked it, and who
  blocks_activation  bool

ContractorMetric                           -- rolled up nightly, shown on the bench
  contractor_id, period
  offers_sent, offers_accepted, accept_rate
  median_response_minutes
  jobs_completed, gmv, avg_ticket
  rating_avg, rework_count, rework_rate

Offer
  id, service_request_id, contractor_id
  sent_at, expires_at
  status             enum                  -- sent | accepted | passed | expired
  responded_at                             -- feeds median_response_minutes

NetworkFee
  id, job_id, contractor_id
  invoice_total      decimal               -- what the contractor invoiced the member
  collected_total    decimal               -- what they actually collected; fee is on this
  fee_rate, fee_amount
  status             enum                  -- accrued | invoiced | paid | disputed | written_off
  accrued_at, invoiced_at, paid_at
  source             enum                  -- reported_by_contractor | member_confirmed | audited
```

Three rules that are easy to get wrong and painful to retrofit:

1. **`expires_at` is a date column on every document**, never free text. The
   entire compliance automation is one nightly query over it.
2. **`fee_rate` lives on the Contractor row**, not in application code. You
   will test 12.5–15% with new vendors in year two, and you promised the early
   ones their rate would not move. Both facts have to be storable at once.
3. **`NetworkFee` distinguishes invoiced from collected.** A fee calculated on
   money the vendor never received is the fastest way to lose a good vendor
   over $40.

---

## 6. Recruiting the first 15

Target roughly 15 active vendors at launch, from 25–30 conversations, with
**at least two in every major trade** — one plumber is not a network, it is a
single point of failure with a truck.

| Trade | Target active |
| --- | --- |
| Handyman / carpentry | 3 |
| Plumbing | 2 |
| Electrical | 2 |
| HVAC | 2 |
| Paint / drywall | 2 |
| Pressure washing / exterior | 2 |
| Roofing / gutters | 2 |
| Flooring / tile | 2 |
| Appliance repair | 1–2 |
| Locksmith | 1 |

### Where to find them

In rough order of yield: contractors already doing good work for people you
know; the busy ones your realtor and home-inspector contacts recommend;
suppliers' counter staff at plumbing and electrical wholesalers, who know
exactly who is good and who is not; and Google reviews filtered to
small operations with 4.7+ and fewer than 100 reviews — big enough to be real,
small enough to want the work.

### The pitch, in one paragraph

> I sell homeowners a membership. When something breaks they text me instead of
> searching Google. I send you the job already described and photographed, at a
> house where they are expecting you. You quote it, you invoice them directly
> at your price, you keep your own customer relationship. You pay me nothing to
> join, nothing per lead, and nothing on a job you do not win. When you get
> paid, you pay me ten percent. If I stop sending you good work, you stop
> paying me anything.

### What to listen for on the call

- How they answer the re-service question, unprompted.
- Whether they ask about the 10% immediately, or about the members first. Both
  are fine; the second is a better sign.
- Whether their insurance is current **right now**, or "I need to check."
- Whether they have capacity. A vendor with no room will accept your jobs and
  then be late, which is worse than passing.
- Whether they text back. Run the entire recruiting conversation over text if
  you can — it is a free audition for the thing you actually need them to do.

### Red flags

Cash-only. No written estimates. Cannot produce a certificate within 48 hours.
Bad-mouths every other contractor in town. Wants an exclusive. Asks whether
they can charge your members more than their normal rate.

---

## 7. Vendor terms to settle before you recruit

Decide these now, so you say the same thing to vendor one and vendor fifteen:

- **Fee rate.** 10% at launch, for everyone. Early vendors keep 10% forever —
  say so, and put it in the agreement. Test 12.5–15% on vendors onboarded after
  you can prove volume.
- **Response window.** How long a job offer stays live before it rolls to the
  next vendor. Start at 30 minutes during business hours.
- **Routing order.** Best-performing vendor first, or round-robin? Start with
  round-robin inside the trade so everyone gets enough volume to judge, then
  switch to performance-weighted once you have 20+ jobs per vendor.
- **Tail period.** 12 months is defensible and easy to explain.
- **Member discounts.** The business plan floats "preferred contractor
  pricing" as a Priority-tier benefit in year two. It is left out of the
  product, because it contradicts what you are telling contractors here —
  that they set their own prices and you never negotiate their rate down for
  a member. Pick one. Discounted labor is how networks lose their best
  vendors; time-based perks (priority scheduling, walkthroughs) buy the same
  perceived value without touching anyone's rate. If you do want the
  discount, strike the "we never negotiate your rate" line from the
  contractor page before you recruit vendor one — not after.
- **Who eats a bad job.** If a member disputes work and the contractor will not
  fix it, does the membership refund come out of your pocket? Budget for it —
  the financial model calls it a customer recovery reserve. Decide the rule
  before it happens to you, not during.
