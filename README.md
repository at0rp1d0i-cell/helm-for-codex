# Codex-Native AI Team

This repository is both the **source** and the **dogfooding runtime** for a Codex-powered development team.  
It keeps the plans, tests, runtime scripts, repo-local skills, and canonical state that let Codex behave not as a single super-context assistant but as a disciplined, accountable engineering team.

## Team Model

The user talks only to the `Lead`. The lead stays user-facing, translates intent into approved work, and routes internal execution through `Ops`. `Ops` then dispatches the narrower specialist roles:

- `Ops`: dispatches bounded work, validates repo-backed handoff artifacts, and advances execution state without exposing internal chatter to the user.  
- `Product`: scopes requests, translates them into goals, and keeps the roadmap honest.  
- `Researcher`: surfaces papers, libraries, or precedents before committing to a build.  
- `Architect`: defines module boundaries, interfaces, and hard constraints.  
- `Builder`: implements bounded tasks inside the agreed architecture and quality constraints.  
- `Reviewer`: inspects correctness, regressions, and completeness of the proposed work.  
- `QA`: validates flows, repro steps, and automation before merging.  
- `Docs`: keeps canonical docs plus decision records aligned with the implementation.  
- `Refactor Planner`: proposes focused cleanup when technical debt blocks safe progress.  
- `Release Manager`: wraps up the final rollout, push, and verification steps.

Roles are codified as repo-local Codex skills under `.agents/skills`, and the `Lead` routes each task through `Ops` without forcing you to address multiple agents directly.

## What the Workflow Does

The system is built on four layers:

- `AGENTS.md` describes the operating guide and canonical state.  
- `.codex/config.toml` plus `.codex/roles/*.toml` bind the live orchestration, review, and execution roles to their latest installed skills.  
- `scripts/team_state.py` writes markdown artifacts such as briefs, review passes, onboarding reports, and refactor proposals.  
- `scripts/lead_loop.py` sequences the stages (`intake → discovery → plan → build → review → qa → docs-sync → ship-ready → evolve`) and keeps `docs/status/EXECUTION_BOARD.md` up to date.

The runtime pack installer copies the necessary scripts, docs, templates, and `.agents/skills` into another repo, so Codex can onboard that project and execute exactly the same orchestration.

Current live Codex role bindings cover `Ops Orchestrator`, `Product Reviewer`, `Architect Reviewer`, `Code Reviewer`, `Implementation Worker`, `QA Runner`, and `Docs Sync`. `Lead` is still the visible session entrypoint rather than a spawned role, while `Ops` now has both a live role surface and the repo-owned orchestration runtime in `scripts/ops_loop.py`.

## Agent Work Granularity

The team favors bounded, measurable slices but currently only the `Lead/Review/Onboarding/Packaging` chain has been fully exercised. Work granularity looks like this:

1. **Task brief** – the smallest unit (bug fix, doc update, refactor slice) with a clear scope, constraints, and verification. Builders and QA runners operate at this level.  
2. **Feature slice** – a concrete surface (API endpoint, screen, workflow) that may already include Builder + QA + Docs touches, but today the runtime has only locked the review/QA handoff path; docs synchronization as part of the same flow is the next tranche.  
3. **Feature branch / PR** – assigned when a slice is owned end-to-end; the lead still orchestrates review, QA, and docs before shipping, while the implementation agent focuses on the aggregated changes across task briefs.

This keeps each agent focused: they solve a small problem or slice inside a shared repository-backed plan, not a vague scope. The `Lead` stitches slices into a cohesive feature and triggers review and QA only after the slice is ready.

## Install Into Another Repo

Use the installer:

```bash
uv run python scripts/install_runtime_pack.py --target /path/to/target-repo
```

It bootstraps `AGENTS.md`, `.codex/config.toml` + roles, `.agents/skills`, runtime scripts, ops templates/checks, and canonical docs. Runtime-managed files refresh while existing canonical state stays intact, so rerunning the installer does not wipe a target repo’s `PROJECT_BRIEF`, `EXECUTION_BOARD`, `ONBOARDING_STATE`, or `AGENTS.md`.

## First Contact And Onboarding

Onboarding follows `detect → shallow-scan → deep-scan-plan → waiting-user-alignment → deep-scan → adopt`.  
Shallow scan is repo-safe and read-only. Deep scan is planned so the lead can explain what it will verify, which probes it will run, what evidence it expects, and what requires user approval.  
You can also trigger the same flow with `uv run python scripts/lead_loop.py init` or `--force` when the repo already has an onboarding state file.

## Runtime Surface

When installed, Codex only relies on:

- `AGENTS.md` for guidance  
- `.agents/skills` for role skills  
- `.codex/config.toml` and `.codex/roles/*.toml` for live role bindings  
- canonical docs under `docs/project/` and `docs/status/` for state  

Plans, tests, and design docs stay in the source repo so this runtime pack can keep evolving without dragging every historical artifact into target projects.
