from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CANONICAL_DOCS = [
    ("docs/project/PROJECT_BRIEF.md", "docs/project/PROJECT_BRIEF.md"),
    ("docs/project/ROADMAP.md", "docs/project/ROADMAP.md"),
    ("docs/project/ARCHITECTURE.md", "docs/project/ARCHITECTURE.md"),
    ("docs/project/QUALITY_BAR.md", "docs/project/QUALITY_BAR.md"),
    ("docs/project/TECH_DEBT.md", "docs/project/TECH_DEBT.md"),
    ("docs/status/EXECUTION_BOARD.md", "docs/status/EXECUTION_BOARD.md"),
    ("docs/status/ONBOARDING_STATE.md", "docs/status/ONBOARDING_STATE.md"),
]

MODULE_CONTRACT_DOCS = [
    ("docs/status/MODULE_CONTRACTS/README.md", "docs/status/MODULE_CONTRACTS/README.md"),
    ("docs/status/MODULE_CONTRACTS/team-lead.md", "docs/status/MODULE_CONTRACTS/team-lead.md"),
]

TARGET_RUNTIME_SCRIPTS = [
    "scripts/bridge_runner.py",
    "scripts/team_state.py",
    "scripts/lead_loop.py",
    "scripts/ops_loop.py",
    "scripts/role_bridge.py",
    "scripts/role_review.py",
]

PACK_ONLY_SCRIPTS = [
    "scripts/install_runtime_pack.py",
    "scripts/runtime_pack_manifest.py",
]

RUNTIME_DIRS = [
    ("ops/templates", "ops/templates"),
    ("ops/checks", "ops/checks"),
]


def skill_dirs(root: Path = ROOT) -> list[Path]:
    return sorted(path for path in (root / "skills").iterdir() if (path / "SKILL.md").exists())


def pack_script_paths() -> list[str]:
    return [*TARGET_RUNTIME_SCRIPTS, *PACK_ONLY_SCRIPTS]

