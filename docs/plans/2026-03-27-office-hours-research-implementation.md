# Office-Hours Research Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a research-first office-hours lane that records repo-backed research artifacts and uses them to sharpen discovery challenge passes before planning.

**Architecture:** Extend the existing office-hours deterministic flow instead of inventing a second discovery system. Add research artifacts and a Researcher role surface, make role_review consume research context during office-hours challenge passes, then update lead_loop so office-hours becomes `brief -> research -> challenge -> gate -> report`.

**Tech Stack:** Python 3.11+, `uv`, `pytest`, repo-backed markdown artifacts, Helm4Codex role bridge/runtime-pack export pipeline.

---

### Task 1: Add Research Discovery Artifacts

**Files:**
- Create: `ops/templates/research-brief.md`
- Create: `planning/discovery/templates/research-report.md`
- Modify: `scripts/team_state.py`
- Test: `tests/test_ops_templates.py`
- Test: `tests/test_team_state_script.py`
- Test: `tests/test_planning_discovery_templates.py`

**Step 1: Write failing tests**

Cover:
- `research-brief`
- `research-report`
- required sections for problem framing, search scope, top options, recommendation, adoption notes, and open risks

**Step 2: Run targeted tests to confirm failure**

Run: `uv run pytest -q tests/test_ops_templates.py tests/test_team_state_script.py tests/test_planning_discovery_templates.py`
Expected: FAIL because the templates and commands do not exist yet.

**Step 3: Add templates and `team_state.py` writers**

Implement repo-backed writers for:
- `research-brief`
- `research-report`

**Step 4: Re-run targeted tests**

Run: `uv run pytest -q tests/test_ops_templates.py tests/test_team_state_script.py tests/test_planning_discovery_templates.py`
Expected: PASS

**Step 5: Commit**

```bash
git add ops/templates/research-brief.md planning/discovery/templates/research-report.md scripts/team_state.py tests/test_ops_templates.py tests/test_team_state_script.py tests/test_planning_discovery_templates.py
git commit -m "feat: add office-hours research artifacts"
```

### Task 2: Add The Researcher Role Surface

**Files:**
- Create: `skills/researcher/SKILL.md`
- Create: `skills/researcher/agents/openai.yaml`
- Create: `.agents/skills/researcher/SKILL.md`
- Create: `.agents/skills/researcher/agents/openai.yaml`
- Create: `.codex/roles/researcher.toml`
- Modify: `.codex/config.toml`
- Modify: `.codex/role_bridge.toml`
- Modify: `scripts/check_repo.py`
- Test: `tests/test_internal_skills.py`
- Test: `tests/test_repo_layout.py`
- Test: `tests/test_role_bridge.py`

**Step 1: Write failing role-surface tests**

Cover:
- source and runtime researcher skill presence
- role config presence
- role bridge resolution for `researcher`

**Step 2: Run tests to confirm failure**

Run: `uv run pytest -q tests/test_internal_skills.py tests/test_repo_layout.py tests/test_role_bridge.py`
Expected: FAIL because the role surface does not exist yet.

**Step 3: Add the Researcher role**

Add:
- skill contract
- runtime mirror
- role config
- role-bridge entry

**Step 4: Re-run tests**

Run: `uv run pytest -q tests/test_internal_skills.py tests/test_repo_layout.py tests/test_role_bridge.py`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/researcher .agents/skills/researcher .codex/roles/researcher.toml .codex/config.toml .codex/role_bridge.toml scripts/check_repo.py tests/test_internal_skills.py tests/test_repo_layout.py tests/test_role_bridge.py
git commit -m "feat: add researcher discovery role surface"
```

### Task 3: Make Office-Hours Challenge Passes Consume Research

**Files:**
- Modify: `scripts/role_review.py`
- Test: `tests/test_role_review.py`

**Step 1: Write failing tests**

Cover:
- Product office-hours challenge references research-backed options
- Design office-hours challenge reacts to adoption/flow risks from research
- Architect office-hours challenge reacts to build-vs-buy posture from research

**Step 2: Run tests to confirm failure**

Run: `uv run pytest -q tests/test_role_review.py`
Expected: FAIL because office-hours mode does not accept or consume research context yet.

**Step 3: Extend deterministic role review**

Add research-aware office-hours behavior so Product, Design, and Architect read both:
- office-hours brief
- research report

**Step 4: Re-run tests**

Run: `uv run pytest -q tests/test_role_review.py`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/role_review.py tests/test_role_review.py
git commit -m "feat: add research-aware office-hours challenge passes"
```

### Task 4: Integrate Research-First Office-Hours Flow

**Files:**
- Modify: `scripts/lead_loop.py`
- Modify: `.agents/skills/team-lead/SKILL.md`
- Modify: `.agents/skills/product-discovery/SKILL.md`
- Create or Modify: `skills/researcher/SKILL.md`
- Test: `tests/test_lead_loop.py`
- Test: `tests/test_team_lead_contract.py`
- Test: `tests/test_internal_role_contracts.py`

**Step 1: Write failing flow tests**

Cover:
- `office-hours run` writes office-hours brief, research brief, research report, challenge passes, discovery gate, and office-hours report
- board transition behavior remains correct across `ready-for-plan`, `reframe`, and `ask-user`
- office-hours report links research artifacts

**Step 2: Run tests to confirm failure**

Run: `uv run pytest -q tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py`
Expected: FAIL because office-hours does not yet run the research-first chain.

**Step 3: Implement the deterministic research-first lane**

Extend `lead_loop.py office-hours` so `run`:
- creates `research-brief`
- creates deterministic `research-report`
- passes research context into Product / Design / Architect challenge passes
- writes a research-aware discovery gate
- writes an office-hours report that references research

**Step 4: Update role contracts**

Update:
- `team-lead`
- `product-discovery`
- `researcher`

so the lane is discoverable in the runtime surface.

**Step 5: Re-run tests**

Run: `uv run pytest -q tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py`
Expected: PASS

**Step 6: Commit**

```bash
git add scripts/lead_loop.py .agents/skills/team-lead/SKILL.md .agents/skills/product-discovery/SKILL.md skills/researcher/SKILL.md tests/test_lead_loop.py tests/test_team_lead_contract.py tests/test_internal_role_contracts.py
git commit -m "feat: add research-first office-hours flow"
```

### Task 5: Sync Runtime Pack And Canonical State

**Files:**
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/project/TECH_DEBT.md`
- Modify: `docs/status/EXECUTION_BOARD.md`
- Modify: `CHANGELOG.md`
- Modify: `plugins/helm4codex/assets/runtime-pack/**`

**Step 1: Update canonical state**

Record that:
- office-hours now includes research-first pressure
- Researcher is part of the discovery harness
- the next gap is live discovery execution rather than missing research artifacts

**Step 2: Export the runtime pack**

Run: `uv run python scripts/export_plugin_runtime.py`
Expected: runtime-pack mirror refreshes without error.

**Step 3: Run full verification**

Run:

```bash
uv run pytest -q
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
uv run python scripts/export_plugin_runtime.py --check .
```

Expected:
- all tests pass
- `repo layout ok`
- `docs structure ok`
- `plugin runtime pack ok`

**Step 4: Commit**

```bash
git add docs/project/PROJECT_BRIEF.md docs/project/ROADMAP.md docs/project/TECH_DEBT.md docs/status/EXECUTION_BOARD.md CHANGELOG.md plugins/helm4codex/assets/runtime-pack
git commit -m "docs: record office-hours research tranche"
```
