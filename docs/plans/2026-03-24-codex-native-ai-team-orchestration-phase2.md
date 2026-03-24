# Codex-Native AI Team Orchestration Phase 2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the bootstrap skeleton into a minimally executable orchestration layer by codifying the lead workflow, internal role output contracts, and repository-backed state update scripts.

**Architecture:** Keep the single-entry `team-lead` skill as the user-facing router, but make its operating contract explicit and testable. Add lightweight Python tooling to generate task briefs, record decisions, and update the execution board so repository state changes stop depending on manual edits alone.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills, YAML metadata

---

### Task 1: Codify The Lead Workflow Contract

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `skills/team-lead/agents/openai.yaml`
- Create: `tests/test_team_lead_contract.py`

**Step 1: Write the failing test**

Add a test that asserts the lead skill now includes:

- the canonical repo-state files
- explicit state-machine handling rules
- the internal role roster
- task brief / decision / execution board automation references
- approval escalation triggers

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py -q`

**Step 3: Write minimal implementation**

Expand `skills/team-lead/SKILL.md` so it describes:

- the lead's single-entry behavior
- when to read/write canonical state
- when to invoke discovery vs build vs approval-needed
- how to use internal roles
- when to use the state scripts

Update `skills/team-lead/agents/openai.yaml` with a tighter short description appropriate for the richer orchestration contract.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead tests/test_team_lead_contract.py
git commit -m "feat: codify team lead workflow contract"
```

### Task 2: Codify Internal Role Output Protocols

**Files:**
- Modify: `skills/product-discovery/SKILL.md`
- Modify: `skills/architecture-review/SKILL.md`
- Modify: `skills/implementation-worker/SKILL.md`
- Modify: `skills/code-reviewer/SKILL.md`
- Modify: `skills/qa-runner/SKILL.md`
- Modify: `skills/docs-sync/SKILL.md`
- Modify: `skills/refactor-planner/SKILL.md`
- Modify: `skills/release-manager/SKILL.md`
- Create: `tests/test_internal_role_contracts.py`

**Step 1: Write the failing test**

Add a test that requires each internal skill to include:

- a clear role purpose
- a bounded output format
- the rule that it reports back to the lead rather than addressing the user directly
- explicit writeback targets when applicable

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_internal_role_contracts.py -q`

**Step 3: Write minimal implementation**

Refine each internal skill so it contains:

- mission
- inputs
- expected output sections
- writeback targets
- non-goals

Keep them concise and internal-facing.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_internal_role_contracts.py -q`

**Step 5: Commit**

```bash
git add skills tests/test_internal_role_contracts.py
git commit -m "feat: codify internal role protocols"
```

### Task 3: Add Repository-Backed State Automation Scripts

**Files:**
- Create: `scripts/team_state.py`
- Create: `tests/test_team_state_script.py`
- Modify: `ops/templates/task-brief.md`
- Modify: `ops/templates/refactor-proposal.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Write the failing test**

Add tests for a CLI that supports:

- `task-brief` to create a new task brief markdown file from structured arguments
- `decision` to create a new decision record from structured arguments
- `board` to update stage and active/completed work in `EXECUTION_BOARD.md`

Use a temporary directory fixture so tests do not mutate the real repo state.

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 3: Write minimal implementation**

Create `scripts/team_state.py` with minimal subcommands:

- `task-brief`
- `decision`
- `board`

Each command should write predictable markdown compatible with the repository conventions.

Update templates and `EXECUTION_BOARD.md` only as needed to align with the generated structure.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py -q`

**Step 5: Run the full suite**

Run: `uv run pytest -q`

**Step 6: Commit**

```bash
git add scripts/team_state.py ops/templates docs/status/EXECUTION_BOARD.md tests/test_team_state_script.py
git commit -m "feat: automate team state updates"
```

### Task 4: Tighten Repo Validation Around Orchestration

**Files:**
- Modify: `scripts/check_repo.py`
- Modify: `ops/checks/check_docs_freshness.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `tests/test_ops_templates.py`

**Step 1: Write the failing test**

Extend the existing validation tests so they require:

- `scripts/team_state.py`
- the richer lead contract checks
- templates that match the generated state script output shape

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Strengthen `scripts/check_repo.py` and `ops/checks/check_docs_freshness.py` only enough to cover the new orchestration baseline.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_repo_layout.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/check_repo.py ops/checks/check_docs_freshness.py tests/test_repo_layout.py tests/test_ops_templates.py
git commit -m "chore: tighten orchestration repo validation"
```

### Task 5: Verify And Record The Phase 2 Baseline

**Files:**
- Modify: `docs/status/EXECUTION_BOARD.md`
- Modify: `docs/project/ROADMAP.md`

**Step 1: Update the board and roadmap**

Reflect that the repo now has:

- a richer lead contract
- internal role protocols
- state update automation
- strengthened orchestration checks

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
git commit -m "docs: record orchestration phase 2 baseline"
```
