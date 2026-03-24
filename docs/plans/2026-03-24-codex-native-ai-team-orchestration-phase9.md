# Codex-Native AI Team Orchestration Phase 9 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add structured review-result capture so live subagent reviewers can return machine-readable role outputs that the lead can collect into canonical review passes and the review gate.

**Architecture:** Extend the repo-backed orchestration layer with a `review-result` artifact and a `review-collect` lead-loop command. Review packets remain the handoff layer, deterministic role review remains fallback, and the lead contract is updated so live subagent review prefers structured result capture over manual transcription.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills

---

### Task 1: Add Review Result Artifacts

**Files:**
- Modify: `scripts/team_state.py`
- Modify: `tests/test_team_state_script.py`
- Modify: `tests/test_ops_templates.py`
- Create: `ops/templates/review-result.md`

**Step 1: Write the failing test**

Extend `tests/test_team_state_script.py` and `tests/test_ops_templates.py` so they require:

- a `review-result` command
- a repo template for review results
- result sections for role, focus, findings, auto decisions, taste decisions, and recommendation

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Add the new template and the smallest `team_state.py` command that writes the result artifact.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py tests/test_team_state_script.py tests/test_ops_templates.py ops/templates/review-result.md
git commit -m "feat: add review result artifacts"
```

### Task 2: Add Lead Loop Review Collection

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing test**

Extend `tests/test_lead_loop.py` so it requires:

- `review-collect`
- conversion from Product, Architect, and Reviewer review-result files into canonical review-pass files
- aggregation into the review gate without manual pass authoring

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Add `review-collect` to `lead_loop.py` and convert structured review-result files into canonical review-pass artifacts before invoking the existing review gate flow.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add live review result collection"
```

### Task 3: Wire Review Result Capture Into Contracts And Validation

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `docs/project/PROJECT_BRIEF.md`

**Step 1: Write the failing tests**

Extend validation so it requires:

- the new review result template
- `lead_loop.py review-collect`
- a phase 9 current goal that references structured review-result capture

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py -q`

**Step 3: Write minimal implementation**

Update the lead contract, repo checks, and brief to prefer structured review-result capture during live subagent review.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead/SKILL.md tests/test_team_lead_contract.py scripts/check_repo.py tests/test_repo_layout.py docs/project/PROJECT_BRIEF.md
git commit -m "feat: wire review result capture into the lead contract"
```

### Task 4: Record The Phase 9 Baseline

**Files:**
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/ARCHITECTURE.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update roadmap, architecture, and board**

Reflect that phase 9 adds:

- review-result artifacts
- lead-managed collection from live role results into canonical review passes
- the next tranche toward direct internal role result capture

**Step 2: Run verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

**Step 3: Commit**

```bash
git add docs/project/ROADMAP.md docs/project/ARCHITECTURE.md docs/status/EXECUTION_BOARD.md
git commit -m "docs: record orchestration phase 9 baseline"
```
