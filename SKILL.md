---
name: risk-guard
description: Analyze planned real-world actions for low-probability high-impact risks. ONLY use when the user explicitly asks for a risk assessment, safety check, or go/no-go judgment — or when they describe a situation that a reasonable person would want a safety review for (e.g., meeting a stranger alone at night, handling hazardous materials, sending money to an unverified party). Do NOT trigger for general advice, planning, recommendations, or casual conversation.
---

# Risk Guard

## Overview

Use this skill to turn a vague planned action into a structured safety review.
Treat the task as low-frequency high-severity risk auditing, not fortune telling.

**Announce at start (only if the user did not explicitly request a risk check):** "I'll review this for safety risks."

## Workflow

1. **Classify** the user's planned action into one or more scenario groups.
2. **Gather** verifiable facts independently (weather, route conditions, venue safety, news) — don't ask the user what you can find yourself.
3. **Ask** only the highest-value missing questions (max 4 in the first round) — questions that could change the recommendation and can't be answered by search.
4. **Model** vulnerability, exposure, friction, safeguards, reversibility, and uncertainty.
5. **Run the risk engine** when structured inputs are available or when the case is complex.
6. **Produce** a short decision-oriented output with missing facts, main risks, worst credible outcomes, and concrete next steps.

## Core Operating Rules

- Distinguish clearly between facts, inferences, and unknowns.
- Prefer false positives over false negatives when the downside is irreversible or severe.
- Raise the level when several moderate factors combine.
- Treat the following as high-sensitivity modifiers: pregnancy, possible pregnancy, infancy, advanced age, disability, surgery recovery, chronic illness, severe fatigue, isolation, unfamiliar locations, hazardous workplaces, coercion, and urgent money movement.
- Never say an outcome is certain unless the user already supplied a confirmed fact.
- Never hide uncertainty. If key information is missing, say so explicitly and lower confidence.
- Do not overwhelm the user with every possible danger. Prioritize the 3 to 5 most material risks.
- Do not present risk reasoning as formal medical, legal, or engineering advice.

## Classification Step

Map the user input to one or more scenario groups. Consult `references/scenario-map.md` when the classification is unclear.

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

If the user message is broad (e.g., "I need to travel tomorrow" or "I'm going to meet someone"), ask a small batch of targeted questions before giving any judgment.

## Active Information Gathering

**Do not just ask the user — verify what you can independently.**

When the user shares verifiable facts (destination, dates, route, venue), use web search, weather APIs, or any available tools to gather:

- **Weather and road conditions** for the travel date and route
- **Destination risk profile** — news about incidents, safety advisories, hazard reports for the specific location
- **Venue information** — if it's a factory/site, any public safety records or news

If you can find the answer by searching, don't waste the user's question quota on it. Instead, report what you found and ask only what you couldn't verify.

## Question Strategy

Consult `references/question-bank.md`.

Ask at most 4 high-value questions in the first round unless the user already provided enough detail.
Choose questions from these dimensions:

| Dimension | Examples |
|-----------|----------|
| **Vulnerability** | Pregnancy, health status, age-related vulnerability, fatigue, medication, recent procedure |
| **Environment** | Location type, hazard sources, crowding, isolation, weather, building conditions |
| **Activity load** | Duration, walking, lifting, standing, night hours, alcohol, cash carried |
| **Counterpart risk** | Stranger identity, verification, pressure, incentives, coercion, urgency |
| **Support and recovery** | Companion, emergency contact, transport fallback, medical access, ability to leave |
| **Transport detail** | Driver status, vehicle condition, route familiarity, weather along route, backup transport |

Do not ask generic filler questions.
Only ask questions that could change the recommendation.

## Risk Model

Use this mental model every time:

| Factor | Question |
|--------|----------|
| **Vulnerability** | How fragile is the user or any dependent person in this scenario? |
| **Exposure** | What harmful source could reach them? |
| **Friction** | What increases duration, load, or difficulty of escaping the situation? |
| **Support and recovery** | What controls and fallbacks exist? Who can help? |
| **Transport detail** | Who is driving, what condition is the vehicle, what's the route and weather? |
| **Reversibility** | How bad is the outcome if the event happens? |
| **Uncertainty** | How much critical information is still missing? |

### Escalation Heuristics

Escalate strongly when **any** of these are present:

- Irreversible or severe health harm
- Pregnancy or possible pregnancy + chemical, infectious, thermal, physical, or overexertion exposure
- Minors, elders, or dependents exposed to unreliable care or transport
- Late night isolation, unfamiliar area, poor exit options, or no trusted contact
- Urgent transfer of money, deposits, gifts, crypto, or identity documents to strangers or weakly verified parties
- User language minimizes risk: "probably fine", "just once", "should be okay", "I don't want to make trouble"
- Several moderate factors stack together

## Script Usage

For complex or borderline cases, structure the facts and run:

```bash
python scripts/risk_engine.py --input case.json
```

The JSON schema is described in `references/risk-engine-schema.md`.

Use the script especially when:

- Multiple scenario groups apply
- There are more than 6 meaningful factors
- The user wants a consistent rating
- You need to explain why a case was escalated

## Output Format

Keep the answer concise and action-oriented. Use this exact structure unless the user asks for something else:

### Situation summary
One sentence confirming what the user is doing, where, when, and with whom. This lets the user verify you understood correctly before they read the judgment.

### What I found automatically
Brief list of facts you verified by search (weather, route conditions, venue info, local news). If nothing was searched, say "No independent search was performed for this case."

### Decision
One line: green / yellow / orange / red, followed by the plain-language takeaway.

### Why this is risky
3 bullets maximum. Focus on compound risk, not a long list.

### Missing critical facts
List only the missing items that could change the recommendation.
If there are none, say "none that materially change the judgment".

### Best next actions
Give 3 to 5 actions in priority order.

### Worst credible outcomes
Name the most material low-probability high-impact outcomes in plain language.

### Confidence
State high / medium / low with a one-line reason.

## Output Style Rules

- Prefer short direct sentences.
- Lead with the judgment, not the background analysis.
- Say "I would not do this as currently described" when the case is orange or red.
- For green or yellow, still include safeguards.
- Do not write like a legal disclaimer.

## Domain References

- `references/scenario-map.md`: scenario identification and typical factor patterns
- `references/question-bank.md`: high-yield follow-up questions by scenario
- `references/risk-taxonomy.md`: cross-domain risk categories, red flags, and compounding logic
- `references/output-examples.md`: style and structure examples
- `references/risk-engine-schema.md`: structured input for the risk engine

## Example Requests That Should Trigger This Skill

- "I'm six weeks pregnant and need to visit a chemical plant for work tomorrow"
- "I'm meeting a stranger from the internet tonight at a bar near the highway"
- "I need to travel alone at 2 am with expensive equipment"
- "A landlord wants a deposit before showing me the place"
- "My parent with dementia wants to take a taxi alone to the hospital"
- "I'm going hiking in extreme heat with limited water"
- "Is it safe to do X?" or "Should I be worried about X?" or "Risk check on X"
- "帮我看看这个事情安不安全" or "风险评估" or "安全审查"

## Do NOT Trigger This Skill For

- General travel planning ("帮我规划一下杭州三日游") — no safety concern expressed
- Casual recommendations ("推荐个餐厅") — no risk context
- Factual questions ("明天杭州天气怎么样") — user just wants info, not a risk judgment
- General advice ("孕期能不能喝咖啡") — not a specific planned action with real-world stakes
- Productivity or work tasks ("帮我写份报告") — no physical/financial safety dimension
- Coding or technical questions — no real-world safety dimension
- Emotional support or general conversation — not a safety review

**Trigger heuristic:** Only activate when (a) the user explicitly asks for a risk/safety assessment, OR (b) a reasonable person in the same situation would proactively seek a safety review. When in doubt, don't trigger — false negatives are preferable to interrupting normal AI usage.

## Final Check Before Responding

Before sending the answer, verify that you have:

- [ ] Separated facts from unknowns
- [ ] Considered compound risk rather than isolated risk
- [ ] Considered the hardest-to-reverse outcomes
- [ ] Given a practical next step
- [ ] Kept the answer concise