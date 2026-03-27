from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def required_paths() -> list[Path]:
    return [
        ROOT / "AGENTS.md",
        ROOT / ".codex" / "config.toml",
        ROOT / ".codex" / "README.md",
        ROOT / ".codex" / "helm4codex.toml",
        ROOT / ".codex" / "role_bridge.toml",
        ROOT / ".codex" / "roles" / "ops-orchestrator.toml",
        ROOT / ".codex" / "roles" / "product-reviewer.toml",
        ROOT / ".codex" / "roles" / "architect-reviewer.toml",
        ROOT / ".codex" / "roles" / "code-reviewer.toml",
        ROOT / ".codex" / "roles" / "implementation-worker.toml",
        ROOT / ".codex" / "roles" / "qa-runner.toml",
        ROOT / ".codex" / "roles" / "docs-sync.toml",
        ROOT / ".agents" / "skills" / "team-lead" / "SKILL.md",
        ROOT / ".agents" / "skills" / "team-lead" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "ops-orchestrator" / "SKILL.md",
        ROOT / ".agents" / "skills" / "ops-orchestrator" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "product-discovery" / "SKILL.md",
        ROOT / ".agents" / "skills" / "product-discovery" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "architecture-review" / "SKILL.md",
        ROOT / ".agents" / "skills" / "architecture-review" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "code-reviewer" / "SKILL.md",
        ROOT / ".agents" / "skills" / "code-reviewer" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "implementation-worker" / "SKILL.md",
        ROOT / ".agents" / "skills" / "implementation-worker" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "qa-runner" / "SKILL.md",
        ROOT / ".agents" / "skills" / "qa-runner" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "docs-sync" / "SKILL.md",
        ROOT / ".agents" / "skills" / "docs-sync" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "refactor-planner" / "SKILL.md",
        ROOT / ".agents" / "skills" / "refactor-planner" / "agents" / "openai.yaml",
        ROOT / ".agents" / "skills" / "release-manager" / "SKILL.md",
        ROOT / ".agents" / "skills" / "release-manager" / "agents" / "openai.yaml",
        ROOT / "docs" / "project" / "PROJECT_BRIEF.md",
        ROOT / "docs" / "project" / "ROADMAP.md",
        ROOT / "docs" / "project" / "ARCHITECTURE.md",
        ROOT / "docs" / "project" / "QUALITY_BAR.md",
        ROOT / "docs" / "project" / "TECH_DEBT.md",
        ROOT / "docs" / "status" / "EXECUTION_BOARD.md",
        ROOT / "docs" / "status" / "ONBOARDING_STATE.md",
        ROOT / "docs" / "status" / "MODULE_CONTRACTS" / "README.md",
        ROOT / "docs" / "plans",
        ROOT / "docs" / "decisions",
        ROOT / "ops" / "templates" / "task-brief.md",
        ROOT / "ops" / "templates" / "dispatch-packet.md",
        ROOT / "ops" / "templates" / "invocation-spec.md",
        ROOT / "ops" / "templates" / "execution-receipt.md",
        ROOT / "ops" / "templates" / "onboarding-state.md",
        ROOT / "ops" / "templates" / "onboarding-report.md",
        ROOT / "ops" / "templates" / "deep-scan-plan.md",
        ROOT / "ops" / "templates" / "review-packet.md",
        ROOT / "ops" / "templates" / "review-result.md",
        ROOT / "ops" / "templates" / "review-gate.md",
        ROOT / "ops" / "templates" / "review-pass.md",
        ROOT / "ops" / "templates" / "review-report.md",
        ROOT / "ops" / "templates" / "qa-report.md",
        ROOT / "ops" / "templates" / "refactor-proposal.md",
        ROOT / "ops" / "checks" / "check_docs_freshness.py",
        ROOT / "scripts" / "check_installed_runtime.py",
        ROOT / "scripts" / "install_runtime_pack.py",
        ROOT / "scripts" / "runtime_pack_manifest.py",
        ROOT / "scripts" / "bridge_runner.py",
        ROOT / "scripts" / "team_state.py",
        ROOT / "scripts" / "lead_loop.py",
        ROOT / "scripts" / "ops_loop.py",
        ROOT / "scripts" / "role_bridge.py",
        ROOT / "scripts" / "role_review.py",
        ROOT / "scripts" / "upgrade_runtime_pack.py",
    ]


def main() -> int:
    missing = [path for path in required_paths() if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(ROOT)}")
        return 1
    print("installed runtime ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
