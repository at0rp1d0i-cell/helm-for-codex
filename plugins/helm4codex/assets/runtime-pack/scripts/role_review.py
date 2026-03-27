from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

from team_state import cmd_review_pass, cmd_sprint_pass


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


def _extract_list_section(content: str, heading: str) -> list[str]:
    section = _extract_section(content, heading)
    if not section:
        return []
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def _count_modules(modules: str) -> int:
    return len([item.strip() for item in modules.split(",") if item.strip()])


def _resolve_office_hours_pass(args: argparse.Namespace) -> SimpleNamespace:
    brief = _read(args.root / args.brief_path)
    research = _read(args.root / args.research_report_path) if args.research_report_path else ""

    problem = _extract_section(brief, "Problem Statement")
    target_user = _extract_section(brief, "Target User Or Operator")
    proposal = _extract_section(brief, "Current Proposal")
    constraints = _extract_section(brief, "Constraints")
    success_criteria = _extract_section(brief, "Success Criteria")
    build_vs_buy = _extract_section(brief, "Build vs Buy Context")
    assumptions = _extract_section(brief, "Assumptions To Challenge")
    top_options = _extract_list_section(research, "Top Options")
    research_recommendation = _extract_section(research, "Recommendation")
    research_posture = _extract_section(research, "Build vs Buy Posture")
    open_risks = _extract_list_section(research, "Open Risks")
    challenge_count = len([line for line in assumptions.splitlines() if line.strip().startswith("- ")])

    if args.role == "Product":
        findings = [
            f"Target user pressure: {target_user or 'missing target user'}",
            f"Current proposal pressure: {proposal or 'missing proposal'}",
        ]
        if top_options:
            findings.append(f"Research baseline pressure: {top_options[0]}")
        auto_decisions = ["Force the next plan to name one primary user and one success metric."]
        taste_decisions = []
        if top_options:
            auto_decisions.append("Carry the strongest external baseline into the next plan brief.")
        if (
            challenge_count >= 3
            or "all" in proposal.lower()
            or "platform" in proposal.lower()
            or ("defer broader platform scope" in research_recommendation.lower())
        ):
            taste_decisions.append("Decide whether to narrow scope to a single user-facing milestone before planning.")
        recommendation = "Reframe around a tighter milestone" if taste_decisions else "Proceed with product framing"
        focus = "Problem framing, scope pressure, and user value"
    elif args.role == "Design":
        findings = [
            f"Primary flow pressure: {proposal or problem or 'missing problem framing'}",
            f"Success-criteria pressure: {success_criteria or 'missing success criteria'}",
        ]
        if open_risks:
            findings.append(f"Research risk pressure: {open_risks[0]}")
        auto_decisions = ["Force the next plan to describe one critical user or operator flow."]
        taste_decisions = []
        lowered = f"{proposal}\n{problem}".lower()
        risk_lowered = "\n".join(open_risks).lower()
        if not any(token in lowered for token in ["flow", "screen", "ui", "interface", "operator path", "journey"]) or "under-specified" in risk_lowered:
            taste_decisions.append("Decide whether the first milestone needs an explicit primary flow before planning.")
        recommendation = "Reframe around one critical flow" if taste_decisions else "Proceed with design framing"
        focus = "Comprehension, workflow clarity, and interaction pressure"
    else:
        findings = [
            f"Build-vs-buy pressure: {build_vs_buy or 'missing build-vs-buy context'}",
            f"Constraint pressure: {constraints or 'missing constraints'}",
        ]
        if research_posture:
            findings.append(f"Research posture pressure: {research_posture}")
        auto_decisions = ["Keep build-vs-buy posture explicit in the next plan brief."]
        taste_decisions = []
        lowered = f"{build_vs_buy}\n{research_posture}".lower()
        if "bounded local build" in lowered:
            auto_decisions.append("Carry forward the bounded local build posture into planning.")
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


def _resolve_sprint_contract_pass(args: argparse.Namespace) -> SimpleNamespace:
    proposal = _read(args.root / args.proposal_path)
    objective = _extract_section(proposal, "Objective")
    scope = _extract_section(proposal, "Scope")
    acceptance = _extract_section(proposal, "Acceptance Criteria")
    implementation_report_target = _extract_section(proposal, "Implementation Report Target")
    evidence_posture = _extract_section(proposal, "Evidence Posture")
    lowered_scope = scope.lower()
    lowered_acceptance = acceptance.lower()
    lowered_evidence = evidence_posture.lower()

    if args.role == "Builder":
        findings = [
            f"Scope pressure: {scope or 'missing scope'}",
            f"Implementation handoff target: {implementation_report_target or 'missing implementation-report target'}",
        ]
        auto_decisions = ["Keep the implementation-report target explicit in the final sprint contract."]
        blocking_issues: list[str] = []
        if any(token in lowered_scope for token in ["all", "everything", "platform", "every workflow"]):
            blocking_issues.append("Scope is too broad for one bounded implementation slice.")
        if "bounded" not in lowered_scope and "one" not in lowered_scope:
            blocking_issues.append("Scope does not clearly describe a bounded first slice.")
        recommendation = (
            "Reframe scope before build"
            if blocking_issues
            else "Proceed to sprint contract materialization"
        )
        focus = "Implementation feasibility and bounded delivery pressure"
    else:
        findings = [
            f"Acceptance pressure: {acceptance or 'missing acceptance criteria'}",
            f"Evidence posture: {evidence_posture or 'missing evidence posture'}",
        ]
        auto_decisions = ["Keep verification and evidence posture explicit in the final sprint contract."]
        blocking_issues = []
        if not any(token in lowered_acceptance for token in ["test", "verify", "report", "qa", "evidence"]):
            blocking_issues.append("Acceptance criteria are not observable enough for QA.")
        if not any(token in lowered_evidence for token in ["scenario", "report", "evidence", "manifest", "targeted"]):
            blocking_issues.append("Evidence posture is too weak to support evaluator handoff.")
        recommendation = (
            "Tighten acceptance and evidence posture before build"
            if blocking_issues
            else "Proceed to sprint contract materialization"
        )
        focus = "Evaluability, verification readiness, and evidence pressure"

    return SimpleNamespace(
        root=args.root,
        output=args.output,
        title=f"{args.role} sprint pass",
        role=args.role,
        focus=focus,
        finding=findings,
        auto_decision=auto_decisions,
        blocking_issue=blocking_issues,
        recommendation=recommendation,
    )


def _resolve_role_pass(args: argparse.Namespace) -> SimpleNamespace:
    if args.mode == "office-hours":
        return _resolve_office_hours_pass(args)
    if args.mode == "sprint-contract":
        return _resolve_sprint_contract_pass(args)

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
    parser.add_argument("--mode", choices=["plan-review", "office-hours", "sprint-contract"], default="plan-review")
    parser.add_argument("--role", choices=["Product", "Architect", "Reviewer", "Design", "Builder", "QA"], required=True)
    parser.add_argument("--plan-path")
    parser.add_argument("--brief-path", dest="brief_path")
    parser.add_argument("--research-report-path", dest="research_report_path")
    parser.add_argument("--proposal-path", dest="proposal_path")
    parser.add_argument("--output", required=True)
    return parser


def main_from_args(args: argparse.Namespace) -> int:
    args.root = args.root.resolve()
    if args.mode == "plan-review" and not args.plan_path:
        raise ValueError("--plan-path is required for plan-review mode")
    if args.mode == "office-hours" and not args.brief_path:
        raise ValueError("--brief-path is required for office-hours mode")
    if args.mode == "sprint-contract" and not args.proposal_path:
        raise ValueError("--proposal-path is required for sprint-contract mode")
    pass_args = _resolve_role_pass(args)
    if args.mode == "sprint-contract":
        return cmd_sprint_pass(pass_args)
    return cmd_review_pass(pass_args)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return main_from_args(args)


if __name__ == "__main__":
    raise SystemExit(main())
