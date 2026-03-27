import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEAM_STATE = ROOT / "scripts" / "team_state.py"
BRIDGE_RUNNER = ROOT / "scripts" / "bridge_runner.py"


def run_team_state(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TEAM_STATE), "--root", str(tmp_path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def run_bridge_runner(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(BRIDGE_RUNNER), "--root", str(tmp_path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _seed_packet_and_spec(tmp_path: Path) -> None:
    packet = run_team_state(
        tmp_path,
        "dispatch-packet",
        "--output",
        "docs/plans/builder-dispatch-demo.md",
        "--title",
        "Demo builder dispatch",
        "--role",
        "Implementation Worker",
        "--logical-role",
        "implementation-worker",
        "--bridge-agent-type",
        "worker",
        "--bridge-model",
        "gpt-5.4",
        "--bridge-reasoning-effort",
        "high",
        "--role-skill",
        ".agents/skills/implementation-worker/SKILL.md",
        "--role-metadata",
        ".agents/skills/implementation-worker/agents/openai.yaml",
        "--role-writeback-target",
        "docs/plans/implementation-report-demo.md",
        "--role-writeback-command",
        "uv run python scripts/team_state.py implementation-report --output docs/plans/implementation-report-demo.md ...",
        "--objective",
        "Implement the bounded task only.",
        "--consumed-artifact",
        "docs/plans/sprint-contract-demo.md",
        "--constraints",
        "Only touch the approved files.",
        "--expected-output",
        "Implementation report at docs/plans/implementation-report-demo.md",
        "--writeback-target",
        "docs/plans/implementation-report-demo.md",
        "--completion-command",
        "Return the implementation handoff by writing the implementation report to docs/plans/implementation-report-demo.md",
    )
    assert packet.returncode == 0, packet.stderr

    spec = run_team_state(
        tmp_path,
        "invocation-spec",
        "--output",
        "docs/plans/builder-dispatch-demo-invocation.md",
        "--title",
        "Demo builder invocation",
        "--role",
        "Implementation Worker",
        "--logical-role",
        "implementation-worker",
        "--source-packet",
        "docs/plans/builder-dispatch-demo.md",
        "--bridge-agent-type",
        "worker",
        "--bridge-model",
        "gpt-5.4",
        "--bridge-reasoning-effort",
        "high",
        "--runtime-skill",
        ".agents/skills/implementation-worker/SKILL.md",
        "--metadata",
        ".agents/skills/implementation-worker/agents/openai.yaml",
        "--consumed-artifact",
        "docs/plans/builder-dispatch-demo.md",
        "--consumed-artifact",
        "docs/plans/sprint-contract-demo.md",
        "--expected-writeback-target",
        "docs/plans/implementation-report-demo.md",
        "--expected-writeback-command",
        "Return the implementation handoff by writing the implementation report to docs/plans/implementation-report-demo.md",
    )
    assert spec.returncode == 0, spec.stderr


def test_bridge_runner_assert_pair_accepts_matching_packet_and_spec(tmp_path: Path) -> None:
    _seed_packet_and_spec(tmp_path)

    result = run_bridge_runner(
        tmp_path,
        "assert-pair",
        "--packet-path",
        "docs/plans/builder-dispatch-demo.md",
        "--invocation-spec-path",
        "docs/plans/builder-dispatch-demo-invocation.md",
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "bridge pair ok"


def test_bridge_runner_render_outputs_reusable_launch_payload(tmp_path: Path) -> None:
    _seed_packet_and_spec(tmp_path)

    result = run_bridge_runner(
        tmp_path,
        "render",
        "--packet-path",
        "docs/plans/builder-dispatch-demo.md",
        "--invocation-spec-path",
        "docs/plans/builder-dispatch-demo-invocation.md",
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["logical_role"] == "implementation-worker"
    assert payload["agent_type"] == "worker"
    assert payload["model"] == "gpt-5.4"
    assert payload["runtime_skill"] == ".agents/skills/implementation-worker/SKILL.md"
    assert payload["packet_path"] == "docs/plans/builder-dispatch-demo.md"
    assert payload["invocation_spec_path"] == "docs/plans/builder-dispatch-demo-invocation.md"
    assert payload["expected_writeback_target"] == "docs/plans/implementation-report-demo.md"
    assert "Implementation Worker" in payload["launch_message"]
    assert "docs/plans/builder-dispatch-demo.md" in payload["launch_message"]


def test_bridge_runner_render_can_write_json_file(tmp_path: Path) -> None:
    _seed_packet_and_spec(tmp_path)

    result = run_bridge_runner(
        tmp_path,
        "render",
        "--packet-path",
        "docs/plans/builder-dispatch-demo.md",
        "--invocation-spec-path",
        "docs/plans/builder-dispatch-demo-invocation.md",
        "--output",
        "docs/plans/bridge-launches/builder.json",
    )

    assert result.returncode == 0, result.stderr
    out = tmp_path / "docs" / "plans" / "bridge-launches" / "builder.json"
    assert out.exists()
    payload = json.loads(out.read_text())
    assert payload["logical_role"] == "implementation-worker"


def test_bridge_runner_rejects_mismatched_invocation_spec(tmp_path: Path) -> None:
    _seed_packet_and_spec(tmp_path)
    bad_spec = tmp_path / "docs" / "plans" / "builder-dispatch-demo-invocation.md"
    bad_spec.write_text(
        bad_spec.read_text().replace(
            "docs/plans/implementation-report-demo.md",
            "docs/plans/unexpected-writeback.md",
            1,
        )
    )

    result = run_bridge_runner(
        tmp_path,
        "assert-pair",
        "--packet-path",
        "docs/plans/builder-dispatch-demo.md",
        "--invocation-spec-path",
        "docs/plans/builder-dispatch-demo-invocation.md",
    )

    assert result.returncode != 0
    assert "Expected writeback target mismatch" in result.stderr
