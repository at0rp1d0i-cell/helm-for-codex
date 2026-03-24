from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

from team_state import (
    cmd_board,
    cmd_decision,
    cmd_discovery_brief,
    cmd_plan_brief,
    cmd_review_gate,
    cmd_review_pass as cmd_write_review_pass,
    cmd_task_brief,
)


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
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        if value and value.lower() != "none":
            items.append(value)
    return items


def _update_board(root: Path, path: str, stage: str, active: list[str]) -> int:
    board_args = SimpleNamespace(
        root=root,
        path=path,
        stage=stage,
        active=active,
        completed=[],
    )
    return cmd_board(board_args)


def cmd_record_review_pass(args: argparse.Namespace) -> int:
    pass_args = SimpleNamespace(
        root=args.root,
        output=args.pass_path,
        title=args.title,
        role=args.role,
        focus=args.focus,
        finding=args.finding,
        auto_decision=args.auto_decision,
        taste_decision=args.taste_decision,
        recommendation=args.recommendation,
    )
    return cmd_write_review_pass(pass_args)


def cmd_discover(args: argparse.Namespace) -> int:
    discovery_args = SimpleNamespace(
        root=args.root,
        output=args.discovery_path,
        title=args.title,
        problem=args.problem,
        research_scope=args.research_scope,
        open_questions=args.open_questions,
        recommendation_target=args.recommendation_target,
    )
    rc = cmd_discovery_brief(discovery_args)
    if rc != 0:
        return rc
    return _update_board(args.root, args.board_path, "discovery", [args.title])


def cmd_plan(args: argparse.Namespace) -> int:
    plan_args = SimpleNamespace(
        root=args.root,
        output=args.plan_path,
        title=args.title,
        goal=args.goal,
        milestone=args.milestone,
        modules=args.modules,
        exit_criteria=args.exit_criteria,
        writeback=args.writeback,
    )
    rc = cmd_plan_brief(plan_args)
    if rc != 0:
        return rc
    return _update_board(args.root, args.board_path, "plan", [args.title])


def cmd_delegate(args: argparse.Namespace) -> int:
    task_args = SimpleNamespace(
        root=args.root,
        output=args.task_path,
        title=args.title,
        objective=args.objective,
        scope=args.scope,
        constraints=args.constraints,
        decisions=args.decisions,
        expected_output=args.expected_output,
        writeback=args.writeback,
    )
    rc = cmd_task_brief(task_args)
    if rc != 0:
        return rc

    return _update_board(args.root, args.board_path, "build", [args.title])


def cmd_review(args: argparse.Namespace) -> int:
    review_passes = args.review_pass
    auto_decisions = args.auto_decision
    taste_decisions = args.taste_decision
    input_summary = args.input_summary
    recommendation = args.recommendation
    approval_target = args.approval_target

    if args.pass_path:
        review_passes = []
        auto_decisions = []
        taste_decisions = []
        for relpath in args.pass_path:
            content = _read(args.root / relpath)
            role = _extract_section(content, "Role") or "Unknown"
            role_recommendation = _extract_section(content, "Recommendation") or "No recommendation"
            review_passes.append(f"{role}: {role_recommendation}")
            auto_decisions.extend(_extract_list_section(content, "Auto Decisions"))
            taste_decisions.extend(_extract_list_section(content, "Taste Decisions"))

        input_summary = input_summary or f"Aggregated from {len(args.pass_path)} review passes"
        recommendation = recommendation or (
            "Resolve taste decisions before build"
            if taste_decisions
            else "Proceed to build"
        )
        approval_target = approval_target or ("user" if taste_decisions else "lead")

    review_args = SimpleNamespace(
        root=args.root,
        output=args.review_path,
        title=args.title,
        input_summary=input_summary,
        review_pass=review_passes,
        auto_decision=auto_decisions,
        taste_decision=taste_decisions,
        recommendation=recommendation,
        approval_target=approval_target,
    )
    rc = cmd_review_gate(review_args)
    if rc != 0:
        return rc

    stage = "approval-needed" if taste_decisions else "review"
    return _update_board(args.root, args.board_path, stage, [args.title])


def cmd_record_decision(args: argparse.Namespace) -> int:
    decision_args = SimpleNamespace(
        root=args.root,
        output=args.decision_path,
        title=args.title,
        context=args.context,
        decision=args.decision,
        consequence=args.consequence,
    )
    rc = cmd_decision(decision_args)
    if rc != 0 or not args.approval_needed:
        return rc

    return _update_board(args.root, args.board_path, "approval-needed", [])


def cmd_status(args: argparse.Namespace) -> int:
    brief = _read(args.root / "docs" / "project" / "PROJECT_BRIEF.md")
    board = _read(args.root / "docs" / "status" / "EXECUTION_BOARD.md")

    goal = _extract_section(brief, "Current Goal") or "unknown"
    stage = _extract_section(board, "Current Stage") or "unknown"
    active = _extract_section(board, "Active Work") or "- none"

    print(f"Current goal: {goal}")
    print(f"Stage: {stage}")
    print("Active work:")
    print(active)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal lead orchestration loop")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser(
        "discover",
        help="Create discovery brief and move board to discovery",
    )
    discover.add_argument("--title", required=True)
    discover.add_argument("--problem", required=True)
    discover.add_argument("--research-scope", required=True, dest="research_scope")
    discover.add_argument("--open-questions", required=True, dest="open_questions")
    discover.add_argument(
        "--recommendation-target",
        required=True,
        dest="recommendation_target",
    )
    discover.add_argument("--discovery-path", required=True)
    discover.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    discover.set_defaults(func=cmd_discover)

    plan = subparsers.add_parser("plan", help="Create plan brief and move board to plan")
    plan.add_argument("--title", required=True)
    plan.add_argument("--goal", required=True)
    plan.add_argument("--milestone", required=True)
    plan.add_argument("--modules", required=True)
    plan.add_argument("--exit-criteria", required=True, dest="exit_criteria")
    plan.add_argument("--writeback", required=True)
    plan.add_argument("--plan-path", required=True)
    plan.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    plan.set_defaults(func=cmd_plan)

    delegate = subparsers.add_parser("delegate", help="Create task brief and move board to build")
    delegate.add_argument("--title", required=True)
    delegate.add_argument("--objective", required=True)
    delegate.add_argument("--scope", required=True)
    delegate.add_argument("--constraints", required=True)
    delegate.add_argument("--decisions", required=True)
    delegate.add_argument("--expected-output", required=True, dest="expected_output")
    delegate.add_argument("--writeback", required=True)
    delegate.add_argument("--task-path", required=True)
    delegate.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    delegate.set_defaults(func=cmd_delegate)

    review_pass = subparsers.add_parser("review-pass", help="Create review pass artifact")
    review_pass.add_argument("--title", required=True)
    review_pass.add_argument("--role", required=True)
    review_pass.add_argument("--focus", required=True)
    review_pass.add_argument("--finding", action="append", default=[], required=True)
    review_pass.add_argument("--auto-decision", action="append", default=[], required=True)
    review_pass.add_argument("--taste-decision", action="append", default=[])
    review_pass.add_argument("--recommendation", required=True)
    review_pass.add_argument("--pass-path", required=True)
    review_pass.set_defaults(func=cmd_record_review_pass)

    review = subparsers.add_parser("review", help="Create review gate and update board")
    review.add_argument("--title", required=True)
    review.add_argument("--input-summary", dest="input_summary")
    review.add_argument("--review-pass", action="append", default=[])
    review.add_argument("--auto-decision", action="append", default=[])
    review.add_argument("--taste-decision", action="append", default=[])
    review.add_argument("--recommendation")
    review.add_argument("--approval-target", dest="approval_target")
    review.add_argument("--pass-path", action="append", default=[])
    review.add_argument("--review-path", required=True)
    review.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    review.set_defaults(func=cmd_review)

    decision = subparsers.add_parser("decision", help="Record decision and optionally gate progress")
    decision.add_argument("--title", required=True)
    decision.add_argument("--context", required=True)
    decision.add_argument("--decision", required=True)
    decision.add_argument("--consequence", action="append", default=[], required=True)
    decision.add_argument("--decision-path", required=True)
    decision.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    decision.add_argument("--approval-needed", action="store_true")
    decision.set_defaults(func=cmd_record_decision)

    status = subparsers.add_parser("status", help="Print compact lead status summary")
    status.set_defaults(func=cmd_status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
