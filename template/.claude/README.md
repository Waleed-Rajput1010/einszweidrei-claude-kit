# `.claude/` — Claude Code configuration

Configures how Claude Code works in this repo. The layout is split into a
**portable template** (drop into any repo — backend or frontend) and a **project instance**
(`project/`, specific to this repo).

```
CLAUDE.md                     # PORTABLE — stack-agnostic engineering standards (stays at repo root)
.claude/
├── README.md                 # PORTABLE — this file
├── workflow.md               # PORTABLE — the working loop + agent routing
├── settings.json             # PORTABLE — shared permissions + commit-audit hook (committed)
├── settings.local.json       # personal config (gitignored)
├── agents/                   # PORTABLE — subagents (backend / frontend / infra / quality)
├── rules/                    # PORTABLE — stack rules auto-apply by file type
│   ├── code-review.md        #   always-on review checklist (stack-agnostic)
│   ├── security.md           #   always-on web/app security
│   ├── dotnet.md             #   paths: **/*.cs  — C# conventions, architecture, async
│   ├── controllers.md        #   paths: **/Controllers/**
│   ├── repositories.md       #   paths: **/*Repository.cs
│   ├── services.md           #   paths: **/Services/**
│   ├── frontend.md           #   paths: **/*.{ts,tsx,vue,...}  — TS/React/Vue
│   └── testing.md            #   paths: test files
├── commands/                 # PORTABLE — slash commands (e.g. /claude-audit)
├── scripts/                  # PORTABLE — kit utilities (claude-audit.sh)
├── hooks/                    # PORTABLE — hook scripts (pre-commit-audit.sh)
└── project/                  # PROJECT-SPECIFIC — do NOT copy to other repos
    ├── context.md            #   profile: stack, layout, conventions, key libraries
    └── …                     #   this repo's own docs (tech-debt register, refactor plans, ADRs)
```

## Reusing this in another project

1. Copy `CLAUDE.md` + `.claude/` into the new repo root — **but skip `.claude/project/`**.
2. On the first task, Claude reads CLAUDE.md, finds `.claude/project/context.md`
   missing, and **scaffolds it** by inspecting the codebase (language, framework, layout,
   key libraries). No manual editing of the template needed — the portable files use
   generic globs and defer project specifics to `context.md`.
3. **Trim the agent roster** to the repo's stack. The kit ships backend-leaning agents
   (`csharp-developer`, `sql-pro`, `azure-infra-engineer`, …) alongside frontend ones
   (`react-developer`, `vue-developer`). Agents are inert until invoked, so extras are
   harmless — but delete the irrelevant ones for a tidy `agents/` folder.

> The portable layer degrades gracefully: even before `context.md` exists, the generic
> rules and standards apply. **Stack rules fire by file type** — `dotnet.md` only on `.cs`,
> `frontend.md` only on `.ts/.tsx/.vue` — so the same kit works in a backend *or* frontend
> repo with nothing to edit.

## How the pieces load

| Location | When it loads | Notes |
|---|---|---|
| `CLAUDE.md` (repo root) | Every session | Always-on core standards. |
| `rules/*.md` **without** `paths` | Every session | e.g. `code-review.md`, `security.md`. |
| `rules/*.md` **with** `paths` | When Claude opens a matching file | e.g. `repositories.md`. |
| `project/context.md` | When referenced (or created on first run) | Project profile; read before project work. |
| `agents/**` | On delegation | Identity comes from the `name` frontmatter; subfolders are organization only. |
| `project/` docs | On demand | Read only when linked. |

## Maintaining the kit

Run **`/claude-audit`** (or `bash .claude/scripts/claude-audit.sh`) to check the kit's
consistency: broken links, agent/rule frontmatter, agent-name uniqueness, stale path
references, and project-name leakage into portable files. It's deterministic — no agent
needed for the mechanical checks; use the main session for judgment work (new agents, ADRs).

## Source control

- **Commit** everything here **except** `settings.local.json` (personal, gitignored).
- `project/` **is** committed in each repo (the team needs that project's context + docs); it's simply **not carried** to other repos.

## Conventions

- Agent/rule files: **kebab-case**. Agent identity = the `name` frontmatter field, not the filename or folder. Keep `name` values unique across `agents/`.
