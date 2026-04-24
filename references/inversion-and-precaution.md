# Phase 2: Inversion & Precaution (逆向与预防)

Two methods that flip the default thinking direction:
- **Inversion** flips "how do I succeed?" to "what would guarantee failure?"
- **Precautionary Principle** flips "prove it's dangerous" to "prove it's safe"

Both attack the same fundamental bias: we naturally think about what we want,
not what we don't want. By reversing the question, we access different
cognitive pathways and see things forward-thinking misses.

---

## Part A: Inversion (逆向思维)

### Origin
Charlie Munger (after Carl Gustav Jacob Jacobi): "Invert, always invert."
René Descartes' Method of Doubt: systematically doubt everything that *can*
be doubted to find what's certain.

### Core Principle
Instead of asking "how do I succeed?", ask "what would absolutely guarantee
failure?" — then make sure none of those conditions exist.

This works because **the exclusion set (what's definitely bad) is often easier
to define than the inclusion set (what's good)**. There are more ways to fail
than to succeed, but the guaranteed-failure conditions are surprisingly
specific and actionable.

### The Inversion Exercise

**Step 1: Define the goal clearly**

Write one sentence: "Success looks like [specific outcome]."

**Step 2: Invert the goal**

"Complete failure looks like [specific failure]." — This is NOT the opposite
of success, it's a vivid, specific description of the worst realistic outcome.

**Step 3: List guaranteed-failure conditions**

For the plan/decision at hand, list 10+ specific behaviors, conditions, or
choices that would make success impossible. Be concrete:

| # | Guaranteed Failure Condition | Present in Plan? | How to Eliminate |
|---|-------------------------------|:-----------------:|-----------------|
| 1 | [specific condition] | ✅/❌ | [action] |

Categories to check:
- **Resource failure** — insufficient time, money, people, compute
- **Dependency failure** — critical dependency unavailable or broken
- **Communication failure** — wrong people informed, wrong timing, missing context
- **Assumption failure** — key assumption about state, behavior, or timing is wrong
- **Skill failure** — nobody on the team has the expertise needed
- **Tool failure** — required tools don't work as expected
- **Priority failure** — competing priorities pull resources away
- **Morale failure** — team burnout, motivation loss, conflict

**Step 4: Method of Doubt**

For each key assumption, ask: "What if this is wrong?"

If the plan survives the assumption being wrong → low concern.
If the plan collapses when the assumption is wrong → this assumption is a
**linchpin** and needs extra validation.

| Assumption | If Wrong, Impact | Validated? | Validation Method |
|------------|-----------------:|:----------:|-------------------|
| [assumption] | [impact] | ✅/❌ | [how to verify] |

**Step 5: Identify death zones**

A **death zone** is a state from which recovery is impossible or
disproportionately costly. These are different from risks — risks have
probability, death zones are about structural irreversibility.

Examples:
- Data deleted without backup
- Public key committed to git
- Irreversible database migration committed
- Contract signed without review clause
- Production config overwritten with no version control

| Death Zone | Why Irreversible | Present in Plan? | Guard Rail |
|------------|------------------|:----------------:|------------|
| [zone] | [reason] | ✅/❌ | [prevention] |

---

## Part B: Precautionary Principle (预防原则)

### Origin
Wingspread Declaration (1998): "When an activity raises threats of serious or
irreversible harm, lack of full scientific certainty shall not be used as a
reason for postponing cost-effective measures to prevent the harm."

### Core Principle
When harm is **irreversible**, the cost of a false negative (underestimating
risk) is MUCH higher than the cost of a false positive (overestimating risk).
The burden of proof shifts: instead of "prove it's dangerous," require
"prove it's safe."

This does NOT mean "don't do anything risky." It means: **when consequences
are irreversible, the standard of evidence for safety must be higher.**

### One-Way Door Audit (Jeff Bezos)

A **one-way door** is a decision that's hard or impossible to reverse.
For each decision point in the plan:

1. **Identify** — Is this reversible? How long would reversal take? At what cost?
2. **Classify:**
   - 🟢 **Two-way door** — Easy to reverse. Decide quickly, iterate.
   - 🟡 **Narrow door** — Reversible but costly. Decide carefully.
   - 🔴 **One-way door** — Irreversible or recovery is prohibitive. Decide slowly, with maximum evidence.
3. **For 🔴 one-way doors**, apply elevated scrutiny:
   - Require proof of safety, not proof of danger
   - Add a mandatory waiting period (sleep on it)
   - Get second opinion from uninvolved person
   - Validate with the smallest possible experiment first
   - Document the decision rationale

| Decision Point | Door Type | Reversal Cost | Evidence Required |
|---------------|:---------:|:--------------:|:-----------------:|
| [decision] | 🟢/🟡/🔴 | [time/cost] | [standard/elevated] |

### Asymmetry Matrix

For each action, classify the cost balance:

| Action | If wrong, can we undo? | Cost of false negative | Cost of false positive | Asymmetry |
|--------|:----------------------:|:----------------------:|:----------------------:|:---------:|
| [action] | Yes/No | [underestimate risk] | [overestimate risk] | High/Low |

**High asymmetry** = false negative cost >> false positive cost → flip burden of proof.

### Minimum Safe Regret

When uncertainty is high, choose the option whose **worst case is least
catastrophic** (minimax regret).

| Option | Best Case | Worst Case | Worst Case Severity | Minimax? |
|--------|:---------:|:----------:|:-------------------:|:--------:|
| [A] | [good] | [bad] | [severity] | |
| [B] | [great] | [terrible] | [severity] | |
| [C] | [ok] | [not great] | [lowest severity] | ← |

---

## Integration Notes

- Inversion is the most practically actionable phase: "avoid known bad" is
  easier than "predict unknown good."
- Precaution is critical when the plan contains **irreversible actions**.
- Both methods complement each other: inversion finds specific failure
  conditions, precaution evaluates the asymmetry of consequences.