# Architecture

## Layers

- Source layer
- Runtime pack layer
- Lead layer
- Ops layer
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
- role invocation bridge
- source skills mirror
- ops orchestrator role
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
- `Lead` remains the only user-facing entrypoint, while `Ops` owns logical dispatch and stage advancement behind that facade
- canonical repo role names are resolved through `.codex/role_bridge.toml` and `scripts/role_bridge.py` before the last-hop agent invocation
- execution dispatch packets and live review packets both preserve the logical role name plus bridge metadata
- execution dispatch packets and live review packets now also preserve runtime role binding details from `.codex/roles/*.toml`
- a paired invocation spec captures the final bridge contract for each live packet so Ops can own dispatch while Lead only supervises the last-hop runtime handoff
- direct role-owned canonical review-pass writeback is the preferred live review path and works after runtime install
- Ops, Product, Architect, Reviewer, Implementation Worker, QA Runner, and Docs Sync live roles are defined in repo-scoped Codex config
- review-result remains supported as a compatibility and recovery path
- deterministic fallback remains available when live subagent review is unavailable
