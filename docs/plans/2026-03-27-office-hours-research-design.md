# Office-Hours Research Design

## Goal

Add a research-first `office-hours` lane that introduces repository-backed research pressure before Product, Design, and Architect challenge passes run.

## Why This Exists

`Helm4Codex` now has a first-class `office-hours` lane, but it still starts from the lead's framing alone. That means the harness can challenge scope and design, yet still miss obvious open-source baselines, paper-backed approaches, or build-vs-buy alternatives.

To close that gap, research needs to become a first-class artifact in discovery rather than an optional note.

## Problem

Current `office-hours` is missing three behaviors:

- there is no distinct `Researcher` runtime surface
- there is no repository-backed research artifact chain before challenge passes
- Product / Design / Architect pressure cannot explicitly react to research findings

This means the discovery loop can still overfit to the initial proposal.

## Decision

Extend `office-hours` into this artifact chain:

`Lead intake -> office-hours brief -> research brief -> research report -> Product / Design / Architect challenge passes -> discovery gate -> office-hours report`

The first tranche should be deterministic by default, while preserving a clean path for later live-role execution.

## Artifact Model

### Research Brief

This artifact translates the discovery brief into a bounded research request. It records:

- problem framing
- research scope
- known constraints
- key questions
- recommendation target

It should be compact and explicitly tied to `office-hours`.

### Research Report

This artifact records the researcher's output in a reusable format:

- search/problem framing
- top options
- recommendation
- build-vs-buy posture
- adoption notes
- open risks

It should act as the research-side equivalent of an implementation report: a consumed artifact that later evaluators can cite.

### Challenge Passes

Product, Design, and Architect challenge passes remain repo-backed `review-pass` artifacts, but their deterministic logic should now consume both:

- the office-hours brief
- the research report

The passes should pressure-test the brief against discovered alternatives instead of just the original proposal.

### Discovery Gate

The discovery gate should now explicitly consume the research report. Its role is still to emit only:

- `reframe`
- `ready-for-plan`
- `ask-user`

but the gate logic should use research findings when deciding whether a proposal is too broad, unjustified, or still strategically unresolved.

## Role Model

### Researcher

The Researcher is discovery-side pressure, not implementation support. It should:

- challenge build-vs-buy assumptions
- surface external baselines
- recommend the default posture for planning
- note unresolved adoption risks

### Product / Design / Architect

These roles remain evaluators, but they are now expected to react to research rather than to the lead brief alone.

## Runtime Scope

This tranche should include:

- a repo-backed `Researcher` role surface
- deterministic `research-report` generation
- `office-hours run` consuming research before challenge passes
- explicit consumption of research in the discovery gate
- runtime-pack export, installer, and checks updated for the new role/artifacts

This tranche should not include:

- live browser-backed research
- external paper crawling automation
- fully live multi-role office-hours execution
- replacing `discover`

## Implementation Shape

### team_state.py

Add writers for:

- `research-brief`
- `research-report`

Update discovery-gate and office-hours-report writeback to carry research linkage.

### role_review.py

Extend office-hours deterministic mode so Product, Design, and Architect challenge passes can read the research report and sharpen their findings and taste decisions.

### lead_loop.py

Extend `office-hours` with deterministic research-first execution:

- write office-hours brief
- write research brief
- write research report
- run Product / Design / Architect challenge passes with research context
- write discovery gate
- write office-hours report

### Skills And Roles

Add:

- `skills/researcher/`
- `.agents/skills/researcher/`
- `.codex/roles/researcher.toml`
- `.codex/config.toml`
- `.codex/role_bridge.toml`

## Outcome Semantics

### reframe

Research shows the current proposal is too broad, too redundant, or too weakly justified for planning.

### ask-user

Research or cross-functional challenge surfaces a strategic or taste-heavy choice that should not be auto-decided.

### ready-for-plan

The problem is sharp enough, the external baseline is understood, and the first milestone is ready for planning.

## Why This Matches The Harness Direction

This tranche strengthens discovery-side adversarial pressure in the exact place where the harness is still weakest:

- the planner no longer frames the problem in isolation
- the evaluator pressure is grounded in external options and build-vs-buy posture
- planning starts from a challenged, research-backed brief rather than a refined intuition

## Non-Goals

- no full live office-hours role runtime yet
- no replacement of `autoplan`
- no generalized research system outside office-hours
- no automatic web browsing executor
