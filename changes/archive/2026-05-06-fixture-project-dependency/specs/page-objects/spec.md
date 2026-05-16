## ADDED Requirements

### Requirement: Stub page objects must be created before saving fixtures
Page object files with `pass` field stubs MUST be created and importable by
the Scrapy project before `scrapy savefixture` is run. The command resolves
the page object class by importing it, so a missing or unimportable class will
cause the command to fail.

#### Scenario: savefixture fails without stub page object
- **WHEN** `scrapy savefixture specs.pages.example_com.ExampleProductPage <url>` is run
- **THEN** if `ExampleProductPage` does not exist the command raises an ImportError and no fixture is saved

#### Scenario: Stub page object is sufficient for savefixture
- **WHEN** a page object exists with all fields returning `pass`
- **THEN** `scrapy savefixture` runs successfully and saves the fixture
