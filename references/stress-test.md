# Phase 4: Stress Test (压力测试)

Three lenses for finding where the plan breaks under pressure:
- **Complexity & Coupling Analysis** — System structure creates inevitable accidents (Perrow)
- **Edge Case / Boundary Testing** — Assumptions fail at extremities
- **Cognitive Debiasing** — The thinking process itself has systematic bugs (Kahneman)

---

## Part A: Complexity & Coupling Analysis (复杂度与耦合分析)

### Origin
Charles Perrow, *Normal Accidents* (1984). Analysis of Three Mile Island,
Challenger, and other systemic failures.

### Core Insight
Accidents in complex systems are not caused by individual component failures —
they are **normal** because system structure makes them inevitable.

**Interactive Complexity** — Components interact in ways not anticipated by
designers. A failure in A causes unexpected behavior in C through a path
nobody mapped.

**Tight Coupling** — Processes depend on each other with zero slack. A delay
in B immediately cascades to C with no buffer.

Systems with both properties are in the **normal accident zone**.

### The Analysis Exercise

**Step 1: Map dependencies**

| Component | Depends On | Type of Dependency |
|-----------|-----------|-------------------|
| [A] | [B, C] | data, compute, auth, timing, ... |

**Step 2: Assess interactive complexity**

- 🟢 **Low** — Interactions are linear, documented, expected
- 🟡 **Medium** — Some interactions are indirect or undocumented
- 🔴 **High** — Many interactions are emergent, feedback loops exist

**Step 3: Assess tight coupling**

- 🟢 **Loose** — Has slack, fallback, degradation path
- 🟡 **Moderate** — Limited slack, some fallback
- 🔴 **Tight** — Zero slack, no fallback, immediate cascade

**Step 4: Plot on the complexity-coupling matrix**

| | Loose | Moderate | Tight |
|---|:---:|:---:|:---:|
| **High Complexity** | ⚠️ | ⚠️ | 🔴 DANGER |
| **Medium Complexity** | ✅ | ⚠️ | ⚠️ |
| **Low Complexity** | ✅ | ✅ | ✅ |

🔴 DANGER = normal accident territory. Accidents here are features of the
system structure, not bugs.

**Step 5: Reduce risk**

- **Reduce complexity:** Simplify interactions, remove feedback loops, document emergent behavior
- **Reduce coupling:** Add slack (buffers, timeouts, retries), add fallback modes, circuit breakers
- **If both intractable:** Consider whether this architecture is fundamentally unsafe

**Key Perrow insight:** Adding safety mechanisms often INCREASES complexity.
Before adding a safety measure, ask: does this actually reduce complexity ×
coupling, or does it increase one while reducing the other?

---

## Part B: Edge Case & Boundary Testing (边界测试)

### Core Insight
Plans contain unstated range assumptions. A deployment plan assumes <1M rows.
A migration assumes all data conforms to schema. These assumptions are invisible
until they break.

### The Boundary Testing Exercise

**Step 1: Identify all parameters and their assumed ranges**

| Parameter | Assumed Range | Actual Range | What happens at extremes? |
|-----------|:-------------:|:------------:|:-------------------------:|
| Data volume | <1M | 200M | Timeout |
| Concurrent users | 100-500 | 50K | OOM |

**Step 2: Test at boundaries**

For each parameter:
- **Zero/null** — What if 0, empty, null, undefined?
- **Minimum** — What if at the lower end?
- **Maximum** — What if at the upper end?
- **Negative** — Can this go negative? What happens?
- **Extreme** — What if 10x the assumed maximum?

**Step 3: Test interactions at boundaries**

| Boundary A | Boundary B | Combined Effect |
|------------|------------|-----------------|
| High volume + | Low memory = | [what happens] |
| Network timeout + | Retry loop = | [what happens] |

**Step 4: Identify unstated assumptions**

- "What does this plan assume about [time/quantity/state/people/availability]?"
- "What must be true for this plan to work?"
- "What conditions would make every assumption false simultaneously?"

---

## Part C: Cognitive Debiasing (认知去偏)

### Origin
Daniel Kahneman, *Thinking, Fast and Slow* (2011). Amos Tversky.

### Core Insight
Human reasoning has systematic bugs. These aren't random errors — they're
predictable distortions. The good news: knowing about them lets you correct.

### The Debiasing Exercise

#### 1. Planning Fallacy (规划谬误)
Systematically underestimate time, cost, and risk.

**Correction: Reference Class Forecasting** — find 10+ similar past projects,
use their actual completion as baseline.

| Estimate Type | Inside View | Outside View (base rate) | Adjusted |
|:-------------:|:-----------:|:------------------------:|:--------:|
| Time | [our estimate] | [base rate] | [higher × 1.5] |
| Cost | [our estimate] | [base rate] | [higher × 1.3] |

**Rule of thumb:** No reference class? Multiply time by 2×, add 30% to cost.

#### 2. Anchoring (锚定效应)
The first number anchors all subsequent estimates.

**Correction:** Write independent estimate BEFORE looking at any reference.

**Check:** Was the timeline set by a deadline before anyone estimated the work?
If yes, the deadline is an anchor, not an estimate.

#### 3. Availability Heuristic (可得性启发)
Overweight vivid, recent, or emotional examples.

**Correction:** Deliberately search for **non-salient** counter-examples.
- What failures are we NOT thinking about because they weren't dramatic?
- Are we focusing on this risk just because it happened recently?

#### 4. Confirmation Bias (确认偏误)
Seek evidence that confirms existing beliefs.

**Correction:** For each key assumption, generate **3 reasons it might be wrong**
before generating reasons it might be right.

| Assumption | 3 Reasons Wrong | 3 Reasons Right | Net Assessment |
|------------|:---------------:|:---------------:|:--------------:|
| [assumption] | 1. 2. 3. | 1. 2. 3. | [revised] |

#### 5. Survivorship Bias (幸存者偏差)
We only see successes. Failures are invisible.

**Correction:** Actively seek failure data:
- "How many projects like this have failed?"
- "What happened to teams that tried this and we don't hear about?"

#### 6. Sunk Cost Fallacy (沉没成本谬误)
Continue investing because already invested, not because future returns justify it.

**Check:** If we hadn't already invested [X], would we still proceed? If NO,
we're in sunk cost territory.

#### 7. Overconfidence (过度自信)
Experts are consistently more confident than accuracy warrants.

**Check:** If you said >80% confidence, you're probably overconfident.
Calibration studies show "90% confident" predictions are correct only 60-70%.

**Correction:** Widen confidence intervals by 2×.

---

## Cross-Pollination

| Method | Finds | Misses Without Others |
|--------|-------|----------------------|
| Complexity/Coupling | Structural accidents in system design | Cognitive biases in estimates (→ Debiasing) |
| Edge Case Testing | Failures at parameter boundaries | Emergent interactions between boundaries (→ Complexity) |
| Cognitive Debiasing | Systematic distortions in reasoning | Real structural problems (→ Complexity) |

**Recommended flow:** Complexity/Coupling → Edge Cases → Debiasing