#!/usr/bin/env python3
"""Rule-based risk engine for risk-guard.

Analyzes structured case inputs and produces a risk score, level,
triggered compound rules, and itemized scoring breakdown.

Usage:
    python scripts/risk_engine.py --input case.json
    python scripts/risk_engine.py --input case.json --verbose
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set

# ──────────────────────────────────────────────────────────────
# Weights: positive = risk factor, negative = safeguard
# ──────────────────────────────────────────────────────────────

WEIGHTS: Dict[str, int] = {
    # vulnerabilities
    "possible_pregnancy": 5,
    "pregnancy": 6,
    "post_op": 5,
    "chronic_illness": 3,
    "elder": 3,
    "child": 4,
    "fatigue": 2,
    "mobility_limit": 3,
    # exposures
    "chemical": 6,
    "infectious": 4,
    "heat": 3,
    "cold": 2,
    "radiation": 6,
    "dust": 3,
    "noise": 2,
    "long_walking": 3,
    "lifting": 3,
    "night_travel": 3,
    "isolation": 4,
    "alcohol": 2,
    "non_reversible_payment": 6,
    "document_handover": 4,
    # counterparty
    "unverified_stranger": 4,
    "pressure": 4,
    "urgency": 4,
    "secrecy": 5,
    "identity_mismatch": 5,
    # constraints
    "cannot_exit_freely": 7,
    "poor_medical_access": 4,
    "no_fallback_transport": 3,
    "dead_phone_risk": 2,
    "dependent_involved": 5,
    # transport
    "driver_fatigue": 4,
    "poor_vehicle_condition": 4,
    "bad_weather_route": 3,
    "unfamiliar_route": 2,
    # digital fraud
    "unsolicited_contact": 4,
    "credential_request": 5,
    "threat_or_ultimatum": 5,
    "suspicious_payment_method": 4,
    # safeguards (negative)
    "public_place": -2,
    "trusted_companion": -3,
    "verified_identity": -3,
    "reversible_payment": -3,
    "confirmed_ppe": -3,
    "can_exit_independently": -3,
    "live_location_shared": -1,
    "medical_support_nearby": -2,
    "checked_weather": -2,
    "travel_insurance": -2,
    "verified_organization": -3,
}

# ──────────────────────────────────────────────────────────────
# Compound rules: when risk factors combine, extra danger
# Format: (primary_set, secondary_set, bonus_score, description)
# If secondary_set == {" confirmed_ppe"}, it's an "absence" rule:
#   triggered when primary is present but confirmed_ppe is NOT present.
# ──────────────────────────────────────────────────────────────

COMPOUND_RULES = [
    ({"pregnancy", "possible_pregnancy"}, {"chemical", "heat", "long_walking", "infectious", "radiation"}, 8,
     "pregnancy-sensitive vulnerability combined with hazardous exposure"),
    ({"night_travel", "isolation"}, {"unverified_stranger", "dead_phone_risk", "no_fallback_transport"}, 6,
     "isolation combined with weak support or counterpart uncertainty"),
    ({"non_reversible_payment"}, {"urgency", "pressure", "identity_mismatch", "secrecy"}, 8,
     "irreversible payment combined with scam pressure signals"),
    ({"dependent_involved"}, {"poor_medical_access", "no_fallback_transport", "cannot_exit_freely"}, 6,
     "dependent safety relies on weak recovery options"),
    ({"chemical", "dust", "radiation", "heat"}, {"confirmed_ppe"}, 4,
     "hazardous site conditions with unconfirmed controls"),
    ({"driver_fatigue"}, {"bad_weather_route", "unfamiliar_route"}, 5,
     "fatigued driver combined with adverse road conditions"),
    ({"driver_fatigue", "poor_vehicle_condition"}, {"night_travel", "bad_weather_route"}, 6,
     "vehicle or driver issues compounded by difficult travel conditions"),
    ({"unsolicited_contact"}, {"credential_request", "non_reversible_payment", "suspicious_payment_method"}, 8,
     "unsolicited contact requesting credentials or irreversible payment — classic scam pattern"),
    ({"threat_or_ultimatum"}, {"urgency", "suspicious_payment_method"}, 7,
     "threats or ultimatums combined with pressure to pay — high fraud risk"),
]

# ──────────────────────────────────────────────────────────────
# Level thresholds
# ──────────────────────────────────────────────────────────────

LEVELS = [
    (0, 5, "green"),
    (6, 11, "yellow"),
    (12, 18, "orange"),
    (19, 999, "red"),
]

LEVEL_LABELS = {
    "green": "✅ Low risk. Proceed with normal precautions.",
    "yellow": "⚠️ Moderate risk. Proceed with added safeguards.",
    "orange": "🟠 Significant risk. Do not proceed without mitigations.",
    "red": "🔴 High risk. Do not proceed as described.",
}


def normalize_case(data: Dict) -> Set[str]:
    """Extract and normalize all tags from a case JSON."""
    tags: Set[str] = set()
    for key in [
        "scenario_tags",
        "vulnerability_tags",
        "exposure_tags",
        "counterparty_tags",
        "safeguard_tags",
        "constraint_tags",
        "transport_tags",
    ]:
        values = data.get(key, []) or []
        if not isinstance(values, list):
            raise ValueError(f"{key} must be a list, got {type(values).__name__}")
        tags.update(str(v).strip() for v in values if str(v).strip())
    return tags


def evaluate(tags: Set[str]) -> Dict:
    """Score tags and determine risk level."""
    score = 0
    reasons: List[str] = []
    triggered_rules: List[str] = []

    # Individual tag scoring
    for tag in sorted(tags):
        weight = WEIGHTS.get(tag, 0)
        score += weight
        if weight > 0:
            reasons.append(f"{tag} (+{weight})")
        elif weight < 0:
            reasons.append(f"{tag} ({weight})")

    # Compound rule scoring
    for primary, secondary, bonus, note in COMPOUND_RULES:
        if tags.intersection(primary):
            if secondary == {"confirmed_ppe"}:
                # Absence rule: primary present but safeguard absent
                if "confirmed_ppe" not in tags:
                    score += bonus
                    triggered_rules.append(f"{note} (+{bonus})")
            elif tags.intersection(secondary):
                score += bonus
                triggered_rules.append(f"{note} (+{bonus})")

    # Determine level
    level = "green"
    for low, high, name in LEVELS:
        if low <= score <= high:
            level = name
            break

    return {
        "score": score,
        "level": level,
        "level_label": LEVEL_LABELS.get(level, ""),
        "reasons": reasons,
        "triggered_rules": triggered_rules,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Risk Guard Engine")
    parser.add_argument("--input", required=True, help="Path to case JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed breakdown")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)

    tags = normalize_case(data)
    result = evaluate(tags)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.verbose:
        print(f"\n--- Detailed Breakdown ---")
        print(f"Tags: {', '.join(sorted(tags)) or '(none)'}")
        print(f"Score: {result['score']}")
        print(f"Level: {result['level']} — {result['level_label']}")
        if result["triggered_rules"]:
            print(f"\nCompound rules triggered:")
            for rule in result["triggered_rules"]:
                print(f"  • {rule}")


if __name__ == "__main__":
    main()