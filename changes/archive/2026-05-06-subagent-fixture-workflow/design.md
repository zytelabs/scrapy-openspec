## Context

The fixture workflow involves two distinct token-heavy tasks per page object:
reading plain text to determine expected values, and reading clean HTML to write
CSS/XPath selectors. These tasks are self-contained per page object and have no
interdependencies, making them ideal for parallel subagent delegation.

## Goals / Non-Goals

**Goals**
- Delegate output.json population and selector implementation to subagents
- Run subagents in parallel when multiple page objects exist
- Each subagent is fully responsible for one page object from fixture to passing test

**Non-Goals**
- Subagent handling of project setup, savefixture, or spider updates
- Automated retry or error recovery within subagents

## Decisions

### Steps 7 and 8 combined into one subagent task per page object
**Rationale:** Both steps operate on the same fixture files for the same page
object. Combining them into one subagent avoids handoff overhead and keeps
context localised — the subagent that reads the plain text also writes the
selectors, ensuring consistency between expected values and extraction logic.

### Parallelism at the page object level
**Rationale:** Page objects are fully independent — `ScanProductPage` selectors
have no dependency on `ScanProductListPage`. Running them in parallel is safe
and reduces total wall-clock time linearly with the number of page objects.

### Main agent retains steps 1–6 and 8
**Rationale:** Project setup, savefixture, and spider updates are sequential,
stateful operations that depend on each other. They remain with the main agent.
Subagents only handle the isolated, parallelisable fixture work.

## Risks / Trade-offs

- **Subagent selector errors** → Each subagent runs pytest and must confirm
  tests pass before finishing. Failures surface immediately.
- **Context size** → Clean HTML can still be large (50–600KB after cleaning).
  The `clean_fixture.py` script mitigates this before the subagent reads it.

## Open Questions

- Should subagents also run `clean_fixture.py`, or should the main agent run it
  before spawning subagents? (Current spec: main agent runs clean_fixture as part
  of step 6, subagents receive already-cleaned files.)
