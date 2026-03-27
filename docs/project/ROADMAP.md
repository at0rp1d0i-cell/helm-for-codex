# Roadmap

## Current Milestone

Phase 22 in progress: build the second productization tranche after landing research-first `office-hours`, `autoplan`, browser-QA evidence, and release gate/prep workflows. The next step on the discovery side is promoting `office-hours` from deterministic research-backed passes into richer live discovery execution.

## Later Milestones

- complete plugin-backed bootstrap validation and treat it as a first-class install path
- sharpen the external install story so users do not need source-repo knowledge to adopt or upgrade the team runtime
- extend browser-QA evidence into a fuller browser-backed QA runtime and a clearer report-only lane
- deepen ship/release from readiness gates into a more complete daily shipping workflow
- harden office-hours from deterministic research-backed challenge passes into live discovery roles
- expand validation from structural checks into richer behavior-aware orchestration checks
- let the live `Ops Orchestrator` role own more of the dispatch path instead of relying on the remaining spawn bridge
- drive more live dispatch through `scripts/role_bridge.py` rather than hand-written per-turn routing
- extend direct live role dispatch beyond packet generation and into more autonomous specialist execution
- let the live `Ops Orchestrator` consume packet plus invocation-spec pairs and hand the last-hop execution to the reusable bridge runner by default
- promote bridge-runner payloads from static launch plans into live specialist execution receipts
- let Ops tie execution receipts back into stage advancement and failure handling rather than recording them as side-channel evidence only
- execute the first bounded execution-handoff slice (delegate -> builder -> QA -> docs-sync -> board update) with installed-runtime verification from day one
- add fresh-repo smoke validation for installed runtime packs
- deepen onboarding into project-specific deep-scan tranches and runtime evidence capture
- automate more canonical state updates, handoff generation, and decision gating
- explore richer live review and build orchestration on top of canonical role-owned artifacts
