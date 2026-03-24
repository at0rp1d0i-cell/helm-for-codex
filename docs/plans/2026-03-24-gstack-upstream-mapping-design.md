# gstack Upstream Mapping Design

<execution_handoff>
  <executor>codex</executor>
  <primary_mode>subagent-driven-development</primary_mode>
  <alternate_mode>executing-plans</alternate_mode>
  <rule>Use upstream gstack as a reference input, not a template to copy verbatim.</rule>
</execution_handoff>

**Goal:** Turn the current Codex-native AI team repo from a conceptually gstack-inspired system into an upstream-informed system with explicit preserve/adapt/reject decisions.

**Context:** The first three phases were designed from the user goal, Codex behavior, and local harness experiments. After checking out `garrytan/gstack`, we now have the real upstream skill corpus available for line-by-line comparison.

## What gstack actually contributes

1. A staged software factory mindset.
   `office-hours -> plan reviews -> build -> review -> qa -> ship -> retro`

2. Strong role posture.
   Each skill is written as a specialist with a clear worldview, not a generic helper.

3. Artifact handoff discipline.
   Design docs and review outputs feed later phases instead of disappearing into chat history.

4. Review pipeline composition.
   `/autoplan` is the clearest example: multiple review passes are chained, auto-decisions are logged, and only taste decisions are escalated.

5. Runtime harness expectations.
   gstack assumes setup hooks, telemetry, repo mode, shared preamble rules, and generated skill outputs.

## What we should preserve

- The staged workflow idea.
- The role-specialist posture.
- The requirement that discovery produces an artifact, not just chat.
- The idea that multi-pass review can be automated and surfaced as a final approval gate.
- The insistence that a plan carries its own review status.

## What we should adapt for Codex

- Slash-command skills become a single visible `team-lead` with internal role routing.
- Shared state should live in repo-backed canonical docs, not in repeated skill preambles.
- Interactive question loops should become narrower approval gates, because Codex subagent orchestration is more valuable than repeatedly pausing the user.
- Review chaining should become a lead-managed pipeline, not a user-invoked sequence of slash commands.
- Runtime harness should prefer Python scripts and repo checks over shell-heavy telemetry and setup scaffolding.

## What we should reject

- Repeating the same large preamble in every skill.
- User telemetry, contributor logging, and upgrade flows inside every role skill.
- Claude-specific `AskUserQuestion` ceremony as the core orchestration mechanism.
- A public surface with many peer slash skills.
- Copying gstack prose style or persona language directly.

## Mapping Table

| gstack upstream | Codex-native equivalent |
|---|---|
| `/office-hours` | `team-lead` intake and discovery flow |
| `/plan-ceo-review` + `/plan-eng-review` + `/plan-design-review` | internal role reviews orchestrated by lead |
| `/autoplan` | future lead-managed review pipeline with approval-needed gate |
| design doc in external gstack project store | canonical repo-backed discovery and planning artifacts |
| slash-command specialist surface | single-entry lead plus internal roles |
| repeated skill preamble | short `AGENTS.md` + scripts + repo checks |

## Recommended next slice

Phase 4 should port the most valuable upstream behavior first:

1. Add repository-backed discovery artifacts.
2. Add repository-backed planning artifacts.
3. Extend `lead_loop.py` so the lead can move `intake -> discovery -> plan -> build` through commands that create those artifacts and update canonical state.
4. Teach `team-lead` to use those commands explicitly.

This is the smallest slice that captures the real gstack value:
not its prose, but its handoff discipline.

## Non-goals for Phase 4

- Full `/autoplan` parity.
- Full review pipeline automation.
- Telemetry or runtime setup parity.
- Template generation or upstream compatibility tooling.
- Reproducing the upstream slash-command surface.
