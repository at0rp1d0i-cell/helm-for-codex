# Project Brief

## Problem

Build a Codex-native AI team with a single lead interface and strong internal execution discipline.

## Current Goal

Phase 12 baseline complete: runtime-pack installation, repo-local `.agents/skills` packaging, onboarding state, and lead-led init/re-init now exist in the preferred Codex path, and the installed runtime has been verified in a fresh target repo.

## Success Criteria

- single-entry lead model exists
- canonical project-state files exist
- internal role skills exist
- runtime-pack installer exists and can install the Codex-facing runtime into another repo
- the installed runtime pack behaves as documented: fresh install works, reinstall preserves AGENTS/PROJECT_BRIEF/ONBOARDING_STATE, and installed docs checks pass
- `.agents/skills` packaging exists for the installed runtime while leaving user `skills/` source files untouched
- onboarding state exists and deep-scan planning is part of first-contact project adoption, but the lead currently needs an explicit `init`/`force` action because onboarding state is bootstrapped immediately
- direct role-owned canonical review-pass writeback exists for Product, Architect, and Reviewer
- repo-scoped Codex role config exists for internal review roles
- review-result compatibility remains available
- repo validation passes
