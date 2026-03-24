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
    (tmp_path / "docs" / "decisions").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "project" / "PROJECT_BRIEF.md").write_text(
        "# Project Brief\n\n## Problem\n\nBuild a Codex-native AI team.\n\n## Current Goal\n\nDrive runtime orchestration.\n\n## Success Criteria\n\n- delegate work\n"
    )
    (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nplan\n\n"
        "## Active Work\n\n- define next task\n\n"
        "## Completed\n\n- bootstrap\n"
    )


def test_delegate_creates_task_brief_and_updates_board(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(
        tmp_path,
        "delegate",
        "--title",
        "Implement lead loop",
        "--objective",
        "Create a minimal orchestration CLI",
        "--scope",
        "Only add scripts and tests for lead loop",
        "--constraints",
        "No dependency additions",
        "--decisions",
        "Use repository-backed state updates",
        "--expected-output",
        "A runnable lead loop plus tests",
        "--writeback",
        "docs/status/EXECUTION_BOARD.md",
        "--task-path",
        "docs/plans/lead-loop-task.md",
    )

    assert result.returncode == 0, result.stderr
    task_brief = tmp_path / "docs" / "plans" / "lead-loop-task.md"
    assert task_brief.exists()
    assert "# Task Brief: Implement lead loop" in task_brief.read_text()

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nbuild" in board
    assert "- Implement lead loop" in board


def test_discover_creates_discovery_brief_and_updates_board(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(
        tmp_path,
        "discover",
        "--title",
        "Research upstream gstack",
        "--problem",
        "Need a repository-backed discovery handoff",
        "--research-scope",
        "Read gstack workflow skills and extract reusable patterns",
        "--open-questions",
        "Which upstream conventions should be adapted or rejected?",
        "--recommendation-target",
        "docs/project/PROJECT_BRIEF.md",
        "--discovery-path",
        "docs/plans/discovery-brief.md",
    )

    assert result.returncode == 0, result.stderr
    discovery = tmp_path / "docs" / "plans" / "discovery-brief.md"
    assert discovery.exists()
    assert "# Discovery Brief: Research upstream gstack" in discovery.read_text()

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\ndiscovery" in board
    assert "- Research upstream gstack" in board


def test_plan_creates_plan_brief_and_updates_board(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(
        tmp_path,
        "plan",
        "--title",
        "Phase 4 orchestration slice",
        "--goal",
        "Move from discovery into execution",
        "--milestone",
        "Phase 4",
        "--modules",
        "scripts/team_state.py, scripts/lead_loop.py",
        "--exit-criteria",
        "Discovery and planning are repo-backed",
        "--writeback",
        "docs/status/EXECUTION_BOARD.md",
        "--plan-path",
        "docs/plans/phase4-plan-brief.md",
    )

    assert result.returncode == 0, result.stderr
    plan = tmp_path / "docs" / "plans" / "phase4-plan-brief.md"
    assert plan.exists()
    assert "# Plan Brief: Phase 4 orchestration slice" in plan.read_text()

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nplan" in board
    assert "- Phase 4 orchestration slice" in board


def test_review_creates_gate_and_moves_board_to_review_when_no_taste_decisions(
    tmp_path: Path,
) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(
        tmp_path,
        "review",
        "--title",
        "Phase 5 review gate",
        "--input-summary",
        "Discovery and planning artifacts were reviewed",
        "--review-pass",
        "Product: scope is coherent",
        "--review-pass",
        "Architecture: module split is acceptable",
        "--auto-decision",
        "Keep the current milestone boundary",
        "--recommendation",
        "Proceed to build",
        "--approval-target",
        "lead",
        "--review-path",
        "docs/plans/review-gate.md",
    )

    assert result.returncode == 0, result.stderr
    review_gate = tmp_path / "docs" / "plans" / "review-gate.md"
    assert review_gate.exists()
    assert "# Review Gate: Phase 5 review gate" in review_gate.read_text()

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nreview" in board
    assert "- Phase 5 review gate" in board


def test_review_moves_board_to_approval_needed_when_taste_decisions_exist(
    tmp_path: Path,
) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(
        tmp_path,
        "review",
        "--title",
        "Phase 5 review gate",
        "--input-summary",
        "Discovery and planning artifacts were reviewed",
        "--review-pass",
        "Product: scope is coherent",
        "--auto-decision",
        "Keep the current milestone boundary",
        "--taste-decision",
        "Decide whether to add a design review pass before build",
        "--recommendation",
        "Pause for approval",
        "--approval-target",
        "user",
        "--review-path",
        "docs/plans/review-gate.md",
    )

    assert result.returncode == 0, result.stderr
    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\napproval-needed" in board
    assert "- Phase 5 review gate" in board


def test_decision_can_move_board_to_approval_needed(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(
        tmp_path,
        "decision",
        "--title",
        "Refactor approval",
        "--context",
        "Architecture drift is growing",
        "--decision",
        "Pause for a scoped refactor proposal",
        "--consequence",
        "Work pauses pending approval",
        "--approval-needed",
        "--decision-path",
        "docs/decisions/refactor.md",
    )

    assert result.returncode == 0, result.stderr
    decision = tmp_path / "docs" / "decisions" / "refactor.md"
    assert decision.exists()
    assert "# Decision: Refactor approval" in decision.read_text()

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\napproval-needed" in board


def test_status_prints_compact_summary(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(tmp_path, "status")

    assert result.returncode == 0, result.stderr
    assert "Current goal: Drive runtime orchestration." in result.stdout
    assert "Stage: plan" in result.stdout
    assert "Active work:" in result.stdout
