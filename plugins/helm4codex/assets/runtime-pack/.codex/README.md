# Codex Runtime Layout

This directory holds Codex runtime configuration for the team system.

## Responsibilities

- `.agents/skills/`
  - Repo-local skills that Codex discovers and can invoke.
  - This is the canonical runtime surface for `team-lead`, `ops-orchestrator`, and the specialist skills.
- `.codex/config.toml`
  - Project-scoped Codex configuration.
- `.codex/roles/*.toml`
  - Live role bindings and metadata for the internal team roles.
- `.codex/role_bridge.toml`
  - Logical-role-to-generic-agent bridge configuration.

## Why Skills Stay In `.agents/skills`

Codex discovers repository skills from `.agents/skills`, not from `.codex/skills`.
Keep team runtime skills in `.agents/skills` so a fresh Codex session can find them without extra indirection.

Use `.codex` for configuration, role metadata, and bridge state.
