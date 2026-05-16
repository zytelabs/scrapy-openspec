# project-settings Specification

## Purpose
TBD - created by archiving change scrapy-multi-domain-scraper. Update Purpose after archive.
## Requirements
### Requirement: Always try WebPage first — only use BrowserPage if selectors fail
Page objects SHALL subclass `WebPage` (HTTP fetch) by default. `BrowserPage`
(browser rendering via `browserHtml`) MAY be used only if selectors consistently
return no results against the HTTP response and the content is confirmed to be
JavaScript-rendered.

The decision to switch from `WebPage` to `BrowserPage` MUST NOT be made
pre-emptively. The correct order is:
1. Implement selectors against the HTTP response (`WebPage`)
2. If selectors fail, verify the content is absent in the raw HTML
3. Only then switch the base class to `BrowserPage`

There are exactly two permitted base classes: `WebPage` and `BrowserPage`. No other
fetch strategies, custom HTTP clients, scripts, or workarounds SHALL be introduced
to handle rendering or fetch failures. If neither `WebPage` nor `BrowserPage`
produces working selectors, the problem is with the selectors, not the fetch strategy.

`browserHtml` SHALL NOT be enabled via `settings.py`, `ZYTE_API_DEFAULT_PARAMS`,
or per-request `meta` — it is controlled exclusively by the page object base class.

```python
# Default — always start here
class ScanProductPage(WebPage, Returns[Product]):
    ...

# Only if HTTP response lacks the content
class ScanProductPage(BrowserPage, Returns[Product]):
    ...
```

#### Scenario: New page object starts as WebPage
- **WHEN** a new page object is created
- **THEN** it subclasses `WebPage`, not `BrowserPage`

#### Scenario: BrowserPage is used only after HTTP selectors fail
- **WHEN** selectors return no results
- **THEN** the raw HTTP HTML is inspected first; `BrowserPage` is only adopted if the content is confirmed absent in HTTP

#### Scenario: No third fetch strategy is introduced
- **WHEN** neither WebPage nor BrowserPage selectors work
- **THEN** the selectors are revised — no scripts, custom clients, or alternative fetch methods are created

#### Scenario: browserHtml is not set directly in settings or meta
- **WHEN** `settings.py` and spider `meta` are inspected
- **THEN** `ZYTE_API_BROWSER_HTML`, `ZYTE_API_DEFAULT_PARAMS`, and per-request `meta` do not contain `browserHtml`

### Requirement: Addons configure middleware and fingerprinting
The project SHALL use Scrapy's `ADDONS` setting to configure `scrapy_poet` and
`scrapy_zyte_api` rather than manually setting middlewares or fingerprinters.
`scrapy_poet.Addon` MUST be listed before `scrapy_zyte_api.Addon` so that
zyte-api can detect and wrap the poet fingerprinter.

#### Scenario: Addons registered in correct order
- **WHEN** `settings.py` is loaded
- **THEN** `ADDONS` contains `scrapy_poet.Addon` at priority 300 and `scrapy_zyte_api.Addon` at priority 500

#### Scenario: No manual middleware configuration
- **WHEN** reviewing `settings.py`
- **THEN** `DOWNLOADER_MIDDLEWARES`, `SPIDER_MIDDLEWARES`, and `REQUEST_FINGERPRINTER_CLASS` are NOT set manually

### Requirement: Project source files live inside the project folder
After running `scrapy startproject <name> .`, all source files SHALL be placed
inside the `<projectname>/` directory that Scrapy creates. This includes
`items.py`, `pipelines.py`, `middlewares.py`, `settings.py`, `spiders/`, and
`pages/`. Test fixtures are the exception and SHALL remain under `tests/` at
the project root.

#### Scenario: items.py is inside the project folder
- **WHEN** the project is set up
- **THEN** items are defined in `<projectname>/items.py`, not at the project root

#### Scenario: page objects are inside the project folder
- **WHEN** the project is set up
- **THEN** page objects live in `<projectname>/pages/<domain>.py`

### Requirement: Page object discovery is configured
The project SHALL set `SCRAPY_POET_DISCOVER` to the list of modules containing
page objects so scrapy-poet registers them at startup.

#### Scenario: Discovery points to pages module
- **WHEN** `settings.py` is loaded
- **THEN** `SCRAPY_POET_DISCOVER` equals `["<projectname>.pages"]`

#### Scenario: Missing discovery causes injection failure
- **WHEN** `SCRAPY_POET_DISCOVER` is not set
- **THEN** page objects are not registered and injection does not occur

### Requirement: pytest is configured with pythonpath
The project SHALL include `[tool.pytest.ini_options]` in `pyproject.toml` with
`pythonpath = ["."]` so that the `<projectname>` package is resolvable during test collection.

#### Scenario: Tests collect without ModuleNotFoundError
- **WHEN** `pytest tests/` is run from the project root
- **THEN** all fixture test cases are collected without import errors

### Requirement: Default project name is base
The Scrapy project SHALL be named `base` when created with `scrapy startproject`
unless the user explicitly specifies a different name.

#### Scenario: Project created without a specified name
- **WHEN** a new Scrapy project is being set up and the user has not specified a name
- **THEN** the project is created as `scrapy startproject base .`

#### Scenario: User specifies a project name
- **WHEN** the user provides a project name
- **THEN** that name is used instead of `base`

### Requirement: Project creation follows a canonical ordered flow
A Scrapy project using this stack MUST be created in the following order.
No step SHALL be attempted before all preceding steps are complete:

1. `scrapy startproject <name> .` — create the Scrapy project
2. Update `<projectname>/settings.py` — configure addons, discovery, pipeline
3. Create `<projectname>/items.py` — define `Product` and `ProductList` dataclasses
4. `scrapy genspider` — generate the spider scaffold in `<projectname>/spiders/`, then rename class and file
5. Create page objects with `pass` stubs in `<projectname>/pages/` — one file per domain, classes importable
6. `scrapy savefixture` — save fixture for each page object, then run `clean_fixture.py`
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

### Requirement: pyproject.toml sections are appended, never inserted mid-block
When editing `pyproject.toml`, new TOML sections SHALL be appended at the end of the
file. Inserting a new section inside an existing block (e.g. adding
`[tool.pytest.ini_options]` in the middle of `[project]`) creates a duplicate section
header and breaks the file.

#### Scenario: Adding pytest config mid-file corrupts the project section
- **WHEN** `[tool.pytest.ini_options]` is inserted inside the `[project]` block
- **THEN** the TOML file becomes invalid and tools such as `uv` fail to parse it

#### Scenario: Appending at end is always safe
- **WHEN** a new TOML section is appended after the last existing line
- **THEN** the file remains valid and all sections are parsed correctly

