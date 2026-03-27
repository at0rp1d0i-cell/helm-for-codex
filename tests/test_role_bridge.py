import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "role_bridge.py"


def run_role_bridge(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_role_bridge_assert_sync_passes_for_repo() -> None:
    result = run_role_bridge("assert-sync")
    assert result.returncode == 0, result.stderr
    assert "role bridge ok" in result.stdout


def test_role_bridge_resolve_returns_bridge_metadata() -> None:
    result = run_role_bridge("resolve", "implementation-worker")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["logical_role"] == "implementation-worker"
    assert payload["display_name"] == "Implementation Worker"
    assert payload["agent_type"] == "worker"
    assert payload["model"] == "gpt-5.4"
    assert payload["reasoning_effort"] == "high"
    assert payload["role_toml"] == "roles/implementation-worker.toml"
    assert payload["skill"] == ".agents/skills/implementation-worker/SKILL.md"


def test_role_bridge_list_covers_live_roles() -> None:
    result = run_role_bridge("list")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    roles = {entry["logical_role"] for entry in payload}
    assert roles == {
        "ops-orchestrator",
        "product-reviewer",
        "architect-reviewer",
        "code-reviewer",
        "implementation-worker",
        "qa-runner",
        "docs-sync",
        "release-manager",
    }
