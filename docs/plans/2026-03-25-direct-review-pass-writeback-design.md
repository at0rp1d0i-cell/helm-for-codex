# Direct Review-Pass Writeback Design

## Goal

Promote live internal review from direct role-owned `review-result` writeback to direct role-owned canonical `review-pass` writeback, while keeping the lead responsible for review-gate aggregation and approval escalation.

## Options Considered

### Option 1: Keep `review-result` As The Preferred Live Path

Continue using review packets that tell Product, Architect, and Reviewer to write `review-result` files, then let the lead collect those files into canonical `review-pass` artifacts.

Pros:
- preserves the phase 10 flow exactly
- keeps a clear separation between raw live output and canonical pass state

Cons:
- still keeps an unnecessary intermediate artifact in the common path
- leaves live subagents on a different path from deterministic `role_review.py`
- keeps extra lead-side orchestration even when child roles can already write structured artifacts

### Option 2: Promote Direct Role-Owned `review-pass` Writeback

Update the preferred live path so Product, Architect, and Reviewer write canonical `review-pass` artifacts directly into the repo, while the lead still aggregates those passes into a `review-gate`.

Pros:
- makes live review and deterministic review converge on the same artifact contract
- reduces orchestration overhead in the common path
- strengthens the internal team model by giving roles direct ownership of canonical review artifacts
- keeps the lead in charge of final gate construction and escalation

Cons:
- requires tighter writeback discipline
- requires role contracts, role config, and packet content to change together

### Option 3: Full Direct Gate Ownership By Internal Roles

Let internal roles write directly into a final `review-gate` or let one of the internal roles own gate generation.

Pros:
- shortest possible lead path

Cons:
- weakens the single visible lead model
- blurs the separation between specialist review and final approval synthesis
- makes escalation policy harder to keep centralized

## Recommendation

Take Option 2.

This keeps the single-entry lead intact while removing a now-redundant artifact hop from the preferred live review path. It also aligns live subagent execution with the deterministic `role_review.py` path, because both flows will produce the same canonical `review-pass` shape.

## Scope

Phase 11 adds:

- direct `review-pass` writeback as the preferred live review packet contract
- Product, Architect, and Reviewer contracts that explicitly own canonical `review-pass` writeback
- Codex role config that points internal review roles at canonical `review-pass` targets
- lead contract and project state updates that make direct `review-pass` ownership the preferred live path

Phase 11 keeps:

- `review-result` artifact support for compatibility and recovery
- lead-owned review-gate aggregation
- deterministic `role_review.py` fallback

Phase 11 does not add:

- direct internal role ownership of `review-gate`
- persistent background agent lifecycle tracking
- QA or Docs live role promotion in this tranche

## Runtime Shape

The preferred live review path becomes:

1. `review-prepare`
   - generate Product, Architect, and Reviewer packets
   - point each packet at canonical `review-pass` targets
   - include a concrete `scripts/team_state.py review-pass` command shape

2. internal role execution
   - Product, Architect, and Reviewer subagents read their packets
   - each role writes its own canonical `review-pass` file into the repo

3. lead aggregation
   - the lead reads canonical `review-pass` files
   - the lead writes the `review-gate`
   - unresolved taste decisions still trigger `approval-needed`

Compatibility path:

- `review-result` plus `review-collect` stays available when a session still uses phase 10 style capture or when partial recovery is needed

## Validation Strategy

This tranche is complete when:

- review packets point live roles at direct canonical `review-pass` writeback
- Product, Architect, and Reviewer contracts explicitly reference `review-pass` ownership
- repo-scoped Codex role config targets canonical `review-pass` files
- the lead contract documents direct `review-pass` ownership as the preferred live path
- full repo verification passes
