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

| Component          | Location                                  | What it is                                                                      |
| ------------------ | ----------------------------------------- | ------------------------------------------------------------------------------- |
| `CLAUDE.md`        | `template/CLAUDE.md`                       | Stack-agnostic engineering standards — SOLID, KISS/DRY/YAGNI, security, testing, quality gates. |
| Settings           | `template/.claude/settings.json`          | Shared permissions + a pre-commit audit hook.                                   |
| Workflow           | `template/.claude/workflow.md`            | The working loop (plan → implement → review → done) and task→agent routing.     |
| Subagents          | `template/.claude/agents/`                | ~21 specialist agents in `backend/`, `frontend/`, `infra/`, `quality/`.         |
| Stack rules        | `template/.claude/rules/`                  | File-type rules (.NET, controllers, repositories, services, frontend, testing) plus always-on `code-review.md` and `security.md`. |
| Slash commands     | `template/.claude/commands/`              | `*.md` commands (e.g. `/claude-audit`); format guide in the README there.       |
| Audit tooling      | `template/.claude/scripts/` + `hooks/`    | `claude-audit.sh` consistency check and the `pre-commit-audit.sh` hook.         |
| Project instance   | `template/.claude/project/`               | Per-repo `context.md` profile + `tech-debt.md` register (placeholders to fill). |
| Skills             | `template/.claude/skills/`                | `<name>/SKILL.md` skills (format guide in the README there; none shipped yet).  |

Everything lives under `template/.claude/` as a **single source of truth** — the
plugin manifests point at it, and the installer copies from it.

## Usage

### Option 1 — Install as a plugin

Add this repo as a marketplace, then install the plugin:

```
/plugin marketplace add EinsZweiDrei-ai/einszweidrei-claude-kit
/plugin install ezd-claude-kit@einszweidrei-ai
```

Plugin commands are namespaced — invoke them as `/ezd-claude-kit:<name>`. The plugin
delivers commands, agents, and skills, and stays updatable.

> Note: the plugin distributes only **commands, agents, and skills**. Project-owned
> and copy-in-only content — `CLAUDE.md`, `.claude/settings.json`, and the kit's
> `rules/`, `hooks/`, and `scripts/` (the consistency audit + pre-commit hook) — is
> **not** delivered by the plugin. Use Option 2 to get those.

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
│   ├── CLAUDE.md            # engineering standards (stays at repo root when copied)
│   └── .claude/
│       ├── README.md        # explains the .claude/ layout
│       ├── workflow.md      # working loop + agent routing
│       ├── settings.json    # permissions + pre-commit audit hook
│       ├── commands/        # *.md slash commands (e.g. /claude-audit) (+ format guide)
│       ├── agents/          # subagents in backend/ frontend/ infra/ quality/ (+ format guide)
│       ├── rules/           # stack rules that auto-apply by file type
│       ├── scripts/         # claude-audit.sh consistency check
│       ├── hooks/           # pre-commit-audit.sh
│       ├── project/         # per-repo context.md + tech-debt.md (placeholders)
│       └── skills/          # <name>/SKILL.md (+ format guide)
├── install.sh               # copy-in installer (non-destructive unless FORCE=1)
├── scripts/validate.py      # no-dependency validator for CI
├── .gitattributes           # forces LF for scripts on every platform
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
