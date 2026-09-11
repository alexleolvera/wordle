#!/usr/bin/env python3
"""Generate a preview build of the site for publishing as a Claude Artifact.

The Artifact host supplies its own <!doctype>/<head>/<body> skeleton, so the
entry page must be body content with the <title>/<meta>/<link> tags left inline.
This strips the document wrapper from index.html and writes the result to
build/index.html. Everything else is published unchanged as supporting files.

    python3 tools/build-preview.py

The source files in site/ stay deployable as-is; this only produces the preview.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

html = (ROOT / "index.html").read_text()

# Drop the document wrapper. <title>, <meta> and <link> survive in place — the
# browser hoists them into the head it creates.
for pattern in (
    r"<!doctype html>\s*",
    r"</?html[^>]*>\s*",
    r"</?head>\s*",
    r"</?body>\s*",
    r'<meta charset="utf-8">\s*',
    r'<meta name="viewport"[^>]*>\s*',
):
    html = re.sub(pattern, "", html, flags=re.I)

(BUILD / "index.html").write_text(html.strip() + "\n")
print("wrote", BUILD / "index.html")
