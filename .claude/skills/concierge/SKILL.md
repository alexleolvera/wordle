---
name: concierge
description: Conventions for the Baton Rouge Home Concierge project — the three prototypes and the deployable site under concierge/. Use when editing, extending or publishing anything in that directory: the member/ops/contractor demo, the dispatch console, or the landing and contractor pages. Covers the shared design tokens, the no-build-step rule, where pricing lives, the legal language that must not drift, and how to verify a change before publishing.
---

# Baton Rouge Home Concierge

A membership home-services concierge for Greater Baton Rouge. Homeowners pay a
recurring fee for one number to text when something breaks; vetted contractors
do the work, **invoice the homeowner directly**, and pay a 10% network fee on
jobs sourced through the platform.

## What is where

| Path | What it is | Status |
| --- | --- | --- |
| `concierge/demo/index.html` | Three-role narrative prototype (member, ops, contractor) | Pitch asset |
| `concierge/ops/index.html` | Dispatch console with a working job lifecycle | Pitch asset, mutable state |
| `concierge/site/` | Homeowner landing page + contractor recruiting page | **Deployable** |
| `concierge/proposal/` | Client-facing launch proposal | Sales asset |
| `concierge/kickoff/` | Shared client requirements checklist (`db`) | Sales asset |
| `concierge/ARCHITECTURE.md` | Build plan for iOS/iPadOS/Android/web | Reference |
| `concierge/CONTRACTOR-NETWORK.md` | Vendor data and operating requirements | Reference |

## Hard rules

**Architecture is web plus SMS — no native apps, no app stores.** Contractors
receive job offers by text, not in an app; members text in. The App Store
route survives as an appendix in `ARCHITECTURE.md` and as a priced second
option in the proposal, gated on 500+ members. Do not reintroduce native app
work without being asked.

**Present options, do not decide for the client.** The proposal's section 03
prices both paths side by side and names the honest reasons to pick the apps
anyway. Recommendations are stated as recommendations; the choice stays with
the person whose money it is.

**No build step, no dependencies, anywhere.** Every file is hand-written HTML,
CSS and vanilla JS that runs by opening it. No npm, no framework, no bundler,
no TypeScript. The prototypes are single self-contained files on purpose — they
get published as Artifacts and shown on a phone in a meeting. Do not introduce
a toolchain without being asked.

**The site's only editable surface is `site/assets/config.js`.** Phone number,
email, Stripe Payment Link URLs, pricing, trades, service areas, and the
founding counter all live there. If a change to the site requires editing HTML
to change a value, that value belongs in config instead.

**Never advertise a trade the contractor bench does not cover.** The landing
page promises "at least two vetted providers in every major trade." The ten
launch categories are in `CONTRACTOR-NETWORK.md` §6. Adding a chip to
`config.trades` is a promise.

**The founding counter ships honest.** `founding.claimed` defaults to `0`
because that is true before launch. Do not seed it with a flattering number.

## Legal language that must not drift

The business model depends on the platform *not* being the contractor. Every
surface has to stay consistent with that, and this is the one category of
change where being clever is a liability:

- The homeowner **contracts with and pays the contractor directly**. The
  platform never quotes construction work, never marks it up, and is not a
  party to that agreement.
- The membership buys **coordination, vetting, matching, quote review and
  accountability** — never labor, materials, or a warranty on the work.
- Contractors are **independent businesses** that set their own prices.
- GMV is **not** platform revenue. Only the 10% fee line is.

Both site pages carry a footer disclaimer saying this. If you change the
product's shape, check those disclaimers still describe it.

## Numbers — one source, and they must reconcile

`$39/month` · `$399/year` · `$299 founding (first 50)` · `10% network fee` ·
`12.5–15%` as the later test rate on new vendors.

These appear across all four surfaces. Before publishing any change that
touches a figure, re-derive the arithmetic rather than eyeballing it — the
prototypes assert totals that must actually add up (147 × $39 = $5,733;
10% of $14,120 = $1,412). A prospect will do this math in the meeting.

Demo data is modelled on the plan's **day-90** state (100–150 members), and
the prototype labels itself that way. The site represents **launch day**. Keep
those two consistent as one timeline.

## Design system

All four surfaces share one token set. Copy it rather than inventing a second.

- **Cypress** `#1F4D3D` — primary. **Brass** `#A8761F` — accent.
- Semantic: good `#2E7D5B`, warn `#A97615`, critical `#A8402F`. Kept separate
  from the accent so SLA and compliance state read at a glance.
- Neutrals are biased slightly green; never a pure mid-grey.
- Type: **Archivo** (display) · **IBM Plex Sans** (UI) · **IBM Plex Mono**
  (IDs, money, timers, uppercase labels).
- Every token is declared on bare `:root`, then redefined under both
  `@media (prefers-color-scheme: dark)` guarded as
  `:root:not([data-theme="light"])` **and** `:root[data-theme="dark"]`. Never
  define a color only inside a media or `[data-theme]` block.

## Verifying before you publish

The prototypes have real interaction, so a visual check is not enough — drive
the workflow. Playwright and Chromium are available:

```js
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
p.on('pageerror', e => console.log('ERR: ' + e.message));
await p.goto('file:///home/user/wordle/concierge/ops/index.html');
// then click through the real path, not just screenshot the first frame
```

For `ops/`, the path that must survive any change is:
triage → send offers → accept → log quote → approve → schedule → close out →
fee appears in the ledger. Three separate bugs have hidden in that chain.

## Publishing

`demo/` and `ops/` publish directly as Artifacts. The site is a full HTML
document, so it needs the wrapper stripped first:

```bash
python3 concierge/site/tools/build-preview.py   # writes site/build/index.html
```

Then publish `site/build/index.html` with `root: concierge/site` and
`assets/styles.css`, `assets/config.js`, `assets/app.js`, `pros.html` as
supporting files. `site/build/` is gitignored — it is a preview artifact, not
source.

Republishing keeps the existing URL. Do not pass a new `favicon` on a
redeploy.

## Capabilities

`kickoff/` is the one page that declares a runtime capability — `db`, so the
client and the consultant tick the same shared checklist. Republishing it
**must** pass `capabilities: {db: {}}` again; omitting it on a redeploy keeps
the stored declaration, but passing a different non-empty set revokes it.
Every other surface is static.

## Not built yet

Nothing is blocked. The contractor screens in `demo/` illustrate the pitch but
are not a roadmap item now that contractors are served by SMS.
