# Project Brief

## Problem

Build a Codex-native AI team with a single lead interface and strong internal execution discipline.

## Current Goal

Phase 22 in progress: continue closing the productization gap with gstack after landing research-first `office-hours`, sprint negotiation, `autoplan`, browser-QA evidence, and release gate/prep loops on top of Helm4Codex's repo-backed orchestration model.

## Success Criteria

- single-entry lead model exists
- canonical project-state files exist
- internal role skills exist
- runtime-pack installer exists and can install the Codex-facing runtime into another repo
- the installed runtime pack behaves as documented: fresh install works, reinstall preserves AGENTS/PROJECT_BRIEF/ONBOARDING_STATE, and installed docs checks pass
- `.agents/skills` packaging exists for the installed runtime while leaving user `skills/` source files untouched
- onboarding state exists and deep-scan planning is part of first-contact project adoption, but the lead currently needs an explicit `init`/`force` action because onboarding state is bootstrapped immediately
- direct role-owned canonical review-pass writeback exists for Product, Architect, and Reviewer
- repo-scoped Codex role config exists for the live orchestration, review, and execution roles
- review-result compatibility remains available
- `Ops` now has a live repo-scoped role surface in addition to the repo-owned `scripts/ops_loop.py` runtime
- role invocation bridge exists and is wired into execution dispatch packets
- role invocation bridge now also resolves the live review lane packets for Product, Architect, and Reviewer
- execution dispatch packets and live review packets now include runtime role binding details from the repo role config
- execution dispatch packets and live review packets now get paired invocation specs for the final bridge hop
- a reusable `scripts/bridge_runner.py` can validate packet/spec pairs and render a last-hop launch payload
- `lead_loop.py bridge-launch` and `ops_loop.py bridge-launch` expose that bridge runner without pulling dispatch ownership back into the Lead
- `team_state.py execution-receipt`, `bridge_runner.py receipt`, and `ops_loop.py bridge-receipt` now persist launch outcomes as repo-backed execution receipts
- a local Codex plugin package exists for discovery and bootstrap
- the plugin bundles a self-contained runtime-pack payload instead of depending on the source repo at install time
- a plugin bootstrap path can install the same runtime surface as the direct installer
- an explicit upgrade command exists for already-installed repositories
- upgrades refresh runtime-managed files while preserving canonical project state
- installed target repos have a runtime-scoped self-check instead of depending on source-only repo validation
- a repo-backed gstack gap assessment exists and identifies the highest-value workflow gaps to close next
- a first-class `office-hours` lane exists to apply Product, Design, and Architect pressure before plan
- `office-hours` now injects repo-backed Researcher pressure before Product, Design, and Architect challenge passes run
- a live `researcher` role surface exists in the repo role bridge and installed runtime
- a repo-backed sprint negotiation lane exists so Builder and QA pressure shape the sprint contract before build
- a first-class `autoplan` lane exists on top of existing review passes and taste-decision gates
- a live `design-reviewer` role surface exists in the repo role bridge and installed runtime
- browser-QA evidence artifacts exist as a repo-backed trust surface, even before the full browser runtime is wired
- a release gate and release prep report exist as repo-backed ship-readiness artifacts
- repo validation passes
