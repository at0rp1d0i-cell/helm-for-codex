# Hybrid Distribution Implementation Plan

<execution_handoff>
  <required_skill>executing-plans</required_skill>
  <execution_mode>subagent-driven or separate-session</execution_mode>
  <goal>Add a Codex plugin distribution surface plus a self-contained runtime bootstrap path.</goal>
</execution_handoff>

**Goal:** Ship a reusable plugin + runtime-pack hybrid distribution for the Codex-native AI team.

**Architecture:** Keep `.agents/skills` as the runtime discovery surface, `.codex` as the configuration surface, and add a self-contained plugin that bootstraps the runtime pack into any target repository.

**Tech Stack:** Python, Markdown, Codex plugin manifests, repo-local marketplace metadata

---

### Task 1: Add plugin distribution metadata

**Files:**
- Create: `plugins/codex-ai-team/.codex-plugin/plugin.json`
- Create: `.agents/plugins/marketplace.json`
- Modify: `README.md`

**Steps:**
1. Scaffold the plugin directory and manifest.
2. Add a repo marketplace entry that points at `./plugins/codex-ai-team`.
3. Document the difference between plugin install and direct runtime-pack install.

### Task 2: Export a self-contained runtime pack into the plugin

**Files:**
- Create: `scripts/export_plugin_runtime.py`
- Create: `plugins/codex-ai-team/assets/runtime-pack/`
- Modify: `scripts/install_runtime_pack.py`
- Modify: `scripts/check_repo.py`

**Steps:**
1. Define the export surface for the runtime pack.
2. Write the export script so plugin assets are rebuilt from the canonical source repo layout.
3. Make repo checks assert that the plugin package exists and has the expected runtime-pack shape.

### Task 3: Add plugin bootstrap entrypoints

**Files:**
- Create: `plugins/codex-ai-team/skills/team-runtime-bootstrap/SKILL.md`
- Create: `plugins/codex-ai-team/scripts/bootstrap_repo.py`
- Modify: `README.md`

**Steps:**
1. Add a bootstrap skill that tells Codex how to install the team runtime into the current repo.
2. Add a bootstrap script that copies the bundled runtime pack into a target repo.
3. Document the plugin bootstrap flow for external users.

### Task 4: Add tests for the plugin path

**Files:**
- Create: `tests/test_plugin_distribution.py`
- Modify: `tests/test_repo_layout.py`
- Modify: `tests/test_install_runtime_pack.py`

**Steps:**
1. Verify the plugin manifest and marketplace entry exist.
2. Verify runtime-pack export artifacts exist where the plugin expects them.
3. Bootstrap a temp repo through the plugin script and assert the resulting runtime passes basic checks.

### Task 5: Verify and update canonical state

**Files:**
- Modify: `README.md`
- Modify: `docs/project/PROJECT_BRIEF.md`
- Modify: `docs/project/ROADMAP.md`
- Modify: `docs/status/EXECUTION_BOARD.md`

**Steps:**
1. Record the new plugin distribution layer in the project docs.
2. Run targeted tests plus repo checks.
3. Update the execution board to reflect the new distribution milestone.
