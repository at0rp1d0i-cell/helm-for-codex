# Live Role Review Execution Design

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Prefer a testable role runner before binding review passes to live subagents.</rule>
</execution_handoff>

**Goal:** Turn structured review passes into real role execution by introducing a unified runtime that generates Product, Architect, and Reviewer passes from repository state and a planning artifact.

## Problem

Phase 6 added structured review pass artifacts, but those passes are still written manually through the lead loop CLI. The system can aggregate role output, but it cannot yet execute role logic itself.

## Options

### 1. Keep manual pass creation and improve prompts

This is the lowest effort path, but it does not actually advance the runtime. The team still depends on hand-authored pass content.

### 2. Add a repo-backed role runner

Introduce a single script that reads canonical docs and a plan artifact, then emits role-specific review passes for Product, Architect, and Reviewer.

This is the recommended option because it gives the team a real execution layer while remaining deterministic and testable.

### 3. Jump directly to live subagent execution

This is the eventual destination, but it would couple orchestration, runtime availability, and agent behavior before the repo has a stable execution contract.

## Recommended architecture

Add:

- `scripts/role_review.py`

This script should:

- read canonical project docs
- read a plan brief
- run role-specific review logic
- write a `review-pass` artifact

Then add a lead-loop command that:

- runs `role_review.py` for Product, Architect, and Reviewer
- writes three review pass artifacts
- aggregates them into the existing review gate

## Role logic for the first slice

### Product

- checks milestone fit against project brief and roadmap
- flags possible scope creep
- emits a taste decision only when scope looks borderline

### Architect

- checks module fit against architecture docs and constraints
- flags boundary expansion
- emits a taste decision only when architecture coverage looks insufficient

### Reviewer

- checks exit criteria against quality bar
- flags missing verification expectations
- emits a taste decision only when the plan omits quality expectations that need approval

## Why this is the right next step

This keeps the system on the main line:

- single visible lead
- repository-backed orchestration
- increasingly real internal team execution

It also sets up the next step cleanly:

- replace deterministic role logic with actual role agents later, without changing artifacts or the review gate contract

## Non-goals

- live agent spawning from the CLI
- QA and Docs runtime passes in the first slice
- replacing the current review gate structure
