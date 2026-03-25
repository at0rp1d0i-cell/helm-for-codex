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
- runtime installer must preserve target canonical state during re-install; deep scan confirmed AGENTS/PROJECT_BRIEF/ONBOARDING_STATE survive reinstall and installed docs checks pass
- installed onboarding currently requires an explicit `init --force` because the installer bootstraps onboarding state immediately
- source `skills/` and repo-local `.agents/skills/` must stay synchronized
- direct role-owned canonical review-pass writeback is the preferred live review path and works after runtime install
- Product, Architect, and Reviewer live review roles are defined in repo-scoped Codex config
- review-result remains supported as a compatibility and recovery path
- deterministic fallback remains available when live subagent review is unavailable
