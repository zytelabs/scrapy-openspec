## Why

Populating `output.json` and implementing selectors are the most token-intensive
and repetitive steps in the fixture workflow. They are also independent per page
object — there is no reason to do them sequentially when multiple page objects
exist. Delegating these steps to subagents reduces the work on the main agent
and allows parallel execution across domains.

## What Changes

- Steps 7 (populate `output.json`) and 8 (implement selectors) in the creation
  flow SHALL be handled by subagents
- Each subagent handles one page object: reads the cleaned fixtures, populates
  `output.json`, implements selectors, and runs the test to verify
- Where multiple page objects exist, subagents SHALL run in parallel

## Capabilities

### New Capabilities

### Modified Capabilities

- `fixture-testing`: Subagents handle output.json population and selector implementation
- `project-settings`: Creation flow updated to reflect subagent steps

## Impact

- `openspec/specs/fixture-testing/spec.md`
- `openspec/specs/project-settings/spec.md`
