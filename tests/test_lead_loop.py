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


def test_review_pass_creates_artifact_for_role(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)

    result = run_lead_loop(
        tmp_path,
        "review-pass",
        "--title",
        "Product pass",
        "--role",
        "Product",
        "--focus",
        "Scope coherence",
        "--finding",
        "Scope is coherent",
        "--auto-decision",
        "Keep the current milestone boundary",
        "--taste-decision",
        "Decide whether to add design references",
        "--recommendation",
        "Proceed after the design reference call",
        "--pass-path",
        "docs/plans/review-pass-product.md",
    )

    assert result.returncode == 0, result.stderr
    review_pass = tmp_path / "docs" / "plans" / "review-pass-product.md"
    assert review_pass.exists()
    assert "# Review Pass: Product pass" in review_pass.read_text()


def test_review_aggregates_passes_and_moves_board_to_review_when_no_taste_decisions(
    tmp_path: Path,
) -> None:
    seed_repo_state(tmp_path)

    run_lead_loop(
        tmp_path,
        "review-pass",
        "--title",
        "Product pass",
        "--role",
        "Product",
        "--focus",
        "Scope coherence",
        "--finding",
        "Scope is coherent",
        "--auto-decision",
        "Keep the milestone boundary",
        "--recommendation",
        "Proceed on scope",
        "--pass-path",
        "docs/plans/review-pass-product.md",
    )
    run_lead_loop(
        tmp_path,
        "review-pass",
        "--title",
        "Architect pass",
        "--role",
        "Architect",
        "--focus",
        "Module boundaries",
        "--finding",
        "Module split is acceptable",
        "--auto-decision",
        "Keep the current module split",
        "--recommendation",
        "Proceed on architecture",
        "--pass-path",
        "docs/plans/review-pass-architect.md",
    )

    result = run_lead_loop(
        tmp_path,
        "review",
        "--title",
        "Phase 6 review gate",
        "--pass-path",
        "docs/plans/review-pass-product.md",
        "--pass-path",
        "docs/plans/review-pass-architect.md",
        "--review-path",
        "docs/plans/review-gate.md",
    )

    assert result.returncode == 0, result.stderr
    review_gate = tmp_path / "docs" / "plans" / "review-gate.md"
    assert review_gate.exists()
    gate_content = review_gate.read_text()
    assert "# Review Gate: Phase 6 review gate" in gate_content
    assert "Product: Proceed on scope" in gate_content
    assert "Architect: Proceed on architecture" in gate_content
    assert "- Keep the milestone boundary" in gate_content
    assert "- Keep the current module split" in gate_content

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nreview" in board
    assert "- Phase 6 review gate" in board


def test_review_aggregates_taste_decisions_and_moves_board_to_approval_needed(
    tmp_path: Path,
) -> None:
    seed_repo_state(tmp_path)

    run_lead_loop(
        tmp_path,
        "review-pass",
        "--title",
        "Reviewer pass",
        "--role",
        "Reviewer",
        "--focus",
        "Completeness and regression risk",
        "--finding",
        "Implementation risk is low",
        "--auto-decision",
        "Keep the current milestone boundary",
        "--taste-decision",
        "Decide whether to add a design review pass before build",
        "--recommendation",
        "Pause for approval",
        "--pass-path",
        "docs/plans/review-pass-reviewer.md",
    )

    result = run_lead_loop(
        tmp_path,
        "review",
        "--title",
        "Phase 6 review gate",
        "--pass-path",
        "docs/plans/review-pass-reviewer.md",
        "--review-path",
        "docs/plans/review-gate.md",
    )

    assert result.returncode == 0, result.stderr
    gate_content = (tmp_path / "docs" / "plans" / "review-gate.md").read_text()
    assert "- Decide whether to add a design review pass before build" in gate_content

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\napproval-needed" in board
    assert "- Phase 6 review gate" in board


def test_review_run_executes_roles_and_aggregates_review_gate(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)
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

    result = run_lead_loop(
        tmp_path,
        "review-run",
        "--title",
        "Phase 7 review gate",
        "--plan-path",
        "docs/plans/phase7-plan-brief.md",
        "--review-dir",
        "docs/plans/review-passes",
        "--review-path",
        "docs/plans/review-gate.md",
    )

    assert result.returncode == 0, result.stderr
    review_dir = tmp_path / "docs" / "plans" / "review-passes"
    assert (review_dir / "product.md").exists()
    assert (review_dir / "architect.md").exists()
    assert (review_dir / "reviewer.md").exists()

    gate_content = (tmp_path / "docs" / "plans" / "review-gate.md").read_text()
    assert "Product: Proceed on scope" in gate_content
    assert "Architect: Proceed on architecture" in gate_content
    assert "Reviewer: Proceed on review" in gate_content

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nreview" in board
    assert "- Phase 7 review gate" in board


def test_review_prepare_generates_live_review_packets_and_moves_board(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)
    (tmp_path / "docs" / "project" / "ROADMAP.md").write_text(
        "# Roadmap\n\n## Current Milestone\n\nPhase 8\n\n## Later Milestones\n\n- more automation\n"
    )
    (tmp_path / "docs" / "project" / "ARCHITECTURE.md").write_text(
        "# Architecture\n\n## Layers\n\n- Lead layer\n- Ops layer\n- Worker layer\n\n## Modules\n\n- canonical docs\n- skills\n- ops templates\n- repo checks\n\n## Constraints\n\n- single visible lead\n- repo as memory\n"
    )
    (tmp_path / "docs" / "project" / "QUALITY_BAR.md").write_text(
        "# Quality Bar\n\n## Code\n\nPrefer modular, bounded, readable implementations.\n\n## Tests\n\nEvery structural rule added to the repo should have a validation check or test.\n\n## Docs\n\nCanonical project-state files must stay current when state changes.\n"
    )
    (tmp_path / "docs" / "plans" / "phase8-plan-brief.md").write_text(
        "# Plan Brief: Phase 8 orchestration slice\n\n## Goal\n\nPrepare live subagent review packets.\n\n## Milestone\n\nPhase 8\n\n## Modules In Scope\n\nscripts/team_state.py, scripts/lead_loop.py, skills/team-lead/SKILL.md\n\n## Exit Criteria\n\nReview packets exist and lead-managed preparation is tested.\n\n## Writeback Target\n\ndocs/status/EXECUTION_BOARD.md\n"
    )

    result = run_lead_loop(
        tmp_path,
        "review-prepare",
        "--title",
        "Phase 8 review preparation",
        "--plan-path",
        "docs/plans/phase8-plan-brief.md",
        "--review-dir",
        "docs/plans/review-packets",
        "--pass-dir",
        "docs/plans/review-passes",
        "--result-dir",
        "docs/plans/review-results",
    )

    assert result.returncode == 0, result.stderr
    review_dir = tmp_path / "docs" / "plans" / "review-packets"
    assert (review_dir / "product.md").exists()
    assert (review_dir / "architect.md").exists()
    assert (review_dir / "reviewer.md").exists()

    product_packet = (review_dir / "product.md").read_text()
    assert "# Review Packet: Product review packet" in product_packet
    assert "docs/project/PROJECT_BRIEF.md" in product_packet
    assert "docs/project/ROADMAP.md" in product_packet
    assert "docs/project/ARCHITECTURE.md" in product_packet
    assert "docs/project/QUALITY_BAR.md" in product_packet
    assert "docs/plans/phase8-plan-brief.md" in product_packet
    assert "Return a review-pass with Role, Focus, Findings, Auto Decisions, Taste Decisions, Recommendation" in product_packet
    assert "docs/plans/review-passes/product.md" in product_packet
    assert "scripts/team_state.py review-pass" in product_packet
    assert '--title "Product live pass"' in product_packet
    assert '--output docs/plans/review-passes/product.md' in product_packet

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nreview" in board
    assert "- Phase 8 review preparation" in board


def test_review_collect_converts_results_into_passes_and_gate(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)
    (tmp_path / "docs" / "plans" / "review-results").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "plans" / "review-results" / "product.md").write_text(
        "# Review Result: Product\n\n## Role\n\nProduct\n\n## Focus\n\nScope coherence\n\n## Findings\n\n- Scope is coherent\n\n## Auto Decisions\n\n- Keep the milestone boundary\n\n## Taste Decisions\n\n- none\n\n## Recommendation\n\nProceed on scope\n"
    )
    (tmp_path / "docs" / "plans" / "review-results" / "architect.md").write_text(
        "# Review Result: Architect\n\n## Role\n\nArchitect\n\n## Focus\n\nModule boundaries\n\n## Findings\n\n- Module split is acceptable\n\n## Auto Decisions\n\n- Keep the current module split\n\n## Taste Decisions\n\n- none\n\n## Recommendation\n\nProceed on architecture\n"
    )
    (tmp_path / "docs" / "plans" / "review-results" / "reviewer.md").write_text(
        "# Review Result: Reviewer\n\n## Role\n\nReviewer\n\n## Focus\n\nVerification readiness\n\n## Findings\n\n- Verification scope is acceptable\n\n## Auto Decisions\n\n- Require verification before build\n\n## Taste Decisions\n\n- none\n\n## Recommendation\n\nProceed on review\n"
    )

    result = run_lead_loop(
        tmp_path,
        "review-collect",
        "--title",
        "Phase 9 review gate",
        "--result-path",
        "docs/plans/review-results/product.md",
        "--result-path",
        "docs/plans/review-results/architect.md",
        "--result-path",
        "docs/plans/review-results/reviewer.md",
        "--pass-dir",
        "docs/plans/review-passes",
        "--review-path",
        "docs/plans/review-gate.md",
    )

    assert result.returncode == 0, result.stderr
    pass_dir = tmp_path / "docs" / "plans" / "review-passes"
    assert (pass_dir / "product.md").exists()
    assert (pass_dir / "architect.md").exists()
    assert (pass_dir / "reviewer.md").exists()

    gate_content = (tmp_path / "docs" / "plans" / "review-gate.md").read_text()
    assert "Product: Proceed on scope" in gate_content
    assert "Architect: Proceed on architecture" in gate_content
    assert "Reviewer: Proceed on review" in gate_content
    assert "- Require verification before build" in gate_content

    board = (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nreview" in board
    assert "- Phase 9 review gate" in board


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
