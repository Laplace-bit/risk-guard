# Risk Guard — Commands

## `check`
Run a quick safety review on a described action.

```bash
/risk-guard check "I'm meeting a stranger from the internet tonight"
```

The agent will classify the scenario, ask follow-up questions if needed, and produce a structured go/no-go judgment.

## `analyze`
Run the full risk engine on a structured case file.

```bash
/risk-guard analyze path/to/case.json
```

Reads the JSON case file, runs the risk engine, and returns a detailed score breakdown.