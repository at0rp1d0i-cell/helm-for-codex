from __future__ import annotations

import argparse
from types import SimpleNamespace
from pathlib import Path

from team_state import cmd_board, cmd_decision, cmd_task_brief


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

    board_args = SimpleNamespace(
        root=args.root,
        path=args.board_path,
        stage="build",
        active=[args.title],
        completed=[],
    )
    return cmd_board(board_args)


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

    board_args = SimpleNamespace(
        root=args.root,
        path=args.board_path,
        stage="approval-needed",
        active=[],
        completed=[],
    )
    return cmd_board(board_args)


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
