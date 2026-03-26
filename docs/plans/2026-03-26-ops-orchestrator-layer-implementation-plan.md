# Ops Orchestrator Layer Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Introduce an explicit `Ops/Orchestrator` runtime layer so the visible lead stops dispatching specialist work directly.

**Architecture:** Checkpoint the current phase 13 handoff slice, then add `ops_loop.py` as the runtime owner for build/qa/docs-sync transitions while shrinking `lead_loop.py` into a user-facing facade. Keep file-based handoffs intact and move ownership boundaries, not the artifact model.

**Tech Stack:** Python 3.11+, `uv`, `pytest`, repo-backed markdown artifacts, Codex repo-local `.agents/skills`

---

### Task 1: Checkpoint The Current Phase 13 Handoff Slice

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `skills/docs-sync/SKILL.md`
- Modify: `.agents/skills/docs-sync/SKILL.md`
- Modify: `tests/test_lead_loop.py`
- Modify: `tests/test_execution_handoff_flow.py`
- Modify: `tests/test_install_runtime_pack.py`
- Modify: `tests/test_internal_skills.py`

**Step 1: Verify the current Task 4 tree is complete**

Run:

```bash
uv run pytest tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py -q
```

Expected: PASS

**Step 2: Commit the current Task 4 slice**

```bash
git add scripts/lead_loop.py skills/docs-sync/SKILL.md .agents/skills/docs-sync/SKILL.md tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py
git commit -m "feat: add docs sync handoff"
```

### Task 2: Add An Explicit Ops Runtime

**Files:**
- Create: `scripts/ops_loop.py`
- Create: `tests/test_ops_loop.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`

**Step 1: Write failing tests**

Require:

- an `ops_loop.py` entrypoint exists
- `ops_loop.py` owns `build`, `qa`, and `docs-sync`
- repo checks recognize the new runtime layer

**Step 2: Run the targeted tests**

Run:

```bash
uv run pytest tests/test_ops_loop.py tests/test_repo_layout.py -q
```

Expected: FAIL before implementation

**Step 3: Implement the minimal runtime**

Add `ops_loop.py` by moving or wrapping only the build/qa/docs-sync execution paths behind a separate runtime command surface.

**Step 4: Re-run the targeted tests**

Run:

```bash
uv run pytest tests/test_ops_loop.py tests/test_repo_layout.py -q
```

Expected: PASS

**Step 5: Commit**

```bash
git add scripts/ops_loop.py tests/test_ops_loop.py scripts/check_repo.py tests/test_repo_layout.py
git commit -m "feat: add explicit ops runtime"
```

### Task 3: Shrink Lead Into A Facade

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`
- Modify: `skills/team-lead/SKILL.md`
- Modify: `.agents/skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`

**Step 1: Write failing tests**

Require:

- `lead_loop.py` no longer owns direct build/qa/docs-sync execution
- facade actions call or instruct `ops_loop.py`
- team-lead contract states that lead does not dispatch specialists directly

**Step 2: Run the targeted tests**

Run:

```bash
uv run pytest tests/test_lead_loop.py tests/test_team_lead_contract.py -q
```

Expected: FAIL before implementation

**Step 3: Implement the facade boundary**

Keep user-facing commands in `lead_loop.py`, but route orchestration work to `ops_loop.py`.

**Step 4: Re-run the targeted tests**

Run:

```bash
uv run pytest tests/test_lead_loop.py tests/test_team_lead_contract.py -q
```

Expected: PASS

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py skills/team-lead/SKILL.md .agents/skills/team-lead/SKILL.md tests/test_team_lead_contract.py
git commit -m "refactor: turn lead loop into facade"
```

### Task 4: Rebind Specialists To Ops Ownership

**Files:**
- Modify: `skills/implementation-worker/SKILL.md`
- Modify: `skills/qa-runner/SKILL.md`
- Modify: `skills/docs-sync/SKILL.md`
- Modify: `.agents/skills/implementation-worker/SKILL.md`
- Modify: `.agents/skills/qa-runner/SKILL.md`
- Modify: `.agents/skills/docs-sync/SKILL.md`
- Modify: `tests/test_internal_role_contracts.py`
- Modify: `tests/test_internal_skills.py`

**Step 1: Write failing tests**

Require:

- specialist roles explicitly report to `Ops`
- builder, QA, and docs-sync consume only repo-backed packets from `Ops`
- source and runtime mirrors stay synchronized

**Step 2: Run the targeted tests**

Run:

```bash
uv run pytest tests/test_internal_role_contracts.py tests/test_internal_skills.py -q
```

Expected: FAIL before implementation

**Step 3: Implement the contract updates**

Update role skills so they no longer appear to receive direct lead dispatch in the runtime model.

**Step 4: Re-run the targeted tests**

Run:

```bash
uv run pytest tests/test_internal_role_contracts.py tests/test_internal_skills.py -q
```

Expected: PASS

**Step 5: Commit**

```bash
git add skills/implementation-worker/SKILL.md skills/qa-runner/SKILL.md skills/docs-sync/SKILL.md .agents/skills/implementation-worker/SKILL.md .agents/skills/qa-runner/SKILL.md .agents/skills/docs-sync/SKILL.md tests/test_internal_role_contracts.py tests/test_internal_skills.py
git commit -m "feat: rebind specialist contracts to ops"
```

### Task 5: Record The Ops Layer Baseline

**Files:**
- Modify: `docs/project/ARCHITECTURE.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update canonical docs**

Reflect that the repository now has:

- `Lead` facade layer
- explicit `Ops` runtime layer
- specialist roles that report through `Ops`

**Step 2: Run verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

Expected: PASS

**Step 3: Commit**

```bash
git add docs/project/ARCHITECTURE.md docs/project/ROADMAP.md docs/project/PROJECT_BRIEF.md docs/status/EXECUTION_BOARD.md
git commit -m "docs: record ops orchestrator baseline"
```
