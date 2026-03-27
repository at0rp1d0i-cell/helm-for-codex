# Sprint Negotiation Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a repo-backed sprint negotiation lane so Builder feasibility and QA evaluability pressure shape the sprint contract before build starts.

**Architecture:** Reuse the existing repo-backed artifact model instead of replacing the build lane. Add sprint proposal/pass/gate writers, extend deterministic role review with a sprint-contract mode for Builder and QA, then wire a new `sprint-negotiate` flow through Ops and the lead facade. Keep the existing direct `build` path as a compatibility shortcut.

**Tech Stack:** Python 3.11+, `uv`, `pytest`, repo-backed markdown artifacts, Helm4Codex lead/ops runtime scripts, role review fallback, runtime-pack export pipeline.

---

### Task 1: Add Sprint Negotiation Artifacts

**Files:**
- Create: `ops/templates/sprint-proposal.md`
- Create: `ops/templates/sprint-pass.md`
- Create: `ops/templates/sprint-gate.md`
- Modify: `scripts/team_state.py`
- Test: `tests/test_ops_templates.py`
- Test: `tests/test_team_state_script.py`

**Step 1: Write failing tests**

Cover:
- `sprint-proposal`
- `sprint-pass`
- `sprint-gate`
- required placeholders for objective, acceptance, blocking issues, negotiated changes, and outcome

**Step 2: Run targeted tests to confirm failure**

Run: `uv run pytest -q tests/test_ops_templates.py tests/test_team_state_script.py`
Expected: FAIL because the templates and commands do not exist yet.

**Step 3: Add templates and team-state writers**

Implement repo-backed writers for:
- `sprint-proposal`
- `sprint-pass`
- `sprint-gate`

**Step 4: Re-run targeted tests**

Run: `uv run pytest -q tests/test_ops_templates.py tests/test_team_state_script.py`
Expected: PASS

**Step 5: Commit**

```bash
git add ops/templates/sprint-proposal.md ops/templates/sprint-pass.md ops/templates/sprint-gate.md scripts/team_state.py tests/test_ops_templates.py tests/test_team_state_script.py
git commit -m "feat: add sprint negotiation artifacts"
```

### Task 2: Add Deterministic Builder and QA Sprint Passes

**Files:**
- Modify: `scripts/role_review.py`
- Test: `tests/test_role_review.py`

**Step 1: Write failing tests**

Cover:
- Builder sprint pass reacts to over-broad or under-specified scope
- QA sprint pass reacts to weak verification and evidence posture
- sprint-contract mode requires a sprint proposal path

**Step 2: Run tests to confirm failure**

Run: `uv run pytest -q tests/test_role_review.py`
Expected: FAIL because sprint-contract mode does not exist yet.

**Step 3: Extend deterministic review**

Add `mode=sprint-contract` with roles:
- `Builder`
- `QA`

Use the sprint proposal as input and emit structured sprint passes.

**Step 4: Re-run tests**

Run: `uv run pytest -q tests/test_role_review.py`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/role_review.py tests/test_role_review.py
git commit -m "feat: add deterministic sprint negotiation passes"
```

### Task 3: Wire Sprint Negotiation Through Ops and Lead

**Files:**
- Modify: `scripts/ops_loop.py`
- Modify: `scripts/lead_loop.py`
- Modify: `.agents/skills/team-lead/SKILL.md`
- Modify: `.agents/skills/implementation-worker/SKILL.md`
- Modify: `.agents/skills/qa-runner/SKILL.md`
- Test: `tests/test_ops_loop.py`
- Test: `tests/test_lead_loop.py`
- Test: `tests/test_team_lead_contract.py`
- Test: `tests/test_internal_role_contracts.py`

**Step 1: Write failing flow tests**

Cover:
- `sprint-negotiate` writes proposal, Builder pass, QA pass, sprint gate
- `ready-for-build` outcome materializes sprint contract plus builder dispatch and moves board to `build`
- `reframe-scope` keeps the board in `plan`
- `ask-user` moves the board to `approval-needed`
- lead facade can route to the Ops negotiation path

**Step 2: Run targeted tests to confirm failure**

Run: `uv run pytest -q tests/test_ops_loop.py tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py`
Expected: FAIL because the sprint negotiation lane does not exist yet.

**Step 3: Implement negotiation flow**

Add:
- `ops_loop.py sprint-negotiate`
- matching lead facade command
- sprint gate logic
- conditional build materialization only on `ready-for-build`

**Step 4: Update contracts**

Update:
- `team-lead`
- `implementation-worker`
- `qa-runner`

so the pre-build negotiation path is visible and preferred.

**Step 5: Re-run targeted tests**

Run: `uv run pytest -q tests/test_ops_loop.py tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py`
Expected: PASS

**Step 6: Commit**

```bash
git add scripts/ops_loop.py scripts/lead_loop.py .agents/skills/team-lead/SKILL.md .agents/skills/implementation-worker/SKILL.md .agents/skills/qa-runner/SKILL.md tests/test_ops_loop.py tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py
git commit -m "feat: add sprint negotiation lane"
```

### Task 4: Sync Runtime Pack and Canonical State

**Files:**
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/TECH_DEBT.md`
- Modify: `docs/status/EXECUTION_BOARD.md`
- Modify: `CHANGELOG.md`
- Modify: `plugins/helm4codex/assets/runtime-pack/**`

**Step 1: Update canonical state**

Record that:
- sprint contract creation now has Builder/QA negotiation pressure
- the next major gap is live execution of those negotiation roles, not the absence of the lane itself

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
git add docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/TECH_DEBT.md docs/status/EXECUTION_BOARD.md CHANGELOG.md plugins/helm4codex/assets/runtime-pack
git commit -m "docs: record sprint negotiation tranche"
```
