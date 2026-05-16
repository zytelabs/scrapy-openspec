## Context

This project scrapes product data from multiple e-commerce domains using Scrapy,
scrapy-poet, and scrapy-zyte-api. The architecture must support adding new domains
without changing spider logic. The stack was chosen to use the Zyte ecosystem
(scrapy-poet for page-object injection, scrapy-zyte-api for managed HTTP) with
fully custom item dataclasses rather than extending `zyte_common_items`.

## Goals / Non-Goals

**Goals**
- Single spider that routes requests to the correct domain-specific page object automatically
- Fixture-based tests per page object, generated from real HTTP responses
- Clear conventions for naming, file structure, and configuration that scale to N domains

**Non-Goals**
- Dynamic URL discovery (all start URLs are explicitly configured)
- JavaScript rendering (Zyte API handles this at the HTTP layer)
- Distributed crawling or job queuing

## Decisions

### Custom items over zyte_common_items extension
**Decision:** Use plain `@attrs.define` dataclasses.
**Rationale:** `zyte_common_items` imposes a fixed schema and pulls in the full Zyte
extraction stack. Custom items keep the data model lean and fully under project control.
**Alternative considered:** Extending `Product` and `ProductList` from `zyte_common_items`.
Rejected because it couples the project to Zyte's schema decisions and adds unnecessary
fields.

### scrapy-poet addon pattern over manual middleware config
**Decision:** Register both addons via `ADDONS`, not `DOWNLOADER_MIDDLEWARES`/`SPIDER_MIDDLEWARES`.
**Rationale:** The addon classes handle all wiring internally, including the
fingerprinter wrapping order between poet and zyte-api. Manual configuration
duplicates logic and can break silently when package internals change.

### Domain-grouped page objects with domain-prefixed class names
**Decision:** One file per domain (`scan_co_uk.py`), two classes per file
(`ScanProductPage`, `ScanProductListPage`).
**Rationale:** Grouping by domain reflects how selectors are scoped — a selector
change for scan.co.uk only affects `scan_co_uk.py`. Domain-prefixed names prevent
class name collisions across modules and make fixture directories unambiguous.

### Items injected directly into callbacks, not page objects
**Decision:** Type-hint callbacks with item classes (`ProductList`, `Product`).
**Rationale:** Spiders become domain-agnostic. scrapy-poet resolves the correct page
object via `handle_urls` and calls `to_item()`. Adding a domain requires no spider changes.
**Alternative considered:** Type-hinting with page object classes. Rejected because it
couples the spider to specific domains.

### async def start() with urls list over start_urls
**Decision:** `async def start()` iterating over a `urls: list` class attribute.
**Rationale:** `start_urls` is synchronous and does not compose well with async Scrapy.
A `urls` list makes start URLs explicit, easy to extend, and overridable per-run.

### Fixture cleaning script for LLM-assisted selector development
**Decision:** Strip HTML noise into a clean HTML file and a plain text file after
saving each fixture.
**Rationale:** Raw fixture HTML is often 100–700KB. LLMs used to generate selectors
or populate `output.json` consume significantly fewer tokens against the cleaned versions
(typically 50–95% smaller).

## Risks / Trade-offs

- **handle_urls pattern specificity** → Overly broad patterns (e.g. `cclonline.com/*/`)
  may match unintended URLs. Mitigation: use the most specific path prefix available.
- **Fixture staleness** → Fixtures capture a point-in-time HTML response. Site redesigns
  will break selectors. Mitigation: re-run `savefixture` periodically and update selectors.
- **SQLite concurrency** → SQLite does not support concurrent writes. Mitigation: keep
  `CONCURRENT_REQUESTS` low or use `INSERT OR REPLACE` with a single connection per crawl.

## Open Questions

- Should `ZYTE_API_TRANSPARENT_MODE` be enabled? Currently `False` — spiders opt in explicitly.
- Should the `urls` list be externalised to a config file or database for operational flexibility?
