from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_team_lead_skill_references_single_entry_and_canonical_state() -> None:
    content = (ROOT / "skills" / "team-lead" / "SKILL.md").read_text()
    assert "single visible lead" in content.lower()
    assert "docs/project/PROJECT_BRIEF.md" in content
    assert "approval-needed" in content
    assert "subagent" in content.lower()


def test_team_lead_openai_metadata_exists() -> None:
    content = (ROOT / "skills" / "team-lead" / "agents" / "openai.yaml").read_text()
    assert "display_name:" in content
    assert "description:" in content
