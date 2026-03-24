from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_HEADINGS = {
    ROOT / "docs" / "project" / "PROJECT_BRIEF.md": [
        "# Project Brief",
        "## Problem",
        "## Success Criteria",
    ],
    ROOT / "docs" / "project" / "ROADMAP.md": [
        "# Roadmap",
        "## Current Milestone",
        "## Later Milestones",
    ],
    ROOT / "docs" / "project" / "ARCHITECTURE.md": [
        "# Architecture",
        "## Modules",
        "## Constraints",
    ],
    ROOT / "docs" / "project" / "QUALITY_BAR.md": [
        "# Quality Bar",
        "## Code",
        "## Tests",
        "## Docs",
    ],
    ROOT / "docs" / "status" / "EXECUTION_BOARD.md": [
        "# Execution Board",
        "## Current Stage",
        "## Active Work",
    ],
}


def main() -> int:
    missing = [path for path in EXPECTED_HEADINGS if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(ROOT)}")
        return 1

    errors: list[str] = []
    for path, headings in EXPECTED_HEADINGS.items():
        content = path.read_text()
        for heading in headings:
            if heading not in content:
                errors.append(f"MISSING HEADING {heading} in {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print("docs structure ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
