## Context

The creation flow has hard dependencies between steps — most critically,
the Scrapy project and stub page objects must exist before `savefixture` can
run. Codifying the flow as a spec requirement ensures it is always surfaced
in generated task lists for new projects.

## Goals / Non-Goals

**Goals**
- Single canonical ordered flow that any new project follows
- Default name `base` for consistency across projects

**Non-Goals**
- Enforcing the flow programmatically — this is a process spec, not a runtime check

## Decisions

### Name default is base not the domain or project intent
A generic name keeps the scaffold reusable. Domain-specific naming belongs
at the spider and page object level, not the project level.

## Risks / Trade-offs

- None — this is an additive clarification.

## Open Questions

- None.
