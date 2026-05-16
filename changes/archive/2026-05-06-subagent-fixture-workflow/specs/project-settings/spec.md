## MODIFIED Requirements

### Requirement: Project creation follows a canonical ordered flow
A Scrapy project using this stack MUST be created in the following order.
No step SHALL be attempted before all preceding steps are complete:

1. `scrapy startproject <name> .` — create the Scrapy project
2. Update `settings.py` — configure addons, discovery, pipeline
3. Create `items.py` — define `Product` and `ProductList` dataclasses
4. `scrapy genspider` — generate the spider scaffold, then rename class and file
5. Create page objects with `pass` stubs — one file per domain, classes importable
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
