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


def _resolve_office_hours_pass(args: argparse.Namespace) -> SimpleNamespace:
    brief = _read(args.root / args.brief_path)

    problem = _extract_section(brief, "Problem Statement")
    target_user = _extract_section(brief, "Target User Or Operator")
    proposal = _extract_section(brief, "Current Proposal")
    constraints = _extract_section(brief, "Constraints")
    success_criteria = _extract_section(brief, "Success Criteria")
    build_vs_buy = _extract_section(brief, "Build vs Buy Context")
    assumptions = _extract_section(brief, "Assumptions To Challenge")
    challenge_count = len([line for line in assumptions.splitlines() if line.strip().startswith("- ")])

    if args.role == "Product":
        findings = [
            f"Target user pressure: {target_user or 'missing target user'}",
            f"Current proposal pressure: {proposal or 'missing proposal'}",
        ]
        auto_decisions = ["Force the next plan to name one primary user and one success metric."]
        taste_decisions = []
        if challenge_count >= 3 or "all" in proposal.lower() or "platform" in proposal.lower():
            taste_decisions.append("Decide whether to narrow scope to a single user-facing milestone before planning.")
        recommendation = "Reframe around a tighter milestone" if taste_decisions else "Proceed with product framing"
        focus = "Problem framing, scope pressure, and user value"
    elif args.role == "Design":
        findings = [
            f"Primary flow pressure: {proposal or problem or 'missing problem framing'}",
            f"Success-criteria pressure: {success_criteria or 'missing success criteria'}",
        ]
        auto_decisions = ["Force the next plan to describe one critical user or operator flow."]
        taste_decisions = []
        lowered = f"{proposal}\n{problem}".lower()
        if not any(token in lowered for token in ["flow", "screen", "ui", "interface", "operator path", "journey"]):
            taste_decisions.append("Decide whether the first milestone needs an explicit primary flow before planning.")
        recommendation = "Reframe around one critical flow" if taste_decisions else "Proceed with design framing"
        focus = "Comprehension, workflow clarity, and interaction pressure"
    else:
        findings = [
            f"Build-vs-buy pressure: {build_vs_buy or 'missing build-vs-buy context'}",
            f"Constraint pressure: {constraints or 'missing constraints'}",
        ]
        auto_decisions = ["Keep build-vs-buy posture explicit in the next plan brief."]
        taste_decisions = []
        lowered = build_vs_buy.lower()
        if "from scratch" in lowered or "custom" in lowered or "reinvent" in lowered:
            taste_decisions.append("Decide whether building from scratch is justified before planning.")
        recommendation = "Pause for architecture tradeoff confirmation" if taste_decisions else "Proceed with architecture framing"
        focus = "Technical posture, coupling risk, and build-vs-buy pressure"

    return SimpleNamespace(
        root=args.root,
        output=args.output,
        title=f"{args.role} office-hours challenge",
        role=args.role,
        focus=focus,
        finding=findings,
        auto_decision=auto_decisions,
        taste_decision=taste_decisions,
        recommendation=recommendation,
    )


def _resolve_role_pass(args: argparse.Namespace) -> SimpleNamespace:
    if args.mode == "office-hours":
        return _resolve_office_hours_pass(args)

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
    parser.add_argument("--mode", choices=["plan-review", "office-hours"], default="plan-review")
    parser.add_argument("--role", choices=["Product", "Architect", "Reviewer", "Design"], required=True)
    parser.add_argument("--plan-path")
    parser.add_argument("--brief-path", dest="brief_path")
    parser.add_argument("--output", required=True)
    return parser


def main_from_args(args: argparse.Namespace) -> int:
    args.root = args.root.resolve()
    if args.mode == "plan-review" and not args.plan_path:
        raise ValueError("--plan-path is required for plan-review mode")
    if args.mode == "office-hours" and not args.brief_path:
        raise ValueError("--brief-path is required for office-hours mode")
    pass_args = _resolve_role_pass(args)
    return cmd_review_pass(pass_args)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return main_from_args(args)


if __name__ == "__main__":
    raise SystemExit(main())
