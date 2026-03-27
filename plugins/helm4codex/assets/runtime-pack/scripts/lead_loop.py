from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

from role_bridge import resolve_role
import role_review
from team_state import (
    cmd_autoplan_report,
    cmd_board,
    cmd_decision,
    cmd_discovery_brief,
    cmd_discovery_gate,
    cmd_invocation_spec,
    cmd_onboarding_report,
    cmd_onboarding_state,
    cmd_office_hours_brief,
    cmd_office_hours_report,
    cmd_plan_brief,
    cmd_research_brief,
    cmd_research_report,
    cmd_review_gate,
    cmd_review_packet,
    cmd_review_pass as cmd_write_review_pass,
    cmd_task_brief,
    cmd_deep_scan_plan,
)

AUTOPLAN_ROLE_FILES = [
    ("Product", "product.md"),
    ("Architect", "architect.md"),
    ("Reviewer", "reviewer.md"),
]

OFFICE_HOURS_ROLE_FILES = [
    ("Product", "product.md"),
    ("Design", "design.md"),
    ("Architect", "architect.md"),
]


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _resolve_path(root: Path, path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def _default_invocation_spec_path(packet_path: str) -> str:
    packet = Path(packet_path)
    if packet.parent.name.endswith("packets"):
        return str(packet.parent.parent / "invocation-specs" / packet.name)
    return str(packet.with_name(f"{packet.stem}-invocation{packet.suffix or '.md'}"))


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


def _autoplan_paths(
    *,
    artifact_dir: str,
    review_dir: str | None = None,
    review_path: str | None = None,
    autoplan_path: str | None = None,
) -> SimpleNamespace:
    base = Path(artifact_dir)
    return SimpleNamespace(
        artifact_dir=str(base),
        report_path=autoplan_path or str(base / "autoplan-report.md"),
        review_path=review_path or str(base / "review-gate.md"),
        review_dir=str(base / "review-packets"),
        invocation_dir=str(base / "invocation-specs"),
        pass_dir=review_dir or str(base / "review-passes"),
        result_dir=str(base / "review-results"),
        review_pass_paths=[
            str(Path(review_dir or str(base / "review-passes")) / filename)
            for _, filename in AUTOPLAN_ROLE_FILES
        ],
        review_packet_paths=[str(base / "review-packets" / filename) for _, filename in AUTOPLAN_ROLE_FILES],
        invocation_paths=[str(base / "invocation-specs" / filename) for _, filename in AUTOPLAN_ROLE_FILES],
        review_result_paths=[str(base / "review-results" / filename) for _, filename in AUTOPLAN_ROLE_FILES],
    )


def _office_hours_paths(
    *,
    artifact_dir: str,
    brief_path: str | None = None,
    research_brief_path: str | None = None,
    research_report_path: str | None = None,
    gate_path: str | None = None,
    report_path: str | None = None,
    pass_dir: str | None = None,
) -> SimpleNamespace:
    base = Path(artifact_dir)
    return SimpleNamespace(
        artifact_dir=str(base),
        brief_path=brief_path or str(base / "office-hours-brief.md"),
        research_brief_path=research_brief_path or str(base / "research-brief.md"),
        research_report_path=research_report_path or str(base / "research-report.md"),
        gate_path=gate_path or str(base / "discovery-gate.md"),
        report_path=report_path or str(base / "office-hours-report.md"),
        pass_dir=pass_dir or str(base / "challenge-passes"),
        pass_paths=[
            str(Path(pass_dir or str(base / "challenge-passes")) / filename)
            for _, filename in OFFICE_HOURS_ROLE_FILES
        ],
    )


def _write_autoplan_report(
    args: argparse.Namespace,
    paths: SimpleNamespace,
    *,
    outcome: str,
    next_step: str,
    discovery_path: str | None = None,
    auto_decisions: list[str] | None = None,
    blocking_issues: list[str] | None = None,
    taste_decisions: list[str] | None = None,
    review_pass_paths: list[str] | None = None,
    review_packet_paths: list[str] | None = None,
    invocation_paths: list[str] | None = None,
    review_result_paths: list[str] | None = None,
    review_path: str | None = None,
) -> int:
    report_args = SimpleNamespace(
        root=args.root,
        output=paths.report_path,
        title=args.title,
        mode=args.mode,
        outcome=outcome,
        discovery_brief=discovery_path,
        plan_brief=args.plan_path,
        review_pass=review_pass_paths or [],
        review_packet=review_packet_paths or [],
        invocation_spec=invocation_paths or [],
        review_result=review_result_paths or [],
        review_gate=review_path,
        auto_decision=auto_decisions or [],
        taste_decision=taste_decisions or [],
        blocking_issue=blocking_issues or [],
        next_action=next_step,
        next_step=next_step,
    )
    return cmd_autoplan_report(report_args)


def _write_office_hours_report(
    args: argparse.Namespace,
    paths: SimpleNamespace,
    *,
    outcome: str,
    next_action: str,
    reframing_changes: list[str] | None = None,
    challenge_pass_paths: list[str] | None = None,
) -> int:
    report_args = SimpleNamespace(
        root=args.root,
        output=paths.report_path,
        title=args.title,
        mode=args.mode,
        outcome=outcome,
        office_hours_brief=paths.brief_path,
        research_brief=paths.research_brief_path,
        research_report=paths.research_report_path,
        challenge_pass=challenge_pass_paths or [],
        discovery_gate=paths.gate_path,
        reframing_change=reframing_changes or [],
        next_action=next_action,
    )
    return cmd_office_hours_report(report_args)


def _gate_outcome(root: Path, review_path: str) -> str:
    taste_decisions = _extract_list_section(_read(root / review_path), "Taste Decisions")
    return "ask-user" if taste_decisions else "auto-clear"


def _discovery_gate_outcome(root: Path, gate_path: str) -> str:
    return _extract_section(_read(root / gate_path), "Outcome") or "reframe"


def _run_ops_loop(args: argparse.Namespace, command: str, command_args: list[str]) -> int:
    script = Path(__file__).with_name("ops_loop.py")
    result = subprocess.run(
        [sys.executable, str(script), "--root", str(args.root), command, *command_args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


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
    invocation_dir = args.root / args.invocation_dir if args.invocation_dir else None
    if invocation_dir is not None:
        invocation_dir.mkdir(parents=True, exist_ok=True)
    pass_dir = args.root / args.pass_dir
    pass_dir.mkdir(parents=True, exist_ok=True)
    for role_name, logical_role, filename, objective in [
        ("Product", "product-reviewer", "product.md", "Assess milestone fit and scope pressure before build."),
        ("Architect", "architect-reviewer", "architect.md", "Assess module boundaries and architecture fit before build."),
        ("Reviewer", "code-reviewer", "reviewer.md", "Assess quality expectations and verification readiness before build."),
    ]:
        resolved_role = resolve_role(args.root, logical_role)
        pass_rel = Path(args.pass_dir) / filename
        packet_rel = Path(args.review_dir) / filename
        packet_args = SimpleNamespace(
            root=args.root,
            output=str(packet_rel),
            title=f"{role_name} review packet",
            role=role_name,
            logical_role=resolved_role["logical_role"],
            bridge_agent_type=resolved_role["agent_type"],
            bridge_model=resolved_role["model"],
            bridge_reasoning_effort=resolved_role["reasoning_effort"],
            role_skill=resolved_role["skill"],
            role_metadata=resolved_role["metadata"],
            role_writeback_target=resolved_role["writeback_target"],
            role_writeback_command=resolved_role["writeback_command"],
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

        invocation_args = SimpleNamespace(
            root=args.root,
            output=(
                str(Path(args.invocation_dir) / filename)
                if args.invocation_dir
                else _default_invocation_spec_path(str(packet_rel))
            ),
            title=f"{role_name} review invocation",
            role=resolved_role["display_name"],
            logical_role=resolved_role["logical_role"],
            source_packet=str(packet_rel),
            bridge_agent_type=resolved_role["agent_type"],
            bridge_model=resolved_role["model"],
            bridge_reasoning_effort=resolved_role["reasoning_effort"],
            runtime_skill=resolved_role["skill"],
            metadata=resolved_role["metadata"],
            consumed_artifact=[
                str(packet_rel),
                "docs/project/PROJECT_BRIEF.md",
                "docs/project/ROADMAP.md",
                "docs/project/ARCHITECTURE.md",
                "docs/project/QUALITY_BAR.md",
                args.plan_path,
            ],
            expected_writeback_target=str(pass_rel),
            expected_writeback_command=packet_args.writeback_command,
        )
        rc = cmd_invocation_spec(invocation_args)
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
            mode="plan-review",
            role=role_name,
            plan_path=args.plan_path,
            brief_path=None,
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
    return _run_ops_loop(
        args,
        "build",
        [
            "--title",
            args.title,
            "--planner",
            args.planner,
            "--generator",
            args.generator,
            "--evaluator",
            args.evaluator,
            "--scope",
            args.scope,
            "--acceptance",
            args.acceptance,
            "--implementation-report-path",
            args.implementation_report_path,
            "--sprint-contract-path",
            args.sprint_contract_path,
            "--builder-packet-path",
            args.builder_packet_path,
            *(
                ["--builder-invocation-spec-path", args.builder_invocation_spec_path]
                if args.builder_invocation_spec_path
                else []
            ),
            "--board-path",
            args.board_path,
        ],
    )


def cmd_sprint_negotiate(args: argparse.Namespace) -> int:
    return _run_ops_loop(
        args,
        "sprint-negotiate",
        [
            "--title",
            args.title,
            "--planner",
            args.planner,
            "--generator",
            args.generator,
            "--evaluator",
            args.evaluator,
            "--scope",
            args.scope,
            "--acceptance",
            args.acceptance,
            "--evidence-posture",
            args.evidence_posture,
            "--implementation-report-path",
            args.implementation_report_path,
            "--sprint-proposal-path",
            args.sprint_proposal_path,
            "--builder-sprint-pass-path",
            args.builder_sprint_pass_path,
            "--qa-sprint-pass-path",
            args.qa_sprint_pass_path,
            "--sprint-gate-path",
            args.sprint_gate_path,
            "--sprint-contract-path",
            args.sprint_contract_path,
            "--builder-packet-path",
            args.builder_packet_path,
            *(
                ["--builder-invocation-spec-path", args.builder_invocation_spec_path]
                if args.builder_invocation_spec_path
                else []
            ),
            "--board-path",
            args.board_path,
        ],
    )


def cmd_qa_prepare(args: argparse.Namespace) -> int:
    command_args = [
        "--title",
        args.title,
        "--sprint-contract-path",
        args.sprint_contract_path,
        "--implementation-report-path",
        args.implementation_report_path,
        "--qa-packet-path",
        args.qa_packet_path,
        *(
            ["--qa-invocation-spec-path", args.qa_invocation_spec_path]
            if args.qa_invocation_spec_path
            else []
        ),
        "--qa-report-path",
        args.qa_report_path,
        "--environment",
        args.environment,
    ]
    for scenario in args.scenario:
        command_args.extend(["--scenario", scenario])
    return _run_ops_loop(args, "qa-prepare", command_args)


def cmd_qa(args: argparse.Namespace) -> int:
    command_args = [
        "--title",
        args.title,
        "--sprint-contract-path",
        args.sprint_contract_path,
        "--implementation-report-path",
        args.implementation_report_path,
        "--qa-report-path",
        args.qa_report_path,
        "--environment",
        args.environment,
    ]
    for scenario in args.scenario:
        command_args.extend(["--scenario", scenario])
    for issue in args.issue:
        command_args.extend(["--issue", issue])
    command_args.extend(
        [
            "--verification-status",
            args.verification_status,
            "--board-path",
            args.board_path,
        ],
    )
    return _run_ops_loop(args, "qa", command_args)


def cmd_docs_sync_prepare(args: argparse.Namespace) -> int:
    command_args = [
        "--title",
        args.title,
        "--implementation-report-path",
        args.implementation_report_path,
        "--qa-report-path",
        args.qa_report_path,
        "--docs-sync-packet-path",
        args.docs_sync_packet_path,
        *(
            ["--docs-sync-invocation-spec-path", args.docs_sync_invocation_spec_path]
            if args.docs_sync_invocation_spec_path
            else []
        ),
        "--docs-sync-report-path",
        args.docs_sync_report_path,
    ]
    for doc in args.docs_updated:
        command_args.extend(["--docs-updated", doc])
    for target in args.canonical_writeback:
        command_args.extend(["--canonical-writeback", target])
    return _run_ops_loop(args, "docs-sync-prepare", command_args)


def cmd_bridge_launch(args: argparse.Namespace) -> int:
    command_args = [
        "--packet-path",
        args.packet_path,
        *(
            ["--invocation-spec-path", args.invocation_spec_path]
            if args.invocation_spec_path
            else []
        ),
        *(["--output", args.output] if args.output else []),
    ]
    return _run_ops_loop(args, "bridge-launch", command_args)


def cmd_bridge_receipt(args: argparse.Namespace) -> int:
    command_args = [
        "--packet-path",
        args.packet_path,
        *(
            ["--invocation-spec-path", args.invocation_spec_path]
            if args.invocation_spec_path
            else []
        ),
        *(
            ["--launch-payload-path", args.launch_payload_path]
            if args.launch_payload_path
            else []
        ),
        *(["--output", args.output] if args.output else []),
        *(["--title", args.title] if args.title else []),
        "--execution-status",
        args.execution_status,
        "--writeback-status",
        args.writeback_status,
        "--specialist-note",
        args.specialist_note,
    ]
    for follow_up in args.follow_up:
        command_args.extend(["--follow-up", follow_up])
    return _run_ops_loop(args, "bridge-receipt", command_args)


def cmd_docs_sync(args: argparse.Namespace) -> int:
    command_args = [
        "--title",
        args.title,
        "--implementation-report-path",
        args.implementation_report_path,
        "--qa-report-path",
        args.qa_report_path,
        "--docs-sync-report-path",
        args.docs_sync_report_path,
    ]
    for doc in args.docs_updated:
        command_args.extend(["--docs-updated", doc])
    for target in args.canonical_writeback:
        command_args.extend(["--canonical-writeback", target])
    for follow_up in args.follow_up:
        command_args.extend(["--follow-up", follow_up])
    command_args.extend(["--board-path", args.board_path])
    return _run_ops_loop(args, "docs-sync", command_args)


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


def cmd_autoplan(args: argparse.Namespace) -> int:
    artifact_dir = args.artifact_dir
    if not artifact_dir:
        if args.autoplan_path:
            artifact_dir = str(Path(args.autoplan_path).parent)
        elif args.review_path:
            artifact_dir = str(Path(args.review_path).parent)
        elif args.review_dir:
            artifact_dir = str(Path(args.review_dir).parent)
        else:
            artifact_dir = "docs/plans/autoplan"

    paths = _autoplan_paths(
        artifact_dir=artifact_dir,
        review_dir=args.review_dir,
        review_path=args.review_path,
        autoplan_path=args.autoplan_path,
    )
    plan_exists = (args.root / args.plan_path).exists()

    if not plan_exists:
        required_inputs = {
            "problem": args.problem,
            "research scope": args.research_scope,
            "open questions": args.open_questions,
            "recommendation target": args.recommendation_target,
            "discovery path": args.discovery_path,
            "goal": args.goal,
            "milestone": args.milestone,
            "modules": args.modules,
            "exit criteria": args.exit_criteria,
            "writeback": args.writeback,
        }
        missing_inputs = [name for name, value in required_inputs.items() if not value]
        if missing_inputs:
            blocking_issue = f"Missing required plan brief: {args.plan_path}"
            _write_autoplan_report(
                args,
                paths,
                outcome="blocked",
                next_step=(
                    "Create or point autoplan at a plan brief before running the lane."
                ),
                discovery_path=args.discovery_path,
                blocking_issues=[blocking_issue, *[f"Missing {name} for autoplan bootstrap" for name in missing_inputs]],
            )
            print(blocking_issue, file=sys.stderr)
            return 1

        discover_args = SimpleNamespace(
            root=args.root,
            title=args.title,
            problem=args.problem,
            research_scope=args.research_scope,
            open_questions=args.open_questions,
            recommendation_target=args.recommendation_target,
            discovery_path=args.discovery_path,
            board_path=args.board_path,
        )
        rc = cmd_discover(discover_args)
        if rc != 0:
            return rc

        plan_args = SimpleNamespace(
            root=args.root,
            title=args.title,
            goal=args.goal,
            milestone=args.milestone,
            modules=args.modules,
            exit_criteria=args.exit_criteria,
            writeback=args.writeback,
            plan_path=args.plan_path,
            board_path=args.board_path,
        )
        rc = cmd_plan(plan_args)
        if rc != 0:
            return rc

    if args.mode == "prepare":
        prepare_args = SimpleNamespace(
            root=args.root,
            title=args.title,
            plan_path=args.plan_path,
            review_dir=paths.review_dir,
            invocation_dir=paths.invocation_dir,
            pass_dir=paths.pass_dir,
            result_dir=paths.result_dir,
            board_path=args.board_path,
        )
        rc = cmd_review_prepare(prepare_args)
        if rc != 0:
            return rc
        return _write_autoplan_report(
            args,
            paths,
            outcome="in-review",
            next_step=(
                "Run Product, Architect, and Reviewer review packets, write results under "
                f"{paths.result_dir}, then rerun `lead_loop.py autoplan --mode collect`."
            ),
            discovery_path=args.discovery_path,
            review_pass_paths=paths.review_pass_paths,
            review_packet_paths=paths.review_packet_paths,
            invocation_paths=paths.invocation_paths,
            review_result_paths=paths.review_result_paths,
        )

    if args.mode == "collect":
        missing_results = [
            relpath for relpath in paths.review_result_paths if not (args.root / relpath).exists()
        ]
        if missing_results:
            _write_autoplan_report(
                args,
                paths,
                outcome="blocked",
                next_step=(
                    "Write Product, Architect, and Reviewer review results under "
                    f"{paths.result_dir} before collecting autoplan."
                ),
                discovery_path=args.discovery_path,
                blocking_issues=[f"Missing review result: {relpath}" for relpath in missing_results],
                review_result_paths=paths.review_result_paths,
            )
            print(
                f"Missing required review results under {paths.result_dir}",
                file=sys.stderr,
            )
            return 1

        collect_args = SimpleNamespace(
            root=args.root,
            title=args.title,
            result_path=paths.review_result_paths,
            pass_dir=paths.pass_dir,
            review_path=paths.review_path,
            board_path=args.board_path,
        )
        rc = cmd_review_collect(collect_args)
        if rc != 0:
            return rc
    else:
        run_args = SimpleNamespace(
            root=args.root,
            title=args.title,
            plan_path=args.plan_path,
            review_dir=paths.pass_dir,
            review_path=paths.review_path,
            board_path=args.board_path,
        )
        rc = cmd_review_run(run_args)
        if rc != 0:
            return rc

    outcome = _gate_outcome(args.root, paths.review_path)
    auto_decisions = _extract_list_section(_read(args.root / paths.review_path), "Auto Decisions")
    taste_decisions = _extract_list_section(_read(args.root / paths.review_path), "Taste Decisions")
    next_step = (
        "Resolve taste decisions before build."
        if outcome == "ask-user"
        else "Proceed to build. Proceed to bounded builder kickoff."
    )
    return _write_autoplan_report(
        args,
        paths,
        outcome=outcome,
        next_step=next_step,
        discovery_path=args.discovery_path,
        auto_decisions=auto_decisions,
        taste_decisions=taste_decisions,
        review_pass_paths=paths.review_pass_paths,
        review_result_paths=paths.review_result_paths if args.mode == "collect" else [],
        review_path=paths.review_path,
    )


def _office_hours_gate_fields(
    root: Path,
    brief_path: str,
    research_report_path: str,
    pass_paths: list[str],
) -> SimpleNamespace:
    brief = _read(root / brief_path)
    research = _read(root / research_report_path)
    problem = _extract_section(brief, "Problem Statement") or "Problem framing missing."
    proposal = _extract_section(brief, "Current Proposal") or "Current proposal missing."
    build_vs_buy = _extract_section(brief, "Build vs Buy Context") or "Build-vs-buy context missing."
    assumptions = _extract_list_section(brief, "Assumptions To Challenge")
    research_recommendation = _extract_section(research, "Recommendation")
    research_posture = _extract_section(research, "Build vs Buy Posture")

    taste_decisions: list[str] = []
    auto_decisions: list[str] = []
    recommendations: list[str] = []
    for relpath in pass_paths:
        content = _read(root / relpath)
        auto_decisions.extend(_extract_list_section(content, "Auto Decisions"))
        taste_decisions.extend(_extract_list_section(content, "Taste Decisions"))
        recommendation = _extract_section(content, "Recommendation")
        if recommendation:
            recommendations.append(recommendation)

    lowered_problem = f"{problem}\n{proposal}".lower()
    lowered_build_vs_buy = build_vs_buy.lower()

    if any(token in lowered_build_vs_buy for token in ["budget", "legal", "procurement", "compliance"]):
        outcome = "ask-user"
        reframed_problem = f"Confirm the strategic boundary before planning: {problem}"
        next_step = "Escalate the unresolved strategic tradeoff to the user before planning."
    elif (
        any(token in lowered_problem for token in ["all", "everything", "platform"])
        or len(assumptions) >= 3
        or "defer broader platform scope" in research_recommendation.lower()
    ):
        outcome = "reframe"
        reframed_problem = f"Reduce the first milestone to one critical path instead of the full proposal: {proposal}"
        next_step = "Rewrite the brief around a narrower first milestone, then rerun office-hours."
    elif taste_decisions:
        outcome = "ask-user"
        reframed_problem = f"Resolve the remaining cross-functional tradeoff before planning: {problem}"
        next_step = "Bring the remaining taste decisions to the user before planning."
    else:
        outcome = "ready-for-plan"
        reframed_problem = problem
        next_step = "Proceed to plan creation using the reframed brief and challenge passes."

    build_vs_buy_posture = research_posture or (
        "build-from-scratch remains under challenge"
        if any(token in lowered_build_vs_buy for token in ["from scratch", "custom", "reinvent"])
        else "current build-vs-buy posture is acceptable for planning"
    )
    recommendation = recommendations[-1] if recommendations else next_step
    return SimpleNamespace(
        outcome=outcome,
        reframed_problem=reframed_problem,
        build_vs_buy_posture=build_vs_buy_posture,
        unresolved_tensions=taste_decisions,
        auto_decisions=auto_decisions,
        recommendation=recommendation,
        next_step=next_step,
    )


def _default_research_questions(args: argparse.Namespace) -> str:
    if args.research_question:
        return "\n".join(f"- {item}" for item in args.research_question)
    return "- What should be built now versus adopted or deferred?\n- Which external baseline should the next plan cite explicitly?"


def _write_deterministic_research(args: argparse.Namespace, paths: SimpleNamespace) -> int:
    brief = _read(args.root / paths.brief_path)
    problem = _extract_section(brief, "Problem Statement") or "Problem framing missing."
    proposal = _extract_section(brief, "Current Proposal") or "Current proposal missing."
    constraints = _extract_section(brief, "Constraints") or "Constraints missing."
    build_vs_buy = _extract_section(brief, "Build vs Buy Context") or "Build-vs-buy context missing."
    assumptions = _extract_list_section(brief, "Assumptions To Challenge")
    lowered = f"{proposal}\n{build_vs_buy}".lower()
    broad_scope = any(token in lowered for token in ["all", "everything", "platform"]) or len(assumptions) >= 3

    if not (args.root / paths.research_brief_path).exists():
        if not args.research_scope:
            print(
                "Missing research scope: provide --research-scope or an existing research brief before running office-hours.",
                file=sys.stderr,
            )
            return 1
        research_brief_args = SimpleNamespace(
            root=args.root,
            output=paths.research_brief_path,
            title=args.title,
            problem_framing=problem,
            research_scope=args.research_scope,
            known_constraints=constraints,
            key_questions=_default_research_questions(args),
            recommendation_target=paths.report_path,
        )
        rc = cmd_research_brief(research_brief_args)
        if rc != 0:
            return rc

    if (args.root / paths.research_report_path).exists():
        return 0

    top_options = [
        "Adopt a bounded repo-local baseline before wider orchestration.",
        "Reuse existing experiment-tracking seams before committing to a full platform build.",
    ]
    if not broad_scope:
        top_options[0] = "Proceed with one bounded repo-local milestone before widening scope."

    recommendation = (
        "Proceed with one bounded local milestone and defer broader platform scope."
        if broad_scope or any(token in lowered for token in ["from scratch", "custom", "risk"])
        else "Proceed with the current bounded milestone while preserving adoption seams."
    )
    posture = (
        "Prefer a bounded local build with explicit reuse over a greenfield platform."
        if broad_scope or any(token in lowered for token in ["from scratch", "custom", "risk"])
        else "Current build-vs-buy posture is acceptable for planning."
    )
    adoption_notes = [
        "Keep integration seams visible in the first plan.",
        "Name the strongest external baseline in the next plan brief.",
    ]
    open_risks = [
        "The operator flow is still under-specified."
        if not any(token in f"{problem}\n{proposal}".lower() for token in ["flow", "journey", "operator", "screen"])
        else "Broader platform scope could reappear without a milestone guardrail."
    ]
    report_args = SimpleNamespace(
        root=args.root,
        output=paths.research_report_path,
        title=args.title,
        problem_framing=problem,
        research_brief=paths.research_brief_path,
        top_option=top_options,
        recommendation=recommendation,
        build_vs_buy_posture=posture,
        adoption_note=adoption_notes,
        open_risk=open_risks,
    )
    return cmd_research_report(report_args)


def cmd_office_hours(args: argparse.Namespace) -> int:
    artifact_dir = args.artifact_dir or "docs/plans/office-hours"
    paths = _office_hours_paths(
        artifact_dir=artifact_dir,
        brief_path=args.office_hours_brief_path,
        research_brief_path=args.research_brief_path,
        research_report_path=args.research_report_path,
        gate_path=args.discovery_gate_path,
        report_path=args.office_hours_report_path,
        pass_dir=args.challenge_pass_dir,
    )

    if args.mode == "prepare":
        rc = _write_office_hours_report(
            args,
            paths,
            outcome="in-review",
            next_action=(
                "Office-hours live role preparation is not wired yet. Use `office-hours --mode run`"
                " for deterministic challenge passes in this tranche."
            ),
        )
        if rc != 0:
            return rc
        return _update_board(args.root, args.board_path, "discovery", [args.title])

    if args.mode == "collect":
        rc = _write_office_hours_report(
            args,
            paths,
            outcome="blocked",
            next_action=(
                "Office-hours collect mode is reserved for future live role execution. "
                "Use `office-hours --mode run` in this tranche."
            ),
        )
        if rc != 0:
            return rc
        return 1

    if not (args.root / paths.brief_path).exists():
        required_inputs = {
            "problem statement": args.problem_statement,
            "target user": args.target_user,
            "current proposal": args.current_proposal,
            "constraint": args.constraint,
            "success criterion": args.success_criterion,
            "build-vs-buy context": args.build_vs_buy_context,
            "assumption to challenge": args.assumption_to_challenge,
        }
        missing = [name for name, value in required_inputs.items() if not value]
        if missing:
            rc = _write_office_hours_report(
                args,
                paths,
                outcome="blocked",
                next_action=(
                    "Provide the missing office-hours inputs or an existing office-hours brief "
                    "before running the deterministic lane."
                ),
            )
            if rc != 0:
                return rc
            print(f"Missing office-hours inputs: {', '.join(missing)}", file=sys.stderr)
            return 1

        brief_args = SimpleNamespace(
            root=args.root,
            output=paths.brief_path,
            title=args.title,
            problem_statement=args.problem_statement,
            target_user=args.target_user,
            current_proposal=args.current_proposal,
            constraint=args.constraint,
            success_criterion=args.success_criterion,
            build_vs_buy_context=args.build_vs_buy_context,
            assumption_to_challenge=args.assumption_to_challenge,
        )
        rc = cmd_office_hours_brief(brief_args)
        if rc != 0:
            return rc

    rc = _write_deterministic_research(args, paths)
    if rc != 0:
        return rc

    pass_dir = args.root / paths.pass_dir
    pass_dir.mkdir(parents=True, exist_ok=True)
    pass_paths: list[str] = []
    for role_name, filename in OFFICE_HOURS_ROLE_FILES:
        output_rel = str(Path(paths.pass_dir) / filename)
        role_args = SimpleNamespace(
            root=args.root,
            mode="office-hours",
            role=role_name,
            brief_path=paths.brief_path,
            research_report_path=paths.research_report_path,
            output=output_rel,
            plan_path=None,
        )
        rc = role_review.main_from_args(role_args)
        if rc != 0:
            return rc
        pass_paths.append(output_rel)

    gate_fields = _office_hours_gate_fields(
        args.root,
        paths.brief_path,
        paths.research_report_path,
        pass_paths,
    )
    gate_args = SimpleNamespace(
        root=args.root,
        output=paths.gate_path,
        title=args.title,
        office_hours_brief=paths.brief_path,
        research_report=paths.research_report_path,
        challenge_pass=pass_paths,
        reframed_problem_statement=gate_fields.reframed_problem,
        build_vs_buy_posture=gate_fields.build_vs_buy_posture,
        unresolved_tension=gate_fields.unresolved_tensions,
        outcome=gate_fields.outcome,
        next_step=gate_fields.next_step,
    )
    rc = cmd_discovery_gate(gate_args)
    if rc != 0:
        return rc

    rc = _write_office_hours_report(
        args,
        paths,
        outcome=gate_fields.outcome,
        next_action=gate_fields.next_step,
        reframing_changes=[
            gate_fields.reframed_problem,
            f"Build-vs-buy posture: {gate_fields.build_vs_buy_posture}",
        ],
        challenge_pass_paths=pass_paths,
    )
    if rc != 0:
        return rc

    stage = {
        "ready-for-plan": "plan",
        "ask-user": "approval-needed",
        "reframe": "discovery",
    }[_discovery_gate_outcome(args.root, paths.gate_path)]
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

    office_hours = subparsers.add_parser(
        "office-hours",
        help="Run the office-hours discovery lane before planning",
    )
    office_hours.add_argument("--mode", choices=["run", "prepare", "collect"], default="run")
    office_hours.add_argument("--title", required=True)
    office_hours.add_argument("--artifact-dir", dest="artifact_dir")
    office_hours.add_argument("--office-hours-brief-path", dest="office_hours_brief_path")
    office_hours.add_argument("--research-brief-path", dest="research_brief_path")
    office_hours.add_argument("--research-report-path", dest="research_report_path")
    office_hours.add_argument("--discovery-gate-path", dest="discovery_gate_path")
    office_hours.add_argument("--office-hours-report-path", dest="office_hours_report_path")
    office_hours.add_argument("--challenge-pass-dir", dest="challenge_pass_dir")
    office_hours.add_argument("--problem-statement", dest="problem_statement")
    office_hours.add_argument("--target-user", dest="target_user")
    office_hours.add_argument("--current-proposal", dest="current_proposal")
    office_hours.add_argument("--constraint", action="append", default=[])
    office_hours.add_argument(
        "--success-criterion",
        action="append",
        default=[],
        dest="success_criterion",
    )
    office_hours.add_argument("--build-vs-buy-context", dest="build_vs_buy_context")
    office_hours.add_argument("--research-scope", dest="research_scope")
    office_hours.add_argument("--research-question", action="append", default=[], dest="research_question")
    office_hours.add_argument(
        "--assumption-to-challenge",
        action="append",
        default=[],
        dest="assumption_to_challenge",
    )
    office_hours.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    office_hours.set_defaults(func=cmd_office_hours)

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
    build.add_argument("--builder-packet-path", required=True, dest="builder_packet_path")
    build.add_argument("--builder-invocation-spec-path", dest="builder_invocation_spec_path")
    build.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    build.set_defaults(func=cmd_build)

    sprint_negotiate = subparsers.add_parser(
        "sprint-negotiate",
        help="Negotiate a sprint proposal through Builder and QA pressure before build",
    )
    sprint_negotiate.add_argument("--title", required=True)
    sprint_negotiate.add_argument("--planner", required=True)
    sprint_negotiate.add_argument("--generator", required=True)
    sprint_negotiate.add_argument("--evaluator", required=True)
    sprint_negotiate.add_argument("--scope", required=True)
    sprint_negotiate.add_argument("--acceptance", required=True)
    sprint_negotiate.add_argument("--evidence-posture", required=True, dest="evidence_posture")
    sprint_negotiate.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    sprint_negotiate.add_argument("--sprint-proposal-path", required=True, dest="sprint_proposal_path")
    sprint_negotiate.add_argument("--builder-sprint-pass-path", required=True, dest="builder_sprint_pass_path")
    sprint_negotiate.add_argument("--qa-sprint-pass-path", required=True, dest="qa_sprint_pass_path")
    sprint_negotiate.add_argument("--sprint-gate-path", required=True, dest="sprint_gate_path")
    sprint_negotiate.add_argument("--sprint-contract-path", required=True, dest="sprint_contract_path")
    sprint_negotiate.add_argument("--builder-packet-path", required=True, dest="builder_packet_path")
    sprint_negotiate.add_argument("--builder-invocation-spec-path", dest="builder_invocation_spec_path")
    sprint_negotiate.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    sprint_negotiate.set_defaults(func=cmd_sprint_negotiate)

    qa_prepare = subparsers.add_parser(
        "qa-prepare",
        help="Create the QA dispatch packet after the implementation report exists",
    )
    qa_prepare.add_argument("--title", required=True)
    qa_prepare.add_argument("--sprint-contract-path", required=True, dest="sprint_contract_path")
    qa_prepare.add_argument(
        "--implementation-report-path",
        required=True,
        dest="implementation_report_path",
    )
    qa_prepare.add_argument("--qa-packet-path", required=True, dest="qa_packet_path")
    qa_prepare.add_argument("--qa-invocation-spec-path", dest="qa_invocation_spec_path")
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

    bridge_launch = subparsers.add_parser(
        "bridge-launch",
        help="Route a packet plus invocation spec through Ops to render a last-hop launch payload",
    )
    bridge_launch.add_argument("--packet-path", required=True, dest="packet_path")
    bridge_launch.add_argument("--invocation-spec-path", dest="invocation_spec_path")
    bridge_launch.add_argument("--output")
    bridge_launch.set_defaults(func=cmd_bridge_launch)

    bridge_receipt = subparsers.add_parser(
        "bridge-receipt",
        help="Route a bridge execution result through Ops and record a repo-backed execution receipt",
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
    review_prepare.add_argument("--invocation-dir")
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

    autoplan = subparsers.add_parser(
        "autoplan",
        help="Run the first-class bounded autoplan lane over existing review primitives",
    )
    autoplan.add_argument("--mode", choices=["run", "prepare", "collect"], default="run")
    autoplan.add_argument("--title", required=True)
    autoplan.add_argument("--plan-path", required=True)
    autoplan.add_argument("--artifact-dir", dest="artifact_dir")
    autoplan.add_argument("--problem")
    autoplan.add_argument("--research-scope", dest="research_scope")
    autoplan.add_argument("--open-questions", dest="open_questions")
    autoplan.add_argument("--recommendation-target", dest="recommendation_target")
    autoplan.add_argument("--discovery-path", dest="discovery_path")
    autoplan.add_argument("--goal")
    autoplan.add_argument("--milestone")
    autoplan.add_argument("--modules")
    autoplan.add_argument("--exit-criteria", dest="exit_criteria")
    autoplan.add_argument("--writeback")
    autoplan.add_argument("--review-dir", dest="review_dir")
    autoplan.add_argument("--review-path", dest="review_path")
    autoplan.add_argument("--autoplan-path", dest="autoplan_path")
    autoplan.add_argument("--board-path", default="docs/status/EXECUTION_BOARD.md")
    autoplan.set_defaults(func=cmd_autoplan)

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
