---
name: product-discovery
description: Use when the lead needs product framing, scope tradeoffs, and a Product review-pass artifact for review gating; continue to mention review-result for compatibility.
---

# Product Discovery

<mission>
Clarify product intent into scoped goals, milestones, tradeoffs, and discovery questions.
</mission>

<inputs>
<input>User intent and constraints from the lead.</input>
<input>Canonical state files and relevant decisions.</input>
<input>Writeback command shape: uv run python scripts/team_state.py review-pass --output docs/plans/review-passes/product.md --role Product ...</input>
<input>Review-result compatibility: scripts/team_state.py review-result output should still be recognized.</input>
</inputs>

<expected_output>
<section>problem framing</section>
<section>scope options with recommendation</section>
<section>open questions and assumptions</section>
<section>review-pass with recommendation for role Product</section>
</expected_output>

<packaging>
<target>.agents/skills/product-discovery/SKILL.md</target>
<target>Install runtime pack output into `.agents/skills/product-discovery` as part of onboarding.</target>
</packaging>

<writeback>
<target>docs/project/PROJECT_BRIEF.md</target>
<target>docs/project/ROADMAP.md</target>
<target>docs/plans/review-passes/product.md</target>
<target>Use scripts/team_state.py review-pass to write structured role output.</target>
</writeback>

<compatibility>
Direct `review-result` writeback remains supported for compatibility and recovery.
<target>docs/plans/review-results/product.md</target>
<target>Use scripts/team_state.py review-result to write structured role output when necessary.</target>
</compatibility>

<non_goals>
<item>Do not implement code changes.</item>
<item>Do not invent product scope without evidence.</item>
</non_goals>

<reporting>
Report only to the lead. Do not address the user directly.
</reporting>
