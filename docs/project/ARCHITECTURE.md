# Architecture

## Layers

- Source layer
- Runtime pack layer
- Lead layer
- Worker layer

## Modules

- canonical docs
- onboarding state
- runtime installer
- installed runtime scripts
- installed ops templates and checks
- skills
- repo-local `.agents/skills`
- codex role config
- source skills mirror
- review packets
- review results
- review passes
- repo checks

## Constraints

- single visible lead
- small active concurrency
- repo as memory
- runtime installer must preserve target canonical state during re-install
- onboarding state is canonical and visible across sessions
- source `skills/` and repo-local `.agents/skills/` must stay synchronized
- direct role-owned canonical review-pass writeback is the preferred live review path
- Product, Architect, and Reviewer live review roles are defined in repo-scoped Codex config
- review-result remains supported as a compatibility and recovery path
- deterministic fallback remains available when live subagent review is unavailable
