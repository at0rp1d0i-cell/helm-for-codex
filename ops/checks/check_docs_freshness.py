import argparse
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def expected_headings(root: Path) -> dict[Path, list[str]]:
    return {
        root / "docs" / "project" / "PROJECT_BRIEF.md": [
            "# Project Brief",
            "## Problem",
            "## Current Goal",
            "## Success Criteria",
        ],
        root / "docs" / "project" / "ROADMAP.md": [
            "# Roadmap",
            "## Current Milestone",
            "## Later Milestones",
        ],
        root / "docs" / "project" / "ARCHITECTURE.md": [
            "# Architecture",
            "## Modules",
            "## Constraints",
        ],
        root / "docs" / "project" / "QUALITY_BAR.md": [
            "# Quality Bar",
            "## Code",
            "## Tests",
            "## Docs",
        ],
        root / "docs" / "status" / "EXECUTION_BOARD.md": [
            "# Execution Board",
            "_This file can be updated manually or via `scripts/team_state.py board`._",
            "## Current Stage",
            "## Active Work",
            "## Completed",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check canonical docs structure")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.root.resolve()
    heading_map = expected_headings(root)

    missing = [path for path in heading_map if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(root)}")
        return 1

    errors: list[str] = []
    for path, headings in heading_map.items():
        content = path.read_text()
        for heading in headings:
            if heading not in content:
                errors.append(f"MISSING HEADING {heading} in {path.relative_to(root)}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print("docs structure ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
