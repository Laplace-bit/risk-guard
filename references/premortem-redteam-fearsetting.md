# Phase 3: Imagine Failure (想象失败)

Three methods that generate failure narratives checklists miss:
- **Pre-mortem** — Assume failure happened, reverse-engineer why (Klein)
- **Red Teaming** — Adopt adversarial perspective, destroy the plan (military/intel)
- **Fear Setting** — Articulate specific fears + cost of inaction (Ferriss/Stoic)

All three exploit the same insight: **imagining a specific failure activates
different cognitive pathways than imagining possible risks.** Research shows
prospective hindsight (telling people an event *happened* vs. *might happen*)
increases causal reasoning by ~30%.

---

## Part A: Pre-Mortem (事前验尸)

### Origin
Gary Klein (2007), based on prospective hindsight research (Mitchell, Russo,
Pennington 1989). Used by DARPA, FBI, and high-reliability organizations.

### Core Exercise

**Imagine you are reading a post-mortem 3 days from now. The headline is:
"[Plan Name] Failed Completely."**

Now explain WHY it failed.

### Step-by-Step

**Step 1: Generate failure narratives**

Write 5-8 specific, vivid stories explaining what went wrong. Not vague
("things went wrong") but concrete ("the migration script hit an undocumented
foreign key at row 47M, locked both tables for 20 minutes, and the application
timeout killed all active sessions").

For each narrative, assess:
- **Likelihood:** high / medium / low
- **Severity:** irreversible data loss / service down / recoverable / embarrassing
- **Detectability:** can we see it coming before it cascades?
- **Preventability:** could we prevent it with a specific action right now?

| # | Failure Narrative | Likelihood | Severity | Detectable? | Early Signal |
|---|------------------|:----------:|:--------:|:-----------:|-------------|
| 1 | [story] | H/M/L | [level] | Yes/No | [signal] |

**Step 2: Find the "nobody saw it coming" narrative**

Among the 5-8 narratives, one should be deliberately surprising — the failure
mode that's NOT a variant of commonly discussed risks. Ask:

- "What's the failure that has nothing to do with what we've been discussing?"
- "What would a completely different type of engineer point out?"
- "What could go wrong that's not a technical failure?" (people, process, timing)

**Step 3: Identify early warning signals**

For each failure narrative, define: **what observable event would tell you this
failure is starting to happen?** The signal must be:
- Specific (not "things seem off")
- Measurable (has a threshold or comparison)
- Available before the failure cascades
- Something you could monitor automatically

**Step 4: Rank by (likelihood × severity × undetectability)**

The most dangerous failures are not the most likely or most severe — they're
the ones that combine likelihood, severity, AND invisibility until it's too late.

Top 3 ranked failures → these become the primary guardrails.

---

## Part B: Red Teaming (红队思维)

### Origin
Military and intelligence tradition. Institutionalized dissent. Formalized
in US Army Red Team Handbook (2005), UK MOD Red Teaming Guide.

### Core Principle
Adopt a dedicated adversarial perspective. The goal is NOT to find balanced
pros/cons — it's to **try to break the plan**. A plan that survives a red
team attack is genuinely robust.

### The Red Team Exercise

**Assume the role of someone who WANTS this plan to fail.**

**Challenge 1: Assumption attack**

For each key assumption, argue the opposite:

| Assumption | "What if the opposite were true?" | Consequence | Plan survives? |
|------------|-----------------------------------|-------------|:--------------:|
| [assumption] | [opposite] | [what happens] | Yes/No |

**Challenge 2: Adversarial exploitation**

"If someone wanted this plan to fail, what would they target?"
- What's the single weakest point?
- What's the most tightly-coupled dependency?
- What would a competitor/adversary do to exploit this?
- What's the simplest way to cause maximum damage?

**Challenge 3: Steel-man counter-arguments**

For each key decision, find the **strongest** version of the opposing argument:
- "The best reason NOT to do this is..."
- "The most credible person who would object would say..."
- "The most likely valid criticism is..."

**Challenge 4: Organizational blind spots**

- Who benefits from the plan proceeding? (check incentive bias)
- Who would lose from the plan? (check resistance/sabotage risk)
- Who was NOT consulted but should have been? (check stakeholder coverage)
- What does nobody want to talk about? (check social taboos/elephants)

---

## Part C: Fear Setting (恐惧设定)

### Origin
Tim Ferriss (2015), based on Stoic *premeditatio malorum* (Seneca).

### Core Principle
Vague fears paralyze. Specific fears empower. By articulating exactly what you
fear — and the cost of doing nothing — you convert anxiety into action.

### The Fear Setting Exercise

**Step 1: Define — What is the worst that could specifically happen?**

| # | Specific Fear | Severity (1-10) | Likelihood (1-10) | Permanence (1-10) |
|---|---------------|:----------------:|:------------------:|:-----------------:|
| 1 | [exact outcome] | | | |

**Step 2: Prevent — What specific step would reduce likelihood?**

| Fear | Prevention Action |
|------|-------------------|
| [fear] | [specific, actionable step] |

**Step 3: Repair — If it happens, what specific step would recover?**

| Fear | Repair Action |
|------|---------------|
| [fear] | [specific recovery step] |

**Step 4: Inaction Cost — What happens if we do NOTHING?**

This is the uniquely powerful element. People fear action risks but ignore
inaction risks.

| Timeframe | Cost of Inaction |
|-----------|-----------------|
| 1 month | [what happens] |
| 6 months | [what happens] |
| 1 year | [what happens] |
| 3 years | [what happens] |

**Step 5: Decide**

Given specific fears (with prevention + repair) + cost of inaction:
Usually the cost of inaction is underestimated and the cost of action is
overestimated — the rational choice is often to act, with guardrails.

---

## Cross-Pollination

| Method | Unique Contribution | Gaps Filled by Others |
|--------|--------------------|-----------------------|
| Pre-mortem | Reverse-engineers specific failure causes | May miss adversarial exploitation (→ Red Team) |
| Red Team | Finds the weakest point under attack | May miss personal/emotional fears (→ Fear Setting) |
| Fear Setting | Makes inaction cost explicit | May miss structural/systemic failures (→ Pre-mortem) |

**Recommended flow:** Pre-mortem → Red Team → Fear Setting
(Structural → Adversarial → Personal)