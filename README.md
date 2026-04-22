# Risk Guard

> Analyze planned real-world actions for low-probability high-impact risks. Structured safety review with compound risk modeling, targeted questions, and go/no-go judgments.

**Risk Guard** is an agentic skill that helps AI assistants provide structured safety reviews when users describe something they're about to do in real life — traveling, meeting strangers, visiting hazardous sites, making transactions, or any action where "probably fine" isn't good enough.

It's built on a methodology from aviation and clinical risk assessment: **classify → question → model → judge**, with explicit handling of compound risk (moderate factors that become serious when combined).

## How It Works

1. **Classify** the user's planned action into one or more scenario groups (travel, health-sensitive activity, stranger meeting, transaction, etc.)
2. **Ask** targeted follow-up questions — only what could change the recommendation (max 4 per round)
3. **Model** compound risk across 6 dimensions: vulnerability, exposure, friction, safeguards, reversibility, uncertainty
4. **Run the risk engine** (optional) for complex cases with 6+ factors
5. **Produce** a structured go/no-go judgment: Decision (green/yellow/orange/red), Why, Missing Facts, Next Actions, Worst Outcomes, Confidence

## Installation

### Claude Code
```bash
# Clone the repo
git clone https://github.com/dzlin/risk-guard.git ~/.claude/risk-guard

# Skills are auto-discovered from the skills/ directory
# Restart Claude Code to activate
```

### OpenAI Codex CLI
```bash
git clone https://github.com/dzlin/risk-guard.git ~/.codex/risk-guard
mkdir -p ~/.agents/skills
ln -s ~/.codex/risk-guard ~/.agents/skills/risk-guard
```
Restart Codex. See [`.codex/INSTALL.md`](.codex/INSTALL.md) for details.

### OpenCode
Add to your `opencode.json`:
```json
{
  "plugin": ["risk-guard@git+https://github.com/dzlin/risk-guard.git"]
}
```
See [`.opencode/INSTALL.md`](.opencode/INSTALL.md) for details.

### Cursor
Install from the plugin marketplace or copy the `.cursor-plugin/` directory.
See the configuration in [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json).

### Gemini
The `gemini-extension.json` and `GEMINI.md` provide context file support.

### Hermes Agent
Use directly — the `SKILL.md` is Hermes-compatible. Copy the skill directory to `~/.hermes/skills/risk-guard/`.

## Risk Engine

The included Python risk engine provides structured scoring:

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
  "constraint_tags": ["poor_medical_access"]
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
├── SKILL.md                          # Main skill definition (agent-agnostic)
├── CLAUDE.md                         # Claude Code context reference
├── GEMINI.md                         # Gemini context reference
├── package.json                       # Package metadata
├── LICENSE                           # MIT License
├── README.md                         # This file
├── agents/
│   └── risk-reviewer.md              # Agent persona for deep safety review
├── commands/
│   └── check.md                      # /risk-guard check command
├── hooks/
│   ├── hooks.json                    # Claude Code hooks
│   ├── hooks-cursor.json             # Cursor hooks
│   ├── session-start                 # Session startup hook
│   └── run-hook.cmd                  # Hook runner script
├── references/
│   ├── scenario-map.md               # 10 scenario groups with triggers
│   ├── question-bank.md              # High-yield follow-up questions
│   ├── risk-taxonomy.md              # Risk levels, compound logic, red flags
│   ├── output-examples.md            # 3 complete output examples
│   └── risk-engine-schema.md         # Full tag reference for risk engine
├── scripts/
│   └── risk_engine.py                # Scoring engine (Python 3)
├── tests/
│   └── test_risk_engine.py           # Test suite
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
    └── ...                            # Issue templates, funding, etc.
```

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

1. **Low-frequency, high-severity** — This skill audits rare but catastrophic risks, not daily inconveniences
2. **Compound risk over isolated risk** — Moderate factors that combine get escalated
3. **Prefer false positives** — When downside is irreversible, conservative beats optimistic
4. **Structured over vague** — Green/yellow/orange/red decisions, not "be careful"
5. **Minimal questions** — Only ask what could change the recommendation
6. **No medical/legal conclusions** — Risk reasoning and precautionary guidance only

## Contributing

Contributions are welcome! Please read the skill content carefully before submitting changes — the risk taxonomy and escalation heuristics are intentionally calibrated.

## License

MIT