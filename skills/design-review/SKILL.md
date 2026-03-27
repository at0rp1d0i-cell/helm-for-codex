---
name: design-review
description: Use when the lead needs interaction, usability, and workflow pressure before planning or during review gating.
---

# Design Review

<mission>
Challenge product framing through user-flow clarity, comprehension, interaction cost, and experience quality pressure.
</mission>

<inputs>
<input>Lead task brief, office-hours brief, or discovery artifact that needs design pressure.</input>
<input>Relevant product context, constraints, and target user or operator.</input>
<input>Writeback command shape: uv run python scripts/team_state.py review-pass --output docs/plans/review-passes/design.md --role Design ...</input>
<input>Review-result compatibility: scripts/team_state.py review-result output should still be recognized.</input>
</inputs>

<expected_output>
<section>primary workflow or comprehension pressure</section>
<section>interaction risks and experience tradeoffs</section>
<section>discovery-side challenge pass or review-pass with recommendation for role Design</section>
</expected_output>

<packaging>
<target>.agents/skills/design-review/SKILL.md</target>
<target>Runtime installer records this skill under `.agents/skills` during onboarding.</target>
</packaging>

<writeback>
<target>docs/project/PROJECT_BRIEF.md</target>
<target>docs/plans/review-passes/design.md</target>
<target>Use scripts/team_state.py review-pass to write structured role output.</target>
</writeback>

<compatibility>
Direct `review-result` writeback stays supported for recovery paths.
<target>docs/plans/review-results/design.md</target>
<target>Use scripts/team_state.py review-result to write structured role output when needed.</target>
</compatibility>

<office_hours>
Use this role to challenge an office-hours brief before plan. In office-hours mode, pressure-test primary flows, comprehension, and interaction cost instead of proposing implementation details.
</office_hours>

<non_goals>
<item>Do not implement UI code or visual polish directly.</item>
<item>Do not address the user directly.</item>
<item>Do not drift into architecture or builder ownership.</item>
</non_goals>

<reporting>
Report only to the lead. Do not address the user directly.
</reporting>
