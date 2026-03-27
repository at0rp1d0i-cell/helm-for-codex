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

    items: list[str] = []
    for line in section.strip().splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        while stripped.startswith("- "):
            stripped = stripped[2:].strip()
        items.append(stripped)
    return items


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


def cmd_sprint_contract(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    content = (
        f"# Sprint Contract: {args.title}\n\n"
        "## Planner\n\n"
        "Planner owns the task plan and acceptance contract.\n\n"
        f"{args.planner}\n\n"
        "## Generator\n\n"
        "Generator owns implementation output only.\n\n"
        f"{args.generator}\n\n"
        "## Evaluator\n\n"
        "Evaluator owns verification and writeback evidence.\n\n"
        f"{args.evaluator}\n\n"
        "## Scope\n\n"
        f"{args.scope}\n\n"
        "## Acceptance Criteria\n\n"
        f"{args.acceptance}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_implementation_report(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    content = (
        f"# Implementation Report: {args.title}\n\n"
        "## Consumed Sprint Contract\n\n"
        f"{args.sprint_contract}\n\n"
        "## Generator Summary\n\n"
        f"{args.summary}\n\n"
        "## Files Touched\n\n"
        f"{args.files_touched}\n\n"
        "## Tests Run\n\n"
        f"{args.tests_run}\n\n"
        "## Follow-Ups\n\n"
        f"{args.follow_ups}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_docs_sync_report(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    content = (
        f"# Docs Sync Report: {args.title}\n\n"
        "## Consumed Implementation Report\n\n"
        f"{args.implementation_report}\n\n"
        "## Consumed QA Report\n\n"
        f"{args.qa_report}\n\n"
        "## Docs Updated\n\n"
        f"{args.docs_updated}\n\n"
        "## Canonical Writeback\n\n"
        f"{args.canonical_writeback}\n\n"
        "## Follow-Ups\n\n"
        f"{args.follow_ups}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_release_gate(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    verification_status = "\n".join(f"- {item}" for item in args.verification_status)
    readiness_checklist = "\n".join(f"- {item}" for item in args.readiness_checklist)
    blocking_risks = "\n".join(f"- {item}" for item in args.blocking_risk) if args.blocking_risk else "- none"
    mitigations = "\n".join(f"- {item}" for item in args.mitigation) if args.mitigation else "- none"
    content = (
        f"# Release Gate: {args.title}\n\n"
        "## Consumed Implementation Report\n\n"
        f"{args.implementation_report}\n\n"
        "## Consumed QA Report\n\n"
        f"{args.qa_report}\n\n"
        "## Consumed Docs Sync Report\n\n"
        f"{args.docs_sync_report}\n\n"
        "## Verification Status\n\n"
        f"{verification_status}\n\n"
        "## Coverage Posture\n\n"
        f"{args.coverage_posture}\n\n"
        "## Version/Changelog Readiness\n\n"
        f"{args.version_changelog_readiness}\n\n"
        "## Merge/PR Prep\n\n"
        f"{args.merge_pr_prep}\n\n"
        "## Readiness Checklist\n\n"
        f"{readiness_checklist}\n\n"
        "## Blocking Risks\n\n"
        f"{blocking_risks}\n\n"
        "## Mitigations\n\n"
        f"{mitigations}\n\n"
        "## Verdict\n\n"
        f"{args.verdict}\n\n"
        "## Recommendation\n\n"
        f"{args.recommendation}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_dispatch_packet(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    consumed_artifacts = "\n".join(f"- {item}" for item in args.consumed_artifact)
    bridge_agent_type = args.bridge_agent_type or "unresolved"
    bridge_model = args.bridge_model or "unresolved"
    bridge_reasoning_effort = args.bridge_reasoning_effort or "unresolved"
    role_skill = args.role_skill or "unresolved"
    role_metadata = args.role_metadata or "unresolved"
    role_writeback_target = args.role_writeback_target or "unresolved"
    role_writeback_command = args.role_writeback_command or "unresolved"
    content = (
        f"# Dispatch Packet: {args.title}\n\n"
        "## Role\n\n"
        f"{args.role}\n\n"
        "## Logical Role\n\n"
        f"{args.logical_role}\n\n"
        "## Invocation Bridge\n\n"
        f"- agent_type: {bridge_agent_type}\n"
        f"- model: {bridge_model}\n"
        f"- reasoning_effort: {bridge_reasoning_effort}\n\n"
        "## Runtime Role Binding\n\n"
        f"- skill: {role_skill}\n"
        f"- metadata: {role_metadata}\n"
        f"- canonical_writeback_target: {role_writeback_target}\n"
        f"- canonical_writeback_command: {role_writeback_command}\n\n"
        "## Objective\n\n"
        f"{args.objective}\n\n"
        "## Consumed Artifacts\n\n"
        f"{consumed_artifacts}\n\n"
        "## Constraints\n\n"
        f"{args.constraints}\n\n"
        "## Expected Output\n\n"
        f"{args.expected_output}\n\n"
        "## Writeback Target\n\n"
        f"{args.writeback_target}\n\n"
        "## Completion Command\n\n"
        f"{args.completion_command}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_invocation_spec(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    consumed_artifacts = "\n".join(f"- {item}" for item in args.consumed_artifact)
    bridge_agent_type = args.bridge_agent_type or "unresolved"
    bridge_model = args.bridge_model or "unresolved"
    bridge_reasoning_effort = args.bridge_reasoning_effort or "unresolved"
    content = (
        f"# Invocation Spec: {args.title}\n\n"
        "## Role\n\n"
        f"{args.role}\n\n"
        "## Logical Role\n\n"
        f"{args.logical_role}\n\n"
        "## Source Packet\n\n"
        f"{args.source_packet}\n\n"
        "## Invocation Bridge\n\n"
        f"- agent_type: {bridge_agent_type}\n"
        f"- model: {bridge_model}\n"
        f"- reasoning_effort: {bridge_reasoning_effort}\n\n"
        "## Runtime Skill\n\n"
        f"{args.runtime_skill}\n\n"
        "## Role Metadata\n\n"
        f"{args.metadata}\n\n"
        "## Consumed Artifacts\n\n"
        f"{consumed_artifacts}\n\n"
        "## Expected Writeback Target\n\n"
        f"{args.expected_writeback_target}\n\n"
        "## Expected Writeback Command\n\n"
        f"{args.expected_writeback_command}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_execution_receipt(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    follow_ups = "\n".join(f"- {item}" for item in args.follow_up) if args.follow_up else "- none"
    content = (
        f"# Execution Receipt: {args.title}\n\n"
        "## Role\n\n"
        f"{args.role}\n\n"
        "## Logical Role\n\n"
        f"{args.logical_role}\n\n"
        "## Source Packet\n\n"
        f"{args.source_packet}\n\n"
        "## Invocation Spec\n\n"
        f"{args.invocation_spec}\n\n"
        "## Launch Payload\n\n"
        f"{args.launch_payload}\n\n"
        "## Execution Status\n\n"
        f"{args.execution_status}\n\n"
        "## Expected Writeback Target\n\n"
        f"{args.expected_writeback_target}\n\n"
        "## Writeback Status\n\n"
        f"{args.writeback_status}\n\n"
        "## Specialist Note\n\n"
        f"{args.specialist_note}\n\n"
        "## Follow-Ups\n\n"
        f"{follow_ups}\n"
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


def cmd_autoplan_report(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    review_passes = "\n".join(f"- {item}" for item in args.review_pass) if args.review_pass else "- none"
    review_packets = (
        "\n".join(f"- {item}" for item in args.review_packet)
        if args.review_packet
        else "- none"
    )
    invocation_specs = (
        "\n".join(f"- {item}" for item in args.invocation_spec)
        if args.invocation_spec
        else "- none"
    )
    review_results = (
        "\n".join(f"- {item}" for item in args.review_result)
        if args.review_result
        else "- none"
    )
    blocking_issues = (
        "\n".join(f"- {item}" for item in args.blocking_issue)
        if args.blocking_issue
        else "- none"
    )
    auto_decisions = (
        "\n".join(f"- {item}" for item in args.auto_decision)
        if args.auto_decision
        else "- none"
    )
    taste_decisions = (
        "\n".join(f"- {item}" for item in args.taste_decision)
        if args.taste_decision
        else "- none"
    )
    next_action = (
        getattr(args, "next_action", None)
        or getattr(args, "next_step", None)
        or "not provided"
    )
    next_step = (
        getattr(args, "next_step", None)
        or getattr(args, "next_action", None)
        or "not provided"
    )
    content = (
        f"# Autoplan Report: {args.title}\n\n"
        "## Mode\n\n"
        f"{args.mode}\n\n"
        "## Outcome\n\n"
        f"{args.outcome}\n\n"
        "## Discovery Brief\n\n"
        f"{args.discovery_brief or 'not written'}\n\n"
        "## Plan Brief\n\n"
        f"{args.plan_brief}\n\n"
        "## Review Passes\n\n"
        f"{review_passes}\n\n"
        "## Review Packets\n\n"
        f"{review_packets}\n\n"
        "## Invocation Specs\n\n"
        f"{invocation_specs}\n\n"
        "## Review Results\n\n"
        f"{review_results}\n\n"
        "## Review Gate\n\n"
        f"{args.review_gate or 'not written'}\n\n"
        "## Auto Decisions\n\n"
        f"{auto_decisions}\n\n"
        "## Taste Decisions\n\n"
        f"{taste_decisions}\n\n"
        "## Blocking Issues\n\n"
        f"{blocking_issues}\n\n"
        "## Next Action\n\n"
        f"{next_action}\n\n"
        "## Next Step\n\n"
        f"{next_step}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_review_pass(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    findings = "\n".join(f"- {item}" for item in args.finding)
    auto_decisions = "\n".join(f"- {item}" for item in args.auto_decision)
    taste_decisions = (
        "\n".join(f"- {item}" for item in args.taste_decision)
        if args.taste_decision
        else "- none"
    )
    content = (
        f"# Review Pass: {args.title}\n\n"
        "## Role\n\n"
        f"{args.role}\n\n"
        "## Focus\n\n"
        f"{args.focus}\n\n"
        "## Findings\n\n"
        f"{findings}\n\n"
        "## Auto Decisions\n\n"
        f"{auto_decisions}\n\n"
        "## Taste Decisions\n\n"
        f"{taste_decisions}\n\n"
        "## Recommendation\n\n"
        f"{args.recommendation}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_review_result(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    findings = "\n".join(f"- {item}" for item in args.finding)
    auto_decisions = "\n".join(f"- {item}" for item in args.auto_decision)
    taste_decisions = (
        "\n".join(f"- {item}" for item in args.taste_decision)
        if args.taste_decision
        else "- none"
    )
    content = (
        f"# Review Result: {args.title}\n\n"
        "## Role\n\n"
        f"{args.role}\n\n"
        "## Focus\n\n"
        f"{args.focus}\n\n"
        "## Findings\n\n"
        f"{findings}\n\n"
        "## Auto Decisions\n\n"
        f"{auto_decisions}\n\n"
        "## Taste Decisions\n\n"
        f"{taste_decisions}\n\n"
        "## Recommendation\n\n"
        f"{args.recommendation}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_review_packet(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    canonical_sources = "\n".join(f"- {item}" for item in args.canonical_source)
    bridge_agent_type = args.bridge_agent_type or "unresolved"
    bridge_model = args.bridge_model or "unresolved"
    bridge_reasoning_effort = args.bridge_reasoning_effort or "unresolved"
    role_skill = args.role_skill or "unresolved"
    role_metadata = args.role_metadata or "unresolved"
    role_writeback_target = args.role_writeback_target or "unresolved"
    role_writeback_command = args.role_writeback_command or "unresolved"
    content = (
        f"# Review Packet: {args.title}\n\n"
        "## Role\n\n"
        f"{args.role}\n\n"
        "## Logical Role\n\n"
        f"{args.logical_role}\n\n"
        "## Invocation Bridge\n\n"
        f"- agent_type: {bridge_agent_type}\n"
        f"- model: {bridge_model}\n"
        f"- reasoning_effort: {bridge_reasoning_effort}\n\n"
        "## Runtime Role Binding\n\n"
        f"- skill: {role_skill}\n"
        f"- metadata: {role_metadata}\n"
        f"- canonical_writeback_target: {role_writeback_target}\n"
        f"- canonical_writeback_command: {role_writeback_command}\n\n"
        "## Objective\n\n"
        f"{args.objective}\n\n"
        "## Canonical Sources\n\n"
        f"{canonical_sources}\n\n"
        "## Plan Brief\n\n"
        f"{args.plan_brief}\n\n"
        "## Expected Output\n\n"
        f"{args.expected_output}\n\n"
        "## Writeback Target\n\n"
        f"{args.writeback}\n\n"
        "## Writeback Command\n\n"
        f"{args.writeback_command}\n"
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


def cmd_onboarding_state(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    pending = args.pending or []
    pending_output = "\n".join(f"- {item}" for item in pending) if pending else "- none"
    content = (
        f"# Onboarding State: {args.title}\n\n"
        "## Stage\n\n"
        f"{args.stage}\n\n"
        "## Last Scan\n\n"
        f"{args.last_scan or 'none yet'}\n\n"
        "## Pending Decisions\n\n"
        f"{pending_output}\n\n"
        "## Notes\n\n"
        f"{args.notes}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_onboarding_report(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    findings = "\n".join(f"- {item}" for item in args.findings)
    recommendations = "\n".join(f"- {item}" for item in args.recommendations)
    plans = "\n".join(f"- {item}" for item in args.next_steps)
    content = (
        f"# Onboarding Report: {args.title}\n\n"
        "## Summary\n\n"
        f"{args.summary}\n\n"
        "## Key Findings\n\n"
        f"{findings}\n\n"
        "## Recommendations\n\n"
        f"{recommendations}\n\n"
        "## Next Steps\n\n"
        f"{plans}\n"
    )
    _write(out, content)
    print(f"wrote {out}")
    return 0


def cmd_deep_scan_plan(args: argparse.Namespace) -> int:
    out = _resolve_path(args.root, args.output)
    probes = "\n".join(f"- {item}" for item in args.probes)
    evidence = "\n".join(f"- {item}" for item in args.evidence)
    escalation = "\n".join(f"- {item}" for item in args.escalation) if args.escalation else "- none"
    writebacks = "\n".join(f"- {item}" for item in args.writeback_targets)
    content = (
        f"# Deep Scan Plan: {args.title}\n\n"
        "## Goals\n\n"
        f"{args.goals}\n\n"
        "## Hypotheses\n\n"
        f"{args.hypotheses}\n\n"
        "## Probes\n\n"
        f"{probes}\n\n"
        "## Expected Evidence\n\n"
        f"{evidence}\n\n"
        "## Risk Level\n\n"
        f"{args.risk_level}\n\n"
        "## Escalation Points\n\n"
        f"{escalation}\n\n"
        "## Writeback Targets\n\n"
        f"{writebacks}\n"
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

    sprint_contract = subparsers.add_parser(
        "sprint-contract",
        help="Create sprint contract markdown",
    )
    sprint_contract.add_argument("--output", required=True)
    sprint_contract.add_argument("--title", required=True)
    sprint_contract.add_argument("--planner", required=True)
    sprint_contract.add_argument("--generator", required=True)
    sprint_contract.add_argument("--evaluator", required=True)
    sprint_contract.add_argument("--scope", required=True)
    sprint_contract.add_argument("--acceptance", required=True)
    sprint_contract.set_defaults(func=cmd_sprint_contract)

    implementation_report = subparsers.add_parser(
        "implementation-report",
        help="Create implementation report markdown",
    )
    implementation_report.add_argument("--output", required=True)
    implementation_report.add_argument("--title", required=True)
    implementation_report.add_argument(
        "--sprint-contract",
        required=True,
        dest="sprint_contract",
    )
    implementation_report.add_argument("--summary", required=True)
    implementation_report.add_argument("--files-touched", required=True, dest="files_touched")
    implementation_report.add_argument("--tests-run", required=True, dest="tests_run")
    implementation_report.add_argument("--follow-ups", required=True, dest="follow_ups")
    implementation_report.set_defaults(func=cmd_implementation_report)

    docs_sync_report = subparsers.add_parser(
        "docs-sync-report",
        help="Create docs sync report markdown",
    )
    docs_sync_report.add_argument("--output", required=True)
    docs_sync_report.add_argument("--title", required=True)
    docs_sync_report.add_argument(
        "--implementation-report",
        required=True,
        dest="implementation_report",
    )
    docs_sync_report.add_argument("--qa-report", required=True, dest="qa_report")
    docs_sync_report.add_argument("--docs-updated", required=True, dest="docs_updated")
    docs_sync_report.add_argument(
        "--canonical-writeback",
        required=True,
        dest="canonical_writeback",
    )
    docs_sync_report.add_argument("--follow-ups", required=True, dest="follow_ups")
    docs_sync_report.set_defaults(func=cmd_docs_sync_report)

    release_gate = subparsers.add_parser(
        "release-gate",
        help="Create release gate markdown",
    )
    release_gate.add_argument("--output", required=True)
    release_gate.add_argument("--title", required=True)
    release_gate.add_argument(
        "--implementation-report",
        required=True,
        dest="implementation_report",
    )
    release_gate.add_argument("--qa-report", required=True, dest="qa_report")
    release_gate.add_argument(
        "--docs-sync-report",
        required=True,
        dest="docs_sync_report",
    )
    release_gate.add_argument(
        "--readiness-checklist",
        action="append",
        default=[],
        required=True,
        dest="readiness_checklist",
    )
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
    release_gate.add_argument("--blocking-risk", action="append", default=[], dest="blocking_risk")
    release_gate.add_argument("--mitigation", action="append", default=[], dest="mitigation")
    release_gate.add_argument("--verdict", required=True)
    release_gate.add_argument("--recommendation", required=True)
    release_gate.set_defaults(func=cmd_release_gate)

    dispatch_packet = subparsers.add_parser(
        "dispatch-packet",
        help="Create a specialist dispatch packet markdown",
    )
    dispatch_packet.add_argument("--output", required=True)
    dispatch_packet.add_argument("--title", required=True)
    dispatch_packet.add_argument("--role", required=True)
    dispatch_packet.add_argument("--logical-role", required=True, dest="logical_role")
    dispatch_packet.add_argument("--bridge-agent-type", dest="bridge_agent_type")
    dispatch_packet.add_argument("--bridge-model", dest="bridge_model")
    dispatch_packet.add_argument("--bridge-reasoning-effort", dest="bridge_reasoning_effort")
    dispatch_packet.add_argument("--role-skill", dest="role_skill")
    dispatch_packet.add_argument("--role-metadata", dest="role_metadata")
    dispatch_packet.add_argument("--role-writeback-target", dest="role_writeback_target")
    dispatch_packet.add_argument("--role-writeback-command", dest="role_writeback_command")
    dispatch_packet.add_argument("--objective", required=True)
    dispatch_packet.add_argument(
        "--consumed-artifact",
        action="append",
        default=[],
        required=True,
        dest="consumed_artifact",
    )
    dispatch_packet.add_argument("--constraints", required=True)
    dispatch_packet.add_argument("--expected-output", required=True, dest="expected_output")
    dispatch_packet.add_argument("--writeback-target", required=True, dest="writeback_target")
    dispatch_packet.add_argument("--completion-command", required=True, dest="completion_command")
    dispatch_packet.set_defaults(func=cmd_dispatch_packet)

    invocation_spec = subparsers.add_parser(
        "invocation-spec",
        help="Create a live invocation spec for bridge-backed specialist dispatch",
    )
    invocation_spec.add_argument("--output", required=True)
    invocation_spec.add_argument("--title", required=True)
    invocation_spec.add_argument("--role", required=True)
    invocation_spec.add_argument("--logical-role", required=True, dest="logical_role")
    invocation_spec.add_argument("--source-packet", required=True, dest="source_packet")
    invocation_spec.add_argument("--bridge-agent-type", dest="bridge_agent_type")
    invocation_spec.add_argument("--bridge-model", dest="bridge_model")
    invocation_spec.add_argument("--bridge-reasoning-effort", dest="bridge_reasoning_effort")
    invocation_spec.add_argument("--runtime-skill", required=True, dest="runtime_skill")
    invocation_spec.add_argument("--metadata", required=True)
    invocation_spec.add_argument(
        "--consumed-artifact",
        action="append",
        default=[],
        required=True,
        dest="consumed_artifact",
    )
    invocation_spec.add_argument(
        "--expected-writeback-target",
        required=True,
        dest="expected_writeback_target",
    )
    invocation_spec.add_argument(
        "--expected-writeback-command",
        required=True,
        dest="expected_writeback_command",
    )
    invocation_spec.set_defaults(func=cmd_invocation_spec)

    execution_receipt = subparsers.add_parser(
        "execution-receipt",
        help="Create an execution receipt for a live bridge-backed specialist run",
    )
    execution_receipt.add_argument("--output", required=True)
    execution_receipt.add_argument("--title", required=True)
    execution_receipt.add_argument("--role", required=True)
    execution_receipt.add_argument("--logical-role", required=True, dest="logical_role")
    execution_receipt.add_argument("--source-packet", required=True, dest="source_packet")
    execution_receipt.add_argument("--invocation-spec", required=True, dest="invocation_spec")
    execution_receipt.add_argument("--launch-payload", required=True, dest="launch_payload")
    execution_receipt.add_argument("--execution-status", required=True, dest="execution_status")
    execution_receipt.add_argument(
        "--expected-writeback-target",
        required=True,
        dest="expected_writeback_target",
    )
    execution_receipt.add_argument("--writeback-status", required=True, dest="writeback_status")
    execution_receipt.add_argument("--specialist-note", required=True, dest="specialist_note")
    execution_receipt.add_argument("--follow-up", action="append", default=[], dest="follow_up")
    execution_receipt.set_defaults(func=cmd_execution_receipt)

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

    autoplan_report = subparsers.add_parser(
        "autoplan-report",
        help="Create autoplan status report markdown",
    )
    autoplan_report.add_argument("--output", required=True)
    autoplan_report.add_argument("--title", required=True)
    autoplan_report.add_argument("--mode", choices=["run", "prepare", "collect"], default="run")
    autoplan_report.add_argument(
        "--outcome",
        choices=["auto-clear", "ask-user", "in-review", "blocked"],
        required=True,
    )
    autoplan_report.add_argument("--discovery-brief", dest="discovery_brief")
    autoplan_report.add_argument("--plan-brief", required=True, dest="plan_brief")
    autoplan_report.add_argument("--review-pass", action="append", default=[], dest="review_pass")
    autoplan_report.add_argument(
        "--review-packet",
        action="append",
        default=[],
        dest="review_packet",
    )
    autoplan_report.add_argument(
        "--invocation-spec",
        action="append",
        default=[],
        dest="invocation_spec",
    )
    autoplan_report.add_argument(
        "--review-result",
        action="append",
        default=[],
        dest="review_result",
    )
    autoplan_report.add_argument("--review-gate", dest="review_gate")
    autoplan_report.add_argument(
        "--auto-decision",
        action="append",
        default=[],
        dest="auto_decision",
    )
    autoplan_report.add_argument(
        "--taste-decision",
        action="append",
        default=[],
        dest="taste_decision",
    )
    autoplan_report.add_argument(
        "--blocking-issue",
        action="append",
        default=[],
        dest="blocking_issue",
    )
    autoplan_report.add_argument("--next-action", dest="next_action")
    autoplan_report.add_argument("--next-step", dest="next_step")
    autoplan_report.set_defaults(func=cmd_autoplan_report)

    review_pass = subparsers.add_parser("review-pass", help="Create review pass markdown")
    review_pass.add_argument("--output", required=True)
    review_pass.add_argument("--title", required=True)
    review_pass.add_argument("--role", required=True)
    review_pass.add_argument("--focus", required=True)
    review_pass.add_argument("--finding", action="append", default=[], required=True)
    review_pass.add_argument("--auto-decision", action="append", default=[], required=True)
    review_pass.add_argument("--taste-decision", action="append", default=[])
    review_pass.add_argument("--recommendation", required=True)
    review_pass.set_defaults(func=cmd_review_pass)

    review_result = subparsers.add_parser(
        "review-result",
        help="Create review result markdown",
    )
    review_result.add_argument("--output", required=True)
    review_result.add_argument("--title", required=True)
    review_result.add_argument("--role", required=True)
    review_result.add_argument("--focus", required=True)
    review_result.add_argument("--finding", action="append", default=[], required=True)
    review_result.add_argument("--auto-decision", action="append", default=[], required=True)
    review_result.add_argument("--taste-decision", action="append", default=[])
    review_result.add_argument("--recommendation", required=True)
    review_result.set_defaults(func=cmd_review_result)

    review_packet = subparsers.add_parser(
        "review-packet",
        help="Create review packet markdown",
    )
    review_packet.add_argument("--output", required=True)
    review_packet.add_argument("--title", required=True)
    review_packet.add_argument("--role", required=True)
    review_packet.add_argument("--logical-role", required=True, dest="logical_role")
    review_packet.add_argument("--bridge-agent-type", dest="bridge_agent_type")
    review_packet.add_argument("--bridge-model", dest="bridge_model")
    review_packet.add_argument("--bridge-reasoning-effort", dest="bridge_reasoning_effort")
    review_packet.add_argument("--role-skill", dest="role_skill")
    review_packet.add_argument("--role-metadata", dest="role_metadata")
    review_packet.add_argument("--role-writeback-target", dest="role_writeback_target")
    review_packet.add_argument("--role-writeback-command", dest="role_writeback_command")
    review_packet.add_argument("--objective", required=True)
    review_packet.add_argument(
        "--canonical-source",
        action="append",
        default=[],
        required=True,
        dest="canonical_source",
    )
    review_packet.add_argument("--plan-brief", required=True, dest="plan_brief")
    review_packet.add_argument("--expected-output", required=True, dest="expected_output")
    review_packet.add_argument("--writeback", required=True)
    review_packet.add_argument("--writeback-command", required=True, dest="writeback_command")
    review_packet.set_defaults(func=cmd_review_packet)

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

    onboarding_state = subparsers.add_parser("onboarding-state", help="Create or update onboarding state")
    onboarding_state.add_argument("--output", required=True)
    onboarding_state.add_argument("--title", required=True)
    onboarding_state.add_argument("--stage", required=True)
    onboarding_state.add_argument("--last-scan", dest="last_scan")
    onboarding_state.add_argument("--pending", action="append", default=[])
    onboarding_state.add_argument("--notes", default="No additional notes.")
    onboarding_state.set_defaults(func=cmd_onboarding_state)

    onboarding_report = subparsers.add_parser("onboarding-report", help="Create onboarding report markdown")
    onboarding_report.add_argument("--output", required=True)
    onboarding_report.add_argument("--title", required=True)
    onboarding_report.add_argument("--summary", required=True)
    onboarding_report.add_argument("--findings", action="append", default=[], required=True)
    onboarding_report.add_argument("--recommendations", action="append", default=[], required=True)
    onboarding_report.add_argument("--next-steps", action="append", default=[], required=True)
    onboarding_report.set_defaults(func=cmd_onboarding_report)

    deep_scan = subparsers.add_parser("deep-scan-plan", help="Create deep scan plan markdown")
    deep_scan.add_argument("--output", required=True)
    deep_scan.add_argument("--title", required=True)
    deep_scan.add_argument("--goals", required=True)
    deep_scan.add_argument("--hypotheses", required=True)
    deep_scan.add_argument("--probes", action="append", default=[], required=True)
    deep_scan.add_argument("--evidence", action="append", default=[], required=True)
    deep_scan.add_argument("--risk-level", required=True)
    deep_scan.add_argument("--escalation", action="append", default=[])
    deep_scan.add_argument("--writeback-targets", action="append", default=[], required=True)
    deep_scan.set_defaults(func=cmd_deep_scan_plan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.root = args.root.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
