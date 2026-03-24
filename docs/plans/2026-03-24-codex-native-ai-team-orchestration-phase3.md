# Codex-Native AI Team Orchestration Phase 3 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add a minimal executable lead loop that can turn a user request into a bounded delegated task, update project state, and surface approval-needed decisions through repository artifacts.

**Architecture:** Keep `scripts/team_state.py` as the low-level markdown writer and add `scripts/lead_loop.py` as the orchestration layer that composes those state operations. The lead contract and repo checks will then treat `lead_loop.py` as the first runnable bridge between the single-entry lead and the repository-backed team state.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills

---

### Task 1: Add The Lead Loop Script

**Files:**
- Create: `scripts/lead_loop.py`
- Create: `tests/test_lead_loop.py`

**Step 1: Write the failing test**

Add tests for a minimal CLI that supports:

- `delegate`: create a task brief and update the execution board active work in one action
- `decision`: create a decision record and optionally move the board to `approval-needed`
- `status`: print a compact summary from canonical state

Use a temporary root so the tests do not mutate the real repo.

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Create `scripts/lead_loop.py` as a dependency-free wrapper around `scripts/team_state.py` behavior. Prefer importing helper functions from `team_state.py` over shelling out.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add minimal lead loop"
```

### Task 2: Integrate Lead Loop Into The Lead Contract

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `docs/project/PROJECT_BRIEF.md`

**Step 1: Write the failing test**

Extend the lead contract test so it requires:

- `scripts/lead_loop.py`
- explicit delegation and approval-needed flow references
- the rule that the lead prefers repository-backed state transitions over ad hoc prose summaries

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py -q`

**Step 3: Write minimal implementation**

Update the lead skill to describe:

- when to use `lead_loop.py delegate`
- when to use `lead_loop.py decision`
- how `status` should be used to answer progress questions

Update `PROJECT_BRIEF.md` so the current goal reflects phase 3.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead/SKILL.md tests/test_team_lead_contract.py docs/project/PROJECT_BRIEF.md
git commit -m "feat: integrate lead loop into team lead contract"
```

### Task 3: Extend Repo Validation For The Lead Loop

**Files:**
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `ops/checks/check_docs_freshness.py`
- Modify: `tests/test_ops_templates.py`

**Step 1: Write the failing test**

Extend existing validation tests so they require:

- `scripts/lead_loop.py`
- the execution board to keep its canonical preamble and active/completed sections
- the presence of a current-goal heading in `PROJECT_BRIEF.md`

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Strengthen the repo checks only enough to cover the phase 3 orchestration baseline.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/check_repo.py tests/test_repo_layout.py ops/checks/check_docs_freshness.py tests/test_ops_templates.py
git commit -m "chore: extend repo checks for lead loop"
```

### Task 4: Record The Phase 3 Baseline

**Files:**
- Modify: `docs/status/EXECUTION_BOARD.md`
- Modify: `docs/project/ROADMAP.md`

**Step 1: Update the board and roadmap**

Reflect that phase 3 adds:

- a runnable lead loop
- repository-backed delegation and decision flow
- stronger orchestration baseline checks

**Step 2: Run verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

**Step 3: Commit**

```bash
git add docs/status/EXECUTION_BOARD.md docs/project/ROADMAP.md
git commit -m "docs: record orchestration phase 3 baseline"
```
