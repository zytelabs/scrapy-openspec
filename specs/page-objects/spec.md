# page-objects Specification

## Purpose
TBD - created by archiving change scrapy-multi-domain-scraper. Update Purpose after archive.
## Requirements
### Requirement: Page objects are grouped by domain in a single file
All page objects for a given domain SHALL live in a single file named after
that domain (e.g. `<projectname>/pages/scan_co_uk.py`). Separate files per item type
are NOT permitted.

#### Scenario: Domain file contains all page objects for that domain
- **WHEN** a new domain is added
- **THEN** both its product page object and product list page object are defined in one file named after the domain

### Requirement: Page object class names include the domain
Page object class names SHALL be prefixed with the domain name to ensure
uniqueness across modules and unambiguous fixture directory names.

#### Scenario: Classes are uniquely named by domain
- **WHEN** page objects from two domains are imported in the same scope
- **THEN** there are no name collisions (e.g. `ScanProductPage` vs `CclonlineProductPage`)

### Requirement: Page objects use Returns[Item] to declare their item type — never to_item()
Page objects SHALL declare their output item type by subclassing `Returns[<Item>]`
from `web_poet`. Implementing a `to_item()` method is NOT permitted. scrapy-poet
reads the `Returns` generic to determine what item to produce; `to_item()` is an
older pattern that bypasses this mechanism.

#### Scenario: Page object declares item type via Returns
- **WHEN** a page object class is defined
- **THEN** its class signature is `class ScanProductPage(WebPage, Returns[Product])` and no `to_item()` method exists

#### Scenario: to_item() is not defined on any page object
- **WHEN** the page object files are inspected
- **THEN** no page object class defines a `to_item()` method

### Requirement: handle_urls takes a string pattern, not a list
The argument to `@handle_urls` SHALL be a string (or multiple positional strings).
Passing a list (e.g. `[]` or `["scan.co.uk"]`) is not valid and will not register
any URL pattern correctly.

#### Scenario: handle_urls passed a list does not register the pattern
- **WHEN** `@handle_urls([])` or `@handle_urls(["scan.co.uk"])` is used
- **THEN** the pattern is not registered and scrapy-poet does not inject the page object

### Requirement: Page objects use real handle_urls patterns
Every page object class SHALL be decorated with `@handle_urls` using a real,
domain-specific URL pattern. Empty string patterns are NOT permitted as they
cause registry conflicts when multiple domains are registered.

#### Scenario: handle_urls has a domain-specific pattern
- **WHEN** a page object is defined
- **THEN** its `@handle_urls` pattern contains the domain and relevant path prefix

#### Scenario: Empty handle_urls causes registry conflicts
- **WHEN** two page objects use `@handle_urls("")`
- **THEN** a registry conflict warning is raised and only the first rule is used

### Requirement: The url field casts response.url to str
The `url` field of every page object SHALL return `str(self.response.url)`.
Returning `self.response.url` directly is not permitted as it returns a
`ResponseUrl` object, not a plain string.

#### Scenario: url field returns a plain string
- **WHEN** `page.url` is accessed
- **THEN** the result is a `str` instance, not a `ResponseUrl`

### Requirement: Unimplemented field stubs use pass
Field stubs without extraction logic SHALL use `pass` as their body, returning
`None` implicitly. `raise NotImplementedError` SHALL NOT be used as it causes
errors during development runs.

#### Scenario: Spider runs with unimplemented fields
- **WHEN** a page object has fields with `pass` bodies
- **THEN** the spider runs without raising exceptions and returns `None` for those fields

### Requirement: Stub page objects must be created before saving fixtures
Page object files with `pass` field stubs MUST be created and importable by
the Scrapy project before `scrapy savefixture` is run. The command resolves
the page object class by importing it, so a missing or unimportable class will
cause the command to fail.

#### Scenario: savefixture fails without stub page object
- **WHEN** `scrapy savefixture <projectname>.pages.example_com.ExampleProductPage <url>` is run
- **THEN** if `ExampleProductPage` does not exist the command raises an ImportError and no fixture is saved

#### Scenario: Stub page object is sufficient for savefixture
- **WHEN** a page object exists with all fields returning `pass`
- **THEN** `scrapy savefixture` runs successfully and saves the fixture

