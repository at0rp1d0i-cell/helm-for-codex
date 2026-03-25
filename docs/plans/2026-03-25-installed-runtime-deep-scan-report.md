# Installed Runtime Deep Scan Report

## Summary

Deep scan on a clean target repo confirmed the runtime pack installs the expected surface, preserves existing `AGENTS`, `PROJECT_BRIEF`, and `ONBOARDING_STATE` on re-run, and leaves the installed docs checklist green.

## Key Findings

- The installer bootstraps `.codex`, `.agents/skills`, runtime scripts, ops templates, and canonical docs; the snapshot inside the target repo matches the source runtime.
- When canonical docs and `AGENTS.md` are modified in the target, rerunning the installer leaves those files untouched while refreshing runtime-managed artifacts.
- The installed `lead_loop.py init` command requires `--force` because the installer generates `ONBOARDING_STATE.md` immediately; without `--force` the run aborts with “Onboarding state already exists.”
- Installed `review-prepare` and `review-pass` execute successfully from the target copy, and the review-pass artifacts can be aggregated via `lead_loop.py review` or `lead_loop.py review-collect`.
- The target repo does not contain `scripts/check_repo.py`, so that script is not part of the installed runtime and should not be treated as a distributed verification harness.

## Evidence

- `uv run python scripts/install_runtime_pack.py --target /tmp/...` succeeds and the resulting `/tmp/.../.agents/skills`, `.codex`, `ops/templates`, `docs/`, and `docs/status/ONBOARDING_STATE.md` exist as expected.
- Running `uv run python ops/checks/check_docs_freshness.py` from the target repo passes.
- Editing `docs/project/PROJECT_BRIEF.md`, `docs/status/ONBOARDING_STATE.md`, and `AGENTS.md` in the target followed by rerunning the installer leaves the edits intact while rewriting runtime-managed files.
- `uv run python scripts/lead_loop.py init --force ...` from the installed target writes a new onboarding report, deep scan plan, and board state; omitting `--force` returns the expected “Onboarding state already exists” message.
- `uv run python scripts/lead_loop.py review-prepare ...` followed by `review`/`review-collect` produces `docs/plans/review-packets/product.md` and `review-passes/installed-product.md` referencing runtime review-pass commands while aggregating them into the gate.

## Recommendations

- Treat `scripts/check_repo.py` as a source-only verification helper; runtime packs should not rely on it existing on the installed target.
- Focus the next tranche on internal execution handoffs (implementation → QA → docs) and clearer onboarding semantics rather than another installer iteration.
- Expand behavior-aware checks to cover installed onboarding transitions and review pass execution from the target repo.
