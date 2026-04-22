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
    result = run_engine({
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": [],
    })
    # Add transport tags
    case_with_transport = {
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": ["fatigue"],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["no_fallback_transport"],
        "transport_tags": ["driver_fatigue", "bad_weather_route"],
    }
    # Manually add transport tags to exposure for the engine
    case_combined = {
        "scenario_tags": ["travel_and_mobility"],
        "vulnerability_tags": ["fatigue"],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["no_fallback_transport", "driver_fatigue", "bad_weather_route"],
    }
    result = run_engine(case_combined)
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']}"
    assert any("fatigued driver" in r.lower() or "adverse road" in r.lower() for r in result["triggered_rules"]), \
        f"Expected driver fatigue compound rule, got: {result['triggered_rules']}"


def test_digital_fraud_unsolicited_credential():
    """unsolicited_contact + credential_request without verified_organization should be high risk."""
    result = run_engine({
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["unsolicited_contact", "credential_request"],
        "safeguard_tags": [],
        "constraint_tags": [],
    })
    # unsolicited_contact(4) + credential_request(5) + non_reversible_payment(6) = 15
    # plus compound rule (+8) = 23 → red
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
    """unsolicited_contact + threat_or_ultimatum without verified_organization should be high risk."""
    result = run_engine({
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["unsolicited_contact", "threat_or_ultimatum", "suspicious_payment_method"],
        "safeguard_tags": [],
        "constraint_tags": [],
    })
    # unsolicited_contact(4) + threat_or_ultimatum(5) + non_reversible_payment(6) + suspicious_payment_method(4) = 19
    # plus compound rules: unsolicited_contact+suspicious_payment_method(+8), threat_or_ultimatum+suspicious_payment_method(+7) = 34 → red
    assert result["level"] == "red", f"Expected red, got {result['level']} (score {result['score']})"
    assert len(result["triggered_rules"]) >= 2, \
        f"Expected at least 2 compound rules, got: {result['triggered_rules']}"
    # Verify that adding verified_organization reduces the score
    result_with_org = run_engine({
        "scenario_tags": ["transaction_payment_or_asset_transfer"],
        "vulnerability_tags": [],
        "exposure_tags": ["non_reversible_payment"],
        "counterparty_tags": ["unsolicited_contact", "threat_or_ultimatum", "suspicious_payment_method"],
        "safeguard_tags": ["verified_organization"],
        "constraint_tags": [],
    })
    assert result_with_org["score"] < result["score"], \
        f"verified_organization should reduce score: {result_with_org['score']} >= {result['score']}"


def test_business_trip_with_transport():
    """Business trip with transport tags should trigger driver fatigue compound."""
    result = run_engine({
        "scenario_tags": ["travel_and_mobility", "workplace_or_site_visit"],
        "vulnerability_tags": [],
        "exposure_tags": [],
        "counterparty_tags": [],
        "safeguard_tags": [],
        "constraint_tags": ["driver_fatigue", "bad_weather_route", "no_fallback_transport"],
    })
    # driver_fatigue(4) + bad_weather_route(3) + no_fallback_transport(3) = 10
    # compound: driver_fatigue + bad_weather_route (+5) = 15 → orange
    assert result["level"] in ("orange", "red"), f"Expected orange/red, got {result['level']} (score {result['score']})"
    assert any("fatigued driver" in r.lower() or "adverse road" in r.lower() for r in result["triggered_rules"]), \
        f"Expected driver fatigue compound rule, got: {result['triggered_rules']}"


if __name__ == "__main__":
    tests = [test_green_low_risk, test_red_high_risk, test_orange_compound_risk,
             test_safeguards_reduce_score, test_yellow_moderate_risk, test_empty_case,
             test_driver_fatigue_compound, test_digital_fraud_unsolicited_credential,
             test_digital_fraud_unsolicited_threat, test_business_trip_with_transport]
    for t in tests:
        t()
        print(f"✓ {t.__name__}")
    print(f"\nAll {len(tests)} tests passed!")