from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from runtime_pack_manifest import (
    CANONICAL_DOCS,
    MODULE_CONTRACT_DOCS,
    ROOT,
    RUNTIME_DIRS,
    pack_script_paths,
    skill_dirs,
)


DEFAULT_TARGET = ROOT / "plugins" / "helm4codex" / "assets" / "runtime-pack"


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _copy_dir(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "*.pyc"))


def export_runtime_pack(target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    _copy_file(ROOT / "AGENTS.md", target / "AGENTS.md")
    for rel_src, rel_dst in CANONICAL_DOCS:
        _copy_file(ROOT / rel_src, target / rel_dst)
    for rel_src, rel_dst in MODULE_CONTRACT_DOCS:
        _copy_file(ROOT / rel_src, target / rel_dst)

    for rel_path in pack_script_paths():
        _copy_file(ROOT / rel_path, target / rel_path)
    for rel_src, rel_dst in RUNTIME_DIRS:
        _copy_dir(ROOT / rel_src, target / rel_dst)

    _copy_file(ROOT / ".codex" / "config.toml", target / ".codex" / "config.toml")
    _copy_file(ROOT / ".codex" / "README.md", target / ".codex" / "README.md")
    _copy_file(ROOT / ".codex" / "role_bridge.toml", target / ".codex" / "role_bridge.toml")
    for role in sorted((ROOT / ".codex" / "roles").glob("*.toml")):
        _copy_file(role, target / ".codex" / "roles" / role.name)

    for skill_dir in skill_dirs(ROOT):
        _copy_dir(skill_dir, target / "skills" / skill_dir.name)


def _collect_files(root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            if "__pycache__" in path.parts:
                continue
            if path.suffix == ".pyc":
                continue
            files[str(path.relative_to(root))] = path.read_bytes()
    return files


def check_runtime_pack(target: Path) -> int:
    with tempfile.TemporaryDirectory() as tmpdir:
        expected = Path(tmpdir) / "runtime-pack"
        export_runtime_pack(expected)
        expected_files = _collect_files(expected)
        actual_files = _collect_files(target)

    if expected_files.keys() != actual_files.keys():
        missing = sorted(set(expected_files) - set(actual_files))
        extra = sorted(set(actual_files) - set(expected_files))
        for rel in missing:
            print(f"MISSING {rel}")
        for rel in extra:
            print(f"EXTRA {rel}")
        return 1

    for relpath, expected_bytes in expected_files.items():
        if actual_files[relpath] != expected_bytes:
            print(f"DIFF {relpath}")
            return 1

    print("plugin runtime pack ok")
    return 0


def _looks_like_repo_root(path: Path) -> bool:
    return (path / "scripts" / "export_plugin_runtime.py").exists() and (
        path / "plugins" / "helm4codex"
    ).exists()


def _resolve_target(path: Path | None) -> Path:
    if path is None:
        return DEFAULT_TARGET
    if _looks_like_repo_root(path):
        return path / "plugins" / "helm4codex" / "assets" / "runtime-pack"
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export the runtime pack into the plugin bundle")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="Plugin runtime-pack target, or repo root containing plugins/helm4codex",
    )
    parser.add_argument("--target", type=Path, help="Plugin runtime-pack target")
    parser.add_argument("--check", action="store_true", help="Verify the checked-in plugin runtime pack is in sync")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.path is not None and args.target is not None:
        parser.error("pass either PATH or --target, not both")

    target = _resolve_target(args.target or args.path).resolve()
    if args.check:
        return check_runtime_pack(target)

    export_runtime_pack(target)
    print(f"Plugin runtime pack exported into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
