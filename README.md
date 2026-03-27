# Helm4Codex

Helm4Codex is a repo-backed AI engineering team for Codex.

It turns a repository into a structured `Lead -> Ops -> Specialists` workflow so you can talk to one responsible lead while the repo keeps the team state, handoff artifacts, review gates, and runtime configuration.

## What It Is

Helm4Codex is not a chat prompt pack. It installs a working team runtime into a repository:

- a single visible `Lead`
- an internal `Ops` orchestrator
- bounded specialist roles for implementation, review, QA, docs, release, and refactor planning
- canonical project state under `docs/project/` and `docs/status/`
- repo-local Codex skills under `.agents/skills`
- role and bridge config under `.codex`

## Why Use It

Use Helm4Codex when you want Codex to behave more like a disciplined engineering team than a single long-context assistant:

- one user-facing lead instead of many agent conversations
- repo-backed handoffs instead of hidden chat-only state
- explicit review, QA, docs, and onboarding stages
- bounded task dispatch instead of vague "go build the feature"
- a reusable install surface you can carry into other repositories

## Team Model

The user talks only to the `Lead`. The lead stays user-facing, translates intent into approved work, and routes internal execution through `Ops`. `Ops` dispatches the narrower specialist roles:

- `Product`
- `Researcher`
- `Architect`
- `Builder`
- `Reviewer`
- `QA`
- `Docs`
- `Refactor Planner`
- `Release Manager`

Roles are codified as repo-local Codex skills under `.agents/skills`, while `.codex` holds config, live role bindings, and logical-role bridge metadata.

## Install Paths

Helm4Codex ships in two forms:

1. **Direct runtime-pack install**
   - best when you already have this repo locally
   - installs the full runtime directly into a target repo

```bash
uv run python scripts/install_runtime_pack.py --target /path/to/target-repo
```

2. **Plugin bootstrap**
   - best when you want a Codex-facing install surface
   - the plugin bootstraps the same runtime pack into the target repo

```bash
python3 plugins/helm4codex/scripts/bootstrap_repo.py --target /path/to/target-repo
```

In both cases, the installed repo runtime is the real execution surface. The plugin is a packaging and bootstrap layer, not a replacement for the installed repo-local runtime.

## Upgrade

If a target repository already has Helm4Codex installed, you can reapply the checked-in runtime from inside that repository with:

```bash
uv run python scripts/upgrade_runtime_pack.py
```

Use that when the repo already contains the Helm4Codex files you want to keep, but you need to reapply runtime-managed surfaces while preserving canonical state.

To install or upgrade from the Helm4Codex source repository instead, run:

```bash
uv run python scripts/upgrade_runtime_pack.py --target /path/to/target-repo
```

This refreshes runtime-managed files while preserving the target repo's canonical project state. See [docs/UPGRADE.md](/home/torpedo/Workspace/codex_exploring/docs/UPGRADE.md).

To validate an installed target repo after install or upgrade:

```bash
uv run python scripts/check_installed_runtime.py
uv run python ops/checks/check_docs_freshness.py
```

## Quick Start

1. Install Helm4Codex into a target repository.
2. Restart Codex in that target repo if the new repo-local skills do not appear immediately.
3. Start with the single visible entrypoint:

```text
Use team-lead. Adopt this repository and give me the next bounded task.
```

4. Let the lead move the repo through onboarding:
   - `detect`
   - `shallow-scan`
   - `deep-scan-plan`
   - `waiting-user-alignment`
   - `deep-scan`
   - `adopt`

For a fuller walkthrough, see [docs/QUICKSTART.md](/home/torpedo/Workspace/codex_exploring/docs/QUICKSTART.md).

## Runtime Layout

The runtime is split on purpose:

- `.agents/skills/` is the canonical repo-local skill surface that Codex discovers at runtime.
- `.codex/` holds `config.toml`, `roles/*.toml`, `role_bridge.toml`, and other project-scoped runtime configuration.

Repo skills stay in `.agents/skills` because that is the official Codex discovery path. `.codex` is reserved for configuration and role metadata.

## How The Workflow Works

The runtime is built on four layers:

- `AGENTS.md` describes the operating guide and canonical state.
- `.codex/config.toml` plus `.codex/roles/*.toml` bind live orchestration and specialist roles.
- `.codex/role_bridge.toml` plus `scripts/role_bridge.py` keep repo role names canonical and resolve them to the available agent API surface.
- `scripts/team_state.py`, `scripts/lead_loop.py`, `scripts/ops_loop.py`, and `scripts/bridge_runner.py` create handoff artifacts, advance state, and compile live dispatch payloads.

The current execution path supports:

- bounded task dispatch packets
- paired invocation specs for live dispatch
- review passes and review gates
- bridge-launch payloads
- execution receipts after live attempts

For a deeper breakdown, see [docs/DISTRIBUTION.md](/home/torpedo/Workspace/codex_exploring/docs/DISTRIBUTION.md) and [docs/project/ARCHITECTURE.md](/home/torpedo/Workspace/codex_exploring/docs/project/ARCHITECTURE.md).

## Agent Work Granularity

Helm4Codex currently favors bounded, measurable slices:

1. **Task brief**
   - the smallest unit: bug fix, doc update, refactor slice
2. **Feature slice**
   - a concrete surface that may include Builder + QA + Docs handoffs
3. **Feature branch / PR**
   - an aggregated slice that the lead still routes through review, QA, and docs before ship-ready

This keeps agents focused: they solve a bounded problem inside a shared repo-backed plan instead of taking vague ownership of an entire codebase.

## Public Distribution Surface

For external users, the repository has three install-facing layers:

- `plugins/helm4codex/`
  - public Codex plugin surface
- `.agents/plugins/marketplace.json`
  - local marketplace metadata for Codex plugin discovery during development
- `scripts/install_runtime_pack.py`
  - direct installer for the full repo runtime

## Open Source Docs

- [docs/README.md](/home/torpedo/Workspace/codex_exploring/docs/README.md)
- [docs/QUICKSTART.md](/home/torpedo/Workspace/codex_exploring/docs/QUICKSTART.md)
- [docs/DISTRIBUTION.md](/home/torpedo/Workspace/codex_exploring/docs/DISTRIBUTION.md)
- [docs/UPGRADE.md](/home/torpedo/Workspace/codex_exploring/docs/UPGRADE.md)
- [CONTRIBUTING.md](/home/torpedo/Workspace/codex_exploring/CONTRIBUTING.md)
- [CHANGELOG.md](/home/torpedo/Workspace/codex_exploring/CHANGELOG.md)
- [SECURITY.md](/home/torpedo/Workspace/codex_exploring/SECURITY.md)
- [CODE_OF_CONDUCT.md](/home/torpedo/Workspace/codex_exploring/CODE_OF_CONDUCT.md)
- [SUPPORT.md](/home/torpedo/Workspace/codex_exploring/SUPPORT.md)

## Development

```bash
uv sync --dev
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
uv run python scripts/export_plugin_runtime.py --check
```

## License

MIT. See [LICENSE](/home/torpedo/Workspace/codex_exploring/LICENSE).
