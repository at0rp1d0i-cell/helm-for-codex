# Roadmap

## Current Milestone

Phase 15 baseline complete: the repository can now install a Codex-facing runtime pack with a repo-backed role invocation bridge, so live team roles stay canonical even when the underlying session tool only exposes generic agent classes.

## Later Milestones

- expand validation from structural checks into richer behavior-aware orchestration checks
- let the live `Ops Orchestrator` role own more of the dispatch path instead of relying on the remaining spawn bridge
- drive more live dispatch through `scripts/role_bridge.py` rather than hand-written per-turn routing
- execute the first bounded execution-handoff slice (delegate -> builder -> QA -> docs-sync -> board update) with installed-runtime verification from day one
- add fresh-repo smoke validation for installed runtime packs
- deepen onboarding into project-specific deep-scan tranches and runtime evidence capture
- automate more canonical state updates, handoff generation, and decision gating
- explore richer live review and build orchestration on top of canonical role-owned artifacts
