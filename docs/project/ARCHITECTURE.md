# Architecture

## Layers

- Lead layer
- Ops layer
- Worker layer

## Modules

- canonical docs
- skills
- codex role config
- ops templates
- review packets
- review results
- review passes
- repo checks

## Constraints

- single visible lead
- small active concurrency
- repo as memory
- direct role-owned review-result writeback is the preferred live review path
- Product, Architect, and Reviewer live review roles are defined in repo-scoped Codex config
- deterministic fallback remains available when live subagent review is unavailable
