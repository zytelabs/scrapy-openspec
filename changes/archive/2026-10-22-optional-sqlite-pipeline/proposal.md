## Why

The canonical creation flow configured a SQLite pipeline in every new project,
but not every project needs SQLite storage. Scrapy feed exports cover the
default case, so the pipeline should only be added when asked for.

## What Changes

- The SQLite pipeline is opt-in: it is only created when the user asks for SQLite storage
- Step 2 of the canonical creation flow no longer configures a pipeline by default

## Capabilities

### New Capabilities

### Modified Capabilities

- `sqlite-pipeline`: Add opt-in requirement and a real Purpose
- `project-settings`: Creation flow step 2 configures the pipeline only on request

## Impact

- `openspec/specs/sqlite-pipeline/spec.md`
- `openspec/specs/project-settings/spec.md`
- `README.md`
