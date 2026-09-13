#!/usr/bin/env python3
"""Assemble the client-facing pages into a folder you can host on your own domain.

The published previews live at claude.ai artifact URLs. Those are fine for your
own review but they tell the client where the work came from, and they break if
an artifact ever moves. This produces a self-contained bundle with:

  - every page wrapped as a proper standalone HTML document
  - all cross-links rewritten to relative paths
  - the shared-checklist code swapped for plain browser storage

    python3 concierge/tools/build-client-package.py

Writes concierge/client-package/. Drag that folder onto Cloudflare Pages or
Netlify and the whole set is live under your own domain.
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "client-package"

# published artifact -> path inside the bundle
LINKS = {
    "c1fa816f-c08c-4568-be67-013d9e157f16": "index.html",       # proposal
    "d2566ef2-2c60-4a89-aba4-2ceb44a7983a": "kickoff.html",
    "0c3a6e3f-4d6d-40f8-a214-7e59623bc691": "costs.html",
    "9b9b12fa-1e42-4482-bbe0-5aef291e3353": "playbook.html",
    "4f8ff4f4-d161-4632-859b-d2aadab216c9": "demo.html",
    "5e73815a-efff-4283-beb8-4ec08d4976c2": "ops.html",
    "d419450d-e6b0-42c6-82a9-ad296b669c84": "site/index.html",
}

PAGES = {
    "proposal/index.html": "index.html",
    "kickoff/index.html": "kickoff.html",
    "costs/index.html": "costs.html",
    "playbook/index.html": "playbook.html",
    "demo/index.html": "demo.html",
    "ops/index.html": "ops.html",
}

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head}
<style>
:root{{color-scheme:light dark}}
body{{margin:0}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
</head>
<body>
{body}
</body>
</html>
"""

# The checklist shares state through the publishing platform. Off-platform there
# is nothing to share through, so it keeps each person's ticks in their browser.
DB_LOADER_OLD = """/* Shared state, so both sides see the same list. The page works without it. */
(async function(){
  try {
    db = await claude.use('db');
  } catch (e) { db = null; }
  if (!db) {
    setStatus('Working offline — your ticks are visible to you only, and will not be saved.', true);
    return;
  }
  db.collection('checklist').onSnapshot(function(snap){
    var next = {};
    snap.docs.forEach(function(d){
      var v = d.data();
      if (v && v.done) next[d.id] = true;
    });
    state = next;
    render();
  }, function(){
    setStatus('Lost the connection to the shared list. Reload to pick it back up.', true);
  });
})();"""

DB_LOADER_NEW = """/* Ticks are kept in this browser. They are not shared between people —
   whoever is tracking progress should own one copy of this page. */
var STORE = 'brhc-kickoff';
function save(){
  try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {}
}
(function(){
  try {
    var raw = localStorage.getItem(STORE);
    if (raw) { state = JSON.parse(raw) || {}; render(); }
  } catch (e) {
    setStatus('This browser is blocking saved data, so your ticks will not persist.', true);
  }
})();"""

CLICK_OLD = """  if (db) {
    db.doc('checklist/' + id).set({ done: next, at: Date.now() }).catch(function(){
      setStatus('That tick did not save. Check your connection and try again.', true);
    });
  }"""
CLICK_NEW = """  save();"""


def rewrite_links(html: str, depth: int = 0) -> str:
    prefix = "../" * depth
    for artifact_id, target in LINKS.items():
        html = html.replace(
            "https://claude.ai/code/artifact/" + artifact_id, prefix + target
        )
    # Anything still pointing at an artifact is a link we forgot to map.
    leftover = re.findall(r"https://claude\.ai/\S*", html)
    if leftover:
        raise SystemExit("Unmapped artifact link: " + leftover[0])
    return html


def build_page(src: str, dest: str) -> None:
    html = (ROOT / src).read_text()

    if src == "kickoff/index.html":
        for old, new in ((DB_LOADER_OLD, DB_LOADER_NEW), (CLICK_OLD, CLICK_NEW)):
            if old not in html:
                raise SystemExit("Checklist storage block not found — " + src)
            html = html.replace(old, new)
        # state is replaced wholesale on load, so the click handler must persist
        html = html.replace("var db = null;", "")

    html = rewrite_links(html)

    head, _, body = html.partition("</style>")
    (OUT / dest).write_text(SHELL.format(head=head.strip() + "\n</style>", body=body.strip()))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for src, dest in PAGES.items():
        build_page(src, dest)

    # The marketing site is already a standalone document set.
    shutil.copytree(ROOT / "site", OUT / "site",
                    ignore=shutil.ignore_patterns("build", "tools", "api", "*.md"))

    (OUT / "READ-ME-FIRST.txt").write_text(
        "Baton Rouge Home Concierge — client package\n"
        "===========================================\n\n"
        "Open index.html to start. Everything links from there.\n\n"
        "  index.html      The proposal. Send this link.\n"
        "  demo.html       Member / ops / contractor walkthrough\n"
        "  ops.html        The working dispatch console\n"
        "  site/           The landing page and contractor recruiting page\n"
        "  costs.html      What the software would cost, itemised\n"
        "  kickoff.html    What we need from you before we start\n"
        "  playbook.html   Coordinator operating manual\n\n"
        "TO PUT IT ONLINE\n"
        "  Drag this whole folder onto https://pages.cloudflare.com (or\n"
        "  https://app.netlify.com/drop). Both are free. You get a URL in\n"
        "  about a minute, and can point your own domain at it after.\n\n"
        "BEFORE YOU SEND IT\n"
        "  playbook.html is the deliverable sold with 'Coordinator hire &\n"
        "  train' ($2,500). It is not linked from the proposal. Delete the\n"
        "  file if you would rather not hand it over before the engagement.\n\n"
        "  kickoff.html keeps its ticks in whoever's browser opens it —\n"
        "  they are not shared between you and the client.\n"
    )
    print("wrote", OUT)
    for p in sorted(OUT.rglob("*")):
        if p.is_file():
            print("   ", p.relative_to(OUT))


if __name__ == "__main__":
    main()
