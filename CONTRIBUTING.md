# Contributing

## Development Setup

```bash
uv sync --dev
```

## Core Validation

Run all of these before opening a pull request:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
uv run python scripts/export_plugin_runtime.py --check
```

## Contribution Rules

- Keep `.agents/skills` as the runtime skill discovery surface.
- Keep `.codex` for config, roles, and bridge metadata.
- Do not hand-edit the exported plugin runtime payload unless you are also updating the source runtime and re-exporting it.
- Keep the explicit upgrade path working for already-installed target repos.
- Prefer bounded changes over broad speculative refactors.
- Update user-facing docs when install paths, naming, or runtime behavior change.
- Update tests when you change runtime-pack shape, plugin packaging, or canonical docs structure.

## Pull Requests

Every pull request should explain:

1. what changed
2. why it changed
3. how it was verified
4. any follow-up work still open

## Design And Planning

For multi-step changes, write a design or implementation note in `docs/plans/` before large edits.
