## Why

The `scrapy savefixture` command is a Scrapy CLI command that runs the crawler
to download a real HTTP response. This means the Scrapy project, its settings,
and a stub page object class must all exist before any fixture can be saved.
The current specs do not capture this hard dependency, which would cause a new
project to fail if fixtures were attempted before project setup.

## What Changes

- `fixture-testing` spec gains a requirement that the Scrapy project and stub
  page object MUST exist before `savefixture` is run
- `tasks` ordering is clarified to reflect: project setup → stub page objects → savefixture

## Capabilities

### New Capabilities

### Modified Capabilities

- `fixture-testing`: The Scrapy project and stub page object MUST exist before `savefixture` is run
- `page-objects`: Stub page objects MUST be created and importable before fixtures are saved

## Impact

- `openspec/specs/fixture-testing/spec.md`
- `openspec/specs/page-objects/spec.md`
