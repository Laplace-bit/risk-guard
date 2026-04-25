#!/usr/bin/env python3
"""Rule-based risk engine for risk-guard.

Analyzes structured case inputs and produces a risk score, level,
triggered compound rules, and itemized scoring breakdown.

Usage:
    python scripts/risk_engine.py --input case.json
    python scripts/risk_engine.py --input case.json --verbose
    echo '{"vulnerability_tags":["pregnancy"]}' | python scripts/risk_engine.py --stdin
    python scripts/risk_engine.py --input case.json --format markdown
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

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
    # anticipatory / coupling dimensions (v2.0)
    "one_way_door": 5,
    "no_rollback": 4,
    "tight_coupling": 4,
    "single_point_of_failure": 5,
    "zero_time_slack": 3,
    "zero_resource_slack": 3,
    "unvalidated_assumption": 3,
    "cross_system_dependency": 3,
    # cognitive bias dimensions (v2.0)
    "overconfidence": 3,
    "planning_fallacy": 3,
    "normalization_of_deviance": 4,
    "survivorship_bias": 2,
    "anchoring": 2,
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
    # anticipatory safeguards (v2.0)
    "rollback_tested": -3,
    "feature_flags": -2,
    "gradual_rollout": -2,
    "monitoring_configured": -2,
    "assumption_validated": -2,
    "buffer_time": -2,
    "buffer_resources": -2,
    "second_opinion_obtained": -2,
    "checklist_completed": -2,
    "belief_update_signals": -1,
}

# Scenario base weights: each scenario classification adds a small baseline risk
SCENARIO_WEIGHTS: Dict[str, int] = {
    "travel_and_mobility": 1,
    "workplace_or_site_visit": 1,
    "health_sensitive_activity": 2,
    "stranger_interaction_or_relationship_meeting": 2,
    "housing_or_property_viewing": 1,
    "transaction_payment_or_asset_transfer": 2,
    "caregiving_or_dependent_protection": 1,
    "outdoor_or_environmental_exposure": 1,
    "nightlife_or_isolated_time_movement": 2,
    "online_to_offline_conversion": 2,
    "business_trip_or_multi_day_travel": 1,
    "digital_fraud_scam_or_phishing_risk": 2,
}

# ──────────────────────────────────────────────────────────────
# Compound rules: when risk factors combine, extra danger
# Format: (primary_set, secondary_set, bonus_score, description)
# If secondary_set == {"confirmed_ppe"}, it's an "absence" rule:
#   triggered when primary is present but confirmed_ppe is NOT present.
# ──────────────────────────────────────────────────────────────

COMPOUND_RULES: List[Tuple[Set[str], Set[str], int, str]] = [
    # Original safety rules
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
    # Anticipatory / coupling rules (v2.0)
    ({"one_way_door", "no_rollback"}, {"unvalidated_assumption", "tight_coupling"}, 8,
     "irreversible action with unvalidated assumptions and tight coupling"),
    ({"tight_coupling", "single_point_of_failure"}, {"zero_time_slack", "urgency"}, 7,
     "tight coupling with single failure point under time pressure"),
    ({"one_way_door"}, {"overconfidence", "planning_fallacy"}, 6,
     "irreversible action combined with cognitive overconfidence"),
    ({"cross_system_dependency"}, {"no_rollback", "tight_coupling"}, 6,
     "cross-system dependency with no rollback in tightly coupled system"),
    ({"normalization_of_deviance"}, {"tight_coupling", "isolation"}, 5,
     "normalized deviance in tightly coupled or isolated situation"),
    ({"planning_fallacy"}, {"zero_time_slack", "zero_resource_slack"}, 5,
     "planning fallacy with zero slack — schedule will definitely slip"),
    ({"overconfidence"}, {"unvalidated_assumption", "single_point_of_failure"}, 5,
     "overconfidence hiding unvalidated assumptions at a single failure point"),
]

# ──────────────────────────────────────────────────────────────
# Level thresholds
# ──────────────────────────────────────────────────────────────

LEVELS: List[Tuple[int, int, str]] = [
    (0, 5, "green"),
    (6, 11, "yellow"),
    (12, 18, "orange"),
    (19, 999, "red"),
]

LEVEL_LABELS: Dict[str, str] = {
    "green": "✅ Low risk. Proceed with normal precautions.",
    "yellow": "⚠️ Moderate risk. Proceed with added safeguards.",
    "orange": "🟠 Significant risk. Do not proceed without mitigations.",
    "red": "🔴 High risk. Do not proceed as described.",
}


def normalize_case(data: Dict) -> Tuple[Set[str], List[str]]:
    """Extract and normalize all tags from a case JSON.

    Returns (tags, warnings) where warnings list unknown tags
    and notes about ignored fields.
    """
    tags: Set[str] = set()
    warnings: List[str] = []

    for key in [
        "scenario_tags",
        "vulnerability_tags",
        "exposure_tags",
        "counterparty_tags",
        "safeguard_tags",
        "constraint_tags",
        "transport_tags",
        "anticipatory_tags",
        "cognitive_bias_tags",
        "anticipatory_safeguard_tags",
    ]:
        values = data.get(key, []) or []
        if not isinstance(values, list):
            raise ValueError(f"{key} must be a list, got {type(values).__name__}")
        for v in values:
            tag = str(v).strip()
            if tag:
                if tag not in WEIGHTS and tag not in SCENARIO_WEIGHTS:
                    warnings.append(f"Unknown tag '{tag}' in {key} — will be ignored in scoring")
                tags.add(tag)

    # Warn about free_text being ignored
    free_text = data.get("free_text", "")
    if free_text and str(free_text).strip():
        warnings.append("free_text is accepted but not used in scoring — for human reference only")

    return tags, warnings


def evaluate(tags: Set[str]) -> Dict:
    """Score tags and determine risk level."""
    score = 0
    reasons: List[str] = []
    triggered_rules: List[str] = []
    rule_details: List[Dict] = []

    # Individual tag scoring (including scenario base weights)
    for tag in sorted(tags):
        weight = WEIGHTS.get(tag, 0)
        scenario_weight = SCENARIO_WEIGHTS.get(tag, 0)
        total = weight + scenario_weight
        if total != 0:
            score += total
            if weight > 0:
                reasons.append(f"{tag} (+{weight})")
            elif scenario_weight > 0:
                reasons.append(f"{tag} (scenario: +{scenario_weight})")
            elif weight < 0:
                reasons.append(f"{tag} ({weight})")

    # Compound rule scoring
    for primary, secondary, bonus, note in COMPOUND_RULES:
        primary_matched = tags.intersection(primary)
        if primary_matched:
            if secondary == {"confirmed_ppe"}:
                # Absence rule: primary present but safeguard absent
                if "confirmed_ppe" not in tags:
                    score += bonus
                    triggered_rules.append(f"{note} (+{bonus})")
                    rule_details.append({
                        "rule": note,
                        "bonus": bonus,
                        "primary_matched": sorted(primary_matched),
                        "type": "absence",
                        "absent_tag": "confirmed_ppe",
                    })
            else:
                secondary_matched = tags.intersection(secondary)
                if secondary_matched:
                    score += bonus
                    triggered_rules.append(f"{note} (+{bonus})")
                    rule_details.append({
                        "rule": note,
                        "bonus": bonus,
                        "primary_matched": sorted(primary_matched),
                        "secondary_matched": sorted(secondary_matched),
                        "type": "presence",
                    })

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
        "rule_details": rule_details,
    }


def format_markdown(result: Dict) -> str:
    """Format result as markdown."""
    lines = [
        f"## Risk Assessment: {result['level'].upper()}",
        f"**Score:** {result['score']} — {result['level_label']}",
        "",
    ]
    if result["reasons"]:
        lines.append("### Factor Breakdown")
        for r in result["reasons"]:
            lines.append(f"- {r}")
        lines.append("")
    if result["triggered_rules"]:
        lines.append("### Compound Rules Triggered")
        for r in result["triggered_rules"]:
            lines.append(f"- {r}")
        lines.append("")
    return "\n".join(lines)


def format_plain(result: Dict) -> str:
    """Format result as plain text."""
    lines = [
        f"Level: {result['level'].upper()}",
        f"Score: {result['score']} — {result['level_label']}",
    ]
    if result["reasons"]:
        lines.append("Factors:")
        for r in result["reasons"]:
            lines.append(f"  {r}")
    if result["triggered_rules"]:
        lines.append("Compound rules:")
        for r in result["triggered_rules"]:
            lines.append(f"  {r}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Risk Guard Engine")
    parser.add_argument("--input", help="Path to case JSON file")
    parser.add_argument("--stdin", action="store_true", help="Read case JSON from stdin")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed breakdown")
    parser.add_argument("--format", choices=["json", "markdown", "plain"], default="json",
                        help="Output format (default: json)")
    args = parser.parse_args()

    if not args.input and not args.stdin:
        parser.error("Either --input or --stdin is required")

    if args.stdin:
        raw = sys.stdin.read()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON from stdin: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        path = Path(args.input)
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {path}: {e}", file=sys.stderr)
            sys.exit(1)

    tags, warnings = normalize_case(data)
    result = evaluate(tags)

    # Add warnings to result
    if warnings:
        result["warnings"] = warnings

    # Output in requested format
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(format_markdown(result))
    else:
        print(format_plain(result))

    if args.verbose:
        print(f"\n--- Detailed Breakdown ---")
        print(f"Tags: {', '.join(sorted(tags)) or '(none)'}")
        print(f"Score: {result['score']}")
        print(f"Level: {result['level']} — {result['level_label']}")
        if result["triggered_rules"]:
            print(f"\nCompound rules triggered:")
            for rule in result["triggered_rules"]:
                print(f"  • {rule}")
        if warnings:
            print(f"\nWarnings:")
            for w in warnings:
                print(f"  ⚠ {w}")


if __name__ == "__main__":
    main()