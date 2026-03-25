# Onboarding Report: Current Repo Onboarding

## Summary

Shallow scan shows this repository is a healthy source-and-runtime harness for a Codex-native AI team. Structural verification is strong, the runtime pack is implemented and self-installable, and the main remaining uncertainty is installed-runtime behavior in a fresh external target plus the fidelity of onboarding state transitions beyond the current deterministic init path.

## Key Findings

- Canonical docs, runtime scripts, role config, and repo-local skill packaging are present and internally consistent.
- A safe verification baseline is already green: uv run pytest -q => 58 passed, scripts/check_repo.py => repo layout ok, check_docs_freshness.py => docs structure ok.
- The runtime installer now bootstraps AGENTS, .codex, .agents/skills, runtime scripts, ops templates/checks, onboarding state, and module-contract docs while preserving pre-existing canonical state in the target repo.
- The biggest structural hotspot is the dual-surface model: source skills under skills/ and installed runtime skills under .agents/skills must stay in lockstep.
- The main unverified area is behavioral rather than structural: external target install, Codex discovery of installed role config, and richer onboarding state progression beyond the current init shortcut.

## Recommendations

- Keep gstack/ out of deep scan scope unless we are explicitly doing upstream comparison work; treat it as reference-only.
- Use deep scan to validate installed-runtime behavior in a clean target repo rather than spending time on more source-repo file reading.
- Probe onboarding execution semantics, especially whether current deterministic init is sufficient or whether intermediate detect/shallow-scan/deep-scan-plan states need richer runtime support.

## Next Steps

- Approve a deep scan focused on external install, runtime discovery, onboarding transition fidelity, and review-role writeback from an installed target.
- After deep scan, decide whether to prioritize behavior-aware orchestration checks or richer onboarding/runtime automation as the next tranche.
