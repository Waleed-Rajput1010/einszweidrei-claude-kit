# Contributing

Thanks for helping improve the EinsZweiDrei Claude Kit! This kit is meant to be
shared and improved by its users — corrections, new commands, agents, and skills
are all welcome.

## Where things live

Everything distributable lives under **`template/.claude/`** — a single source of
truth that both the plugin manifests and the copy-in installer read from. Add your
contribution in the matching directory:

| You're adding…   | Put it here                                  | Shape                                  |
| ---------------- | -------------------------------------------- | -------------------------------------- |
| A slash command  | `template/.claude/commands/<name>.md`        | One `*.md` file with frontmatter.      |
| A subagent       | `template/.claude/agents/<name>.md`          | One `*.md` file with frontmatter.      |
| A skill          | `template/.claude/skills/<name>/SKILL.md`    | A directory containing `SKILL.md`.     |

Each directory has a `README.md` with the full format guide and an example — read
it before adding files.

## Frontmatter formats (quick reference)

**Command** (`commands/<name>.md`):

```markdown
---
description: required — shown in the command picker
argument-hint: optional
allowed-tools: optional
model: optional
---
Body prompt. Use $ARGUMENTS / $1, !shell-cmd, and @file.
```

**Agent** (`agents/<name>.md`):

```markdown
---
name: required
description: required — when to use this agent
tools: optional
model: optional
---
System prompt body.
```

**Skill** (`skills/<name>/SKILL.md`):

```markdown
---
description: required — when Claude should use this skill
name: optional
allowed-tools: optional
disable-model-invocation: optional
---
Step-by-step instructions. May reference supporting files in the same dir.
```

## Validate locally

Before opening a PR, run the same checks CI runs:

```sh
python3 scripts/validate.py     # JSON parses; manifests & SKILL.md frontmatter valid
sh -n install.sh                # install.sh has no shell syntax errors
```

The validator treats missing command/agent frontmatter as a warning (so the empty
scaffold stays green) but a missing `SKILL.md` description is an error.

If you change behavior or add a component, add an entry to `CHANGELOG.md` under
`## [Unreleased]`.

## PR workflow

1. Fork and create a branch (`feature/my-command`, `fix/agent-typo`, …).
2. Make your change under `template/.claude/`.
3. Run the local validation steps above.
4. Update `CHANGELOG.md` if relevant.
5. Open a PR using the template and fill in the "how I tested" checklist.

Be kind and constructive — see our [Code of Conduct](CODE_OF_CONDUCT.md).
