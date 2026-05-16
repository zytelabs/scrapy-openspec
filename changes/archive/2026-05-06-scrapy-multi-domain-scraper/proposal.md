## Why

We need a structured, extensible Scrapy project that can scrape product data from multiple e-commerce domains without changing the spider logic when new domains are added. The corrections captured during development reveal a clear set of patterns and conventions that should be codified as a reusable spec.

## What Changes

- Scrapy project configured via the `ADDONS` setting using `scrapy_poet.Addon` and `scrapy_zyte_api.Addon`
- Custom item dataclasses (`Product`, `ProductList`) defined with `attrs`, independent of `zyte_common_items`
- Page objects grouped by domain in `specs/pages/<domain>.py`, named with domain prefix (e.g. `ScanProductPage`)
- Page objects registered via `@handle_urls` with real URL patterns — never empty string
- Spiders import items only, not page objects — scrapy-poet resolves the correct page object via the `handle_urls` registry
- All spider callbacks are `async def`; `start_urls` replaced by `async def start()` iterating a `urls` list
- SQLite pipeline stores scraped `Product` items
- Fixture-based tests using `scrapy savefixture` + `web-poet` pytest plugin
- Helper script (`scripts/clean_fixture.py`) strips HTML noise from fixtures to reduce LLM token usage

## Capabilities

### New Capabilities

- `project-settings`: Scrapy settings configuration using addons, discovery, and pipeline
- `custom-items`: Custom `attrs`-based item dataclasses (`Product`, `ProductList`)
- `page-objects`: Domain-grouped page objects with `@handle_urls`, `@field`, and `WebPage`
- `spider`: Async multi-domain spider with `urls` list and item-typed callbacks
- `sqlite-pipeline`: Pipeline to persist scraped `Product` items to SQLite
- `fixture-testing`: Workflow for saving, cleaning, and testing fixtures per page object

### Modified Capabilities

## Impact

- `specs/settings.py` — ADDONS, SCRAPY_POET_DISCOVER, SQLITE_DB_PATH
- `specs/items.py` — `Product`, `ProductList` dataclasses
- `specs/pages/<domain>.py` — one file per domain, two classes per file
- `specs/spiders/gpu.py` — single multi-domain spider
- `specs/pipelines.py` — `SQLitePipeline`
- `scripts/clean_fixture.py` — fixture HTML cleaner
- `tests/fixtures/` — per-class fixture directories
- `pyproject.toml` — pytest `pythonpath` config
