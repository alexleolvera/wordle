# Repository contents

Two unrelated things live here. Read the right one.

## `concierge/` — Baton Rouge Home Concierge

The active project. A membership home-services concierge for Greater Baton
Rouge: homeowners pay a recurring fee for one number to text when something
breaks; vetted contractors do the work, invoice the homeowner directly, and
pay a 10% network fee on jobs sourced through the platform.

Four surfaces, all hand-written HTML/CSS/vanilla JS with **no build step and
no dependencies**:

| Path | What | Status |
| --- | --- | --- |
| `concierge/demo/` | Three-role narrative prototype | Pitch asset |
| `concierge/ops/` | Dispatch console, working job lifecycle | Pitch asset |
| `concierge/site/` | Landing page + contractor recruiting | **Deployable** |
| `concierge/*.md` | Build plan, contractor requirements | Reference |

**Before editing anything under `concierge/`, load the `concierge` skill**
(`.claude/skills/concierge/SKILL.md`). It carries the design tokens, the
pricing figures that have to reconcile across all four surfaces, the legal
language that must not drift, and the workflow to drive before publishing.

Published previews (private to the owner's account):

- Demo — https://claude.ai/code/artifact/4f8ff4f4-d161-4632-859b-d2aadab216c9
- Dispatch console — https://claude.ai/code/artifact/5e73815a-efff-4283-beb8-4ec08d4976c2
- Site — https://claude.ai/code/artifact/d419450d-e6b0-42c6-82a9-ad296b669c84

Republishing keeps those URLs. See the skill for how.

### Open work

The contractor mobile app exists only as three static screens inside
`demo/`. Making it a working prototype — offer with countdown, accept/pass,
close-out with photos and invoice total — is the next piece, and the one that
connects both sides of the marketplace.

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
