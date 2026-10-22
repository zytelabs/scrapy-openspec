# sqlite-pipeline Specification

## Purpose
Optional SQLite storage for scraped `Product` items. Projects do not include
this pipeline by default; the requirements below apply only once the user has
asked for SQLite output.
## Requirements
### Requirement: SQLite pipeline is opt-in
The `SQLitePipeline` SHALL NOT be created or registered in `ITEM_PIPELINES`
unless the user explicitly asks for SQLite storage. Without it, items are
written with Scrapy feed exports (e.g. `scrapy crawl <spider> -O items.jsonl`)
and `SQLITE_DB_PATH` is not set.

#### Scenario: New project without a storage request
- **WHEN** a project is created and the user has not asked for SQLite output
- **THEN** `pipelines.py` contains no `SQLitePipeline`, `ITEM_PIPELINES` does not reference it, and `SQLITE_DB_PATH` is not set

#### Scenario: User asks for SQLite output
- **WHEN** the user asks for items to be stored in SQLite
- **THEN** `SQLitePipeline` is implemented and registered following the requirements in this spec

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

### Requirement: Schema covers all standard Product fields
The `products` table SHALL include a column for every field on the `Product`
item. The `url` column SHALL be declared `TEXT UNIQUE` (not `PRIMARY KEY`) so
an auto-increment integer primary key can be used alongside it. Text fields are
stored as `TEXT`; list fields (`images`, `breadcrumbs`) are stored as JSON
strings.

#### Scenario: Table includes currency_raw column
- **WHEN** the `products` table is inspected
- **THEN** a `currency_raw TEXT` column is present alongside `currency TEXT`

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

