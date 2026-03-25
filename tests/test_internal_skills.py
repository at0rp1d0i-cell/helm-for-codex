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


def test_internal_review_skill_openai_metadata_exists() -> None:
    roles = {
        "product-discovery": "Product Reviewer",
        "architecture-review": "Architect Reviewer",
        "code-reviewer": "Code Reviewer",
    }
    for skill_name, display_name in roles.items():
        content = (ROOT / "skills" / skill_name / "agents" / "openai.yaml").read_text()
        assert f"display_name: {display_name}" in content
        assert "description:" in content
        assert "allow_implicit_invocation: false" in content


def test_runtime_skill_mirror_matches_source_skills() -> None:
    for source_dir in sorted((ROOT / "skills").iterdir()):
        skill_file = source_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        mirrored_dir = ROOT / ".agents" / "skills" / source_dir.name
        mirrored_skill = mirrored_dir / "SKILL.md"
        assert mirrored_skill.exists(), f"missing mirrored skill for {source_dir.name}"
        assert mirrored_skill.read_text() == skill_file.read_text()

        source_metadata = source_dir / "agents" / "openai.yaml"
        mirrored_metadata = mirrored_dir / "agents" / "openai.yaml"
        if source_metadata.exists():
            assert mirrored_metadata.exists(), f"missing mirrored metadata for {source_dir.name}"
            assert mirrored_metadata.read_text() == source_metadata.read_text()
