# Risk Guard

> Help people think more thoroughly and avoid unexpected failures. Structured safety review, cognitive framework switching, and resilience design — from quick risk checks to full 6-phase anticipatory thinking.

**Risk Guard** is an agentic skill that helps AI assistants think thoroughly before acting. It has two modes:

- **Quick Review** — Safety-focused risk assessment for real-world actions (travel, meetings, transactions, hazardous activities). Classify → Question → Model → Judge.
- **Full Review** — 6-phase anticipatory thinking for complex decisions (deployments, migrations, launches, project plans). Checklist → Inversion → Pre-mortem → Stress Test → Scenario Planning → Resilience.

## Three Layers of Defense

Most failures come from three sources, and each layer addresses one:

| Layer | Source | Method |
|-------|--------|--------|
| **Layer 1** | Known risks we forgot to check | Checklists |
| **Layer 2** | Blind spots in thinking | Cognitive framework switching (inversion, pre-mortem, red team, scenarios) |
| **Layer 3** | Things no one could predict | Resilience design (antifragility, graceful degradation, belief-update signals) |

Current risk assessment tools stop at Layer 1. Risk Guard covers all three.

## Quick Review

For safety-specific scenarios: travel, stranger meetings, transactions, hazardous activities.

1. **Classify** the action into scenario groups (12 categories)
2. **Ask** targeted questions (max 4 per round, only what changes the recommendation)
3. **Model** compound risk across 7 dimensions (vulnerability, exposure, friction, safeguards, reversibility, transport, uncertainty)
4. **Run risk engine** for complex cases (optional, 6+ factors)
5. **Produce** structured go/no-go judgment: Decision (green/yellow/orange/red), Why, Next Actions, Worst Outcomes, Confidence

## Full Review — 6 Phases

### Phase 1: Checklist (检查清单)
Catch every known risk. Universal checklist + scenario-specific checklists (deploy, migration, data, integration, release, config). Any 🔴 blocker must be resolved before proceeding. *Based on Gawande's checklist research (47% surgical mortality reduction).*

### Phase 2: Inversion & Precaution (逆向与预防)
What would guarantee failure? What's irreversible? Inversion exercise (Munger/Descartes), one-way door audit (Bezos), precautionary principle (Wingspread Declaration). *Flips the question to access different cognitive pathways.*

### Phase 3: Imagine Failure (想象失败)
Generate failure narratives checklists miss. Pre-mortem (Klein, ~30% more failures identified), red team thinking (military/intel), fear setting (Ferriss/Seneca) including **cost of inaction** — the uniquely powerful element.

### Phase 4: Stress Test (压力测试)
Find where the plan breaks. Complexity & coupling analysis (Perrow's Normal Accident Theory), edge case/boundary testing, cognitive debiasing (Kahneman's 7 systematic biases). *Most plans assume normal conditions. This tests extremes.*

### Phase 5: Scenario Planning (多未来场景)
The plan was built for one expected future. Test it against 4 qualitatively different ones. Identify robust actions (work across scenarios) and hedging actions (insurance for worst cases). *Based on Shell/ Schwartz scenario planning methodology.*

### Phase 6: Build Resilience (构建韧性)
Prepare for what no one can predict. Antifragile design (Taleb — get stronger from disruption), graceful degradation (Hollnagel — what breaks first, what survives last), belief-update signals (Bayesian Surprise — what observations should force plan revision). *For unknowable risks, the answer isn't prediction — it's resilience.*

## Installation

**Note:** Installation differs by platform. Commands below have been tested on the actual platforms.

### Claude Code

Add the marketplace first, then install:

```bash
# Register the marketplace
claude plugin marketplace add Laplace-bit/risk-guard

# Install the plugin
claude plugin install risk-guard@risk-guard-dev
```

Or use `--plugin-dir` for a local session:
```bash
claude --plugin-dir /path/to/risk-guard
```

Restart Claude Code to activate.

### Gemini CLI

```bash
gemini extensions install https://github.com/Laplace-bit/risk-guard
```

Or link a local clone for development:
```bash
git clone https://github.com/Laplace-bit/risk-guard.git
gemini extensions link ./risk-guard
```

Update:
```bash
gemini extensions update risk-guard
```

### OpenAI Codex CLI

Manual install via symlink:
```bash
git clone https://github.com/Laplace-bit/risk-guard.git ~/.codex/risk-guard
mkdir -p ~/.agents/skills
ln -s ~/.codex/risk-guard ~/.agents/skills/risk-guard
```
Restart Codex. See [`.codex/INSTALL.md`](.codex/INSTALL.md) for details.

### Hermes Agent

```bash
git clone https://github.com/Laplace-bit/risk-guard.git ~/.hermes/skills/risk-guard
```
Hermes auto-discovers skills from `~/.hermes/skills/`. Restart if needed.

### OpenCode

Add to your `opencode.json`:
```json
{
  "plugin": ["risk-guard@git+https://github.com/Laplace-bit/risk-guard.git"]
}
```
To pin a version:
```json
{
  "plugin": ["risk-guard@git+https://github.com/Laplace-bit/risk-guard.git#v2.0.2"]
}
```
See [`.opencode/INSTALL.md`](.opencode/INSTALL.md) for details.

### Cursor & GitHub Copilot

Installation commands for these platforms have not been tested yet. The configuration files are included (`.cursor-plugin/`) but we recommend waiting for marketplace availability. If you test them, please open an issue with your results.

### Verify Installation

Ask your agent: *"Tell me about your risk-guard skill"* — it should describe both Quick Review and Full Review modes.

## Risk Engine

The included Python risk engine provides structured scoring for Quick Review:

```bash
python scripts/risk_engine.py --input case.json
```

Example case:
```json
{
  "scenario_tags": ["workplace_or_site_visit", "health_sensitive_activity"],
  "vulnerability_tags": ["possible_pregnancy", "fatigue"],
  "exposure_tags": ["chemical", "long_walking", "heat"],
  "counterparty_tags": [],
  "safeguard_tags": ["can_exit_independently"],
  "constraint_tags": ["poor_medical_access"],
  "transport_tags": [],
  "anticipatory_tags": [],
  "cognitive_bias_tags": [],
  "anticipatory_safeguard_tags": []
}
```

Output:
```json
{
  "score": 33,
  "level": "red",
  "level_label": "🔴 High risk. Do not proceed as described.",
  "reasons": [
    "chemical (+6)",
    "fatigue (+2)",
    "heat (+3)",
    "long_walking (+3)",
    "possible_pregnancy (+5)",
    "poor_medical_access (+4)",
    "can_exit_independently (-3)"
  ],
  "triggered_rules": [
    "pregnancy-sensitive vulnerability combined with hazardous exposure (+8)"
  ]
}
```

## Running Tests

```bash
python tests/test_risk_engine.py
```

## Skill Structure

```
risk-guard/
├── SKILL.md                          # Main skill: Quick Review + Full Review 6-phase workflow
├── CLAUDE.md                         # Claude Code context reference
├── GEMINI.md                         # Gemini context reference
├── package.json                       # Package metadata
├── LICENSE                            # Apache 2.0 License
├── README.md                          # This file
├── agents/
│   └── risk-reviewer.md              # Agent persona for deep safety review
├── commands/
│   ├── analyze.md                    # /risk-guard analyze command
│   └── check.md                      # /risk-guard check command
├── hooks/
│   ├── hooks.json                    # Claude Code hooks
│   ├── hooks-cursor.json             # Cursor hooks
│   ├── session-start                 # Session startup hook
│   └── run-hook.cmd                  # Hook runner script
├── references/
│   ├── scenario-map.md               # 12 scenario groups with triggers
│   ├── question-bank.md              # High-yield follow-up questions
│   ├── risk-taxonomy.md              # Risk levels, compound logic, red flags
│   ├── output-examples.md            # Complete output examples (Quick Review)
│   ├── risk-engine-schema.md         # Full tag reference for risk engine
│   ├── checklists.md                # Phase 1: universal + scenario checklists
│   ├── inversion-and-precaution.md   # Phase 2: inversion, one-way doors, precaution
│   ├── premortem-redteam-fearsetting.md  # Phase 3: pre-mortem, red team, fear setting
│   ├── stress-test.md               # Phase 4: complexity/coupling, edge cases, debiasing
│   ├── scenario-planning.md         # Phase 5: 4-scenario matrix, robust & hedging
│   └── resilience-building.md       # Phase 6: antifragility, degradation, signals
├── scripts/
│   └── risk_engine.py                # Scoring engine (Python 3)
├── tests/
│   └── test_risk_engine.py          # Test suite
├── .claude-plugin/
│   ├── plugin.json                   # Claude Code plugin metadata
│   └── marketplace.json              # Claude marketplace config
├── .codex/
│   └── INSTALL.md                    # Codex installation guide
├── .cursor-plugin/
│   └── plugin.json                   # Cursor plugin metadata
├── .opencode/
│   ├── INSTALL.md                    # OpenCode installation guide
│   └── plugins/                      # OpenCode plugin directory
└── .github/
    └── ...                           # Issue templates, funding, etc.
```

## Scientific Foundation

| Phase | Method | Origin |
|-------|--------|--------|
| Phase 1 | Checklists | Atul Gawande, *The Checklist Manifesto* |
| Phase 2 | Inversion | Charlie Munger / Descartes' Method of Doubt |
| Phase 2 | Precautionary Principle | Wingspread Declaration (1998) |
| Phase 3 | Pre-mortem | Gary Klein, prospective hindsight research (~30% more failures identified) |
| Phase 3 | Red Teaming | US Army Red Team Handbook (2005) |
| Phase 3 | Fear Setting | Tim Ferriss / Stoic *premeditatio malorum* |
| Phase 4 | Normal Accident Theory | Charles Perrow (1984) |
| Phase 4 | Cognitive Debiasing | Daniel Kahneman, *Thinking, Fast and Slow* (2011) |
| Phase 5 | Scenario Planning | Peter Schwartz / Royal Dutch Shell (1991) |
| Phase 6 | Antifragility | Nassim Nicholas Taleb (2012) |
| Phase 6 | Resilience Engineering | Erik Hollnagel (2006) |
| Phase 6 | Bayesian Surprise | Itti & Baldi (2006) |

## Compatibility

| Platform | Support Level | Method |
|----------|--------------|--------|
| Claude Code | ✅ Full | Plugin + SKILL.md |
| OpenAI Codex CLI | ✅ Full | Skill discovery + SKILL.md |
| OpenCode | ✅ Full | Plugin system |
| Cursor | ✅ Full | Plugin + hooks |
| Gemini | ✅ Full | Extension + context file |
| Hermes Agent | ✅ Full | Native skill directory |
| Windsurf | ✅ SKILL.md | Context file |
| Kiro | ✅ SKILL.md | Context file |
| Any MCP-compatible agent | ✅ SKILL.md | Context file |

## Design Principles

1. **Three-layer defense** — Checklists catch known risks, framework switching catches blind spots, resilience catches the unknowable
2. **Quick when possible, thorough when needed** — Quick Review for safety checks, Full Review for complex decisions
3. **Compound risk over isolated risk** — Moderate factors that combine get escalated
4. **Prefer false positives** — When downside is irreversible, conservative beats optimistic
5. **Structured over vague** — Green/yellow/orange/red decisions, not "be careful"
6. **Minimal questions** — Only ask what could change the recommendation
7. **Scientifically grounded** — Every phase has peer-reviewed cognitive science research behind it
8. **No medical/legal conclusions** — Risk reasoning and precautionary guidance only

## Contributing

Contributions are welcome! Please read the skill content carefully before submitting changes — the risk taxonomy, escalation heuristics, and cognitive methods are intentionally grounded in peer-reviewed research.

## License

Apache 2.0