# Subagent Review Runtime Design

## Goal

Move phase 7's deterministic review runtime toward a real Codex-native internal review team without introducing a heavy persistent agent runtime.

## Options Considered

### Option 1: Session-Only Review Delegation

Have the lead spawn Product, Architect, and Reviewer subagents directly and summarize their responses in chat.

Pros:
- fastest to start
- uses real subagents immediately

Cons:
- no repo-backed handoff artifact
- weak repeatability
- poor testing surface
- easy to drift from canonical state

### Option 2: Hybrid Subagent Review Runtime

Use the repository to prepare role-scoped review packets and preserve canonical review passes, while the lead uses real Codex subagents to perform the actual analysis and report back.

Pros:
- keeps repo-as-memory intact
- uses real subagents now
- testable packet preparation and aggregation
- preserves the phase 7 deterministic runner as a fallback

Cons:
- still requires the lead to capture subagent output into repo artifacts
- not yet a persistent background team

### Option 3: Persistent Agent Team Runtime

Add a longer-lived internal runtime that tracks role lifecycles, agent ids, and background review execution.

Pros:
- closest to a true autonomous team
- strongest illusion of continuity

Cons:
- too heavy for this tranche
- higher lifecycle complexity than the current Codex environment justifies

## Recommendation

Take Option 2.

This keeps the single visible lead model intact while adding the first real Codex subagent execution path. It improves team feel without overfitting the repo to a long-lived runtime that the current environment does not naturally support.

## Scope

Phase 8 tranche 1 adds:

- a repo-backed `review packet` artifact for Product, Architect, and Reviewer
- a `lead_loop.py review-prepare` command that generates those packets from canonical state and a plan brief
- contract updates so the lead prefers subagent-backed review preparation over deterministic fallback when real internal review is desired
- retention of `review-run` and `scripts/role_review.py` as deterministic fallback and structural test baseline

Phase 8 tranche 1 does not add:

- persistent agent lifecycle tracking
- automated child-agent spawning from inside repo scripts
- direct child-agent file writes as the canonical path

## Runtime Shape

The lead should execute review in two layers:

1. Repository preparation
   - generate one packet per role
   - point each packet at canonical sources and the active plan brief
   - define the expected review-pass sections

2. Live subagent execution
   - spawn Product, Architect, and Reviewer subagents from the current session
   - provide the packet path and role objective
   - collect structured findings, auto-decisions, taste decisions, and recommendations
   - write canonical review-pass artifacts back into the repo
   - aggregate them with the existing review gate flow

## Artifacts

### Review Packet

The packet is a lead-authored handoff document. It should include:

- role
- review objective
- canonical sources to read
- plan brief path
- expected output sections
- writeback target

### Review Pass

The review pass remains the canonical result artifact. It is written by the lead based on live subagent output or deterministic fallback output.

## Fallback Strategy

`scripts/role_review.py` and `lead_loop.py review-run` remain supported.

They provide:

- structural test coverage
- deterministic local validation
- a fallback when live subagent execution is unavailable or unnecessary

## Validation Strategy

This tranche should be considered complete when:

- packet artifacts can be generated and tested
- lead orchestration can prepare Product, Architect, and Reviewer packets from canonical state
- the lead contract documents the preferred live subagent path and the deterministic fallback path
- repo checks and tests cover the new packet-based baseline

