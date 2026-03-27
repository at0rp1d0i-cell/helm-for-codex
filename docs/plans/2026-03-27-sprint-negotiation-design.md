# Sprint Negotiation Design

## Goal

Add a repo-backed pre-build sprint negotiation lane that makes Builder feasibility and QA evaluability pressure part of sprint contract creation.

## Why This Exists

`Helm4Codex` already has a sprint contract, but today the contract is mostly written top-down by the lead and Ops. That is structurally useful, but it does not yet match the strongest harness behavior described in Anthropic's long-running application-development article:

- planner proposes the bounded task
- generator pushes back on feasibility
- evaluator pushes back on verifiability
- build starts only after the contract survives that pressure

This is the most important remaining gap between our current orchestration kernel and a stronger long-running engineering harness.

## Problem

Current build kickoff is too linear:

`Lead -> Ops build -> sprint contract -> builder dispatch`

This misses three things:

- Builder cannot challenge whether the contract is small enough or technically feasible
- QA cannot challenge whether the contract is testable or observable enough
- The final sprint contract can still overfit to planner intent rather than negotiated delivery reality

That makes the harness strong at coordination but softer than it should be at adversarial execution planning.

## Decision

Introduce a new pre-build lane with this artifact chain:

`Lead intent -> sprint proposal -> Builder sprint pass + QA sprint pass -> sprint gate -> sprint contract -> builder dispatch`

This lane should be deterministic by default and later promotable to live role execution.

## Artifact Model

### Sprint Proposal

This is the pre-contract artifact. It records:

- bounded task title
- objective
- scope
- acceptance criteria
- implementation-report target
- intended evidence posture

It is planner-owned, but not yet final.

### Sprint Passes

Two structured role passes challenge the proposal:

- `Builder`
- `QA`

They should record:

- strongest concern
- auto-decisions
- blocking issues
- recommendation

These are not implementation or QA reports. They are contract pressure artifacts.

### Sprint Gate

The gate consumes the proposal and both passes, then produces one of:

- `ready-for-build`
- `reframe-scope`
- `ask-user`

It records:

- consumed proposal
- consumed sprint passes
- negotiated contract changes
- unresolved tensions
- outcome
- next step

### Sprint Contract

The existing sprint contract remains the builder kickoff artifact, but it is no longer the first artifact. It becomes the post-gate contract produced only after the negotiation lane clears.

## Role Model

### Builder

Builder pressure is about feasibility:

- is the bounded task actually bounded
- are the contract and acceptance criteria implementable in one slice
- is the report target clear enough

### QA

QA pressure is about evaluability:

- are the acceptance criteria observable
- is the contract testable
- does the task define enough evidence and scenario surface to validate safely

## Runtime Scope

This tranche should include:

- repo-backed sprint proposal, sprint pass, and sprint gate artifacts
- deterministic `sprint-negotiate` execution
- lead/ops hooks so the preferred pre-build path goes through negotiation
- existing `build` kept as a compatibility shortcut

This tranche should not include:

- full live Builder/QA negotiation
- browser-backed execution inside negotiation itself
- replacing the existing build lane

## Implementation Shape

### team_state.py

Add writers for:

- `sprint-proposal`
- `sprint-pass`
- `sprint-gate`

### role_review.py

Extend deterministic review support with a `sprint-contract` mode that can emit:

- Builder sprint pass
- QA sprint pass

These should be driven by the sprint proposal, not by the final sprint contract.

### ops_loop.py

Add a negotiation entrypoint that:

- writes the sprint proposal
- runs deterministic Builder and QA sprint passes
- writes the sprint gate
- if clear, materializes the sprint contract and builder dispatch packet

### lead_loop.py

Add a facade command that routes the user-facing build request through Ops negotiation instead of direct build when using the preferred path.

## Outcome Semantics

### ready-for-build

The proposal is feasible and evaluable enough. Ops writes the sprint contract and builder dispatch packet, then moves the board into `build`.

### reframe-scope

The proposal is too broad or under-specified. The board remains in `plan`.

### ask-user

There is a strategic or taste-heavy tradeoff that should be escalated before build.

## Why This Matches The Harness Direction

This tranche is the direct equivalent of the generator-evaluator negotiation pressure described in Anthropic's harness writeup:

- planner proposes
- generator challenges feasibility
- evaluator challenges validation
- build starts only after the contract clears that gauntlet

It is the missing behavior layer between our existing orchestration structure and a stronger long-running engineering harness.

## Non-Goals

- no feature-branch autonomy
- no live multi-turn Builder/QA chat loop yet
- no replacement of review, QA, or release gates
- no broader project-management workflow beyond bounded pre-build negotiation
