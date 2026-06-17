#!/usr/bin/env python3
"""install.py — copy the EinsZweiDrei Claude Kit template into a project.

Cross-platform (Windows + Linux + macOS). Standard library only — no dependencies.

Usage:
    python install.py [TARGET_DIR] [--force]

    TARGET_DIR   Directory to install into. Defaults to the current directory.
    --force      Overwrite files that already exist (default: skip them).
                 The FORCE=1 environment variable is honored too, for parity
                 with install.sh.

Copies everything under ./template/ into TARGET_DIR, mirroring paths. This
delivers CLAUDE.md and .claude/ (settings, commands, agents, skills) into a
project — content the plugin system cannot inject for you.

Non-destructive by default: existing files are skipped unless --force/FORCE=1.
"""

import argparse
import os
import shutil
import sys

# Personal, per-developer config that must never be distributed into a target
# project — it is gitignored in this repo for the same reason.
SKIP_SUFFIXES = ("settings.local.json",)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="install.py",
        description="Copy the EinsZweiDrei Claude Kit template into a project.",
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Directory to install into (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=os.environ.get("FORCE") == "1",
        help="Overwrite files that already exist (default: skip them).",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])

    # Resolve paths relative to this script so it works from any CWD.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, "template")

    if not os.path.isdir(src_dir):
        print(f"error: template directory not found at {src_dir}", file=sys.stderr)
        return 1

    os.makedirs(args.target_dir, exist_ok=True)
    target_dir = os.path.abspath(args.target_dir)

    print("Installing EinsZweiDrei Claude Kit")
    print(f"  from: {src_dir}")
    print(f"  into: {target_dir}")
    print(
        "  mode: FORCE (overwriting existing files)"
        if args.force
        else "  mode: non-destructive (skipping existing files)"
    )
    print()

    wrote = 0
    skipped = 0

    # Walk every file under the template, preserving relative paths. Sorting keeps
    # the output deterministic across platforms (os.walk order is filesystem-dependent).
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames.sort()
        for name in sorted(filenames):
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, src_dir)
            # Display paths use forward slashes on every platform.
            rel_display = rel.replace(os.sep, "/")
            dest = os.path.join(target_dir, rel)

            if rel_display.endswith(SKIP_SUFFIXES):
                print(f"  skip   {rel_display} (personal config, never distributed)")
                continue

            if os.path.exists(dest) and not args.force:
                print(f"  skip   {rel_display} (exists)")
                skipped += 1
                continue

            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(src, dest)
            print(f"  write  {rel_display}")
            wrote += 1

    print()
    print(f"Done. {wrote} written, {skipped} skipped. Next steps:")
    print("  1. Edit CLAUDE.md and replace the placeholder content with your project's details.")
    print("  2. Review .claude/settings.json and add any permissions you want.")
    print("  3. Add your own commands, agents, and skills under .claude/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
