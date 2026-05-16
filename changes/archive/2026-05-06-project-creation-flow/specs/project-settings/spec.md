## ADDED Requirements

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
2. Update `settings.py` — configure addons, discovery, pipeline
3. Create `items.py` — define `Product` and `ProductList` dataclasses
4. `scrapy genspider` — generate the spider scaffold, then rename class and file
5. Create page objects with `pass` stubs — one file per domain, classes importable
6. `scrapy savefixture` — save fixture for each page object
7. Update `output.json` — populate expected values from cleaned fixture
8. Implement selectors — update page object fields with real CSS/XPath
9. Update spider — add `urls`, `allowed_domains`, and wire callbacks

#### Scenario: savefixture fails if page objects do not exist
- **WHEN** step 6 is attempted before step 5
- **THEN** the command fails with an ImportError

#### Scenario: selectors cannot be written without a fixture
- **WHEN** step 8 is attempted before step 6
- **THEN** there is no fixture HTML to develop selectors against

#### Scenario: full flow produces passing tests
- **WHEN** all 9 steps are completed in order
- **THEN** `pytest tests/` passes for all page object fixtures
