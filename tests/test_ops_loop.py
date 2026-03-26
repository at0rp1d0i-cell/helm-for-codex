import subprocess
import sys
from pathlib import Path


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

    qa = run_ops_loop(
        tmp_path,
        "qa",
        "--title",
        "Ops task",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-ops.md",
        "--implementation-report-path",
        "docs/plans/implementation-report-ops.md",
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


def test_ops_loop_exists_for_repo_runtime() -> None:
    assert SCRIPT.exists()
