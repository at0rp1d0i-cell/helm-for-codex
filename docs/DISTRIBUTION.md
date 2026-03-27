# Helm4Codex Distribution

## Overview

Helm4Codex ships as a hybrid distribution:

- a direct runtime pack installer
- a Codex plugin that bootstraps the same runtime pack

The installed repo runtime is the canonical execution surface in both cases.

## Direct Runtime-Pack Install

Use when:

- you already have this repository locally
- you want the shortest path to a working target repo runtime

Entry point:

```bash
uv run python scripts/install_runtime_pack.py --target /path/to/target-repo
```

## Plugin Bootstrap

Use when:

- you want a Codex plugin surface
- you want installation and discovery to look more like a packaged Codex workflow

Plugin path:

- `plugins/helm4codex/`

Bootstrap entry point:

```bash
python3 plugins/helm4codex/scripts/bootstrap_repo.py --target /path/to/target-repo
```

## Directory Responsibilities

- `.agents/skills/`
  - repo-local skill discovery surface
- `.codex/`
  - config, live role bindings, and role bridge metadata
- `plugins/helm4codex/`
  - distribution and bootstrap surface
- `plugins/helm4codex/assets/runtime-pack/`
  - exported self-contained runtime payload

## Synchronization Rule

The plugin runtime payload is generated from the source repo. It is not hand-maintained.

Use:

```bash
uv run python scripts/export_plugin_runtime.py
uv run python scripts/export_plugin_runtime.py --check
```

## Why The Plugin Does Not Replace The Runtime Pack

Helm4Codex is not just a skill bundle. The working team runtime depends on:

- repo-local skills
- `.codex` config and roles
- canonical docs
- runtime scripts
- ops templates and checks

The plugin makes distribution easier. The installed runtime pack is still where the real team behavior lives.
