# Codex-Native AI Team Design

**Date:** 2026-03-24

## Goal

Build a Codex-native system that feels like working with a strong software team through a single conversation with one responsible lead. The user provides ideas, constraints, and approvals. The system turns those inputs into plans, code, tests, docs, reviews, QA, and an evolution path without forcing the user to manually manage multiple roles.

## Product Principles

1. Single entry point. The user only talks to one lead.
2. Team feeling, not skill roulette. Internal roles exist to divide responsibility, not to create prompt theater.
3. Repo as memory. Shared project state lives in the repository, not in a long AGENTS file or chat history.
4. Low communication overhead. The system should reduce repeated explanation, rework, and context pollution.
5. Quality is enforced by gates and checks. High quality cannot depend on reminders alone.
6. Research before reinvention. Discovery must prevent avoidable wheel reinvention in both 0-1 work and implementation spikes.
7. Refactor with permission. Structural cleanup is encouraged, but major refactors require an explicit proposal and user approval.

## User Experience

The user interacts with a single `Lead` role. Internally, the system coordinates a virtual team. The lead should:

- absorb messy user input and restate it as goals, constraints, and next steps
- keep execution moving without frequent interruption
- escalate only when a decision materially affects scope, architecture, cost, or refactor risk
- return with synthesized updates rather than raw subagent noise

The intended feel is "one capable engineering lead running a team for me," not "I am manually switching between agents."

## Team Model

### External Interface

- `Lead`: the only role visible to the user

### Internal Fixed Responsibilities

- `Product`: refines goals, scope, milestones, and product tradeoffs
- `Researcher`: performs product and technical discovery when uncertainty or cost justifies it
- `Architect`: defines module boundaries, interfaces, constraints, and evolution paths
- `Builder`: implements bounded tasks
- `Reviewer`: independently checks correctness, regression risk, and completeness
- `QA`: validates user flows and regressions
- `Docs`: keeps project docs and decision records current
- `Refactor Planner`: proposes structural cleanup when quality debt blocks safe progress
- `Release`: packages readiness, rollout, and post-change verification

Roles are fixed responsibilities, not always-live agents. Runtime concurrency stays small even if the role model is rich.

## Runtime Architecture

The system should be modeled as three layers:

### 1. Lead Layer

Handles user dialogue, interprets intent, chooses when to ask for approval, and synthesizes team output.

### 2. Ops Layer

Maintains shared project state, selects the current workflow stage, dispatches subagents, and enforces gates.

### 3. Worker Layer

Runs bounded specialist tasks with narrow context and clear ownership.

This separation avoids overloading a single agent with user conversation, project management, and implementation at the same time.

## Shared Project State

Shared state must stay small and canonical. It is not a general knowledge base.

### Canonical Files

- `docs/project/PROJECT_BRIEF.md`
- `docs/project/ROADMAP.md`
- `docs/project/ARCHITECTURE.md`
- `docs/project/QUALITY_BAR.md`
- `docs/project/TECH_DEBT.md`
- `docs/status/EXECUTION_BOARD.md`
- `docs/status/MODULE_CONTRACTS/*.md`
- `docs/decisions/YYYY-MM-DD-*.md`
- `docs/plans/YYYY-MM-DD-*.md`

### Rules

1. Only a small set of files count as truth sources.
2. Derived summaries may be regenerated and should not become competing truth.
3. State is updated when the project changes state, not on every chat turn.
4. Append-only logs are preferred where possible.
5. Every canonical file has a clear owner, usually `Lead` or `Ops`.

## AGENTS.md Strategy

`AGENTS.md` should remain short and act as a router:

- define the single-entry team model
- identify the canonical project-state files
- define approval escalation rules
- describe how internal skills and subagents should be used

It should not become a giant instruction dump. Long-lived guidance belongs in skill files or repository docs that can be loaded progressively.

## Workflow State Machine

The default state machine is:

`intake -> discovery -> plan -> approval-needed -> build -> review -> qa -> docs-sync -> ship-ready -> evolve`

### Notes

- `discovery` is a first-class stage, not a small preamble.
- discovery can be re-entered from `build` when the team hits a new technical unknown.
- `approval-needed` is the only normal pause state for user decisions.
- the system should prefer long execution windows with few interruptions.

## Discovery and Research

Discovery splits into two modes:

- `product discovery`: users, workflows, alternatives, scope, and UX references
- `technical discovery`: papers, open source projects, official docs, libraries, and build-vs-buy analysis

Research should be mandatory for high-uncertainty or high-cost decisions, including:

- new project foundations
- unfamiliar frameworks or infrastructure
- papers or advanced technical methods
- likely existing open-source solutions
- performance or architecture bottlenecks where naive implementation is risky

Users may also explicitly request research at any time.

Research output should stay compressed:

- problem
- search scope
- top options
- recommendation
- adoption notes
- open risks

## Parallelism Model

The system should separate role richness from runtime concurrency.

### Defaults

- active subagents: usually 1-3
- common steady-state pattern: 1-2 builders plus 1 reviewer or QA seat

### Parallelism Preconditions

Parallel implementation is allowed only when:

- module boundaries are defined
- interface contracts are written
- ownership is explicit
- write scopes are mostly disjoint
- integration points are known

The system must not pretend that five vague tasks can safely run in parallel just because five modules exist on paper.

## Quality System

Quality should be enforced by both workflow gates and repository checks.

### Workflow Gates

- `plan -> build`: goals, boundaries, constraints, and test strategy must exist
- `build -> review`: implementation and relevant tests must exist
- `review -> qa`: major findings must be resolved or explicitly logged
- `qa -> docs-sync`: critical paths must pass or be tracked
- `docs-sync -> ship-ready`: project state and docs must be synchronized

### Quality Bar

The system should optimize for:

- modular code
- explicit boundaries
- current docs
- meaningful tests
- visible technical debt
- willingness to pause for cleanup when further feature work would compound damage

## Refactor Policy

When the system determines that quality is too poor for safe feature work:

1. do not silently refactor
2. move to `approval-needed`
3. invoke `Refactor Planner`
4. produce a proposal covering:
   - problem scope
   - why the cleanup is necessary now
   - viable options
   - risks
   - smallest useful intervention
5. wait for user approval before structural work

This keeps the system brave about quality without making it reckless.

## Proposed Repository Skeleton

```text
.
├── AGENTS.md
├── docs/
│   ├── project/
│   │   ├── PROJECT_BRIEF.md
│   │   ├── ROADMAP.md
│   │   ├── ARCHITECTURE.md
│   │   ├── QUALITY_BAR.md
│   │   └── TECH_DEBT.md
│   ├── decisions/
│   ├── plans/
│   └── status/
│       ├── EXECUTION_BOARD.md
│       └── MODULE_CONTRACTS/
├── ops/
│   ├── templates/
│   └── checks/
└── skills/
    ├── team-lead/
    ├── product-discovery/
    ├── architecture-review/
    ├── implementation-worker/
    ├── code-reviewer/
    ├── qa-runner/
    ├── docs-sync/
    ├── refactor-planner/
    └── release-manager/
```

## First-Version Scope

Version 1 should focus on the minimum viable orchestration system:

- one visible `team-lead` entry point
- internal role skills with clear boundaries
- canonical project-state files
- templates for task briefs, review reports, QA reports, and refactor proposals
- a simple execution board
- quality-bar documentation
- initial checks for doc freshness and structural boundaries

Version 1 should not assume:

- unlimited always-on background agents
- high parallel fan-out
- perfect automatic synchronization
- full autonomous project creation without approval gates

## Success Criteria

The first useful version should:

1. let the user talk to a single lead while still benefiting from internal delegation
2. reduce repeated explanation compared with a single long-running general-purpose agent
3. preserve project intent through repository state, not fragile chat memory
4. keep quality visible through plans, reviews, QA, docs, and refactor proposals
5. make future implementation of a real Codex-native AI team straightforward
