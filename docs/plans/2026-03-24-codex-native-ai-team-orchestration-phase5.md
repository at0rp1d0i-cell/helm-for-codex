# Codex-Native AI Team Orchestration Phase 5 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add a lead-managed review gate that captures multi-role review passes, logs auto-decisions, and escalates only taste decisions before build.

**Architecture:** Keep `scripts/team_state.py` as the markdown-writing control surface and extend it with a review gate artifact writer. Then extend `scripts/lead_loop.py` with a `review` command that composes those writes and updates the execution board to `review` or `approval-needed`. Finally, make `team-lead` and repo validation treat this review gate as part of the canonical orchestration baseline.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills

---

### Task 1: Add The Review Gate Artifact Writer

**Files:**
- Modify: `scripts/team_state.py`
- Modify: `tests/test_team_state_script.py`
- Create: `ops/templates/review-gate.md`

**Step 1: Write the failing test**

Extend `tests/test_team_state_script.py` so it requires:

- a `review-gate` command
- stable sections for review passes, auto decisions, taste decisions, recommendation, and approval target

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 3: Write minimal implementation**

Add the new writer to `scripts/team_state.py` and a matching template under `ops/templates/`.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py tests/test_team_state_script.py ops/templates/review-gate.md
git commit -m "feat: add review gate artifact"
```

### Task 2: Extend The Lead Loop With A Review Gate

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing test**

Extend `tests/test_lead_loop.py` so it requires:

- `review`: create a review gate artifact
- move the board to `review` when no taste decisions remain
- move the board to `approval-needed` when taste decisions exist

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Add `review` to `scripts/lead_loop.py`, backed by the new `review-gate` writer.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add review gate to the lead loop"
```

### Task 3: Wire The Review Gate Into Skills And Repo Validation

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `tests/test_ops_templates.py`
- Modify: `docs/project/PROJECT_BRIEF.md`

**Step 1: Write the failing tests**

Extend validation so it requires:

- `lead_loop.py review`
- repository-backed review gate language in the lead contract
- the review gate template as part of the baseline
- a phase 5 current goal in `PROJECT_BRIEF.md`

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Update the lead contract and repo checks only enough to cover the phase 5 baseline.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead/SKILL.md tests/test_team_lead_contract.py scripts/check_repo.py tests/test_repo_layout.py tests/test_ops_templates.py docs/project/PROJECT_BRIEF.md
git commit -m "feat: wire review gate into the lead contract"
```

### Task 4: Record The Phase 5 Baseline

**Files:**
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update roadmap and board**

Reflect that phase 5 adds:

- a repository-backed review gate
- auto-decision and taste-decision separation
- a lead-managed gate between planning and build

**Step 2: Run verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

**Step 3: Commit**

```bash
git add docs/project/ROADMAP.md docs/status/EXECUTION_BOARD.md
git commit -m "docs: record orchestration phase 5 baseline"
```
