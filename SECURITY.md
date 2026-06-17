# Security Policy

## Supported Versions

Only the **latest released version** of this kit receives security fixes.
Pin to a specific git tag or GitHub release rather than tracking a moving branch
so you know exactly which version you are running.

## Reporting a Vulnerability

Please report security vulnerabilities **privately** — do not open a public
issue.

1. Use GitHub's private vulnerability reporting: open the repository's
   **Security** tab and click **Report a vulnerability**.
2. Alternatively, email [INSERT SECURITY CONTACT EMAIL].

We will acknowledge your report as soon as possible and work with you on a
coordinated disclosure timeline.

## Trust and Review Before Use

This developer kit ships **commands, agents, and skills that Claude Code
executes on your machine**. Treat every component like source code you would
run locally:

- **Review** the contents of `template/.claude/commands/`, `agents/`, and
  `skills/` before installing or enabling them in a project.
- **Pin** to a specific git tag or release so you can audit exactly what you
  install instead of silently picking up changes from a branch.
- **Customize** permissions in `template/.claude/settings.json` (or your
  project copy) to match your security posture.

If you discover a vulnerability in this repository, please report it using the
process above.
