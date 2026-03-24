from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_initial_module_contract_and_decision_exist() -> None:
    contract = (ROOT / "docs" / "status" / "MODULE_CONTRACTS" / "team-lead.md").read_text()
    assert "# Module Contract: team-lead" in contract
    assert "## Inputs" in contract
    assert "## Outputs" in contract

    decision = (ROOT / "docs" / "decisions" / "2026-03-24-single-entry-lead.md").read_text()
    assert "# Decision: Single Entry Lead" in decision
    assert "## Context" in decision
    assert "## Decision" in decision
