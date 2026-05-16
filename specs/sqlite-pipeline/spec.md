# sqlite-pipeline Specification

## Purpose
TBD - created by archiving change scrapy-multi-domain-scraper. Update Purpose after archive.
## Requirements
### Requirement: Pipeline stores only Product items
The `SQLitePipeline` SHALL process only `Product` items. All other item types
SHALL be passed through unchanged.

#### Scenario: ProductList items pass through
- **WHEN** a `ProductList` item reaches the pipeline
- **THEN** it is returned unchanged and not written to the database

### Requirement: Database path is configurable via settings
The pipeline SHALL read the database path from `SQLITE_DB_PATH` in settings,
defaulting to `"output.db"` if not set. It SHALL be instantiated via
`from_crawler`.

#### Scenario: Custom db path is used
- **WHEN** `SQLITE_DB_PATH = "custom.db"` is set
- **THEN** the pipeline writes to `custom.db`

### Requirement: List fields are serialised as JSON
The `images` and `breadcrumbs` fields on `Product`, being lists, SHALL be
serialised to JSON strings before being written to SQLite.

#### Scenario: images stored as JSON string
- **WHEN** a `Product` with a list of image URLs is processed
- **THEN** the `images` column contains a valid JSON array string

### Requirement: Pipeline lifecycle methods do not accept spider argument
The `open_spider`, `close_spider`, and `process_item` methods SHALL NOT
declare a `spider` parameter, in line with the current Scrapy deprecation.

#### Scenario: No spider argument on lifecycle methods
- **WHEN** the pipeline class is inspected
- **THEN** `open_spider`, `close_spider`, and `process_item` have no `spider` parameter

