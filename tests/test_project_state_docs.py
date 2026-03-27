from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text()


def test_canonical_state_docs_have_required_headings() -> None:
    expected = {
        "AGENTS.md": ["# AI Team Operating Guide", "## Single Entry", "## Canonical State"],
        "docs/project/PROJECT_BRIEF.md": ["# Project Brief", "## Problem", "## Success Criteria"],
        "docs/project/ROADMAP.md": ["# Roadmap", "## Current Milestone", "## Later Milestones"],
        "docs/project/ARCHITECTURE.md": ["# Architecture", "## Modules", "## Constraints"],
        "docs/project/QUALITY_BAR.md": ["# Quality Bar", "## Code", "## Tests", "## Docs"],
        "docs/project/TECH_DEBT.md": ["# Tech Debt", "## Active Debt", "## Deferred Debt"],
        "docs/status/ONBOARDING_STATE.md": ["# Onboarding State:", "## Stage", "## Last Scan", "## Notes"],
        "docs/status/EXECUTION_BOARD.md": ["# Execution Board", "## Current Stage", "## Active Work"],
        "docs/status/MODULE_CONTRACTS/README.md": ["# Module Contracts", "## Required Fields"],
    }
    for relpath, headings in expected.items():
        content = read(relpath)
        for heading in headings:
            assert heading in content, f"{heading} missing from {relpath}"


def test_readme_describes_team_model_and_granularity() -> None:
    content = read("README.md")
    required = [
        "# Codex-Native AI Team",
        "## Team Model",
        "## Runtime Layout",
        "## Install Paths",
        "## Install Via Plugin",
        "## Distribution Surface",
        "## Agent Work Granularity",
        "bounded task",
        "feature slice",
        "feature branch",
        "Lead",
        ".agents/skills",
        ".codex/config.toml",
        "plugins/codex-ai-team",
    ]
    for token in required:
        if token.islower():
            assert token in content.lower(), f"{token} missing from README"
        else:
            assert token in content, f"{token} missing from README"
