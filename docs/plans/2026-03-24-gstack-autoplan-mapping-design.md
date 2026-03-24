# gstack Autoplan Mapping Design

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Port the gate mechanism, not the slash-command ceremony.</rule>
</execution_handoff>

**Goal:** Adapt the most valuable behavior from upstream `gstack /autoplan` into the Codex-native single-lead system.

## What autoplan actually gets right

1. It runs multiple review voices before implementation.
2. It auto-decides mechanical issues instead of burdening the user with every fork.
3. It separates mechanical decisions from taste decisions.
4. It writes an explicit final gate instead of burying those decisions in chat history.

## What does not translate directly

- The repeated global preamble.
- Claude-specific `AskUserQuestion` choreography.
- A user-facing slash command that exposes every intermediate review phase.
- Shell-heavy logging and telemetry.

## Codex-native mapping

The single visible `Lead` should own a repo-backed review gate with three responsibilities:

1. Record multi-role review passes.
2. Record auto-decisions taken by the team.
3. Surface only the unresolved taste decisions as the approval gate.

That means phase 5 should add:

- a canonical review gate artifact
- a `lead_loop.py review` command
- board transitions that distinguish:
  - `review` when the plan passes internal review without user escalation
  - `approval-needed` when taste decisions remain

## Why this slice comes next

Phases 3 and 4 already gave us:

- repository-backed discovery
- repository-backed planning
- repository-backed delegation

What is missing is the bridge between planning and build. That bridge is the main thing
upstream `autoplan` provides.

## Recommended artifact shape

The review gate should record:

- `inputs`
- `review passes`
- `auto decisions`
- `taste decisions`
- `recommendation`
- `approval target`

This is enough to keep the user-facing lead concise while preserving team reasoning in the repo.

## Non-goals for Phase 5

- Running real subagents or Codex sidecars automatically from the script
- Full CEO/design/eng review parity
- Reproducing upstream prompt language
- Reproducing upstream dual-voice execution
- Replacing later build/review/qa stages
