# Live Office-Hours Execution Design

## Goal

Promote `office-hours` from a deterministic research-backed discovery lane into a live discovery execution lane with repo-backed packets, invocation specs, and collect-time aggregation.

## Why This Exists

`Helm4Codex` now has strong discovery structure:

- office-hours brief
- research brief
- research report
- Product / Design / Architect challenge passes
- discovery gate
- office-hours report

What it still lacks is live execution behavior. The lead can run the deterministic lane, but cannot yet prepare live discovery work, let roles write back, and then collect those results into the canonical gate. This is the biggest remaining gap on the discovery side between the current runtime and the harness direction described in Anthropic's long-running application-development article.

## Problem

Current `office-hours` modes are asymmetric:

- `run` is fully functional
- `prepare` writes an in-review placeholder only
- `collect` writes a blocked placeholder only

That means discovery still cannot operate like the existing live review lane.

## Decision

Extend `office-hours` into a true live execution lane with this shape:

`office-hours brief -> research brief -> discovery packets -> invocation specs -> live writeback -> collect -> discovery gate -> office-hours report`

`run` remains the deterministic fallback. `prepare` and `collect` become the live path.

## Artifact Model

### Discovery Packets

Use repo-backed dispatch packets, stored under the office-hours artifact directory, for:

- `Researcher`
- `Product`
- `Design`
- `Architect`

These packets should bind:

- logical repo role
- runtime skill and metadata
- consumed artifacts
- expected writeback target
- completion command

This keeps the final bridge hop explicit and consistent with the rest of Helm4Codex.

### Invocation Specs

Each live discovery packet gets a paired invocation spec, just like build, QA, docs-sync, and review.

### Live Writeback Targets

Preferred live writeback should be direct canonical artifacts:

- `Researcher` -> `research-report.md`
- `Product` -> `challenge-passes/product.md`
- `Design` -> `challenge-passes/design.md`
- `Architect` -> `challenge-passes/architect.md`

Compatibility capture can still use `review-result`-style files for Product / Design / Architect, but that should not be the preferred path.

### Collect

`office-hours collect` should:

- verify research output exists
- prefer direct challenge-pass writeback
- optionally convert compatibility results into challenge passes when present
- write the discovery gate
- write the office-hours report
- move the board based on the gate outcome

## Runtime Scope

This tranche should include:

- real `office-hours --mode prepare`
- real `office-hours --mode collect`
- office-hours packet and invocation directories
- collect-time aggregation from live outputs
- deterministic `run` preserved as fallback

This tranche should not include:

- browser-backed or web-search-backed research runtime
- multi-turn conversational discovery theater
- live role execution itself inside this session's tooling

## Implementation Shape

### lead_loop.py

Extend `_office_hours_paths()` to include:

- discovery packet paths
- invocation spec paths
- compatibility result paths

Replace placeholder `prepare` and `collect` behavior with live orchestration:

- `prepare` writes packets and invocation specs and marks the lane `in-review`
- `collect` validates or converts role outputs and then writes the gate/report

### team_state.py

No new artifact types are required if live office-hours reuses:

- `dispatch-packet`
- `invocation-spec`
- `review-pass`
- `review-result`
- existing research report writeback

The office-hours report should expand to mention the live packet/result surfaces.

### Contracts

Update:

- `team-lead`
- `researcher`
- `product-discovery`
- `design-review`
- `architecture-review`

so live office-hours prepare/collect is visible as the preferred live discovery path, with deterministic `run` as fallback.

## Outcome Semantics

### in-review

Used only by `prepare`, indicating that live discovery work is outstanding.

### blocked

Used by `collect` when required live artifacts are missing.

### ready-for-plan / reframe / ask-user

Computed by the same gate logic as deterministic `run`, but now driven by live outputs.

## Why This Matches The Harness Direction

This tranche upgrades discovery from “artifact exists” to “artifact can be produced and collected through a live role loop.” That closes another piece of the gap between our current system and a more complete long-running harness:

- planner prepares bounded live work
- specialists write back through repo contracts
- collect produces a canonical gate

It does not yet make discovery fully live in practice, but it gives the harness a real live-discovery interface.

## Non-Goals

- no full live researcher browser/runtime
- no installation rollout yet
- no replacement of deterministic office-hours
- no attempt to solve live sprint negotiation in the same tranche
