from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DOCS = [
    ("docs/project/PROJECT_BRIEF.md", "docs/project/PROJECT_BRIEF.md"),
    ("docs/project/ROADMAP.md", "docs/project/ROADMAP.md"),
    ("docs/project/ARCHITECTURE.md", "docs/project/ARCHITECTURE.md"),
    ("docs/project/QUALITY_BAR.md", "docs/project/QUALITY_BAR.md"),
    ("docs/project/TECH_DEBT.md", "docs/project/TECH_DEBT.md"),
    ("docs/status/EXECUTION_BOARD.md", "docs/status/EXECUTION_BOARD.md"),
]


def skill_dirs() -> list[Path]:
    return sorted(path for path in (ROOT / "skills").iterdir() if (path / "SKILL.md").exists())


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dst.resolve():
        return
    shutil.copy2(src, dst)


def _copy_dir(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
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
    (codex_dir / "roles").mkdir(parents=True, exist_ok=True)
    for role in ("product-reviewer.toml", "architect-reviewer.toml", "code-reviewer.toml"):
        _copy_file(ROOT / ".codex" / "roles" / role, codex_dir / "roles" / role)


def bootstrap_docs(target: Path) -> None:
    for rel_src, rel_dst in CANONICAL_DOCS:
        _copy_file(ROOT / rel_src, target / rel_dst)
    (target / "docs" / "status" / "MODULE_CONTRACTS").mkdir(parents=True, exist_ok=True)
    (target / "docs" / "decisions").mkdir(parents=True, exist_ok=True)
    (target / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (target / "docs" / "plans" / "archive").mkdir(parents=True, exist_ok=True)
    (target / "docs" / "plans" / "archive" / ".gitkeep").write_text("")


def install_project_fields(target: Path) -> None:
    _copy_file(ROOT / "AGENTS.md", target / "AGENTS.md")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install the runtime pack into another repo")
    parser.add_argument("--target", type=Path, default=Path.cwd(), help="Target repository root")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = args.target.resolve()
    if not target.exists():
        target.mkdir(parents=True)

    install_project_fields(target)
    bootstrap_docs(target)
    install_skills(target)
    install_codex_config(target)

    print(f"Runtime pack installed into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
