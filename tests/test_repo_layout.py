import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_top_level_paths_exist() -> None:
    required = [
        ROOT / "docs" / "project",
        ROOT / "docs" / "plans",
        ROOT / "docs" / "status" / "MODULE_CONTRACTS",
        ROOT / "docs" / "decisions",
        ROOT / "ops" / "templates",
        ROOT / "ops" / "checks",
        ROOT / "skills" / "team-lead",
        ROOT / "scripts" / "check_repo.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []


def test_repo_check_covers_minimum_team_shape() -> None:
    spec = importlib.util.spec_from_file_location(
        "check_repo",
        ROOT / "scripts" / "check_repo.py",
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    expected = [
        "AGENTS.md",
        "docs/project/PROJECT_BRIEF.md",
        "docs/project/ROADMAP.md",
        "docs/project/ARCHITECTURE.md",
        "docs/project/QUALITY_BAR.md",
        "docs/status/EXECUTION_BOARD.md",
        "skills/team-lead/SKILL.md",
        "skills/team-lead/agents/openai.yaml",
        "skills/product-discovery/SKILL.md",
        "skills/architecture-review/SKILL.md",
        "skills/implementation-worker/SKILL.md",
        "skills/code-reviewer/SKILL.md",
        "skills/qa-runner/SKILL.md",
        "skills/docs-sync/SKILL.md",
        "skills/refactor-planner/SKILL.md",
        "skills/release-manager/SKILL.md",
        "ops/templates/task-brief.md",
        "ops/checks/check_docs_freshness.py",
    ]
    actual = {str(path.relative_to(ROOT)) for path in module.required_paths()}
    assert set(expected).issubset(actual)


def test_gitignore_covers_python_artifacts() -> None:
    content = (ROOT / ".gitignore").read_text()
    expected = [
        ".venv/",
        ".pytest_cache/",
        "__pycache__/",
        "*.pyc",
    ]
    for pattern in expected:
        assert pattern in content
