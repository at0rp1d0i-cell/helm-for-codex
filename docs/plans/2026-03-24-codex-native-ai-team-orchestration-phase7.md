# Codex-Native AI Team Orchestration Phase 7 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add a real role review runtime so Product, Architect, and Reviewer can generate their own structured review passes from repository state and a plan brief.

**Architecture:** Add `scripts/role_review.py` as a deterministic role runner that reads canonical docs and a plan brief, then writes a `review-pass` artifact for one role. Extend `scripts/lead_loop.py` with a `review-run` command that invokes this runner for Product, Architect, and Reviewer and then aggregates their passes into the existing review gate. Update contracts and repo validation so this runtime becomes part of the orchestration baseline.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills

---

### Task 1: Add The Role Review Runner

**Files:**
- Create: `scripts/role_review.py`
- Create: `tests/test_role_review.py`

**Step 1: Write the failing test**

Add tests for a role runner that:

- supports `--role Product|Architect|Reviewer`
- reads a plan brief plus canonical docs
- writes a `review-pass` artifact

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_role_review.py -q`

**Step 3: Write minimal implementation**

Implement deterministic Product, Architect, and Reviewer role logic with small, explicit heuristics.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_role_review.py -q`

**Step 5: Commit**

```bash
git add scripts/role_review.py tests/test_role_review.py
git commit -m "feat: add role review runner"
```

### Task 2: Add Lead Loop Review-Run Orchestration

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing test**

Extend `tests/test_lead_loop.py` so it requires:

- `review-run`
- automatic generation of Product, Architect, and Reviewer pass files
- aggregation into the review gate without hand-authored pass content

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Add `review-run` to `scripts/lead_loop.py` and invoke `scripts/role_review.py` logic directly.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add live role-driven review orchestration"
```

### Task 3: Wire Live Role Execution Into Contracts And Validation

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `docs/project/PROJECT_BRIEF.md`

**Step 1: Write the failing tests**

Extend validation so it requires:

- `scripts/role_review.py`
- `lead_loop.py review-run`
- phase 7 current goal in `PROJECT_BRIEF.md`

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py -q`

**Step 3: Write minimal implementation**

Update the lead contract, repo checks, and brief only enough to cover the phase 7 baseline.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead/SKILL.md tests/test_team_lead_contract.py scripts/check_repo.py tests/test_repo_layout.py docs/project/PROJECT_BRIEF.md
git commit -m "feat: wire live role review execution into the lead contract"
```

### Task 4: Record The Phase 7 Baseline

**Files:**
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update roadmap and board**

Reflect that phase 7 adds:

- a live role review runner
- lead-managed execution of Product, Architect, and Reviewer passes
- aggregation from live role execution into the review gate

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
git commit -m "docs: record orchestration phase 7 baseline"
```
