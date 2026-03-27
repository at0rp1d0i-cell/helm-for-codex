# Architecture

## Layers

- Source layer
- Plugin distribution layer
- Runtime pack layer
- Lead layer
- Ops layer
- Worker layer

## Modules

- canonical docs
- onboarding state
- runtime installer
- plugin manifest and marketplace
- plugin bootstrap skill and script
- exported plugin runtime pack
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
- plugin distribution must bootstrap the same runtime surface as the direct installer instead of inventing a second execution path
- installed onboarding currently requires an explicit `init --force` because the installer bootstraps onboarding state immediately
- source `skills/` and repo-local `.agents/skills/` must stay synchronized
- `Lead` remains the only user-facing entrypoint, while `Ops` owns logical dispatch and stage advancement behind that facade
- canonical repo role names are resolved through `.codex/role_bridge.toml` and `scripts/role_bridge.py` before the last-hop agent invocation
- execution dispatch packets and live review packets both preserve the logical role name plus bridge metadata
- execution dispatch packets and live review packets now also preserve runtime role binding details from `.codex/roles/*.toml`
- a paired invocation spec captures the final bridge contract for each live packet so Ops can own dispatch while Lead only supervises the last-hop runtime handoff
- `scripts/bridge_runner.py` is the shared compiler for the last-hop launch payload; `lead_loop.py` and `ops_loop.py` may invoke it, but only `Ops` owns the decision to consume a packet/spec pair and move specialist execution forward
- execution receipts are the canonical evidence for what happened after a bridge launch; they preserve execution status, writeback status, and specialist notes without pretending the launch itself was fully repo-native
- direct role-owned canonical review-pass writeback is the preferred live review path and works after runtime install
- Ops, Product, Architect, Reviewer, Implementation Worker, QA Runner, and Docs Sync live roles are defined in repo-scoped Codex config
- review-result remains supported as a compatibility and recovery path
- deterministic fallback remains available when live subagent review is unavailable
