import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORT_SCRIPT = ROOT / "scripts" / "export_plugin_runtime.py"
BOOTSTRAP_SCRIPT = ROOT / "plugins" / "helm4codex" / "scripts" / "bootstrap_repo.py"


def test_plugin_manifest_and_marketplace_are_wired() -> None:
    manifest = json.loads((ROOT / "plugins" / "helm4codex" / ".codex-plugin" / "plugin.json").read_text())
    marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text())

    assert manifest["name"] == "helm4codex"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["displayName"] == "Helm4Codex"
    assert marketplace["name"] == "helm4codex-local"
    assert marketplace["plugins"][0]["name"] == "helm4codex"
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/helm4codex"


def test_exported_plugin_runtime_pack_is_in_sync() -> None:
    result = subprocess.run(
        [sys.executable, str(EXPORT_SCRIPT), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "plugin runtime pack ok" in result.stdout


def test_exported_plugin_runtime_pack_is_in_sync_from_repo_root_argument() -> None:
    result = subprocess.run(
        [sys.executable, str(EXPORT_SCRIPT), "--check", "."],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "plugin runtime pack ok" in result.stdout


def test_plugin_bootstrap_installs_runtime_into_target_repo(tmp_path: Path) -> None:
    target = tmp_path / "repo"
    result = subprocess.run(
        [sys.executable, str(BOOTSTRAP_SCRIPT), "--target", str(target)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert (target / ".agents" / "skills" / "team-lead" / "SKILL.md").exists()
    assert (target / ".codex" / "config.toml").exists()
    assert (target / "scripts" / "lead_loop.py").exists()
    assert (target / "scripts" / "install_runtime_pack.py").exists()
    assert (target / "scripts" / "runtime_pack_manifest.py").exists()
    assert (target / "scripts" / "check_installed_runtime.py").exists()
    assert (target / "scripts" / "upgrade_runtime_pack.py").exists()

    installed_check = subprocess.run(
        [sys.executable, str(target / "scripts" / "check_installed_runtime.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert installed_check.returncode == 0, installed_check.stderr
    assert "installed runtime ok" in installed_check.stdout

    docs_check = subprocess.run(
        [sys.executable, str(target / "ops" / "checks" / "check_docs_freshness.py"), "--root", str(target)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert docs_check.returncode == 0, docs_check.stderr
    assert "docs structure ok" in docs_check.stdout
