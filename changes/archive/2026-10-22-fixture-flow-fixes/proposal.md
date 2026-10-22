## Why

Several requirements could not be followed as written. Shopify detection asked
for a direct request that `fixture-testing` forbids. `fixture-testing` numbered
the subagent steps differently from the creation flow and used a `specs.`
project name in its example. `clean_fixture.py` was required but not shipped,
so every project wrote its own, and its fixed `HttpResponse-*` filenames did not
match what `savefixture` writes for `BrowserPage`. Selectors were also developed
against the clear-html output, which drops `class`/`id` attributes and renames
tags, so they did not match the raw response the page object is tested on. Nothing said where the Zyte
API key comes from or what to do when it is missing.

## What Changes

- Shopify detection is a `scrapy savefixture` of the stub listing page object; Ecwid detection reads the raw fixture HTML
- `fixture-testing` refers to creation-flow step 7 and uses the `base` project name
- `scripts/clean_fixture.py` ships with the spec, is copied into new projects, and handles `BrowserResponse` fixtures, JSON bodies and XML sitemaps
- Selectors are developed against the raw `<Response>-body.html`; the clean HTML is for reading only
- New requirement: the Zyte API key comes from `ZYTE_API_KEY`, and a missing key means asking the developer, not working around it

## Capabilities

### New Capabilities

### Modified Capabilities

- `project-settings`: platform detection through savefixture, Zyte API key requirement, creation flow copies and runs the cleaning helper
- `fixture-testing`: cleaning helper shipped and copied, BrowserPage filenames, selectors target raw HTML, step numbering, example project name

## Impact

- `openspec/specs/project-settings/spec.md`
- `openspec/specs/fixture-testing/spec.md`
- `openspec/scripts/clean_fixture.py` (new)
- `README.md`
