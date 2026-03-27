---
name: team-runtime-bootstrap
description: Use when Codex needs to install the Codex AI Team runtime into the current repository so `team-lead` and the internal repo-local roles become available.
---

# Team Runtime Bootstrap

Install the Codex AI Team runtime into the target repository.

## When To Use

- The current repository does not yet have the team runtime installed.
- The user wants the full `Lead -> Ops -> Specialists` runtime, not just a standalone skill.
- A target repo needs `.agents/skills`, `.codex`, runtime scripts, and canonical docs bootstrapped together.

## Steps

1. Confirm the target repository root.
2. Run the bootstrap script:

```bash
python3 ../../scripts/bootstrap_repo.py --target <repo-root>
```

3. Tell the user what was installed:
   - `.agents/skills/`
   - `.codex/`
   - `scripts/`
   - `ops/`
   - canonical docs under `docs/project/` and `docs/status/`
4. Tell the user to restart Codex in the target repo if the new repo-local skills do not appear immediately.
5. After installation, use the repo-local `team-lead` skill as the single visible entrypoint.

## Notes

- Do not move the installed skills into `.codex/`; Codex discovers repo-local skills from `.agents/skills/`.
- The bootstrap path is a packaging layer. The installed repo runtime remains the canonical execution surface.
