from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def required_paths() -> list[Path]:
    return [
        ROOT / "docs" / "project",
        ROOT / "docs" / "plans",
        ROOT / "docs" / "status" / "MODULE_CONTRACTS",
        ROOT / "docs" / "decisions",
        ROOT / "ops" / "templates",
        ROOT / "ops" / "checks",
        ROOT / "skills" / "team-lead",
    ]


def main() -> int:
    missing = [path for path in required_paths() if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(ROOT)}")
        return 1
    print("repo layout ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
