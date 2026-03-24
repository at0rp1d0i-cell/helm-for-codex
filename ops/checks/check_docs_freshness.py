from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    required = [
        ROOT / "docs" / "project" / "PROJECT_BRIEF.md",
        ROOT / "docs" / "project" / "ROADMAP.md",
        ROOT / "docs" / "project" / "ARCHITECTURE.md",
        ROOT / "docs" / "project" / "QUALITY_BAR.md",
        ROOT / "docs" / "status" / "EXECUTION_BOARD.md",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(ROOT)}")
        return 1
    print("docs freshness baseline ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
