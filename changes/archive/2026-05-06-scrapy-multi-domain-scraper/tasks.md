## 1. Project Setup

- [ ] 1.1 Run `scrapy startproject` in the project root
- [ ] 1.2 Add `scrapy-poet`, `scrapy-zyte-api`, `price-parser`, and `attrs` to `pyproject.toml` dependencies
- [ ] 1.3 Configure `ADDONS` in `settings.py` with `scrapy_poet.Addon` (300) and `scrapy_zyte_api.Addon` (500)
- [ ] 1.4 Set `SCRAPY_POET_DISCOVER = ["<project>.pages"]` in `settings.py`
- [ ] 1.5 Add `[tool.pytest.ini_options]` with `pythonpath = ["."]` to `pyproject.toml`
- [ ] 1.6 Create `<project>/pages/` package with `__init__.py`

## 2. Custom Items

- [ ] 2.1 Ask the user whether to extend `zyte_common_items` or create custom `attrs` items
- [ ] 2.2 Define `Product` with `url` (required) and standard optional fields in `items.py`
- [ ] 2.3 Define `ProductList` with `url`, `product_urls`, and `next_page_url` only in `items.py`

## 3. Page Objects (per domain)

- [ ] 3.1 Create `<project>/pages/<domain>.py` (one file per domain)
- [ ] 3.2 Name classes with domain prefix: `<Domain>ProductPage`, `<Domain>ProductListPage`
- [ ] 3.3 Inherit from `WebPage` and `Returns[Item]` for each class
- [ ] 3.4 Decorate each class with `@handle_urls("<domain>/<path-prefix>/")` — never empty string
- [ ] 3.5 Define `url` field returning `str(self.response.url)`
- [ ] 3.6 Add `pass` stubs for all other fields matching the item schema

## 4. Spider

- [ ] 4.1 Run `scrapy genspider` to scaffold the spider, then rename class and file to reflect scope
- [ ] 4.2 Replace `start_urls` with a `urls: list` class attribute
- [ ] 4.3 Implement `async def start()` iterating over `self.urls` with `scrapy.Request`
- [ ] 4.4 Implement `async def parse(self, response, product_list: ProductList)` using `response.follow`
- [ ] 4.5 Implement `async def parse_product(self, _, product: Product)` yielding the product
- [ ] 4.6 Import only item classes — no page object imports in the spider
- [ ] 4.7 Add all domains to `allowed_domains`

## 5. SQLite Pipeline

- [ ] 5.1 Implement `SQLitePipeline` with `from_crawler` reading `SQLITE_DB_PATH`
- [ ] 5.2 Implement `open_spider(self)`, `close_spider(self)`, `process_item(self, item)` — no `spider` arg
- [ ] 5.3 Filter to `Product` items only; pass everything else through
- [ ] 5.4 Serialise `images` and `breadcrumbs` list fields as JSON strings
- [ ] 5.5 Register pipeline in `settings.py` `ITEM_PIPELINES`

## 6. Fixture Testing Workflow (per page object)

- [ ] 6.1 Create `scripts/clean_fixture.py` to produce clean HTML and plain text from fixture HTML
- [ ] 6.2 Run `scrapy savefixture <module.ClassName> <url>` with the correct fully-qualified class name
- [ ] 6.3 Run `clean_fixture.py` on the saved fixture
- [ ] 6.4 Use plain text to populate `output.json` with expected field values
- [ ] 6.5 Use clean HTML to develop and verify CSS/XPath selectors
- [ ] 6.6 Implement selectors in the page object fields
- [ ] 6.7 Run `pytest tests/` and fix any mismatches between selectors and `output.json`

## 7. Adding a New Domain

- [ ] 7.1 Create `<project>/pages/<new_domain>.py` with `<Domain>ProductPage` and `<Domain>ProductListPage`
- [ ] 7.2 Set real `@handle_urls` patterns for each class
- [ ] 7.3 Save and clean fixtures for both page objects
- [ ] 7.4 Populate `output.json` and implement selectors
- [ ] 7.5 Add new domain to spider `allowed_domains` and list URL to `urls`
- [ ] 7.6 Rename spider class and file if the current name no longer reflects scope
- [ ] 7.7 Run full test suite to confirm no regressions
