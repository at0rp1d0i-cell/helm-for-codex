# Deep Scan Plan: Current Repo Onboarding

## Goals

Validate that the Codex-native AI team runtime behaves correctly when installed into a fresh target repo, that first-contact onboarding produces the intended repository-backed artifacts, and that installed review-role/runtime paths remain operational outside the source repo.

## Hypotheses

The source repo baseline is sound, but the highest remaining risks are at the installed-runtime edge: Codex discovery of .agents/skills and .codex config, re-install preservation semantics under real target edits, and the gap between documented onboarding states and the currently implemented init shortcut.

## Probes

- Install the runtime pack into a clean temporary target repo and inspect the exported runtime surface (.agents/skills, .codex, scripts, ops, canonical docs).
- Modify canonical state in that temporary target and re-run the installer to confirm preserved files stay intact while runtime-managed files refresh.
- From the installed target, run the repo-backed onboarding path to generate onboarding report, deep scan plan, onboarding state, and approval-needed execution-board state.
- Validate installed role config and runtime commands by exercising review preparation or direct review-pass writeback from the installed target, not just the source repo.
- Perform a focused smoke test for source/runtime mirror integrity after install, including team-lead and the three review-role skills.

## Expected Evidence

- Installer exits zero and the target contains the expected runtime surface with no missing required paths.
- Target-side edits to PROJECT_BRIEF, ONBOARDING_STATE, and AGENTS survive re-install while runtime scripts and skill mirror remain refreshed.
- Installed repo can create onboarding artifacts and lands in waiting-user-alignment/approval-needed without manual file scaffolding.
- Installed role config resolves .agents/skills paths correctly and review-role writeback commands succeed from the installed target.

## Risk Level

medium

## Escalation Points

- If deep scan needs real Codex interactive discovery beyond repo-backed smoke commands, pause and decide whether to use this source repo or a separate throwaway target under active Codex control.
- If any probe suggests installer output can still drift from source/runtime expectations, pause before changing packaging semantics or canonical doc ownership rules.

## Writeback Targets

- docs/project/PROJECT_BRIEF.md
- docs/project/ROADMAP.md
- docs/project/ARCHITECTURE.md
- docs/project/TECH_DEBT.md
- docs/status/ONBOARDING_STATE.md
- docs/status/EXECUTION_BOARD.md
