# scrapy-openspec

Behavioural specifications for a Scrapy project using scrapy-poet and scrapy-zyte-api.

Each spec covers one area of the project and defines requirements as scenarios in a
Given/When/Then style. Specs are derived from real corrections made during development.

## Usage

Clone into the root of any Scrapy project as the `openspec/` directory:

```bash
git clone https://github.com/zytelabs/scrapy-openspec.git openspec
```

## Structure

```
openspec/
  specs/              # One subdirectory per feature, each with a spec.md
    spider/
    page-objects/
    custom-items/
    fixture-testing/
    project-settings/
    scrapy-playwright/
    sqlite-pipeline/
  changes/            # Change log and archive
```

## Specs

| Spec | What it covers |
|------|----------------|
| `spider` | Async callbacks, `urls` list, `response.follow`, unused `_` param, `DummyResponse` policy |
| `page-objects` | Domain-per-file layout, class naming, `handle_urls` patterns, `url` field casting, stub convention |
| `custom-items` | Plain `attrs` items, field definitions for `Product` and `ProductList` |
| `fixture-testing` | `scrapy savefixture` workflow, `output.json` accuracy, subagent parallelism |
| `project-settings` | `ADDONS` order, `SCRAPY_POET_DISCOVER`, pytest config, project creation flow |
| `scrapy-playwright` | Browser rendering without Zyte API: stock handler, per-request middleware, patchright/camoufox providers, camoufox `no_viewport`/`domcontentloaded` gotchas |
| `sqlite-pipeline` | Item filtering, configurable DB path, JSON serialisation of list fields |
