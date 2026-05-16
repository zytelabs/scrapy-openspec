# spider Specification

## Purpose
TBD - created by archiving change scrapy-multi-domain-scraper. Update Purpose after archive.
## Requirements
### Requirement: Spider imports items not page objects
Spider callbacks SHALL be type-hinted with item classes only. Page objects
SHALL NOT be imported into the spider. scrapy-poet resolves the correct page
object via the `handle_urls` registry and calls `to_item()` automatically.

#### Scenario: Spider has no page object imports
- **WHEN** the spider file is inspected
- **THEN** no page object classes are imported and all callback parameters are typed with item classes

### Requirement: All spider callbacks are async
All spider callbacks SHALL be defined with `async def`. Synchronous callbacks
are not permitted.

#### Scenario: parse and parse_product are async
- **WHEN** the spider class is inspected
- **THEN** `start`, `parse`, and `parse_product` are all `async def`

### Requirement: start() replaces start_urls
The spider SHALL define `async def start()` as an async generator yielding
initial requests. The `start_urls` class attribute SHALL NOT be used.

#### Scenario: start() yields one request per url
- **WHEN** `start()` is called
- **THEN** it yields one `scrapy.Request` for each URL in `self.urls`

### Requirement: Spider uses a urls list for start URLs
The spider SHALL define a `urls` class attribute as a list of starting URLs.
Adding a new domain or category requires only appending to this list, not
changing callback logic.

#### Scenario: New URL added without logic change
- **WHEN** a new URL is appended to `self.urls`
- **THEN** the spider crawls it without any changes to `start()`, `parse()`, or `parse_product()`

### Requirement: Callbacks use response.follow for subsequent requests
Inside callbacks where `response` is available, `response.follow()` SHALL be
used instead of `scrapy.Request()`. `scrapy.Request()` is only used in `start()`
where no response exists.

#### Scenario: parse uses response.follow
- **WHEN** `parse` yields follow-up requests
- **THEN** it calls `response.follow()` not `scrapy.Request()`

### Requirement: Unused response parameter is named _
When a callback does not use the `response` argument, it SHALL be named `_`
to signal it is intentionally unused.

#### Scenario: parse_product names unused response as _
- **WHEN** `parse_product` is defined
- **THEN** its second parameter is `_` not `response`

### Requirement: DummyResponse is not used — _ convention is preferred
`DummyResponse` (from scrapy-poet) prevents Scrapy from downloading the HTTP response
when only the page object is needed. This project SHALL NOT use `DummyResponse`.
The `_` parameter name is the preferred way to signal an intentionally unused response.

#### Scenario: Spider does not import DummyResponse
- **WHEN** the spider file is inspected
- **THEN** `DummyResponse` is not imported and not used in any callback signature

### Requirement: Spider covers all domains in allowed_domains
When a new domain is added, its hostname MUST be added to `allowed_domains`
and the spider class and file MUST be renamed to reflect its broader scope.

#### Scenario: New domain is added correctly
- **WHEN** a new domain is added
- **THEN** `allowed_domains`, `urls`, the spider class name, and the spider filename are all updated

