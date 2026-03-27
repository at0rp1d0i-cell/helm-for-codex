# Office-Hours Discovery Design

## Goal

Add a first-class `office-hours` discovery lane that applies adversarial product, design, and architecture pressure before planning begins.

## Why This Exists

`Helm4Codex` already has repo-backed discovery, planning, review, QA, and release primitives. What it still lacks is a memorable discovery workflow that actively challenges the problem definition instead of merely recording it.

This lane is intended to close the biggest remaining gap with `gstack` and with the harness principles described in Anthropic's long-running application-development article:

- planner and evaluator pressure should happen before build
- generator work should start from a sharpened problem, not a vague prompt
- challenge passes should be repo-backed artifacts, not transient chat turns

## Problem

Current discovery is structurally sound but behaviorally soft:

- `discover` can write a discovery brief, but it does not create strong cross-functional pressure
- `autoplan` reviews a plan after the problem has already been framed
- there is no distinct `office-hours` style lane that asks whether the team is solving the right problem

That means the harness is good at controlled execution, but weaker at adversarial thinking.

## Decision

Introduce a dedicated `office-hours` lane with this artifact chain:

`Lead intake -> office-hours brief -> Product / Design / Architect challenge passes -> discovery gate -> office-hours report -> plan`

The lane should be repo-backed, deterministic by default, and compatible with later live-role execution.

## Artifact Model

### Office-Hours Brief

The first artifact in the lane. It records:

- problem statement
- target user or operator
- current proposal
- constraints
- success criteria
- build-vs-buy context
- assumptions to challenge

This is the discovery-side equivalent of a sprint contract: a bounded statement of what is being questioned.

### Challenge Passes

Three structured challenge artifacts, one per role:

- `Product`
- `Design`
- `Architect`

These are not implementation suggestions. They should pressure-test the brief by recording:

- strongest concern
- counterargument or reframing
- scope or quality pressure
- auto-decisions
- taste decisions
- recommendation

The existing `review-pass` structure is close enough to reuse, as long as the role semantics are discovery-specific.

### Discovery Gate

The gate aggregates challenge passes and produces one of three outcomes:

- `reframe`
- `ready-for-plan`
- `ask-user`

This is the discovery-side equivalent of the existing review gate. It records:

- consumed brief
- consumed challenge passes
- reframed problem statement
- unresolved tensions
- build-vs-buy posture
- outcome
- next step

### Office-Hours Report

A compact top-level artifact for the lead and the user. It links the brief, challenge passes, and gate, and summarizes:

- what changed in the framing
- whether the lane recommends reframe, user escalation, or planning
- the next action for the lead

## Role Model

### Product

Challenges whether the proposed work is solving the right user problem and whether scope matches the milestone.

### Design

Challenges comprehension, user flow, interaction burden, and product usability. This role is new to the current runtime surface.

### Architect

Challenges technical fit, coupling, build-vs-buy cost, and long-term maintenance pressure.

## Runtime Scope

First tranche only:

- add repo-backed office-hours artifacts
- add a deterministic `office-hours` lead command
- add deterministic challenge-pass generation for Product, Design, and Architect
- add a discovery gate writer
- add a compact office-hours report artifact
- add the Design role to the repo role/config surface

Not in this tranche:

- live multi-turn conversation orchestration inside office-hours
- browser-backed research
- external-paper or open-source runtime integration
- fully live discovery roles by default

## Implementation Shape

### team_state.py

Add writers for:

- `office-hours-brief`
- `discovery-gate`
- `office-hours-report`

### lead_loop.py

Add `office-hours` with bounded modes:

- `run`
- `prepare`
- `collect`

`run` should support deterministic challenge-pass generation.

### role_review.py

Extend deterministic review support with a discovery mode that can emit Product, Design, and Architect challenge passes from the office-hours brief.

### Skills and Config

Add a `design-review` specialist surface:

- `skills/design-review/`
- `.agents/skills/design-review/`
- `.codex/roles/design-reviewer.toml`
- `.codex/config.toml`
- `.codex/role_bridge.toml`

## Outcome Semantics

### reframe

The proposal is not ready for plan. The discovery gate rewrites the problem or scope and keeps the board in `discovery`.

### ask-user

There are unresolved user-facing tradeoffs or strategic tensions. The board moves to `approval-needed`.

### ready-for-plan

The problem framing is strong enough to move into plan creation. The board may advance to `plan`.

## Why This Matches The Harness Direction

This lane makes discovery adversarial before build:

- `Lead` remains planner/facade
- `Product / Design / Architect` act as evaluator pressure
- `Builder` does not begin until the discovery gate is satisfactory

That is the missing half of the generator-evaluator loop: not just judging implementation later, but judging framing earlier.

## Non-Goals

- no feature-branch autonomy
- no full office-hours persona theater
- no replacement of `autoplan`
- no replacement of the existing review gate

`office-hours` should complement `autoplan`, not absorb it.
