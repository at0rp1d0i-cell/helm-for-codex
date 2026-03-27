# Helm4Codex Gap Program Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Run the highest-value Helm4Codex productization gaps in parallel without breaking the repo-backed orchestration core.

**Architecture:** Keep `bootstrap-ai-team` as the integration branch and split the next major gaps into three isolated worktrees: `gap/ship-release`, `gap/browser-qa`, and `gap/planning-workflows`. Each track owns a narrow write surface and lands tranche-by-tranche back into the integration branch after verification.

**Tech Stack:** Git worktrees, Python 3.11+, `uv`, `pytest`, repo-backed canonical docs, Helm4Codex runtime installer/export pipeline.

---

### Task 1: Record The Parallel Program Structure

**Files:**
- Create: `docs/plans/2026-03-27-gap-program-implementation.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Record the three-track gap program**

Write the parallel execution structure into this plan:

- `integration/gap-program` stays on `bootstrap-ai-team`
- `gap/ship-release` owns release gate, ship artifacts, and release-manager workflow
- `gap/browser-qa` owns browser-backed QA evidence, screenshot artifacts, and QA report UX
- `gap/planning-workflows` owns `autoplan` and `office-hours` style planning/discovery productization

**Step 2: Keep canonical status at the integration layer only**

The integration branch owns:

- `docs/project/PROJECT_BRIEF.md`
- `docs/project/ROADMAP.md`
- `docs/status/EXECUTION_BOARD.md`
- public README and changelog rollups

Feature tracks may update local design docs and tests, but final canonical state changes land only through integration.

**Step 3: Verify the plan exists**

Run:

```bash
test -f docs/plans/2026-03-27-gap-program-implementation.md
```

Expected: exit code `0`

### Task 2: Land The Current Verified Baseline

**Files:**
- Modify: tracked files from the current verified tranche

**Step 1: Review the current working tree**

Run:

```bash
git status --short
```

Expected: only the verified gap-assessment and installed-runtime-check tranche changes are present.

**Step 2: Commit the baseline**

Run:

```bash
git add README.md docs/QUICKSTART.md docs/UPGRADE.md docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/TECH_DEBT.md docs/status/EXECUTION_BOARD.md docs/plans/2026-03-27-gstack-gap-assessment.md docs/plans/2026-03-27-gap-program-implementation.md scripts/check_installed_runtime.py scripts/check_repo.py scripts/runtime_pack_manifest.py scripts/upgrade_runtime_pack.py tests/test_install_runtime_pack.py tests/test_plugin_distribution.py tests/test_repo_layout.py plugins/helm4codex/assets/runtime-pack
git commit -m "feat: assess gstack gaps and add installed runtime check"
```

Expected: a clean commit on `bootstrap-ai-team`

### Task 3: Create Isolated Worktrees

**Files:**
- Create: global worktree directories outside the repo root

**Step 1: Use a global worktree root**

Use:

```bash
~/.config/superpowers/worktrees/codex_exploring/
```

This avoids touching repo-local ignore rules while the integration branch is active.

**Step 2: Create the three worktrees**

Run:

```bash
git worktree add ~/.config/superpowers/worktrees/codex_exploring/gap-ship-release -b gap/ship-release
git worktree add ~/.config/superpowers/worktrees/codex_exploring/gap-browser-qa -b gap/browser-qa
git worktree add ~/.config/superpowers/worktrees/codex_exploring/gap-planning-workflows -b gap/planning-workflows
```

Expected: each command succeeds and each worktree starts from the integration baseline commit.

**Step 3: Verify branch ownership**

Run in each worktree:

```bash
git branch --show-current
```

Expected:

- `gap/ship-release`
- `gap/browser-qa`
- `gap/planning-workflows`

### Task 4: Define First-Tranche Ownership

**Files:**
- Create: track-local design docs as needed

**Step 1: Ship track ownership**

`gap/ship-release` may modify:

- `skills/release-manager/**`
- `.agents/skills/release-manager/**`
- `scripts/ops_loop.py`
- `scripts/team_state.py`
- `ops/templates/release-*`
- release-focused tests

It must not rewrite browser QA or planning workflows.

**Step 2: Browser QA track ownership**

`gap/browser-qa` may modify:

- `skills/qa-runner/**`
- `.agents/skills/qa-runner/**`
- `scripts/ops_loop.py`
- `scripts/team_state.py`
- `ops/templates/qa-*`
- browser evidence helpers and tests

It must not own release flow or autoplan/discovery.

**Step 3: Planning track ownership**

`gap/planning-workflows` may modify:

- `skills/team-lead/**`
- `.agents/skills/team-lead/**`
- `skills/product-discovery/**`
- `.agents/skills/product-discovery/**`
- `scripts/lead_loop.py`
- `scripts/team_state.py`
- planning/discovery templates and tests

It must not own ship/release or browser QA evidence.

### Task 5: Spawn Subagents By Track

**Files:**
- None directly, orchestration task

**Step 1: Assign one worker per track**

Spawn one worker subagent per worktree and give it:

- exact worktree path
- exact branch name
- exact write ownership
- the rule that it is not alone in the codebase and must not revert unrelated changes

**Step 2: Give each worker a bounded first tranche**

- `gap/ship-release`: design and implement a first release gate artifact and release preparation loop
- `gap/browser-qa`: design and implement browser-backed QA evidence artifacts without yet adding the full browser runtime
- `gap/planning-workflows`: design and implement a first-class `autoplan` lane, not full office-hours yet

**Step 3: Keep integration local**

The lead stays on `bootstrap-ai-team` and only integrates, verifies, and updates canonical docs after worker results return.

### Task 6: Verify The Parallel Program Skeleton

**Files:**
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Confirm the integration repo remains healthy**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
uv run python scripts/export_plugin_runtime.py --check
```

Expected:

- tests pass
- repo layout ok
- docs structure ok
- plugin runtime pack ok

**Step 2: Confirm worktrees exist**

Run:

```bash
git worktree list
```

Expected: the three new gap worktrees appear.
