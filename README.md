# einszweidrei-claude-kit

> A reusable Claude Code developer kit — an opinionated `CLAUDE.md`, subagents,
> slash commands, skills, and settings you can drop into any project, and improve
> together.

Published by [EinsZweiDrei.ai](https://einszweidrei.ai) under the MIT license.

The kit ships **two ways**, because Claude Code's plugin system distributes
commands, agents, and skills — but it **cannot** inject a project-owned `CLAUDE.md`
or `.claude/settings.json` into your repo. So:

- Use the **plugin** for versioned, auto-updatable commands / agents / skills.
- Use the **copy-in installer** to drop `CLAUDE.md` and `.claude/settings.json`
  (and, if you prefer, everything else) directly into your project.

You can use either or both.

## What's inside

| Component               | Location                          | What it is                                                     |
| ----------------------- | --------------------------------- | -------------------------------------------------------------- |
| `CLAUDE.md`             | `template/CLAUDE.md`              | Project-context skeleton for Claude (placeholder — replace it). |
| Settings                | `template/.claude/settings.json`  | Minimal permissions scaffold.                                  |
| Slash commands          | `template/.claude/commands/`      | `*.md` commands (see the README there for the format).         |
| Subagents               | `template/.claude/agents/`        | `*.md` specialized agents (format guide in the README there).  |
| Skills                  | `template/.claude/skills/`        | `<name>/SKILL.md` skills (format guide in the README there).   |

Everything lives under `template/.claude/` as a **single source of truth** — the
plugin manifests point at it, and the installer copies from it.

## Usage

### Option 1 — Install as a plugin

Add this repo as a marketplace, then install the plugin:

```
/plugin marketplace add EinsZweiDrei-ai/einszweidrei-claude-kit
/plugin install einszweidrei@einszweidrei-kit
```

Plugin commands are namespaced — invoke them as `/einszweidrei:<name>`. The plugin
delivers commands, agents, and skills, and stays updatable.

> Note: the plugin does **not** install `CLAUDE.md` or `.claude/settings.json` —
> those are project-owned. Use Option 2 for those.

### Option 2 — Copy into your project

Clone the repo and run the installer against your project directory:

```sh
git clone https://github.com/EinsZweiDrei-ai/einszweidrei-claude-kit.git
cd einszweidrei-claude-kit
./install.sh /path/to/your/project
```

The installer is non-destructive: it skips files that already exist. To overwrite,
set `FORCE=1`:

```sh
FORCE=1 ./install.sh /path/to/your/project
```

With no argument it installs into the current directory. Copy-in commands are
invoked as `/<name>` (no namespace).

## Repository layout

```
einszweidrei-claude-kit/
├── .claude-plugin/
│   ├── plugin.json          # reads content from template/.claude/*
│   └── marketplace.json     # one plugin, "source": "./"
├── template/                # single source of truth (the open-sourced kit)
│   ├── CLAUDE.md
│   └── .claude/
│       ├── settings.json
│       ├── commands/        # *.md slash commands  (+ README format guide)
│       ├── agents/          # *.md subagents        (+ README format guide)
│       └── skills/          # <name>/SKILL.md       (+ README format guide)
├── install.sh               # copy-in installer (non-destructive unless FORCE=1)
├── scripts/validate.py      # no-dependency validator for CI
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
└── .github/
```

## Contributing

Improvements are welcome — that's the whole point. See [CONTRIBUTING.md](CONTRIBUTING.md)
for where each component type lives, the frontmatter formats, and the PR workflow.

## License

MIT © EinsZweiDrei.ai — see [LICENSE](LICENSE).
