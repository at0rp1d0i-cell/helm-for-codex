# Ship/Release Gate Design

## Goal

Turn the current release-gate slice into a bounded ship/release loop that stays repo-backed and stops short of deployment automation.

## Approved Option

Option 1: add a first-class `release-prep-report` between `docs-sync` and `release-gate`, keep the board at `ship-ready`, and let `Ops` own both preparation and final release readiness writeback.

## Scope

This tranche adds:

- a canonical `release-prep-report` artifact
- an updated `release-prepare` flow that writes the prep report before emitting the release-manager packet
- a `release-gate` flow that consumes the prep report and carries its readiness checklist forward
- release-manager contract, template, and validation updates for the new artifact

This tranche does not add:

- deploy automation
- canary or benchmark lanes
- automatic PR creation or merge execution

## Flow

`docs-sync-report` remains the upstream readiness checkpoint.

`release-prepare` now writes `release-prep-report`, which captures:

- consumed implementation, QA, and docs-sync evidence
- planned verification commands
- coverage, version/changelog, and merge/PR preparation plans
- readiness checklist items and bounded follow-ups

The release-manager packet consumes that prep report plus upstream artifacts.

`release-gate` consumes the prep report, records actual verification status and blockers, and writes the canonical go/no-go artifact without inventing a new board stage.

## Rationale

This keeps the release lane repo-backed instead of hiding the planning step inside packet prose. It also gives later tranches a stable place to attach richer ship ergonomics without taking on deploy or operational follow-through yet.
