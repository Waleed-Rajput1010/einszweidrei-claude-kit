#!/bin/sh
# install.sh — copy the EinsZweiDrei Claude Kit template into a project.
#
# Usage:
#   ./install.sh [TARGET_DIR]
#
#   TARGET_DIR   Directory to install into. Defaults to the current directory.
#   FORCE=1      Overwrite files that already exist (default: skip them).
#
# Copies everything under ./template/ into TARGET_DIR, mirroring paths. This
# delivers CLAUDE.md and .claude/ (settings, commands, agents, skills) into a
# project — content the plugin system cannot inject for you.
#
# Non-destructive by default: existing files are skipped unless FORCE=1.

set -eu

# Resolve the directory this script lives in (so it works from anywhere).
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SRC_DIR="$SCRIPT_DIR/template"

TARGET_DIR=${1:-.}
FORCE=${FORCE:-0}

if [ ! -d "$SRC_DIR" ]; then
  echo "error: template directory not found at $SRC_DIR" >&2
  exit 1
fi

# Create target dir if needed.
mkdir -p "$TARGET_DIR"
TARGET_DIR=$(CDPATH= cd -- "$TARGET_DIR" && pwd)

echo "Installing EinsZweiDrei Claude Kit"
echo "  from: $SRC_DIR"
echo "  into: $TARGET_DIR"
[ "$FORCE" = "1" ] && echo "  mode: FORCE (overwriting existing files)" || echo "  mode: non-destructive (skipping existing files)"
echo

wrote=0
skipped=0

# Walk every file under the template, preserving relative paths.
# Using find + read keeps this POSIX and handles nested dirs.
find "$SRC_DIR" -type f | while IFS= read -r src; do
  rel=${src#"$SRC_DIR"/}
  dest="$TARGET_DIR/$rel"

  # Never distribute personal config — settings.local.json is per-developer and
  # gitignored, so it must not be copied into a target project.
  case "$rel" in
    *settings.local.json)
      echo "  skip   $rel (personal config, never distributed)"
      continue
      ;;
  esac

  if [ -e "$dest" ] && [ "$FORCE" != "1" ]; then
    echo "  skip   $rel (exists)"
    skipped=$((skipped + 1))
    continue
  fi

  mkdir -p "$(dirname -- "$dest")"
  cp "$src" "$dest"
  echo "  write  $rel"
  wrote=$((wrote + 1))
done

echo
echo "Done. Next steps:"
echo "  1. Edit CLAUDE.md and replace the placeholder content with your project's details."
echo "  2. Review .claude/settings.json and add any permissions you want."
echo "  3. Add your own commands, agents, and skills under .claude/."
