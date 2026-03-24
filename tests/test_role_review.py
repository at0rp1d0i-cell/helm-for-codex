import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "role_review.py"


def run_role_review(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def seed_repo_state(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "project" / "PROJECT_BRIEF.md").write_text(
        "# Project Brief\n\n## Problem\n\nBuild a Codex-native AI team.\n\n## Current Goal\n\nRun live role reviews.\n\n## Success Criteria\n\n- review passes exist\n"
    )
    (tmp_path / "docs" / "project" / "ROADMAP.md").write_text(
        "# Roadmap\n\n## Current Milestone\n\nPhase 7\n\n## Later Milestones\n\n- more automation\n"
    )
    (tmp_path / "docs" / "project" / "ARCHITECTURE.md").write_text(
        "# Architecture\n\n## Layers\n\n- Lead layer\n- Ops layer\n- Worker layer\n\n## Modules\n\n- canonical docs\n- skills\n- ops templates\n- repo checks\n\n## Constraints\n\n- single visible lead\n- repo as memory\n"
    )
    (tmp_path / "docs" / "project" / "QUALITY_BAR.md").write_text(
        "# Quality Bar\n\n## Code\n\nPrefer modular, bounded, readable implementations.\n\n## Tests\n\nEvery structural rule added to the repo should have a validation check or test.\n\n## Docs\n\nCanonical project-state files must stay current when state changes.\n"
    )
    (tmp_path / "docs" / "plans" / "phase7-plan-brief.md").write_text(
        "# Plan Brief: Phase 7 orchestration slice\n\n## Goal\n\nRun Product, Architect, and Reviewer passes from canonical state.\n\n## Milestone\n\nPhase 7\n\n## Modules In Scope\n\nscripts/role_review.py, scripts/lead_loop.py, skills/team-lead/SKILL.md\n\n## Exit Criteria\n\nLive role review execution exists with tests and docs updates.\n\n## Writeback Target\n\ndocs/status/EXECUTION_BOARD.md\n"
    )


def test_role_review_runs_product_pass(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_role_review(
        tmp_path,
        "--role",
        "Product",
        "--plan-path",
        "docs/plans/phase7-plan-brief.md",
        "--output",
        "docs/plans/review-pass-product.md",
    )

    assert result.returncode == 0, result.stderr
    content = (tmp_path / "docs" / "plans" / "review-pass-product.md").read_text()
    assert "# Review Pass: Product review" in content
    assert "## Role\n\nProduct" in content
    assert "Keep the current milestone focus" in content


def test_role_review_runs_architect_pass(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_role_review(
        tmp_path,
        "--role",
        "Architect",
        "--plan-path",
        "docs/plans/phase7-plan-brief.md",
        "--output",
        "docs/plans/review-pass-architect.md",
    )

    assert result.returncode == 0, result.stderr
    content = (tmp_path / "docs" / "plans" / "review-pass-architect.md").read_text()
    assert "# Review Pass: Architect review" in content
    assert "## Role\n\nArchitect" in content
    assert "Keep the current repo-backed orchestration boundary" in content


def test_role_review_runs_reviewer_pass(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_role_review(
        tmp_path,
        "--role",
        "Reviewer",
        "--plan-path",
        "docs/plans/phase7-plan-brief.md",
        "--output",
        "docs/plans/review-pass-reviewer.md",
    )

    assert result.returncode == 0, result.stderr
    content = (tmp_path / "docs" / "plans" / "review-pass-reviewer.md").read_text()
    assert "# Review Pass: Reviewer review" in content
    assert "## Role\n\nReviewer" in content
    assert "Require verification before build" in content
