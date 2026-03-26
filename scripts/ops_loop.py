from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

from team_state import cmd_board, cmd_dispatch_packet, cmd_sprint_contract


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _resolve_path(root: Path, path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


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


def _first_nonempty_line(value: str) -> str:
    for line in value.splitlines():
        candidate = line.strip()
        if candidate:
            return candidate
    return ""


def _normalize_verification_status(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in {"passed", "failed"}:
        raise ValueError(f"Invalid verification status: {value}")
    return normalized


def _normalize_repo_backed_targets(targets: list[str], *, label: str) -> list[str]:
    normalized: list[str] = []
    for target in targets:
        value = target.strip()
        if not value:
            continue
        candidate = Path(value)
        if candidate.is_absolute() or not value.startswith("docs/"):
            raise ValueError(f"{label} must stay repo-backed under docs/: {target}")
        normalized.append(value)
    if not normalized:
        raise ValueError(f"{label} must include at least one repo-backed docs/ target.")
    return normalized


def _assert_consumed_sprint_contract(
    root: Path,
    sprint_contract_arg: str,
    implementation_report_path: Path,
) -> None:
    implementation_content = _read(implementation_report_path)
    consumed_contract = _extract_section(implementation_content, "Consumed Sprint Contract")
    if not consumed_contract:
        raise ValueError(
            "Implementation report consumed sprint contract is missing from the implementation report.",
        )

    consumed_contract_path = _resolve_path(root, consumed_contract)
    expected_contract_path = _resolve_path(root, sprint_contract_arg)
    if consumed_contract_path != expected_contract_path:
        raise ValueError(
            "Implementation report consumed sprint contract does not match the supplied sprint contract.",
        )


def _update_board(root: Path, path: str, stage: str, active: list[str]) -> int:
    board_args = SimpleNamespace(
        root=root,
        path=path,
        stage=stage,
        active=active,
        completed=[],
    )
    return cmd_board(board_args)


def _board_stage(root: Path, path: str) -> str:
    board = _read(root / path)
    return _extract_section(board, "Current Stage") if board else ""


def _write_dispatch_packet(
    *,
    root: Path,
    output: str,
    title: str,
    role: str,
    objective: str,
    consumed_artifact: list[str],
    constraints: str,
    expected_output: str,
    writeback_target: str,
    completion_command: str,
) -> int:
    dispatch_args = SimpleNamespace(
        root=root,
        output=output,
        title=title,
        role=role,
        objective=objective,
        consumed_artifact=consumed_artifact,
        constraints=constraints,
        expected_output=expected_output,
        writeback_target=writeback_target,
        completion_command=completion_command,
    )
    return cmd_dispatch_packet(dispatch_args)


def cmd_build(args: argparse.Namespace) -> int:
    sprint_args = SimpleNamespace(
        root=args.root,
        output=args.sprint_contract_path,
        title=args.title,
        planner=(
            f"{args.planner}\n\n"
            f"Implementation report path: {args.implementation_report_path}"
        ),
        generator=args.generator,
        evaluator=args.evaluator,
        scope=args.scope,
        acceptance=(
            f"{args.acceptance}\n\n"
            "Builder handoff output: "
            f"{args.implementation_report_path}"
        ),
    )
    rc = cmd_sprint_contract(sprint_args)
    if rc != 0:
        return rc

    rc = _write_dispatch_packet(
        root=args.root,
        output=args.builder_packet_path,
        title=f"{args.title} builder dispatch",
        role="Builder",
        objective=args.generator,
        consumed_artifact=[args.sprint_contract_path],
        constraints=f"{args.scope}\n\nAcceptance contract:\n{args.acceptance}",
        expected_output=f"Implementation report at {args.implementation_report_path}",
        writeback_target=args.implementation_report_path,
        completion_command=(
            "Return the implementation handoff by writing the implementation report to "
            f"{args.implementation_report_path}"
        ),
    )
    if rc != 0:
        return rc

    return _update_board(args.root, args.board_path, "build", [args.title])


def cmd_qa_prepare(args: argparse.Namespace) -> int:
    sprint_contract = _resolve_path(args.root, args.sprint_contract_path)
    implementation_report = _resolve_path(args.root, args.implementation_report_path)
    if not sprint_contract.exists():
        raise FileNotFoundError(f"Missing sprint contract: {sprint_contract}")
    if not implementation_report.exists():
        raise FileNotFoundError(f"Missing implementation report: {implementation_report}")
    _assert_consumed_sprint_contract(
        args.root,
        args.sprint_contract_path,
        implementation_report,
    )
    return _write_dispatch_packet(
        root=args.root,
        output=args.qa_packet_path,
        title=f"{args.title} QA dispatch",
        role="QA",
        objective="Validate the bounded task against the sprint contract and implementation report.",
        consumed_artifact=[args.sprint_contract_path, args.implementation_report_path],
        constraints=(
            f"Environment: {args.environment}\n\n"
            f"Scenarios:\n" + "\n".join(f"- {item}" for item in args.scenario)
        ),
        expected_output=f"QA report at {args.qa_report_path}",
        writeback_target=args.qa_report_path,
        completion_command=(
            "Return QA findings by writing the QA report to "
            f"{args.qa_report_path}"
        ),
    )


def cmd_qa(args: argparse.Namespace) -> int:
    sprint_contract = _resolve_path(args.root, args.sprint_contract_path)
    implementation_report = _resolve_path(args.root, args.implementation_report_path)
    if not sprint_contract.exists():
        raise FileNotFoundError(f"Missing sprint contract: {sprint_contract}")
    if not implementation_report.exists():
        raise FileNotFoundError(f"Missing implementation report: {implementation_report}")
    _assert_consumed_sprint_contract(
        args.root,
        args.sprint_contract_path,
        implementation_report,
    )
    verification_status = _normalize_verification_status(args.verification_status)

    issues = "\n".join(f"- {item}" for item in args.issue) if args.issue else "- none"
    scenarios = "\n".join(f"- {item}" for item in args.scenario)
    qa_report = _resolve_path(args.root, args.qa_report_path)
    content = (
        "# QA Report\n\n"
        "## Consumed Sprint Contract\n\n"
        f"{args.sprint_contract_path}\n\n"
        "## Consumed Implementation Report\n\n"
        f"{args.implementation_report_path}\n\n"
        "QA must validate the generator output against the consumed artifacts before board advancement.\n\n"
        "## Environment\n\n"
        f"{args.environment}\n\n"
        "## Scenarios Tested\n\n"
        f"{scenarios}\n\n"
        "## Issues Found\n\n"
        f"{issues}\n\n"
        "## Verification Status\n\n"
        f"{verification_status}\n"
    )
    _write(qa_report, content)

    next_stage = "build" if verification_status == "failed" else "qa"
    return _update_board(args.root, args.board_path, next_stage, [args.title])


def cmd_docs_sync(args: argparse.Namespace) -> int:
    implementation_report = _resolve_path(args.root, args.implementation_report_path)
    qa_report = _resolve_path(args.root, args.qa_report_path)
    if not implementation_report.exists():
        raise FileNotFoundError(f"Missing implementation report: {implementation_report}")
    if not qa_report.exists():
        raise FileNotFoundError(f"Missing QA report: {qa_report}")
    if _board_stage(args.root, args.board_path) != "qa":
        raise ValueError("Execution board must be at qa stage before docs-sync can proceed.")

    qa_content = _read(qa_report)
    consumed_implementation = _extract_section(qa_content, "Consumed Implementation Report")
    if not consumed_implementation:
        raise ValueError("QA report consumed implementation report is missing from the QA report.")

    consumed_implementation_path = _resolve_path(
        args.root,
        _first_nonempty_line(consumed_implementation),
    )
    expected_implementation_path = _resolve_path(args.root, args.implementation_report_path)
    if consumed_implementation_path != expected_implementation_path:
        raise ValueError(
            "QA report consumed implementation report does not match the supplied implementation report.",
        )
    verification_status = _normalize_verification_status(
        _first_nonempty_line(_extract_section(qa_content, "Verification Status")),
    )
    if verification_status != "passed":
        raise ValueError("QA report verification status must be passed before docs-sync can proceed.")

    docs_updated = "\n".join(f"- {item}" for item in args.docs_updated) if args.docs_updated else "- none"
    follow_ups = "\n".join(f"- {item}" for item in args.follow_up) if args.follow_up else "- none"
    canonical_targets = _normalize_repo_backed_targets(
        args.canonical_writeback,
        label="Canonical writeback targets",
    )
    canonical_writeback = "\n".join(f"- {item}" for item in canonical_targets)

    rc = _update_board(args.root, args.board_path, "docs-sync", [args.title])
    if rc != 0:
        return rc

    docs_sync_report = _resolve_path(args.root, args.docs_sync_report_path)
    content = (
        f"# Docs Sync Report: {args.title}\n\n"
        "## Consumed Implementation Report\n\n"
        f"{args.implementation_report_path}\n\n"
        "## Consumed QA Report\n\n"
        f"{args.qa_report_path}\n\n"
        "## Docs Updated\n\n"
        f"{docs_updated}\n\n"
        "## Canonical Writeback\n\n"
        f"{canonical_writeback}\n\n"
        "## Follow-Ups\n\n"
        f"{follow_ups}\n"
    )
    _write(docs_sync_report, content)
    return _update_board(args.root, args.board_path, "ship-ready", [args.title])


def cmd_docs_sync_prepare(args: argparse.Namespace) -> int:
    implementation_report = _resolve_path(args.root, args.implementation_report_path)
    qa_report = _resolve_path(args.root, args.qa_report_path)
    if not implementation_report.exists():
        raise FileNotFoundError(f"Missing implementation report: {implementation_report}")
    if not qa_report.exists():
        raise FileNotFoundError(f"Missing QA report: {qa_report}")
    qa_content = _read(qa_report)
    verification_status = _normalize_verification_status(
        _first_nonempty_line(_extract_section(qa_content, "Verification Status")),
    )
    if verification_status != "passed":
        raise ValueError("QA report verification status must be passed before docs-sync prepare can proceed.")

    canonical_targets = _normalize_repo_backed_targets(
        args.canonical_writeback,
        label="Canonical writeback targets",
    )
    docs_targets = args.docs_updated if args.docs_updated else ["none"]
    return _write_dispatch_packet(
        root=args.root,
        output=args.docs_sync_packet_path,
        title=f"{args.title} docs-sync dispatch",
        role="Docs Sync",
        objective="Sync canonical project state after QA passes without creating new scope.",
        consumed_artifact=[args.implementation_report_path, args.qa_report_path],
        constraints=(
            "Docs updated:\n"
            + "\n".join(f"- {item}" for item in docs_targets)
            + "\n\nCanonical writeback targets:\n"
            + "\n".join(f"- {item}" for item in canonical_targets)
        ),
        expected_output=f"Docs sync report at {args.docs_sync_report_path}",
        writeback_target=args.docs_sync_report_path,
        completion_command=(
            "Return docs-sync evidence by writing the docs-sync report to "
            f"{args.docs_sync_report_path}"
        ),
    )


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
    build.add_argument("--builder-packet-path", required=True, dest="builder_packet_path")
    build.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    build.set_defaults(func=cmd_build)

    qa_prepare = subparsers.add_parser(
        "qa-prepare",
        help="Create the QA dispatch packet once the implementation report exists",
    )
    qa_prepare.add_argument("--title", required=True)
    qa_prepare.add_argument("--sprint-contract-path", required=True, dest="sprint_contract_path")
    qa_prepare.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    qa_prepare.add_argument("--qa-packet-path", required=True, dest="qa_packet_path")
    qa_prepare.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    qa_prepare.add_argument("--environment", required=True)
    qa_prepare.add_argument("--scenario", action="append", default=[], required=True)
    qa_prepare.set_defaults(func=cmd_qa_prepare)

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

    docs_sync_prepare = subparsers.add_parser(
        "docs-sync-prepare",
        help="Create the docs-sync dispatch packet once QA has passed",
    )
    docs_sync_prepare.add_argument("--title", required=True)
    docs_sync_prepare.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    docs_sync_prepare.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    docs_sync_prepare.add_argument(
        "--docs-sync-packet-path",
        required=True,
        dest="docs_sync_packet_path",
    )
    docs_sync_prepare.add_argument(
        "--docs-sync-report-path",
        required=True,
        dest="docs_sync_report_path",
    )
    docs_sync_prepare.add_argument("--docs-updated", action="append", default=[], dest="docs_updated")
    docs_sync_prepare.add_argument(
        "--canonical-writeback",
        action="append",
        default=[],
        required=True,
        dest="canonical_writeback",
    )
    docs_sync_prepare.set_defaults(func=cmd_docs_sync_prepare)

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
