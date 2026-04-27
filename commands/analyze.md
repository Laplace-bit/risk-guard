---
description: "Deep risk analysis: 6-phase full assessment (checklist → inversion → premortem → stress test → scenario planning → resilience)"
---

Deep risk analysis. Runs all 6 phases. Use for complex decisions and major plans.

Use for: deployments, migrations, major surgery decisions, complex travel, large transactions, etc.

Example: `/risk-guard analyze "We're migrating the production database this weekend"`

6 phases:
1. **Checklist** — Systematic check of known risks
2. **Inversion & Precaution** — What guarantees failure? What's irreversible?
3. **Premortem + Red Team + Fear Setting** — Imagine it failed; work backward
4. **Stress Test** — Complexity/coupling, edge cases, cognitive debiasing
5. **Scenario Planning** — 4 alternative future scenarios
6. **Resilience Building** — Antifragility, graceful degradation, belief-update signals

Only use when the user explicitly requests deep analysis. For everyday safety reminders, use `check`.