# Codex-Native AI Team Orchestration Phase 6 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Make the review gate consume structured multi-role review passes from Product, Architect, and Reviewer.

**Architecture:** Extend `scripts/team_state.py` with a `review-pass` writer and a matching template. Then upgrade `scripts/lead_loop.py review` so it can aggregate pass files into a review gate instead of depending on manual summaries. Finally, update the relevant role skills, lead contract, and baseline validation so the multi-role review pass flow becomes part of the canonical orchestration system.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills

---

### Task 1: Add The Review Pass Artifact Writer

**Files:**
- Modify: `scripts/team_state.py`
- Modify: `tests/test_team_state_script.py`
- Create: `ops/templates/review-pass.md`

**Step 1: Write the failing test**

Extend `tests/test_team_state_script.py` so it requires:

- a `review-pass` command
- stable sections for role, focus, findings, auto decisions, taste decisions, and recommendation

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 3: Write minimal implementation**

Add the writer to `scripts/team_state.py` and a matching template under `ops/templates/`.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py tests/test_team_state_script.py ops/templates/review-pass.md
git commit -m "feat: add review pass artifacts"
```

### Task 2: Aggregate Review Passes In The Lead Loop

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing test**

Extend `tests/test_lead_loop.py` so it requires:

- `review-pass`: create a pass artifact for a role
- `review`: accept multiple `--pass-path` inputs and aggregate them into a gate artifact
- board moves to `review` when aggregated taste decisions are empty
- board moves to `approval-needed` when aggregated taste decisions are non-empty

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Add a `review-pass` command and teach `review` to parse structured pass files.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: aggregate multi-role review passes"
```

### Task 3: Wire Review Passes Into Skills And Validation

**Files:**
- Modify: `skills/product-discovery/SKILL.md`
- Modify: `skills/architecture-review/SKILL.md`
- Modify: `skills/code-reviewer/SKILL.md`
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_internal_role_contracts.py`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `tests/test_ops_templates.py`
- Modify: `docs/project/PROJECT_BRIEF.md`

**Step 1: Write the failing tests**

Extend validation so it requires:

- a review pass template in the baseline
- Product, Architect, and Reviewer contracts to allow review pass writeback
- `lead_loop.py review-pass` in the lead contract
- a phase 6 current goal in `PROJECT_BRIEF.md`

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_internal_role_contracts.py tests/test_team_lead_contract.py tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Update only the relevant role skills, the lead contract, and baseline checks.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_internal_role_contracts.py tests/test_team_lead_contract.py tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add skills/product-discovery/SKILL.md skills/architecture-review/SKILL.md skills/code-reviewer/SKILL.md skills/team-lead/SKILL.md tests/test_internal_role_contracts.py tests/test_team_lead_contract.py scripts/check_repo.py tests/test_repo_layout.py tests/test_ops_templates.py docs/project/PROJECT_BRIEF.md
git commit -m "feat: wire multi-role review passes into the contracts"
```

### Task 4: Record The Phase 6 Baseline

**Files:**
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update roadmap and board**

Reflect that phase 6 adds:

- structured review pass artifacts
- aggregation from role passes into the review gate
- the first real multi-role internal review chain

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
git commit -m "docs: record orchestration phase 6 baseline"
```
