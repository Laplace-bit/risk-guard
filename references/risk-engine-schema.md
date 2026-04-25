# Risk Engine Schema

Use this schema when calling `python scripts/risk_engine.py --input case.json`.

```json
{
  "scenario_tags": ["workplace_or_site_visit", "health_sensitive_activity"],
  "vulnerability_tags": ["possible_pregnancy", "fatigue"],
  "exposure_tags": ["chemical", "long_walking", "heat"],
  "counterparty_tags": [],
  "safeguard_tags": ["can_exit_independently"],
  "constraint_tags": ["poor_medical_access"],
  "transport_tags": [],
  "anticipatory_tags": [],
  "cognitive_bias_tags": [],
  "anticipatory_safeguard_tags": [],
  "free_text": "optional case note"
}
```

## Notes
- Use short machine-friendly tags.
- Prefer explicit tags over long free-text.
- `free_text` is optional and only for human reference. It is accepted but not used in scoring.
- All tag fields default to `[]` when absent — the engine handles missing fields gracefully.
- The engine returns a score, level, triggered rules, rule details, and explanation snippets.
- Tags not in the weight dictionary produce a warning and are ignored in scoring.
- `scenario_tags` contribute a small base weight (+1 or +2) per scenario. This means the scenario classification itself carries a small risk signal.

## Absence Rules

Most compound rules trigger when **both** primary and secondary tags are present. One rule uses an **absence** pattern:

- **`confirmed_ppe` absence rule**: When hazardous conditions exist (`chemical`, `dust`, `radiation`, or `heat`) and `confirmed_ppe` is **not** present, the rule triggers. This is the only absence-style rule — all others are presence-based.

## Output Format

The engine outputs JSON with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `score` | int | Total risk score after all weights and compound rules |
| `level` | string | green / yellow / orange / red |
| `level_label` | string | Human-readable level description with emoji |
| `reasons` | string[] | Per-tag scoring breakdown (e.g., "chemical (+6)") |
| `triggered_rules` | string[] | Human-readable compound rule descriptions |
| `rule_details` | object[] | Structured rule data: rule name, bonus, matched tags, type (presence/absence) |
| `warnings` | string[] | Non-fatal issues: unknown tags, free_text note (only present if there are warnings) |

## CLI Options

```bash
# From file
python scripts/risk_engine.py --input case.json

# From stdin
echo '{"vulnerability_tags":["pregnancy"]}' | python scripts/risk_engine.py --stdin

# Verbose output
python scripts/risk_engine.py --input case.json --verbose

# Output formats
python scripts/risk_engine.py --input case.json --format json      # default
python scripts/risk_engine.py --input case.json --format markdown   # markdown table
python scripts/risk_engine.py --input case.json --format plain      # plain text
```

## Complete Tag Reference

### Vulnerability Tags
| Tag | Weight | Description |
|-----|--------|-------------|
| possible_pregnancy | 5 | User might be pregnant but unconfirmed |
| pregnancy | 6 | Confirmed pregnancy |
| post_op | 5 | Post-surgery recovery |
| chronic_illness | 3 | Ongoing medical condition |
| elder | 3 | Advanced age vulnerability |
| child | 4 | Minor involved |
| fatigue | 2 | Significant tiredness or sleep debt |
| mobility_limit | 3 | Physical mobility constraint |

### Exposure Tags
| Tag | Weight | Description |
|-----|--------|-------------|
| chemical | 6 | Chemical exposure risk |
| infectious | 4 | Biological/infection risk |
| heat | 3 | Extreme heat exposure |
| cold | 2 | Extreme cold exposure |
| radiation | 6 | Radiation hazard |
| dust | 3 | Dust/particulate exposure |
| noise | 2 | Hazardous noise levels |
| long_walking | 3 | Extended walking expected |
| lifting | 3 | Heavy lifting expected |
| night_travel | 3 | Travel during late night |
| isolation | 4 | Remote or isolated location |
| alcohol | 2 | Alcohol involvement |
| non_reversible_payment | 6 | Payment cannot be reversed |
| document_handover | 4 | Sensitive documents being handed over |
| extreme_exertion | 3 | Intense physical activity beyond normal capacity |
| altitude | 3 | High altitude exposure |
| deep_water | 4 | Open water or deep water activity |
| construction_hazard | 4 | Active construction or renovation site |
| formaldehyde_fumes | 4 | Renovation off-gassing or chemical fumes in living space |

### Counterparty Tags
| Tag | Weight | Description |
|-----|--------|-------------|
| unverified_stranger | 4 | Person not independently verified |
| pressure | 4 | Felt pressure or urgency from counterpart |
| urgency | 4 | Time pressure applied |
| secrecy | 5 | Request for secrecy or discretion |
| identity_mismatch | 5 | Identity doesn't match expectations |
| unverified_organization | 4 | Company or organization not independently verified |
| upfront_fee_required | 5 | Demanding payment before service is rendered |
| document_confiscation | 6 | Taking ID, bank card, or phone — trafficking signal |
| movement_restriction | 6 | Limiting ability to leave or communicate |

### Constraint Tags
| Tag | Weight | Description |
|-----|--------|-------------|
| cannot_exit_freely | 7 | User cannot leave independently |
| poor_medical_access | 4 | No nearby medical support |
| no_fallback_transport | 3 | No backup transport option |
| dead_phone_risk | 2 | Risk of phone running out |
| dependent_involved | 5 | Vulnerable dependent is involved |

### Transport Tags
| Tag | Weight | Description |
|-----|--------|-------------|
| driver_fatigue | 4 | Driver is tired, sleepy, or not well-rested |
| poor_vehicle_condition | 4 | Vehicle has known issues or hasn't been serviced |
| bad_weather_route | 3 | Rain, snow, fog, or extreme weather along the route |
| unfamiliar_route | 2 | Driver has not driven this route before |

### Digital Fraud Tags
| Tag | Weight | Description |
|-----|--------|-------------|
| unsolicited_contact | 4 | Contact came to you, not initiated by you |
| credential_request | 5 | Asking for passwords, codes, IDs, or account access |
| threat_or_ultimatum | 5 | "Act now or lose access" / "Your account will be locked" |
| suspicious_payment_method | 4 | Gift cards, crypto to unknown wallet, wire to unfamiliar account |

### Anticipatory Tags (v2.0 — pre-mortem / coupling / resilience dimensions)
| Tag | Weight | Description |
|-----|--------|-------------|
| one_way_door | 5 | Decision is irreversible or very costly to reverse |
| no_rollback | 4 | No tested rollback path exists |
| unvalidated_assumption | 3 | Key assumption not validated |
| tight_coupling | 4 | Components depend on each other with zero slack |
| single_point_of_failure | 5 | No fallback for a critical component |
| cross_system_dependency | 3 | Failure propagates across system boundaries |
| zero_time_slack | 3 | No time buffer for recovery |
| zero_resource_slack | 3 | No resource buffer for recovery |

### Cognitive Bias Tags (v2.0 — Kahneman-style debiasing)
| Tag | Weight | Description |
|-----|--------|-------------|
| overconfidence | 3 | Timeline or outcome confidence exceeds accuracy |
| planning_fallacy | 3 | Time/cost systematically underestimated |
| anchoring | 2 | Estimate anchored to first available number |
| survivorship_bias | 2 | Only considering successful cases |
| normalization_of_deviance | 4 | "It worked before" tolerance of increasing risk |

### Safeguard Tags (negative weights reduce risk)
| Tag | Weight | Description |
|-----|--------|-------------|
| public_place | -2 | Activity in a public, populated setting |
| trusted_companion | -3 | Reliable companion present |
| verified_identity | -3 | Counterparty identity verified independently |
| reversible_payment | -3 | Payment method allows chargeback or refund |
| confirmed_ppe | -3 | Personal protective equipment confirmed available |
| can_exit_independently | -3 | User can leave at any time without dependency |
| live_location_shared | -1 | Real-time location shared with trusted contact |
| medical_support_nearby | -2 | Medical facility accessible nearby |
| checked_weather | -2 | Weather and route conditions verified before travel |
| travel_insurance | -2 | Travel or trip insurance in place |
| verified_organization | -3 | Organization or venue independently verified as legitimate |
| feature_flags | -2 | Feature flags or kill switch available for rollback |
| gradual_rollout | -2 | Canary / staged rollout plan in place |
| belief_update_signals | -1 | Defined thresholds for plan revision |

### Life/Work Safety Tags (v2.1 — everyday risk scenarios)
| Tag | Weight | Description |
|-----|--------|-------------|
| second_medical_opinion | -3 | Got a second medical opinion before decision |
| written_contract | -2 | Have a written, reviewed contract |
| safety_briefing_received | -2 | Received site safety orientation or briefing |
| emergency_kit_ready | -1 | Emergency supplies prepared (water, food, first aid, flashlight) |
| home_alarm_or_monitoring | -1 | Home security system active |

### Scenario Tags (base weights, +1 or +2)
| Tag | Weight | Description |
|-----|--------|-------------|
| travel_and_mobility | 1 | Flights, trains, taxis, driving, rideshare |
| workplace_or_site_visit | 2 | Plant, lab, construction site, warehouse |
| health_sensitive_activity | 2 | Pregnancy, post-op, chronic illness |
| stranger_interaction_or_relationship_meeting | 2 | Dates, online contacts, private interviews |
| housing_or_property_viewing | 1 | Rentals, viewings, sublets |
| transaction_payment_or_asset_transfer | 2 | Deposits, wire transfers, crypto |
| caregiving_or_dependent_protection | 1 | Children, elders, disability support |
| outdoor_or_environmental_exposure | 1 | Hiking, camping, boating, beaches |
| nightlife_or_isolated_time_movement | 2 | Late trains, bars, clubs, early departures |
| online_to_offline_conversion | 2 | Moving online conversation to real-world meeting |
| business_trip_or_multi_day_travel | 1 | Work trips, conferences, multi-day travel |
| digital_fraud_scam_or_phishing_risk | 2 | Suspicious links, phishing, romance scams |
| job_interview_or_onboarding | 1 | Job interviews, trial work, recruitment |
| medical_visit_or_decision | 2 | Surgery decisions, treatment plans, hospital choices |
| natural_disaster_response | 2 | Typhoon, earthquake, flood, wildfire warning |
| home_and_family_safety | 1 | Elderly alone, child safety, home security |
| job_scam_or_exploitation | 2 | Suspicious offers, MLM, upfront fee scams |
| sports_and_fitness_activity | 1 | New exercise, extreme sports, marathon |
| home_service_or_renovation | 1 | Hiring workers, renovation, cleaning service |

### Anticipatory Safeguard Tags (v2.0 — reduce pre-mortem/coupling risk)
| Tag | Weight | Description |
|-----|--------|-------------|
| rollback_tested | -3 | Rollback plan tested and confirmed working |
| buffer_time | -2 | Time buffer added to schedule |
| buffer_resources | -2 | Resource buffer (compute, budget, people) set aside |
| second_opinion_obtained | -2 | Independent person reviewed the plan |
| monitoring_configured | -2 | Leading indicators set up before execution |
| checklist_completed | -2 | Phase 1 checklist fully completed |
| assumption_validated | -2 | Key assumptions confirmed through independent check |
