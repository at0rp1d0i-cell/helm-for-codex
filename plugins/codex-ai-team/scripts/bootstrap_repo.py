from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PACK_ROOT = PLUGIN_ROOT / "assets" / "runtime-pack"
INSTALLER = RUNTIME_PACK_ROOT / "scripts" / "install_runtime_pack.py"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap the Codex AI Team runtime into a repository")
    parser.add_argument("--target", type=Path, default=Path.cwd(), help="Target repository root")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = args.target.resolve()
    if not INSTALLER.exists():
        raise SystemExit(f"Missing embedded installer: {INSTALLER}")

    result = subprocess.run(
        [sys.executable, str(INSTALLER), "--target", str(target)],
        cwd=RUNTIME_PACK_ROOT,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return result.returncode
    print(f"Bootstrapped Codex AI Team runtime into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
