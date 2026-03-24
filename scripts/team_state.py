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
