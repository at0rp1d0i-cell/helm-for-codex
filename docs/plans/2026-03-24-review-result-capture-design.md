# Review Result Capture Design

## Goal

Reduce lead-side transcription during live subagent review by introducing a structured review-result handoff that can be collected into canonical review passes.

## Options Considered

### Option 1: Keep Manual Lead Transcription

Continue using review packets plus free-form subagent replies, with the lead manually converting replies into canonical review passes.

Pros:
- zero new runtime surface
- flexible human interpretation

Cons:
- high coordination cost
- easy to introduce drift between subagent output and canonical pass
- weak foundation for stronger internal-team automation

### Option 2: Structured Review Result Capture

Require internal review roles to respond in a stable review-result format. The lead records those results and uses repo automation to collect them into canonical review passes and the existing review gate.

Pros:
- lowers lead-side transcription cost
- keeps repo-as-memory intact
- introduces a testable capture layer
- stays compatible with current Codex session constraints

Cons:
- still requires the lead to place role output into repo artifacts
- not yet true autonomous worker writeback

### Option 3: Direct Child-Agent Canonical Writes

Push internal reviewers to write canonical review-pass files directly.

Pros:
- smallest lead role during review execution
- closest to a true internal team

Cons:
- fragile write ownership
- harder to validate and recover from partial writes
- too big a jump from the current hybrid model

## Recommendation

Take Option 2.

This is the smallest tranche that meaningfully improves the team model. It removes the most repetitive part of live review while preserving clean ownership of canonical state.

## Scope

Phase 9 adds:

- a repo-backed `review-result` artifact
- a `lead_loop.py review-collect` command that converts structured role results into canonical review passes
- contract updates so live subagent review uses `review-result` as the preferred response shape
- retention of phase 8 review packets, phase 7 deterministic fallback, and the existing review gate aggregation

Phase 9 does not add:

- direct child-agent writes into canonical review-pass files
- persistent role lifecycle management
- background autonomous review execution

## Runtime Shape

The review path becomes:

1. `review-prepare`
   - generate Product, Architect, and Reviewer packets
   - include the expected response shape and result target

2. live subagent execution
   - each subagent returns a structured review-result

3. `review-collect`
   - convert review-result files into canonical review-pass files
   - aggregate them through the existing review gate path

## Artifacts

### Review Packet

The packet remains the lead-authored handoff and now points the role at the review-result response shape.

### Review Result

The review result is the role-authored structured response. It should include:

- role
- focus
- findings
- auto decisions
- taste decisions
- recommendation

### Review Pass

The review pass remains the canonical stored review artifact that downstream review-gate logic reads.

## Validation Strategy

This tranche is complete when:

- `review-result` artifacts can be created and tested
- `review-collect` can turn role results into canonical review passes
- the lead contract documents review-result capture as the preferred live subagent path
- full repo checks still pass

