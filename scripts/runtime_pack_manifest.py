from __future__ import annotations

from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ".codex/helm4codex.toml"
PROJECT_NAME = "Helm4Codex"

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
    "scripts/upgrade_runtime_pack.py",
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


def project_version(root: Path = ROOT) -> str:
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        data = tomllib.loads(pyproject.read_text())
        return str(data["project"]["version"])
    return "0.1.0"


HELM4CODEX_VERSION = project_version()


def render_runtime_metadata(*, action: str, previous_version: str | None) -> str:
    lines = [
        "[helm4codex]",
        f'name = "{PROJECT_NAME}"',
        f'version = "{HELM4CODEX_VERSION}"',
        f'last_action = "{action}"',
    ]
    if previous_version:
        lines.append(f'previous_version = "{previous_version}"')
    return "\n".join(lines) + "\n"
