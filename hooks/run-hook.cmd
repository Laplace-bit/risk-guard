#!/usr/bin/env bash
# Risk Guard hook runner for Claude Code plugin
# Usage: run-hook.cmd <hook-name>
case "$1" in
  session-start)
    echo "Risk Guard skill loaded. Describe any planned action for a safety review."
    ;;
  *)
    echo "Unknown hook: $1"
    ;;
esac