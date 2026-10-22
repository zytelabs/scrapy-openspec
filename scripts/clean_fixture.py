"""Clean saved scrapy-poet fixtures with clear-html for selector development.

Usage: python scripts/clean_fixture.py tests/fixtures/<PageObject>/test-N [...]

For each fixture, reads inputs/<Response>-body.html (HttpResponse for WebPage,
BrowserResponse for BrowserPage) and writes alongside it:

- <Response>-body-clean.html: readable HTML for finding content. Do not
  write selectors against it: clear-html drops class/id attributes and
  renames tags. Selectors target the raw <Response>-body.html.
- <Response>-body.txt: plain text for populating output.json

JSON bodies (e.g. Shopify products.json) and XML documents such as sitemaps
are skipped: read them directly.
This script never fetches a page; it only reads files savefixture wrote.
"""

import json
import re
import sys
from pathlib import Path

from clear_html import clean_node, cleaned_node_to_html, cleaned_node_to_text
from lxml.html import document_fromstring

XML_DECLARATION = re.compile(r"^\s*<\?xml[^>]*\?>", re.IGNORECASE)
XML_ROOTS = ("<urlset", "<sitemapindex", "<rss", "<feed")


def clean_fixture(fixture_dir: Path) -> None:
    inputs = fixture_dir / "inputs"
    bodies = sorted(
        p for p in inputs.glob("*-body.html") if not p.name.endswith("-clean.html")
    )
    if not bodies:
        raise SystemExit(f"{inputs}: no *-body.html found; was savefixture run?")

    for body in bodies:
        prefix = body.name.removesuffix("-body.html")
        # Decode as UTF-8 ourselves so lxml doesn't fall back to Latin-1
        # when the document has no charset declaration.
        text = body.read_bytes().decode("utf-8", errors="replace")
        if text.lstrip().startswith(("{", "[")):
            print(f"{body}: JSON body, skipped (read it directly)")
            continue
        # lxml rejects str input that carries an encoding declaration, and
        # XHTML pages sometimes start with one, so drop it before parsing.
        text = XML_DECLARATION.sub("", text, count=1)
        if text.lstrip().lower().startswith(XML_ROOTS):
            print(f"{body}: XML document (e.g. sitemap), skipped (read it directly)")
            continue

        url = None
        info = inputs / f"{prefix}-info.json"
        if info.exists():
            url = json.loads(info.read_text()).get("url")

        node = clean_node(document_fromstring(text), url)
        clean_path = inputs / f"{prefix}-body-clean.html"
        text_path = inputs / f"{prefix}-body.txt"
        clean_path.write_text(cleaned_node_to_html(node), encoding="utf-8")
        text_path.write_text(cleaned_node_to_text(node) or "", encoding="utf-8")
        print(f"{body}: wrote {clean_path.name}, {text_path.name}")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for arg in sys.argv[1:]:
        clean_fixture(Path(arg))


if __name__ == "__main__":
    main()
