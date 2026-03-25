# Roadmap

## Current Milestone

Phase 12 baseline complete: the repository can now install a Codex-facing runtime pack into another repo, preserve target canonical state during re-install, bootstrap repo-local `.agents/skills`, and move unfamiliar projects through onboarding state plus deep-scan planning, and we have validated that installed runtime commands (including `lead_loop.py init`, `review-prepare`, and `review-pass`) work from the target copy.

## Later Milestones

- expand validation from structural checks into richer behavior-aware orchestration checks
- execute the first bounded execution-handoff slice (delegate -> builder -> QA -> docs-sync -> board update) with installed-runtime verification from day one
- add fresh-repo smoke validation for installed runtime packs
- deepen onboarding into project-specific deep-scan tranches and runtime evidence capture
- automate more canonical state updates, handoff generation, and decision gating
- explore richer live review and build orchestration on top of canonical role-owned artifacts
