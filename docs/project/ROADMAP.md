# Roadmap

## Current Milestone

Phase 22 in progress: close the productization gap with gstack, starting with ship/release workflow, browser-backed QA evidence, and a first-class autoplan lane.

## Later Milestones

- complete plugin-backed bootstrap validation and treat it as a first-class install path
- sharpen the external install story so users do not need source-repo knowledge to adopt or upgrade the team runtime
- add a ship/release gate that turns bounded task execution into a real daily shipping loop
- add browser-backed QA evidence and a report-only QA lane
- productize an autoplan workflow on top of existing review passes and taste-decision gates
- strengthen discovery with an office-hours style product reframing loop
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
