# Helm4Codex vs gstack Gap Assessment

## Scope

This document compares the latest `gstack` main branch, fetched on 2026-03-27 at `18bf424`, against the current `Helm4Codex` runtime.

The goal is not to clone gstack command-for-command. The goal is to identify where `Helm4Codex` already exceeds gstack's orchestration core, and where it still lacks the productized workflows that make gstack feel "ready to use every day."

## Summary

`Helm4Codex` is already stronger than gstack on repo-backed orchestration architecture:

- single visible `Lead` plus explicit `Ops`
- canonical project state in the repo
- packet/spec/bridge/receipt execution chain
- install, bootstrap, and upgrade surfaces for Codex repos
- onboarding and repository adoption state

But `gstack` is still ahead on productized workflow maturity. Its strongest advantage is not "more agents." It is that core builder loops already feel finished:

- product reframing
- auto-reviewed planning
- browser-backed QA with evidence
- shipping and release hygiene
- post-ship documentation and deploy follow-through

That is the main gap to close.

## Where Helm4Codex Already Leads

### 1. Orchestration Architecture

`Helm4Codex` has a clearer internal operating model:

- `Lead -> Ops -> Specialists`
- repo-backed dispatch packets
- invocation specs
- bridge-launch payloads
- execution receipts

This is more explicit than gstack's slash-command chaining model.

### 2. Repo-Backed State

`Helm4Codex` stores team state directly in canonical files:

- `docs/project/*`
- `docs/status/*`
- `docs/decisions/*`

This makes project continuity stronger across sessions and installations.

### 3. Codex-Native Distribution

`Helm4Codex` already has:

- repo-local `.agents/skills`
- `.codex` role bindings
- runtime pack installer
- plugin bootstrap path
- explicit upgrade flow

This is more native to Codex than gstack's original Claude-first surface.

## Highest-Value Gaps

### Gap 1. Product Discovery Is Not Yet a Signature Workflow

gstack has `/office-hours`, `/plan-ceo-review`, `/plan-design-review`, and `/design-consultation`. These do more than collect requirements. They challenge framing, force tradeoffs, and make the builder feel like they are getting cross-functional product pressure.

`Helm4Codex` has onboarding and discovery scaffolding, but it does not yet have a polished, opinionated discovery loop that feels like "talk to a sharp product team and get a stronger project back."

What is missing:

- a repeatable discovery conversation that reframes the problem
- first-class product and design pressure, not just architecture pressure
- a default artifact chain from discovery to plan

### Gap 2. Autoplan Is Still Weaker Than gstack's Review Pipeline

gstack's `/autoplan` is one of its strongest surfaces. It chains CEO, design, and engineering review, auto-resolves low-risk decisions, and only escalates taste decisions.

`Helm4Codex` already has review passes, review gates, and taste-decision concepts. But it still lacks a one-command plan gauntlet that feels finished.

What is missing:

- a first-class `autoplan` user workflow
- clearer distinction between auto-clear, ask, and blocked outcomes
- smoother review-readiness UX for plans

### Gap 3. QA Needs Real Browser Evidence

gstack's QA lane is much more mature because it uses a persistent browser workflow and screenshot evidence as first-class outputs.

`Helm4Codex` has `qa-runner`, but not the same operational surface.

What is missing:

- browser-backed QA execution
- screenshot or evidence artifacts
- authenticated-session testing helpers
- a clean `qa-only` report mode

### Gap 4. Release and Ship Workflow Is Underpowered

gstack's `/ship` is not just "run tests and push." It bundles:

- merge-base sync
- test and coverage audit
- changelog/version handling
- PR creation
- readiness framing
- downstream doc updates

`Helm4Codex` has `release-manager`, but it does not yet provide an end-to-end ship lane with that level of default rigor.

What is missing:

- a bounded ship pipeline with release gate artifacts
- coverage-aware release readiness
- version/changelog workflow
- PR or merge preparation ergonomics

### Gap 5. Post-Ship and Operational Follow-Through

gstack extends beyond "branch ready":

- `/land-and-deploy`
- `/canary`
- `/benchmark`
- `/document-release`

`Helm4Codex` currently stops earlier. This makes it strong as an orchestration kernel, but weaker as a daily shipping system.

What is missing:

- deploy follow-through
- post-release validation
- benchmark/perf evidence
- automated doc release sync as part of ship

### Gap 6. Specialized Quality Loops Are Still Thin

gstack has specialized lanes like:

- `/investigate`
- `/cso`
- `/design-review`

`Helm4Codex` has building blocks for these concerns, but not equivalent packaged workflows.

What is missing:

- a root-cause-first investigation workflow
- first-class security audit workflow
- stronger design quality loop

## Lower-Priority Productization Gaps

These matter, but they are not the first things to build:

- proactive skill suggestions
- opt-in telemetry and contributor feedback loops
- review-readiness dashboards
- global self-update ergonomics similar to `/gstack-upgrade`
- richer public examples and workflow demos

## Recommended Gap-Closing Order

### 1. Ship and Release Gate

This is the highest leverage next tranche.

Reason:

- it turns bounded execution into a real daily shipping loop
- it closes a very visible gap with gstack
- it forces stronger QA, docs, and verification integration

### 2. Browser-Backed QA Evidence

This is the next most important gap.

Reason:

- it upgrades QA from "role exists" to "QA has eyes"
- it produces visible trust artifacts
- it improves installed-runtime validation in real repos

### 3. Autoplan Productization

This should come next.

Reason:

- the underlying review primitives already exist
- the missing piece is user-facing productization
- this directly attacks the "one command, reviewed plan" gap

### 4. Office-Hours Style Product Discovery

This should follow once plan and ship loops are sharper.

Reason:

- the current discovery model is solid but not memorable
- a stronger discovery lane will improve the quality of everything downstream

## Recommendation

Do not chase gstack feature parity line-by-line.

Instead:

1. keep the `Lead -> Ops -> Specialists` architecture intact
2. preserve repo-backed state and dispatch artifacts
3. selectively import the productized workflows where gstack is strongest

That means the next Helm4Codex roadmap should prioritize:

- `ship`
- `browser-qa`
- `autoplan`
- `office-hours`

in that order.
