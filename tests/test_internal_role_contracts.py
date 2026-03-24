from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ROLE_FILES = [
    ROOT / "skills" / "product-discovery" / "SKILL.md",
    ROOT / "skills" / "architecture-review" / "SKILL.md",
    ROOT / "skills" / "implementation-worker" / "SKILL.md",
    ROOT / "skills" / "code-reviewer" / "SKILL.md",
    ROOT / "skills" / "qa-runner" / "SKILL.md",
    ROOT / "skills" / "docs-sync" / "SKILL.md",
    ROOT / "skills" / "refactor-planner" / "SKILL.md",
    ROOT / "skills" / "release-manager" / "SKILL.md",
]


def test_internal_roles_use_xml_like_contracts() -> None:
    required_blocks = [
        ("<mission>", "</mission>"),
        ("<inputs>", "</inputs>"),
        ("<expected_output>", "</expected_output>"),
        ("<writeback>", "</writeback>"),
        ("<non_goals>", "</non_goals>"),
        ("<reporting>", "</reporting>"),
    ]

    for path in ROLE_FILES:
        content = path.read_text()
        for start, end in required_blocks:
            assert start in content, f"{path.name} missing {start}"
            assert end in content, f"{path.name} missing {end}"
        assert "<input>" in content, f"{path.name} missing structured inputs"
        assert "<section>" in content, f"{path.name} missing structured output sections"
        assert "<target>" in content, f"{path.name} missing writeback targets"
        assert "<item>" in content, f"{path.name} missing non-goal items"
        assert "lead" in content.lower(), f"{path.name} must mention lead reporting"
        assert "do not address the user directly" in content.lower(), (
            f"{path.name} must explicitly prevent direct user-facing voice"
        )
        assert "ops/templates/" not in content, (
            f"{path.name} should write back to project state, not template paths"
        )
