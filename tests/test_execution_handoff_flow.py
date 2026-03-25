import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lead_loop.py"


def run_lead_loop(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
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
        "# Project Brief\n\n## Current Goal\n\nDrive runtime orchestration.\n"
    )
    (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nreview\n\n"
        "## Active Work\n\n- Phase 13 task 3\n\n"
        "## Completed\n\n- bootstrap\n"
    )


def write_implementation_report(tmp_path: Path) -> None:
    (tmp_path / "docs" / "plans" / "implementation-report-phase13-task3.md").write_text(
        "# Implementation Report: Phase 13 task 3\n\n"
        "## Consumed Sprint Contract\n\n"
        "docs/plans/sprint-contract-phase13-task3.md\n\n"
        "## Generator Summary\n\nBuilder completed the bounded task.\n\n"
        "## Files Touched\n\nscripts/lead_loop.py\n\n"
        "## Tests Run\n\nuv run pytest tests/test_lead_loop.py -q\n\n"
        "## Follow-Ups\n\nnone\n"
    )


def test_build_then_qa_passes_with_canonical_artifacts(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    build = run_lead_loop(
        tmp_path,
        "build",
        "--title",
        "Phase 13 task 3",
        "--planner",
        "Lead owns the sprint contract and acceptance for one bounded task.",
        "--generator",
        "Builder implements the approved task and writes the implementation report.",
        "--evaluator",
        "QA evaluates the builder output against the sprint contract and implementation report.",
        "--scope",
        "Add QA handoff and defect loop only.",
        "--acceptance",
        "QA consumes the upstream artifacts and writes the canonical qa-report.",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-phase13-task3.md",
    )

    assert build.returncode == 0, build.stderr
    write_implementation_report(tmp_path)

    qa = run_lead_loop(
        tmp_path,
        "qa",
        "--title",
        "Phase 13 task 3",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-phase13-task3.md",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--qa-report-path",
        "docs/plans/qa-report-phase13-task3.md",
        "--environment",
        "Fresh repo checkout",
        "--scenario",
        "Run builder-to-QA handoff validation",
        "--verification-status",
        "passed",
    )

    assert qa.returncode == 0, qa.stderr
    report = (tmp_path / "docs" / "plans" / "qa-report-phase13-task3.md").read_text()
    assert "docs/plans/sprint-contract-phase13-task3.md" in report
    assert "docs/plans/implementation-report-phase13-task3.md" in report
    assert "Run builder-to-QA handoff validation" in report

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nqa" in board
    assert "- Phase 13 task 3" in board


def test_build_then_qa_failure_loops_back_to_build(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    build = run_lead_loop(
        tmp_path,
        "build",
        "--title",
        "Phase 13 task 3",
        "--planner",
        "Lead owns the sprint contract and acceptance for one bounded task.",
        "--generator",
        "Builder implements the approved task and writes the implementation report.",
        "--evaluator",
        "QA evaluates the builder output against the sprint contract and implementation report.",
        "--scope",
        "Add QA handoff and defect loop only.",
        "--acceptance",
        "QA consumes the upstream artifacts and writes the canonical qa-report.",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-phase13-task3.md",
    )

    assert build.returncode == 0, build.stderr
    write_implementation_report(tmp_path)

    qa = run_lead_loop(
        tmp_path,
        "qa",
        "--title",
        "Phase 13 task 3",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-phase13-task3.md",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--qa-report-path",
        "docs/plans/qa-report-phase13-task3.md",
        "--environment",
        "Fresh repo checkout",
        "--scenario",
        "Run builder-to-QA handoff validation",
        "--issue",
        "QA found a reproducible regression",
        "--verification-status",
        "failed",
    )

    assert qa.returncode == 0, qa.stderr
    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nbuild" in board
    assert "- Phase 13 task 3" in board
