## Context

`scrapy savefixture` is not a standalone HTTP client — it boots the full Scrapy
crawler, applies settings and addons, and injects the page object class to
capture the response. This means it has hard runtime dependencies on the
project being in a working state before it can be invoked.

## Goals / Non-Goals

**Goals**
- Make the ordering constraint explicit in specs and tasks
- Prevent wasted effort from attempting to save fixtures before the project exists

**Non-Goals**
- Changing the fixture workflow itself

## Decisions

### Capture ordering as a spec requirement, not just a task note
The dependency is a hard constraint, not a style preference. It belongs in the
spec so it is enforced when generating tasks for any new project using this spec.

## Risks / Trade-offs

- None — this is a clarification, not a behaviour change.

## Open Questions

- None.
