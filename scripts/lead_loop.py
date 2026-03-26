from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

import role_review
from team_state import (
    cmd_board,
    cmd_decision,
    cmd_discovery_brief,
    cmd_onboarding_report,
    cmd_onboarding_state,
    cmd_plan_brief,
    cmd_review_gate,
    cmd_review_packet,
    cmd_review_pass as cmd_write_review_pass,
    cmd_sprint_contract,
    cmd_task_brief,
    cmd_deep_scan_plan,
)


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
    sprint_contract_path: Path,
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


def _onboarding_stage(root: Path, path: str) -> str:
    content = _read(root / path)
    return _extract_section(content, "Stage") if content else ""


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


def cmd_init(args: argparse.Namespace) -> int:
    onboarding_rel = args.onboarding_state_path
    current_stage = _onboarding_stage(args.root, onboarding_rel)
    if current_stage and not args.force:
        print(
            "Onboarding state already exists. Re-run with --force to perform a manual re-init.",
        )
        return 1

    report_args = SimpleNamespace(
        root=args.root,
        output=args.report_path,
        title=args.title,
        summary=args.summary,
        findings=args.finding,
        recommendations=args.recommendation,
        next_steps=args.next_step,
    )
    rc = cmd_onboarding_report(report_args)
    if rc != 0:
        return rc

    scan_args = SimpleNamespace(
        root=args.root,
        output=args.deep_scan_path,
        title=args.title,
        goals=args.goals,
        hypotheses=args.hypotheses,
        probes=args.probe,
        evidence=args.evidence,
        risk_level=args.risk_level,
        escalation=args.escalation,
        writeback_targets=args.writeback_target,
    )
    rc = cmd_deep_scan_plan(scan_args)
    if rc != 0:
        return rc

    notes = (
        "Missing onboarding state detected. "
        "Shallow scan complete and deep scan plan prepared for user alignment."
    )
    state_args = SimpleNamespace(
        root=args.root,
        output=onboarding_rel,
        title=args.title,
        stage="waiting-user-alignment",
        last_scan="deep-scan-plan",
        pending=args.pending,
        notes=notes,
    )
    rc = cmd_onboarding_state(state_args)
    if rc != 0:
        return rc

    return _update_board(args.root, args.board_path, "approval-needed", [args.title])


def cmd_review_prepare(args: argparse.Namespace) -> int:
    review_dir = args.root / args.review_dir
    review_dir.mkdir(parents=True, exist_ok=True)
    pass_dir = args.root / args.pass_dir
    pass_dir.mkdir(parents=True, exist_ok=True)
    for role_name, filename, objective in [
        ("Product", "product.md", "Assess milestone fit and scope pressure before build."),
        ("Architect", "architect.md", "Assess module boundaries and architecture fit before build."),
        ("Reviewer", "reviewer.md", "Assess quality expectations and verification readiness before build."),
    ]:
        pass_rel = Path(args.pass_dir) / filename
        packet_args = SimpleNamespace(
            root=args.root,
            output=str(Path(args.review_dir) / filename),
            title=f"{role_name} review packet",
            role=role_name,
            objective=objective,
            canonical_source=[
                "docs/project/PROJECT_BRIEF.md",
                "docs/project/ROADMAP.md",
                "docs/project/ARCHITECTURE.md",
                "docs/project/QUALITY_BAR.md",
            ],
            plan_brief=args.plan_path,
            expected_output=(
                "Return a review-pass with Role, Focus, Findings, Auto Decisions, "
                "Taste Decisions, Recommendation"
            ),
            writeback=str(pass_rel),
            writeback_command=(
                f"uv run python scripts/team_state.py review-pass "
                f"--output {pass_rel} "
                f"--title \"{role_name} live pass\" "
                f"--role {role_name} "
                f'--focus "<focus>" '
                f'--finding "<finding>" '
                f'--auto-decision "<auto decision>" '
                f'--recommendation "<recommendation>"'
            ),
        )
        rc = cmd_review_packet(packet_args)
        if rc != 0:
            return rc

    return _update_board(args.root, args.board_path, "review", [args.title])


def cmd_review_collect(args: argparse.Namespace) -> int:
    pass_dir = args.root / args.pass_dir
    pass_dir.mkdir(parents=True, exist_ok=True)
    pass_paths: list[str] = []

    for relpath in args.result_path:
        result_path = args.root / relpath
        content = _read(result_path)
        role = _extract_section(content, "Role") or result_path.stem.title()
        focus = _extract_section(content, "Focus") or "No focus provided"
        findings = _extract_list_section(content, "Findings")
        auto_decisions = _extract_list_section(content, "Auto Decisions")
        taste_decisions = _extract_list_section(content, "Taste Decisions")
        recommendation = _extract_section(content, "Recommendation") or "No recommendation"

        pass_rel = str(Path(args.pass_dir) / result_path.name)
        pass_args = SimpleNamespace(
            root=args.root,
            pass_path=pass_rel,
            title=f"{role} collected pass",
            role=role,
            focus=focus,
            finding=findings or ["No findings provided"],
            auto_decision=auto_decisions or ["No auto decisions recorded"],
            taste_decision=taste_decisions,
            recommendation=recommendation,
        )
        rc = cmd_record_review_pass(pass_args)
        if rc != 0:
            return rc
        pass_paths.append(pass_rel)

    review_args = SimpleNamespace(
        root=args.root,
        title=args.title,
        input_summary=None,
        review_pass=[],
        auto_decision=[],
        taste_decision=[],
        recommendation=None,
        approval_target=None,
        pass_path=pass_paths,
        review_path=args.review_path,
        board_path=args.board_path,
    )
    return cmd_review(review_args)


def cmd_review_run(args: argparse.Namespace) -> int:
    review_dir = args.root / args.review_dir
    review_dir.mkdir(parents=True, exist_ok=True)
    pass_paths: list[str] = []
    for role_name, filename in [
        ("Product", "product.md"),
        ("Architect", "architect.md"),
        ("Reviewer", "reviewer.md"),
    ]:
        output_rel = str(Path(args.review_dir) / filename)
        role_args = SimpleNamespace(
            root=args.root,
            role=role_name,
            plan_path=args.plan_path,
            output=output_rel,
        )
        rc = role_review.main_from_args(role_args)
        if rc != 0:
            return rc
        pass_paths.append(output_rel)

    review_args = SimpleNamespace(
        root=args.root,
        title=args.title,
        input_summary=None,
        review_pass=[],
        auto_decision=[],
        taste_decision=[],
        recommendation=None,
        approval_target=None,
        pass_path=pass_paths,
        review_path=args.review_path,
        board_path=args.board_path,
    )
    return cmd_review(review_args)


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
    return 0


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

    return _update_board(args.root, args.board_path, "build", [args.title])


def cmd_qa(args: argparse.Namespace) -> int:
    sprint_contract = _resolve_path(args.root, args.sprint_contract_path)
    implementation_report = _resolve_path(args.root, args.implementation_report_path)
    if not sprint_contract.exists():
        raise FileNotFoundError(f"Missing sprint contract: {sprint_contract}")
    if not implementation_report.exists():
        raise FileNotFoundError(f"Missing implementation report: {implementation_report}")
    _assert_consumed_sprint_contract(
        args.root,
        sprint_contract,
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

    init = subparsers.add_parser(
        "init",
        help="Create onboarding state, shallow-scan report, and deep-scan plan",
    )
    init.add_argument("--title", required=True)
    init.add_argument("--summary", required=True)
    init.add_argument("--finding", action="append", default=[], required=True)
    init.add_argument("--recommendation", action="append", default=[], required=True)
    init.add_argument("--next-step", action="append", default=[], required=True, dest="next_step")
    init.add_argument("--goals", required=True)
    init.add_argument("--hypotheses", required=True)
    init.add_argument("--probe", action="append", default=[], required=True)
    init.add_argument("--evidence", action="append", default=[], required=True)
    init.add_argument("--risk-level", required=True, dest="risk_level")
    init.add_argument("--escalation", action="append", default=[])
    init.add_argument("--writeback-target", action="append", default=[], required=True, dest="writeback_target")
    init.add_argument("--pending", action="append", default=[])
    init.add_argument("--report-path", default="docs/plans/onboarding-report.md")
    init.add_argument("--deep-scan-path", default="docs/plans/deep-scan-plan.md")
    init.add_argument("--onboarding-state-path", default="docs/status/ONBOARDING_STATE.md")
    init.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    delegate = subparsers.add_parser(
        "delegate",
        help="Create a delegated task brief without starting builder kickoff",
    )
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

    review_prepare = subparsers.add_parser(
        "review-prepare",
        help="Create Product, Architect, and Reviewer packets for live subagent review",
    )
    review_prepare.add_argument("--title", required=True)
    review_prepare.add_argument("--plan-path", required=True)
    review_prepare.add_argument("--review-dir", required=True)
    review_prepare.add_argument("--pass-dir", required=True)
    review_prepare.add_argument("--result-dir")
    review_prepare.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    review_prepare.set_defaults(func=cmd_review_prepare)

    review_collect = subparsers.add_parser(
        "review-collect",
        help="Collect Product, Architect, and Reviewer review results into passes and a review gate",
    )
    review_collect.add_argument("--title", required=True)
    review_collect.add_argument("--result-path", action="append", default=[], required=True)
    review_collect.add_argument("--pass-dir", required=True)
    review_collect.add_argument("--review-path", required=True)
    review_collect.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    review_collect.set_defaults(func=cmd_review_collect)

    review_run = subparsers.add_parser(
        "review-run",
        help="Run Product, Architect, and Reviewer passes and aggregate the review gate",
    )
    review_run.add_argument("--title", required=True)
    review_run.add_argument("--plan-path", required=True)
    review_run.add_argument("--review-dir", required=True)
    review_run.add_argument("--review-path", required=True)
    review_run.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    review_run.set_defaults(func=cmd_review_run)

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
