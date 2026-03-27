from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

from bridge_runner import cmd_render as cmd_render_bridge_launch
from role_bridge import resolve_role
from team_state import (
    cmd_board,
    cmd_dispatch_packet,
    cmd_invocation_spec,
    cmd_qa_evidence,
    cmd_qa_report,
    cmd_release_gate as cmd_write_release_gate,
    cmd_sprint_contract,
)


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _resolve_path(root: Path, path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def _default_invocation_spec_path(packet_path: str) -> str:
    packet = Path(packet_path)
    if packet.parent.name.endswith("packets"):
        return str(packet.parent.parent / "invocation-specs" / packet.name)
    return str(packet.with_name(f"{packet.stem}-invocation{packet.suffix or '.md'}"))


def _default_qa_evidence_path(qa_report_path: str) -> str:
    report = Path(qa_report_path)
    suffix = report.suffix or ".md"
    name = report.name
    if name.startswith("qa-report"):
        evidence_name = name.replace("qa-report", "qa-evidence", 1)
    else:
        evidence_name = f"{report.stem}-evidence{suffix}"
    return str(report.with_name(evidence_name))


def _default_qa_artifact_root(qa_evidence_path: str) -> str:
    evidence = Path(qa_evidence_path)
    stem = evidence.stem
    if stem.startswith("qa-evidence-"):
        stem = stem[len("qa-evidence-") :]
    elif stem.endswith("-evidence"):
        stem = stem[: -len("-evidence")]

    if evidence.parent.name == "plans":
        return str(evidence.parent / "qa-artifacts" / stem)
    return str(evidence.parent / f"{stem}-artifacts")


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


def _normalize_browser_evidence_status(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in {"placeholder", "captured", "not-requested"}:
        raise ValueError(f"Invalid browser evidence status: {value}")
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


def _qa_placeholder_contract(artifact_root: str, scenarios: list[str]) -> tuple[list[str], list[str]]:
    screenshot_placeholders: list[str] = []
    artifact_placeholders: list[str] = []
    for index, scenario in enumerate(scenarios, start=1):
        key = f"scenario-{index:02d}"
        screenshot_placeholders.append(
            f"{artifact_root}/screenshots/{key}.png | {scenario}",
        )
        artifact_placeholders.append(
            f"{artifact_root}/dom/{key}.md | DOM snapshot placeholder for {scenario}",
        )
        artifact_placeholders.append(
            f"{artifact_root}/console/{key}.log | Console log placeholder for {scenario}",
        )
    return screenshot_placeholders, artifact_placeholders


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
    invocation_spec_output: str | None,
    title: str,
    logical_role: str,
    objective: str,
    consumed_artifact: list[str],
    constraints: str,
    expected_output: str,
    writeback_target: str,
    completion_command: str,
) -> int:
    resolved_role = resolve_role(root, logical_role)
    dispatch_args = SimpleNamespace(
        root=root,
        output=output,
        title=title,
        role=resolved_role["display_name"],
        logical_role=resolved_role["logical_role"],
        bridge_agent_type=resolved_role["agent_type"],
        bridge_model=resolved_role["model"],
        bridge_reasoning_effort=resolved_role["reasoning_effort"],
        role_skill=resolved_role["skill"],
        role_metadata=resolved_role["metadata"],
        role_writeback_target=resolved_role["writeback_target"],
        role_writeback_command=resolved_role["writeback_command"],
        objective=objective,
        consumed_artifact=consumed_artifact,
        constraints=constraints,
        expected_output=expected_output,
        writeback_target=writeback_target,
        completion_command=completion_command,
    )
    rc = cmd_dispatch_packet(dispatch_args)
    if rc != 0:
        return rc

    invocation_args = SimpleNamespace(
        root=root,
        output=invocation_spec_output or _default_invocation_spec_path(output),
        title=f"{title} invocation",
        role=resolved_role["display_name"],
        logical_role=resolved_role["logical_role"],
        source_packet=output,
        bridge_agent_type=resolved_role["agent_type"],
        bridge_model=resolved_role["model"],
        bridge_reasoning_effort=resolved_role["reasoning_effort"],
        runtime_skill=resolved_role["skill"],
        metadata=resolved_role["metadata"],
        consumed_artifact=[output, *consumed_artifact],
        expected_writeback_target=writeback_target,
        expected_writeback_command=completion_command,
    )
    return cmd_invocation_spec(invocation_args)


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
        invocation_spec_output=args.builder_invocation_spec_path,
        title=f"{args.title} builder dispatch",
        logical_role="implementation-worker",
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
    browser_evidence_status = _normalize_browser_evidence_status(args.browser_evidence_status)
    qa_evidence_path = args.qa_evidence_path or _default_qa_evidence_path(args.qa_report_path)
    qa_evidence_path = _normalize_repo_backed_targets(
        [qa_evidence_path],
        label="QA evidence path",
    )[0]
    artifact_root = _default_qa_artifact_root(qa_evidence_path)
    screenshot_placeholders, artifact_placeholders = _qa_placeholder_contract(
        artifact_root,
        args.scenario,
    )
    return _write_dispatch_packet(
        root=args.root,
        output=args.qa_packet_path,
        invocation_spec_output=args.qa_invocation_spec_path,
        title=f"{args.title} QA dispatch",
        logical_role="qa-runner",
        objective="Validate the bounded task against the sprint contract and implementation report.",
        consumed_artifact=[args.sprint_contract_path, args.implementation_report_path],
        constraints=(
            f"Environment: {args.environment}\n\n"
            + "Scenarios:\n"
            + "\n".join(f"- {item}" for item in args.scenario)
            + "\n\nEvidence contract:\n"
            + f"- qa_report: {args.qa_report_path}\n"
            + f"- qa_evidence: {qa_evidence_path}\n"
            + f"- browser_evidence_status: {browser_evidence_status}\n"
            + f"- evidence_mode: {args.evidence_mode}\n\n"
            + "Screenshot placeholders:\n"
            + "\n".join(f"- {item}" for item in screenshot_placeholders)
            + "\n\nAdditional artifact placeholders:\n"
            + "\n".join(f"- {item}" for item in artifact_placeholders)
        ),
        expected_output=(
            f"QA report at {args.qa_report_path} plus QA evidence at {qa_evidence_path}"
        ),
        writeback_target=args.qa_report_path,
        completion_command=(
            "Return QA findings by writing the QA report to "
            f"{args.qa_report_path} and the QA evidence artifact to {qa_evidence_path}"
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
    browser_evidence_status = _normalize_browser_evidence_status(args.browser_evidence_status)
    qa_evidence_path = args.qa_evidence_path or _default_qa_evidence_path(args.qa_report_path)
    qa_evidence_path = _normalize_repo_backed_targets(
        [qa_evidence_path],
        label="QA evidence path",
    )[0]
    artifact_root = _default_qa_artifact_root(qa_evidence_path)
    screenshot_placeholders, artifact_placeholders = _qa_placeholder_contract(
        artifact_root,
        args.scenario,
    )
    qa_dispatch_packet = "none"
    if args.qa_packet_path:
        qa_packet = _resolve_path(args.root, args.qa_packet_path)
        if not qa_packet.exists():
            raise FileNotFoundError(f"Missing QA dispatch packet: {qa_packet}")
        qa_dispatch_packet = args.qa_packet_path

    report_args = SimpleNamespace(
        root=args.root,
        output=args.qa_report_path,
        title=args.title,
        sprint_contract=args.sprint_contract_path,
        implementation_report=args.implementation_report_path,
        qa_dispatch_packet=qa_dispatch_packet,
        evidence_report=qa_evidence_path,
        browser_evidence_status=browser_evidence_status,
        environment=args.environment,
        scenario=args.scenario,
        issue=args.issue,
        verification_status=verification_status,
    )
    rc = cmd_qa_report(report_args)
    if rc != 0:
        return rc

    evidence_notes = list(args.evidence_note)
    if not evidence_notes:
        evidence_notes.append(
            "Browser runtime capture is not wired yet; placeholder paths reserve the evidence contract.",
        )
    evidence_args = SimpleNamespace(
        root=args.root,
        output=qa_evidence_path,
        title=args.title,
        qa_report=args.qa_report_path,
        qa_dispatch_packet=qa_dispatch_packet,
        sprint_contract=args.sprint_contract_path,
        implementation_report=args.implementation_report_path,
        evidence_mode=args.evidence_mode,
        browser_evidence_status=browser_evidence_status,
        environment=args.environment,
        scenario=args.scenario,
        screenshot_placeholder=screenshot_placeholders,
        artifact_placeholder=artifact_placeholders,
        note=evidence_notes,
    )
    rc = cmd_qa_evidence(evidence_args)
    if rc != 0:
        return rc

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
        invocation_spec_output=args.docs_sync_invocation_spec_path,
        title=f"{args.title} docs-sync dispatch",
        logical_role="docs-sync",
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


def cmd_bridge_launch(args: argparse.Namespace) -> int:
    render_args = SimpleNamespace(
        root=args.root,
        packet_path=args.packet_path,
        invocation_spec_path=args.invocation_spec_path or _default_invocation_spec_path(args.packet_path),
        output=args.output,
    )
    return cmd_render_bridge_launch(render_args)


def cmd_bridge_receipt(args: argparse.Namespace) -> int:
    from bridge_runner import cmd_receipt as cmd_write_bridge_receipt

    receipt_args = SimpleNamespace(
        root=args.root,
        packet_path=args.packet_path,
        invocation_spec_path=args.invocation_spec_path,
        launch_payload_path=args.launch_payload_path,
        output=args.output,
        title=args.title,
        execution_status=args.execution_status,
        writeback_status=args.writeback_status,
        specialist_note=args.specialist_note,
        follow_up=args.follow_up,
    )
    return cmd_write_bridge_receipt(receipt_args)


def cmd_release_prepare(args: argparse.Namespace) -> int:
    implementation_report = _resolve_path(args.root, args.implementation_report_path)
    qa_report = _resolve_path(args.root, args.qa_report_path)
    docs_sync_report = _resolve_path(args.root, args.docs_sync_report_path)
    if not implementation_report.exists():
        raise FileNotFoundError(f"Missing implementation report: {implementation_report}")
    if not qa_report.exists():
        raise FileNotFoundError(f"Missing QA report: {qa_report}")
    if not docs_sync_report.exists():
        raise FileNotFoundError(f"Missing docs sync report: {docs_sync_report}")
    if _board_stage(args.root, args.board_path) != "ship-ready":
        raise ValueError("Execution board must be at ship-ready stage before release-prepare can proceed.")

    checklist = "\n".join(f"- {item}" for item in args.readiness_checklist)
    return _write_dispatch_packet(
        root=args.root,
        output=args.release_packet_path,
        invocation_spec_output=args.release_invocation_spec_path,
        title=f"{args.title} release dispatch",
        logical_role="release-manager",
        objective="Evaluate release readiness for the bounded slice without expanding into deploy automation.",
        consumed_artifact=[
            args.implementation_report_path,
            args.qa_report_path,
            args.docs_sync_report_path,
        ],
        constraints=(
            "Release readiness checklist:\n"
            + checklist
            + "\n\nEvidence-first release gate sections:\n"
            + "- verification status\n"
            + "- coverage posture\n"
            + "- version/changelog readiness\n"
            + "- merge/PR prep\n\nRelease gate output:\n"
            + args.release_gate_path
        ),
        expected_output=f"Release gate at {args.release_gate_path}",
        writeback_target=args.release_gate_path,
        completion_command=(
            "Return release readiness by writing the release gate to "
            f"{args.release_gate_path}"
        ),
    )


def cmd_release_gate(args: argparse.Namespace) -> int:
    implementation_report = _resolve_path(args.root, args.implementation_report_path)
    qa_report = _resolve_path(args.root, args.qa_report_path)
    docs_sync_report = _resolve_path(args.root, args.docs_sync_report_path)
    if not implementation_report.exists():
        raise FileNotFoundError(f"Missing implementation report: {implementation_report}")
    if not qa_report.exists():
        raise FileNotFoundError(f"Missing QA report: {qa_report}")
    if not docs_sync_report.exists():
        raise FileNotFoundError(f"Missing docs sync report: {docs_sync_report}")
    if _board_stage(args.root, args.board_path) != "ship-ready":
        raise ValueError("Execution board must be at ship-ready stage before release-gate can proceed.")
    if args.verdict not in {"go", "no-go"}:
        raise ValueError("Release verdict must be go or no-go.")

    release_args = SimpleNamespace(
        root=args.root,
        output=args.release_gate_path,
        title=args.title,
        implementation_report=args.implementation_report_path,
        qa_report=args.qa_report_path,
        docs_sync_report=args.docs_sync_report_path,
        verification_status=args.verification_status,
        coverage_posture=args.coverage_posture,
        version_changelog_readiness=args.version_changelog_readiness,
        merge_pr_prep=args.merge_pr_prep,
        readiness_checklist=args.readiness_checklist,
        blocking_risk=args.blocking_risk,
        mitigation=args.mitigation,
        verdict=args.verdict,
        recommendation=args.recommendation,
    )
    rc = cmd_write_release_gate(release_args)
    if rc != 0:
        return rc
    return _update_board(args.root, args.board_path, "ship-ready", [args.title])


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
    build.add_argument(
        "--builder-invocation-spec-path",
        dest="builder_invocation_spec_path",
    )
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
    qa_prepare.add_argument(
        "--qa-invocation-spec-path",
        dest="qa_invocation_spec_path",
    )
    qa_prepare.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    qa_prepare.add_argument("--qa-evidence-path", dest="qa_evidence_path")
    qa_prepare.add_argument("--environment", required=True)
    qa_prepare.add_argument(
        "--browser-evidence-status",
        default="placeholder",
        dest="browser_evidence_status",
    )
    qa_prepare.add_argument("--evidence-mode", default="browser-placeholder", dest="evidence_mode")
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
    qa.add_argument("--qa-packet-path", dest="qa_packet_path")
    qa.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    qa.add_argument("--qa-evidence-path", dest="qa_evidence_path")
    qa.add_argument("--environment", required=True)
    qa.add_argument(
        "--browser-evidence-status",
        default="placeholder",
        dest="browser_evidence_status",
    )
    qa.add_argument("--evidence-mode", default="browser-placeholder", dest="evidence_mode")
    qa.add_argument("--scenario", action="append", default=[], required=True)
    qa.add_argument("--issue", action="append", default=[])
    qa.add_argument("--evidence-note", action="append", default=[], dest="evidence_note")
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
        "--docs-sync-invocation-spec-path",
        dest="docs_sync_invocation_spec_path",
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

    release_prepare = subparsers.add_parser(
        "release-prepare",
        help="Create the release-manager dispatch packet once docs-sync has completed",
    )
    release_prepare.add_argument("--title", required=True)
    release_prepare.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    release_prepare.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    release_prepare.add_argument(
        "--docs-sync-report-path",
        required=True,
        dest="docs_sync_report_path",
    )
    release_prepare.add_argument("--release-packet-path", required=True, dest="release_packet_path")
    release_prepare.add_argument(
        "--release-invocation-spec-path",
        dest="release_invocation_spec_path",
    )
    release_prepare.add_argument("--release-gate-path", required=True, dest="release_gate_path")
    release_prepare.add_argument(
        "--readiness-checklist",
        action="append",
        default=[],
        required=True,
        dest="readiness_checklist",
    )
    release_prepare.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    release_prepare.set_defaults(func=cmd_release_prepare)

    release_gate = subparsers.add_parser(
        "release-gate",
        help="Write the canonical release gate while keeping the board at ship-ready",
    )
    release_gate.add_argument("--title", required=True)
    release_gate.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    release_gate.add_argument("--qa-report-path", required=True, dest="qa_report_path")
    release_gate.add_argument(
        "--docs-sync-report-path",
        required=True,
        dest="docs_sync_report_path",
    )
    release_gate.add_argument("--release-gate-path", required=True, dest="release_gate_path")
    release_gate.add_argument(
        "--verification-status",
        action="append",
        default=[],
        required=True,
        dest="verification_status",
    )
    release_gate.add_argument("--coverage-posture", required=True, dest="coverage_posture")
    release_gate.add_argument(
        "--version-changelog-readiness",
        required=True,
        dest="version_changelog_readiness",
    )
    release_gate.add_argument("--merge-pr-prep", required=True, dest="merge_pr_prep")
    release_gate.add_argument(
        "--readiness-checklist",
        action="append",
        default=[],
        required=True,
        dest="readiness_checklist",
    )
    release_gate.add_argument("--blocking-risk", action="append", default=[], dest="blocking_risk")
    release_gate.add_argument("--mitigation", action="append", default=[], dest="mitigation")
    release_gate.add_argument("--verdict", required=True)
    release_gate.add_argument("--recommendation", required=True)
    release_gate.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    release_gate.set_defaults(func=cmd_release_gate)

    bridge_launch = subparsers.add_parser(
        "bridge-launch",
        help="Render a reusable last-hop launch payload from a packet plus invocation spec",
    )
    bridge_launch.add_argument("--packet-path", required=True, dest="packet_path")
    bridge_launch.add_argument("--invocation-spec-path", dest="invocation_spec_path")
    bridge_launch.add_argument("--output")
    bridge_launch.set_defaults(func=cmd_bridge_launch)

    bridge_receipt = subparsers.add_parser(
        "bridge-receipt",
        help="Record a repo-backed execution receipt after a bridge-launch payload has been used",
    )
    bridge_receipt.add_argument("--packet-path", required=True, dest="packet_path")
    bridge_receipt.add_argument("--invocation-spec-path", dest="invocation_spec_path")
    bridge_receipt.add_argument("--launch-payload-path", dest="launch_payload_path")
    bridge_receipt.add_argument("--output")
    bridge_receipt.add_argument("--title")
    bridge_receipt.add_argument("--execution-status", required=True, dest="execution_status")
    bridge_receipt.add_argument("--writeback-status", required=True, dest="writeback_status")
    bridge_receipt.add_argument("--specialist-note", required=True, dest="specialist_note")
    bridge_receipt.add_argument("--follow-up", action="append", default=[], dest="follow_up")
    bridge_receipt.set_defaults(func=cmd_bridge_receipt)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
