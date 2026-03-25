# Onboarding, Packaging, and Hardening Design

## Goal

Turn the current Codex-native AI team repo from an internal orchestration source repo into a reusable runtime pack that can be installed into real projects, automatically onboard unfamiliar repositories, and maintain a cleaner long-term operating model.

## Problem

Phase 11 established the core review and role-orchestration path, but three gaps remain:

1. The repo still behaves mainly like a source repo for its own evolution, not a clean runtime pack for other projects.
2. A newly opened project does not yet have a formal `init` or onboarding state machine that scans the codebase, aligns with the user, and adopts the project into canonical state.
3. `docs/plans/` and structural checks are still too lightweight for long-running project operations.

## Options Considered

### Option 1: Keep Evolving The Current Repo And Install It Manually

Treat this repo as both source and runtime. Users copy selected files by hand into target projects and rely on the existing lead/review flow.

Pros:
- low short-term work
- no installer or export layer

Cons:
- poor usability for real projects
- no clean onboarding entrypoint
- easy drift between source repo and installed runtime
- weak first-use experience

### Option 2: Add A Runtime Pack Plus Onboarding State Machine

Keep this repo as the design and test source, but add an explicit install/export path for runtime files and a first-contact onboarding workflow driven by the lead.

Pros:
- fastest route to real-world usage
- preserves the current repo as the canonical development source
- makes project adoption a first-class workflow instead of an ad hoc conversation
- aligns with Codex repo-local configuration patterns

Cons:
- adds packaging logic
- requires stronger separation between source artifacts and runtime artifacts

### Option 3: Convert The Entire Repo Into A Template Project

Turn this repo directly into the installable runtime, with less distinction between source and installed output.

Pros:
- conceptually simple

Cons:
- bloats target projects with design-phase material
- makes ongoing evolution and testing noisier
- weak fit for multi-project adoption

## Recommendation

Take Option 2.

This preserves the current repo as the design and verification source while adding the minimum packaging and onboarding layer needed for real use in Codex projects.

## Runtime Pack Model

This repo should remain the source of truth for:

- orchestration logic
- tests
- design and phase plans
- runtime templates and scripts

The installed runtime pack should contain only what a target project needs:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/roles/*.toml`
- `.agents/skills/`
- runtime scripts
- runtime templates
- canonical docs directories

The runtime pack should not include the full historical phase-design archive from this source repo.

## Install Strategy

The first install strategy should be a repo installer/exporter, not a full packaging system.

Recommended shape:

- source command in this repo exports runtime files into a target repo
- installed runtime skills live in `.agents/skills/`
- installed project config lives in `.codex/`
- canonical docs and status files are bootstrapped into the target project

This installer should support:

- first install into a new project
- re-install / upgrade without destroying project-specific canonical state
- dry-run or preview mode for verification

## Repo Skill Packaging

For Codex, repo-local skills should live in `.agents/skills/`.

That means phase 12 should formalize a runtime skill layout where:

- `team-lead` remains the single user-facing entrypoint
- internal skills are installed as repo-local skills under `.agents/skills/`
- role metadata and `.codex/roles/*.toml` remain aligned with those installed skill paths

The source repo may continue to maintain its own development layout, but the runtime exporter must install the Codex-facing layout cleanly.

## Onboarding / Init Model

Onboarding should be both automatic on first contact and manually re-runnable.

### Triggers

- automatic when the lead detects a repo without onboarding state
- manual when the user says `init`, `re-init`, `adopt this repo`, or equivalent

### State Machine

`detect -> shallow-scan -> deep-scan-plan -> waiting-user-alignment -> deep-scan -> adopt`

### State File

Add:

- `docs/status/ONBOARDING_STATE.md`

This file should track:

- current onboarding phase
- last completed scan tranche
- active hypotheses
- pending user decisions
- adoption readiness

## Shallow Scan

The first scan should be fast, repo-safe, and mostly read-only.

Default internal scan seats:

- `Codebase Mapper`
- `Quality Auditor`
- `Docs Auditor`
- `Risk / Refactor Scout`

Outputs should be compressed into:

- onboarding report
- draft architecture truth
- draft technical debt and quality baseline
- candidate deep-scan hypotheses

## Deep Scan Planning

Deep scan should never auto-run blindly.

Instead, the lead should first generate a targeted `Deep Scan Plan` with:

- scan goals
- hypotheses
- probes
- expected evidence
- risk level
- escalation points
- writeback targets

Suggested scan tranches:

- runtime tranche
- quality tranche
- architecture tranche
- performance tranche

The deep scan plan is then discussed with the user before execution.

## Deep Scan Execution

Deep scan should be based on project understanding, not a generic checklist.

It may include:

- install
- build
- test
- run
- smoke verification
- logs and failure-path inspection
- dependency and contract checks
- profiling or performance probes when warranted

The lead should escalate when probes require:

- credentials
- external paid services
- database writes
- deployment actions
- destructive or high-cost runtime operations

## Adoption Outputs

Long-lived truth must be written back into canonical state, not left inside one-off plans.

Canonical targets:

- `docs/project/PROJECT_BRIEF.md`
- `docs/project/ARCHITECTURE.md`
- `docs/project/ROADMAP.md`
- `docs/project/TECH_DEBT.md`
- `docs/status/EXECUTION_BOARD.md`
- `docs/status/ONBOARDING_STATE.md`

Working outputs:

- `docs/plans/onboarding-report-YYYY-MM-DD.md`
- `docs/plans/deep-scan-plan-YYYY-MM-DD.md`

## Plan Lifecycle

`docs/plans/` should remain a working area, not a permanent graveyard.

Add:

- `docs/plans/archive/`

Rules:

- active plans stay in `docs/plans/`
- completed, abandoned, or superseded plans move to archive or get explicitly marked
- canonical docs must be updated when a plan changes project truth
- onboarding reports and deep scan plans are not long-term truth sources

## Hardening Priorities

After phase 11, the most valuable hardening work is:

1. onboarding state and install flow
2. clearer runtime pack boundaries
3. behavior-aware orchestration checks
4. plan lifecycle and archive hygiene

Behavior-aware checks should evolve beyond file-existence checks and validate:

- onboarding state transitions
- review path invariants
- canonical writeback ownership
- install/runtime pack integrity

## Non-Goals

This tranche should not attempt:

- persistent background agents
- full packaging/publishing to an external marketplace
- one-click universal environment setup for every framework
- replacing the lead with a fully autonomous planner
- deep production deployment automation

## Validation Strategy

This design should be considered complete when the repo can:

- export a clean runtime pack into another project
- install repo-local Codex skills under `.agents/skills/`
- track onboarding progress in canonical state
- generate onboarding and deep-scan plans before runtime probing
- archive or manage stale plans cleanly
- validate the above through repo checks and tests
