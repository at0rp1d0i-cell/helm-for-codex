from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_internal_skills_exist_with_frontmatter() -> None:
    expected = [
        "product-discovery",
        "architecture-review",
        "implementation-worker",
        "code-reviewer",
        "qa-runner",
        "docs-sync",
        "refactor-planner",
        "release-manager",
    ]
    for name in expected:
        content = (ROOT / "skills" / name / "SKILL.md").read_text()
        assert content.startswith("---")
        assert f"name: {name}" in content
