#!/usr/bin/env bash
# claude-audit.sh — consistency audit for the .claude kit (portable, stack-agnostic).
# FAIL (exit 1): broken links, invalid agent/rule frontmatter, duplicate agent names.
# WARN (exit 0): stale backtick path refs, project-name leakage into portable files.
set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 2
fail=0; warn=0
tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT

mdfiles() { { find .claude -name '*.md' 2>/dev/null; [ -f CLAUDE.md ] && echo CLAUDE.md; }; }

echo "Auditing .claude kit at: $ROOT"

# 1. Broken markdown links -------------------------------------------------- FAIL
echo ""; echo "=== 1. Broken markdown links ==="
: > "$tmp"
for f in $(mdfiles); do
  dir="$(dirname "$f")"
  while IFS= read -r link; do
    case "$link" in http*|\#*|mailto*) continue;; esac
    target="${link%%#*}"; [ -z "$target" ] && continue
    # project/ is the per-repo instance, created on first run (and the README tells
    # users to drop it when carrying the kit elsewhere). Don't fail links into it
    # until that instance exists; once it does, validate them like any other link.
    case "$target" in
      */project/*|project/*) [ -d "$ROOT/.claude/project" ] || continue ;;
    esac
    [ -e "$dir/$target" ] || echo "  BROKEN: $f -> $link" >> "$tmp"
  done < <(grep -oE '\]\([^) ]+\)' "$f" 2>/dev/null | sed -E 's/^\]\(//; s/\)$//')
done
if [ -s "$tmp" ]; then cat "$tmp"; fail=1; else echo "  ok"; fi

# 2. Backtick `.claude/...` path refs that don't exist ---------------------- WARN
echo ""; echo "=== 2. Stale backtick path references (\`.claude/...\`) ==="
: > "$tmp"
for f in $(mdfiles); do
  grep -oE '`\.claude/[^`]+`' "$f" 2>/dev/null | tr -d '`' | while IFS= read -r p; do
    [ -e "$p" ] || echo "  MISSING: $f -> \`$p\`" >> "$tmp"
  done
done
if [ -s "$tmp" ]; then cat "$tmp"; warn=1; else echo "  ok"; fi

# 3. Agent frontmatter + precedence ----------------------------------------- FAIL
echo ""; echo "=== 3. Agent frontmatter (name + description required; tools/model optional) + precedence ==="
: > "$tmp"
# README.md files are format-guide keepfiles, not agents — skip them.
for a in $(find .claude/agents -name '*.md' -not -name 'README.md' 2>/dev/null); do
  head -1 "$a" | grep -q '^---$' || echo "  NO FRONTMATTER: $a" >> "$tmp"
  for k in name description; do
    grep -qm1 "^$k:" "$a" || echo "  MISSING $k: $a" >> "$tmp"
  done
  grep -qm1 "Project precedence" "$a" || echo "  NO PRECEDENCE LINE: $a" >> "$tmp"
done
if [ -s "$tmp" ]; then cat "$tmp"; fail=1; else echo "  ok ($(find .claude/agents -name '*.md' -not -name 'README.md' 2>/dev/null | wc -l) agents)"; fi

# 4. Rule frontmatter ------------------------------------------------------- FAIL
echo ""; echo "=== 4. Rule frontmatter (description) ==="
: > "$tmp"
for r in $(find .claude/rules -name '*.md' -not -name 'README.md' 2>/dev/null); do
  head -1 "$r" | grep -q '^---$' || echo "  NO FRONTMATTER: $r" >> "$tmp"
  grep -qm1 '^description:' "$r" || echo "  MISSING description: $r" >> "$tmp"
done
if [ -s "$tmp" ]; then cat "$tmp"; fail=1; else
  echo "  ok ($(find .claude/rules -name '*.md' -not -name 'README.md' 2>/dev/null | wc -l) rules: $(for r in .claude/rules/*.md; do [ "$(basename "$r")" = README.md ] && continue; grep -qm1 '^paths:' "$r" && echo -n 'scoped ' || echo -n 'always '; done | tr ' ' '\n' | sort | uniq -c | tr '\n' ' '))"
fi

# 5. Agent name uniqueness -------------------------------------------------- FAIL
echo ""; echo "=== 5. Agent name uniqueness ==="
dupes="$(grep -rh '^name:' .claude/agents 2>/dev/null | sort | uniq -d)"
if [ -n "$dupes" ]; then echo "  DUPLICATE NAMES:"; echo "$dupes" | sed 's/^/    /'; fail=1; else
  echo "  ok ($(grep -rh '^name:' .claude/agents 2>/dev/null | sort -u | wc -l) unique)"
fi

# 6. Project-name leakage into portable files ------------------------------- WARN
echo ""; echo "=== 6. Project-name leakage into portable files ==="
if [ -f .claude/project/context.md ]; then
  token="$(grep -oiE '[A-Za-z][A-Za-z0-9]+\.sln' .claude/project/context.md | head -1 | sed -E 's/\.sln$//')"
  if [ -n "$token" ]; then
    hits="$(grep -rilw "$token" CLAUDE.md .claude/rules .claude/agents .claude/README.md .claude/commands .claude/scripts 2>/dev/null)"
    if [ -n "$hits" ]; then
      echo "  Portable files mention project token '$token' (should live only in .claude/project/):"
      echo "$hits" | sed 's/^/    /'; warn=1
    else echo "  ok (no '$token' in portable files)"; fi
  else echo "  skipped (no .sln token in context.md)"; fi
else echo "  skipped (.claude/project/context.md not present)"; fi

# 7. context.md references match the codebase ------------------------------ WARN
echo ""; echo "=== 7. context.md references match the codebase ==="
if [ -f .claude/project/context.md ]; then
  prefix="$(grep -oiE '[A-Za-z][A-Za-z0-9]+\.sln' .claude/project/context.md | head -1 | sed -E 's/\.sln$//')"
  if [ -n "$prefix" ]; then
    : > "$tmp"
    grep -oiE "${prefix}\.[A-Za-z][A-Za-z0-9]+" .claude/project/context.md | grep -viE '\.(sln|csproj|cs|md|json|ya?ml|sh|txt)$' | sort -u | while IFS= read -r proj; do
      if [ -d "$proj" ] || find . -maxdepth 3 -name "${proj}.csproj" 2>/dev/null | grep -q .; then :;
      else echo "  MISSING (referenced in context.md, not found in repo): $proj" >> "$tmp"; fi
    done
    if [ -s "$tmp" ]; then cat "$tmp"; warn=1; else echo "  ok (referenced projects exist)"; fi
  else echo "  skipped (no .sln token in context.md)"; fi
else echo "  skipped (.claude/project/context.md not present)"; fi

# Summary ------------------------------------------------------------------
echo ""; echo "============================================"
if [ "$fail" -ne 0 ]; then echo "RESULT: FAIL (structural issues above)";
elif [ "$warn" -ne 0 ]; then echo "RESULT: PASS with warnings (review above)";
else echo "RESULT: PASS — kit is consistent ✓"; fi
echo "============================================"
exit "$fail"
