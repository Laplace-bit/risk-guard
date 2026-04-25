---
name: risk-guard
description: Use when the user asks to think something through, wants a risk assessment, asks "is this safe", "what could go wrong", describes a plan with real consequences, or is preparing for travel/outdoor/business trip activities. Two modes: Quick Review for safety checks and Full Review for thorough anticipatory analysis. Do NOT use for simple actions, info queries, code debugging, or casual conversation.
---

# Risk Guard — 周全思维

## Core Principle

Most failures come from three sources: known risks we forgot to check, blind spots in our thinking, and things no one could predict. Risk Guard applies a three-layer defense: checklists, framework switching, and resilience design.

## The Iron Law

```
NO PLAN EXECUTION WITHOUT RISK REVIEW WHEN STAKES ARE REAL
```

Violating the letter = violating the spirit. "Probably fine" is not a review. "I'll be careful" is not a safeguard. "Just this once" is not an exception.

## When to Use

- User asks: "风险评估" / "安全审查" / "安不安全" / "is this safe" / "what could go wrong" / "pitfalls" → **Quick Review**
- User asks: "帮我想想周全一点" / "有什么没想到的" / "全面分析一下" / "think it through" → **Full Review**
- User describes a multi-step plan about to execute with real consequences → **Full Review**
- User mentions travel / outing / business trip / outdoor preparation → **Quick Review**
- A reasonable person would proactively seek a safety review

## When NOT to Use

- Simple single-step actions ("帮我改这个文件")
- Information queries ("这个API怎么用")
- Casual conversation or completed-action retrospectives
- Code debugging (→ use systematic-debugging)
- When user just wants a quick answer, not thorough analysis
- Everyday offhand remarks with no preparation or stakes ("我下楼买个咖啡")

**Trigger heuristic:** Only activate when (a) user explicitly asks for risk/thorough analysis, OR (b) a multi-step plan with real stakes is about to execute, OR (c) travel/outing/business trip/outdoor activity preparation. When in doubt, don't trigger — false negatives are preferable to interrupting normal AI usage.

If unclear, ask: "需要全面分析还是只看安全问题？"

## Quick Review

**Announce at start (only if unsolicited):** "I'll review this for safety risks."

### Step 1: Classify

Map to scenario groups in `./references/scenario-map.md`.

### Step 2: Gather

Verify facts independently (weather, route conditions, venue safety, news). Don't ask the user what you can find yourself.

### Step 3: Ask

At most 4 high-value questions per round. Only ask what could change the recommendation. Consult `./references/question-bank.md`.

### Step 4: Model

Assess across 7 dimensions:

| Factor | Question |
|--------|----------|
| Vulnerability | How fragile is the user or any dependent? |
| Exposure | What harmful source could reach them? |
| Friction | What increases difficulty of escaping? |
| Support & recovery | What controls and fallbacks exist? |
| Transport detail | Who is driving, what's the route and weather? |
| Reversibility | How bad is the outcome if it happens? |
| Uncertainty | How much critical information is missing? |

### Step 5: Run Risk Engine (optional)

For complex cases with 6+ factors or multiple scenario groups:

```bash
python scripts/risk_engine.py --input case.json
```

Schema: `./references/risk-engine-schema.md`

### Step 6: Output

Follow the Quick Review output format in `./references/output-examples.md`.

## Full Review — 6 Phases

**Announce at start:** "I'll run a full 6-phase review."

Run all phases in order. Each builds on the previous. Skip phases only when trivially inapplicable (state which and why). **Any Phase 1 🔴 must be resolved before proceeding.**

| Phase | Goal | Reference |
|:-----:|------|-----------|
| 1 | Catch every known risk | `./references/checklists.md` |
| 2 | What guarantees failure? What's irreversible? | `./references/inversion-and-precaution.md` |
| 3 | Pre-mortem, red team, fear setting | `./references/premortem-redteam-fearsetting.md` |
| 4 | Complexity/coupling, edge cases, debiasing | `./references/stress-test.md` |
| 5 | Test against 4 different futures | `./references/scenario-planning.md` |
| 6 | Antifragile design, graceful degradation | `./references/resilience-building.md` |

**After Phase 3, identify the kill assumption:** What single assumption, if wrong, would reverse this entire assessment?

Output format → `./references/output-examples.md`

## Core Operating Rules

- Distinguish clearly between facts, inferences, and unknowns
- Prefer false positives over false negatives when downside is irreversible or severe
- Raise the level when several moderate factors combine
- High-sensitivity modifiers: pregnancy, infancy, advanced age, disability, surgery recovery, chronic illness, severe fatigue, isolation, unfamiliar locations, hazardous workplaces, coercion, urgent money movement
- Never say an outcome is certain unless confirmed
- Never hide uncertainty — if key info is missing, say so explicitly
- Do not overwhelm with every danger. Prioritize the 3-5 most material risks
- Do not present risk reasoning as formal medical, legal, or engineering advice

## Escalation Heuristics

**STOP and inform the user when:**
- Phase 1 finds 🔴 blockers
- Phase 2 identifies ≥2 one-way doors with no checkpoints
- Phase 3 pre-mortem finds irreversible failure with no detection signal
- Quick Review compound risk reaches red level
- Irreversible or severe health harm is possible
- Pregnancy + chemical/infectious/thermal/physical exposure
- Minors/elders/dependents with unreliable care or transport
- Late night isolation + unfamiliar area + poor exit options
- Urgent money/identity transfer to weakly verified parties
- User language minimizes risk: "probably fine", "just once", "should be okay"

**Recommend but don't block when:**
- Medium-likelihood failure modes found
- Plan fragile in 2+ scenarios but not all
- Resilience improvements suggested

## Red Flags

| Thought | Reality |
|---------|---------|
| "Probably fine" | Unguarded risk. If you can't articulate why it's fine, it isn't. |
| "Just this once" | One-time exceptions create precedent and miss compound risk. |
| "Should be okay" | "Should" means you don't know. Find out. |
| "I'll be careful" | Care is not a safeguard. Safeguards are structural. |
| "They seem trustworthy" | Feeling is not verification. Verify independently. |
| "Nothing happened before" | Survivorship bias. Absence of failure ≠ presence of safety. |
| "We don't have time to review" | Time pressure itself is a risk factor (urgency tag). |

## Final Check Before Responding

Before sending the answer, verify:
1. [ ] Facts separated from unknowns? If not, mark each claim as [FACT], [INFERENCE], or [UNKNOWN]
2. [ ] Compound risk considered? If only isolated risks listed, combine them
3. [ ] Hardest-to-reverse outcomes identified? If none, you missed something
4. [ ] Practical next step given? If only "be careful", specify an action
5. [ ] Kill assumption identified? Name the single assumption whose failure reverses the conclusion
6. [ ] Answer concise? Quick Review ≤ 500 words; Full Review as long as needed but no padding

## Domain References

### Quick Review
- `./references/scenario-map.md` — scenario identification and typical factor patterns
- `./references/question-bank.md` — high-yield follow-up questions by scenario
- `./references/risk-taxonomy.md` — cross-domain risk categories, red flags, compounding logic
- `./references/output-examples.md` — style and structure examples
- `./references/risk-engine-schema.md` — structured input for the risk engine

### Full Review
- `./references/checklists.md` — Phase 1: universal + scenario-specific checklists
- `./references/inversion-and-precaution.md` — Phase 2: inversion, one-way doors, precautionary principle
- `./references/premortem-redteam-fearsetting.md` — Phase 3: pre-mortem, red team, fear setting
- `./references/stress-test.md` — Phase 4: complexity/coupling, edge cases, cognitive debiasing
- `./references/scenario-planning.md` — Phase 5: 4-scenario matrix, robust & hedging actions
- `./references/resilience-building.md` — Phase 6: antifragility, graceful degradation, belief-update signals