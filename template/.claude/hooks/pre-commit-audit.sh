#!/bin/sh
# PreToolUse(Bash) hook — blocks a `git commit` if the .claude kit audit fails.
# Wired in .claude/settings.json with  if: "Bash(git commit*)"  so it only fires on commits.
# Deterministic guard: you can't commit a structurally-broken kit (broken links,
# invalid frontmatter, duplicate agent names). WARN-level items don't block.
#
# Thin POSIX launcher: the audit logic lives in claude-audit.py (cross-platform).
# This hook runs inside Claude Code, where sh is available on every platform; it
# locates a Python 3 interpreter and forwards to the audit in --pre-commit mode
# (silent on PASS; prints guidance and exits 2 to block the commit on FAIL).
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "BLOCKED: Python 3 is required to run the .claude kit audit but was not found on PATH." >&2
  exit 2
fi

exec "$PY" "$ROOT/.claude/scripts/claude-audit.py" --pre-commit
