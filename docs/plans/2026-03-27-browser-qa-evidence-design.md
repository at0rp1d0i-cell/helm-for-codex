# Browser QA Evidence Design

## Goal

Add a repo-backed browser QA evidence surface without introducing the full browser runtime yet.

## Options Considered

1. Expand `qa-report` only with screenshot placeholder sections.
2. Add a companion `qa-evidence` artifact while keeping `qa-report` as the canonical summary.
3. Delay evidence artifacts until a real browser runner exists.

## Decision

Choose option 2.

Keep `qa-report` load-bearing for the phase-13 handoff chain, but make it point to a new `qa-evidence` companion artifact. The companion holds the screenshot placeholder ledger and additional artifact placeholders so Ops and QA have a clearer handoff path without pretending that browser capture is already live.

## Artifact Shape

- `qa-report` remains the canonical pass/fail summary and now records the consumed QA dispatch packet, the companion evidence path, and browser evidence status.
- `qa-evidence` is repo-backed markdown that records evidence mode, scenario coverage, screenshot placeholders, and additional placeholder artifact paths.
- Default placeholder paths live under `docs/plans/qa-artifacts/<task>/...` so future runtime capture can write into a stable location without changing the contract.

## Runtime Scope

- `ops_loop.py qa-prepare` advertises the evidence contract in the QA dispatch packet.
- `ops_loop.py qa` writes both the canonical report and the evidence companion by default.
- `team_state.py` gets explicit `qa-report` and `qa-evidence` writers so the evidence path is not hidden inside Ops-only string assembly.

## Non-Goals

- No live browser automation.
- No binary screenshot generation.
- No change to docs-sync ownership or release packaging in this tranche.
