from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

from team_state import cmd_review_pass


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _extract_section(content: str, heading: str) -> str:
    marker = f"## {heading}\n\n"
    start = content.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    next_header = content.find("\n## ", start)
    if next_header == -1:
        return content[start:].strip()
    return content[start:next_header].strip()


def _count_modules(modules: str) -> int:
    return len([item.strip() for item in modules.split(",") if item.strip()])


def _resolve_role_pass(args: argparse.Namespace) -> SimpleNamespace:
    plan = _read(args.root / args.plan_path)
    brief = _read(args.root / "docs" / "project" / "PROJECT_BRIEF.md")
    roadmap = _read(args.root / "docs" / "project" / "ROADMAP.md")
    architecture = _read(args.root / "docs" / "project" / "ARCHITECTURE.md")
    quality_bar = _read(args.root / "docs" / "project" / "QUALITY_BAR.md")

    goal = _extract_section(plan, "Goal")
    milestone = _extract_section(plan, "Milestone")
    modules = _extract_section(plan, "Modules In Scope")
    exit_criteria = _extract_section(plan, "Exit Criteria")
    module_count = _count_modules(modules)

    if args.role == "Product":
        findings = [f"Plan goal aligns with current goal: {goal or _extract_section(brief, 'Current Goal')}"]
        auto_decisions = [f"Keep the current milestone focus: {milestone or _extract_section(roadmap, 'Current Milestone')}"]
        taste_decisions = (
            ["Decide whether to narrow scope before build"]
            if module_count >= 4
            else []
        )
        recommendation = (
            "Pause for scope confirmation" if taste_decisions else "Proceed on scope"
        )
        focus = "Milestone fit and scope pressure"
    elif args.role == "Architect":
        findings = [f"Modules in scope fit current architecture boundaries: {modules}"]
        auto_decisions = ["Keep the current repo-backed orchestration boundary"]
        taste_decisions = (
            ["Decide whether architecture coverage is sufficient for the current module set"]
            if module_count >= 4
            else []
        )
        recommendation = (
            "Pause for architecture confirmation" if taste_decisions else "Proceed on architecture"
        )
        focus = "Module boundaries and architectural fit"
    else:
        findings = [f"Exit criteria reviewed against quality bar: {exit_criteria}"]
        auto_decisions = ["Require verification before build"]
        taste_decisions = []
        lowered = exit_criteria.lower()
        if "test" not in lowered or "doc" not in lowered:
            taste_decisions.append(
                "Decide whether the plan should explicitly require tests and docs before build"
            )
        recommendation = (
            "Pause for quality confirmation" if taste_decisions else "Proceed on review"
        )
        focus = "Quality expectations and verification readiness"

    return SimpleNamespace(
        root=args.root,
        output=args.output,
        title=f"{args.role} review",
        role=args.role,
        focus=focus,
        finding=findings,
        auto_decision=auto_decisions,
        taste_decision=taste_decisions,
        recommendation=recommendation,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic role review pass")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--role", choices=["Product", "Architect", "Reviewer"], required=True)
    parser.add_argument("--plan-path", required=True)
    parser.add_argument("--output", required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    pass_args = _resolve_role_pass(args)
    return cmd_review_pass(pass_args)


if __name__ == "__main__":
    raise SystemExit(main())
