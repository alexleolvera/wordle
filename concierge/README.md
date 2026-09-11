# Baton Rouge Home Concierge

A membership home-services concierge for Greater Baton Rouge: homeowners pay a
recurring fee for one number to call when something breaks; a vetted contractor
network does the work, invoices the homeowner directly, and pays a 10% network
fee on jobs sourced through the platform.

## What is here

- **`demo/index.html`** — an interactive prototype covering all three sides of
  the marketplace. Open it in a browser; no build step, no dependencies.
  - **Member** — the text-box request composer, the matching flow, a job
    timeline showing where the membership earns its keep, the home file, and
    the membership screen.
  - **Concierge Ops** — the dispatch board with response-time SLA clocks, the
    contractor bench with compliance state, and the network-fee ledger.
  - **Contractor** — a job offer with a countdown, job list, and the monthly
    earnings view that shows the fee against zero ad spend.
- **`ARCHITECTURE.md`** — how to ship this to iOS, iPadOS, Android and the web
  from one codebase, what to build in what order, what it costs, and the two
  App Store rules that will cause a rejection.

## Note on the demo data

Every member, contractor, address, price and rating in the prototype is
fabricated for illustration. Nothing in it is a real business or a real quote.
