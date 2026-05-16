## MODIFIED Requirements

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
- **WHEN** `scrapy savefixture specs.pages.cclonline_com.CclonlineProductPage <url>` is run
- **THEN** the fixture is saved to `tests/fixtures/specs.pages.cclonline_com.CclonlineProductPage/test-N/`
