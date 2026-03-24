from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def required_paths() -> list[Path]:
    return [
        ROOT / "AGENTS.md",
        ROOT / "docs" / "project" / "PROJECT_BRIEF.md",
        ROOT / "docs" / "project" / "ROADMAP.md",
        ROOT / "docs" / "project" / "ARCHITECTURE.md",
        ROOT / "docs" / "project" / "QUALITY_BAR.md",
        ROOT / "docs" / "status" / "EXECUTION_BOARD.md",
        ROOT / "docs" / "status" / "MODULE_CONTRACTS",
        ROOT / "docs" / "plans",
        ROOT / "docs" / "decisions",
        ROOT / "ops" / "templates" / "task-brief.md",
        ROOT / "ops" / "templates" / "discovery-brief.md",
        ROOT / "ops" / "templates" / "plan-brief.md",
        ROOT / "ops" / "templates" / "review-packet.md",
        ROOT / "ops" / "templates" / "review-gate.md",
        ROOT / "ops" / "templates" / "review-pass.md",
        ROOT / "ops" / "templates" / "review-report.md",
        ROOT / "ops" / "templates" / "qa-report.md",
        ROOT / "ops" / "templates" / "refactor-proposal.md",
        ROOT / "ops" / "checks" / "check_docs_freshness.py",
        ROOT / "scripts" / "team_state.py",
        ROOT / "scripts" / "lead_loop.py",
        ROOT / "scripts" / "role_review.py",
        ROOT / "skills" / "team-lead" / "SKILL.md",
        ROOT / "skills" / "team-lead" / "agents" / "openai.yaml",
        ROOT / "skills" / "product-discovery" / "SKILL.md",
        ROOT / "skills" / "architecture-review" / "SKILL.md",
        ROOT / "skills" / "implementation-worker" / "SKILL.md",
        ROOT / "skills" / "code-reviewer" / "SKILL.md",
        ROOT / "skills" / "qa-runner" / "SKILL.md",
        ROOT / "skills" / "docs-sync" / "SKILL.md",
        ROOT / "skills" / "refactor-planner" / "SKILL.md",
        ROOT / "skills" / "release-manager" / "SKILL.md",
    ]


def main() -> int:
    missing = [path for path in required_paths() if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(ROOT)}")
        return 1
    print("repo layout ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
