# fixture-testing Specification

## Purpose
TBD - created by archiving change scrapy-multi-domain-scraper. Update Purpose after archive.
## Requirements
### Requirement: scrapy savefixture is the only permitted way to save fixtures
Fixtures SHALL be saved exclusively using the `scrapy savefixture` CLI command.
Writing custom scripts, Python code, or any other mechanism to download and save
fixture files is NOT permitted. `scrapy savefixture` boots the full Scrapy and
scrapy-poet stack, ensuring the fixture is saved in exactly the format that
`pytest-web-poet` expects.

```bash
# Correct
scrapy savefixture specs.pages.scan_co_uk.ScanProductPage https://www.scan.co.uk/products/...

# Never acceptable
python scripts/save_fixture.py ...
requests.get(url) + manual file writing
```

#### Scenario: Custom fixture script is not used
- **WHEN** a fixture needs to be saved
- **THEN** `scrapy savefixture` is run — no custom scripts or HTTP clients are used

### Requirement: Fixtures are saved with the correct page object class
The Scrapy project MUST be fully initialised and the target page object class
MUST exist as a stub before `scrapy savefixture` is run. `scrapy savefixture`
is a Scrapy CLI command that boots the full crawler stack to download a real
HTTP response — it is not a standalone HTTP client. The command SHALL be run
with the fully-qualified class name of the page object being tested. Fixtures
SHALL NOT be saved under a different domain's page object class name.

#### Scenario: Project must exist before savefixture
- **WHEN** `scrapy savefixture` is run in a new project
- **THEN** the Scrapy project, settings, and stub page object class must already exist or the command will fail

#### Scenario: Fixture directory matches page object class
- **WHEN** `scrapy savefixture <projectname>.pages.cclonline_com.CclonlineProductPage <url>` is run
- **THEN** the fixture is saved to `tests/fixtures/<projectname>.pages.cclonline_com.CclonlineProductPage/test-N/`

### Requirement: Fixtures are cleaned before selector development
After saving a fixture, the `scripts/clean_fixture.py` helper SHALL be run to
produce two additional files:
- `HttpResponse-body-clean.html` — noise-free HTML for selector development
- `HttpResponse-body.txt` — plain text for populating `output.json`

#### Scenario: Cleaner reduces HTML size significantly
- **WHEN** `clean_fixture.py` is run on a fixture
- **THEN** the clean HTML is smaller than the original and the plain text is at least 80% smaller

### Requirement: output.json matches selector output exactly
The `output.json` expected values SHALL match exactly what the implemented
selectors return — not a manually summarised or truncated version. Truncation
causes test failures.

#### Scenario: Truncated description causes test failure
- **WHEN** `output.json` contains a shorter description than the selector extracts
- **THEN** the `description` test case fails

### Requirement: Fixtures are stored under the page object class name
Fixture directories SHALL be named after the fully-qualified page object class.
When a page object is renamed, the fixture directory MUST be renamed to match.

#### Scenario: Renamed class requires renamed fixture directory
- **WHEN** a page object class is renamed from `ProductPage` to `ScanProductPage`
- **THEN** the fixture directory is renamed from `...ProductPage` to `...ScanProductPage`

### Requirement: Subagents populate output.json and implement selectors
Steps 7 (populate `output.json`) and 8 (implement selectors) SHALL be delegated
to subagents rather than performed by the main agent. Each subagent is responsible
for a single page object and SHALL:

1. Read `HttpResponse-body.txt` to extract expected field values and write `output.json`
2. Read `HttpResponse-body-clean.html` to develop CSS/XPath selectors for each field
3. Update the page object with the implemented selectors
4. Run `pytest` for that fixture and confirm all tests pass

#### Scenario: Subagent handles one page object end to end
- **WHEN** a subagent is spawned for a page object
- **THEN** it reads the plain text and clean HTML fixtures, writes output.json, implements selectors, and confirms tests pass

### Requirement: Subagents run in parallel when multiple page objects exist
Subagents SHALL run in parallel — one per page object — when a domain has more
than one page object or when multiple domains are being set up simultaneously.

#### Scenario: Two page objects processed in parallel
- **WHEN** both `ScanProductPage` and `ScanProductListPage` need fixtures populated
- **THEN** two subagents are spawned concurrently, one per page object

#### Scenario: Single page object uses a single subagent
- **WHEN** only one page object needs its fixture populated
- **THEN** a single subagent is used without parallelism

