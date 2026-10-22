## 1. Update Specs

- [x] 1.1 Route Shopify detection through `scrapy savefixture`; read Ecwid config from the raw fixture HTML
- [x] 1.2 Align `fixture-testing` subagent requirement with creation-flow step 7
- [x] 1.3 Use `base` as the project name in the savefixture example
- [x] 1.4 Add `ZYTE_API_KEY` requirement to `project-settings`

## 2. Cleaning Helper

- [x] 2.1 Add `scripts/clean_fixture.py` using clear-html
- [x] 2.2 Handle `BrowserResponse` fixtures, skip JSON and XML (sitemap) bodies, strip XML declarations from XHTML
- [x] 2.3 Require copying the helper in the creation flow and `fixture-testing`
- [x] 2.4 Restrict clean HTML to reading; selectors target the raw response body
