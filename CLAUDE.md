# Repository contents

Two unrelated things live here. Read the right one.

## `concierge/` — Baton Rouge Home Concierge

The active project. A membership home-services concierge for Greater Baton
Rouge: homeowners pay a recurring fee for one number to text when something
breaks; vetted contractors do the work, invoice the homeowner directly, and
pay a 10% network fee on jobs sourced through the platform.

Eight surfaces, all hand-written HTML/CSS/vanilla JS with **no build step and
no dependencies**:

| Path | What | Status |
| --- | --- | --- |
| `concierge/demo/` | Three-role narrative prototype | Pitch asset |
| `concierge/ops/` | Dispatch console, working job lifecycle | Pitch asset |
| `concierge/site/` | Landing page + contractor recruiting | **Deployable** |
| `concierge/proposal/` | Client-facing launch proposal | Sales asset |
| `concierge/kickoff/` | Shared client requirements checklist | Sales asset, `db` |
| `concierge/costs/` | Line-by-line build estimate breakdown | Sales asset |
| `concierge/playbook/` | Coordinator operating manual | Deliverable |
| `concierge/*.md` | Build plan, contractor requirements | Reference |

**Before editing anything under `concierge/`, load the `concierge` skill**
(`.claude/skills/concierge/SKILL.md`). It carries the design tokens, the
pricing figures that have to reconcile across all four surfaces, the legal
language that must not drift, and the workflow to drive before publishing.

Published previews (private to the owner's account):

- Demo — https://claude.ai/code/artifact/4f8ff4f4-d161-4632-859b-d2aadab216c9
- Dispatch console — https://claude.ai/code/artifact/5e73815a-efff-4283-beb8-4ec08d4976c2
- Site — https://claude.ai/code/artifact/d419450d-e6b0-42c6-82a9-ad296b669c84
- Proposal — https://claude.ai/code/artifact/c1fa816f-c08c-4568-be67-013d9e157f16
- Kickoff checklist — https://claude.ai/code/artifact/d2566ef2-2c60-4a89-aba4-2ceb44a7983a
- Cost breakdown — https://claude.ai/code/artifact/0c3a6e3f-4d6d-40f8-a214-7e59623bc691
- Coordinator playbook — https://claude.ai/code/artifact/9b9b12fa-1e42-4482-bbe0-5aef291e3353

Republishing keeps those URLs. See the skill for how.

`kickoff/` is the only page that declares a runtime capability (`db`), so the
client and the consultant tick the same shared list. Republish it with
`capabilities: {db: {}}` or the stored declaration is revoked.

`proposal/` is Le’Olvera Consulting's pitch to the prospective owner, not part
of the product. Section 03 presents **both** build paths — web and text
(recommended) against native apps — with honest costs and tradeoffs on each,
and names the genuine reasons to choose the apps anyway. Do not reduce it back
to a single recommendation; the client makes that call, not us. Pricing and
the consulting identity live in that file.

**Scope boundary, stated because it is easy to blur:** the client recruits the
contractor bench — their market, their relationships, their vendors. The
engagement supplies the recruiting *kit* (outreach scripts, vendor agreement
requirements, screening checklist, compliance tracker), not the phone calls.
Running the outreach is a separate paid add-on, never bundled into the launch
package. Contractor calls fall to the consultant only under the operate
retainer, and that is dispatching against a bench the client already built.

`playbook/` is the coordinator's daily operating manual and the asset sold
with "Coordinator hire & train" ($2,500). It is written for whoever answers
the texts — the client at first, a hire later — so keep its voice plain and
operational, never salesy. Its thresholds (quote limit, hours, response
targets) are defaults the owner overrides on day one.

Proposal section 05 offers **two ways to run it after launch**: Option A, the
client operates and the engagement advises at $900/month (recommended);
Option B, the consultant operates for 90 days at $2,000/month. Both start
with the same $6,000 Launch Package and both lead to the coordinator hire.
Do not collapse this back to one option.

`costs/` itemises the console build as 60 working days and shows that the
price range is driven by who builds it, not what gets built. **The day counts
and the dollar figures there are the source of truth** — the proposal quotes
them, so change them in `costs/` first and carry them across. Cheaper paths
(offer engine only at $12k–19k, no-code at $3k–8k) are priced there too.

### Open work

`ARCHITECTURE.md` now recommends **web plus SMS, no native apps**. Contractors
take job offers by text rather than in an app, which means the contractor
mobile screens in `demo/` are a pitch illustration, not a roadmap item. If a
working contractor prototype is ever wanted, build it as an SMS thread
simulator rather than an app.

The site is finished on the code side. What remains is account setup the
owner has to do: hosting, an OpenPhone number, and Stripe products plus
Payment Links pasted into `concierge/site/assets/config.js`. Steps are in
`concierge/site/SETUP.md`.

## `wordle.py`

Unrelated leftover from this repository's original purpose. Not part of the
concierge project; leave it alone.

# Conventions

- Work happens on `claude/baton-rouge-concierge-app-gqqv8y`, not `main`.
- Never introduce npm, a framework, or a bundler into `concierge/` without
  being asked. The single-file prototypes are deliberate.
- Playwright and Chromium are available for verification
  (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`). Drive the real interaction
  before publishing; screenshotting the first frame has missed real bugs.
