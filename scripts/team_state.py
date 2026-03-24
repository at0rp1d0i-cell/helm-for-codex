from __future__ import annotations

import argparse
from pathlib import Path


BOARD_PREAMBLE = "_This file can be updated manually or via `scripts/team_state.py board`._"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _resolve_path(root: Path, relpath: str) -> Path:
    path = Path(relpath)
    if path.is_absolute():
        return path
    return root / path


def _extract_board_section(content: str, header: str) -> list[str]:
    marker = f"## {header}\n\n"
    start = content.find(marker)
    if start == -1:
        return []
    start += len(marker)

    next_header = content.find("\n## ", start)
    if next_header == -1:
        section = content[start:]
    else:
        section = content[start:next_header]

    lines = [line for line in section.strip().splitlines() if line.strip()]
    return lines


def cmd_task_brief(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    content = (
        f"# Task Brief: {args.title}\n\n"
        "## Objective\n\n"
        f"{args.objective}\n\n"
        "## Scope\n\n"
        f"{args.scope}\n\n"
        "## Constraints\n\n"
        f"{args.constraints}\n\n"
        "## Relevant Decisions\n\n"
        f"{args.decisions}\n\n"
        "## Expected Output\n\n"
        f"{args.expected_output}\n\n"
        "## Writeback Target\n\n"
        f"{args.writeback}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_discovery_brief(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    content = (
        f"# Discovery Brief: {args.title}\n\n"
        "## Problem Signal\n\n"
        f"{args.problem}\n\n"
        "## Research Scope\n\n"
        f"{args.research_scope}\n\n"
        "## Open Questions\n\n"
        f"{args.open_questions}\n\n"
        "## Recommendation Target\n\n"
        f"{args.recommendation_target}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_plan_brief(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    content = (
        f"# Plan Brief: {args.title}\n\n"
        "## Goal\n\n"
        f"{args.goal}\n\n"
        "## Milestone\n\n"
        f"{args.milestone}\n\n"
        "## Modules In Scope\n\n"
        f"{args.modules}\n\n"
        "## Exit Criteria\n\n"
        f"{args.exit_criteria}\n\n"
        "## Writeback Target\n\n"
        f"{args.writeback}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_review_gate(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    review_passes = "\n".join(f"- {item}" for item in args.review_pass)
    auto_decisions = "\n".join(f"- {item}" for item in args.auto_decision)
    taste_decisions = (
        "\n".join(f"- {item}" for item in args.taste_decision)
        if args.taste_decision
        else "- none"
    )
    content = (
        f"# Review Gate: {args.title}\n\n"
        "## Inputs\n\n"
        f"{args.input_summary}\n\n"
        "## Review Passes\n\n"
        f"{review_passes}\n\n"
        "## Auto Decisions\n\n"
        f"{auto_decisions}\n\n"
        "## Taste Decisions\n\n"
        f"{taste_decisions}\n\n"
        "## Recommendation\n\n"
        f"{args.recommendation}\n\n"
        "## Approval Target\n\n"
        f"{args.approval_target}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_decision(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    consequence_lines = "\n".join(f"- {item}" for item in args.consequence)
    content = (
        f"# Decision: {args.title}\n\n"
        "## Context\n\n"
        f"{args.context}\n\n"
        "## Decision\n\n"
        f"{args.decision}\n\n"
        "## Consequences\n\n"
        f"{consequence_lines}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_board(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.path)
    existing = out.read_text() if out.exists() else ""
    active_items = args.active or _extract_board_section(existing, "Active Work")
    completed_items = args.completed or _extract_board_section(existing, "Completed")
    active_lines = "\n".join(f"- {item}" for item in active_items) if active_items else "- none"
    completed_lines = (
        "\n".join(f"- {item}" for item in completed_items) if completed_items else "- none"
    )
    content = (
        "# Execution Board\n\n"
        f"{BOARD_PREAMBLE}\n\n"
        "## Current Stage\n\n"
        f"{args.stage}\n\n"
        "## Active Work\n\n"
        f"{active_lines}\n\n"
        "## Completed\n\n"
        f"{completed_lines}\n"
    )
    _write(out, content)
    print(f"updated {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Team state utility")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    task_brief = subparsers.add_parser("task-brief", help="Create task brief markdown")
    task_brief.add_argument("--output", required=True)
    task_brief.add_argument("--title", required=True)
    task_brief.add_argument("--objective", required=True)
    task_brief.add_argument("--scope", required=True)
    task_brief.add_argument("--constraints", required=True)
    task_brief.add_argument("--decisions", required=True)
    task_brief.add_argument("--expected-output", required=True, dest="expected_output")
    task_brief.add_argument("--writeback", required=True)
    task_brief.set_defaults(func=cmd_task_brief)

    discovery_brief = subparsers.add_parser(
        "discovery-brief",
        help="Create discovery brief markdown",
    )
    discovery_brief.add_argument("--output", required=True)
    discovery_brief.add_argument("--title", required=True)
    discovery_brief.add_argument("--problem", required=True)
    discovery_brief.add_argument("--research-scope", required=True, dest="research_scope")
    discovery_brief.add_argument("--open-questions", required=True, dest="open_questions")
    discovery_brief.add_argument(
        "--recommendation-target",
        required=True,
        dest="recommendation_target",
    )
    discovery_brief.set_defaults(func=cmd_discovery_brief)

    plan_brief = subparsers.add_parser("plan-brief", help="Create plan brief markdown")
    plan_brief.add_argument("--output", required=True)
    plan_brief.add_argument("--title", required=True)
    plan_brief.add_argument("--goal", required=True)
    plan_brief.add_argument("--milestone", required=True)
    plan_brief.add_argument("--modules", required=True)
    plan_brief.add_argument("--exit-criteria", required=True, dest="exit_criteria")
    plan_brief.add_argument("--writeback", required=True)
    plan_brief.set_defaults(func=cmd_plan_brief)

    review_gate = subparsers.add_parser("review-gate", help="Create review gate markdown")
    review_gate.add_argument("--output", required=True)
    review_gate.add_argument("--title", required=True)
    review_gate.add_argument("--input-summary", required=True, dest="input_summary")
    review_gate.add_argument("--review-pass", action="append", default=[], required=True)
    review_gate.add_argument("--auto-decision", action="append", default=[], required=True)
    review_gate.add_argument("--taste-decision", action="append", default=[])
    review_gate.add_argument("--recommendation", required=True)
    review_gate.add_argument("--approval-target", required=True, dest="approval_target")
    review_gate.set_defaults(func=cmd_review_gate)

    decision = subparsers.add_parser("decision", help="Create decision markdown")
    decision.add_argument("--output", required=True)
    decision.add_argument("--title", required=True)
    decision.add_argument("--context", required=True)
    decision.add_argument("--decision", required=True)
    decision.add_argument("--consequence", action="append", default=[], required=True)
    decision.set_defaults(func=cmd_decision)

    board = subparsers.add_parser("board", help="Update execution board")
    board.add_argument("--path", required=True)
    board.add_argument("--stage", required=True)
    board.add_argument("--active", action="append", default=[])
    board.add_argument("--completed", action="append", default=[])
    board.set_defaults(func=cmd_board)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
