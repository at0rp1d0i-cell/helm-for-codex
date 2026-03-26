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


def test_internal_skill_openai_metadata_exists_for_live_roles() -> None:
    roles = {
        "product-discovery": "Product Reviewer",
        "architecture-review": "Architect Reviewer",
        "code-reviewer": "Code Reviewer",
        "implementation-worker": "Implementation Worker",
        "qa-runner": "QA Runner",
        "docs-sync": "Docs Sync",
        "refactor-planner": "Refactor Planner",
        "release-manager": "Release Manager",
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


def test_runtime_builder_and_lead_skill_contracts_include_phase13_handoff_terms() -> None:
    for name in ["team-lead", "implementation-worker"]:
        content = (ROOT / ".agents" / "skills" / name / "SKILL.md").read_text().lower()
        assert "sprint contract" in content
        assert "implementation-report" in content

    team_lead = (ROOT / ".agents" / "skills" / "team-lead" / "SKILL.md").read_text().lower()
    assert "planner owns the sprint contract" in team_lead
    assert "build" in team_lead

    implementation_worker = (
        ROOT / ".agents" / "skills" / "implementation-worker" / "SKILL.md"
    ).read_text().lower()
    assert "do not claim feature-branch autonomy" in implementation_worker


def test_runtime_qa_skill_contract_includes_phase13_handoff_terms() -> None:
    content = (ROOT / ".agents" / "skills" / "qa-runner" / "SKILL.md").read_text().lower()
    assert "sprint contract" in content
    assert "implementation report" in content
    assert "qa-report" in content
    assert "evaluator" in content


def test_runtime_docs_sync_skill_contract_includes_phase13_handoff_terms() -> None:
    content = (ROOT / ".agents" / "skills" / "docs-sync" / "SKILL.md").read_text().lower()
    assert "implementation report" in content
    assert "qa report" in content
    assert "docs-sync report" in content
    assert "final consistency-evaluator" in content
    assert "repo-backed" in content


def test_runtime_execution_roles_report_to_ops() -> None:
    for name in ["implementation-worker", "qa-runner", "docs-sync"]:
        content = (ROOT / ".agents" / "skills" / name / "SKILL.md").read_text().lower()
        assert "report only to ops" in content
