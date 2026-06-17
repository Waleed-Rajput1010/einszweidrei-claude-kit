#!/usr/bin/env python3
"""claude-audit.py — consistency audit for the .claude kit (portable, stack-agnostic).

FAIL (exit 1): broken links, invalid agent/rule frontmatter, duplicate agent names.
WARN (exit 0): stale backtick path refs, project-name leakage, context.md drift.

Cross-platform (Windows + Linux + macOS). Standard library only — no dependencies.

Usage:
    python claude-audit.py [--pre-commit]

    (no flag)      Run the audit and print the full report. Exit 1 on FAIL, else 0.
    --pre-commit   Silent on PASS; on FAIL print guidance + report to stderr and
                   exit 2 (which blocks a Claude Code `git commit` tool call).
"""

import argparse
import os
import re
import subprocess
import sys

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
BACKTICK_RE = re.compile(r"`(\.claude/[^`]+)`")
SLN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]+\.sln", re.IGNORECASE)
EXT_RE = re.compile(r"\.(sln|csproj|cs|md|json|ya?ml|sh|txt)$", re.IGNORECASE)


def repo_root():
    """Git top-level, or the current directory if not in a repo."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
        )
        top = out.stdout.strip()
        if out.returncode == 0 and top:
            return os.path.abspath(top)
    except OSError:
        pass
    return os.getcwd()


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def rel(root, path):
    return os.path.relpath(path, root).replace(os.sep, "/")


def md_files(root):
    """Every *.md under .claude/, plus CLAUDE.md at the root."""
    out = []
    claude_dir = os.path.join(root, ".claude")
    if os.path.isdir(claude_dir):
        for dirpath, dirnames, filenames in os.walk(claude_dir):
            dirnames.sort()
            for name in sorted(filenames):
                if name.endswith(".md"):
                    out.append(os.path.join(dirpath, name))
    claude_md = os.path.join(root, "CLAUDE.md")
    if os.path.isfile(claude_md):
        out.append(claude_md)
    return out


def find_under(root, subpath, predicate):
    """All files under root/subpath (recursively) matching predicate(name)."""
    base = os.path.join(root, *subpath.split("/"))
    out = []
    if os.path.isdir(base):
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for name in sorted(filenames):
                if predicate(name):
                    out.append(os.path.join(dirpath, name))
    return out


def agent_files(root):
    return find_under(
        root, ".claude/agents", lambda n: n.endswith(".md") and n != "README.md"
    )


def rule_files(root):
    return find_under(
        root, ".claude/rules", lambda n: n.endswith(".md") and n != "README.md"
    )


def has_line(text, prefix):
    return any(line.startswith(prefix) for line in text.splitlines())


def first_line_is_fence(text):
    lines = text.splitlines()
    return bool(lines) and lines[0].strip() == "---"


def find_csproj(root, filename, maxdepth=3):
    """True if `filename` exists within `maxdepth` levels below root."""
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        depth = dirpath[len(root) :].count(os.sep)
        if depth >= maxdepth:
            dirnames[:] = []
        if filename in filenames:
            return True
    return False


def run_audit(root):
    """Return (fail, warn, report_lines)."""
    fail = False
    warn = False
    out = [f"Auditing .claude kit at: {root}"]
    project_dir = os.path.join(root, ".claude", "project")
    project_exists = os.path.isdir(project_dir)
    mds = md_files(root)

    # 1. Broken markdown links -------------------------------------------- FAIL
    out += ["", "=== 1. Broken markdown links ==="]
    broken = []
    for f in mds:
        d = os.path.dirname(f)
        for link in LINK_RE.findall(read(f)):
            if link.startswith(("http", "#", "mailto")):
                continue
            target = link.split("#", 1)[0]
            if not target:
                continue
            # project/ is the per-repo instance, created on first run. Don't fail
            # links into it until that instance exists.
            if ("/project/" in target or target.startswith("project/")) and not project_exists:
                continue
            if not os.path.exists(os.path.join(d, target)):
                broken.append(f"  BROKEN: {rel(root, f)} -> {link}")
    if broken:
        out += broken
        fail = True
    else:
        out.append("  ok")

    # 2. Stale backtick `.claude/...` path refs --------------------------- WARN
    out += ["", "=== 2. Stale backtick path references (`.claude/...`) ==="]
    stale = []
    for f in mds:
        for p in BACKTICK_RE.findall(read(f)):
            if not os.path.exists(os.path.join(root, p)):
                stale.append(f"  MISSING: {rel(root, f)} -> `{p}`")
    if stale:
        out += stale
        warn = True
    else:
        out.append("  ok")

    # 3. Agent frontmatter + precedence ----------------------------------- FAIL
    agents = agent_files(root)
    out += [
        "",
        "=== 3. Agent frontmatter (name + description required; tools/model optional) + precedence ===",
    ]
    issues = []
    for a in agents:
        text = read(a)
        if not first_line_is_fence(text):
            issues.append(f"  NO FRONTMATTER: {rel(root, a)}")
        for k in ("name", "description"):
            if not has_line(text, k + ":"):
                issues.append(f"  MISSING {k}: {rel(root, a)}")
        if "Project precedence" not in text:
            issues.append(f"  NO PRECEDENCE LINE: {rel(root, a)}")
    if issues:
        out += issues
        fail = True
    else:
        out.append(f"  ok ({len(agents)} agents)")

    # 4. Rule frontmatter ------------------------------------------------- FAIL
    rules = rule_files(root)
    out += ["", "=== 4. Rule frontmatter (description) ==="]
    issues = []
    for r in rules:
        text = read(r)
        if not first_line_is_fence(text):
            issues.append(f"  NO FRONTMATTER: {rel(root, r)}")
        if not has_line(text, "description:"):
            issues.append(f"  MISSING description: {rel(root, r)}")
    if issues:
        out += issues
        fail = True
    else:
        scoped = sum(1 for r in rules if has_line(read(r), "paths:"))
        always = len(rules) - scoped
        out.append(f"  ok ({len(rules)} rules: {always} always, {scoped} scoped)")

    # 5. Agent name uniqueness -------------------------------------------- FAIL
    out += ["", "=== 5. Agent name uniqueness ==="]
    name_lines = []
    for a in agents:
        name_lines += [
            line.rstrip() for line in read(a).splitlines() if line.startswith("name:")
        ]
    seen = {}
    for line in name_lines:
        seen[line] = seen.get(line, 0) + 1
    dupes = sorted(line for line, n in seen.items() if n > 1)
    if dupes:
        out.append("  DUPLICATE NAMES:")
        out += [f"    {d}" for d in dupes]
        fail = True
    else:
        out.append(f"  ok ({len(set(name_lines))} unique)")

    # 6. Project-name leakage into portable files ------------------------- WARN
    out += ["", "=== 6. Project-name leakage into portable files ==="]
    context_md = os.path.join(project_dir, "context.md")
    token = None
    if os.path.isfile(context_md):
        m = SLN_RE.search(read(context_md))
        if m:
            token = m.group()[:-4]  # strip .sln
    if token:
        word_re = re.compile(r"\b" + re.escape(token) + r"\b", re.IGNORECASE)
        portable = []
        for rel_path in ("CLAUDE.md", ".claude/README.md"):
            p = os.path.join(root, *rel_path.split("/"))
            if os.path.isfile(p):
                portable.append(p)
        for sub in (".claude/rules", ".claude/agents", ".claude/commands", ".claude/scripts"):
            portable += find_under(root, sub, lambda n: True)
        hits = [rel(root, p) for p in portable if word_re.search(read(p))]
        if hits:
            out.append(
                f"  Portable files mention project token '{token}' (should live only in .claude/project/):"
            )
            out += [f"    {h}" for h in hits]
            warn = True
        else:
            out.append(f"  ok (no '{token}' in portable files)")
    elif os.path.isfile(context_md):
        out.append("  skipped (no .sln token in context.md)")
    else:
        out.append("  skipped (.claude/project/context.md not present)")

    # 7. context.md references match the codebase ------------------------- WARN
    out += ["", "=== 7. context.md references match the codebase ==="]
    if os.path.isfile(context_md):
        ctx = read(context_md)
        m = SLN_RE.search(ctx)
        prefix = m.group()[:-4] if m else None
        if prefix:
            token_re = re.compile(re.escape(prefix) + r"\.[A-Za-z][A-Za-z0-9]+")
            projs = sorted(
                {t for t in token_re.findall(ctx) if not EXT_RE.search(t)}
            )
            missing = []
            for proj in projs:
                if os.path.isdir(os.path.join(root, proj)):
                    continue
                if find_csproj(root, proj + ".csproj", maxdepth=3):
                    continue
                missing.append(
                    f"  MISSING (referenced in context.md, not found in repo): {proj}"
                )
            if missing:
                out += missing
                warn = True
            else:
                out.append("  ok (referenced projects exist)")
        else:
            out.append("  skipped (no .sln token in context.md)")
    else:
        out.append("  skipped (.claude/project/context.md not present)")

    # Summary -----------------------------------------------------------------
    out += ["", "============================================"]
    if fail:
        out.append("RESULT: FAIL (structural issues above)")
    elif warn:
        out.append("RESULT: PASS with warnings (review above)")
    else:
        out.append("RESULT: PASS - kit is consistent")
    out.append("============================================")
    return fail, warn, out


def main(argv=None):
    parser = argparse.ArgumentParser(prog="claude-audit.py")
    parser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Silent on PASS; on FAIL print guidance to stderr and exit 2.",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    root = repo_root()
    try:
        os.chdir(root)
    except OSError:
        pass
    fail, _warn, report = run_audit(root)

    if args.pre_commit:
        if fail:
            print("BLOCKED: the .claude kit audit FAILED - fix before committing.", file=sys.stderr)
            print("\n".join(report), file=sys.stderr)
            print("Run /claude-audit and resolve the FAIL items, then retry the commit.", file=sys.stderr)
            return 2  # exit 2 = block the tool call; stderr is fed back to Claude
        return 0

    print("\n".join(report))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
