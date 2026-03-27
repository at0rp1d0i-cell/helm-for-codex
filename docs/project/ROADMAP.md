# Roadmap

## Current Milestone

Phase 18 baseline complete: the repository can now compile execution and live review packet/spec pairs into reusable bridge-launch payloads through a shared runner.

## Later Milestones

- expand validation from structural checks into richer behavior-aware orchestration checks
- let the live `Ops Orchestrator` role own more of the dispatch path instead of relying on the remaining spawn bridge
- drive more live dispatch through `scripts/role_bridge.py` rather than hand-written per-turn routing
- extend direct live role dispatch beyond packet generation and into more autonomous specialist execution
- let the live `Ops Orchestrator` consume packet plus invocation-spec pairs and hand the last-hop execution to the reusable bridge runner by default
- promote bridge-runner payloads from static launch plans into live specialist execution receipts
- execute the first bounded execution-handoff slice (delegate -> builder -> QA -> docs-sync -> board update) with installed-runtime verification from day one
- add fresh-repo smoke validation for installed runtime packs
- deepen onboarding into project-specific deep-scan tranches and runtime evidence capture
- automate more canonical state updates, handoff generation, and decision gating
- explore richer live review and build orchestration on top of canonical role-owned artifacts
