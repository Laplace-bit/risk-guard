# Release Notes

## v2.0.1 (2026-04-24)

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
