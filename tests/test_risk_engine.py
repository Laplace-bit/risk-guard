#!/usr/bin/env python3
"""Risk Guard test suite."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "risk_engine.py"


def run_engine(case: dict) -> dict:
    """Run the risk engine on a case dict and return parsed result."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(case, f)
        f.flush()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", f.name],
            capture_output=True, text=True
        )
    Path(f.name).unlink(missing_ok=True)
    assert result.returncode == 0, f"Engine failed: {result.stderr}"
    return json.loads(result.stdout)


def test_green_low_risk():
    """Routine activity with safeguards should be green."""
    result = run_engine({
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": ["public_place", "trusted_companion", "can_exit_independently"],
        "constraint_tags": [],
    })
    assert result["level"] == "green", f"Expected green, got {result['level']} (score {result['score']})"
    assert result["score"] <= 5, f"Green score too high: {result['score']}"


def test_red_high_risk():
    """Pregnancy + chemical + no exit should be red."""
    result = run_engine({
        "scenario_tags": ["workplace_or_site_visit", "health_sensitive_activity"],
        "vulnerability_tags": ["pregnancy"],
        "exposure_tags": ["chemical", "heat", "long_walking"],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["cannot_exit_freely", "poor_medical_access"],
    })
    assert result["level"] == "red", f"Expected red, got {result['level']} (score {result['score']})"
    assert len(result["triggered_rules"]) > 0, "Expected compound rule to trigger"


def test_orange_compound_risk():
    """Urgent payment + identity mismatch should be orange or red."""
    result = run_engine({
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["urgency", "identity_mismatch", "secrecy"],
        "safeguard_tags": [],
        "constraint_tags": [],
    })
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']}"


def test_safeguards_reduce_score():
    """Safeguards should lower the score."""
    base = {
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": [],
        "exposure_tags": ["night_travel", "isolation"],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
    }
    with_safeguards = {
        **base,
        "safeguard_tags": ["trusted_companion", "can_exit_independently", "live_location_shared"],
    }
    score_base = run_engine(base)["score"]
    score_safe = run_engine(with_safeguards)["score"]
    assert score_safe < score_base, f"Safeguards should reduce score: {score_safe} >= {score_base}"


def test_yellow_moderate_risk():
    """Typical moderate travel risk should be yellow."""
    result = run_engine({
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": ["fatigue"],
        "exposure_tags": ["night_travel"],
        "counterparty_tags": [],
        "safeguard_tags": ["can_exit_independently"],
        "constraint_tags": [],
    })
    assert result["level"] in ("yellow", "green"), f"Expected yellow/green, got {result['level']}"


def test_empty_case():
    """Empty case should score 0 (green)."""
    result = run_engine({
        "scenario_tags": [],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
    })
    assert result["score"] == 0
    assert result["level"] == "green"


def test_driver_fatigue_compound():
    """Driver fatigue + bad weather should trigger compound rule."""
    case_combined = {
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": ["fatigue"],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["no_fallback_transport"],
        "transport_tags": ["driver_fatigue", "bad_weather_route"],
    }
    result = run_engine(case_combined)
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']}"
    assert any("fatigued driver" in r.lower() or "adverse road" in r.lower() for r in result["triggered_rules"]), \
        f"Expected driver fatigue compound rule, got: {result['triggered_rules']}"


def test_digital_fraud_unsolicited_credential():
    """unsolicited_contact + credential_request should be high risk."""
    result = run_engine({
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["unsolicited_contact", "credential_request"],
        "safeguard_tags": [],
        "constraint_tags": [],
    })
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']} (score {result['score']})"
    assert any("unsolicited contact" in r.lower() and "credential" in r.lower() for r in result["triggered_rules"]), \
        f"Expected unsolicited contact + credential compound rule, got: {result['triggered_rules']}"
    # Verify that adding verified_organization reduces the score
    result_with_org = run_engine({
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["unsolicited_contact", "credential_request"],
        "safeguard_tags": ["verified_organization"],
        "constraint_tags": [],
    })
    assert result_with_org["score"] < result["score"], \
        f"verified_organization should reduce score: {result_with_org['score']} >= {result['score']}"


def test_digital_fraud_unsolicited_threat():
    """unsolicited_contact + threat_or_ultimatum should be red."""
    result = run_engine({
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["unsolicited_contact", "threat_or_ultimatum", "suspicious_payment_method"],
        "safeguard_tags": [],
        "constraint_tags": [],
    })
    assert result["level"] == "red", f"Expected red, got {result['level']} (score {result['score']})"
    assert len(result["triggered_rules"]) >= 2, \
        f"Expected at least 2 compound rules, got: {result['triggered_rules']}"


def test_business_trip_with_transport():
    """Business trip with transport tags should trigger driver fatigue compound."""
    result = run_engine({
        "scenario_tags": ["travel_and_mobility", "workplace_or_site_visit"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["no_fallback_transport"],
        "transport_tags": ["driver_fatigue", "bad_weather_route"],
    })
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']} (score {result['score']})"


# ── v2.0 Anticipatory dimension tests ──


def test_one_way_door_compound():
    """One-way door + unvalidated assumption + tight coupling should trigger new compound rule."""
    result = run_engine({
        "scenario_tags": ["technical_deployment_or_system_change"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
        "anticipatory_tags": ["one_way_door", "no_rollback", "unvalidated_assumption", "tight_coupling"],
    })
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']} (score {result['score']})"
    assert any("irreversible" in r.lower() or "unvalidated" in r.lower() for r in result["triggered_rules"]), \
        f"Expected irreversible+unvalidated compound rule, got: {result['triggered_rules']}"


def test_tight_coupling_spof_urgency():
    """Tight coupling + single point of failure + urgency should trigger compound."""
    result = run_engine({
        "scenario_tags": ["technical_deployment_or_system_change"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": ["urgency"],
        "safeguard_tags": [],
        "constraint_tags": [],
        "anticipatory_tags": ["tight_coupling", "single_point_of_failure", "zero_time_slack"],
    })
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']} (score {result['score']})"
    assert any("tight coupling" in r.lower() or "single failure" in r.lower() for r in result["triggered_rules"]), \
        f"Expected tight coupling compound rule, got: {result['triggered_rules']}"


def test_overconfidence_one_way_door():
    """Overconfidence + one-way door should trigger cognitive bias compound."""
    result = run_engine({
        "scenario_tags": ["project_decision_or_plan_execution"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
        "anticipatory_tags": ["one_way_door"],
        "cognitive_bias_tags": ["overconfidence"],
    })
    assert result["score"] > 0, "Expected non-zero score for overconfidence + one-way door"
    assert any("overconfidence" in r.lower() or "cognitive" in r.lower() or "irreversible" in r.lower()
               for r in result["triggered_rules"]), \
        f"Expected overconfidence compound rule, got: {result['triggered_rules']}"


def test_anticipatory_safeguards_reduce_score():
    """Anticipatory safeguards should reduce the score."""
    base = {
        "scenario_tags": ["technical_deployment_or_system_change"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
        "anticipatory_tags": ["one_way_door", "tight_coupling"],
    }
    with_safeguards = {
        **base,
        "anticipatory_safeguard_tags": ["rollback_tested", "buffer_time", "second_opinion_obtained"],
    }
    score_base = run_engine(base)["score"]
    score_safe = run_engine(with_safeguards)["score"]
    assert score_safe < score_base, f"Anticipatory safeguards should reduce score: {score_safe} >= {score_base}"


def test_planning_fallacy_zero_slack():
    """Planning fallacy + zero slack should trigger compound rule."""
    result = run_engine({
        "scenario_tags": ["project_decision_or_plan_execution"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
        "cognitive_bias_tags": ["planning_fallacy"],
        "anticipatory_tags": ["zero_time_slack", "zero_resource_slack"],
    })
    assert result["level"] in ("yellow", "orange", "red"), f"Expected yellow+, got {result['level']} (score {result['score']})"
    assert any("planning fallacy" in r.lower() or "slack" in r.lower() for r in result["triggered_rules"]), \
        f"Expected planning fallacy compound, got: {result['triggered_rules']}"


def test_checklist_safeguard():
    """Checklist completion should reduce risk score."""
    base = {
        "scenario_tags": ["technical_deployment_or_system_change"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
        "anticipatory_tags": ["tight_coupling", "single_point_of_failure"],
    }
    with_checklist = {
        **base,
        "anticipatory_safeguard_tags": ["checklist_completed", "assumption_validated", "monitoring_configured"],
    }
    score_base = run_engine(base)["score"]
    score_safe = run_engine(with_checklist)["score"]
    assert score_safe < score_base, f"Checklist should reduce score: {score_safe} >= {score_base}"


def test_travel_safeguards_reduce_score():
    """checked_weather + travel_insurance should reduce risk score."""
    base = {
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": ["fatigue"],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
        "transport_tags": ["driver_fatigue", "bad_weather_route"],
    }
    with_safeguards = {
        **base,
        "safeguard_tags": ["checked_weather", "travel_insurance"],
    }
    score_base = run_engine(base)["score"]
    score_safe = run_engine(with_safeguards)["score"]
    assert score_safe < score_base, f"Travel safeguards should reduce score: {score_safe} >= {score_base}"


def test_verified_identity_reversible_payment():
    """verified_identity + reversible_payment should reduce fraud scenario score."""
    base = {
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["unsolicited_contact", "credential_request"],
        "safeguard_tags": [],
        "constraint_tags": [],
    }
    with_safeguards = {
        **base,
        "safeguard_tags": ["verified_identity", "reversible_payment", "verified_organization"],
    }
    score_base = run_engine(base)["score"]
    score_safe = run_engine(with_safeguards)["score"]
    assert score_safe < score_base, f"Identity/payment safeguards should reduce score: {score_safe} >= {score_base}"


def test_ppe_and_medical_safeguard():
    """confirmed_ppe + medical_support_nearby should reduce hazard scenario score."""
    base = {
        "scenario_tags": ["workplace_or_site_visit"],
        "vulnerability_tags": [],
        "exposure_tags": ["chemical", "dust", "heat"],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["poor_medical_access"],
    }
    with_safeguards = {
        **base,
        "safeguard_tags": ["confirmed_ppe", "medical_support_nearby"],
    }
    score_base = run_engine(base)["score"]
    score_safe = run_engine(with_safeguards)["score"]
    assert score_safe < score_base, f"PPE/medical safeguards should reduce score: {score_safe} >= {score_base}"


def test_deployment_safeguards_reduce_risk():
    """feature_flags + gradual_rollout should reduce deployment risk."""
    base = {
        "scenario_tags": ["technical_deployment_or_system_change"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
        "anticipatory_tags": ["tight_coupling", "single_point_of_failure"],
    }
    with_safeguards = {
        **base,
        "safeguard_tags": ["feature_flags", "gradual_rollout"],
        "anticipatory_safeguard_tags": ["rollback_tested", "buffer_time", "monitoring_configured"],
    }
    score_base = run_engine(base)["score"]
    score_safe = run_engine(with_safeguards)["score"]
    assert score_safe < score_base, f"Deployment safeguards should reduce score: {score_safe} >= {score_base}"


def test_safeguards_dramatically_reduce_score():
    """Multiple safeguards should dramatically reduce a severe case's score."""
    high_risk = {
        "scenario_tags": ["workplace_or_site_visit", "health_sensitive_activity"],
        "vulnerability_tags": ["pregnancy"],
        "exposure_tags": ["chemical", "heat", "long_walking"],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["cannot_exit_freely", "poor_medical_access"],
    }
    mitigated = {
        **high_risk,
        "safeguard_tags": [
            "confirmed_ppe", "medical_support_nearby", "can_exit_independently",
            "checked_weather", "trusted_companion",
        ],
    }
    score_high = run_engine(high_risk)["score"]
    score_mitigated = run_engine(mitigated)["score"]
    assert score_high > 18, f"High-risk case should be >18 (red), got {score_high}"
    # Safeguards should reduce score by at least 10 points
    reduction = score_high - score_mitigated
    assert reduction >= 10, f"Safeguards should reduce score by >=10, got {reduction}"


if __name__ == "__main__":
    tests = [test_green_low_risk, test_red_high_risk, test_orange_compound_risk,
             test_safeguards_reduce_score, test_yellow_moderate_risk, test_empty_case,
             test_driver_fatigue_compound, test_digital_fraud_unsolicited_credential,
             test_digital_fraud_unsolicited_threat, test_business_trip_with_transport,
             test_one_way_door_compound, test_tight_coupling_spof_urgency,
             test_overconfidence_one_way_door, test_anticipatory_safeguards_reduce_score,
             test_planning_fallacy_zero_slack, test_checklist_safeguard,
             test_travel_safeguards_reduce_score, test_verified_identity_reversible_payment,
             test_ppe_and_medical_safeguard, test_deployment_safeguards_reduce_risk,
             test_safeguards_dramatically_reduce_score]
    for t in tests:
        t()
        print(f"✓ {t.__name__}")
    print(f"\nAll {len(tests)} tests passed!")