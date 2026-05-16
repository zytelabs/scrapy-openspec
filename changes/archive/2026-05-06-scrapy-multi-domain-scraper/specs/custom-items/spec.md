## ADDED Requirements

### Requirement: Items are plain attrs dataclasses
Custom items SHALL be defined using `@attrs.define` with no dependency on
`zyte_common_items`. Before creating items, the developer MUST confirm whether
to extend `zyte_common_items` or create fully custom classes, as this affects
item structure, page object inheritance, and pipeline design.

#### Scenario: Product item is a plain attrs class
- **WHEN** `specs/items.py` is inspected
- **THEN** `Product` is decorated with `@attrs.define` and does not inherit from any `zyte_common_items` class

#### Scenario: Developer is asked before item base class is chosen
- **WHEN** a new project is being set up
- **THEN** the developer is asked whether to extend `zyte_common_items` or create custom items before any item code is written

### Requirement: Product item defines standard e-commerce fields
The `Product` item SHALL define fields covering the standard data points
extractable from a product detail page. The `url` field is required; all
others are `Optional`.

#### Scenario: Product has required and optional fields
- **WHEN** `Product(url="https://example.com")` is instantiated
- **THEN** the instance is created successfully with all optional fields defaulting to `None`

### Requirement: ProductList item is a crawl-control item
The `ProductList` item SHALL represent a listing page used to harvest URLs
for crawling. It SHALL contain only `url`, `product_urls`, and `next_page_url`.
It SHALL NOT store product data from listing pages.

#### Scenario: ProductList only contains crawl fields
- **WHEN** `specs/items.py` is inspected
- **THEN** `ProductList` contains exactly `url`, `product_urls`, and `next_page_url` and no other fields
