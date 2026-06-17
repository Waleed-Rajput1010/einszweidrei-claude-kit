---
description: Rules for ASP.NET Core controllers (API layer)
paths:
  - "**/Controllers/**/*.cs"
  - "**/*Controller.cs"
---

# Controller rules (API layer)

Auto-applies when editing controllers. Full standards: [CLAUDE.md](../../CLAUDE.md). Project stack/helpers: [project/context.md](../project/context.md).

- **Thin controllers only** — no business logic. Delegate to an application-layer service via its interface.
- No `DbContext`, EF Core, or repository access in the API layer.
- Accept and return **DTOs**, never entities.
- Validate input (the project's model-validation filter); `[Authorize]` by default — justify any `[AllowAnonymous]`.
- Propagate `CancellationToken` from the action into the service call.
- Let exceptions bubble to the global error-handling middleware — don't catch-and-swallow. Use the project's standard result wrapper.
- One responsibility per endpoint; keep actions small.
