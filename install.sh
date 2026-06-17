#!/bin/sh
# install.sh — thin POSIX shim around install.py (the cross-platform installer).
#
# Usage:
#   ./install.sh [TARGET_DIR]      install into TARGET_DIR (default: current dir)
#   FORCE=1 ./install.sh [DIR]     overwrite files that already exist
#
# The real logic lives in install.py so Windows, Linux, and macOS share one
# implementation. This shim just locates a Python 3 interpreter and forwards to it.
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "error: Python 3 is required but neither 'python3' nor 'python' was found on PATH." >&2
  echo "       Install Python 3, or run the installer directly: python3 install.py [TARGET_DIR]" >&2
  exit 1
fi

exec "$PY" "$SCRIPT_DIR/install.py" "$@"
