## ADDED Requirements

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
