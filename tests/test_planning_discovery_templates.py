from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_autoplan_template_exists_with_outcome_placeholders() -> None:
    template = ROOT / "planning" / "discovery" / "templates" / "autoplan-report.md"
    assert template.exists()

    content = template.read_text()
    assert "# Autoplan Report: <title>" in content
    assert "<discovery_brief_path>" in content
    assert "<plan_brief_path>" in content
    assert "<review_pass_paths>" in content
    assert "<review_gate_path>" in content
    assert "<outcome>" in content
    assert "<auto_decisions>" in content
    assert "<taste_decisions>" in content
    assert "<next_action>" in content


def test_office_hours_template_exists_with_outcome_placeholders() -> None:
    template = ROOT / "planning" / "discovery" / "templates" / "office-hours-report.md"
    assert template.exists()

    content = template.read_text()
    assert "# Office-Hours Report: <title>" in content
    assert "<mode>" in content
    assert "<outcome>" in content
    assert "<office_hours_brief_path>" in content
    assert "<challenge_pass_paths>" in content
    assert "<discovery_gate_path>" in content
    assert "<reframing_changes>" in content
    assert "<next_action>" in content
