# Helm4Codex Quickstart

## Goal

Install Helm4Codex into a repository and start using `team-lead` as the single visible entrypoint.

## Option 1: Direct Runtime-Pack Install

From this repository:

```bash
uv run python scripts/install_runtime_pack.py --target /path/to/target-repo
```

## Option 2: Plugin Bootstrap

From this repository:

```bash
python3 plugins/helm4codex/scripts/bootstrap_repo.py --target /path/to/target-repo
```

## After Install

1. Open Codex in the target repository root.
2. Trust the project if Codex asks.
3. Start with:

```text
Use team-lead. Adopt this repository and give me the next bounded task.
```

4. If you want to validate the installed runtime before first use:

```bash
uv run python scripts/check_installed_runtime.py
uv run python ops/checks/check_docs_freshness.py
```

## Expected Runtime Surface

The target repo should now contain:

- `AGENTS.md`
- `.agents/skills/`
- `.codex/config.toml`
- `.codex/roles/`
- `.codex/role_bridge.toml`
- `scripts/lead_loop.py`
- `scripts/ops_loop.py`
- `scripts/bridge_runner.py`
- `docs/project/`
- `docs/status/`

## If Skills Do Not Appear

- restart Codex in the target repo
- confirm you launched Codex from the repo root
- check that `.agents/skills/team-lead/SKILL.md` exists

## First Workflow

On first contact, the lead should move through:

- `detect`
- `shallow-scan`
- `deep-scan-plan`
- `waiting-user-alignment`
- `deep-scan`
- `adopt`

The lead should stay user-facing while `Ops` and specialists work behind that interface.
