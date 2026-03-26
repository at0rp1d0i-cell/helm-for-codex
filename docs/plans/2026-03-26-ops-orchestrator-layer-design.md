# Ops Orchestrator Layer Design

## Problem

The repository currently behaves like:

`user -> Lead(+Ops mixed) -> Specialist agents`

but the intended team model is:

`user -> Lead -> Ops/Orchestrator -> Specialist agents`

This mismatch shows up in practice because the visible lead still dispatches work directly, reads and writes orchestration state itself, and acts as the runtime scheduler. That breaks the single-entry contract the user asked for and makes it hard to reason about who owns planning, who owns dispatch, and who owns stage transitions.

## Goals

- Make `Lead` a true facade layer that only handles user-facing conversation, escalation, and approvals.
- Introduce an explicit `Ops/Orchestrator` runtime layer that owns dispatch, collection, gates, and board advancement.
- Keep specialist roles narrow: they should only consume repo-backed handoff artifacts and report back to `Ops`.
- Preserve the existing file-based handoff system from phase 13.
- Keep the first `Ops` slice small enough to land without rewriting the whole harness.

## Non-Goals

- Do not introduce a queue system, daemon, or always-on event bus.
- Do not redesign the role roster.
- Do not replace repo-backed artifacts with chat-only orchestration.
- Do not couple this change to long-running cloud execution.

## Why Now

Phase 13 proved that `sprint-contract -> implementation-report -> qa-report -> docs-sync-report` is a good handoff spine, but it also exposed a structural problem: the visible lead still directly invokes worker behavior. If we keep building on top of that shape, every later tranche will preserve the same boundary violation.

## Approaches Considered

### 1. Naming-Only Ops

Keep the current runtime as-is and just describe part of `lead_loop.py` as “Ops”.

This is cheap, but fake. It does not create a new boundary, does not change ownership, and will keep leaking direct lead dispatch behavior into later features.

### 2. Explicit Ops Runtime Behind The Lead

Add an `ops_loop.py` runtime that owns task dispatch, gate evaluation, handoff validation, and stage advancement. Keep `lead_loop.py` as the user-facing facade that writes intent or approval artifacts and invokes `ops_loop.py` for execution moves.

This is the recommended option. It creates a real boundary without forcing a full harness rewrite.

### 3. Full Event-Driven Orchestrator

Model every handoff as an event stream with queues and state reducers.

This is too heavy for the current repo. It would add system complexity before the simpler boundary is even proven.

## Recommendation

Use **Explicit Ops Runtime Behind The Lead**.

The resulting structure becomes:

- `Lead`: user-facing facade, intent intake, explanations, approvals, escalation.
- `Ops`: runtime dispatcher, artifact/gate validator, board owner, stage mover.
- `Specialists`: bounded workers that only consume repo-backed packets and produce repo-backed outputs.

## Layer Responsibilities

### Lead Layer

The lead:

- talks to the user
- translates user input into an approved intent or question
- can request status from canonical state
- can approve or reject `Ops` recommendations
- does not directly dispatch specialist tasks
- does not directly own build/qa/docs-sync stage movement

### Ops Layer

The orchestrator:

- reads canonical state
- creates or validates handoff packets
- dispatches work to specialists
- validates gate preconditions
- writes or advances `EXECUTION_BOARD`
- records when a stage is blocked, passed, or needs escalation

### Specialist Layer

Specialists:

- do not talk to the user
- do not decide whether the project advances
- do not invent their own task context from chat history
- only consume the artifacts named by `Ops`

## Artifact Contract

The current phase 13 artifacts stay load-bearing:

- `sprint-contract`
- `implementation-report`
- `qa-report`
- `docs-sync-report`

The change is ownership:

- `Lead` authorizes that a bounded task should proceed
- `Ops` creates and validates the operative packet
- specialists consume and produce the packet chain
- `Ops` advances the board only when the current gate passes

## First Slice

The first `Ops` slice should not rewrite the whole repo. It should:

1. checkpoint the current phase 13 Task 4 work so the tree is clean
2. add `scripts/ops_loop.py`
3. move the build/qa/docs-sync execution commands behind `ops_loop.py`
4. keep `lead_loop.py` as a facade that no longer owns worker dispatch
5. update contracts and tests so the new ownership is explicit

## Rules

- `Lead` may create intent, approval, and escalation records.
- `Ops` is the only layer allowed to advance `build -> qa -> docs-sync -> ship-ready`.
- `Ops` is the only layer allowed to dispatch specialist workers.
- repo-backed artifacts remain the only accepted handoff surface.
- every writeback target must stay under `docs/` unless explicitly approved otherwise.

## Testing Strategy

The first `Ops` tranche should be verified at three levels:

- unit-level command tests for `ops_loop.py`
- facade tests proving `lead_loop.py` delegates rather than owns dispatch
- installed-runtime tests proving the same `Ops` path works after runtime-pack installation

## Risks

- Partial migration may leave duplicate logic in `lead_loop.py` and `ops_loop.py`.
- If we move too much at once, phase 13 and the new `Ops` layer will blur together.
- If we move too little, the user-facing lead will still effectively be the scheduler.

## Mitigation

- keep the first slice narrow
- checkpoint current phase 13 work before migration
- move one orchestration lane at a time
- add explicit tests for ownership boundaries, not only happy-path behavior

## Expected Outcome

After this change, the repository should finally reflect the intended mental model:

`user -> Lead -> Ops -> Specialists`

That gives the user a true single entry point while making the runtime scheduler explicit, testable, and easier to evolve.
