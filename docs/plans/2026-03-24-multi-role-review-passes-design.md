# Multi-Role Review Passes Design

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Make the review gate consume structured role passes before adding more orchestration layers.</rule>
</execution_handoff>

**Goal:** Upgrade the phase 5 review gate from a manual summary artifact into an aggregator of structured review passes from internal roles.

## Problem

Phase 5 introduced a useful gate, but the gate still depends on manually supplied summaries. That is not yet a real internal review pipeline. The next useful step is to make the gate read structured passes produced by concrete roles.

## Recommended scope

Start with three roles:

- `Product`
- `Architect`
- `Reviewer`

These three roles cover the same territory that upstream gstack gets from early strategic and engineering reviews, without forcing us to solve full QA, design review, or dual-model execution yet.

## Options considered

### 1. Structured review-pass artifacts plus aggregation

Each role writes a structured pass artifact. The lead review gate reads those files and derives:

- review pass summaries
- auto decisions
- taste decisions
- gate recommendation

This is the recommended option because it creates a real machine-readable handoff chain.

### 2. Extend the review gate CLI with more inline flags

Keep one artifact, but add more CLI arguments such as `--product-summary` and `--architect-summary`.

This is simpler short term, but it is not a real team artifact chain. The data still lives in one ad hoc command invocation.

### 3. Jump directly to live subagent execution

Spawn real review roles and write the aggregator around runtime results.

This is the eventual direction, but it is too early. Without structured pass artifacts first, the runtime system becomes harder to test and easier to drift.

## Recommended architecture

Add a new canonical artifact type:

- `review pass`

The artifact should record:

- role
- focus
- findings
- auto decisions
- taste decisions
- recommendation

Then upgrade `lead_loop.py review` so it can read multiple review pass files and build the review gate from them.

## Why this is the right next step

It preserves the important gstack idea:

- multiple specialist reviews before implementation

But it translates that idea into Codex-native repo state:

- file-backed handoffs
- single visible lead
- testable aggregation logic
- smaller active orchestration burden

## Non-goals

- live subagent spawning from the CLI
- full upstream autoplan parity
- QA or docs passes in the first slice
- design review integration in the first slice
