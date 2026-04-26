# Release Notes

## v3.0.0 (2026-04-26)

### What Changed

**Complete redesign: from analysis framework to risk sentinel.**

The old 6-phase analysis workflow assumed users would ask for risk assessment. Reality: people don't ask — they need to be reminded at the right moment. Risk Guard v3 is now a **proactive sentinel**, not a reactive analysis tool.

**Key changes:**

- **L0 Quick Reminder** (default): 5 sentences max, 1-3 key risks + 1 actionable suggestion. No 6-phase analysis unless explicitly requested.
- **19 scenario categories** with clear trigger conditions and compound-risk patterns
- **Progressive disclosure**: L0 (quick reminder) → L1 (scenario checklists) → L2 (6-phase deep analysis)
- **Proactive triggering**: flag risks when users mention travel, meetings, transactions, health decisions — don't wait for them to ask
- **Red Flags table**: must-respond phrases like "应该没事", "就去一趟", "以前都没事"
- **Compound risk emphasis**: single factors are manageable; combinations are where real danger lives
- **All reference files preserved** for deep analysis, but not loaded by default
- **Version bump**: 2.1.0 → 3.0.0 (breaking change in core behavior)

## v2.1.0 (2026-04-25)

### What's New

**18 safety scenario checklists** — The PRIMARY checklists are now organized around real-life risk scenarios, not just technical operations:
- ✈️ Travel & mobility, 👤 Stranger meeting, 💰 Transaction & payment
- 🏕️ Outdoor & environment, 🌙 Nightlife & isolated time, 🏥 Health-sensitive activity
- 👶 Caregiving & dependent, 🏠 Housing & property, 💻 Digital fraud & phishing
- 🏢 Business trip, 🌐 Online-to-offline
- 🏭 Workplace & site visit, 💼 Job interview & onboarding
- 🏥 Medical visit & decision, 🌊 Natural disaster response
- 🏠 Home & family safety, 🤝 Job scam & exploitation
- 🏋️ Sports & fitness, 🔧 Home service & renovation

**20 scenario groups** (was 12) — New: workplace visit, job interview, medical decision, natural disaster, home safety, job scam, sports & fitness, home service.

**10 new risk tags** — `extreme_exertion`, `altitude`, `deep_water`, `construction_hazard`, `formaldehyde_fumes`, `unverified_organization`, `upfront_fee_required`, `document_confiscation`, `movement_restriction` + 5 new safeguards.

**4 new compound rules** — Document confiscation + movement restriction (trafficking signal), upfront fee + unverified org (scam pattern), extreme exertion + hazardous environment, formaldehyde + vulnerable person.

**SKILL.md restructured** — Slimmed from 363 → 170 lines following superpowers skill pattern:
- Iron Law: "NO PLAN EXECUTION WITHOUT RISK REVIEW WHEN STAKES ARE REAL"
- Red Flags table (7 rationalization patterns and their reality)
- Kill Assumption step added after Phase 3
- Progressive disclosure: output formats and detailed tables moved to references
- Trigger-only description for better activation

**Risk engine v2.1** — `--stdin` flag, `--format` (json/markdown/plain), `scenario_tags` base weighting, unknown tag warnings, `free_text` warning, compound rule trigger details.

**43 tests** (was 21) — New tests for v2.1 tags, compound rules, stdin, format, error paths, boundary values, absence rules.

**Bug fixes** — License unified to MIT (was inconsistent), Cursor plugin skills path fixed, OpenCode version pin fixed.

---

## v2.0.2 (2026-04-24)

### What's New
- **Full Review 6-phase workflow** — Complete anticipatory thinking from checklists to resilience design
- **Quick Review risk engine** — Structured scoring with Python risk engine (`scripts/risk_engine.py`)
- **21-test test suite** — 5 new safeguard tests (travel, fraud, PPE, deployment, combination)
- **Universal installation** — Claude Code / Gemini / Codex / Cursor / Hermes / Windsurf / OpenCode / any MCP agent
- **Schema docs** — Full risk engine tag reference and transport tags
- **Full Review output example** — Complete 6-phase demonstration case

### Security
- No security fixes (first stable release)
- `.env` / secrets excluded from git

### Compatibility
| Platform | Status | Method |
|----------|--------|--------|
| Claude Code | ✅ Full | Plugin + marketplace |
| Gemini CLI | ✅ Full | Extension |
| OpenAI Codex CLI | ✅ Full | Symlink + skill discovery |
| Cursor | ✅ Plugin | Plugin manifest |
| Hermes Agent | ✅ Full | Native skill directory |
| OpenCode | ✅ Full | Plugin system |
| Windsurf | ✅ Context | SKILL.md |
| Any MCP agent | ✅ Context | SKILL.md |

### Install / Upgrade
```bash
# Hermes (recommended for testing)
git clone https://github.com/Laplace-bit/risk-guard.git ~/.hermes/skills/risk-guard

# Claude Code
claude plugin marketplace add Laplace-bit/risk-guard
claude plugin install risk-guard@risk-guard-dev

# Gemini
gemini extensions install https://github.com/Laplace-bit/risk-guard

# Codex (manual)
git clone https://github.com/Laplace-bit/risk-guard.git ~/.codex/risk-guard
mkdir -p ~/.agents/skills && ln -s ~/.codex/risk-guard ~/.agents/skills/risk-guard
```

See [README.md](README.md) for full platform-specific instructions.

### Known Issues
- Cursor / GitHub Copilot install commands untested (marked in README)
- No auto-update mechanism for non-marketplace platforms (re-clone recommended)

---

## v2.0.0 (2026-04-22)

Initial v2.0 release. Dual-mode architecture: Quick Review + Full Review 6-phase.
