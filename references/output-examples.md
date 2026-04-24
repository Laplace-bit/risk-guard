# Output Examples

## Example 1: Pregnancy Plus Chemical Site Visit

### Situation summary
A user who may be in early pregnancy is planning to visit a chemical plant for work tomorrow.

### What I found automatically
No independent search was performed for this case.

### Decision
Red — I would not do this as currently described.

### Why this is risky
- Possible early pregnancy changes the tolerance for chemical and exertion exposure.
- A plant visit combines uncertain exposure with prolonged walking and limited control over the environment.
- The downside is high and hard to reverse even if the probability is not high.

### Missing critical facts
- Exact gestational status and any clinician restrictions
- Confirmed chemicals and exposure controls
- Expected walking/standing load and ability to opt out on site

### Best next actions
1. Avoid entering the site until pregnancy status and exposure controls are clarified.
2. Ask for the site's hazard list and PPE requirements in writing.
3. Replace the visit with remote participation or a delegate if possible.
4. If attendance is still discussed, get clinician input before going.

### Worst credible outcomes
Pregnancy harm, acute illness from exposure, overexertion with delayed medical access.

### Confidence
Medium — the exact exposure is unknown, but the downside is serious enough to justify a conservative judgment.

---

## Example 2: Deposit Before Viewing a Rental

### Situation summary
A user is being asked to send a deposit before viewing a rental property, with pressure to act quickly.

### What I found automatically
No independent search was performed for this case.

### Decision
Orange — Do not send money yet.

### Why this is risky
- Asking for money before a normal viewing flow is a classic fraud pattern.
- The payment may be hard to recover.
- Urgency reduces your chance to verify ownership and authority.

### Missing critical facts
- Whether ownership or agency authority was verified independently
- Payment method and reversibility

### Best next actions
1. Verify the property and the person through an independent channel.
2. Refuse deposits before a legitimate viewing and documented agreement.
3. Keep all communication in writing.
4. Walk away if urgency or secrecy increases.

### Worst credible outcomes
Deposit loss, identity misuse, repeated payment requests.

### Confidence
High — the pattern itself is a strong warning sign.

---

## Example 3: Solo Late-Night Rideshare

### Situation summary
A user plans to take a rideshare alone late at night to an unfamiliar area.

### What I found automatically
No independent search was performed for this case.

### Decision
Yellow — Proceed with added safeguards.

### Why this is risky
- Solo late-night travel increases vulnerability if the ride goes off-route.
- Limited transit fallback if you need to exit mid-trip.
- Phone and location sharing are unconfirmed.

### Missing critical facts
- Whether you have a charged phone and live location sharing enabled
- Whether someone is expecting you at a specific time

### Best next actions
1. Share your trip details and live location with a trusted contact.
2. Confirm the driver and vehicle match the app before getting in.
3. Keep your phone charged and accessible during the ride.
4. If anything feels off, ask to be dropped at a well-lit public location.

### Worst credible outcomes
Stranded in an unfamiliar area, targeted robbery, limited recourse if the driver deviates.

### Confidence
Medium — standard precautions reduce most risk, but late-night solo travel always carries more exposure.

---

## Example 4: Business Trip to a Chemical Plant

### Situation summary
A user is traveling domestically for three days to visit a chemical manufacturing plant in an industrial corridor, staying at a nearby hotel and entering the production floor daily.

### What I found automatically
- Weather forecast for the area shows heat advisory (38 °C / 100 °F) on the visit dates.
- Local news reports a minor chemical release at the same facility eight months ago, no injuries reported.
- The industrial corridor is 25 minutes from the nearest hospital by car.

### Decision
Orange — Proceed only after confirming exposure controls and medical access; do not enter the production floor unprotected.

### Why this is risky
- Heat advisory plus mandatory PPE (likely heavy, non-breathable) on the production floor raises heat illness risk substantially.
- Previous chemical releases at the site indicate a non-trivial baseline exposure probability.
- Distance to emergency medical care adds friction if acute exposure or heat illness occurs on site.

### Missing critical facts
- Whether the host company provides site-specific hazard orientation and appropriate PPE
- Whether the user has any respiratory, cardiac, or heat-sensitivity conditions
- Whether the user will have a rental car or depend on site transportation

### Best next actions
1. Request the facility's current hazard list, exposure controls, and PPE requirements in writing before travel.
2. Confirm on-site medical resources and the exact route/time to the nearest hospital.
3. Rent a car rather than depending on shuttles, so you can leave immediately if needed.
4. Hydrate aggressively and schedule plant floor time for early morning only during the heat advisory.
5. Tell a colleague or family member your daily itinerary and check in at set times.

### Worst credible outcomes
Acute chemical exposure with delayed medical response, severe heat illness on the production floor, extended isolation without transport if something goes wrong.

### Confidence
Medium — the site's hazard controls are unknown; the heat advisory and past release are verifiable compounding factors that push the level up.

---

## Example 5: Digital Fraud / Phishing Risk

### Situation summary
A user received an urgent email appearing to be from their bank, asking them to click a link and verify account credentials within 24 hours or face account suspension.

### What I found automatically
- The sender domain does not match the bank's official domain (uses a lookalike with an extra hyphen).
- No record of widespread alerts for this bank today, but domain-spoof phishing campaigns targeting this bank have been reported in the past month.
- The linked URL shortener obscures the true destination.

### Decision
Red — Do not click the link or enter any credentials.

### Why this is risky
- Urgency ("suspension within 24 hours") and domain mismatch are textbook phishing indicators.
- Entering credentials on a spoofed site gives attackers direct access to financial accounts and potentially broader identity theft.
- The obscured URL removes the last easy verification a user could perform.

### Missing critical facts
- Whether the user has Multi-Factor Authentication enabled on the real banking account
- Whether the user has already clicked the link on any device

### Best next actions
1. Do not click the link or open it in any browser.
2. Log in to your bank directly through its official app or by typing the known URL — do not use any link from the email.
3. If you already clicked the link, immediately change your bank password from a clean device and enable MFA.
4. Forward the email to your bank's fraud address and delete it.
5. Monitor your account for unauthorized transactions over the next 72 hours.

### Worst credible outcomes
Bank account drained, identity theft enabling credit fraud, credential reuse exposing other accounts.

### Confidence
High — the domain mismatch and urgency pattern are unambiguous phishing signals.

---

## Full Review Example: Production Database Migration

### 🧠 Risk Guard — Full Review

**Plan:** Migrate production PostgreSQL (500 GB, ~200 concurrent users) to MySQL this weekend. Estimated downtime: 4 hours on Saturday. Rollback plan exists but only tested in staging.

---

**Phase 1 — Checklist:**

| Item | Status | Note |
|------|:------:|------|
| Rollback path tested? | ⚠️ | Tested in staging only. Production scale is 10x larger. |
| Database migration reversible? | 🔴 | Schema differences (JSONB, arrays, CTEs) — some transformations may not reverse cleanly. |
| Feature flags in place? | ✅ | Kill switch can redirect read traffic back to PostgreSQL. |
| Monitoring and alerts set up? | ⚠️ | Key metrics defined but no baseline for MySQL performance under full production load. |
| Write path dual-run tested? | ⚠️ | Dual-write tested for 48h in staging. Production dual-write not possible due to connection limits. |
| Migration script tested at scale? | 🔴 | Tested with 1 GB (0.2% of production data). 500 GB behavior untested. |
| Data comparison plan exists? | ✅ | Row count + checksum comparison script ready. But no test at 500 GB. |
| Stakeholders notified? | ✅ | Team aware, maintenance window approved. |

**Checklist verdict:** 2 🔴 blockers + 3 ⚠️ risks. Migration should not proceed as described.

---

**Phase 2 — Death zones & one-way doors:**

- **Death zone (🔴):** Schema transformation errors on JSONB columns — PostgreSQL JSONB data type has no direct MySQL equivalent. Lossy conversion of nested JSON operations may silently corrupt data with no detection signal.
- **Death zone (🔴):** Foreign key cascade path change — the production app uses 17 FK cascades. A single FK mapping mismatch in the migration script could orphan data across 4+ tables.
- **One-way door (🔴):** ETL cutover — once app writes switch to MySQL, the PostgreSQL instance has new data that was never in MySQL. Rolling back means 4+ hours of lost writes.
- **One-way door (🟡):** Migration script running in production with no pause point — 4-hour script can't be stopped mid-way without risking partial migration state.

**Linchpin assumption:** "The 1 GB test accurately predicts 500 GB behavior." — If wrong, the migration takes 12+ hours instead of 4, exceeding the maintenance window.

---

**Phase 3 — Failure hypotheses:**

| # | Failure Narrative | Likelihood | Severity | Detectable? | Early Signal |
|---|------------------|:----------:|:--------:|:-----------:|-------------|
| 1 | Migration script hits unindexed FK at row 300M, locks both tables for 40 minutes, app timeout cascades | High | Data corrupt | No | No — lock is invisible until it happens |
| 2 | JSONB → TEXT conversion silently drops nested data in 12% of records; data inconsistency found 3 days post-migration | Medium | Data loss | No | No — silent transformation |
| 3 | MySQL connection pool is 1/4 of PostgreSQL's; under post-migration peak load, connections queue up and health checks fail | Medium | Service down | Partial | Connection wait times increase before failure |

- **Inaction cost:** Not migrating means ongoing PostgreSQL licensing cost + increasing maintenance burden as data grows. But rushing the migration risks data loss that would set the project back 6+ months.

---

**Phase 4 — Fragility map:**

| Component | Fragile Under | Condition |
|-----------|--------------|-----------|
| Schema migration script | Data volume 10x tested | 500 GB → memory exhaustion |
| JSONB conversion | Any non-ASCI JSON structure | 12% records affected |
| Write path cutover | Rollback needed after MySQL receives data | 4+ hours data loss |
| Team | Only 1 person knows PostgreSQL schema details | Bus factor = 1 |

**Debiased estimates:**
| Estimate | Inside View | Outside View (base rate) | Adjusted |
|:--------:|:-----------:|:------------------------:|:--------:|
| Migration time | 4 hours | Similar DB migrations: 6-14 hours (N=8 orgs) | 8-12 hours |
| Success rate | "90% confident" | Industry DB migration: ~65% first-attempt success | 50-65% |
| Data integrity | "We'll catch issues" | Silent data loss found in ~30% of post-migration audits | 30% chance of undetected issues |

---

**Phase 5 — Scenario test:**

| Scenario | Plan works? | Fragile points |
|----------|:-----------:|---------------|
| 🚀 **"Smooth Sailing"** — Schema maps cleanly, no edge cases, script finishes in 3.5h | ✅ | Works but no room for error |
| 💥 **"The Hidden Schema"** — Production has undocumented FK triggers, migration fails at 65% | ❌ | No incremental checkpoint; total restart needed |
| 🐌 **"Slow Burn"** — 500 GB takes 11 hours, maintenance window expires at 6h, team decides to abort mid-migration | ❌ | No pause-and-rollback point; partial state is unrecoverable |
| 🏥 **"Silent Corruption"** — Migration completes on time but JSONB conversion corrupted 5% of user profile data | ⚠️ | No automated data quality check post-migration; corruption detected by user support tickets 48h later |

**Robust actions:** Add migration checkpoints at every 25% and validate data integrity incrementally.
**Hedging actions:** Keep both DBs running for 7 days post-cutover; maintain read-traffic redirect to PostgreSQL as safety valve.

---

**Phase 6 — Resilience:**

- **Antifragile moves:** After migration, rebuild the schema comparison tool as a reusable framework — it gets stronger with each migration experience. Consider this the first of many.
- **Graceful degradation:** If MySQL becomes read-only under load, keep PostgreSQL read replica online as fallback for read queries (degraded but functional).
- **Watch signals:**
  - 🟢 **Green:** First 10% of data migrates in <30 min, no FK errors
  - 🟡 **Yellow:** Per-100GB migration time >50 min → escalate, consider pausing at next checkpoint
  - 🔴 **Red:** Any FK violation or data type error → STOP migration immediately, revert to PostgreSQL
- **Recommended slack:** Add 2 extra hours to maintenance window (6h instead of 4). Assign a second engineer to monitor MySQL connection pool live.

---

**Blind spot alert:** Nobody tested the migration script against production's actual index configuration. Staging indexes are a simplified subset. A missing composite index on the order_history table (120M rows) could turn a 10-second query into a 30-minute full table scan — inside the migration transaction.

**Recommended guardrails (top 5):**
1. 🔴 **Do NOT migrate without running the script against a production-size data sample** — even a partial snapshot (50 GB) would catch the volume issue
2. 🔴 **Add incremental checkpoints** — migration should be resumable, not all-or-nothing
3. 🟡 **Dual-write for 7 days post-migration** — keeps PostgreSQL as a true fallback, not a theoretical one
4. 🟡 **Run automated data quality checks immediately post-migration** — row count + checksum + 5% random sample deep-compare
5. 🟡 **Assign a named second engineer** — bus factor < 2 is unacceptable for an irreversible operation of this scale