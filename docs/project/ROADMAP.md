# Roadmap

## Current Milestone

Phase 14 baseline complete: the repository can now install a Codex-facing runtime pack into another repo with a live `Ops Orchestrator` role, explicit execution roles (`Implementation Worker`, `QA Runner`, `Docs Sync`), and the earlier live review roles, while keeping `Lead` as the only user-facing entrypoint.

## Later Milestones

- expand validation from structural checks into richer behavior-aware orchestration checks
- let the live `Ops Orchestrator` role own more of the dispatch path instead of relying on the current spawn bridge
- execute the first bounded execution-handoff slice (delegate -> builder -> QA -> docs-sync -> board update) with installed-runtime verification from day one
- add fresh-repo smoke validation for installed runtime packs
- deepen onboarding into project-specific deep-scan tranches and runtime evidence capture
- automate more canonical state updates, handoff generation, and decision gating
- explore richer live review and build orchestration on top of canonical role-owned artifacts
