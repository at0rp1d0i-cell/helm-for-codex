# Helm4Codex Upgrade

## When To Use

Use the upgrade path when a repository already has Helm4Codex installed and you want the latest runtime-managed files without replacing the repository's canonical project state.

## Upgrade Command

Run from the Helm4Codex source repository:

```bash
uv run python scripts/upgrade_runtime_pack.py --target /path/to/target-repo
```

## What Gets Updated

- `.agents/skills/`
- `.codex/`
- runtime scripts under `scripts/`
- ops templates and checks under `ops/`
- Helm4Codex runtime metadata at `.codex/helm4codex.toml`

## What Gets Preserved

- `AGENTS.md`
- `docs/project/PROJECT_BRIEF.md`
- `docs/status/EXECUTION_BOARD.md`
- `docs/status/ONBOARDING_STATE.md`

## After Upgrading

1. restart Codex in the target repository
2. rerun checks in the target repository:

```bash
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

3. if the upgrade changes your workflow assumptions significantly, run:

```bash
uv run python scripts/lead_loop.py --root /path/to/target-repo init --force
```

## Runtime Metadata

The installed repo records the current Helm4Codex runtime version at:

`/.codex/helm4codex.toml`

This file is runtime-managed and is refreshed on install and upgrade.
