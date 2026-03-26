from __future__ import annotations

import argparse
from pathlib import Path

from lead_loop import cmd_build, cmd_docs_sync, cmd_qa


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Explicit ops orchestration loop")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser(
        "build",
        help="Create sprint contract for bounded builder kickoff and move board to build",
    )
    build.add_argument("--title", required=True)
    build.add_argument("--planner", required=True)
    build.add_argument("--generator", required=True)
    build.add_argument("--evaluator", required=True)
    build.add_argument("--scope", required=True)
    build.add_argument("--acceptance", required=True)
    build.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    build.add_argument("--sprint-contract-path", required=True, dest="sprint_contract_path")
    build.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    build.set_defaults(func=cmd_build)

    qa = subparsers.add_parser(
        "qa",
        help="Write the canonical QA report and move the board to qa or back to build",
    )
    qa.add_argument("--title", required=True)
    qa.add_argument("--sprint-contract-path", required=True, dest="sprint_contract_path")
    qa.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    qa.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    qa.add_argument("--environment", required=True)
    qa.add_argument("--scenario", action="append", default=[], required=True)
    qa.add_argument("--issue", action="append", default=[])
    qa.add_argument("--verification-status", required=True, dest="verification_status")
    qa.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    qa.set_defaults(func=cmd_qa)

    docs_sync = subparsers.add_parser(
        "docs-sync",
        help="Write the canonical docs-sync report and move the board to ship-ready",
    )
    docs_sync.add_argument("--title", required=True)
    docs_sync.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    docs_sync.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    docs_sync.add_argument("--docs-sync-report-path", required=True, dest="docs_sync_report_path")
    docs_sync.add_argument("--docs-updated", action="append", default=[], dest="docs_updated")
    docs_sync.add_argument(
        "--canonical-writeback",
        action="append",
        default=[],
        required=True,
        dest="canonical_writeback",
    )
    docs_sync.add_argument("--follow-up", action="append", default=[], dest="follow_up")
    docs_sync.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    docs_sync.set_defaults(func=cmd_docs_sync)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
