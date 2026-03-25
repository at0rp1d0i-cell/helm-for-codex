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
    (tmp_path / "docs" / "decisions").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "project" / "PROJECT_BRIEF.md").write_text(
        "# Project Brief\n\n## Problem\n\nAdopt a real project.\n\n## Current Goal\n\nStart onboarding.\n\n## Success Criteria\n\n- onboarding begins\n"
    )
    (tmp_path / "docs" / "status" / "EXECUTION_BOARD.md").write_text(
        "# Execution Board\n\n"
        "_This file can be updated manually or via `scripts/team_state.py board`._\n\n"
        "## Current Stage\n\nintake\n\n"
        "## Active Work\n\n- none\n\n"
        "## Completed\n\n- none\n"
    )


def test_init_requires_force_when_onboarding_state_already_exists(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)
    onboarding = tmp_path / "docs" / "status" / "ONBOARDING_STATE.md"
    onboarding.write_text(
        "# Onboarding State: Existing\n\n"
        "## Stage\n\nadopted\n\n"
        "## Last Scan\n\nshallow-scan\n\n"
        "## Pending Decisions\n\n- none\n\n"
        "## Notes\n\nAlready onboarded.\n"
    )

    result = run_lead_loop(
        tmp_path,
        "init",
        "--title",
        "Repository onboarding",
        "--summary",
        "Initial shallow scan complete",
        "--finding",
        "Tests are sparse",
        "--recommendation",
        "Add a smoke path",
        "--next-step",
        "Align on runtime validation tranche",
        "--goals",
        "Validate install build and run behavior",
        "--hypotheses",
        "Install may fail without env",
        "--probe",
        "install",
        "--evidence",
        "Install exits zero",
        "--risk-level",
        "medium",
        "--writeback-target",
        "docs/project/PROJECT_BRIEF.md",
    )

    assert result.returncode == 1
    assert "Re-run with --force" in result.stdout


def test_init_force_allows_manual_reinit(tmp_path: Path) -> None:
    seed_repo_state(tmp_path)
    onboarding = tmp_path / "docs" / "status" / "ONBOARDING_STATE.md"
    onboarding.write_text(
        "# Onboarding State: Existing\n\n"
        "## Stage\n\nadopted\n\n"
        "## Last Scan\n\nshallow-scan\n\n"
        "## Pending Decisions\n\n- none\n\n"
        "## Notes\n\nAlready onboarded.\n"
    )

    result = run_lead_loop(
        tmp_path,
        "init",
        "--title",
        "Repository onboarding",
        "--summary",
        "Initial shallow scan complete",
        "--finding",
        "Tests are sparse",
        "--recommendation",
        "Add a smoke path",
        "--next-step",
        "Align on runtime validation tranche",
        "--goals",
        "Validate install build and run behavior",
        "--hypotheses",
        "Install may fail without env",
        "--probe",
        "install",
        "--evidence",
        "Install exits zero",
        "--risk-level",
        "medium",
        "--writeback-target",
        "docs/project/PROJECT_BRIEF.md",
        "--force",
    )

    assert result.returncode == 0, result.stderr
    content = onboarding.read_text()
    assert "## Stage\n\nwaiting-user-alignment" in content
    assert "Shallow scan complete and deep scan plan prepared" in content
