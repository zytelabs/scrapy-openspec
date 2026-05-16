## ADDED Requirements

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

### Requirement: Page object discovery is configured
The project SHALL set `SCRAPY_POET_DISCOVER` to the list of modules containing
page objects so scrapy-poet registers them at startup.

#### Scenario: Discovery points to pages module
- **WHEN** `settings.py` is loaded
- **THEN** `SCRAPY_POET_DISCOVER` equals `["specs.pages"]`

#### Scenario: Missing discovery causes injection failure
- **WHEN** `SCRAPY_POET_DISCOVER` is not set
- **THEN** page objects are not registered and injection does not occur

### Requirement: pytest is configured with pythonpath
The project SHALL include `[tool.pytest.ini_options]` in `pyproject.toml` with
`pythonpath = ["."]` so that the `specs` package is resolvable during test collection.

#### Scenario: Tests collect without ModuleNotFoundError
- **WHEN** `pytest tests/` is run from the project root
- **THEN** all fixture test cases are collected without import errors
