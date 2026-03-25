import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install_runtime_pack.py"


def run_installer(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--target", str(target)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_installer_populates_runtime_dirs(tmp_path: Path) -> None:
    target = tmp_path / "project"
    result = run_installer(target)
    assert result.returncode == 0, result.stderr
    assert target.exists()

    assert (target / "AGENTS.md").exists()
    assert (target / ".codex" / "config.toml").exists()
    assert (target / ".codex" / "roles" / "product-reviewer.toml").exists()
    assert (target / ".codex" / "roles" / "architect-reviewer.toml").exists()
    assert (target / ".codex" / "roles" / "code-reviewer.toml").exists()

    assert (target / ".agents" / "skills" / "team-lead" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "product-discovery" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "architecture-review" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "code-reviewer" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "implementation-worker" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "qa-runner" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "docs-sync" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "refactor-planner" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "release-manager" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "team-lead" / "agents" / "openai.yaml").exists()

    assert (target / "scripts" / "team_state.py").exists()
    assert (target / "scripts" / "lead_loop.py").exists()
    assert (target / "scripts" / "role_review.py").exists()
    assert (target / "ops" / "templates" / "task-brief.md").exists()
    assert (target / "ops" / "templates" / "onboarding-state.md").exists()
    assert (target / "ops" / "templates" / "deep-scan-plan.md").exists()
    assert (target / "ops" / "checks" / "check_docs_freshness.py").exists()

    assert (target / "docs" / "project" / "PROJECT_BRIEF.md").exists()
    assert (target / "docs" / "project" / "ARCHITECTURE.md").exists()
    assert (target / "docs" / "project" / "QUALITY_BAR.md").exists()
    assert (target / "docs" / "project" / "TECH_DEBT.md").exists()
    assert (target / "docs" / "status" / "EXECUTION_BOARD.md").exists()
    assert (target / "docs" / "status" / "ONBOARDING_STATE.md").exists()
    assert (target / "docs" / "status" / "MODULE_CONTRACTS").exists()
    assert (target / "docs" / "status" / "MODULE_CONTRACTS" / "README.md").exists()
    assert (target / "docs" / "plans").exists()

    assert (target / "docs" / "decisions").exists()

    assert (target / "docs" / "plans").exists()
    assert (target / "docs" / "plans" / "archive").exists()


def test_installer_preserves_existing_canonical_state(tmp_path: Path) -> None:
    target = tmp_path / "project"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr

    project_brief = target / "docs" / "project" / "PROJECT_BRIEF.md"
    onboarding_state = target / "docs" / "status" / "ONBOARDING_STATE.md"
    agents = target / "AGENTS.md"

    project_brief.write_text("# Project Brief\n\ncustom project state\n")
    onboarding_state.write_text("# Onboarding State: Custom\n\nmanual state\n")
    agents.write_text("# Project AGENTS\n\ncustom guidance\n")

    second = run_installer(target)
    assert second.returncode == 0, second.stderr

    assert project_brief.read_text() == "# Project Brief\n\ncustom project state\n"
    assert onboarding_state.read_text() == "# Onboarding State: Custom\n\nmanual state\n"
    assert agents.read_text() == "# Project AGENTS\n\ncustom guidance\n"
