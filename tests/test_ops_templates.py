import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_CHECK = ROOT / "ops" / "checks" / "check_docs_freshness.py"


def run_doc_check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DOC_CHECK), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )


def test_ops_templates_and_checks_exist() -> None:
    required = [
        ROOT / "ops" / "templates" / "task-brief.md",
        ROOT / "ops" / "templates" / "discovery-brief.md",
        ROOT / "ops" / "templates" / "plan-brief.md",
        ROOT / "ops" / "templates" / "review-gate.md",
        ROOT / "ops" / "templates" / "review-pass.md",
        ROOT / "ops" / "templates" / "review-packet.md",
        ROOT / "ops" / "templates" / "review-result.md",
        ROOT / "ops" / "templates" / "review-report.md",
        ROOT / "ops" / "templates" / "qa-report.md",
        ROOT / "ops" / "templates" / "refactor-proposal.md",
        ROOT / "ops" / "checks" / "check_docs_freshness.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []

    task_brief = (ROOT / "ops" / "templates" / "task-brief.md").read_text()
    assert "# Task Brief: <title>" in task_brief
    assert "<objective>" in task_brief
    assert "<writeback_target>" in task_brief

    discovery_brief = (ROOT / "ops" / "templates" / "discovery-brief.md").read_text()
    assert "# Discovery Brief: <title>" in discovery_brief
    assert "<problem_signal>" in discovery_brief
    assert "<recommendation_target>" in discovery_brief

    plan_brief = (ROOT / "ops" / "templates" / "plan-brief.md").read_text()
    assert "# Plan Brief: <title>" in plan_brief
    assert "<modules_in_scope>" in plan_brief
    assert "<writeback_target>" in plan_brief

    review_gate = (ROOT / "ops" / "templates" / "review-gate.md").read_text()
    assert "# Review Gate: <title>" in review_gate
    assert "<review_passes>" in review_gate
    assert "<taste_decisions>" in review_gate
    assert "<approval_target>" in review_gate

    review_pass = (ROOT / "ops" / "templates" / "review-pass.md").read_text()
    assert "# Review Pass: <title>" in review_pass
    assert "<role>" in review_pass
    assert "<auto_decisions>" in review_pass
    assert "<taste_decisions>" in review_pass

    review_packet = (ROOT / "ops" / "templates" / "review-packet.md").read_text()
    assert "# Review Packet: <title>" in review_packet
    assert "<role>" in review_packet
    assert "<objective>" in review_packet
    assert "<canonical_sources>" in review_packet
    assert "<plan_brief_path>" in review_packet
    assert "<expected_output>" in review_packet
    assert "<writeback_target>" in review_packet
    assert "## Writeback Command" in review_packet
    assert "<writeback_command>" in review_packet
    assert "scripts/team_state.py review-pass" in review_packet

    review_result = (ROOT / "ops" / "templates" / "review-result.md").read_text()
    assert "# Review Result: <title>" in review_result
    assert "<role>" in review_result
    assert "<focus>" in review_result
    assert "<findings>" in review_result
    assert "<auto_decisions>" in review_result
    assert "<taste_decisions>" in review_result
    assert "<recommendation>" in review_result

    refactor = (ROOT / "ops" / "templates" / "refactor-proposal.md").read_text()
    assert "# Refactor Proposal" in refactor
    assert "<problem_scope>" in refactor
    assert "<minimum_intervention>" in refactor


def test_check_docs_freshness_validates_structure() -> None:
    result = run_doc_check(ROOT)
    assert result.returncode == 0
    assert "docs structure ok" in result.stdout
    assert "docs freshness baseline ok" not in result.stdout


def test_check_docs_freshness_rejects_board_without_preamble(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True)
    (tmp_path / "docs" / "status").mkdir(parents=True)

    files = {
        "docs/project/PROJECT_BRIEF.md": "# Project Brief\n\n## Problem\n\nx\n\n## Current Goal\n\nship phase 3\n\n## Success Criteria\n\ny\n",
        "docs/project/ROADMAP.md": "# Roadmap\n\n## Current Milestone\n\nx\n\n## Later Milestones\n\ny\n",
        "docs/project/ARCHITECTURE.md": "# Architecture\n\n## Modules\n\nx\n\n## Constraints\n\ny\n",
        "docs/project/QUALITY_BAR.md": "# Quality Bar\n\n## Code\n\nx\n\n## Tests\n\ny\n\n## Docs\n\nz\n",
        "docs/status/EXECUTION_BOARD.md": "# Execution Board\n\n## Current Stage\n\nplan\n\n## Active Work\n\n- x\n\n## Completed\n\n- y\n",
    }
    for relpath, content in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    result = run_doc_check(tmp_path)
    assert result.returncode == 1
    assert "scripts/team_state.py board" in result.stdout


def test_check_docs_freshness_rejects_board_without_completed_section(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True)
    (tmp_path / "docs" / "status").mkdir(parents=True)

    files = {
        "docs/project/PROJECT_BRIEF.md": "# Project Brief\n\n## Problem\n\nx\n\n## Current Goal\n\nship phase 3\n\n## Success Criteria\n\ny\n",
        "docs/project/ROADMAP.md": "# Roadmap\n\n## Current Milestone\n\nx\n\n## Later Milestones\n\ny\n",
        "docs/project/ARCHITECTURE.md": "# Architecture\n\n## Modules\n\nx\n\n## Constraints\n\ny\n",
        "docs/project/QUALITY_BAR.md": "# Quality Bar\n\n## Code\n\nx\n\n## Tests\n\ny\n\n## Docs\n\nz\n",
        "docs/status/EXECUTION_BOARD.md": "# Execution Board\n\n_This file can be updated manually or via `scripts/team_state.py board`._\n\n## Current Stage\n\nplan\n\n## Active Work\n\n- x\n",
    }
    for relpath, content in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    result = run_doc_check(tmp_path)
    assert result.returncode == 1
    assert "## Completed" in result.stdout


def test_check_docs_freshness_rejects_project_brief_without_current_goal(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True)
    (tmp_path / "docs" / "status").mkdir(parents=True)

    files = {
        "docs/project/PROJECT_BRIEF.md": "# Project Brief\n\n## Problem\n\nx\n\n## Success Criteria\n\ny\n",
        "docs/project/ROADMAP.md": "# Roadmap\n\n## Current Milestone\n\nx\n\n## Later Milestones\n\ny\n",
        "docs/project/ARCHITECTURE.md": "# Architecture\n\n## Modules\n\nx\n\n## Constraints\n\ny\n",
        "docs/project/QUALITY_BAR.md": "# Quality Bar\n\n## Code\n\nx\n\n## Tests\n\ny\n\n## Docs\n\nz\n",
        "docs/status/EXECUTION_BOARD.md": "# Execution Board\n\n_This file can be updated manually or via `scripts/team_state.py board`._\n\n## Current Stage\n\nplan\n\n## Active Work\n\n- x\n\n## Completed\n\n- y\n",
    }
    for relpath, content in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    result = run_doc_check(tmp_path)
    assert result.returncode == 1
    assert "## Current Goal" in result.stdout
