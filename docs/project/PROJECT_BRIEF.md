# Project Brief

## Problem

Build a Codex-native AI team with a single lead interface and strong internal execution discipline.

## Current Goal

Phase 18 baseline complete: the repository now compiles packet plus invocation-spec pairs through a reusable bridge runner, so Ops can hand the last-hop specialist launch to a shared runtime instead of reconstructing generic-agent payloads lane by lane.

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
- repo validation passes
