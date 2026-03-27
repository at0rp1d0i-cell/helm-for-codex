# Autoplan Lane Design

## Goal

Productize a first-class `autoplan` lane on top of the existing discovery, plan brief, review-pass, and review-gate primitives without building the broader office-hours workflow.

## Scope

- Add a bounded `lead_loop.py autoplan` command with `run`, `prepare`, and `collect` modes.
- Keep the lane repo-backed by writing a single autoplan report that points at the underlying plan and review artifacts.
- Reuse the current review-pass and review-gate flow instead of replacing it.
- Update the lead and product contracts so the lane is visible in the skill surface.

## Approach

`autoplan run` should accept an existing plan brief or bootstrap discovery plus plan artifacts when the inputs are provided in one shot. It then runs the deterministic Product, Architect, and Reviewer passes, aggregates the review gate, and writes an autoplan report with an explicit outcome and next step.

`autoplan prepare` should package the live review handoff by creating review packets, invocation specs, and expected review-result paths, then write an autoplan report with the `in-review` outcome.

`autoplan collect` should convert live review results back into canonical review passes, regenerate the review gate, and refresh the autoplan report from the collected outputs.

## Outcome Model

- `auto-clear`: no taste decisions remain, so the next step can point at bounded builder kickoff.
- `ask-user`: taste decisions remain, so the report should direct the lead back to approval.
- `blocked`: required repo-backed inputs are missing, so the lane writes a blocked report instead of failing silently.
- `in-review`: live review packets have been prepared and the lane is waiting on role output.

## Artifacts

- `docs/plans/autoplan/autoplan-report.md`
- `docs/plans/autoplan/review-gate.md`
- `docs/plans/autoplan/review-passes/`
- `docs/plans/autoplan/review-packets/`
- `docs/plans/autoplan/invocation-specs/`
- `docs/plans/autoplan/review-results/`
- `planning/discovery/templates/autoplan-report.md`

## Non-Goals

- Full office-hours or multi-turn discovery conversation design
- New workflow stages beyond the existing board stages
- Changes to ship/release or browser-QA ownership
- Replacing live review packets with a separate planning system

## Verification

- `uv run pytest tests/test_team_state_script.py tests/test_planning_discovery_templates.py -q`
- `uv run pytest tests/test_lead_loop.py -q`
- `uv run pytest tests/test_team_lead_contract.py tests/test_internal_role_contracts.py tests/test_internal_skills.py -q`
