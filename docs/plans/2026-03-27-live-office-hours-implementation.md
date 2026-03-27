# Live Office-Hours Execution Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn `office-hours prepare/collect` into a real live discovery execution lane with repo-backed packets, invocation specs, and collect-time aggregation.

**Architecture:** Reuse the existing packet/spec/collect pattern already proven in live review and execution handoff. Extend `office-hours` so it prepares Researcher/Product/Design/Architect live packets, prefers direct canonical writeback, and collects live outputs into the existing discovery gate and office-hours report.

**Tech Stack:** Python 3.11+, `uv`, `pytest`, repo-backed markdown artifacts, Helm4Codex lead runtime, role bridge, invocation specs, runtime-pack export pipeline.

---

### Task 1: Extend Office-Hours Paths And Report Surface

**Files:**
- Modify: `planning/discovery/templates/office-hours-report.md`
- Modify: `scripts/lead_loop.py`
- Test: `tests/test_planning_discovery_templates.py`
- Test: `tests/test_lead_loop.py`

**Step 1: Write failing tests**

Cover:
- office-hours report includes discovery packet, invocation spec, and compatibility result surfaces
- `_office_hours_paths()` exposes packet/invocation/result locations

**Step 2: Run targeted tests to confirm failure**

Run: `uv run pytest -q tests/test_planning_discovery_templates.py tests/test_lead_loop.py`
Expected: FAIL because the live office-hours path surface is missing.

**Step 3: Extend path/report shape**

Add:
- packet dir and packet paths
- invocation dir and invocation paths
- result dir and result paths
- report sections or references for these live artifacts

**Step 4: Re-run targeted tests**

Run: `uv run pytest -q tests/test_planning_discovery_templates.py tests/test_lead_loop.py`
Expected: PASS

**Step 5: Commit**

```bash
git add planning/discovery/templates/office-hours-report.md scripts/lead_loop.py tests/test_planning_discovery_templates.py tests/test_lead_loop.py
git commit -m "feat: extend office-hours live artifact surface"
```

### Task 2: Implement Live Office-Hours Prepare

**Files:**
- Modify: `scripts/lead_loop.py`
- Test: `tests/test_lead_loop.py`

**Step 1: Write failing tests**

Cover:
- `office-hours --mode prepare` writes discovery packets for Researcher/Product/Design/Architect
- invocation specs are written
- report outcome is `in-review`
- board stays in `discovery`

**Step 2: Run targeted tests to confirm failure**

Run: `uv run pytest -q tests/test_lead_loop.py`
Expected: FAIL because prepare is still a placeholder.

**Step 3: Implement prepare**

Prepare should:
- ensure office-hours brief and research brief exist
- create discovery packets and invocation specs
- point each role at canonical writeback targets
- write an in-review office-hours report with next-action instructions

**Step 4: Re-run targeted tests**

Run: `uv run pytest -q tests/test_lead_loop.py`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add live office-hours preparation lane"
```

### Task 3: Implement Live Office-Hours Collect

**Files:**
- Modify: `scripts/lead_loop.py`
- Test: `tests/test_lead_loop.py`

**Step 1: Write failing tests**

Cover:
- collect blocks when required live artifacts are missing
- collect succeeds when research report plus challenge passes exist
- collect can optionally convert compatibility results into challenge passes
- collect writes discovery gate and office-hours report and updates the board

**Step 2: Run targeted tests to confirm failure**

Run: `uv run pytest -q tests/test_lead_loop.py`
Expected: FAIL because collect is still a placeholder.

**Step 3: Implement collect**

Collect should:
- require research report
- prefer direct challenge-pass writeback
- optionally convert compatibility results into challenge passes
- write discovery gate and office-hours report
- move board based on the gate outcome

**Step 4: Re-run targeted tests**

Run: `uv run pytest -q tests/test_lead_loop.py`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add live office-hours collect lane"
```

### Task 4: Update Contracts, Canonical State, And Runtime Pack

**Files:**
- Modify: `.agents/skills/team-lead/SKILL.md`
- Modify: `skills/team-lead/SKILL.md`
- Modify: `.agents/skills/researcher/SKILL.md`
- Modify: `skills/researcher/SKILL.md`
- Modify: `.agents/skills/product-discovery/SKILL.md`
- Modify: `skills/product-discovery/SKILL.md`
- Modify: `.agents/skills/design-review/SKILL.md`
- Modify: `skills/design-review/SKILL.md`
- Modify: `.agents/skills/architecture-review/SKILL.md`
- Modify: `skills/architecture-review/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `tests/test_internal_role_contracts.py`
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/TECH_DEBT.md`
- Modify: `docs/status/EXECUTION_BOARD.md`
- Modify: `CHANGELOG.md`
- Modify: `plugins/helm4codex/assets/runtime-pack/**`

**Step 1: Update contracts and tests**

Record that:
- `office-hours prepare/collect` is now the preferred live discovery path
- deterministic `office-hours run` remains the fallback

**Step 2: Export runtime pack**

Run: `uv run python scripts/export_plugin_runtime.py`
Expected: runtime-pack mirror refreshes without error.

**Step 3: Run full verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
uv run python scripts/export_plugin_runtime.py --check .
```

Expected:
- all tests pass
- `repo layout ok`
- `docs structure ok`
- `plugin runtime pack ok`

**Step 4: Commit**

```bash
git add .agents/skills skills tests/test_team_lead_contract.py tests/test_internal_role_contracts.py docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/TECH_DEBT.md docs/status/EXECUTION_BOARD.md CHANGELOG.md plugins/helm4codex/assets/runtime-pack
git commit -m "docs: record live office-hours execution tranche"
```
