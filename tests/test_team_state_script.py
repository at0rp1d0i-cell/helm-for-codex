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
        "--objective",
        "Assess milestone fit and scope pressure",
        "--canonical-source",
        "docs/project/PROJECT_BRIEF.md",
        "--canonical-source",
        "docs/project/ROADMAP.md",
        "--plan-brief",
        "docs/plans/phase8-plan-brief.md",
        "--expected-output",
        "Findings, auto decisions, taste decisions, recommendation",
        "--writeback",
        "docs/plans/review-pass-product.md",
        "--writeback-command",
        "uv run python scripts/team_state.py review-result --output docs/plans/review-results/product.md --title '<title>' --role Product --focus '<focus>' --finding '<finding>' --auto-decision '<auto_decision>' --recommendation '<recommendation>'",
    )
    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "review-packets" / "product.md"
    assert out.exists()
    content = out.read_text()
    assert "# Review Packet: Product packet" in content
    assert "## Role" in content
    assert "## Objective" in content
    assert "## Canonical Sources" in content
    assert "- docs/project/PROJECT_BRIEF.md" in content
    assert "- docs/project/ROADMAP.md" in content
    assert "## Plan Brief" in content
    assert "docs/plans/phase8-plan-brief.md" in content
    assert "## Expected Output" in content
    assert "## Writeback Target" in content
    assert "## Writeback Command" in content
    assert "scripts/team_state.py review-result" in content


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
