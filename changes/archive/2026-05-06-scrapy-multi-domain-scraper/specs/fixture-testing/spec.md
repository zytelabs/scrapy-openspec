## ADDED Requirements

### Requirement: Fixtures are saved with the correct page object class
The `scrapy savefixture` command SHALL be run with the fully-qualified class
name of the page object being tested. Fixtures SHALL NOT be saved under a
different domain's page object class name.

#### Scenario: Fixture directory matches page object class
- **WHEN** `scrapy savefixture specs.pages.cclonline_com.CclonlineProductPage <url>` is run
- **THEN** the fixture is saved to `tests/fixtures/specs.pages.cclonline_com.CclonlineProductPage/test-N/`

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
