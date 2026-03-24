# Codex-Native AI Team Orchestration Phase 8 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add a subagent-ready review preparation flow so the lead can hand real Product, Architect, and Reviewer packets to Codex subagents before aggregating review passes.

**Architecture:** Extend the repo-backed orchestration layer with a `review-packet` artifact and a `review-prepare` lead-loop command. The deterministic phase 7 runtime remains as a fallback, while the lead contract is updated to prefer live subagent review when the session can provide it.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills

---

### Task 1: Add Review Packet Artifacts

**Files:**
- Modify: `scripts/team_state.py`
- Modify: `tests/test_team_state_script.py`
- Modify: `tests/test_ops_templates.py`
- Create: `ops/templates/review-packet.md`

**Step 1: Write the failing test**

Extend `tests/test_team_state_script.py` and `tests/test_ops_templates.py` so they require:

- a `review-packet` command
- a repo template for review packets
- packet sections for role, objective, canonical sources, plan brief, expected output, and writeback target

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Add the new template and the smallest `team_state.py` command that writes the packet artifact.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py tests/test_team_state_script.py tests/test_ops_templates.py ops/templates/review-packet.md
git commit -m "feat: add review packet artifacts"
```

### Task 2: Add Lead Loop Review Preparation

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing test**

Extend `tests/test_lead_loop.py` so it requires:

- `review-prepare`
- automatic generation of Product, Architect, and Reviewer packets
- board movement into `review`

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Add `review-prepare` to `lead_loop.py` and generate bounded packet artifacts from canonical state plus the provided plan brief.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add live subagent review preparation"
```

### Task 3: Wire Subagent Review Preparation Into Contracts And Validation

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `docs/project/PROJECT_BRIEF.md`

**Step 1: Write the failing tests**

Extend validation so it requires:

- the new review packet template
- `lead_loop.py review-prepare`
- a phase 8 current goal that references live subagent review preparation

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py -q`

**Step 3: Write minimal implementation**

Update the lead contract, repo checks, and brief to prefer live subagent review preparation while keeping deterministic fallback documented.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead/SKILL.md tests/test_team_lead_contract.py scripts/check_repo.py tests/test_repo_layout.py docs/project/PROJECT_BRIEF.md
git commit -m "feat: wire live subagent review preparation into the lead contract"
```

### Task 4: Record The Phase 8 Baseline

**Files:**
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update roadmap and board**

Reflect that phase 8 adds:

- review packets for internal review roles
- lead-managed live subagent review preparation
- deterministic role review as fallback

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
git commit -m "docs: record orchestration phase 8 baseline"
```
