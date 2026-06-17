# custom-items Specification

## Purpose
TBD - created by archiving change scrapy-multi-domain-scraper. Update Purpose after archive.
## Requirements
### Requirement: Items are plain attrs dataclasses
Custom items SHALL be defined using `@attrs.define` with no dependency on
`zyte_common_items`. Before creating items, the developer MUST confirm whether
to extend `zyte_common_items` or create fully custom classes, as this affects
item structure, page object inheritance, and pipeline design.

#### Scenario: Product item is a plain attrs class
- **WHEN** `<projectname>/items.py` is inspected
- **THEN** `Product` is decorated with `@attrs.define` and does not inherit from any `zyte_common_items` class

#### Scenario: Developer is asked before item base class is chosen
- **WHEN** a new project is being set up
- **THEN** the developer is asked whether to extend `zyte_common_items` or create custom items before any item code is written

### Requirement: Product item defines standard e-commerce fields
The `Product` item SHALL define fields covering the standard data points
extractable from a product detail page. The `url` field is required; all
others are `Optional`.

The standard set of fields is:

| Field | Type | Notes |
|---|---|---|
| `url` | `str` | Required — the canonical product URL |
| `name` | `Optional[str]` | Product title |
| `price` | `Optional[str]` | Current selling price as a decimal string |
| `regular_price` | `Optional[str]` | Pre-discount price as a decimal string |
| `currency` | `Optional[str]` | Normalised currency code (e.g. `"GBP"`) |
| `currency_raw` | `Optional[str]` | Raw currency symbol as it appears on the page (e.g. `"£"`) |
| `sku` | `Optional[str]` | Manufacturer or retailer SKU / MPN |
| `brand` | `Optional[str]` | Brand or manufacturer name |
| `description` | `Optional[str]` | Plain-text product description |
| `availability` | `Optional[str]` | Stock status (e.g. `"InStock"`, `"OutOfStock"`) |
| `breadcrumbs` | `Optional[List[str]]` | Category path from the page breadcrumb trail |
| `images` | `Optional[List[str]]` | Product image URLs |

`currency` and `currency_raw` are complementary: `currency` is the normalised ISO
code derived from the raw symbol; `currency_raw` preserves the symbol exactly as
scraped so downstream consumers can audit the source.

#### Scenario: Product has required and optional fields
- **WHEN** `Product(url="https://example.com")` is instantiated
- **THEN** the instance is created successfully with all optional fields defaulting to `None`

#### Scenario: currency and currency_raw are both present
- **WHEN** a price such as `"£12.99"` is scraped
- **THEN** `currency_raw` is `"£"` and `currency` is `"GBP"`

### Requirement: ProductList item is a crawl-control item
The `ProductList` item SHALL represent a listing page used to harvest URLs
for crawling. It SHALL contain only `url`, `product_urls`, and `next_page_url`.
It SHALL NOT store product data from listing pages.

#### Scenario: ProductList only contains crawl fields
- **WHEN** `<projectname>/items.py` is inspected
- **THEN** `ProductList` contains exactly `url`, `product_urls`, and `next_page_url` and no other fields

