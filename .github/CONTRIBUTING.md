# Contributing to Risk Guard

Thank you for your interest in contributing!

## How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/my-feature`)
3. **Test** your changes — run `python tests/test_risk_engine.py` and verify the skill still produces sensible outputs
4. **Commit** with clear messages
5. **Open** a Pull Request

## Guidelines

- The risk taxonomy and escalation heuristics are intentionally calibrated. If you want to change weights or compound rules, include a test case demonstrating why the change is needed.
- Keep the skill content in English.
- Follow the existing structure: SKILL.md for the main skill, references/ for domain reference, scripts/ for the engine.
- All new tags must be documented in `references/risk-engine-schema.md`.
- Run the test suite before submitting: `python tests/test_risk_engine.py`

## Code of Conduct

Be respectful. We're all here to make safety reviews better.