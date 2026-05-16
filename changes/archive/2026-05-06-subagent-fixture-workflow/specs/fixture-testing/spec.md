## ADDED Requirements

### Requirement: Subagents populate output.json and implement selectors
Steps 7 (populate `output.json`) and 8 (implement selectors) SHALL be delegated
to subagents rather than performed by the main agent. Each subagent is responsible
for a single page object and SHALL:

1. Read `HttpResponse-body.txt` to extract expected field values and write `output.json`
2. Read `HttpResponse-body-clean.html` to develop CSS/XPath selectors for each field
3. Update the page object with the implemented selectors
4. Run `pytest` for that fixture and confirm all tests pass

#### Scenario: Subagent handles one page object end to end
- **WHEN** a subagent is spawned for a page object
- **THEN** it reads the plain text and clean HTML fixtures, writes output.json, implements selectors, and confirms tests pass

### Requirement: Subagents run in parallel when multiple page objects exist
Subagents SHALL run in parallel — one per page object — when a domain has more
than one page object or when multiple domains are being set up simultaneously.

#### Scenario: Two page objects processed in parallel
- **WHEN** both `ScanProductPage` and `ScanProductListPage` need fixtures populated
- **THEN** two subagents are spawned concurrently, one per page object

#### Scenario: Single page object uses a single subagent
- **WHEN** only one page object needs its fixture populated
- **THEN** a single subagent is used without parallelism
