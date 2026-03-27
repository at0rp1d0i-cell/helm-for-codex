# Hybrid Distribution Design

## Goal

Turn this repository from an internal runtime into a reusable Codex package that other developers can install and bootstrap without understanding the repo internals first.

## Problem

The current runtime pack works when the source repository is available and the user runs `scripts/install_runtime_pack.py`. That is enough for dogfooding, but not enough for a broader audience:

- there is no formal Codex plugin surface
- there is no repo marketplace entry
- there is no self-contained bootstrap path from a plugin install to a working repo runtime
- the public README still reads more like an internal engineering document than an external install guide

## Options

### 1. Installer Only

Keep `scripts/install_runtime_pack.py` as the only install path.

Pros:
- smallest change
- no plugin duplication

Cons:
- weak discoverability
- not aligned with Codex plugin distribution
- users must clone or reference this repo directly before they can use the team runtime

### 2. Plugin Only

Package the team entirely as a Codex plugin and remove the runtime pack installer.

Pros:
- distribution shape matches Codex product surfaces
- easier to explain as a single artifact

Cons:
- plugin install alone does not replace repo-local runtime setup
- the project still needs canonical docs, scripts, config, and state files inside the target repository
- too much pressure on the plugin to act as both discovery layer and runtime installer

### 3. Hybrid

Ship both:

- a Codex plugin for discovery, installability, and bootstrap entrypoints
- a runtime pack installer for the full repo-local team surface

Pros:
- matches Codex plugin conventions
- preserves the full repo-local runtime
- lets users discover the system as a plugin, then bootstrap a repo into the full Lead -> Ops -> Specialists workflow

Cons:
- requires keeping plugin assets synchronized with the runtime pack

## Decision

Choose `Hybrid`.

The plugin is the public distribution and discovery surface. The runtime pack remains the canonical repo-local execution surface. The plugin should not attempt to replace the runtime pack; it should bootstrap it.

## Architecture

### Public Layers

1. `plugins/codex-ai-team/`
   - Codex plugin package
   - contains plugin manifest, bootstrap skill, bootstrap script, and bundled runtime-pack assets

2. `.agents/plugins/marketplace.json`
   - local repo marketplace so the plugin is visible in Codex plugin surfaces during development

3. `scripts/install_runtime_pack.py`
   - keeps working as the direct repo installer
   - should share the same runtime-pack manifest as the plugin bootstrap path

### Bootstrap Flow

The plugin bootstrap flow should be:

1. user installs or loads the plugin
2. user invokes the bootstrap skill in a target repo
3. plugin bootstrap script copies the bundled runtime pack into the target repo
4. target repo now exposes `.agents/skills`, `.codex`, runtime scripts, and canonical docs
5. target repo opens with `team-lead` as the visible entrypoint

### Synchronization Strategy

The runtime pack inside the plugin must be generated from the source repo, not manually maintained. The repository should own a single source of truth for:

- skills
- `.codex` config and roles
- runtime scripts
- ops templates and checks
- canonical docs/bootstrap docs

The plugin should bundle an exported copy of that runtime pack.

## Initial Scope

This tranche should deliver:

- plugin directory with valid `.codex-plugin/plugin.json`
- local marketplace entry
- bundled runtime-pack export
- plugin bootstrap skill and script
- updated README that explains direct installer vs plugin bootstrap
- tests proving the plugin bootstrap produces a working repo runtime

This tranche does not need:

- official marketplace publishing
- remote install flows
- app integrations or MCP packaging

## Validation

Success means:

- the repo contains a valid plugin package and marketplace entry
- a temp target repo can be bootstrapped through the plugin path
- the resulting target repo passes the same minimum runtime checks as the direct installer path
- external-facing docs clearly explain what lives in `.agents/skills` vs `.codex`
