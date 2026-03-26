# Project Brief

## Problem

Build a Codex-native AI team with a single lead interface and strong internal execution discipline.

## Current Goal

Phase 15 baseline complete: the repository now keeps repo role names canonical through a role invocation bridge, so `Lead` and `Ops` dispatch `ops-orchestrator`, `implementation-worker`, `qa-runner`, and the review roles first, then resolve them to the currently available generic agent API only at the last hop.

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
- repo validation passes
