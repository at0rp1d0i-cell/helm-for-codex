# Codex-Native AI Team Orchestration Phase 10 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add direct internal role-owned `review-result` writeback and Codex-native role configuration for key internal review agents.

**Architecture:** Extend review packets with a direct writeback protocol, update Product/Architect/Reviewer contracts to own `review-result` writeback, and add repo-scoped Codex role configuration through `.codex/config.toml`, role TOMLs, and role skill metadata. Keep `review-collect` as the collection layer and keep deterministic fallback intact.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md`, Codex `agents/openai.yaml`, Codex `.codex/config.toml`

---

### Task 1: Add Direct Writeback Protocol To Review Packets

**Files:**
- Modify: `scripts/team_state.py`
- Modify: `tests/test_team_state_script.py`
- Modify: `tests/test_ops_templates.py`
- Modify: `ops/templates/review-packet.md`

**Step 1: Write the failing test**

Extend packet tests so they require:

- a `Writeback Command` section in review packets
- packet templates that show the command placeholder
- direct reference to `scripts/team_state.py review-result`

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Add the new packet field and the smallest implementation needed to carry a direct writeback command.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py tests/test_team_state_script.py tests/test_ops_templates.py ops/templates/review-packet.md
git commit -m "feat: add direct review-result writeback protocol"
```

### Task 2: Add Lead Loop Support For Direct Role Writeback

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`

**Step 1: Write the failing test**

Extend `tests/test_lead_loop.py` so it requires:

- `review-prepare` to generate a concrete `review-result` writeback command per role
- packet output that points roles at direct repo writeback

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 3: Write minimal implementation**

Update `review-prepare` to emit the direct writeback command for Product, Architect, and Reviewer.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py tests/test_lead_loop.py
git commit -m "feat: add direct role-owned review-result writeback"
```

### Task 3: Add Codex Role Metadata And Config

**Files:**
- Create: `skills/product-discovery/agents/openai.yaml`
- Create: `skills/architecture-review/agents/openai.yaml`
- Create: `skills/code-reviewer/agents/openai.yaml`
- Create: `.codex/config.toml`
- Create: `.codex/roles/product-reviewer.toml`
- Create: `.codex/roles/architect-reviewer.toml`
- Create: `.codex/roles/code-reviewer.toml`
- Modify: `skills/product-discovery/SKILL.md`
- Modify: `skills/architecture-review/SKILL.md`
- Modify: `skills/code-reviewer/SKILL.md`
- Modify: `tests/test_internal_role_contracts.py`
- Modify: `tests/test_internal_skills.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`

**Step 1: Write the failing tests**

Extend validation so it requires:

- role skill metadata files for Product, Architect, and Reviewer
- repo-scoped Codex role config
- internal review contracts that explicitly support direct `review-result` writeback

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_internal_role_contracts.py tests/test_internal_skills.py tests/test_repo_layout.py -q`

**Step 3: Write minimal implementation**

Add the role metadata and config files, then update the review-role contracts and repo validation.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_internal_role_contracts.py tests/test_internal_skills.py tests/test_repo_layout.py -q`

**Step 5: Commit**

```bash
git add skills/product-discovery/agents/openai.yaml skills/architecture-review/agents/openai.yaml skills/code-reviewer/agents/openai.yaml .codex/config.toml .codex/roles/product-reviewer.toml .codex/roles/architect-reviewer.toml .codex/roles/code-reviewer.toml skills/product-discovery/SKILL.md skills/architecture-review/SKILL.md skills/code-reviewer/SKILL.md tests/test_internal_role_contracts.py tests/test_internal_skills.py scripts/check_repo.py tests/test_repo_layout.py
git commit -m "feat: add codex role configs for internal reviewers"
```

### Task 4: Wire Phase 10 Baseline And Verify

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/ARCHITECTURE.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update contracts and canonical docs**

Reflect that phase 10 adds:

- direct role-owned `review-result` writeback
- Codex-native internal role metadata
- repo-scoped internal role config

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
git commit -m "docs: record orchestration phase 10 baseline"
```
