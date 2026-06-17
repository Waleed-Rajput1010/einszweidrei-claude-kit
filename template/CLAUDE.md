<!--
  ┌─────────────────────────────────────────────────────────────────────┐
  │  PLACEHOLDER — REPLACE THIS FILE                                       │
  │                                                                       │
  │  This CLAUDE.md ships with the EinsZweiDrei Claude Kit as a starting  │
  │  skeleton. It is intentionally generic. Replace the bracketed         │
  │  [PLACEHOLDER] text below with facts about YOUR project, then delete  │
  │  this comment block.                                                  │
  │                                                                       │
  │  CLAUDE.md is project-owned: it lives in your repo and is read by     │
  │  Claude Code automatically. Keep it short, factual, and current.      │
  └─────────────────────────────────────────────────────────────────────┘
-->

# [PROJECT NAME]

## Overview

[One paragraph: what this project is, who it's for, and what problem it solves.
Replace this with a real description.]

## Architecture

[Describe the high-level structure: main entry points, key directories, how the
pieces fit together. Point Claude at the parts of the tree that matter.]

- `[src/]` — [what lives here]
- `[tests/]` — [what lives here]
- `[...]` — [...]

## Conventions

[Coding standards Claude should follow in this repo. Be specific — these override
Claude's defaults.]

- **Language / runtime:** [e.g. TypeScript 5.x, Node 20]
- **Formatting:** [e.g. Prettier, 2-space indent, run `npm run format`]
- **Naming:** [e.g. kebab-case files, PascalCase components]
- **Testing:** [e.g. Vitest; colocate `*.test.ts`; cover new branches]
- **Commits:** [e.g. Conventional Commits]

## Workflows

[Common commands and how to run them. Claude will use these instead of guessing.]

- **Install:** `[npm install]`
- **Dev server:** `[npm run dev]`
- **Build:** `[npm run build]`
- **Test:** `[npm test]`
- **Lint / typecheck:** `[npm run lint && npm run typecheck]`

## Notes for Claude

[Anything that doesn't fit above: gotchas, things NOT to touch, security-sensitive
areas, preferred libraries, review expectations.]

- [e.g. Never edit files under `generated/` by hand.]
- [e.g. Prefer the existing HTTP client in `src/lib/http.ts` over adding new deps.]
- [e.g. Ask before changing the public API surface in `src/index.ts`.]
