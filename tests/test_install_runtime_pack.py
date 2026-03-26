import subprocess
import sys
from pathlib import Path

import importlib.util


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install_runtime_pack.py"


def run_installer(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--target", str(target)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def run_runtime_lead_loop(target: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(target / "scripts" / "lead_loop.py"), "--root", str(target), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_installer_populates_runtime_dirs(tmp_path: Path) -> None:
    target = tmp_path / "project"
    result = run_installer(target)
    assert result.returncode == 0, result.stderr
    assert target.exists()

    assert (target / "AGENTS.md").exists()
    assert (target / ".codex" / "config.toml").exists()
    assert (target / ".codex" / "role_bridge.toml").exists()
    assert (target / ".codex" / "roles" / "ops-orchestrator.toml").exists()
    assert (target / ".codex" / "roles" / "product-reviewer.toml").exists()
    assert (target / ".codex" / "roles" / "architect-reviewer.toml").exists()
    assert (target / ".codex" / "roles" / "code-reviewer.toml").exists()
    assert (target / ".codex" / "roles" / "implementation-worker.toml").exists()
    assert (target / ".codex" / "roles" / "qa-runner.toml").exists()
    assert (target / ".codex" / "roles" / "docs-sync.toml").exists()

    assert (target / ".agents" / "skills" / "ops-orchestrator" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "ops-orchestrator" / "agents" / "openai.yaml").exists()
    assert (target / ".agents" / "skills" / "team-lead" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "product-discovery" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "architecture-review" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "code-reviewer" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "implementation-worker" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "implementation-worker" / "agents" / "openai.yaml").exists()
    assert (target / ".agents" / "skills" / "qa-runner" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "qa-runner" / "agents" / "openai.yaml").exists()
    assert (target / ".agents" / "skills" / "docs-sync" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "docs-sync" / "agents" / "openai.yaml").exists()
    assert (target / ".agents" / "skills" / "refactor-planner" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "refactor-planner" / "agents" / "openai.yaml").exists()
    assert (target / ".agents" / "skills" / "release-manager" / "SKILL.md").exists()
    assert (target / ".agents" / "skills" / "release-manager" / "agents" / "openai.yaml").exists()
    assert (target / ".agents" / "skills" / "team-lead" / "agents" / "openai.yaml").exists()

    assert (target / "scripts" / "team_state.py").exists()
    assert (target / "scripts" / "lead_loop.py").exists()
    assert (target / "scripts" / "ops_loop.py").exists()
    assert (target / "scripts" / "role_bridge.py").exists()
    assert (target / "scripts" / "role_review.py").exists()
    assert (target / "ops" / "templates" / "task-brief.md").exists()
    assert (target / "ops" / "templates" / "dispatch-packet.md").exists()
    assert (target / "ops" / "templates" / "invocation-spec.md").exists()
    assert (target / "ops" / "templates" / "onboarding-state.md").exists()
    assert (target / "ops" / "templates" / "deep-scan-plan.md").exists()
    assert (target / "ops" / "checks" / "check_docs_freshness.py").exists()

    assert (target / "docs" / "project" / "PROJECT_BRIEF.md").exists()
    assert (target / "docs" / "project" / "ARCHITECTURE.md").exists()
    assert (target / "docs" / "project" / "QUALITY_BAR.md").exists()
    assert (target / "docs" / "project" / "TECH_DEBT.md").exists()
    assert (target / "docs" / "status" / "EXECUTION_BOARD.md").exists()
    assert (target / "docs" / "status" / "ONBOARDING_STATE.md").exists()
    assert (target / "docs" / "status" / "MODULE_CONTRACTS").exists()
    assert (target / "docs" / "status" / "MODULE_CONTRACTS" / "README.md").exists()
    assert (target / "docs" / "plans").exists()

    assert (target / "docs" / "decisions").exists()

    assert (target / "docs" / "plans").exists()
    assert (target / "docs" / "plans" / "archive").exists()


def test_installer_preserves_existing_canonical_state(tmp_path: Path) -> None:
    target = tmp_path / "project"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr

    project_brief = target / "docs" / "project" / "PROJECT_BRIEF.md"
    onboarding_state = target / "docs" / "status" / "ONBOARDING_STATE.md"
    agents = target / "AGENTS.md"

    project_brief.write_text("# Project Brief\n\ncustom project state\n")
    onboarding_state.write_text("# Onboarding State: Custom\n\nmanual state\n")
    agents.write_text("# Project AGENTS\n\ncustom guidance\n")

    second = run_installer(target)
    assert second.returncode == 0, second.stderr

    assert project_brief.read_text() == "# Project Brief\n\ncustom project state\n"
    assert onboarding_state.read_text() == "# Onboarding State: Custom\n\nmanual state\n"
    assert agents.read_text() == "# Project AGENTS\n\ncustom guidance\n"


def test_copy_dir_is_noop_when_source_equals_destination(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location(
        "install_runtime_pack",
        SCRIPT,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    ops_dir = tmp_path / "ops" / "templates"
    ops_dir.mkdir(parents=True)
    marker = ops_dir / "marker.md"
    marker.write_text("present\n")

    module._copy_dir(ops_dir, ops_dir)

    assert marker.read_text() == "present\n"


def test_installed_runtime_supports_build_to_qa_to_docs_sync_handoff(tmp_path: Path) -> None:
    target = tmp_path / "project"
    result = run_installer(target)
    assert result.returncode == 0, result.stderr

    build = run_runtime_lead_loop(
        target,
        "build",
        "--title",
        "Phase 13 task 3",
        "--planner",
        "Lead owns the sprint contract and acceptance for one bounded task.",
        "--generator",
        "Builder implements the approved task and writes the implementation report.",
        "--evaluator",
        "QA evaluates the builder output against the sprint contract and implementation report.",
        "--scope",
        "Add QA handoff and defect loop only.",
        "--acceptance",
        "QA consumes the upstream artifacts and writes the canonical qa-report.",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-phase13-task3.md",
        "--builder-packet-path",
        "docs/plans/builder-dispatch-phase13-task3.md",
    )
    assert build.returncode == 0, build.stderr
    assert (target / "docs" / "plans" / "builder-dispatch-phase13-task3.md").exists()
    assert (target / "docs" / "plans" / "builder-dispatch-phase13-task3-invocation.md").exists()
    builder_packet = (target / "docs" / "plans" / "builder-dispatch-phase13-task3.md").read_text()
    assert "implementation-worker" in builder_packet
    assert "- agent_type: worker" in builder_packet
    builder_invocation = (
        target / "docs" / "plans" / "builder-dispatch-phase13-task3-invocation.md"
    ).read_text()
    assert ".agents/skills/implementation-worker/SKILL.md" in builder_invocation

    (target / "docs" / "plans" / "implementation-report-phase13-task3.md").write_text(
        "# Implementation Report: Phase 13 task 3\n\n"
        "## Consumed Sprint Contract\n\n"
        "docs/plans/sprint-contract-phase13-task3.md\n\n"
        "## Generator Summary\n\nBuilder completed the bounded task.\n\n"
        "## Files Touched\n\nscripts/lead_loop.py\n\n"
        "## Tests Run\n\nuv run pytest tests/test_lead_loop.py -q\n\n"
        "## Follow-Ups\n\nnone\n"
    )

    qa_prepare = run_runtime_lead_loop(
        target,
        "qa-prepare",
        "--title",
        "Phase 13 task 3",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-phase13-task3.md",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--qa-packet-path",
        "docs/plans/qa-dispatch-phase13-task3.md",
        "--qa-report-path",
        "docs/plans/qa-report-phase13-task3.md",
        "--environment",
        "Installed runtime repo",
        "--scenario",
        "Run the builder-to-QA handoff from the installed runtime",
    )
    assert qa_prepare.returncode == 0, qa_prepare.stderr
    assert (target / "docs" / "plans" / "qa-dispatch-phase13-task3.md").exists()
    assert (target / "docs" / "plans" / "qa-dispatch-phase13-task3-invocation.md").exists()
    qa_packet = (target / "docs" / "plans" / "qa-dispatch-phase13-task3.md").read_text()
    assert "qa-runner" in qa_packet
    assert "- agent_type: worker" in qa_packet

    qa = run_runtime_lead_loop(
        target,
        "qa",
        "--title",
        "Phase 13 task 3",
        "--sprint-contract-path",
        "docs/plans/sprint-contract-phase13-task3.md",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--qa-report-path",
        "docs/plans/qa-report-phase13-task3.md",
        "--environment",
        "Installed runtime repo",
        "--scenario",
        "Run the builder-to-QA handoff from the installed runtime",
        "--verification-status",
        "passed",
    )
    assert qa.returncode == 0, qa.stderr

    report = (target / "docs" / "plans" / "qa-report-phase13-task3.md").read_text()
    assert "docs/plans/sprint-contract-phase13-task3.md" in report
    assert "docs/plans/implementation-report-phase13-task3.md" in report
    assert "Run the builder-to-QA handoff from the installed runtime" in report

    docs_prepare = run_runtime_lead_loop(
        target,
        "docs-sync-prepare",
        "--title",
        "Phase 13 task 3",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--qa-report-path",
        "docs/plans/qa-report-phase13-task3.md",
        "--docs-sync-packet-path",
        "docs/plans/docs-sync-dispatch-phase13-task3.md",
        "--docs-sync-report-path",
        "docs/plans/docs-sync-report-phase13-task3.md",
        "--docs-updated",
        "docs/status/EXECUTION_BOARD.md",
        "--canonical-writeback",
        "docs/project/PROJECT_BRIEF.md",
        "--canonical-writeback",
        "docs/status/EXECUTION_BOARD.md",
    )
    assert docs_prepare.returncode == 0, docs_prepare.stderr
    assert (target / "docs" / "plans" / "docs-sync-dispatch-phase13-task3.md").exists()
    docs_packet = (target / "docs" / "plans" / "docs-sync-dispatch-phase13-task3.md").read_text()
    assert "docs-sync" in docs_packet
    assert "- agent_type: worker" in docs_packet

    docs_sync = run_runtime_lead_loop(
        target,
        "docs-sync",
        "--title",
        "Phase 13 task 3",
        "--implementation-report-path",
        "docs/plans/implementation-report-phase13-task3.md",
        "--qa-report-path",
        "docs/plans/qa-report-phase13-task3.md",
        "--docs-sync-report-path",
        "docs/plans/docs-sync-report-phase13-task3.md",
        "--docs-updated",
        "docs/status/EXECUTION_BOARD.md",
        "--canonical-writeback",
        "docs/project/PROJECT_BRIEF.md",
        "--canonical-writeback",
        "docs/status/EXECUTION_BOARD.md",
    )
    assert docs_sync.returncode == 0, docs_sync.stderr

    docs_sync_report = (target / "docs" / "plans" / "docs-sync-report-phase13-task3.md").read_text()
    assert "docs/plans/implementation-report-phase13-task3.md" in docs_sync_report
    assert "docs/plans/qa-report-phase13-task3.md" in docs_sync_report
    assert "- docs/project/PROJECT_BRIEF.md" in docs_sync_report

    board = (target / "docs" / "status" / "EXECUTION_BOARD.md").read_text()
    assert "## Current Stage\n\nship-ready" in board
