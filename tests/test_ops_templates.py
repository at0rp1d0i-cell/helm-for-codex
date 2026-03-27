import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_CHECK = ROOT / "ops" / "checks" / "check_docs_freshness.py"


def run_doc_check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DOC_CHECK), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )


def test_ops_templates_and_checks_exist() -> None:
    required = [
        ROOT / "ops" / "templates" / "task-brief.md",
        ROOT / "ops" / "templates" / "discovery-brief.md",
        ROOT / "ops" / "templates" / "plan-brief.md",
        ROOT / "ops" / "templates" / "sprint-contract.md",
        ROOT / "ops" / "templates" / "dispatch-packet.md",
        ROOT / "ops" / "templates" / "invocation-spec.md",
        ROOT / "ops" / "templates" / "execution-receipt.md",
        ROOT / "ops" / "templates" / "implementation-report.md",
        ROOT / "ops" / "templates" / "onboarding-state.md",
        ROOT / "ops" / "templates" / "onboarding-report.md",
        ROOT / "ops" / "templates" / "deep-scan-plan.md",
        ROOT / "ops" / "templates" / "review-gate.md",
        ROOT / "ops" / "templates" / "review-pass.md",
        ROOT / "ops" / "templates" / "review-packet.md",
        ROOT / "ops" / "templates" / "review-result.md",
        ROOT / "ops" / "templates" / "review-report.md",
        ROOT / "ops" / "templates" / "qa-report.md",
        ROOT / "ops" / "templates" / "qa-evidence.md",
        ROOT / "ops" / "templates" / "docs-sync-report.md",
        ROOT / "ops" / "templates" / "release-prep-report.md",
        ROOT / "ops" / "templates" / "refactor-proposal.md",
        ROOT / "ops" / "checks" / "check_docs_freshness.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []

    task_brief = (ROOT / "ops" / "templates" / "task-brief.md").read_text()
    assert "# Task Brief: <title>" in task_brief
    assert "<objective>" in task_brief
    assert "<writeback_target>" in task_brief

    discovery_brief = (ROOT / "ops" / "templates" / "discovery-brief.md").read_text()
    assert "# Discovery Brief: <title>" in discovery_brief
    assert "<problem_signal>" in discovery_brief
    assert "<recommendation_target>" in discovery_brief

    plan_brief = (ROOT / "ops" / "templates" / "plan-brief.md").read_text()
    assert "# Plan Brief: <title>" in plan_brief
    assert "<modules_in_scope>" in plan_brief
    assert "<writeback_target>" in plan_brief

    sprint_contract = (ROOT / "ops" / "templates" / "sprint-contract.md").read_text()
    assert "# Sprint Contract: <title>" in sprint_contract
    assert "Planner owns the task plan and acceptance contract." in sprint_contract
    assert "<planner_role>" in sprint_contract
    assert "Generator owns implementation output only." in sprint_contract
    assert "<generator_role>" in sprint_contract
    assert "Evaluator owns verification and writeback evidence." in sprint_contract
    assert "<evaluator_role>" in sprint_contract
    assert "<acceptance_criteria>" in sprint_contract

    dispatch_packet = (ROOT / "ops" / "templates" / "dispatch-packet.md").read_text()
    assert "# Dispatch Packet: <title>" in dispatch_packet
    assert "<role>" in dispatch_packet
    assert "<logical_role>" in dispatch_packet
    assert "<bridge_agent_type>" in dispatch_packet
    assert "<bridge_model>" in dispatch_packet
    assert "<bridge_reasoning_effort>" in dispatch_packet
    assert "<role_skill>" in dispatch_packet
    assert "<role_metadata>" in dispatch_packet
    assert "<role_writeback_target>" in dispatch_packet
    assert "<role_writeback_command>" in dispatch_packet
    assert "<consumed_artifacts>" in dispatch_packet
    assert "<writeback_target>" in dispatch_packet
    assert "<completion_command>" in dispatch_packet

    invocation_spec = (ROOT / "ops" / "templates" / "invocation-spec.md").read_text()
    assert "# Invocation Spec: <title>" in invocation_spec
    assert "<logical_role>" in invocation_spec
    assert "<source_packet>" in invocation_spec
    assert "<bridge_agent_type>" in invocation_spec
    assert "<bridge_model>" in invocation_spec
    assert "<bridge_reasoning_effort>" in invocation_spec
    assert "<runtime_skill>" in invocation_spec
    assert "<metadata>" in invocation_spec
    assert "<consumed_artifacts>" in invocation_spec
    assert "<expected_writeback_target>" in invocation_spec
    assert "<expected_writeback_command>" in invocation_spec

    execution_receipt = (ROOT / "ops" / "templates" / "execution-receipt.md").read_text()
    assert "# Execution Receipt: <title>" in execution_receipt
    assert "<logical_role>" in execution_receipt
    assert "<source_packet>" in execution_receipt
    assert "<invocation_spec>" in execution_receipt
    assert "<launch_payload>" in execution_receipt
    assert "<execution_status>" in execution_receipt
    assert "<expected_writeback_target>" in execution_receipt
    assert "<writeback_status>" in execution_receipt
    assert "<specialist_note>" in execution_receipt
    assert "<follow_ups>" in execution_receipt

    implementation_report = (ROOT / "ops" / "templates" / "implementation-report.md").read_text()
    assert "# Implementation Report: <title>" in implementation_report
    assert "## Consumed Sprint Contract" in implementation_report
    assert "<sprint_contract_path>" in implementation_report
    assert "## Generator Summary" in implementation_report
    assert "<files_touched>" in implementation_report
    assert "<tests_run>" in implementation_report

    review_gate = (ROOT / "ops" / "templates" / "review-gate.md").read_text()
    assert "# Review Gate: <title>" in review_gate
    assert "<review_passes>" in review_gate
    assert "<taste_decisions>" in review_gate
    assert "<approval_target>" in review_gate

    review_pass = (ROOT / "ops" / "templates" / "review-pass.md").read_text()
    assert "# Review Pass: <title>" in review_pass
    assert "<role>" in review_pass
    assert "<auto_decisions>" in review_pass
    assert "<taste_decisions>" in review_pass

    review_packet = (ROOT / "ops" / "templates" / "review-packet.md").read_text()
    assert "# Review Packet: <title>" in review_packet
    assert "<role>" in review_packet
    assert "<logical_role>" in review_packet
    assert "<bridge_agent_type>" in review_packet
    assert "<bridge_model>" in review_packet
    assert "<bridge_reasoning_effort>" in review_packet
    assert "<role_skill>" in review_packet
    assert "<role_metadata>" in review_packet
    assert "<role_writeback_target>" in review_packet
    assert "<role_writeback_command>" in review_packet
    assert "<objective>" in review_packet
    assert "<canonical_sources>" in review_packet
    assert "<plan_brief_path>" in review_packet
    assert "<expected_output>" in review_packet
    assert "<writeback_target>" in review_packet
    assert "## Writeback Command" in review_packet
    assert "<writeback_command>" in review_packet
    assert "scripts/team_state.py review-pass" in review_packet
    assert "Preferred canonical path: `docs/plans/review-passes/<role>.md`" in review_packet

    review_result = (ROOT / "ops" / "templates" / "review-result.md").read_text()
    assert "# Review Result: <title>" in review_result
    assert "<role>" in review_result
    assert "<focus>" in review_result
    assert "<findings>" in review_result
    assert "<auto_decisions>" in review_result
    assert "<taste_decisions>" in review_result
    assert "<recommendation>" in review_result

    onboarding_state = (ROOT / "ops" / "templates" / "onboarding-state.md").read_text()
    assert "# Onboarding State: <title>" in onboarding_state
    assert "<stage>" in onboarding_state
    assert "<pending_decisions>" in onboarding_state
    assert "<notes>" in onboarding_state

    onboarding_report = (ROOT / "ops" / "templates" / "onboarding-report.md").read_text()
    assert "# Onboarding Report: <title>" in onboarding_report
    assert "<summary>" in onboarding_report
    assert "<findings>" in onboarding_report
    assert "<recommendations>" in onboarding_report
    assert "<next_steps>" in onboarding_report

    deep_scan_plan = (ROOT / "ops" / "templates" / "deep-scan-plan.md").read_text()
    assert "# Deep Scan Plan: <title>" in deep_scan_plan
    assert "<goals>" in deep_scan_plan
    assert "<hypotheses>" in deep_scan_plan
    assert "<probes>" in deep_scan_plan
    assert "<evidence>" in deep_scan_plan

    qa_report = (ROOT / "ops" / "templates" / "qa-report.md").read_text()
    assert "# QA Report" in qa_report
    assert "## Consumed Sprint Contract" in qa_report
    assert "<sprint_contract_path>" in qa_report
    assert "## Consumed Implementation Report" in qa_report
    assert "<implementation_report_path>" in qa_report
    assert "## Consumed QA Dispatch Packet" in qa_report
    assert "<qa_dispatch_packet_path>" in qa_report
    assert "QA must validate the generator output against the consumed artifacts before board advancement." in qa_report
    assert "## QA Evidence Report" in qa_report
    assert "<qa_evidence_report_path>" in qa_report
    assert "## Browser Evidence Status" in qa_report
    assert "<browser_evidence_status>" in qa_report
    assert "<verification_status>" in qa_report

    qa_evidence = (ROOT / "ops" / "templates" / "qa-evidence.md").read_text()
    assert "# QA Evidence" in qa_evidence
    assert "## Consumed QA Report" in qa_evidence
    assert "<qa_report_path>" in qa_evidence
    assert "## Consumed QA Dispatch Packet" in qa_evidence
    assert "<qa_dispatch_packet_path>" in qa_evidence
    assert "## Consumed Sprint Contract" in qa_evidence
    assert "<sprint_contract_path>" in qa_evidence
    assert "## Consumed Implementation Report" in qa_evidence
    assert "<implementation_report_path>" in qa_evidence
    assert "repo-backed browser evidence paths" in qa_evidence
    assert "## Evidence Mode" in qa_evidence
    assert "<evidence_mode>" in qa_evidence
    assert "## Browser Evidence Status" in qa_evidence
    assert "<browser_evidence_status>" in qa_evidence
    assert "## Screenshot Placeholders" in qa_evidence
    assert "<screenshot_placeholders>" in qa_evidence
    assert "## Additional Artifact Placeholders" in qa_evidence
    assert "<artifact_placeholders>" in qa_evidence
    assert "## Notes" in qa_evidence
    assert "<notes>" in qa_evidence

    docs_sync_report = (ROOT / "ops" / "templates" / "docs-sync-report.md").read_text()
    assert "# Docs Sync Report: <title>" in docs_sync_report
    assert "## Consumed Implementation Report" in docs_sync_report
    assert "<implementation_report_path>" in docs_sync_report
    assert "## Consumed QA Report" in docs_sync_report
    assert "<qa_report_path>" in docs_sync_report
    assert "<canonical_writeback_target>" in docs_sync_report

    release_prep_report = (ROOT / "ops" / "templates" / "release-prep-report.md").read_text()
    assert "# Release Prep Report: <title>" in release_prep_report
    assert "<implementation_report_path>" in release_prep_report
    assert "<qa_report_path>" in release_prep_report
    assert "<docs_sync_report_path>" in release_prep_report
    assert "<verification_plan>" in release_prep_report
    assert "<coverage_plan>" in release_prep_report
    assert "<version_changelog_plan>" in release_prep_report
    assert "<merge_pr_plan>" in release_prep_report
    assert "<readiness_checklist>" in release_prep_report
    assert "<follow_ups>" in release_prep_report

    refactor = (ROOT / "ops" / "templates" / "refactor-proposal.md").read_text()
    assert "# Refactor Proposal" in refactor
    assert "<problem_scope>" in refactor
    assert "<minimum_intervention>" in refactor


def test_check_docs_freshness_validates_structure() -> None:
    result = run_doc_check(ROOT)
    assert result.returncode == 0
    assert "docs structure ok" in result.stdout
    assert "docs freshness baseline ok" not in result.stdout


def test_check_docs_freshness_rejects_board_without_preamble(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True)
    (tmp_path / "docs" / "status").mkdir(parents=True)

    files = {
        "docs/project/PROJECT_BRIEF.md": "# Project Brief\n\n## Problem\n\nx\n\n## Current Goal\n\nship phase 3\n\n## Success Criteria\n\ny\n",
        "docs/project/ROADMAP.md": "# Roadmap\n\n## Current Milestone\n\nx\n\n## Later Milestones\n\ny\n",
        "docs/project/ARCHITECTURE.md": "# Architecture\n\n## Modules\n\nx\n\n## Constraints\n\ny\n",
        "docs/project/QUALITY_BAR.md": "# Quality Bar\n\n## Code\n\nx\n\n## Tests\n\ny\n\n## Docs\n\nz\n",
        "docs/status/ONBOARDING_STATE.md": "# Onboarding State: x\n\n## Stage\n\nadopted\n\n## Last Scan\n\nphase-12\n\n## Pending Decisions\n\n- none\n\n## Notes\n\nready\n",
        "docs/status/EXECUTION_BOARD.md": "# Execution Board\n\n## Current Stage\n\nplan\n\n## Active Work\n\n- x\n\n## Completed\n\n- y\n",
    }
    for relpath, content in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    result = run_doc_check(tmp_path)
    assert result.returncode == 1
    assert "scripts/team_state.py board" in result.stdout


def test_check_docs_freshness_rejects_board_without_completed_section(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True)
    (tmp_path / "docs" / "status").mkdir(parents=True)

    files = {
        "docs/project/PROJECT_BRIEF.md": "# Project Brief\n\n## Problem\n\nx\n\n## Current Goal\n\nship phase 3\n\n## Success Criteria\n\ny\n",
        "docs/project/ROADMAP.md": "# Roadmap\n\n## Current Milestone\n\nx\n\n## Later Milestones\n\ny\n",
        "docs/project/ARCHITECTURE.md": "# Architecture\n\n## Modules\n\nx\n\n## Constraints\n\ny\n",
        "docs/project/QUALITY_BAR.md": "# Quality Bar\n\n## Code\n\nx\n\n## Tests\n\ny\n\n## Docs\n\nz\n",
        "docs/status/ONBOARDING_STATE.md": "# Onboarding State: x\n\n## Stage\n\nadopted\n\n## Last Scan\n\nphase-12\n\n## Pending Decisions\n\n- none\n\n## Notes\n\nready\n",
        "docs/status/EXECUTION_BOARD.md": "# Execution Board\n\n_This file can be updated manually or via `scripts/team_state.py board`._\n\n## Current Stage\n\nplan\n\n## Active Work\n\n- x\n",
    }
    for relpath, content in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    result = run_doc_check(tmp_path)
    assert result.returncode == 1
    assert "## Completed" in result.stdout


def test_check_docs_freshness_rejects_project_brief_without_current_goal(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True)
    (tmp_path / "docs" / "status").mkdir(parents=True)

    files = {
        "docs/project/PROJECT_BRIEF.md": "# Project Brief\n\n## Problem\n\nx\n\n## Success Criteria\n\ny\n",
        "docs/project/ROADMAP.md": "# Roadmap\n\n## Current Milestone\n\nx\n\n## Later Milestones\n\ny\n",
        "docs/project/ARCHITECTURE.md": "# Architecture\n\n## Modules\n\nx\n\n## Constraints\n\ny\n",
        "docs/project/QUALITY_BAR.md": "# Quality Bar\n\n## Code\n\nx\n\n## Tests\n\ny\n\n## Docs\n\nz\n",
        "docs/status/ONBOARDING_STATE.md": "# Onboarding State: x\n\n## Stage\n\nadopted\n\n## Last Scan\n\nphase-12\n\n## Pending Decisions\n\n- none\n\n## Notes\n\nready\n",
        "docs/status/EXECUTION_BOARD.md": "# Execution Board\n\n_This file can be updated manually or via `scripts/team_state.py board`._\n\n## Current Stage\n\nplan\n\n## Active Work\n\n- x\n\n## Completed\n\n- y\n",
    }
    for relpath, content in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    result = run_doc_check(tmp_path)
    assert result.returncode == 1
    assert "## Current Goal" in result.stdout


def test_check_docs_freshness_rejects_missing_onboarding_state_sections(tmp_path: Path) -> None:
    (tmp_path / "docs" / "project").mkdir(parents=True)
    (tmp_path / "docs" / "status").mkdir(parents=True)

    files = {
        "docs/project/PROJECT_BRIEF.md": "# Project Brief\n\n## Problem\n\nx\n\n## Current Goal\n\nship phase 12\n\n## Success Criteria\n\ny\n",
        "docs/project/ROADMAP.md": "# Roadmap\n\n## Current Milestone\n\nx\n\n## Later Milestones\n\ny\n",
        "docs/project/ARCHITECTURE.md": "# Architecture\n\n## Modules\n\nx\n\n## Constraints\n\ny\n",
        "docs/project/QUALITY_BAR.md": "# Quality Bar\n\n## Code\n\nx\n\n## Tests\n\ny\n\n## Docs\n\nz\n",
        "docs/status/ONBOARDING_STATE.md": "# Onboarding State: x\n\n## Stage\n\nadopted\n\n## Notes\n\nready\n",
        "docs/status/EXECUTION_BOARD.md": "# Execution Board\n\n_This file can be updated manually or via `scripts/team_state.py board`._\n\n## Current Stage\n\nplan\n\n## Active Work\n\n- x\n\n## Completed\n\n- y\n",
    }
    for relpath, content in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    result = run_doc_check(tmp_path)
    assert result.returncode == 1
    assert "## Last Scan" in result.stdout
