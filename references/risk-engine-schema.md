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
  "free_text": "optional case note"
}
```

## Notes
- Use short machine-friendly tags.
- Prefer explicit tags over long free-text.
- `free_text` is optional and only for human reference.
- The engine returns a score, level, triggered rules, and explanation snippets.

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

### Counterparty Tags
| Tag | Weight | Description |
|-----|--------|-------------|
| unverified_stranger | 4 | Person not independently verified |
| pressure | 4 | Felt pressure or urgency from counterpart |
| urgency | 4 | Time pressure applied |
| secrecy | 5 | Request for secrecy or discretion |
| identity_mismatch | 5 | Identity doesn't match expectations |

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