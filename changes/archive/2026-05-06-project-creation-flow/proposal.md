## Why

The correct order for creating a Scrapy project using this stack is not
currently captured as a spec. Without it, steps get done out of order —
most critically, fixtures are attempted before the project exists. Additionally,
the default project name is not defined, leading to inconsistent naming across projects.

## What Changes

- The default Scrapy project name SHALL be `base` unless the user specifies otherwise
- A canonical creation flow is codified covering all steps from `scrapy startproject`
  through to updating the spider with real selectors

## Capabilities

### New Capabilities

### Modified Capabilities

- `project-settings`: Add default project name requirement and canonical creation flow

## Impact

- `openspec/specs/project-settings/spec.md`
