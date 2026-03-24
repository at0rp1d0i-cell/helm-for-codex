# Codex-Native AI Team Bootstrap Implementation Plan

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Execute task-by-task with verification after each task.</rule>
</execution_handoff>

**Goal:** Bootstrap the first working repository skeleton for a Codex-native AI team system with a single-entry lead, canonical project-state docs, internal role skills, and basic repo validation.

**Architecture:** The repository acts as the system memory while `AGENTS.md` stays short and routes work into a small set of skills. A lightweight Python validation harness guards the required repo shape so the memory layer, role skills, and ops templates do not drift immediately.

**Tech Stack:** Markdown, Python 3.11+, `uv`, `pytest`, Codex `SKILL.md` skills, `agents/openai.yaml`

---

### Task 1: Bootstrap The Validation Harness

**Files:**
- Create: `pyproject.toml`
- Create: `scripts/check_repo.py`
- Create: `tests/test_repo_layout.py`

**Step 1: Write the failing test**

Create `tests/test_repo_layout.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_top_level_paths_exist() -> None:
    required = [
        ROOT / "docs" / "project",
        ROOT / "docs" / "plans",
        ROOT / "docs" / "status" / "MODULE_CONTRACTS",
        ROOT / "docs" / "decisions",
        ROOT / "ops" / "templates",
        ROOT / "ops" / "checks",
        ROOT / "skills" / "team-lead",
        ROOT / "scripts" / "check_repo.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []
```

**Step 2: Add the minimal Python project config**

Create `pyproject.toml`:

```toml
[project]
name = "codex-native-ai-team"
version = "0.1.0"
description = "Bootstrap harness for a Codex-native AI team"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = [
  "pytest>=8.4.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Step 3: Run test to verify it fails**

Run: `uv run pytest tests/test_repo_layout.py -q`  
Expected: `FAILED` with missing required paths.

**Step 4: Write minimal implementation**

Create `scripts/check_repo.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def required_paths() -> list[Path]:
    return [
        ROOT / "docs" / "project",
        ROOT / "docs" / "plans",
        ROOT / "docs" / "status" / "MODULE_CONTRACTS",
        ROOT / "docs" / "decisions",
        ROOT / "ops" / "templates",
        ROOT / "ops" / "checks",
        ROOT / "skills" / "team-lead",
    ]


def main() -> int:
    missing = [path for path in required_paths() if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(ROOT)}")
        return 1
    print("repo layout ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 5: Run the test again**

Run: `uv run pytest tests/test_repo_layout.py -q`  
Expected: still `FAILED`, but now only because the directories have not been created yet.

**Step 6: Commit**

```bash
git add pyproject.toml scripts/check_repo.py tests/test_repo_layout.py
git commit -m "chore: bootstrap repo validation harness"
```

### Task 2: Scaffold Canonical Project-State Files

**Files:**
- Create: `AGENTS.md`
- Create: `docs/project/PROJECT_BRIEF.md`
- Create: `docs/project/ROADMAP.md`
- Create: `docs/project/ARCHITECTURE.md`
- Create: `docs/project/QUALITY_BAR.md`
- Create: `docs/project/TECH_DEBT.md`
- Create: `docs/status/EXECUTION_BOARD.md`
- Create: `docs/status/MODULE_CONTRACTS/README.md`
- Create: `docs/decisions/.gitkeep`

**Step 1: Write the failing test**

Create `tests/test_project_state_docs.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text()


def test_canonical_state_docs_have_required_headings() -> None:
    expected = {
        "AGENTS.md": ["# AI Team Operating Guide", "## Single Entry", "## Canonical State"],
        "docs/project/PROJECT_BRIEF.md": ["# Project Brief", "## Problem", "## Success Criteria"],
        "docs/project/ROADMAP.md": ["# Roadmap", "## Current Milestone", "## Later Milestones"],
        "docs/project/ARCHITECTURE.md": ["# Architecture", "## Modules", "## Constraints"],
        "docs/project/QUALITY_BAR.md": ["# Quality Bar", "## Code", "## Tests", "## Docs"],
        "docs/project/TECH_DEBT.md": ["# Tech Debt", "## Active Debt", "## Deferred Debt"],
        "docs/status/EXECUTION_BOARD.md": ["# Execution Board", "## Current Stage", "## Active Work"],
        "docs/status/MODULE_CONTRACTS/README.md": ["# Module Contracts", "## Required Fields"],
    }
    for relpath, headings in expected.items():
        content = read(relpath)
        for heading in headings:
            assert heading in content, f"{heading} missing from {relpath}"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_project_state_docs.py -q`  
Expected: `FAILED` with file-not-found errors.

**Step 3: Write minimal implementation**

Create `AGENTS.md`:

```md
# AI Team Operating Guide

## Single Entry

The user speaks only to the lead. Internal specialist skills and subagents are coordinated behind that interface.

## Canonical State

Use these files as the source of truth:

- `docs/project/PROJECT_BRIEF.md`
- `docs/project/ROADMAP.md`
- `docs/project/ARCHITECTURE.md`
- `docs/project/QUALITY_BAR.md`
- `docs/project/TECH_DEBT.md`
- `docs/status/EXECUTION_BOARD.md`
- `docs/status/MODULE_CONTRACTS/`
- `docs/decisions/`
- `docs/plans/`

## Approval Escalation

Escalate to the user for structural refactors, major scope changes, high-impact architecture decisions, and cost-heavy dependency choices.
```

Create `docs/project/PROJECT_BRIEF.md`:

```md
# Project Brief

## Problem

Build a Codex-native AI team with a single lead interface and strong internal execution discipline.

## Current Goal

Bootstrap the repository skeleton and operating harness.

## Success Criteria

- single-entry lead model exists
- canonical project-state files exist
- internal role skills exist
- repo validation passes
```

Create `docs/project/ROADMAP.md`:

```md
# Roadmap

## Current Milestone

Bootstrap the repository structure, role skills, and validation harness.

## Later Milestones

- add richer role prompts
- add stronger checks
- add execution workflows
```

Create `docs/project/ARCHITECTURE.md`:

```md
# Architecture

## Layers

- Lead layer
- Ops layer
- Worker layer

## Modules

- canonical docs
- skills
- ops templates
- repo checks

## Constraints

- single visible lead
- small active concurrency
- repo as memory
```

Create `docs/project/QUALITY_BAR.md`:

```md
# Quality Bar

## Code

Prefer modular, bounded, readable implementations.

## Tests

Every structural rule added to the repo should have a validation check or test.

## Docs

Canonical project-state files must stay current when state changes.
```

Create `docs/project/TECH_DEBT.md`:

```md
# Tech Debt

## Active Debt

- none yet

## Deferred Debt

- richer automation and drift detection
```

Create `docs/status/EXECUTION_BOARD.md`:

```md
# Execution Board

## Current Stage

plan

## Active Work

- bootstrap repository skeleton
- create internal role skills
- add validation harness
```

Create `docs/status/MODULE_CONTRACTS/README.md`:

```md
# Module Contracts

## Required Fields

Each module contract should capture:

- purpose
- ownership
- inputs
- outputs
- dependencies
- test expectations
```

Create `docs/decisions/.gitkeep` as an empty file.

**Step 4: Run the targeted tests**

Run: `uv run pytest tests/test_repo_layout.py tests/test_project_state_docs.py -q`  
Expected: `FAILED` only because the skills and ops directories still do not exist.

**Step 5: Commit**

```bash
git add AGENTS.md docs/project docs/status docs/decisions/.gitkeep tests/test_project_state_docs.py
git commit -m "docs: add canonical project state files"
```

### Task 3: Create The Lead Skill

**Files:**
- Create: `skills/team-lead/SKILL.md`
- Create: `skills/team-lead/agents/openai.yaml`
- Create: `tests/test_team_lead_skill.py`

**Step 1: Write the failing test**

Create `tests/test_team_lead_skill.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_team_lead_skill_references_single_entry_and_canonical_state() -> None:
    content = (ROOT / "skills" / "team-lead" / "SKILL.md").read_text()
    assert "single visible lead" in content.lower()
    assert "docs/project/PROJECT_BRIEF.md" in content
    assert "approval-needed" in content
    assert "subagent" in content.lower()


def test_team_lead_openai_metadata_exists() -> None:
    content = (ROOT / "skills" / "team-lead" / "agents" / "openai.yaml").read_text()
    assert "display_name:" in content
    assert "description:" in content
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_team_lead_skill.py -q`  
Expected: `FAILED` with file-not-found errors.

**Step 3: Write minimal implementation**

Create `skills/team-lead/SKILL.md`:

```md
---
name: team-lead
description: Single-entry lead for a Codex-native AI team. Use when the user wants one responsible interface that can absorb ideas, maintain project state, delegate to internal specialist roles, and move the project through discovery, planning, build, review, QA, docs, and release with explicit approval gates.
---

# Team Lead

You are the single visible lead for this repository's AI team.

## Core Duties

- translate messy user input into project goals and next actions
- read and maintain canonical state in:
  - `docs/project/PROJECT_BRIEF.md`
  - `docs/project/ROADMAP.md`
  - `docs/project/ARCHITECTURE.md`
  - `docs/project/QUALITY_BAR.md`
  - `docs/project/TECH_DEBT.md`
  - `docs/status/EXECUTION_BOARD.md`
- keep the user experience centered on a single visible lead
- use subagent delegation only when it materially improves execution

## Workflow

Move work through:

`intake -> discovery -> plan -> approval-needed -> build -> review -> qa -> docs-sync -> ship-ready -> evolve`

## Escalation

Pause in `approval-needed` for structural refactors, large scope shifts, or major architecture choices.
```

Create `skills/team-lead/agents/openai.yaml`:

```yaml
display_name: Team Lead
description: Single-entry lead for the Codex-native AI team
allow_implicit_invocation: false
```

**Step 4: Run the targeted tests**

Run: `uv run pytest tests/test_team_lead_skill.py -q`  
Expected: `PASS`

**Step 5: Commit**

```bash
git add skills/team-lead tests/test_team_lead_skill.py
git commit -m "feat: add team lead skill"
```

### Task 4: Add Internal Role Skills

**Files:**
- Create: `skills/product-discovery/SKILL.md`
- Create: `skills/architecture-review/SKILL.md`
- Create: `skills/implementation-worker/SKILL.md`
- Create: `skills/code-reviewer/SKILL.md`
- Create: `skills/qa-runner/SKILL.md`
- Create: `skills/docs-sync/SKILL.md`
- Create: `skills/refactor-planner/SKILL.md`
- Create: `skills/release-manager/SKILL.md`
- Create: `tests/test_internal_skills.py`

**Step 1: Write the failing test**

Create `tests/test_internal_skills.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_internal_skills_exist_with_frontmatter() -> None:
    expected = [
        "product-discovery",
        "architecture-review",
        "implementation-worker",
        "code-reviewer",
        "qa-runner",
        "docs-sync",
        "refactor-planner",
        "release-manager",
    ]
    for name in expected:
        content = (ROOT / "skills" / name / "SKILL.md").read_text()
        assert content.startswith("---")
        assert f"name: {name}" in content
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_internal_skills.py -q`  
Expected: `FAILED` with file-not-found errors.

**Step 3: Write minimal implementation**

Create one short skill file per role. Use this shape and adapt the `name` and `description` line for each file:

```md
---
name: product-discovery
description: Internal specialist for turning product ideas into clarified goals, milestones, tradeoffs, and research questions for the team lead.
---

# Product Discovery

Operate as an internal specialist. Return concise findings and recommended next actions to the lead. Do not behave as the user-facing owner of the project.
```

Create equivalent files for:

- `skills/architecture-review/SKILL.md`
- `skills/implementation-worker/SKILL.md`
- `skills/code-reviewer/SKILL.md`
- `skills/qa-runner/SKILL.md`
- `skills/docs-sync/SKILL.md`
- `skills/refactor-planner/SKILL.md`
- `skills/release-manager/SKILL.md`

Each file should state its bounded role, the expectation to return structured output to the lead, and the rule that it is not the user-facing primary voice.

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_internal_skills.py -q`  
Expected: `PASS`

**Step 5: Commit**

```bash
git add skills tests/test_internal_skills.py
git commit -m "feat: add internal role skills"
```

### Task 5: Add Ops Templates And Repo Checks

**Files:**
- Create: `ops/templates/task-brief.md`
- Create: `ops/templates/review-report.md`
- Create: `ops/templates/qa-report.md`
- Create: `ops/templates/refactor-proposal.md`
- Create: `ops/checks/check_docs_freshness.py`
- Create: `tests/test_ops_templates.py`

**Step 1: Write the failing test**

Create `tests/test_ops_templates.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ops_templates_and_checks_exist() -> None:
    required = [
        ROOT / "ops" / "templates" / "task-brief.md",
        ROOT / "ops" / "templates" / "review-report.md",
        ROOT / "ops" / "templates" / "qa-report.md",
        ROOT / "ops" / "templates" / "refactor-proposal.md",
        ROOT / "ops" / "checks" / "check_docs_freshness.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ops_templates.py -q`  
Expected: `FAILED` with missing file paths.

**Step 3: Write minimal implementation**

Create `ops/templates/task-brief.md`:

```md
# Task Brief

## Objective

## Scope

## Constraints

## Relevant Decisions

## Expected Output

## Writeback Target
```

Create `ops/templates/review-report.md`:

```md
# Review Report

## Findings

## Risks

## Suggested Fixes

## Follow-Up
```

Create `ops/templates/qa-report.md`:

```md
# QA Report

## Environment

## Scenarios Tested

## Issues Found

## Verification Status
```

Create `ops/templates/refactor-proposal.md`:

```md
# Refactor Proposal

## Problem Scope

## Why Now

## Options

## Risks

## Minimum Useful Intervention
```

Create `ops/checks/check_docs_freshness.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    required = [
        ROOT / "docs" / "project" / "PROJECT_BRIEF.md",
        ROOT / "docs" / "project" / "ROADMAP.md",
        ROOT / "docs" / "project" / "ARCHITECTURE.md",
        ROOT / "docs" / "project" / "QUALITY_BAR.md",
        ROOT / "docs" / "status" / "EXECUTION_BOARD.md",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        for path in missing:
            print(f"MISSING {path.relative_to(ROOT)}")
        return 1
    print("docs freshness baseline ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_ops_templates.py -q`  
Expected: `PASS`

**Step 5: Run the lightweight checks**

Run: `uv run python scripts/check_repo.py && uv run python ops/checks/check_docs_freshness.py`  
Expected:

```text
repo layout ok
docs freshness baseline ok
```

**Step 6: Commit**

```bash
git add ops tests/test_ops_templates.py
git commit -m "feat: add ops templates and baseline checks"
```

### Task 6: Add The First Module Contract And Decision Record

**Files:**
- Create: `docs/status/MODULE_CONTRACTS/team-lead.md`
- Create: `docs/decisions/2026-03-24-single-entry-lead.md`
- Create: `tests/test_initial_records.py`

**Step 1: Write the failing test**

Create `tests/test_initial_records.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_initial_module_contract_and_decision_exist() -> None:
    contract = (ROOT / "docs" / "status" / "MODULE_CONTRACTS" / "team-lead.md").read_text()
    assert "# Module Contract: team-lead" in contract
    assert "## Inputs" in contract
    assert "## Outputs" in contract

    decision = (ROOT / "docs" / "decisions" / "2026-03-24-single-entry-lead.md").read_text()
    assert "# Decision: Single Entry Lead" in decision
    assert "## Context" in decision
    assert "## Decision" in decision
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_initial_records.py -q`  
Expected: `FAILED` with file-not-found errors.

**Step 3: Write minimal implementation**

Create `docs/status/MODULE_CONTRACTS/team-lead.md`:

```md
# Module Contract: team-lead

## Purpose

Provide the single visible entry point for the user.

## Ownership

Lead

## Inputs

- user requests
- canonical project state
- subagent results

## Outputs

- synthesized user updates
- delegated task briefs
- approval requests when required

## Dependencies

- canonical project docs
- internal role skills

## Test Expectations

- skill exists
- AGENTS routing stays aligned
```

Create `docs/decisions/2026-03-24-single-entry-lead.md`:

```md
# Decision: Single Entry Lead

## Context

The system should feel like working with one responsible engineering lead, not many visible agents.

## Decision

Expose one visible lead to the user and keep specialist roles internal.

## Consequences

- clearer user experience
- more pressure on the lead's orchestration quality
- stronger need for canonical project state
```

**Step 4: Run the targeted test**

Run: `uv run pytest tests/test_initial_records.py -q`  
Expected: `PASS`

**Step 5: Commit**

```bash
git add docs/status/MODULE_CONTRACTS/team-lead.md docs/decisions/2026-03-24-single-entry-lead.md tests/test_initial_records.py
git commit -m "docs: add initial contract and decision record"
```

### Task 7: Run Full Verification And Record The Bootstrap Baseline

**Files:**
- Modify: `docs/status/EXECUTION_BOARD.md`

**Step 1: Update the execution board**

Update `docs/status/EXECUTION_BOARD.md` to reflect the completed bootstrap baseline:

```md
# Execution Board

## Current Stage

evolve

## Active Work

- define next implementation tranche for richer orchestration

## Completed

- canonical project-state docs
- team lead skill
- internal role skills
- ops templates
- baseline repo checks
```

**Step 2: Run the full test suite**

Run: `uv run pytest -q`  
Expected: all tests `PASS`

**Step 3: Run the lightweight checks**

Run:

```bash
uv run python scripts/check_repo.py
uv run python ops/checks/check_docs_freshness.py
```

Expected:

```text
repo layout ok
docs freshness baseline ok
```

**Step 4: Commit**

```bash
git add docs/status/EXECUTION_BOARD.md
git commit -m "chore: record bootstrap baseline"
```
