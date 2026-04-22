# Installing Risk Guard for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add risk-guard to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["risk-guard@git+https://github.com/Laplace-bit/risk-guard.git"]
}
```

Restart OpenCode. The plugin auto-installs and registers all skills.

Verify by asking: "Tell me about your risk-guard skill"

## Uninstalling

Remove the risk-guard entry from your `opencode.json` plugin array and restart OpenCode.

## Updating

Risk-guard updates automatically when you restart OpenCode.

To pin a specific version:

```json
{
  "plugin": ["risk-guard@git+https://github.com/Laplace-bit/risk-guard.git#v1.0.0"]
}
```