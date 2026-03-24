from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ops_templates_and_checks_exist() -> None:
    required = [
        ROOT / "ops" / "templates" / "task-brief.md",
        ROOT / "ops" / "templates" / "review-report.md",
        ROOT / "ops" / "templates" / "qa-report.md",
        ROOT / "ops" / "templates" / "refactor-proposal.md",
        ROOT / "ops" / "checks" / "check_docs_freshness.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []
