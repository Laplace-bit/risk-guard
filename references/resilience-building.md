# Phase 6: Build Resilience (构建韧性)

### Core Insight
Phases 1-5 help you think better about what might happen. But the most
important risks are the ones nobody can think of. Phase 6 doesn't try to
predict — it tries to **build systems that survive the unpredictable**.

Three lenses:
- **Antifragile Design** — Systems that get STRONGER from disruption (Taleb)
- **Graceful Degradation** — Systems that degrade gradually, not catastrophically (Hollnagel)
- **Belief-Update Signals** — Knowing WHEN to revise the plan (Bayesian Surprise)

---

## Part A: Antifragile Design (反脆弱设计)

### Origin
Nassim Nicholas Taleb, *Antifragile* (2012). Extension of Black Swan theory.

### Core Insight
Three types of systems:
- **Fragile** — Breaks under stress (glass)
- **Robust** — Survives stress unchanged (rock)
- **Antifragile** — Gets STRONGER under stress (muscles, immune system)

Most risk management aims for robust. Antifragility aims higher: benefit from
volatility and disorder.

### The Barbell Strategy

Avoid the "medium-risk" middle:
- **One side:** Limit maximum loss (cap tail risk)
- **Other side:** Take many small upside bets (convexity)

| Dimension | Cap the Downside | Small Upside Bets |
|-----------|-------------------------------|-------------------------------|
| Features | Ship minimum + measure | Try 5 experimental, kill 4 |
| Architecture | Core must never fail | Plugins fail independently |
| Team | Key person risk mitigated | Cross-train, rotate |
| Data | Backup + tested restore | Capture new sources opportunistically |

### Antifragility Audit

| Component | Fragile? | Robust? | Antifragile? | How to Move Right |
|-----------|:-------:|:-------:|:------------:|-------------------|
| [component] | ✅/❌ | ✅/❌ | ✅/❌ | [specific action] |

**How to move from fragile to antifragile:**
- Add **variation** — diverse approaches, not single methods
- Add **skin in the game** — consequences for failure create learning
- Add **optionality** — preserve ability to change course
- Remove **debt** (technical, operational) — debt amplifies stress
- Add **stress regularly** — small controlled stressors build adaptive capacity

**Key test:** If this plan encountered unexpected disruption, would it:
(a) break, (b) survive but weakened, (c) survive and potentially improve?

---

## Part B: Graceful Degradation (优雅降级)

### Origin
Erik Hollnagel, *Resilience Engineering* (2006). Safety-II paradigm.

### Core Insight
Most systems are brittle: they work perfectly until they catastrophically
don't. Resilient systems degrade gradually — they lose features one at a time
while maintaining core function.

**What breaks first, and what survives last?**

### The Efficiency-Thoroughness Trade-Off (ETTO)

People ALWAYS trade thoroughness for efficiency. This is normal. The question
is: **has context changed so the usual shortcuts are now dangerous?**

| Where | Efficiency Shortcut | When Dangerous? |
|-------|---------------------|-----------------|
| [step] | [what's skipped] | [condition making skip unsafe] |

### Degradation Cascade Analysis

| Failure Order | What Fails | System Function | User Impact | Recovery |
|:------------:|-----------|:--------------:|:-----------:|----------|
| 1st | [most likely] | Full/Partial/None | [impact] | [action] |
| 2nd | [next] | Partial/Minimal | [impact] | [action] |
| 3rd | [critical] | Minimal/None | [impact] | [action] |

**Goal:** System reaches "minimal viable function" before "none."
If jump from "partial" to "none" is abrupt, that component needs redundancy.

### Four Resilience Capacities (Hollnagel)

| Capacity | Question | Rating | Improve How |
|----------|---------|:------:|-------------|
| **Responding** | Can the plan adapt to disruptions as they happen? | H/M/L | [action] |
| **Monitoring** | Are there leading indicators of degradation? | H/M/L | [action] |
| **Anticipating** | Are there known futures the plan isn't ready for? | H/M/L | [action] |
| **Learning** | Does the plan get better from experience? | H/M/L | [action] |

### Margin Audit

Where is there **zero slack**? Zero slack = first thing to break.

| Component | Current Slack | Required Min | Adequate? | Add Slack How |
|-----------|:------------:|:------------:|:---------:|---------------|
| Time | [buffer] | [min] | ✅/❌ | [how] |
| Compute | [headroom] | [min] | ✅/❌ | |
| People | [bus factor] | ≥2 | ✅/❌ | |
| Budget | [contingency] | 20%+ | ✅/❌ | |
| Data | [replication] | [min] | ✅/❌ | |

---

## Part C: Belief-Update Signals (信念更新信号)

### Origin
Bayesian Surprise (Itti & Baldi, 2006). Signal Detection Theory.

### Core Insight
Not all unexpected events are equally important. A rare event that confirms
existing beliefs is less important than a moderate event that **changes beliefs.**

**What observation would force us to revise our plan?**

If nothing could change your plan, you're not planning — you're hoping.

### Signal Design Exercise

**Step 1: List key plan assumptions** (from Phase 2)

| Assumption | Currently Believed | What Evidence Changes Belief? | How to Monitor |
|------------|-------------------|-------------------------------|----------------|
| [assumption] | [confidence] | [specific observation] | [method] |

**Step 2: Define trigger thresholds**

| Signal | 🟢 Green (continue) | 🟡 Yellow (review) | 🔴 Red (stop + revise) |
|--------|:------------------:|:------------------:|:---------------------:|
| [metric] | [range] | [range] | [range] |

**Step 3: Define revision protocols**

| Signal Level | Action | Who Decides | Time to Decision |
|:------------:|--------|:-----------:|:----------------:|
| 🟢 Green | Continue | anyone | N/A |
| 🟡 Yellow | Review within [timeframe] | [role] | [deadline] |
| 🔴 Red | Stop, emergency review | [role] | immediately |

**Step 4: Safe-to-fail experiments**

Instead of predicting, run small experiments that are safe to fail but informative:

| Experiment | Tests | Cost If Fails | What We Learn |
|------------|-------|:------------:|---------------|
| [small probe] | [hypothesis] | [bounded] | [signal] |

These are antifragile: small downside, potentially large informational upside.

---

## Synthesis

| Layer | Question | If Missing |
|-------|----------|-----------|
| **Antifragile Design** | Where can we benefit from disruption? | Plan survives only in expected conditions |
| **Graceful Degradation** | What breaks first? What survives last? | Plan is brittle — works or doesn't |
| **Belief-Update Signals** | What would force us to change the plan? | Plan continues even when evidence says stop |

**The ultimate test:** After all 6 phases, ask:

> "If everything we didn't think of happened simultaneously, what would still work?"

The answer defines the true resilience of the plan.