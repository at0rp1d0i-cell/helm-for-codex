from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from runtime_pack_manifest import (
    CANONICAL_DOCS,
    MODULE_CONTRACT_DOCS,
    ROOT,
    RUNTIME_DIRS,
    TARGET_RUNTIME_SCRIPTS,
    skill_dirs,
)


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dst.resolve():
        return
    shutil.copy2(src, dst)


def _bootstrap_file(src: Path, dst: Path) -> None:
    if dst.exists():
        return
    _copy_file(src, dst)


def _copy_dir(src: Path, dst: Path) -> None:
    if src.resolve() == dst.resolve():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "*.pyc"))


def install_skills(target: Path) -> None:
    base = target / ".agents" / "skills"
    base.mkdir(parents=True, exist_ok=True)
    for src in skill_dirs():
        dst = base / src.name
        _copy_dir(src, dst)


def install_codex_config(target: Path) -> None:
    codex_dir = target / ".codex"
    codex_dir.mkdir(parents=True, exist_ok=True)
    _copy_file(ROOT / ".codex" / "config.toml", codex_dir / "config.toml")
    _bootstrap_file(ROOT / ".codex" / "README.md", codex_dir / "README.md")
    _copy_file(ROOT / ".codex" / "role_bridge.toml", codex_dir / "role_bridge.toml")
    (codex_dir / "roles").mkdir(parents=True, exist_ok=True)
    for role in sorted((ROOT / ".codex" / "roles").glob("*.toml")):
        _copy_file(role, codex_dir / "roles" / role.name)


def bootstrap_docs(target: Path) -> None:
    for rel_src, rel_dst in CANONICAL_DOCS:
        _bootstrap_file(ROOT / rel_src, target / rel_dst)
    (target / "docs" / "status" / "MODULE_CONTRACTS").mkdir(parents=True, exist_ok=True)
    for rel_src, rel_dst in MODULE_CONTRACT_DOCS:
        _bootstrap_file(ROOT / rel_src, target / rel_dst)
    (target / "docs" / "decisions").mkdir(parents=True, exist_ok=True)
    (target / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (target / "docs" / "plans" / "archive").mkdir(parents=True, exist_ok=True)
    (target / "docs" / "plans" / "archive" / ".gitkeep").write_text("")


def install_project_fields(target: Path) -> None:
    _bootstrap_file(ROOT / "AGENTS.md", target / "AGENTS.md")


def install_runtime_files(target: Path) -> None:
    for rel_path in TARGET_RUNTIME_SCRIPTS:
        _copy_file(ROOT / rel_path, target / rel_path)
    for rel_src, rel_dst in RUNTIME_DIRS:
        _copy_dir(ROOT / rel_src, target / rel_dst)


def install_runtime_pack(target: Path) -> None:
    install_project_fields(target)
    bootstrap_docs(target)
    install_skills(target)
    install_codex_config(target)
    install_runtime_files(target)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install the runtime pack into another repo")
    parser.add_argument("--target", type=Path, default=Path.cwd(), help="Target repository root")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = args.target.resolve()
    if not target.exists():
        target.mkdir(parents=True)

    install_runtime_pack(target)

    print(f"Runtime pack installed into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
