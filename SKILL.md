---
name: risk-guard
description: >
  Help people think more thoroughly and avoid unexpected failures. Use when the
  user asks to think something through, wants a risk assessment, or is about to
  execute a plan with real consequences. Two modes: Quick Review (safety-focused,
  physical/financial risk) and Full Review (6-phase anticipatory thinking).
  ONLY use when explicitly requested or when a multi-step plan with real stakes
  is about to execute. Do NOT trigger for simple actions, info queries, or casual
  conversation.
version: 2.0.2
---

# Risk Guard — 周全思维

## Core Idea

Most failures come from three sources:
1. **Known risks we forgot to check** → solved by checklists
2. **Blind spots in our thinking** → solved by switching cognitive frameworks
3. **Things no one could predict** → solved by building resilience

Risk Guard helps you think thoroughly before acting. It applies a three-layer
defense: checklists (known risks), framework switching (blind spots), and
resilience design (unknowable risks).

## Two Modes

### Quick Review (快速审查)
For safety-specific scenarios: travel, stranger meetings, transactions, hazardous
activities. Uses the classic Classify → Question → Model → Judge workflow.
Focused on physical/financial/personal safety.

### Full Review (全面审查)
When the user asks to "think it through" or "think more thoroughly", or before
executing a multi-step plan with real consequences. Runs all 6 phases.

**Mode selection:**
- User asks "安不安全" / "风险评估" → Quick Review
- User asks "想周全一点" / "有什么没想到的" / "帮我想想这件事" → Full Review
- Multi-step plan about to execute with real stakes → Full Review
- In doubt → ask "需要全面分析还是只看安全问题？"

---

## Quick Review (快速审查)

**Announce at start (only if unsolicited):** "I'll review this for safety risks."

### Step 1: Classify

Map to one or more scenario groups. Consult `references/scenario-map.md` when unclear.

| # | Scenario Group |
|---|----------------|
| 1 | Travel and mobility |
| 2 | Workplace or site visit |
| 3 | Health-sensitive activity |
| 4 | Stranger interaction or relationship meeting |
| 5 | Housing or property viewing |
| 6 | Transaction, payment, or asset transfer |
| 7 | Caregiving or dependent protection |
| 8 | Outdoor or environmental exposure |
| 9 | Nightlife or isolated-time movement |
| 10 | Online-to-offline conversion |
| 11 | Business trip or multi-day travel |
| 12 | Digital fraud, scam, or phishing risk |

### Step 2: Gather

Verify facts independently (weather, route conditions, venue safety, news).
Don't ask the user what you can find yourself.

### Step 3: Ask

At most 4 high-value questions per round. Only ask what could change the
recommendation. Consult `references/question-bank.md`.

### Step 4: Model

Assess across 7 dimensions:

| Factor | Question |
|--------|----------|
| **Vulnerability** | How fragile is the user or any dependent? |
| **Exposure** | What harmful source could reach them? |
| **Friction** | What increases difficulty of escaping? |
| **Support & recovery** | What controls and fallbacks exist? |
| **Transport detail** | Who is driving, what's the route and weather? |
| **Reversibility** | How bad is the outcome if it happens? |
| **Uncertainty** | How much critical information is missing? |

### Step 5: Run Risk Engine (optional)

For complex cases with 6+ factors:
```bash
python scripts/risk_engine.py --input case.json
```
Schema: `references/risk-engine-schema.md`

### Step 6: Produce Output

**Quick Review output format:**

### Situation summary
One sentence: what, where, when, with whom.

### What I found automatically
Facts verified by search. Or: "No independent search was performed."

### Decision
green / yellow / orange / red — plain-language takeaway.

### Why this is risky
3 bullets max. Focus on compound risk.

### Missing critical facts
Items that could change the recommendation. Or: "none that materially change the judgment."

### Best next actions
3-5 actions in priority order.

### Worst credible outcomes
Most material low-probability high-impact outcomes.

### Confidence
high / medium / low — one-line reason.

---

## Full Review (全面审查) — 6 Phases

Apply all phases in order. Each builds on the previous.
Skip phases only when trivially inapplicable (state which and why).

---

### Phase 1: Checklist (检查清单)

**Goal:** Catch every known risk. No known pitfall should slip through.

Consult `references/checklists.md` for:
- **Universal checklist** — applies to ALL plans
- **Scenario-specific checklists** — deploy, migration, data operation, integration, release, config change

For each item: ✅ (safe), ⚠️ (risk noted), 🔴 (blocks execution).

**Phase gate:** Any 🔴 must be resolved before proceeding.

---

### Phase 2: Inversion & Precaution (逆向与预防)

**Goal:** What would guarantee failure? What's irreversible?

Consult `references/inversion-and-precaution.md` for:
- **Inversion exercise** — "What would absolutely guarantee failure?" List and eliminate.
- **One-way door audit** — 🟢 Two-way / 🟡 Narrow / 🔴 One-way (irreversible)
- **Precautionary principle** — For irreversible actions, flip burden of proof: require "prove it's safe"
- **Death zones** — States from which recovery is impossible

**Output:** Death zones + one-way doors + linchpin assumptions.

---

### Phase 3: Imagine Failure (想象失败)

**Goal:** Generate failure narratives that checklists miss.

Consult `references/premortem-redteam-fearsetting.md` for:
- **Pre-mortem** (Klein) — Assume failure already happened, reverse-engineer causes. Generates ~30% more failure modes than forward risk analysis.
- **Red team** — Adopt adversarial perspective: "How would I destroy this plan?" Challenge each assumption.
- **Fear setting** (Ferriss/Stoic) — Articulate specific fears + prevention + repair + **cost of inaction**

**Output:** Top failure hypotheses + strongest counter-arguments + inaction cost.

---

### Phase 4: Stress Test (压力测试)

**Goal:** Find where the plan breaks under pressure.

Consult `references/stress-test.md` for:
- **Complexity & coupling analysis** (Perrow) — High complexity + tight coupling = normal accident zone. Adding safety measures may increase risk.
- **Edge case / boundary testing** — What happens at parameter extremes? When multiple boundaries hit simultaneously?
- **Cognitive debiasing** (Kahneman) — Correct: planning fallacy (use reference class forecasting), anchoring, availability heuristic, confirmation bias, survivorship bias, sunk cost, overconfidence

**Output:** Fragility map + debiased estimates + edge case behaviors.

---

### Phase 5: Scenario Planning (多未来场景)

**Goal:** The plan was built for one expected future. Test it against completely different ones.

Consult `references/scenario-planning.md` for:
- Identify 2 most uncertain + impactful dimensions
- Build 4 qualitatively different futures (not best/worst — genuinely different worlds)
- Test plan against each scenario
- Identify **robust actions** (work across scenarios) and **hedging actions** (insurance for worst cases)

**Output:** 4 scenario narratives + plan robustness per scenario + robust & hedging actions.

---

### Phase 6: Build Resilience (构建韧性)

**Goal:** Prepare for what no one can predict.

Consult `references/resilience-building.md` for:
- **Antifragile design** (Taleb) — Where can the plan get STRONGER from disruption? Barbell strategy: cap downside + small upside bets.
- **Graceful degradation** (Hollnagel) — What breaks first? What survives last? Four capacities: Responding, Monitoring, Anticipating, Learning.
- **Belief-update signals** — What observations should force plan revision? Define green/yellow/red thresholds.
- **Margin audit** — Where is there zero slack?

**Output:** Resilience recommendations + monitoring signals + safe-to-fail experiments.

---

**Full Review output format:**

### 🧠 Risk Guard — Full Review

**Plan:** [one-line summary]

**Phase 1 — Checklist:**
| Item | Status | Note |
|------|--------|------|
| ... | ✅/⚠️/🔴 | ... |

**Phase 2 — Death zones & one-way doors:**
- [Death zone]: [why unrecoverable]
- [One-way door 🟡/🔴]: [what makes it irreversible]

**Phase 3 — Failure hypotheses:**
1. [Most likely] — likelihood × severity
2. [Second] — ...
3. [Unexpected] — ...
- **Inaction cost:** [what happens if we do nothing]

**Phase 4 — Fragility map:**
- [Component]: fragile under [condition]
- **Debiased estimates:** [original → corrected]

**Phase 5 — Scenario test:**
| Scenario | Plan works? | Fragile points |
|----------|:-----------:|---------------|
| [A] | ✅/⚠️/❌ | ... |

**Phase 6 — Resilience:**
- **Antifragile moves:** [where plan benefits from disruption]
- **Graceful degradation:** [what fails first, what survives]
- **Watch signals:** [observations that should trigger revision]
- **Recommended slack:** [where to add buffer]

**Blind spot alert:** [The one thing across all phases nobody thought to check]

**Recommended guardrails (top 5):**
1. ...
2. ...
3. ...
4. ...
5. ...

---

## Core Operating Rules

- Distinguish clearly between facts, inferences, and unknowns
- Prefer false positives over false negatives when downside is irreversible or severe
- Raise the level when several moderate factors combine
- High-sensitivity modifiers: pregnancy, infancy, advanced age, disability, surgery recovery, chronic illness, severe fatigue, isolation, unfamiliar locations, hazardous workplaces, coercion, urgent money movement
- Never say an outcome is certain unless confirmed
- Never hide uncertainty — if key info is missing, say so explicitly
- Do not overwhelm with every danger. Prioritize the 3-5 most material risks
- Do not present risk reasoning as formal medical, legal, or engineering advice

### Escalation Heuristics

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

---

## When to Trigger

### ✅ Trigger When
- User asks: "风险评估" / "安全审查" / "安不安全" → Quick Review
- User asks: "帮我想想周全一点" / "有什么没想到的" / "全面分析一下" → Full Review
- User describes a multi-step plan about to execute with real consequences
- A reasonable person would proactively seek a safety review

### ❌ Do NOT Trigger For
- Simple single-step actions ("帮我改这个文件")
- Information queries ("这个API怎么用")
- Casual conversation
- General advice without specific planned action
- Code debugging (→ systematic-debugging)
- When user just wants a quick answer, not thorough analysis

**Trigger heuristic:** Only activate when (a) user explicitly asks for risk/thorough analysis, OR (b) a multi-step plan with real stakes is about to execute. When in doubt, don't trigger — false negatives are preferable to interrupting normal AI usage.

---

## Domain References

### Quick Review
- `references/scenario-map.md` — scenario identification and typical factor patterns
- `references/question-bank.md` — high-yield follow-up questions by scenario
- `references/risk-taxonomy.md` — cross-domain risk categories, red flags, compounding logic
- `references/output-examples.md` — style and structure examples
- `references/risk-engine-schema.md` — structured input for the risk engine

### Full Review
- `references/checklists.md` — Phase 1: universal + scenario-specific checklists
- `references/inversion-and-precaution.md` — Phase 2: inversion, one-way doors, precautionary principle
- `references/premortem-redteam-fearsetting.md` — Phase 3: pre-mortem, red team, fear setting
- `references/stress-test.md` — Phase 4: complexity/coupling, edge cases, cognitive debiasing
- `references/scenario-planning.md` — Phase 5: 4-scenario matrix, robust & hedging actions
- `references/resilience-building.md` — Phase 6: antifragility, graceful degradation, belief-update signals

---

## Example Requests

### Quick Review
- "I'm six weeks pregnant and need to visit a chemical plant tomorrow"
- "I'm meeting a stranger from the internet tonight at a bar"
- "A landlord wants a deposit before showing me the place"
- "帮我看看这个事情安不安全" / "风险评估"

### Full Review
- "我要部署新版本到生产环境，帮我想周全一点"
- "准备迁移数据库，有什么没想到的"
- "我们准备上线这个功能，全面分析一下"
- "帮我想想这件事有没有什么遗漏"

---

## Final Check Before Responding

Before sending the answer, verify that you have:
- [ ] Separated facts from unknowns
- [ ] Considered compound risk rather than isolated risk
- [ ] Considered the hardest-to-reverse outcomes
- [ ] Given a practical next step
- [ ] Kept the answer concise