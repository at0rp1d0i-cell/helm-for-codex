# Office-Hours Discovery Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a first-class `office-hours` discovery lane with adversarial Product, Design, and Architect challenge passes before planning.

**Architecture:** Reuse the existing repo-backed orchestration model instead of inventing a separate planning system. Add new discovery artifacts to `team_state.py`, extend `lead_loop.py` with a bounded `office-hours` lane, extend deterministic role review for discovery-specific challenge passes, and add a new Design role surface so the runtime can later promote the lane to live-role execution.

**Tech Stack:** Python 3.11+, `uv`, `pytest`, repo-backed markdown artifacts, Helm4Codex role bridge/runtime-pack export pipeline.

---

### Task 1: Add Office-Hours Artifact Writers

**Files:**
- Create: `ops/templates/office-hours-brief.md`
- Create: `ops/templates/discovery-gate.md`
- Create: `planning/discovery/templates/office-hours-report.md`
- Modify: `scripts/team_state.py`
- Test: `tests/test_ops_templates.py`
- Test: `tests/test_team_state_script.py`
- Test: `tests/test_planning_discovery_templates.py`

**Step 1: Write failing template and artifact-writer tests**

Cover:
- `office-hours-brief`
- `discovery-gate`
- `office-hours-report`
- required placeholders for outcome, build-vs-buy posture, reframed problem, and next step

**Step 2: Run targeted tests to confirm failure**

Run: `uv run pytest -q tests/test_ops_templates.py tests/test_team_state_script.py tests/test_planning_discovery_templates.py`
Expected: FAIL with missing template or command assertions.

**Step 3: Add templates and `team_state.py` writers**

Implement:
- `office-hours-brief`
- `discovery-gate`
- `office-hours-report`

Keep the shape repo-backed and parallel to `autoplan-report`.

**Step 4: Re-run targeted tests**

Run: `uv run pytest -q tests/test_ops_templates.py tests/test_team_state_script.py tests/test_planning_discovery_templates.py`
Expected: PASS

**Step 5: Commit**

```bash
git add ops/templates/office-hours-brief.md ops/templates/discovery-gate.md planning/discovery/templates/office-hours-report.md scripts/team_state.py tests/test_ops_templates.py tests/test_team_state_script.py tests/test_planning_discovery_templates.py
git commit -m "feat: add office-hours discovery artifacts"
```

### Task 2: Add Deterministic Discovery Challenge Passes

**Files:**
- Modify: `scripts/role_review.py`
- Test: `tests/test_role_review.py`

**Step 1: Write failing deterministic discovery-pass tests**

Cover:
- Product discovery challenge pass
- Design discovery challenge pass
- Architect discovery challenge pass
- discovery-specific findings, taste decisions, and recommendations

**Step 2: Run tests to confirm failure**

Run: `uv run pytest -q tests/test_role_review.py`
Expected: FAIL because discovery mode / Design role support does not exist yet.

**Step 3: Extend `role_review.py`**

Add a deterministic office-hours/discovery mode that:
- reads the office-hours brief
- emits Product, Design, and Architect challenge passes
- keeps output in the existing `review-pass` format

**Step 4: Re-run tests**

Run: `uv run pytest -q tests/test_role_review.py`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/role_review.py tests/test_role_review.py
git commit -m "feat: add deterministic office-hours challenge passes"
```

### Task 3: Add The Design Role Surface

**Files:**
- Create: `skills/design-review/SKILL.md`
- Create: `skills/design-review/agents/openai.yaml`
- Create: `.agents/skills/design-review/SKILL.md`
- Create: `.agents/skills/design-review/agents/openai.yaml`
- Create: `.codex/roles/design-reviewer.toml`
- Modify: `.codex/config.toml`
- Modify: `.codex/role_bridge.toml`
- Modify: `scripts/check_repo.py`
- Test: `tests/test_internal_skills.py`
- Test: `tests/test_repo_layout.py`
- Test: `tests/test_role_bridge.py`

**Step 1: Write failing role-surface tests**

Cover:
- Design skill exists in source and runtime mirror
- role config exists
- role bridge resolves `design-reviewer`

**Step 2: Run tests to confirm failure**

Run: `uv run pytest -q tests/test_internal_skills.py tests/test_repo_layout.py tests/test_role_bridge.py`
Expected: FAIL with missing role/config assertions.

**Step 3: Add the Design role**

Add:
- skill contract
- runtime mirror
- role config
- role-bridge entry

**Step 4: Re-run tests**

Run: `uv run pytest -q tests/test_internal_skills.py tests/test_repo_layout.py tests/test_role_bridge.py`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/design-review .agents/skills/design-review .codex/roles/design-reviewer.toml .codex/config.toml .codex/role_bridge.toml scripts/check_repo.py tests/test_internal_skills.py tests/test_repo_layout.py tests/test_role_bridge.py
git commit -m "feat: add design discovery role surface"
```

### Task 4: Add The Office-Hours Lead Lane

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `.agents/skills/team-lead/SKILL.md`
- Modify: `.agents/skills/product-discovery/SKILL.md`
- Create or Modify: `skills/design-review/SKILL.md`
- Test: `tests/test_lead_loop.py`
- Test: `tests/test_team_lead_contract.py`
- Test: `tests/test_internal_role_contracts.py`

**Step 1: Write failing lead-loop tests**

Cover:
- `office-hours run` writes brief, challenge passes, discovery gate, and office-hours report
- `ready-for-plan` outcome
- `reframe` outcome
- `ask-user` outcome
- board transition behavior

**Step 2: Run tests to confirm failure**

Run: `uv run pytest -q tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py`
Expected: FAIL because the office-hours lane does not exist yet.

**Step 3: Implement `lead_loop.py office-hours`**

Add bounded modes:
- `run`
- `prepare`
- `collect`

For this tranche, `run` must be fully functional with deterministic challenge-pass generation. `prepare` and `collect` can be stubbed only if they write explicit repo-backed blocked/in-review outputs and are tested.

**Step 4: Update role contracts**

Update:
- `team-lead`
- `product-discovery`
- `design-review`

so the lane is discoverable in the runtime surface.

**Step 5: Re-run tests**

Run: `uv run pytest -q tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py`
Expected: PASS

**Step 6: Commit**

```bash
git add scripts/lead_loop.py .agents/skills/team-lead/SKILL.md .agents/skills/product-discovery/SKILL.md skills/design-review/SKILL.md tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py
git commit -m "feat: add office-hours discovery lane"
```

### Task 5: Sync Runtime Pack And Canonical State

**Files:**
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/TECH_DEBT.md`
- Modify: `docs/status/EXECUTION_BOARD.md`
- Modify: `CHANGELOG.md`
- Modify: `plugins/helm4codex/assets/runtime-pack/**`

**Step 1: Update canonical state**

Record that:
- office-hours exists as a first-class discovery lane
- discovery-side adversarial pressure is now part of the harness
- next gap after this tranche is likely live research / office-hours polish

**Step 2: Export the runtime pack**

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
git add docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/TECH_DEBT.md docs/status/EXECUTION_BOARD.md CHANGELOG.md plugins/helm4codex/assets/runtime-pack
git commit -m "docs: record office-hours discovery tranche"
```
