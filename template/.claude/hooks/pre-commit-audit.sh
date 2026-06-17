#!/usr/bin/env bash
# PreToolUse(Bash) hook — blocks a `git commit` if the .claude kit audit fails.
# Wired in .claude/settings.json with  if: "Bash(git commit*)"  so it only fires on commits.
# Deterministic guard: you can't commit a structurally-broken kit (broken links,
# invalid frontmatter, duplicate agent names). WARN-level items don't block.
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
out="$(bash "$ROOT/.claude/scripts/claude-audit.sh" 2>&1)"; rc=$?
if [ "$rc" -ne 0 ]; then
  {
    echo "BLOCKED: the .claude kit audit FAILED — fix before committing."
    echo "$out"
    echo "Run /claude-audit and resolve the FAIL items, then retry the commit."
  } >&2
  exit 2   # exit 2 = block the tool call; stderr is fed back to Claude
fi
exit 0
