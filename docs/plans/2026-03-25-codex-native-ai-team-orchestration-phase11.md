# Codex-Native AI Team Orchestration Phase 11 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Promote live internal review from direct `review-result` writeback to direct canonical `review-pass` writeback while keeping review-gate synthesis with the lead.

**Architecture:** Update the live review packet protocol, internal review role contracts, and Codex role config so Product, Architect, and Reviewer write canonical `review-pass` artifacts directly. Keep `review-result` and `review-collect` as a compatibility path, but make direct `review-pass` ownership the default live path.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md`, Codex `agents/openai.yaml`, Codex `.codex/config.toml`

---

### Task 1: Promote Review Packets To Direct Review-Pass Writeback

**Files:**
- Modify: `scripts/team_state.py`
- Modify: `ops/templates/review-packet.md`
- Modify: `tests/test_team_state_script.py`
- Modify: `tests/test_ops_templates.py`

**Step 1: Write the failing tests**

Require review packets to:

- point the preferred live writeback target at canonical `review-pass` paths
- show `scripts/team_state.py review-pass` in the writeback command
- describe `review-pass` as the expected live output artifact

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Update packet generation and template text so the preferred live packet contract is direct canonical `review-pass` writeback.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py ops/templates/review-packet.md tests/test_team_state_script.py tests/test_ops_templates.py
git commit -m "feat: promote review packets to direct review-pass writeback"
```

### Task 2: Update Lead Loop Live Review Preparation And Compatibility

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing tests**

Require `review-prepare` to:

- emit concrete `review-pass` writeback commands for Product, Architect, and Reviewer
- point live role outputs at canonical `docs/plans/review-passes/*.md`
- keep `review-collect` available for compatibility with phase 10 `review-result` artifacts

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Update `review-prepare` so the preferred live path writes direct canonical passes while leaving `review-collect` intact.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: promote live review to direct review-pass writeback"
```

### Task 3: Rebind Internal Review Roles To Canonical Review-Pass Ownership

**Files:**
- Modify: `.codex/config.toml`
- Modify: `.codex/roles/product-reviewer.toml`
- Modify: `.codex/roles/architect-reviewer.toml`
- Modify: `.codex/roles/code-reviewer.toml`
- Modify: `skills/product-discovery/agents/openai.yaml`
- Modify: `skills/architecture-review/agents/openai.yaml`
- Modify: `skills/code-reviewer/agents/openai.yaml`
- Modify: `skills/product-discovery/SKILL.md`
- Modify: `skills/architecture-review/SKILL.md`
- Modify: `skills/code-reviewer/SKILL.md`
- Modify: `tests/test_internal_role_contracts.py`
- Modify: `tests/test_internal_skills.py`
- Modify: `tests/test_repo_layout.py`

**Step 1: Write the failing tests**

Require:

- internal role contracts to reference canonical `review-pass` ownership
- repo-scoped Codex role config to point at canonical `review-pass` targets
- skill metadata text to reflect canonical pass ownership

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_internal_role_contracts.py tests/test_internal_skills.py tests/test_repo_layout.py -q`

**Step 3: Write minimal implementation**

Update role contracts, metadata, and Codex role config so Product, Architect, and Reviewer own canonical `review-pass` writes in the preferred live path.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_internal_role_contracts.py tests/test_internal_skills.py tests/test_repo_layout.py -q`

**Step 5: Commit**

```bash
git add .codex/config.toml .codex/roles/product-reviewer.toml .codex/roles/architect-reviewer.toml .codex/roles/code-reviewer.toml skills/product-discovery/agents/openai.yaml skills/architecture-review/agents/openai.yaml skills/code-reviewer/agents/openai.yaml skills/product-discovery/SKILL.md skills/architecture-review/SKILL.md skills/code-reviewer/SKILL.md tests/test_internal_role_contracts.py tests/test_internal_skills.py tests/test_repo_layout.py
git commit -m "feat: rebind internal reviewers to canonical review passes"
```

### Task 4: Wire Phase 11 Baseline And Verify

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/ARCHITECTURE.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update contracts and canonical docs**

Reflect that phase 11:

- prefers direct role-owned canonical `review-pass` writeback
- keeps `review-result` as a compatibility path
- keeps the lead as the owner of review-gate synthesis

**Step 2: Run verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

**Step 3: Commit**

```bash
git add skills/team-lead/SKILL.md tests/test_team_lead_contract.py docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/ARCHITECTURE.md docs/status/EXECUTION_BOARD.md
git commit -m "docs: record orchestration phase 11 baseline"
```
