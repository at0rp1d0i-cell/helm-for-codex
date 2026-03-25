# Codex-Native AI Team Orchestration Phase 13 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add the first real execution-handoff slice so the lead can delegate one bounded task through builder, QA, and docs-sync handoffs with canonical board updates in both the source repo and an installed runtime copy.

**Architecture:** Keep the system single-threaded and bounded-task oriented. Introduce a file-based sprint contract that defines the builder/QA agreement before implementation starts, then add structured implementation, QA, and docs-sync artifacts plus the smallest lead-loop commands needed to move one task through `build -> qa -> docs-sync -> ship-ready` or back from `qa -> build`. Reuse the existing `qa-report` artifact instead of creating a parallel QA format, and require the same handoff chain to prove itself in an installed runtime copy. Keep planner, generator, and evaluator responsibilities separate: the lead plans and delegates, the builder generates implementation output, and QA/docs evaluate and write back evidence before the board advances.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex repo-local `.agents/skills`, installed runtime pack validation

---

### Task 1: Add The Sprint Contract And Execution Handoff Artifacts

**Files:**
- Modify: `scripts/team_state.py`
- Create: `ops/templates/sprint-contract.md`
- Create: `ops/templates/implementation-report.md`
- Modify: `ops/templates/qa-report.md`
- Create: `ops/templates/docs-sync-report.md`
- Modify: `tests/test_team_state_script.py`
- Modify: `tests/test_ops_templates.py`

**Step 1: Write the failing tests**

Extend the team-state tests so they require:

- a `sprint-contract` artifact with planner/generator/evaluator sections
- an `implementation-report` artifact for the builder handoff
- the existing `qa-report` template to explicitly consume the sprint contract plus implementation report
- a `docs-sync-report` artifact for the final documentation handoff
- explicit references to the previous artifact each downstream role must consume

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Add the sprint-contract, implementation-report, and docs-sync-report writers to `scripts/team_state.py`, and tighten `ops/templates/qa-report.md` so QA has a canonical input contract instead of an implicit free-form report.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py ops/templates/sprint-contract.md ops/templates/implementation-report.md ops/templates/qa-report.md ops/templates/docs-sync-report.md tests/test_team_state_script.py tests/test_ops_templates.py
git commit -m "feat: add execution handoff artifacts"
```

### Task 2: Add Lead-Led Builder Handoff With A Sprint Contract

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`
- Modify: `skills/team-lead/SKILL.md`
- Modify: `skills/implementation-worker/SKILL.md`
- Modify: `.agents/skills/team-lead/SKILL.md`
- Modify: `.agents/skills/implementation-worker/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `tests/test_internal_role_contracts.py`
- Modify: `tests/test_internal_skills.py`

**Step 1: Write the failing tests**

Extend the lead-loop and contract tests so they require:

- a lead command that creates a sprint contract before builder work starts
- a builder handoff that emits an implementation-report path, not just a generic task brief
- explicit planner/generator separation between `team-lead` and `implementation-worker`
- the runtime `.agents/skills` mirror to stay synchronized with the source skill contracts
- a bounded-task scope rule so this tranche does not claim full feature-branch autonomy

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py tests/test_internal_skills.py -q`

**Step 3: Write minimal implementation**

Add the smallest lead-loop command surface for builder kickoff and wire the lead and builder contracts to the new sprint contract plus implementation-report flow, keeping the runtime skill mirror in lockstep with the source contracts.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py tests/test_internal_skills.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py skills/team-lead/SKILL.md skills/implementation-worker/SKILL.md .agents/skills/team-lead/SKILL.md .agents/skills/implementation-worker/SKILL.md tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py tests/test_internal_skills.py
git commit -m "feat: add builder handoff sprint contract"
```

### Task 3: Add QA Evaluation, Defect Loop, And Installed-Runtime Verification

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `skills/qa-runner/SKILL.md`
- Modify: `.agents/skills/qa-runner/SKILL.md`
- Modify: `tests/test_lead_loop.py`
- Create: `tests/test_execution_handoff_flow.py`
- Modify: `tests/test_install_runtime_pack.py`
- Modify: `tests/test_internal_skills.py`

**Step 1: Write the failing tests**

Extend the flow tests so they require:

- QA to consume the sprint contract and implementation report
- a `qa` handoff that writes the canonical `qa-report` and moves the board to `qa`
- a defect-loop path that sends the task back to `build` when QA fails
- the same builder-to-QA handoff commands to work in a fresh installed runtime repo, not only in the source repo
- the runtime `.agents/skills` mirror to stay synchronized with the updated QA role contract

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py -q`

**Step 3: Write minimal implementation**

Add the minimal QA command surface to the lead loop, keep the evaluator role separate from the builder, cover source-repo plus installed-runtime execution with the same artifact contract, and keep the runtime QA skill mirror in sync.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py skills/qa-runner/SKILL.md .agents/skills/qa-runner/SKILL.md tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py
git commit -m "feat: add qa handoff and defect loop"
```

### Task 4: Add Docs-Sync Handoff And Ship-Ready Board Update

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `skills/docs-sync/SKILL.md`
- Modify: `.agents/skills/docs-sync/SKILL.md`
- Modify: `tests/test_lead_loop.py`
- Modify: `tests/test_execution_handoff_flow.py`
- Modify: `tests/test_install_runtime_pack.py`
- Modify: `tests/test_internal_skills.py`

**Step 1: Write the failing tests**

Extend the orchestration tests so they require:

- docs-sync to consume the implementation report and QA report
- a `docs-sync` handoff that writes a docs-sync report
- the board to move to `docs-sync` and then `ship-ready` only after docs-sync completes
- the installed runtime verification path to exercise the full builder -> QA -> docs-sync slice, not just the earlier handoffs
- the runtime `.agents/skills` mirror to stay synchronized with the updated Docs role contract
- canonical writeback targets to remain repo-backed rather than ad hoc session notes

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py -q`

**Step 3: Write minimal implementation**

Add the smallest docs-sync command path and update the docs role contract so the final handoff completes the bounded task lifecycle in both the source repo and a freshly installed runtime copy, while keeping the runtime skill mirror aligned.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py skills/docs-sync/SKILL.md .agents/skills/docs-sync/SKILL.md tests/test_lead_loop.py tests/test_execution_handoff_flow.py tests/test_install_runtime_pack.py tests/test_internal_skills.py
git commit -m "feat: add docs sync handoff"
```

### Task 5: Record The Phase 13 Baseline And Link The Next Tranche

**Files:**
- Modify: `README.md`
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/ARCHITECTURE.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update baseline docs**

Reflect that phase 13 introduces:

- the first bounded execution-handoff slice
- sprint contracts between planner, builder, and QA
- generator/evaluator separation across builder, QA, and docs-sync
- installed-runtime verification for execution handoffs from day one

**Step 2: Run verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

**Step 3: Commit**

```bash
git add README.md docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/ARCHITECTURE.md docs/status/EXECUTION_BOARD.md
git commit -m "docs: record orchestration phase 13 baseline"
```
