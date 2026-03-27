import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "team_state.py"


def run_team_state(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_task_brief_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "task-brief",
        "--output",
        "docs/plans/task-brief-demo.md",
        "--title",
        "Lead handoff",
        "--objective",
        "Create a bounded task brief",
        "--scope",
        "Only update planning artifacts",
        "--constraints",
        "No source code edits",
        "--decisions",
        "Use XML-like contracts",
        "--expected-output",
        "A concise handoff doc",
        "--writeback",
        "docs/status/EXECUTION_BOARD.md",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "task-brief-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Task Brief: Lead handoff" in content
    assert "## Objective" in content
    assert "## Scope" in content
    assert "## Constraints" in content
    assert "## Relevant Decisions" in content
    assert "## Expected Output" in content
    assert "## Writeback Target" in content


def test_discovery_brief_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "discovery-brief",
        "--output",
        "docs/plans/discovery-demo.md",
        "--title",
        "Daily briefing research",
        "--problem",
        "The project needs a sharper discovery artifact",
        "--research-scope",
        "Look at product references and technical references",
        "--open-questions",
        "What should be built now versus later?",
        "--recommendation-target",
        "docs/project/PROJECT_BRIEF.md",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "discovery-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Discovery Brief: Daily briefing research" in content
    assert "## Problem Signal" in content
    assert "## Research Scope" in content
    assert "## Open Questions" in content
    assert "## Recommendation Target" in content


def test_office_hours_brief_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "office-hours-brief",
        "--output",
        "docs/plans/office-hours-brief-demo.md",
        "--title",
        "Pixiu office hours",
        "--problem-statement",
        "The project needs a sharper daily experimentation loop.",
        "--target-user",
        "ML engineer running local experiments",
        "--current-proposal",
        "Build a full experimentation platform for every workflow.",
        "--constraint",
        "Keep the first milestone within one bounded slice.",
        "--success-criterion",
        "One experiment can be created and reviewed without manual glue.",
        "--build-vs-buy-context",
        "A partial in-house flow is acceptable, but building a full platform from scratch is risky.",
        "--assumption-to-challenge",
        "Users need the whole platform immediately.",
        "--assumption-to-challenge",
        "Custom orchestration is better than integrating existing tooling.",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "office-hours-brief-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Office-Hours Brief: Pixiu office hours" in content
    assert "## Problem Statement" in content
    assert "## Target User Or Operator" in content
    assert "## Current Proposal" in content
    assert "## Build vs Buy Context" in content
    assert "## Assumptions To Challenge" in content


def test_plan_brief_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "plan-brief",
        "--output",
        "docs/plans/plan-demo.md",
        "--title",
        "Phase 4 orchestration slice",
        "--goal",
        "Move from discovery into execution",
        "--milestone",
        "Phase 4",
        "--modules",
        "scripts/team_state.py, scripts/lead_loop.py, skills/team-lead/SKILL.md",
        "--exit-criteria",
        "Discovery and plan artifacts are repo-backed and tested",
        "--writeback",
        "docs/status/EXECUTION_BOARD.md",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "plan-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Plan Brief: Phase 4 orchestration slice" in content
    assert "## Goal" in content
    assert "## Milestone" in content
    assert "## Modules In Scope" in content
    assert "## Exit Criteria" in content
    assert "## Writeback Target" in content


def test_discovery_gate_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "discovery-gate",
        "--output",
        "docs/plans/discovery-gate-demo.md",
        "--title",
        "Pixiu office hours",
        "--office-hours-brief",
        "docs/plans/office-hours-brief-demo.md",
        "--challenge-pass",
        "docs/plans/challenge-passes/product.md",
        "--challenge-pass",
        "docs/plans/challenge-passes/design.md",
        "--challenge-pass",
        "docs/plans/challenge-passes/architect.md",
        "--reframed-problem-statement",
        "Focus the first milestone on one critical experiment path.",
        "--build-vs-buy-posture",
        "Current build-vs-buy posture is acceptable for planning.",
        "--unresolved-tension",
        "Decide whether to narrow scope before planning.",
        "--outcome",
        "reframe",
        "--next-step",
        "Rewrite the brief around one user-facing milestone.",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "discovery-gate-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Discovery Gate: Pixiu office hours" in content
    assert "docs/plans/office-hours-brief-demo.md" in content
    assert "docs/plans/challenge-passes/design.md" in content
    assert "## Reframed Problem Statement" in content
    assert "## Build vs Buy Posture" in content
    assert "## Outcome" in content
    assert "reframe" in content


def test_office_hours_report_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "office-hours-report",
        "--output",
        "docs/plans/office-hours-report-demo.md",
        "--title",
        "Pixiu office hours",
        "--mode",
        "run",
        "--outcome",
        "ready-for-plan",
        "--office-hours-brief",
        "docs/plans/office-hours-brief-demo.md",
        "--challenge-pass",
        "docs/plans/challenge-passes/product.md",
        "--challenge-pass",
        "docs/plans/challenge-passes/design.md",
        "--discovery-gate",
        "docs/plans/discovery-gate-demo.md",
        "--reframing-change",
        "Narrowed the first milestone to one critical experiment path.",
        "--next-action",
        "Write the plan brief for the narrowed milestone.",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "office-hours-report-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Office-Hours Report: Pixiu office hours" in content
    assert "## Outcome" in content
    assert "ready-for-plan" in content
    assert "docs/plans/office-hours-brief-demo.md" in content
    assert "docs/plans/discovery-gate-demo.md" in content
    assert "## Reframing Changes" in content
    assert "## Next Action" in content


def test_autoplan_report_command_writes_markdown_with_discovery_and_decisions(
    tmp_path: Path,
) -> None:
    result = run_team_state(
        tmp_path,
        "autoplan-report",
        "--output",
        "docs/plans/autoplan-demo.md",
        "--title",
        "Phase 14 autoplan",
        "--mode",
        "run",
        "--discovery-brief",
        "docs/plans/discovery-demo.md",
        "--plan-brief",
        "docs/plans/plan-demo.md",
        "--review-pass",
        "docs/plans/review-passes/product.md",
        "--review-pass",
        "docs/plans/review-passes/architect.md",
        "--review-pass",
        "docs/plans/review-passes/reviewer.md",
        "--review-gate",
        "docs/plans/review-gate-demo.md",
        "--outcome",
        "ask-user",
        "--auto-decision",
        "Keep the current milestone boundary",
        "--taste-decision",
        "Decide whether to narrow scope before build",
        "--next-step",
        "Resolve taste decisions before build.",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "autoplan-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Autoplan Report: Phase 14 autoplan" in content
    assert "## Discovery Brief" in content
    assert "docs/plans/discovery-demo.md" in content
    assert "## Plan Brief" in content
    assert "docs/plans/plan-demo.md" in content
    assert "## Review Passes" in content
    assert "docs/plans/review-passes/product.md" in content
    assert "## Review Gate" in content
    assert "docs/plans/review-gate-demo.md" in content
    assert "## Outcome" in content
    assert "ask-user" in content
    assert "## Auto Decisions" in content
    assert "## Taste Decisions" in content
    assert "## Next Step" in content


def test_sprint_contract_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "sprint-contract",
        "--output",
        "docs/plans/sprint-contract-demo.md",
        "--title",
        "Task 1 builder kickoff",
        "--planner",
        "Lead defines the bounded handoff and acceptance criteria",
        "--generator",
        "Builder implements only the artifact writers and templates",
        "--evaluator",
        "QA and Docs consume the artifact chain before board advancement",
        "--scope",
        "team_state artifact writers and matching templates only",
        "--acceptance",
        "Sprint contract, implementation report, qa report template, and docs sync report are repo-backed",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "sprint-contract-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Sprint Contract: Task 1 builder kickoff" in content
    assert "## Planner" in content
    assert "Lead defines the bounded handoff and acceptance criteria" in content
    assert "## Generator" in content
    assert "Builder implements only the artifact writers and templates" in content
    assert "## Evaluator" in content
    assert "QA and Docs consume the artifact chain before board advancement" in content
    assert "## Scope" in content
    assert "## Acceptance Criteria" in content


def test_implementation_report_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "implementation-report",
        "--output",
        "docs/plans/implementation-report-demo.md",
        "--title",
        "Task 1 implementation report",
        "--sprint-contract",
        "docs/plans/sprint-contract-demo.md",
        "--summary",
        "Added bounded artifact writers for the execution handoff chain",
        "--files-touched",
        "scripts/team_state.py, ops/templates/sprint-contract.md",
        "--tests-run",
        "uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q",
        "--follow-ups",
        "QA handoff still lands in phase 13 task 3",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "implementation-report-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Implementation Report: Task 1 implementation report" in content
    assert "## Consumed Sprint Contract" in content
    assert "docs/plans/sprint-contract-demo.md" in content
    assert "## Generator Summary" in content
    assert "## Files Touched" in content
    assert "## Tests Run" in content
    assert "## Follow-Ups" in content


def test_qa_report_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "qa-report",
        "--output",
        "docs/plans/qa-report-demo.md",
        "--title",
        "Task 1 QA report",
        "--sprint-contract",
        "docs/plans/sprint-contract-demo.md",
        "--implementation-report",
        "docs/plans/implementation-report-demo.md",
        "--qa-dispatch-packet",
        "docs/plans/qa-dispatch-demo.md",
        "--browser-evidence-mode",
        "browser-placeholder",
        "--browser-evidence-manifest",
        "docs/plans/qa-evidence-demo.md",
        "--browser-evidence-status",
        "placeholder",
        "--browser-evidence-artifact-root",
        "docs/plans/qa-artifacts/demo",
        "--environment",
        "Fresh repo checkout",
        "--scenario",
        "Open the dashboard in a seeded repo",
        "--issue",
        "Console log placeholder still empty",
        "--verification-status",
        "failed",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "qa-report-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# QA Report: Task 1 QA report" in content
    assert "## Consumed Sprint Contract" in content
    assert "docs/plans/sprint-contract-demo.md" in content
    assert "## Consumed Implementation Report" in content
    assert "docs/plans/implementation-report-demo.md" in content
    assert "## Consumed QA Dispatch Packet" in content
    assert "docs/plans/qa-dispatch-demo.md" in content
    assert "## Browser Evidence Status" in content
    assert "placeholder" in content
    assert "## Browser Evidence Mode" in content
    assert "browser-placeholder" in content
    assert "## Browser Evidence Manifest" in content
    assert "docs/plans/qa-evidence-demo.md" in content
    assert "## Browser Evidence Artifact Root" in content
    assert "docs/plans/qa-artifacts/demo" in content
    assert "## Scenarios Tested" in content
    assert "Open the dashboard in a seeded repo" in content
    assert "## Issues Found" in content
    assert "Console log placeholder still empty" in content
    assert "## Verification Status" in content
    assert "failed" in content


def test_qa_evidence_manifest_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "qa-evidence-manifest",
        "--output",
        "docs/plans/qa-evidence-demo.md",
        "--title",
        "Task 1 QA evidence",
        "--qa-report",
        "docs/plans/qa-report-demo.md",
        "--qa-dispatch-packet",
        "docs/plans/qa-dispatch-demo.md",
        "--sprint-contract",
        "docs/plans/sprint-contract-demo.md",
        "--implementation-report",
        "docs/plans/implementation-report-demo.md",
        "--evidence-mode",
        "browser-placeholder",
        "--browser-evidence-status",
        "placeholder",
        "--artifact-root",
        "docs/plans/qa-artifacts/demo",
        "--environment",
        "Fresh repo checkout",
        "--scenario",
        "Open the dashboard in a seeded repo",
        "--screenshot-target",
        "docs/plans/qa-artifacts/demo/screenshots/scenario-01.png | Open the dashboard in a seeded repo",
        "--dom-target",
        "docs/plans/qa-artifacts/demo/dom/scenario-01.md | DOM snapshot placeholder for Open the dashboard in a seeded repo",
        "--console-target",
        "docs/plans/qa-artifacts/demo/console/scenario-01.log | Console log placeholder for Open the dashboard in a seeded repo",
        "--note",
        "Browser runtime capture is not wired yet.",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "qa-evidence-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# QA Evidence Manifest: Task 1 QA evidence" in content
    assert "## Consumed QA Report" in content
    assert "docs/plans/qa-report-demo.md" in content
    assert "## Consumed QA Dispatch Packet" in content
    assert "docs/plans/qa-dispatch-demo.md" in content
    assert "## Consumed Sprint Contract" in content
    assert "docs/plans/sprint-contract-demo.md" in content
    assert "## Consumed Implementation Report" in content
    assert "docs/plans/implementation-report-demo.md" in content
    assert "## Evidence Mode" in content
    assert "browser-placeholder" in content
    assert "## Artifact Root" in content
    assert "docs/plans/qa-artifacts/demo" in content
    assert "## Screenshot Targets" in content
    assert "docs/plans/qa-artifacts/demo/screenshots/scenario-01.png" in content
    assert "## DOM Snapshot Targets" in content
    assert "docs/plans/qa-artifacts/demo/dom/scenario-01.md" in content
    assert "## Console Log Targets" in content
    assert "docs/plans/qa-artifacts/demo/console/scenario-01.log" in content
    assert "## Notes" in content
    assert "Browser runtime capture is not wired yet." in content


def test_dispatch_packet_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "dispatch-packet",
        "--output",
        "docs/plans/builder-dispatch-demo.md",
        "--title",
        "Task 1 builder dispatch",
        "--role",
        "Builder",
        "--logical-role",
        "implementation-worker",
        "--bridge-agent-type",
        "worker",
        "--bridge-model",
        "gpt-5.4",
        "--bridge-reasoning-effort",
        "high",
        "--role-skill",
        ".agents/skills/implementation-worker/SKILL.md",
        "--role-metadata",
        ".agents/skills/implementation-worker/agents/openai.yaml",
        "--role-writeback-target",
        "docs/plans/implementation-report-demo.md",
        "--role-writeback-command",
        "uv run python scripts/team_state.py implementation-report --output docs/plans/implementation-report-demo.md ...",
        "--objective",
        "Implement the bounded task only.",
        "--consumed-artifact",
        "docs/plans/sprint-contract-demo.md",
        "--constraints",
        "Stay within the approved sprint contract.",
        "--expected-output",
        "Implementation report at docs/plans/implementation-report-demo.md",
        "--writeback-target",
        "docs/plans/implementation-report-demo.md",
        "--completion-command",
        "uv run python scripts/team_state.py implementation-report ...",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "builder-dispatch-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Dispatch Packet: Task 1 builder dispatch" in content
    assert "## Role" in content
    assert "## Logical Role" in content
    assert "implementation-worker" in content
    assert "## Invocation Bridge" in content
    assert "- agent_type: worker" in content
    assert "- model: gpt-5.4" in content
    assert "- reasoning_effort: high" in content
    assert "## Runtime Role Binding" in content
    assert ".agents/skills/implementation-worker/SKILL.md" in content
    assert ".agents/skills/implementation-worker/agents/openai.yaml" in content
    assert "canonical_writeback_target: docs/plans/implementation-report-demo.md" in content
    assert "scripts/team_state.py implementation-report" in content
    assert "## Consumed Artifacts" in content
    assert "docs/plans/sprint-contract-demo.md" in content
    assert "## Writeback Target" in content
    assert "## Completion Command" in content


def test_invocation_spec_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "invocation-spec",
        "--output",
        "docs/plans/invocation-specs/builder.md",
        "--title",
        "Task 1 builder invocation",
        "--role",
        "Implementation Worker",
        "--logical-role",
        "implementation-worker",
        "--source-packet",
        "docs/plans/builder-dispatch-demo.md",
        "--bridge-agent-type",
        "worker",
        "--bridge-model",
        "gpt-5.4",
        "--bridge-reasoning-effort",
        "high",
        "--runtime-skill",
        ".agents/skills/implementation-worker/SKILL.md",
        "--metadata",
        ".agents/skills/implementation-worker/agents/openai.yaml",
        "--consumed-artifact",
        "docs/plans/builder-dispatch-demo.md",
        "--consumed-artifact",
        "docs/plans/sprint-contract-demo.md",
        "--expected-writeback-target",
        "docs/plans/implementation-report-demo.md",
        "--expected-writeback-command",
        "uv run python scripts/team_state.py implementation-report ...",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "invocation-specs" / "builder.md"
    assert out.exists()
    content = out.read_text()
    assert "# Invocation Spec: Task 1 builder invocation" in content
    assert "## Logical Role" in content
    assert "implementation-worker" in content
    assert "## Source Packet" in content
    assert "docs/plans/builder-dispatch-demo.md" in content
    assert "## Invocation Bridge" in content
    assert "- agent_type: worker" in content
    assert "- model: gpt-5.4" in content
    assert "## Runtime Skill" in content
    assert ".agents/skills/implementation-worker/SKILL.md" in content
    assert "## Role Metadata" in content
    assert ".agents/skills/implementation-worker/agents/openai.yaml" in content
    assert "## Consumed Artifacts" in content
    assert "docs/plans/sprint-contract-demo.md" in content
    assert "## Expected Writeback Target" in content
    assert "docs/plans/implementation-report-demo.md" in content
    assert "## Expected Writeback Command" in content


def test_execution_receipt_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "execution-receipt",
        "--output",
        "docs/plans/execution-receipts/builder.md",
        "--title",
        "Task 1 builder receipt",
        "--role",
        "Implementation Worker",
        "--logical-role",
        "implementation-worker",
        "--source-packet",
        "docs/plans/builder-dispatch-demo.md",
        "--invocation-spec",
        "docs/plans/builder-dispatch-demo-invocation.md",
        "--launch-payload",
        "docs/plans/bridge-launches/builder.json",
        "--execution-status",
        "succeeded",
        "--expected-writeback-target",
        "docs/plans/implementation-report-demo.md",
        "--writeback-status",
        "written",
        "--specialist-note",
        "Implementation report written successfully.",
        "--follow-up",
        "None",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "execution-receipts" / "builder.md"
    assert out.exists()
    content = out.read_text()
    assert "# Execution Receipt: Task 1 builder receipt" in content
    assert "## Logical Role" in content
    assert "implementation-worker" in content
    assert "## Source Packet" in content
    assert "docs/plans/builder-dispatch-demo.md" in content
    assert "## Invocation Spec" in content
    assert "docs/plans/builder-dispatch-demo-invocation.md" in content
    assert "## Launch Payload" in content
    assert "docs/plans/bridge-launches/builder.json" in content
    assert "## Execution Status" in content
    assert "succeeded" in content
    assert "## Expected Writeback Target" in content
    assert "docs/plans/implementation-report-demo.md" in content
    assert "## Writeback Status" in content
    assert "written" in content
    assert "## Specialist Note" in content


def test_docs_sync_report_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "docs-sync-report",
        "--output",
        "docs/plans/docs-sync-report-demo.md",
        "--title",
        "Task 1 docs sync report",
        "--implementation-report",
        "docs/plans/implementation-report-demo.md",
        "--qa-report",
        "docs/plans/qa-report-demo.md",
        "--docs-updated",
        "ops/templates/qa-report.md and canonical docs alignment notes",
        "--canonical-writeback",
        "docs/status/EXECUTION_BOARD.md",
        "--follow-ups",
        "None for task 1",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "docs-sync-report-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Docs Sync Report: Task 1 docs sync report" in content
    assert "## Consumed Implementation Report" in content
    assert "docs/plans/implementation-report-demo.md" in content
    assert "## Consumed QA Report" in content
    assert "docs/plans/qa-report-demo.md" in content
    assert "## Docs Updated" in content
    assert "## Canonical Writeback" in content
    assert "## Follow-Ups" in content


def test_release_prep_report_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "release-prep-report",
        "--output",
        "docs/plans/release-prep-report-demo.md",
        "--title",
        "Task 1 release prep",
        "--implementation-report",
        "docs/plans/implementation-report-demo.md",
        "--qa-report",
        "docs/plans/qa-report-demo.md",
        "--docs-sync-report",
        "docs/plans/docs-sync-report-demo.md",
        "--verification-plan",
        "uv run pytest -q",
        "--verification-plan",
        "uv run python scripts/check_repo.py",
        "--coverage-plan",
        "Confirm targeted regression coverage matches the bounded release slice.",
        "--version-changelog-plan",
        "No version bump or changelog entry is needed until the tranche is merged.",
        "--merge-pr-plan",
        "Prepare a focused PR summary with reviewer assignment before merge.",
        "--readiness-checklist",
        "tests green",
        "--readiness-checklist",
        "docs synced",
        "--follow-up",
        "Release notes review still pending",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "release-prep-report-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Release Prep Report: Task 1 release prep" in content
    assert "## Consumed Implementation Report" in content
    assert "docs/plans/implementation-report-demo.md" in content
    assert "## Consumed QA Report" in content
    assert "docs/plans/qa-report-demo.md" in content
    assert "## Consumed Docs Sync Report" in content
    assert "docs/plans/docs-sync-report-demo.md" in content
    assert "## Verification Plan" in content
    assert "uv run pytest -q" in content
    assert "## Coverage Plan" in content
    assert "## Version/Changelog Plan" in content
    assert "## Merge/PR Plan" in content
    assert "## Readiness Checklist" in content
    assert "tests green" in content
    assert "## Follow-Ups" in content
    assert "Release notes review still pending" in content


def test_release_gate_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "release-gate",
        "--output",
        "docs/plans/release-gate-demo.md",
        "--title",
        "Task 1 release gate",
        "--release-prep-report",
        "docs/plans/release-prep-report-demo.md",
        "--implementation-report",
        "docs/plans/implementation-report-demo.md",
        "--qa-report",
        "docs/plans/qa-report-demo.md",
        "--docs-sync-report",
        "docs/plans/docs-sync-report-demo.md",
        "--verification-status",
        "uv run pytest -q: passed",
        "--verification-status",
        "uv run python scripts/check_repo.py: passed",
        "--coverage-posture",
        "Targeted regression coverage exists for the release gate writer and ops handoff; no standalone coverage automation was added in this tranche.",
        "--version-changelog-readiness",
        "pyproject version remains unchanged and CHANGELOG.md needs no entry until the bounded slice is merged.",
        "--merge-pr-prep",
        "Diff is scoped to the release-gate contract, tests, and mirrored runtime assets; PR body still needs final reviewer assignment.",
        "--readiness-checklist",
        "tests green",
        "--readiness-checklist",
        "docs synced",
        "--blocking-risk",
        "release notes still need review",
        "--mitigation",
        "review release notes before merge",
        "--verdict",
        "no-go",
        "--recommendation",
        "Hold release until the release notes review is complete",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "release-gate-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Release Gate: Task 1 release gate" in content
    assert "## Consumed Release Prep Report" in content
    assert "docs/plans/release-prep-report-demo.md" in content
    assert "## Consumed Implementation Report" in content
    assert "docs/plans/implementation-report-demo.md" in content
    assert "## Consumed QA Report" in content
    assert "docs/plans/qa-report-demo.md" in content
    assert "## Consumed Docs Sync Report" in content
    assert "docs/plans/docs-sync-report-demo.md" in content
    assert "## Verification Status" in content
    assert "uv run pytest -q: passed" in content
    assert "## Coverage Posture" in content
    assert "## Version/Changelog Readiness" in content
    assert "## Merge/PR Prep" in content
    assert "## Readiness Checklist" in content
    assert "tests green" in content
    assert "## Blocking Risks" in content
    assert "release notes still need review" in content
    assert "## Mitigations" in content
    assert "## Verdict" in content
    assert "## Recommendation" in content


def test_review_gate_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "review-gate",
        "--output",
        "docs/plans/review-gate-demo.md",
        "--title",
        "Phase 5 review gate",
        "--input-summary",
        "Plan brief and architecture context were reviewed",
        "--review-pass",
        "Product: scope holds after discovery",
        "--review-pass",
        "Architecture: module boundaries are acceptable",
        "--auto-decision",
        "Keep the current module split",
        "--taste-decision",
        "Decide whether to run design review before build",
        "--recommendation",
        "Proceed after user resolves the remaining taste decision",
        "--approval-target",
        "user",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "review-gate-demo.md"
    assert out.exists()
    content = out.read_text()
    assert "# Review Gate: Phase 5 review gate" in content
    assert "## Inputs" in content
    assert "## Review Passes" in content
    assert "## Auto Decisions" in content
    assert "## Taste Decisions" in content
    assert "## Recommendation" in content
    assert "## Approval Target" in content


def test_autoplan_report_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "autoplan-report",
        "--output",
        "docs/plans/autoplan/report.md",
        "--title",
        "Phase 22 autoplan",
        "--mode",
        "run",
        "--outcome",
        "auto-clear",
        "--plan-brief",
        "docs/plans/phase22-plan.md",
        "--review-pass",
        "docs/plans/autoplan/review-passes/product.md",
        "--review-pass",
        "docs/plans/autoplan/review-passes/architect.md",
        "--review-gate",
        "docs/plans/autoplan/review-gate.md",
        "--next-step",
        "Proceed to bounded builder kickoff",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "autoplan" / "report.md"
    assert out.exists()
    content = out.read_text()
    assert "# Autoplan Report: Phase 22 autoplan" in content
    assert "## Mode" in content
    assert "## Outcome" in content
    assert "auto-clear" in content
    assert "## Plan Brief" in content
    assert "docs/plans/phase22-plan.md" in content
    assert "## Review Passes" in content
    assert "docs/plans/autoplan/review-passes/product.md" in content
    assert "## Review Gate" in content
    assert "docs/plans/autoplan/review-gate.md" in content
    assert "## Next Step" in content
    assert "Proceed to bounded builder kickoff" in content


def test_review_pass_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "review-pass",
        "--output",
        "docs/plans/review-pass-product.md",
        "--title",
        "Product pass",
        "--role",
        "Product",
        "--focus",
        "Scope clarity and milestone fit",
        "--finding",
        "Current scope is coherent",
        "--auto-decision",
        "Keep the milestone boundary",
        "--taste-decision",
        "Decide whether to expand discovery to design references",
        "--recommendation",
        "Proceed if the design reference question is resolved",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "review-pass-product.md"
    assert out.exists()
    content = out.read_text()
    assert "# Review Pass: Product pass" in content
    assert "## Role" in content
    assert "## Focus" in content
    assert "## Findings" in content
    assert "## Auto Decisions" in content
    assert "## Taste Decisions" in content
    assert "## Recommendation" in content


def test_review_packet_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "review-packet",
        "--output",
        "docs/plans/review-packets/product.md",
        "--title",
        "Product packet",
        "--role",
        "Product",
        "--logical-role",
        "product-reviewer",
        "--bridge-agent-type",
        "explorer",
        "--bridge-model",
        "gpt-5.4",
        "--bridge-reasoning-effort",
        "medium",
        "--role-skill",
        ".agents/skills/product-discovery/SKILL.md",
        "--role-metadata",
        ".agents/skills/product-discovery/agents/openai.yaml",
        "--role-writeback-target",
        "docs/plans/review-passes/product.md",
        "--role-writeback-command",
        "uv run python scripts/team_state.py review-pass --output docs/plans/review-passes/product.md --role Product ...",
        "--objective",
        "Assess milestone fit and scope pressure",
        "--canonical-source",
        "docs/project/PROJECT_BRIEF.md",
        "--canonical-source",
        "docs/project/ROADMAP.md",
        "--plan-brief",
        "docs/plans/phase8-plan-brief.md",
        "--expected-output",
        "Return a review-pass with Role, Focus, Findings, Auto Decisions, Taste Decisions, Recommendation",
        "--writeback",
        "docs/plans/review-passes/product.md",
        "--writeback-command",
        "uv run python scripts/team_state.py review-pass --output docs/plans/review-passes/product.md --title '<title>' --role Product --focus '<focus>' --finding '<finding>' --auto-decision '<auto_decision>' --recommendation '<recommendation>'",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "review-packets" / "product.md"
    assert out.exists()
    content = out.read_text()
    assert "# Review Packet: Product packet" in content
    assert "## Role" in content
    assert "## Logical Role" in content
    assert "product-reviewer" in content
    assert "## Invocation Bridge" in content
    assert "- agent_type: explorer" in content
    assert "- model: gpt-5.4" in content
    assert "- reasoning_effort: medium" in content
    assert "## Runtime Role Binding" in content
    assert ".agents/skills/product-discovery/SKILL.md" in content
    assert ".agents/skills/product-discovery/agents/openai.yaml" in content
    assert "canonical_writeback_target: docs/plans/review-passes/product.md" in content
    assert "scripts/team_state.py review-pass" in content
    assert "## Objective" in content
    assert "## Canonical Sources" in content
    assert "- docs/project/PROJECT_BRIEF.md" in content
    assert "- docs/project/ROADMAP.md" in content
    assert "## Plan Brief" in content
    assert "docs/plans/phase8-plan-brief.md" in content
    assert "## Expected Output" in content
    assert "## Writeback Target" in content
    assert "## Writeback Command" in content
    assert "docs/plans/review-passes/product.md" in content
    assert "scripts/team_state.py review-pass" in content


def test_review_result_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "review-result",
        "--output",
        "docs/plans/review-results/product.md",
        "--title",
        "Product result",
        "--role",
        "Product",
        "--focus",
        "Milestone fit and scope coherence",
        "--finding",
        "Scope is coherent for this tranche",
        "--auto-decision",
        "Keep current milestone focus",
        "--taste-decision",
        "Decide whether to widen discovery in this sprint",
        "--recommendation",
        "Proceed after milestone sync",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "review-results" / "product.md"
    assert out.exists()
    content = out.read_text()
    assert "# Review Result: Product result" in content
    assert "## Role" in content
    assert "## Focus" in content
    assert "## Findings" in content
    assert "## Auto Decisions" in content
    assert "## Taste Decisions" in content
    assert "## Recommendation" in content


def test_onboarding_state_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "onboarding-state",
        "--output",
        "docs/status/onboarding-state.md",
        "--title",
        "Initial contact",
        "--stage",
        "shallow-scan",
        "--last-scan",
        "directory review",
        "--pending",
        "Decide entry module",
        "--notes",
        "Initial review complete",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "status" / "onboarding-state.md"
    content = out.read_text()
    assert "# Onboarding State: Initial contact" in content
    assert "## Stage" in content
    assert "shallow-scan" in content
    assert "Decide entry module" in content
    assert "Initial review complete" in content


def test_onboarding_report_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "onboarding-report",
        "--output",
        "docs/plans/onboarding-report.md",
        "--title",
        "Initial survey",
        "--summary",
        "Project is in early stage",
        "--findings",
        "Tests missing",
        "--recommendations",
        "Add smoke tests",
        "--next-steps",
        "Schedule design review",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "onboarding-report.md"
    content = out.read_text()
    assert "# Onboarding Report: Initial survey" in content
    assert "Project is in early stage" in content
    assert "- Tests missing" in content
    assert "- Add smoke tests" in content
    assert "- Schedule design review" in content


def test_deep_scan_plan_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "deep-scan-plan",
        "--output",
        "docs/plans/deep-scan-plan.md",
        "--title",
        "Runtime validation",
        "--goals",
        "Validate startup",
        "--hypotheses",
        "Install fails without env",
        "--probes",
        "install",
        "--probes",
        "run",
        "--evidence",
        "build exit 0",
        "--risk-level",
        "medium",
        "--writeback-targets",
        "docs/project/PROJECT_BRIEF.md",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "deep-scan-plan.md"
    content = out.read_text()
    assert "# Deep Scan Plan: Runtime validation" in content
    assert "Validate startup" in content
    assert "- install" in content
    assert "- run" in content
    assert "- build exit 0" in content
    assert "medium" in content
    assert "docs/project/PROJECT_BRIEF.md" in content


def test_decision_command_writes_markdown(tmp_path: Path) -> None:
    result = run_team_state(
        tmp_path,
        "decision",
        "--output",
        "docs/decisions/2026-03-24-cli.md",
        "--title",
        "Use state script",
        "--context",
        "Manual state edits are drifting",
        "--decision",
        "Adopt scripts/team_state.py",
        "--consequence",
        "Consistent artifacts",
        "--consequence",
        "Lower coordination overhead",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "decisions" / "2026-03-24-cli.md"
    assert out.exists()
    content = out.read_text()
    assert "# Decision: Use state script" in content
    assert "## Context" in content
    assert "## Decision" in content
    assert "## Consequences" in content
    assert "- Consistent artifacts" in content
    assert "- Lower coordination overhead" in content


def test_board_command_updates_execution_board(tmp_path: Path) -> None:
    board_path = tmp_path / "docs" / "status" / "EXECUTION_BOARD.md"
    board_path.parent.mkdir(parents=True, exist_ok=True)
    board_path.write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nplan\n\n"
        "## Active Work\n\n- old task\n\n"
        "## Completed\n\n- done thing\n"
    )

    result = run_team_state(
        tmp_path,
        "board",
        "--path",
        "docs/status/EXECUTION_BOARD.md",
        "--stage",
        "build",
        "--active",
        "Implement team_state.py",
        "--active",
        "Add orchestration tests",
        "--completed",
        "Codify role contracts",
    )
    assert result.returncode == 0, result.stderr

    content = board_path.read_text()
    assert "_This file can be updated manually or via `scripts/team_state.py board`._" in content
    assert "## Current Stage\n\nbuild" in content
    assert "- Implement team_state.py" in content
    assert "- Add orchestration tests" in content
    assert "- Codify role contracts" in content


def test_board_command_preserves_existing_sections_when_not_overridden(tmp_path: Path) -> None:
    board_path = tmp_path / "docs" / "status" / "EXECUTION_BOARD.md"
    board_path.parent.mkdir(parents=True, exist_ok=True)
    board_path.write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nreview\n\n"
        "## Active Work\n\n- keep me\n\n"
        "## Completed\n\n- keep done\n"
    )

    result = run_team_state(
        tmp_path,
        "board",
        "--path",
        "docs/status/EXECUTION_BOARD.md",
        "--stage",
        "qa",
    )
    assert result.returncode == 0, result.stderr

    content = board_path.read_text()
    assert "## Current Stage\n\nqa" in content
    assert "## Active Work\n\n- keep me" in content
    assert "## Completed\n\n- keep done" in content
    assert "- - keep me" not in content
    assert "- - keep done" not in content


def test_board_command_normalizes_historically_double_prefixed_items(tmp_path: Path) -> None:
    board_path = tmp_path / "docs" / "status" / "EXECUTION_BOARD.md"
    board_path.parent.mkdir(parents=True, exist_ok=True)
    board_path.write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nreview\n\n"
        "## Active Work\n\n- - duplicated task\n\n"
        "## Completed\n\n- - duplicated done\n"
    )

    result = run_team_state(
        tmp_path,
        "board",
        "--path",
        "docs/status/EXECUTION_BOARD.md",
        "--stage",
        "qa",
    )
    assert result.returncode == 0, result.stderr

    content = board_path.read_text()
    assert "## Current Stage\n\nqa" in content
    assert "## Active Work\n\n- duplicated task" in content
    assert "## Completed\n\n- duplicated done" in content
    assert "- - duplicated task" not in content
    assert "- - duplicated done" not in content
