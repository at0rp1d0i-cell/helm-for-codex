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
    (tmp_path / "docs" / "plans" / "office-hours-brief.md").write_text(
        "# Office-Hours Brief: Pixiu office hours\n\n"
        "## Problem Statement\n\n"
        "Pixiu needs a sharper experiment-creation loop.\n\n"
        "## Target User Or Operator\n\n"
        "ML engineer running local experiments.\n\n"
        "## Current Proposal\n\n"
        "Build a full experimentation platform for every workflow.\n\n"
        "## Constraints\n\n"
        "- First milestone must stay bounded.\n\n"
        "## Success Criteria\n\n"
        "- One experiment can be created and reviewed end to end.\n\n"
        "## Build vs Buy Context\n\n"
        "Building from scratch is possible but risky.\n\n"
        "## Assumptions To Challenge\n\n"
        "- Users need the whole platform immediately.\n"
        "- Custom orchestration is better than integrating existing tooling.\n"
        "- The first release must solve every workflow.\n"
    )
    (tmp_path / "docs" / "plans" / "research-report.md").write_text(
        "# Research Report: Pixiu office-hours research\n\n"
        "## Problem Framing\n\n"
        "The first milestone should optimize for one repo-local experiment path.\n\n"
        "## Research Brief\n\n"
        "docs/plans/research-brief.md\n\n"
        "## Top Options\n\n"
        "- Adopt a bounded repo-local baseline before wider orchestration.\n"
        "- Reuse existing experiment-tracking seams instead of a full platform build.\n\n"
        "## Recommendation\n\n"
        "Proceed with one bounded local milestone and defer broader platform scope.\n\n"
        "## Build vs Buy Posture\n\n"
        "Prefer a bounded local build with explicit reuse over a greenfield platform.\n\n"
        "## Adoption Notes\n\n"
        "- Keep integration seams visible in the first plan.\n\n"
        "## Open Risks\n\n"
        "- The operator flow is still under-specified.\n"
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


def test_role_review_runs_product_office_hours_pass(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_role_review(
        tmp_path,
        "--mode",
        "office-hours",
        "--role",
        "Product",
        "--brief-path",
        "docs/plans/office-hours-brief.md",
        "--research-report-path",
        "docs/plans/research-report.md",
        "--output",
        "docs/plans/challenge-pass-product.md",
    )

    assert result.returncode == 0, result.stderr
    content = (tmp_path / "docs" / "plans" / "challenge-pass-product.md").read_text()
    assert "# Review Pass: Product office-hours challenge" in content
    assert "## Role\n\nProduct" in content
    assert "target user pressure" in content.lower()
    assert "bounded repo-local baseline" in content.lower()
    assert "narrow scope" in content.lower()


def test_role_review_runs_design_office_hours_pass(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_role_review(
        tmp_path,
        "--mode",
        "office-hours",
        "--role",
        "Design",
        "--brief-path",
        "docs/plans/office-hours-brief.md",
        "--research-report-path",
        "docs/plans/research-report.md",
        "--output",
        "docs/plans/challenge-pass-design.md",
    )

    assert result.returncode == 0, result.stderr
    content = (tmp_path / "docs" / "plans" / "challenge-pass-design.md").read_text()
    assert "# Review Pass: Design office-hours challenge" in content
    assert "## Role\n\nDesign" in content
    assert "under-specified" in content.lower()
    assert "critical user or operator flow" in content.lower()


def test_role_review_runs_architect_office_hours_pass(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_role_review(
        tmp_path,
        "--mode",
        "office-hours",
        "--role",
        "Architect",
        "--brief-path",
        "docs/plans/office-hours-brief.md",
        "--research-report-path",
        "docs/plans/research-report.md",
        "--output",
        "docs/plans/challenge-pass-architect.md",
    )

    assert result.returncode == 0, result.stderr
    content = (tmp_path / "docs" / "plans" / "challenge-pass-architect.md").read_text()
    assert "# Review Pass: Architect office-hours challenge" in content
    assert "## Role\n\nArchitect" in content
    assert "build-vs-buy" in content.lower()
    assert "bounded local build" in content.lower()
    assert "building from scratch is justified" in content.lower()
