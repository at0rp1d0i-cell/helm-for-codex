import subprocess
import sys
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops_loop.py"


def run_ops_loop(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def seed_repo_state(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "status").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "project" / "PROJECT_BRIEF.md").write_text(
        "# Project Brief\n\n## Current Goal\n\nDrive ops orchestration.\n"
    )
    (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nplan\n\n"
        "## Active Work\n\n- define next task\n\n"
        "## Completed\n\n- bootstrap\n"
    )


def write_implementation_report(tmp_path: Path) -> None:
    (tmp_path / "docs" / "plans" / "implementation-report-ops.md").write_text(
        "# Implementation Report: Ops task\n\n"
        "## Consumed Sprint Contract\n\n"
        "docs/plans/sprint-contract-ops.md\n\n"
        "## Generator Summary\n\nBuilder completed the bounded task.\n"
    )


def write_qa_report(tmp_path: Path) -> None:
    (tmp_path / "docs" / "plans" / "qa-report-ops.md").write_text(
        "# QA Report\n\n"
        "## Consumed Sprint Contract\n\n"
        "docs/plans/sprint-contract-ops.md\n\n"
        "## Consumed Implementation Report\n\n"
        "docs/plans/implementation-report-ops.md\n\n"
        "## Verification Status\n\n"
        "passed\n"
    )


def test_ops_loop_runs_build_qa_and_docs_sync_happy_path(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    build = run_ops_loop(
        tmp_path,
        "build",
        "--title",
        "Ops task",
        "--planner",
        "Lead approved a bounded task.",
        "--generator",
        "Builder implements the approved task.",
        "--evaluator",
        "QA and docs-sync evaluate the handoff chain.",
        "--scope",
        "Exercise the ops runtime only.",
        "--acceptance",
        "Sprint contract exists before builder work.",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-ops.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-ops.md",
    )
    assert build.returncode == 0, build.stderr
    builder_packet = (tmp_path / "docs" / "plans" / "builder-dispatch-ops.md").read_text()
    assert "# Dispatch Packet: Ops task builder dispatch" in builder_packet
    assert "docs/plans/sprint-contract-ops.md" in builder_packet
    builder_invocation = (tmp_path / "docs" / "plans" / "builder-dispatch-ops-invocation.md").read_text()
    assert "# Invocation Spec: Ops task builder dispatch invocation" in builder_invocation
    assert "implementation-worker" in builder_invocation
    assert "docs/plans/builder-dispatch-ops.md" in builder_invocation

    write_implementation_report(tmp_path)

    qa_prepare = run_ops_loop(
        tmp_path,
        "qa-prepare",
        "--title",
        "Ops task",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-ops.md",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops.md",
        "--qa-packet-path",
        "docs/plans/qa-dispatch-ops.md",
        "--qa-report-path",
        "docs/plans/qa-report-ops.md",
        "--environment",
        "ops loop test repo",
        "--scenario",
        "Run the ops runtime QA handoff",
    )
    assert qa_prepare.returncode == 0, qa_prepare.stderr
    qa_packet = (tmp_path / "docs" / "plans" / "qa-dispatch-ops.md").read_text()
    assert "# Dispatch Packet: Ops task QA dispatch" in qa_packet
    assert "docs/plans/implementation-report-ops.md" in qa_packet
    assert "browser_evidence_manifest: docs/plans/qa-evidence-ops.md" in qa_packet
    assert "artifact_root: docs/plans/qa-artifacts/ops" in qa_packet
    assert "docs/plans/qa-artifacts/ops/screenshots/scenario-01.png" in qa_packet
    qa_invocation = (tmp_path / "docs" / "plans" / "qa-dispatch-ops-invocation.md").read_text()
    assert "qa-runner" in qa_invocation
    assert "docs/plans/qa-dispatch-ops.md" in qa_invocation

    qa = run_ops_loop(
        tmp_path,
        "qa",
        "--title",
        "Ops task",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-ops.md",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops.md",
        "--qa-packet-path",
        "docs/plans/qa-dispatch-ops.md",
        "--qa-report-path",
        "docs/plans/qa-report-ops.md",
        "--environment",
        "ops loop test repo",
        "--scenario",
        "Run the ops runtime QA handoff",
        "--verification-status",
        "passed",
    )
    assert qa.returncode == 0, qa.stderr
    qa_report = (tmp_path / "docs" / "plans" / "qa-report-ops.md").read_text()
    assert "## Browser Evidence Status" in qa_report
    assert "## Browser Evidence Mode" in qa_report
    assert "## Browser Evidence Manifest" in qa_report
    assert "docs/plans/qa-evidence-ops.md" in qa_report
    assert "## Browser Evidence Artifact Root" in qa_report
    assert "docs/plans/qa-artifacts/ops" in qa_report
    assert "## Consumed QA Dispatch Packet" in qa_report
    assert "docs/plans/qa-dispatch-ops.md" in qa_report
    qa_evidence = (tmp_path / "docs" / "plans" / "qa-evidence-ops.md").read_text()
    assert "# QA Evidence Manifest: Ops task" in qa_evidence
    assert "docs/plans/qa-report-ops.md" in qa_evidence
    assert "## Artifact Root" in qa_evidence
    assert "docs/plans/qa-artifacts/ops" in qa_evidence
    assert "## Screenshot Targets" in qa_evidence
    assert "docs/plans/qa-artifacts/ops/screenshots/scenario-01.png" in qa_evidence
    assert "## DOM Snapshot Targets" in qa_evidence
    assert "docs/plans/qa-artifacts/ops/dom/scenario-01.md" in qa_evidence
    assert "## Console Log Targets" in qa_evidence
    assert "docs/plans/qa-artifacts/ops/console/scenario-01.log" in qa_evidence

    docs_prepare = run_ops_loop(
        tmp_path,
        "docs-sync-prepare",
        "--title",
        "Ops task",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops.md",
        "--qa-report-path",
        "docs/plans/qa-report-ops.md",
        "--docs-sync-packet-path",
        "docs/plans/docs-sync-dispatch-ops.md",
        "--docs-sync-report-path",
        "docs/plans/docs-sync-report-ops.md",
        "--docs-updated",
        "docs/status/EXECUTION_BOARD.md",
        "--canonical-writeback",
        "docs/project/PROJECT_BRIEF.md",
    )
    assert docs_prepare.returncode == 0, docs_prepare.stderr
    docs_packet = (tmp_path / "docs" / "plans" / "docs-sync-dispatch-ops.md").read_text()
    assert "# Dispatch Packet: Ops task docs-sync dispatch" in docs_packet
    assert "docs/plans/qa-report-ops.md" in docs_packet
    docs_invocation = (tmp_path / "docs" / "plans" / "docs-sync-dispatch-ops-invocation.md").read_text()
    assert "docs-sync" in docs_invocation
    assert "docs/plans/docs-sync-dispatch-ops.md" in docs_invocation

    docs_sync = run_ops_loop(
        tmp_path,
        "docs-sync",
        "--title",
        "Ops task",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops.md",
        "--qa-report-path",
        "docs/plans/qa-report-ops.md",
        "--docs-sync-report-path",
        "docs/plans/docs-sync-report-ops.md",
        "--docs-updated",
        "docs/status/EXECUTION_BOARD.md",
        "--canonical-writeback",
        "docs/project/PROJECT_BRIEF.md",
    )
    assert docs_sync.returncode == 0, docs_sync.stderr

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nship-ready" in board
    assert "- Ops task" in board


def test_ops_loop_sprint_negotiate_materializes_build_when_ready(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_ops_loop(
        tmp_path,
        "sprint-negotiate",
        "--title",
        "Negotiated ops task",
        "--planner",
        "Lead proposes one bounded delivery slice.",
        "--generator",
        "Builder implements the bounded lane.",
        "--evaluator",
        "QA validates the bounded lane.",
        "--scope",
        "Implement one bounded sprint negotiation lane only.",
        "--acceptance",
        "Targeted tests verify the lane and implementation report handoff.",
        "--evidence-posture",
        "Targeted regression evidence and QA report are required.",
        "--implementation-report-path",
        "docs/plans/implementation-report-negotiated.md",
        "--sprint-proposal-path",
        "docs/plans/sprint-proposal-negotiated.md",
        "--builder-sprint-pass-path",
        "docs/plans/sprint-passes/builder.md",
        "--qa-sprint-pass-path",
        "docs/plans/sprint-passes/qa.md",
        "--sprint-gate-path",
        "docs/plans/sprint-gate-negotiated.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-negotiated.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-negotiated.md",
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "docs" / "plans" / "sprint-proposal-negotiated.md").exists()
    assert (tmp_path / "docs" / "plans" / "sprint-passes" / "builder.md").exists()
    assert (tmp_path / "docs" / "plans" / "sprint-passes" / "qa.md").exists()
    gate = (tmp_path / "docs" / "plans" / "sprint-gate-negotiated.md").read_text()
    assert "# Sprint Gate: Negotiated ops task" in gate
    assert "## Outcome\n\nready-for-build" in gate
    assert (tmp_path / "docs" / "plans" / "sprint-contract-negotiated.md").exists()
    assert (tmp_path / "docs" / "plans" / "builder-dispatch-negotiated.md").exists()
    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nbuild" in board
    assert "- Negotiated ops task" in board


def test_ops_loop_sprint_negotiate_reframes_scope_when_blocked(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_ops_loop(
        tmp_path,
        "sprint-negotiate",
        "--title",
        "Broad ops task",
        "--planner",
        "Lead proposes a task.",
        "--generator",
        "Builder implements the task.",
        "--evaluator",
        "QA validates the task.",
        "--scope",
        "Build a full platform for every workflow.",
        "--acceptance",
        "Targeted tests verify the lane and implementation report handoff.",
        "--evidence-posture",
        "Targeted regression evidence and QA report are required.",
        "--implementation-report-path",
        "docs/plans/implementation-report-broad.md",
        "--sprint-proposal-path",
        "docs/plans/sprint-proposal-broad.md",
        "--builder-sprint-pass-path",
        "docs/plans/sprint-passes/builder-broad.md",
        "--qa-sprint-pass-path",
        "docs/plans/sprint-passes/qa-broad.md",
        "--sprint-gate-path",
        "docs/plans/sprint-gate-broad.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-broad.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-broad.md",
    )

    assert result.returncode == 0, result.stderr
    gate = (tmp_path / "docs" / "plans" / "sprint-gate-broad.md").read_text()
    assert "## Outcome\n\nreframe-scope" in gate
    assert not (tmp_path / "docs" / "plans" / "sprint-contract-broad.md").exists()
    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nplan" in board
    assert "- Broad ops task" in board


def test_ops_loop_sprint_negotiate_asks_user_for_strategic_tradeoff(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_ops_loop(
        tmp_path,
        "sprint-negotiate",
        "--title",
        "Strategic ops task",
        "--planner",
        "Lead proposes a task.",
        "--generator",
        "Builder implements the task.",
        "--evaluator",
        "QA validates the task.",
        "--scope",
        "Implement one bounded release lane.",
        "--acceptance",
        "Targeted tests verify the lane and implementation report handoff.",
        "--evidence-posture",
        "Budget and compliance approval are required before evaluator signoff.",
        "--implementation-report-path",
        "docs/plans/implementation-report-strategic.md",
        "--sprint-proposal-path",
        "docs/plans/sprint-proposal-strategic.md",
        "--builder-sprint-pass-path",
        "docs/plans/sprint-passes/builder-strategic.md",
        "--qa-sprint-pass-path",
        "docs/plans/sprint-passes/qa-strategic.md",
        "--sprint-gate-path",
        "docs/plans/sprint-gate-strategic.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-strategic.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-strategic.md",
    )

    assert result.returncode == 0, result.stderr
    gate = (tmp_path / "docs" / "plans" / "sprint-gate-strategic.md").read_text()
    assert "## Outcome\n\nask-user" in gate
    assert not (tmp_path / "docs" / "plans" / "sprint-contract-strategic.md").exists()
    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\napproval-needed" in board


def test_ops_loop_release_prepare_and_release_gate(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)
    (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nship-ready\n\n"
        "## Active Work\n\n- release candidate\n\n"
        "## Completed\n\n- docs sync\n"
    )
    (tmp_path / "docs" / "plans" / "implementation-report-release.md").write_text(
        "# Implementation Report: Release task\n\n"
        "## Consumed Sprint Contract\n\n"
        "docs/plans/sprint-contract-release.md\n\n"
        "## Generator Summary\n\nReady for release.\n"
    )
    (tmp_path / "docs" / "plans" / "qa-report-release.md").write_text(
        "# QA Report\n\n"
        "## Consumed Sprint Contract\n\n"
        "docs/plans/sprint-contract-release.md\n\n"
        "## Consumed Implementation Report\n\n"
        "docs/plans/implementation-report-release.md\n\n"
        "## Verification Status\n\n"
        "passed\n"
    )
    (tmp_path / "docs" / "plans" / "docs-sync-report-release.md").write_text(
        "# Docs Sync Report: Release task\n\n"
        "## Consumed Implementation Report\n\n"
        "docs/plans/implementation-report-release.md\n\n"
        "## Consumed QA Report\n\n"
        "docs/plans/qa-report-release.md\n\n"
        "## Docs Updated\n\n"
        "- docs/status/EXECUTION_BOARD.md\n\n"
        "## Canonical Writeback\n\n"
        "- docs/project/PROJECT_BRIEF.md\n\n"
        "## Follow-Ups\n\n"
        "- none\n"
    )

    prepare = run_ops_loop(
        tmp_path,
        "release-prepare",
        "--title",
        "Release task",
        "--implementation-report-path",
        "docs/plans/implementation-report-release.md",
        "--qa-report-path",
        "docs/plans/qa-report-release.md",
        "--docs-sync-report-path",
        "docs/plans/docs-sync-report-release.md",
        "--release-prep-report-path",
        "docs/plans/release-prep-report-release.md",
        "--release-packet-path",
        "docs/plans/release-dispatch-release.md",
        "--release-gate-path",
        "docs/plans/release-gate-release.md",
        "--verification-plan",
        "uv run pytest -q",
        "--verification-plan",
        "uv run python scripts/check_repo.py",
        "--coverage-plan",
        "Targeted regression coverage exists for the release gate writer and ops handoff; no standalone coverage automation was added in this tranche.",
        "--version-changelog-plan",
        "pyproject version remains unchanged and CHANGELOG.md needs no entry until the bounded slice is merged.",
        "--merge-pr-plan",
        "Diff is scoped to the release-gate contract, tests, and mirrored runtime assets; PR body still needs final reviewer assignment.",
        "--readiness-checklist",
        "tests green",
        "--readiness-checklist",
        "docs synced",
        "--follow-up",
        "release notes review pending",
    )
    assert prepare.returncode == 0, prepare.stderr
    prep_report = (tmp_path / "docs" / "plans" / "release-prep-report-release.md").read_text()
    assert "# Release Prep Report: Release task" in prep_report
    assert "uv run pytest -q" in prep_report
    assert "release notes review pending" in prep_report
    packet = (tmp_path / "docs" / "plans" / "release-dispatch-release.md").read_text()
    assert "# Dispatch Packet: Release task release dispatch" in packet
    assert "release-manager" in packet
    assert "docs/plans/release-prep-report-release.md" in packet
    assert "Evidence-first release gate sections:" in packet
    assert "- verification status" in packet
    assert "- merge/PR prep" in packet
    invocation = (tmp_path / "docs" / "plans" / "release-dispatch-release-invocation.md").read_text()
    assert ".agents/skills/release-manager/SKILL.md" in invocation

    gate = run_ops_loop(
        tmp_path,
        "release-gate",
        "--title",
        "Release task",
        "--release-prep-report-path",
        "docs/plans/release-prep-report-release.md",
        "--release-gate-path",
        "docs/plans/release-gate-release.md",
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
        "--blocking-risk",
        "release notes review pending",
        "--mitigation",
        "review release notes before merge",
        "--verdict",
        "no-go",
        "--recommendation",
        "Hold release until release notes review is complete",
    )
    assert gate.returncode == 0, gate.stderr
    report = (tmp_path / "docs" / "plans" / "release-gate-release.md").read_text()
    assert "## Consumed Release Prep Report" in report
    assert "docs/plans/release-prep-report-release.md" in report
    assert "## Consumed Docs Sync Report" in report
    assert "## Verification Status" in report
    assert "uv run pytest -q: passed" in report
    assert "## Coverage Posture" in report
    assert "## Version/Changelog Readiness" in report
    assert "## Merge/PR Prep" in report
    assert "## Readiness Checklist" in report
    assert "tests green" in report
    assert "release notes review pending" in report
    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nship-ready" in board


def test_ops_loop_dispatch_packets_include_logical_role_bridge(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    build = run_ops_loop(
        tmp_path,
        "build",
        "--title",
        "Ops bridge task",
        "--planner",
        "Lead approved a bounded task.",
        "--generator",
        "Builder implements the approved task.",
        "--evaluator",
        "QA and docs-sync evaluate the handoff chain.",
        "--scope",
        "Exercise bridge-aware dispatch packets only.",
        "--acceptance",
        "Builder packet must name the logical role and bridge resolution.",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops-bridge.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-ops-bridge.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-ops-bridge.md",
    )
    assert build.returncode == 0, build.stderr

    builder_packet = (tmp_path / "docs" / "plans" / "builder-dispatch-ops-bridge.md").read_text()
    assert "## Logical Role" in builder_packet
    assert "implementation-worker" in builder_packet
    assert "## Invocation Bridge" in builder_packet
    assert "- agent_type: worker" in builder_packet
    assert "- model: gpt-5.4" in builder_packet
    builder_invocation = (tmp_path / "docs" / "plans" / "builder-dispatch-ops-bridge-invocation.md").read_text()
    assert "## Runtime Skill" in builder_invocation
    assert ".agents/skills/implementation-worker/SKILL.md" in builder_invocation
    assert "## Expected Writeback Target" in builder_invocation
    assert "docs/plans/implementation-report-ops-bridge.md" in builder_invocation
    assert "## Runtime Role Binding" in builder_packet
    assert ".agents/skills/implementation-worker/SKILL.md" in builder_packet
    assert ".agents/skills/implementation-worker/agents/openai.yaml" in builder_packet
    assert "scripts/team_state.py implementation-report" in builder_packet


def test_ops_loop_exists_for_repo_runtime() -> None:
    assert SCRIPT.exists()


def test_ops_loop_bridge_launch_renders_launch_payload(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    build = run_ops_loop(
        tmp_path,
        "build",
        "--title",
        "Ops bridge launch task",
        "--planner",
        "Lead approved a bounded task.",
        "--generator",
        "Builder implements the approved task.",
        "--evaluator",
        "QA and docs-sync evaluate the handoff chain.",
        "--scope",
        "Exercise the bridge launch runtime.",
        "--acceptance",
        "Ops can compile a reusable last-hop payload.",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops-launch.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-ops-launch.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-ops-launch.md",
    )
    assert build.returncode == 0, build.stderr

    launch = run_ops_loop(
        tmp_path,
        "bridge-launch",
        "--packet-path",
        "docs/plans/builder-dispatch-ops-launch.md",
    )
    assert launch.returncode == 0, launch.stderr
    payload = json.loads(launch.stdout)
    assert payload["logical_role"] == "implementation-worker"
    assert payload["agent_type"] == "worker"
    assert "builder-dispatch-ops-launch.md" in payload["launch_message"]


def test_ops_loop_bridge_receipt_writes_execution_receipt(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)
    build = run_ops_loop(
        tmp_path,
        "build",
        "--title",
        "Ops receipt task",
        "--planner",
        "Lead approved a bounded task.",
        "--generator",
        "Builder implements the approved task.",
        "--evaluator",
        "QA and docs-sync evaluate the handoff chain.",
        "--scope",
        "Exercise bridge receipt runtime.",
        "--acceptance",
        "Ops can record a specialist execution receipt.",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops-receipt.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-ops-receipt.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-ops-receipt.md",
    )
    assert build.returncode == 0, build.stderr
    launch = run_ops_loop(
        tmp_path,
        "bridge-launch",
        "--packet-path",
        "docs/plans/builder-dispatch-ops-receipt.md",
        "--output",
        "docs/plans/bridge-launches/builder.json",
    )
    assert launch.returncode == 0, launch.stderr

    receipt = run_ops_loop(
        tmp_path,
        "bridge-receipt",
        "--packet-path",
        "docs/plans/builder-dispatch-ops-receipt.md",
        "--launch-payload-path",
        "docs/plans/bridge-launches/builder.json",
        "--execution-status",
        "succeeded",
        "--writeback-status",
        "written",
        "--specialist-note",
        "Implementation report written successfully.",
    )
    assert receipt.returncode == 0, receipt.stderr
    out = (tmp_path / "docs" / "plans" / "builder-dispatch-ops-receipt-receipt.md").read_text()
    assert "Execution Receipt" in out
    assert "written" in out
