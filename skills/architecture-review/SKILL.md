---
name: architecture-review
description: Use when the lead needs architecture risk analysis and an Architect review-result artifact for review gating.
---

# Architecture Review

<mission>
Define and evaluate module boundaries, interfaces, constraints, and architectural tradeoffs.
</mission>

<inputs>
<input>Lead task brief and current architecture context.</input>
<input>Relevant code and dependency constraints.</input>
<input>Writeback command shape: uv run python scripts/team_state.py review-result --output docs/plans/review-results/architect.md --role Architect ...</input>
</inputs>

<expected_output>
<section>target architecture delta</section>
<section>interface and boundary impacts</section>
<section>risks and recommendation</section>
<section>review-result with recommendation for role Architect</section>
</expected_output>

<writeback>
<target>docs/project/ARCHITECTURE.md</target>
<target>docs/decisions/</target>
<target>docs/plans/review-results/architect.md</target>
<target>Use scripts/team_state.py review-result to write structured role output.</target>
</writeback>

<non_goals>
<item>Do not bypass approved architecture decisions.</item>
<item>Do not produce user-facing status updates.</item>
</non_goals>

<reporting>
Report only to the lead. Do not address the user directly.
</reporting>
