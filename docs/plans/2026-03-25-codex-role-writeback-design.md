# Codex Role Writeback Design

## Goal

Move the review flow from lead-owned result capture to direct internal role-owned writeback, while adding Codex-native role configuration so the internal team is discoverable and reusable as first-class agent roles.

## Options Considered

### Option 1: Keep Lead-Owned Result Capture

Continue letting subagents return structured review results in chat while the lead writes those results into repo artifacts.

Pros:
- no new runtime surface
- simple to reason about

Cons:
- the lead still acts as a transcriber
- weakens the team illusion
- does not use Codex role configuration beyond the top-level lead

### Option 2: Direct Role-Owned Review-Result Writeback

Teach review packets to include an explicit writeback protocol and let Product, Architect, and Reviewer subagents write their own structured `review-result` artifacts directly into the repository.

Pros:
- removes lead-side transcription for live review
- strengthens the team model
- builds naturally on phase 9

Cons:
- requires stronger writeback contracts
- needs validation to keep write ownership predictable

### Option 3: Direct Role-Owned Review-Pass Writeback

Skip `review-result` and have internal reviewers write canonical review-pass files directly.

Pros:
- fewer artifact layers
- shortest runtime path

Cons:
- too abrupt a jump from the current design
- makes fallback and collection behavior harder to preserve
- gives up the useful separation between live role output and canonical collected pass

## Recommendation

Take Option 2.

This keeps the current phase 9 architecture intact while making the live review path more autonomous. It also creates the right foundation for later promotion from role-owned `review-result` files to more direct canonical writes if needed.

## Codex-Specific Additions

Phase 10 should add Codex-native role configuration, not just more markdown contracts.

That means:

- repo-scoped `.codex/config.toml`
- named internal review agent roles
- role-specific config files
- skill-level `agents/openai.yaml` metadata for the key internal review skills

This aligns with Codex guidance that `AGENTS.md`, `skills`, and `multi-agents` are complementary layers, and that agent roles can be described in project-scoped `.codex/config.toml`.

## Scope

Phase 10 adds:

- direct `review-result` writeback protocol inside review packets
- internal review-role contracts that explicitly own `review-result` writeback
- Codex role metadata for Product, Architect, and Reviewer skills
- project-scoped Codex role config for internal review agents

Phase 10 does not add:

- persistent background agents
- direct role-owned `review-pass` writes
- automatic spawning from inside repo scripts

## Runtime Shape

The live review path becomes:

1. `review-prepare`
   - generate review packets
   - include direct writeback target and writeback command shape

2. internal role execution
   - Product, Architect, and Reviewer subagents read their packets
   - each role writes its own `review-result` file into the repo

3. `review-collect`
   - the lead converts those role-owned results into canonical review passes
   - the existing review-gate aggregation stays intact

## Validation Strategy

This tranche is complete when:

- review packets expose a stable direct writeback protocol
- Product, Architect, and Reviewer contracts explicitly support direct `review-result` writeback
- `.codex/config.toml` defines internal review roles with role config files
- internal role skills include Codex metadata via `agents/openai.yaml`
- full repo verification passes

