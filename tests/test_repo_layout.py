import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_top_level_paths_exist() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "docs" / "project",
        ROOT / "docs" / "plans",
        ROOT / "docs" / "plans" / "archive",
        ROOT / "docs" / "status" / "ONBOARDING_STATE.md",
        ROOT / "docs" / "status" / "MODULE_CONTRACTS",
        ROOT / "docs" / "decisions",
        ROOT / "ops" / "templates",
        ROOT / "ops" / "checks",
        ROOT / "skills" / "team-lead",
        ROOT / "scripts" / "check_repo.py",
        ROOT / "scripts" / "install_runtime_pack.py",
        ROOT / "scripts" / "bridge_runner.py",
        ROOT / "scripts" / "ops_loop.py",
        ROOT / "scripts" / "role_bridge.py",
        ROOT / "scripts" / "team_state.py",
        ROOT / "scripts" / "lead_loop.py",
        ROOT / "scripts" / "role_review.py",
        ROOT / ".agents" / "skills" / "ops-orchestrator",
        ROOT / ".agents" / "skills" / "team-lead",
        ROOT / ".agents" / "skills" / "product-discovery",
        ROOT / ".agents" / "skills" / "architecture-review",
        ROOT / ".agents" / "skills" / "code-reviewer",
        ROOT / ".agents" / "skills" / "implementation-worker",
        ROOT / ".agents" / "skills" / "qa-runner",
        ROOT / ".agents" / "skills" / "docs-sync",
        ROOT / ".agents" / "skills" / "refactor-planner",
        ROOT / ".agents" / "skills" / "release-manager",
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
        "README.md",
        "AGENTS.md",
        "docs/project/PROJECT_BRIEF.md",
        "docs/project/ROADMAP.md",
        "docs/project/ARCHITECTURE.md",
        "docs/project/QUALITY_BAR.md",
        "docs/project/TECH_DEBT.md",
        "docs/status/EXECUTION_BOARD.md",
        "docs/status/ONBOARDING_STATE.md",
        "docs/status/MODULE_CONTRACTS/README.md",
        "docs/plans/archive/.gitkeep",
        ".codex/config.toml",
        ".codex/role_bridge.toml",
        ".codex/roles/product-reviewer.toml",
        ".codex/roles/architect-reviewer.toml",
        ".codex/roles/code-reviewer.toml",
        ".codex/roles/implementation-worker.toml",
        ".codex/roles/qa-runner.toml",
        ".codex/roles/docs-sync.toml",
        ".codex/roles/ops-orchestrator.toml",
        "skills/ops-orchestrator/SKILL.md",
        "skills/ops-orchestrator/agents/openai.yaml",
        "skills/team-lead/SKILL.md",
        "skills/team-lead/agents/openai.yaml",
        ".agents/skills/ops-orchestrator/SKILL.md",
        ".agents/skills/ops-orchestrator/agents/openai.yaml",
        ".agents/skills/team-lead/SKILL.md",
        ".agents/skills/product-discovery/SKILL.md",
        ".agents/skills/architecture-review/SKILL.md",
        ".agents/skills/code-reviewer/SKILL.md",
        ".agents/skills/implementation-worker/SKILL.md",
        ".agents/skills/implementation-worker/agents/openai.yaml",
        ".agents/skills/qa-runner/SKILL.md",
        ".agents/skills/qa-runner/agents/openai.yaml",
        ".agents/skills/docs-sync/SKILL.md",
        ".agents/skills/docs-sync/agents/openai.yaml",
        ".agents/skills/refactor-planner/SKILL.md",
        ".agents/skills/refactor-planner/agents/openai.yaml",
        ".agents/skills/release-manager/SKILL.md",
        ".agents/skills/release-manager/agents/openai.yaml",
        "skills/product-discovery/SKILL.md",
        "skills/product-discovery/agents/openai.yaml",
        "skills/architecture-review/SKILL.md",
        "skills/architecture-review/agents/openai.yaml",
        "skills/implementation-worker/SKILL.md",
        "skills/implementation-worker/agents/openai.yaml",
        "skills/code-reviewer/SKILL.md",
        "skills/code-reviewer/agents/openai.yaml",
        "skills/qa-runner/SKILL.md",
        "skills/qa-runner/agents/openai.yaml",
        "skills/docs-sync/SKILL.md",
        "skills/docs-sync/agents/openai.yaml",
        "skills/refactor-planner/SKILL.md",
        "skills/refactor-planner/agents/openai.yaml",
        "skills/release-manager/SKILL.md",
        "skills/release-manager/agents/openai.yaml",
        "ops/templates/task-brief.md",
        "ops/templates/discovery-brief.md",
        "ops/templates/plan-brief.md",
        "ops/templates/dispatch-packet.md",
        "ops/templates/invocation-spec.md",
        "ops/templates/onboarding-state.md",
        "ops/templates/onboarding-report.md",
        "ops/templates/deep-scan-plan.md",
        "ops/templates/review-packet.md",
        "ops/templates/review-result.md",
        "ops/templates/review-gate.md",
        "ops/templates/review-pass.md",
        "ops/templates/review-report.md",
        "ops/templates/qa-report.md",
        "ops/templates/refactor-proposal.md",
        "ops/checks/check_docs_freshness.py",
        "scripts/install_runtime_pack.py",
        "scripts/bridge_runner.py",
        "scripts/ops_loop.py",
        "scripts/role_bridge.py",
        "scripts/team_state.py",
        "scripts/lead_loop.py",
        "scripts/role_review.py",
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


def test_team_lead_contract_is_visible_to_repo_validation() -> None:
    content = (ROOT / "skills" / "team-lead" / "SKILL.md").read_text()
    required_tokens = [
        "<canonical_state>",
        "<workflow>",
        "<automation_hooks>",
        "<approval_triggers>",
        "scripts/team_state.py",
        "ONBOARDING_STATE.md",
        "review-prepare",
        "review-collect",
        "approval-needed",
    ]
    for token in required_tokens:
        assert token in content


def test_codex_internal_role_config_declares_live_roles() -> None:
    content = (ROOT / ".codex" / "config.toml").read_text()
    required_tokens = [
        "roles/ops-orchestrator.toml",
        "roles/product-reviewer.toml",
        "roles/architect-reviewer.toml",
        "roles/code-reviewer.toml",
        "roles/implementation-worker.toml",
        "roles/qa-runner.toml",
        "roles/docs-sync.toml",
        'role_bridge = "role_bridge.toml"',
        'default_skill_path = ".agents/skills"',
        'onboarding_state = "docs/status/ONBOARDING_STATE.md"',
    ]
    for token in required_tokens:
        assert token in content
