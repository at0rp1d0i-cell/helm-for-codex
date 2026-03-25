# Codex-Native AI Team

This repository is the source repo for a Codex-native AI team runtime.

It keeps the design, tests, runtime scripts, repo-local skills, and canonical project state that back a single-entry `Lead` experience. The source repo can also export a runtime pack into another project so Codex can adopt and run that repo with the same team model.

## Install Into Another Repo

Use the installer from this repo:

```bash
uv run python scripts/install_runtime_pack.py --target /path/to/target-repo
```

The installer bootstraps:

- `AGENTS.md`
- `.codex/config.toml` and `.codex/roles/*.toml`
- `.agents/skills/`
- `scripts/team_state.py`, `scripts/lead_loop.py`, `scripts/role_review.py`
- `ops/templates/` and `ops/checks/check_docs_freshness.py`
- canonical docs under `docs/project/`, `docs/status/`, `docs/decisions/`, and `docs/plans/archive/`

Runtime-managed files are refreshed on install. Existing canonical project state is preserved so re-installing the runtime pack does not wipe a target repo's `PROJECT_BRIEF`, `EXECUTION_BOARD`, `ONBOARDING_STATE`, or `AGENTS.md`.

## First Contact And Onboarding

The installed team uses a single visible `Lead`.

On first contact with an unfamiliar repo, the lead should notice a missing or incomplete `docs/status/ONBOARDING_STATE.md` and start onboarding rather than jumping straight into implementation. The intended flow is:

`detect -> shallow-scan -> deep-scan-plan -> waiting-user-alignment -> deep-scan -> adopt`

Shallow scan is repo-safe and read-heavy. Deep scan is planned before execution so the lead can explain:

- what the team wants to verify
- which probes it wants to run
- what evidence it expects
- what requires user approval or credentials

You can also trigger the same flow manually with `init` or `re-init`.

## Runtime Surface

The runtime pack depends on these Codex-facing surfaces:

- `AGENTS.md` for repo guidance
- `.agents/skills` for repo-local role skills
- `.codex/config.toml` and `.codex/roles/*.toml` for internal review roles
- canonical docs in `docs/project/` and `docs/status/`

The source repo also keeps tests and implementation plans so the runtime can keep evolving without mixing every historical phase artifact into installed target projects.
