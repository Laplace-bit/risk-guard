# Installing Risk Guard for Codex

Enable risk-guard skills in Codex via native skill discovery. Just clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the risk-guard repository:**
   ```bash
   git clone https://github.com/dzlin/risk-guard.git ~/.codex/risk-guard
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/risk-guard ~/.agents/skills/risk-guard
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\risk-guard" "$env:USERPROFILE\.codex\risk-guard"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Verify

```bash
ls -la ~/.agents/skills/risk-guard
```

You should see a symlink (or junction on Windows) pointing to your risk-guard directory.

## Updating

```bash
cd ~/.codex/risk-guard && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.agents/skills/risk-guard
```

Optionally delete the clone: `rm -rf ~/.codex/risk-guard`.