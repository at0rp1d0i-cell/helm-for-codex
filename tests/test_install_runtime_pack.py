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

    assert (target / "docs" / "project" / "PROJECT_BRIEF.md").exists()
    assert (target / "docs" / "project" / "ARCHITECTURE.md").exists()
    assert (target / "docs" / "project" / "QUALITY_BAR.md").exists()
    assert (target / "docs" / "project" / "TECH_DEBT.md").exists()
    assert (target / "docs" / "status" / "EXECUTION_BOARD.md").exists()
    assert (target / "docs" / "status" / "MODULE_CONTRACTS").exists()
    assert (target / "docs" / "plans").exists()

    assert (target / "docs" / "decisions").exists()

    assert (target / "docs" / "plans").exists()
    assert (target / "docs" / "plans" / "archive").exists()
