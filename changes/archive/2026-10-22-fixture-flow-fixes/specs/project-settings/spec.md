## ADDED Requirements

### Requirement: Zyte API key comes from the environment
The Zyte API key SHALL be provided through the `ZYTE_API_KEY` environment
variable, which `scrapy-zyte-api` reads automatically. The key SHALL NOT be
written to `settings.py`, `pyproject.toml`, or any other file in the project.

`scrapy savefixture` and `scrapy crawl` cannot fetch pages without the key. If
it is missing, the developer SHALL be asked to set it. The missing key SHALL NOT
be worked around by removing `scrapy_zyte_api.Addon`, falling back to Scrapy's
default downloader, or fetching pages any other way.

Projects that render with `scrapy-playwright` instead of Zyte API (see the
`scrapy-playwright` spec) do not need the key.

#### Scenario: Key is not stored in the project
- **WHEN** the project files are inspected
- **THEN** no file contains a Zyte API key and `ZYTE_API_KEY` is not assigned in `settings.py`

#### Scenario: Key is missing when saving a fixture
- **WHEN** `scrapy savefixture` fails because `ZYTE_API_KEY` is not set
- **THEN** the developer is asked to set it, and no workaround is attempted

## MODIFIED Requirements

### Requirement: Check for known platform APIs before building HTML page objects
Before implementing HTML selectors for a new domain's listing page, the developer
SHALL probe the site for known e-commerce platform APIs. If a platform API is
detected, it SHALL be used as the start URL and data source for the listing page
object instead of the HTML collection page. The listing page object then parses
JSON via `json.loads(self.response.body)` rather than CSS/XPath selectors.

#### Platform: Shopify
**Detection**: probe through the Scrapy project, never with a direct request
(see `fixture-testing`). Create the stub listing page object with
`@handle_urls("{domain}/products.json")` and save its fixture:

```bash
scrapy savefixture <projectname>.pages.<domain_file>.<Prefix>ProductListPage "https://{domain}/products.json?limit=250"
```

If the saved `inputs/HttpResponse-body.html` is JSON with a `"products"` array,
the store is Shopify and that fixture is the listing page object's fixture. If
`savefixture` fails or the body is anything else, the site is not Shopify:
delete that fixture directory, change `handle_urls` to the HTML listing pattern,
and continue with the HTML approach.

**Start URL**: `{domain}/products.json?limit=250`

**Pagination**: `page=N` — if the response contains exactly 250 items, increment
the `page` parameter by 1. Do NOT use `since_id`: Shopify stores sort products by
"featured" order (not by ID), so `since_id` repeats the same products on every page.
Continue until a page returns fewer than 250 items.

**Product URLs**: construct from the `handle` field — `{base}/products/{handle}`.

**`handle_urls` pattern**: match the API path, e.g. `example.myshopify.com/products.json`
or `www.example.com/products.json`.

```python
@handle_urls("example.com/products.json")
class ExampleProductListPage(WebPage, Returns[ProductList]):
    @field
    def product_urls(self) -> Optional[list]:
        data = json.loads(self.response.body)
        parsed = urlparse(str(self.response.url))
        base = f"{parsed.scheme}://{parsed.netloc}"
        return [f"{base}/products/{p['handle']}" for p in data.get("products", [])] or None

    @field
    def next_page_url(self) -> Optional[str]:
        data = json.loads(self.response.body)
        products = data.get("products", [])
        if len(products) < 250:
            return None
        parsed = urlparse(str(self.response.url))
        params = parse_qs(parsed.query, keep_blank_values=True)
        params["page"] = [str(int(params.get("page", ["1"])[0]) + 1)]
        return urlunparse(parsed._replace(query=urlencode({k: v[0] for k, v in params.items()})))
```

#### Platform: Ecwid
**Detection**: look for `ecwidStoreID` in the HTML listing page's fixture. The
store ID and public token (`public_…`) are embedded in the page's JavaScript
configuration, so search the raw `inputs/HttpResponse-body.html`, not the
`-clean.html` or `.txt` files: clear-html strips the `<script>` tags that hold it.

**Store ID**: extract from `ecwidStoreID = "..."` or from CDN image URLs
(`d2j6dbq0eux0bg.cloudfront.net/images/{storeId}/...`).

**Public token**: search the HTML for `"public_[A-Za-z0-9]+"`. Use the first
match that is not scoped to a named app — or the one under `appsPublicTokens`
if no general token exists.

**Category ID**: visible in the rendered HTML as a class on the product browser
element, e.g. `ecwid-productBrowser-CategoryPage-{categoryId}`.

**Start URL**: `https://app.ecwid.com/api/v3/{storeId}/products?categoryId={categoryId}&enabled=true&limit=100&token={publicToken}`

Once the start URL is known, save the listing page object's fixture against it
with `scrapy savefixture`, like any other page.

**Pagination**: offset-based — if `offset + count < total`, increment `offset`
by `limit` and request the same URL with the new `offset`.

**`handle_urls` pattern**: match the Ecwid API path, e.g.
`app.ecwid.com/api/v3/{storeId}/products`. Add `app.ecwid.com` to
`allowed_domains`.

```python
@handle_urls("app.ecwid.com/api/v3/32430141/products")
class ExampleProductListPage(WebPage, Returns[ProductList]):
    @field
    def product_urls(self) -> Optional[list]:
        data = json.loads(self.response.body)
        return [item["url"] for item in data.get("items", []) if item.get("url")] or None

    @field
    def next_page_url(self) -> Optional[str]:
        data = json.loads(self.response.body)
        offset, count, total, limit = (
            data.get("offset", 0), data.get("count", 0),
            data.get("total", 0), data.get("limit", 100),
        )
        if offset + count < total:
            parsed = urlparse(str(self.response.url))
            params = parse_qs(parsed.query, keep_blank_values=True)
            params["offset"] = [str(offset + limit)]
            return urlunparse(parsed._replace(query=urlencode({k: v[0] for k, v in params.items()})))
        return None
```

#### Scenario: Shopify site uses products.json instead of collection HTML
- **WHEN** a new domain is confirmed to be a Shopify store
- **THEN** the spider start URL is `{domain}/products.json?limit=250` and the listing page object parses JSON — no CSS selectors are written for the listing page

#### Scenario: Ecwid site uses the REST API instead of the storefront HTML
- **WHEN** a new domain embeds `ecwidStoreID` in its HTML
- **THEN** the store ID, category ID, and public token are extracted from the HTML and the spider start URL is the Ecwid REST API endpoint

#### Scenario: Platform detection goes through savefixture
- **WHEN** a site is probed for a Shopify `products.json` endpoint
- **THEN** the probe is a `scrapy savefixture` of the stub listing page object, and no HTTP library, fetch tool, or other direct request is used

#### Scenario: Unknown platform falls back to HTML scraping
- **WHEN** no known platform API is detected
- **THEN** proceed with the standard WebPage HTML approach, switching to BrowserPage if data is missing

### Requirement: Project creation follows a canonical ordered flow
A Scrapy project using this stack MUST be created in the following order.
No step SHALL be attempted before all preceding steps are complete:

1. `scrapy startproject <name> .` — create the Scrapy project, then copy `openspec/scripts/clean_fixture.py` to `scripts/clean_fixture.py`
2. Update `<projectname>/settings.py` — configure addons and discovery (plus the SQLite pipeline only if the user asked for it)
3. Create `<projectname>/items.py` — define `Product` and `ProductList` dataclasses
4. `scrapy genspider` — generate the spider scaffold in `<projectname>/spiders/`, then rename class and file
5. Create page objects with `pass` stubs in `<projectname>/pages/` — one file per domain, classes importable
6. `scrapy savefixture` — save fixture for each page object, then run `python scripts/clean_fixture.py <fixture dir>`
7. **Subagent(s)**: populate `output.json` and implement selectors — one subagent per page object, run in parallel where possible
8. Update spider — add `urls`, `allowed_domains`, and wire callbacks

#### Scenario: savefixture fails if page objects do not exist
- **WHEN** step 6 is attempted before step 5
- **THEN** the command fails with an ImportError

#### Scenario: selectors cannot be written without a fixture
- **WHEN** step 7 is attempted before step 6
- **THEN** there is no fixture HTML for the subagent to develop selectors against

#### Scenario: full flow produces passing tests
- **WHEN** all 8 steps are completed in order
- **THEN** `pytest tests/` passes for all page object fixtures
