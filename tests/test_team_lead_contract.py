from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_team_lead_skill_has_phase2_orchestration_contract() -> None:
    content = (ROOT / "skills" / "team-lead" / "SKILL.md").read_text()

    xml_blocks = [
        ("<canonical_state>", "</canonical_state>"),
        ("<internal_roles>", "</internal_roles>"),
        ("<core_duties>", "</core_duties>"),
        ("<workflow>", "</workflow>"),
        ("<automation_hooks>", "</automation_hooks>"),
        ("<approval_triggers>", "</approval_triggers>"),
    ]
    for start, end in xml_blocks:
        assert start in content
        assert end in content

    canonical_refs = [
        "docs/project/PROJECT_BRIEF.md",
        "docs/project/ROADMAP.md",
        "docs/project/ARCHITECTURE.md",
        "docs/project/QUALITY_BAR.md",
        "docs/project/TECH_DEBT.md",
        "docs/status/EXECUTION_BOARD.md",
        "docs/status/MODULE_CONTRACTS/",
        "docs/decisions/",
        "docs/plans/",
    ]
    for ref in canonical_refs:
        assert ref in content

    state_machine_tokens = [
        "intake -> discovery -> plan -> approval-needed -> build -> review -> qa -> docs-sync -> ship-ready -> evolve",
        "approval-needed",
    ]
    for token in state_machine_tokens:
        assert token in content

    role_roster = [
        "Ops",
        "Product",
        "Researcher",
        "Architect",
        "Builder",
        "Reviewer",
        "QA",
        "Docs",
        "Refactor Planner",
        "Release",
    ]
    for role in role_roster:
        assert role in content

    automation_refs = [
        "task brief",
        "sprint contract",
        "implementation-report",
        "decision",
        "execution board",
        "ops/templates/review-packet.md",
        "ops/templates/review-result.md",
        ".codex/config.toml",
        ".codex/roles/",
        "ops-orchestrator",
        "scripts/team_state.py",
        "scripts/lead_loop.py",
        "scripts/ops_loop.py",
        "scripts/role_review.py",
        "discover",
        "plan",
        "build",
        "qa-prepare",
        "docs-sync-prepare",
        "delegate",
        "review-prepare",
        "review-collect",
        "review-pass",
        "review",
        "review-run",
        "status",
        "onboarding",
        ".agents/skills/",
    ]
    for ref in automation_refs:
        assert ref in content.lower()

    assert "`scripts/team_state.py`" not in content
    assert "`intake -> discovery -> plan -> approval-needed -> build -> review -> qa -> docs-sync -> ship-ready -> evolve`" not in content

    escalation_triggers = [
        "structural refactor",
        "major scope",
        "high-impact architecture",
        "cost-heavy dependency",
    ]
    for trigger in escalation_triggers:
        assert trigger in content.lower()

    assert "repository-backed state transitions" in content.lower()
    assert "repository-backed discovery" in content.lower()
    assert "repository-backed planning" in content.lower()
    assert "review gate" in content.lower()
    assert "taste decisions" in content.lower()
    assert "multi-role review passes" in content.lower()
    assert "live subagent review preparation" in content.lower()
    assert "direct role-owned canonical review-pass writeback" in content.lower()
    assert "repo-scoped codex review role config" in content.lower()
    assert "review-result plus lead_loop.py review-collect available as a compatibility path" in content.lower()
    assert "onboarding" in content.lower()
    assert ".agents/skills" in content
    assert "deterministic fallback" in content.lower()
    assert "planner owns the sprint contract" in content.lower()
    assert "builder must not start before the sprint contract exists" in content.lower()
    assert "implementation-report" in content.lower()
    assert "bounded task" in content.lower()
    assert "do not imply full feature-branch autonomy" in content.lower()
    assert "sole builder kickoff path" in content.lower()
    assert "delegate to create a bounded delegated task and move the board into build" not in content.lower()
    assert "user-facing facade" in content.lower()
    assert "does not dispatch specialist work directly" in content.lower()
    assert "routes execution through ops_loop.py" in content.lower()
    assert "ops" in content.lower()


def test_team_lead_openai_metadata_is_tight_and_explicit() -> None:
    content = (ROOT / "skills" / "team-lead" / "agents" / "openai.yaml").read_text()
    assert "display_name: Team Lead" in content
    assert "description:" in content
    assert "Single-entry lead" in content
    assert "allow_implicit_invocation: false" in content
