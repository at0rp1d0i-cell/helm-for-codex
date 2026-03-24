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
