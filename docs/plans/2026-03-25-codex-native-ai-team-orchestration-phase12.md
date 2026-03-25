# Codex-Native AI Team Orchestration Phase 12 Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Add a real install/runtime-pack path, formalize init/onboarding for unfamiliar repos, and harden the system around plan lifecycle and behavior-aware orchestration checks.

**Architecture:** Keep this repo as the source of truth, add an exporter/installer that writes the Codex-facing runtime into target repos, introduce onboarding state plus shallow/deep scan planning, and upgrade validation so the team can safely adopt unfamiliar projects.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `AGENTS.md`, Codex `.codex/config.toml`, Codex repo-local `.agents/skills`

---

### Task 1: Add Runtime Pack Installer And Repo-Local Skill Export

**Files:**
- Create: `scripts/install_runtime_pack.py`
- Modify: `scripts/check_repo.py`
- Modify: `tests/test_repo_layout.py`
- Create: `tests/test_install_runtime_pack.py`
- Create: `docs/plans/archive/.gitkeep`

**Step 1: Write the failing tests**

Require the installer to:

- export runtime files into a target repo
- install skills under `.agents/skills/`
- install `.codex/config.toml` and role TOMLs
- bootstrap canonical doc directories without copying this repo’s full phase archive

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_install_runtime_pack.py tests/test_repo_layout.py -q`

**Step 3: Write minimal implementation**

Add a runtime pack installer/exporter that copies or renders the runtime-facing files into a target repo and update repo validation for the new packaging layer.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_install_runtime_pack.py tests/test_repo_layout.py -q`

**Step 5: Commit**

```bash
git add scripts/install_runtime_pack.py scripts/check_repo.py tests/test_install_runtime_pack.py tests/test_repo_layout.py docs/plans/archive/.gitkeep
git commit -m "feat: add runtime pack installer"
```

### Task 2: Add Onboarding State And Planning Artifacts

**Files:**
- Modify: `scripts/team_state.py`
- Create: `ops/templates/onboarding-state.md`
- Create: `ops/templates/onboarding-report.md`
- Create: `ops/templates/deep-scan-plan.md`
- Modify: `tests/test_team_state_script.py`
- Modify: `tests/test_ops_templates.py`

**Step 1: Write the failing tests**

Require team state tooling to support:

- onboarding state artifact creation/update
- onboarding report creation
- deep scan plan creation

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 3: Write minimal implementation**

Add the onboarding and deep-scan artifacts plus the smallest state commands needed to create them.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_state_script.py tests/test_ops_templates.py -q`

**Step 5: Commit**

```bash
git add scripts/team_state.py ops/templates/onboarding-state.md ops/templates/onboarding-report.md ops/templates/deep-scan-plan.md tests/test_team_state_script.py tests/test_ops_templates.py
git commit -m "feat: add onboarding state artifacts"
```

### Task 3: Add Lead-Led Init / Re-Init Flow

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `tests/test_lead_loop.py`
- Modify: `scripts/role_review.py`
- Create: `tests/test_onboarding_flow.py`

**Step 1: Write the failing tests**

Require the lead loop to support:

- detecting a missing onboarding state
- creating a shallow-scan report
- creating a deep-scan plan
- moving onboarding state through `detect -> shallow-scan -> deep-scan-plan -> waiting-user-alignment`
- preserving `manual re-init` capability

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_lead_loop.py tests/test_onboarding_flow.py -q`

**Step 3: Write minimal implementation**

Add lead-loop commands and state transitions for onboarding, keeping the first slice repo-backed and deterministic.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_lead_loop.py tests/test_onboarding_flow.py -q`

**Step 5: Commit**

```bash
git add scripts/lead_loop.py scripts/role_review.py tests/test_lead_loop.py tests/test_onboarding_flow.py
git commit -m "feat: add lead-led onboarding flow"
```

### Task 4: Repackage Team Skills For Runtime Use

**Files:**
- Modify: `skills/team-lead/SKILL.md`
- Modify: `skills/product-discovery/SKILL.md`
- Modify: `skills/architecture-review/SKILL.md`
- Modify: `skills/code-reviewer/SKILL.md`
- Modify: `.codex/config.toml`
- Modify: `.codex/roles/product-reviewer.toml`
- Modify: `.codex/roles/architect-reviewer.toml`
- Modify: `.codex/roles/code-reviewer.toml`
- Modify: `tests/test_team_lead_contract.py`
- Modify: `tests/test_internal_role_contracts.py`
- Modify: `tests/test_internal_skills.py`

**Step 1: Write the failing tests**

Require the contracts to reflect:

- `.agents/skills` as the runtime packaging target
- onboarding/init as part of the lead’s formal behavior
- `review-result` compatibility and canonical writeback rules staying intact

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_internal_role_contracts.py tests/test_internal_skills.py -q`

**Step 3: Write minimal implementation**

Update the lead and internal role contracts so the runtime pack and onboarding flow are part of the documented system.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_team_lead_contract.py tests/test_internal_role_contracts.py tests/test_internal_skills.py -q`

**Step 5: Commit**

```bash
git add skills/team-lead/SKILL.md skills/product-discovery/SKILL.md skills/architecture-review/SKILL.md skills/code-reviewer/SKILL.md .codex/config.toml .codex/roles/product-reviewer.toml .codex/roles/architect-reviewer.toml .codex/roles/code-reviewer.toml tests/test_team_lead_contract.py tests/test_internal_role_contracts.py tests/test_internal_skills.py
git commit -m "feat: wire onboarding and runtime packaging into contracts"
```

### Task 5: Record Phase 12 Baseline And Add Install Docs

**Files:**
- Create: `README.md`
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/ARCHITECTURE.md`
- Modify: `docs/status/EXECUTION_BOARD.md`
- Create: `docs/status/ONBOARDING_STATE.md`

**Step 1: Update baseline docs**

Reflect that phase 12 adds:

- runtime pack installation
- repo-local Codex skill packaging
- onboarding state
- shallow scan and deep scan planning
- plan archive hygiene

**Step 2: Run verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

**Step 3: Commit**

```bash
git add README.md docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/ARCHITECTURE.md docs/status/EXECUTION_BOARD.md docs/status/ONBOARDING_STATE.md
git commit -m "docs: record orchestration phase 12 baseline"
```
