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


def test_implementation_worker_contract_requires_sprint_contract_and_report_path() -> None:
    content = (ROOT / "skills" / "implementation-worker" / "SKILL.md").read_text().lower()

    assert "sprint contract" in content
    assert "implementation-report" in content
    assert "generator" in content
    assert "planner" in content
    assert "bounded task" in content
    assert "do not claim feature-branch autonomy" in content


def test_review_roles_can_write_structured_review_passes() -> None:
    review_roles = {
        ROOT / "skills" / "product-discovery" / "SKILL.md": "Product",
        ROOT / "skills" / "architecture-review" / "SKILL.md": "Architect",
        ROOT / "skills" / "code-reviewer" / "SKILL.md": "Reviewer",
    }

    for path, role in review_roles.items():
        content = path.read_text()
        assert "review-result" in content.lower(), f"{role} contract should mention review-result output"
        assert (
            "docs/plans/review-results/" in content
        ), f"{role} contract should allow direct review-result writeback"
        assert (
            "scripts/team_state.py review-result" in content
        ), f"{role} contract should include review-result writeback command shape"
        assert "review-pass" in content.lower(), f"{role} contract should mention review-pass ownership"
        assert (
            "docs/plans/review-passes/" in content
        ), f"{role} contract should allow direct review-pass writeback"
        assert (
            "scripts/team_state.py review-pass" in content
        ), f"{role} contract should include review-pass writeback command shape"
        assert "compatibility" in content.lower(), f"{role} contract should mention compatibility behavior"
        assert ".agents/skills" in content, f"{role} contract should refer to runtime packaging target"


def test_codex_role_files_bind_review_skills_and_writeback_paths() -> None:
    expected = {
        ROOT / ".codex" / "roles" / "product-reviewer.toml": (
            ".agents/skills/product-discovery/SKILL.md",
            "docs/plans/review-passes/product.md",
        ),
        ROOT / ".codex" / "roles" / "architect-reviewer.toml": (
            ".agents/skills/architecture-review/SKILL.md",
            "docs/plans/review-passes/architect.md",
        ),
        ROOT / ".codex" / "roles" / "code-reviewer.toml": (
            ".agents/skills/code-reviewer/SKILL.md",
            "docs/plans/review-passes/reviewer.md",
        ),
    }
    for path, (skill_path, result_path) in expected.items():
        content = path.read_text()
        assert skill_path in content
        assert result_path in content
        assert "scripts/team_state.py review-pass" in content
        assert "compatibility_writeback_target" in content
        assert "scripts/team_state.py review-result" in content
        assert ".agents/skills" in content
