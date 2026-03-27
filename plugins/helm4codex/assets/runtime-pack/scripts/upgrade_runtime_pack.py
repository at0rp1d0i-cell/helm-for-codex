from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from install_runtime_pack import install_runtime_pack, read_installed_version
from runtime_pack_manifest import HELM4CODEX_VERSION, PROJECT_NAME


PRESERVED_STATE = [
    "AGENTS.md",
    "docs/project/PROJECT_BRIEF.md",
    "docs/status/EXECUTION_BOARD.md",
    "docs/status/ONBOARDING_STATE.md",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upgrade Helm4Codex in an installed repository")
    parser.add_argument("--target", type=Path, default=Path.cwd(), help="Target repository root")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = args.target.resolve()
    if not target.exists():
        raise SystemExit(f"Target repository does not exist: {target}")

    previous_version = read_installed_version(target)
    install_runtime_pack(target, action="upgrade", previous_version=previous_version)

    print(f"{PROJECT_NAME} runtime upgraded in {target}")
    print(f"previous version: {previous_version or 'unknown'}")
    print(f"current version: {HELM4CODEX_VERSION}")
    print("preserved canonical state:")
    for relpath in PRESERVED_STATE:
        print(f"- {relpath}")
    print("recommendation: restart Codex in the target repo and run the installed runtime checks after upgrading")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
