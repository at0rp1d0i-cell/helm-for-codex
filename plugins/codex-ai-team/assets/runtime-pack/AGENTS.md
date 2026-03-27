# AI Team Operating Guide

## Single Entry

The user speaks only to the lead. Internal specialist skills and subagents are coordinated behind that interface.

## Runtime Surface

- `.agents/skills/` is the repo-local skill discovery surface for Codex.
- `.codex/` holds project configuration, role bindings, and bridge metadata.
- Do not move runtime skills into `.codex/`; keep them in `.agents/skills/` so Codex can discover them as repo skills.

## Canonical State

Use these files as the source of truth:

- `docs/project/PROJECT_BRIEF.md`
- `docs/project/ROADMAP.md`
- `docs/project/ARCHITECTURE.md`
- `docs/project/QUALITY_BAR.md`
- `docs/project/TECH_DEBT.md`
- `docs/status/EXECUTION_BOARD.md`
- `docs/status/MODULE_CONTRACTS/`
- `docs/decisions/`
- `docs/plans/`

## Approval Escalation

Escalate to the user for structural refactors, major scope changes, high-impact architecture decisions, and cost-heavy dependency choices.
