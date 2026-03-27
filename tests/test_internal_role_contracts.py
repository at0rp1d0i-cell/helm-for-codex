from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ROLE_FILES = [
    ROOT / "skills" / "ops-orchestrator" / "SKILL.md",
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
        assert "lead" in content.lower() or "ops" in content.lower(), (
            f"{path.name} must mention lead or ops reporting"
        )
        assert "do not address the user directly" in content.lower(), (
            f"{path.name} must explicitly prevent direct user-facing voice"
        )
        assert "ops/templates/" not in content, (
            f"{path.name} should write back to project state, not template paths"
        )


def test_implementation_worker_contract_requires_sprint_contract_and_report_path() -> None:
    content = (ROOT / "skills" / "implementation-worker" / "SKILL.md").read_text().lower()

    assert "dispatch packet" in content
    assert "sprint contract" in content
    assert "implementation-report" in content
    assert "generator" in content
    assert "planner" in content
    assert "bounded task" in content
    assert "do not claim feature-branch autonomy" in content
    assert "report only to ops" in content


def test_execution_roles_report_to_ops_layer() -> None:
    execution_roles = [
        ROOT / "skills" / "implementation-worker" / "SKILL.md",
        ROOT / "skills" / "qa-runner" / "SKILL.md",
        ROOT / "skills" / "docs-sync" / "SKILL.md",
    ]

    for path in execution_roles:
        content = path.read_text().lower()
        assert "report only to ops" in content, f"{path.name} should report to ops"
        assert "do not address the user directly" in content, (
            f"{path.name} must not address the user directly"
        )

    assert "dispatch packet" in (ROOT / "skills" / "implementation-worker" / "SKILL.md").read_text().lower()
    assert "dispatch packet" in (ROOT / "skills" / "qa-runner" / "SKILL.md").read_text().lower()
    assert "dispatch packet" in (ROOT / "skills" / "docs-sync" / "SKILL.md").read_text().lower()


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


def test_product_discovery_contract_mentions_autoplan_lane() -> None:
    content = (ROOT / "skills" / "product-discovery" / "SKILL.md").read_text().lower()
    assert "autoplan" in content
    assert "review gate" in content


def test_codex_role_files_bind_live_skills_and_writeback_paths() -> None:
    expected = {
        ROOT / ".codex" / "roles" / "ops-orchestrator.toml": (
            ".agents/skills/ops-orchestrator/SKILL.md",
            "docs/status/EXECUTION_BOARD.md",
            "scripts/ops_loop.py",
        ),
        ROOT / ".codex" / "roles" / "product-reviewer.toml": (
            ".agents/skills/product-discovery/SKILL.md",
            "docs/plans/review-passes/product.md",
            "scripts/team_state.py review-pass",
        ),
        ROOT / ".codex" / "roles" / "architect-reviewer.toml": (
            ".agents/skills/architecture-review/SKILL.md",
            "docs/plans/review-passes/architect.md",
            "scripts/team_state.py review-pass",
        ),
        ROOT / ".codex" / "roles" / "code-reviewer.toml": (
            ".agents/skills/code-reviewer/SKILL.md",
            "docs/plans/review-passes/reviewer.md",
            "scripts/team_state.py review-pass",
        ),
        ROOT / ".codex" / "roles" / "implementation-worker.toml": (
            ".agents/skills/implementation-worker/SKILL.md",
            "docs/plans/implementation-report-<task>.md",
            "scripts/team_state.py implementation-report",
        ),
        ROOT / ".codex" / "roles" / "qa-runner.toml": (
            ".agents/skills/qa-runner/SKILL.md",
            "docs/plans/qa-report-<task>.md",
            "scripts/ops_loop.py qa",
        ),
        ROOT / ".codex" / "roles" / "docs-sync.toml": (
            ".agents/skills/docs-sync/SKILL.md",
            "docs/plans/docs-sync-report-<task>.md",
            "scripts/ops_loop.py docs-sync",
        ),
    }
    for path, (skill_path, result_path, writeback_command) in expected.items():
        content = path.read_text()
        assert skill_path in content
        assert result_path in content
        assert writeback_command in content
        assert ".agents/skills" in content
        assert "metadata =" in content
        if "reviewer" in path.name:
            assert "compatibility_writeback_target" in content
            assert "scripts/team_state.py review-result" in content


def test_ops_orchestrator_contract_owns_dispatch_boundary() -> None:
    content = (ROOT / "skills" / "ops-orchestrator" / "SKILL.md").read_text().lower()
    assert "dispatch bounded work" in content
    assert "dispatch packets" in content
    assert "stage advancement" in content
    assert "report only to the lead" in content
    assert "specialists receive bounded packets from ops" in content
