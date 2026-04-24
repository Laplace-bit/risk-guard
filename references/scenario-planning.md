# Phase 5: Scenario Planning (多未来场景)

### Origin
Peter Schwartz, *The Art of the Long View* (1991). Royal Dutch Shell's
scenario planning practice. Successfully anticipated the 1973 oil crisis.

### Core Insight
Every plan is built for ONE expected future. But that future is just one of
many possibilities. Risk analysis generates variations of the same future
(best case / worst case). Scenario planning generates **qualitatively different
worlds** — and tests the plan against each.

---

## Why Standard Risk Analysis Fails Here

Standard risk analysis: base case, worst case, best case — incremental
variations of the same future.

Scenario planning: what if the ENTIRE CONTEXT changes? A plan that survives a
20% budget cut (risk variation) may collapse entirely if regulation changes
(scenario difference).

---

## The Scenario Planning Exercise

### Step 1: Identify Driving Forces

What forces will shape the outcome?

| Category | Driving Force | Impact (H/M/L) | Uncertainty (H/M/L) |
|----------|--------------|:---------------:|:--------------------:|
| Technology | [force] | | |
| Market/Customer | [force] | | |
| Regulatory/Legal | [force] | | |
| Organizational | [force] | | |
| Economic | [force] | | |
| Social/Cultural | [force] | | |

### Step 2: Separate Predetermined from Critical Uncertainties

**Predetermined elements** — already in motion, will play out regardless:
- Demographic shifts already underway
- Technology already developed and deployed
- Contracts already signed
- Resources already committed

**Critical uncertainties** — could go either way with high impact:
- Will the regulation pass?
- Will the competitor launch first?
- Will the API partner maintain compatibility?

### Step 3: Select the 2 Most Impactful + Uncertain Dimensions

These become the **axes** of the scenario matrix. They should be:
- Independent (not correlated)
- Genuinely uncertain
- High impact on the plan

### Step 4: Build 4 Scenarios at the Intersections

Each scenario is a **complete, internally consistent world**, not just a
description of one variable.

| | Axis 2: Positive | Axis 2: Negative |
|---|---|---|
| **Axis 1: Positive** | Scenario A | Scenario B |
| **Axis 1: Negative** | Scenario C | Scenario D |

For each scenario:
1. **Give it a vivid name** — names engage narrative reasoning
2. **Tell the story** — how this world came to be
3. **Describe specific conditions** this creates for our plan
4. **Describe who wins and who loses** in this world

### Step 5: Test the Plan Against Each Scenario

| Scenario | Plan Works? | Fragile Points | What Breaks First |
|----------|:-----------:|---------------|-------------------|
| [A name] | ✅/⚠️/❌ | | |
| [B name] | ✅/⚠️/❌ | | |
| [C name] | ✅/⚠️/❌ | | |
| [D name] | ✅/⚠️/❌ | | |

For each ⚠️/❌:
- What specific change would fix the fragility?
- Is this a **robust action** (make it now, helps in multiple scenarios) or
  a **hedging action** (prepare to make it if the scenario emerges)?

### Step 6: Identify Robust and Hedging Actions

| Action Type | Action | Protects Against | Cost | Worth It? |
|------------|--------|------------------|------|:---------:|
| Robust | [action] | Multiple scenarios | [cost] | Usually yes |
| Hedge | [action] | Specific scenario | [cost] | If scenario is severe enough |

### Step 7: Wildcard Scenarios (Optional)

1-2 **wildcard** scenarios — unlikely but high-impact events:
- Market crash, pandemic, key person departure
- Technological discontinuity
- Regulatory shock

For each: What would happen? Is there anything cheap we can do NOW that helps?

---

## Example: Software Release

**Axes:** User adoption rate (slow ↔ fast) × Infrastructure stability (stable ↔ unstable)

| | Fast Adoption | Slow Adoption |
|---|---|---|
| **Stable Infra** | 🚀 "Hockey Stick" | 🐌 "Slow Burn" |
| **Unstable Infra** | 💥 "Success Disaster" | 🏥 "Bleeding Out" |

**Plan test:**
- Hockey Stick: ✅ needs auto-scaling from day 1
- Slow Burn: ✅ needs better onboarding
- Success Disaster: ❌ no auto-scaling, no rate limiting
- Bleeding Out: ⚠️ users won't return after downtime

**Robust actions:** Add auto-scaling + rate limiting (helps both unstable scenarios)
**Hedging actions:** Prepare "we're fixing it" landing page (cheap insurance)

---

## Key Principle

**The value is NOT in predicting which scenario occurs. It's in finding actions
that work across multiple scenarios (robust) and cheap insurance for the worst
ones (hedging).** A plan that survives 3 of 4 scenarios is much stronger than
one that only works in the most likely one.