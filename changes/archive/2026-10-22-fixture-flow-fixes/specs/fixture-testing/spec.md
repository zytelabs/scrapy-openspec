## MODIFIED Requirements

### Requirement: All page HTML is obtained through the Scrapy project
The agent SHALL NOT fetch page content directly using MCP tools, HTTP libraries,
external API calls, or any other mechanism outside the Scrapy project. If the HTML
of a page is needed — for selector development, page inspection, or any other purpose
— a fixture MUST be saved first using `scrapy savefixture`. The fixture HTML is the
only permitted source of page content during development.

Do NOT:
- Call `mcp__zyte__fetch_http`, `mcp__zyte__render_page`, or any Zyte API MCP tool to retrieve page HTML
- Use `requests`, `httpx`, `aiohttp`, or any HTTP library directly to fetch a page
- Use browser automation or screenshot tools to inspect page structure
- Fetch a page outside the Scrapy project for any reason, including "just to check" the structure

If you need to inspect a page's HTML, save the fixture first, then read the fixture files.

#### Scenario: Agent needs to inspect page HTML
- **WHEN** the agent needs to see the HTML of a page
- **THEN** `scrapy savefixture` is run first and the resulting `inputs/HttpResponse-body-clean.html` is read

#### Scenario: Direct fetch is not used as a shortcut
- **WHEN** a fixture has not yet been saved
- **THEN** the agent does not fetch the page directly — it saves the fixture instead

### Requirement: scrapy savefixture is the only permitted way to save fixtures
`scrapy savefixture` is the ONLY permitted method for saving fixtures. There are
no exceptions. This is a hard rule.

Do NOT:
- Write a custom Python script to download and save fixture files
- Use `requests`, `httpx`, `aiohttp`, or any HTTP client directly
- Use `scrapy crawl` or any other Scrapy command as a substitute
- Create any helper, wrapper, or workaround around `scrapy savefixture`
- Attempt to construct the fixture directory structure manually

If `scrapy savefixture` fails, the correct response is to fix the underlying
problem (missing page object stub, misconfigured project, bad URL) — not to
work around it with a custom script.

```bash
# The only acceptable command
scrapy savefixture base.pages.scan_co_uk.ScanProductPage https://www.scan.co.uk/products/...
```

#### Scenario: Custom fixture script is not used
- **WHEN** a fixture needs to be saved
- **THEN** `scrapy savefixture` is run and nothing else is attempted

#### Scenario: savefixture fails
- **WHEN** `scrapy savefixture` fails
- **THEN** the root cause is diagnosed and fixed — no alternative method is tried

### Requirement: Fixtures are cleaned with clear-html before selector development
After saving a fixture, run the cleaning helper on it:

```bash
python scripts/clean_fixture.py tests/fixtures/<fully-qualified-page-object>/test-N
```

The helper ships with this spec at `openspec/scripts/clean_fixture.py` and SHALL
be copied into the project's `scripts/` directory when the project is created.
It SHALL NOT be rewritten, replaced, or reimplemented per project. The project
SHALL declare `clear-html` as a direct dependency.

The helper processes the saved response with `clear-html` (`clean_node`,
`cleaned_node_to_html`, `cleaned_node_to_text`). `scrapy savefixture` stores the
response input as `test-N/inputs/HttpResponse-body.html` for `WebPage` page
objects and `test-N/inputs/BrowserResponse-body.html` for `BrowserPage` page
objects. The helper writes two files alongside it with the same prefix:
- `inputs/<Response>-body-clean.html` — readable HTML for understanding the page's content and structure
- `inputs/<Response>-body.txt` — plain text for populating `output.json`

The clean HTML is for reading only. clear-html drops `class` and `id`
attributes, renames tags (e.g. `<h1>` becomes `<h2>`), and removes or flattens
wrappers such as `<nav>` and `<div>`, so selectors written against it do not
match the response the page object actually receives.

JSON bodies, such as a Shopify `products.json` fixture, and XML documents, such
as a sitemap used as a listing page, are skipped; read `inputs/HttpResponse-body.html`
directly for those. An XML declaration at the top of an XHTML page is stripped
before cleaning.

The helper operates solely on the saved fixture and never fetches a page. It
decodes the source as UTF-8 to avoid lxml's Latin-1 fallback when an HTML
document lacks an explicit charset declaration.

#### Scenario: Clean HTML is not used for selectors
- **WHEN** a selector is being written for a field
- **THEN** it is developed and checked against the raw `inputs/<Response>-body.html`, not `-clean.html`

#### Scenario: Helper is copied, not rewritten
- **WHEN** a new project is created
- **THEN** `scripts/clean_fixture.py` is a copy of `openspec/scripts/clean_fixture.py`

#### Scenario: BrowserPage fixture is cleaned
- **WHEN** `clean_fixture.py` is run on a fixture saved for a `BrowserPage` page object
- **THEN** `inputs/BrowserResponse-body-clean.html` and `inputs/BrowserResponse-body.txt` are created

#### Scenario: Cleaner uses clear-html on the saved response input
- **WHEN** `clean_fixture.py` is run on a fixture
- **THEN** `inputs/HttpResponse-body-clean.html` and `inputs/HttpResponse-body.txt` are created from `inputs/HttpResponse-body.html` without fetching a URL

### Requirement: Subagents populate output.json and implement selectors
Step 7 of the creation flow (populate `output.json` and implement selectors)
SHALL be delegated to subagents rather than performed by the main agent. Each subagent is responsible
for a single page object and SHALL:

1. Read `inputs/HttpResponse-body.txt` (`BrowserResponse-body.txt` for a `BrowserPage`) to extract expected field values and write `output.json`
2. Use `inputs/HttpResponse-body-clean.html` (`BrowserResponse-body-clean.html` for a `BrowserPage`) to locate each field's content, then develop CSS/XPath selectors against the raw `inputs/HttpResponse-body.html` (`BrowserResponse-body.html`), which is what the page object receives in tests
3. Update the page object with the implemented selectors
4. Run `pytest` for that fixture and confirm all tests pass

#### Scenario: Subagent handles one page object end to end
- **WHEN** a subagent is spawned for a page object
- **THEN** it reads the plain text and clean HTML fixtures, writes output.json, implements selectors, and confirms tests pass
