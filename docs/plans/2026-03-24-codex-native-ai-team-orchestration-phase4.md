# Codex-Native AI Team Orchestration Phase 4 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Port the most valuable upstream gstack behavior into this repo by making discovery and planning first-class repository-backed handoffs inside the lead loop.

**Architecture:** Keep the single-entry `team-lead` interface and existing canonical docs, but extend the harness so `scripts/team_state.py` can create discovery and planning artifacts, and `scripts/lead_loop.py` can move the execution board across `discovery -> plan -> build` while writing those artifacts. This ports gstack's artifact handoff discipline without copying its repeated preambles or slash-command surface.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills

---

### Task 1: Add Discovery And Plan Artifact Writers

**Files:**
- Modify: `scripts/team_state.py`
- Modify: `tests/test_team_state_script.py`
- Create: `ops/templates/discovery-brief.md`
- Create: `ops/templates/plan-brief.md`

**Step 1: Write the failing tests**

Extend `tests/test_team_state_script.py` so it requires:

- a `discovery-brief` command
- a `plan-brief` command
- markdown outputs with stable section headings for both artifact types

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 3: Write minimal implementation**

Add artifact writers to `scripts/team_state.py` and add matching templates under `ops/templates/`.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py tests/test_team_state_script.py ops/templates/discovery-brief.md ops/templates/plan-brief.md
git commit -m "feat: add discovery and planning artifacts"
```

### Task 2: Extend The Lead Loop To Cover Discovery And Planning

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing tests**

Extend `tests/test_lead_loop.py` so it requires:

- `discover`: create a discovery artifact and move the board to `discovery`
- `plan`: create a planning artifact and move the board to `plan`
- `delegate`: still remains the build-stage handoff

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Add `discover` and `plan` commands to `scripts/lead_loop.py`, backed by the new `team_state.py` commands.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add discovery and planning lead loop commands"
```

### Task 3: Integrate The New Flow Into Skills And Repo Validation

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `tests/test_ops_templates.py`
- Modify: `docs/project/PROJECT_BRIEF.md`

**Step 1: Write the failing tests**

Extend validation so it requires:

- `lead_loop.py discover`
- `lead_loop.py plan`
- the new artifact templates
- a phase 4 current goal in `PROJECT_BRIEF.md`

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Update the lead contract to explain when to use `discover`, `plan`, and `delegate`, and tighten repo validation only enough to cover the phase 4 baseline.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead/SKILL.md tests/test_team_lead_contract.py scripts/check_repo.py tests/test_repo_layout.py tests/test_ops_templates.py docs/project/PROJECT_BRIEF.md
git commit -m "feat: wire discovery and planning flow into the lead contract"
```

### Task 4: Record The Phase 4 Baseline

**Files:**
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update roadmap and board**

Reflect that phase 4 adds:

- repository-backed discovery artifacts
- repository-backed planning artifacts
- a lead loop that can move through discovery, plan, and build

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
git commit -m "docs: record orchestration phase 4 baseline"
```
