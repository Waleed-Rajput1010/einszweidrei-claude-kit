# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-17

### Added

- Initial scaffold of the EinsZweiDrei Claude Kit.
- Plugin + marketplace manifests under `.claude-plugin/`, both pointing at
  `template/.claude/` as a single source of truth.
- `template/CLAUDE.md` placeholder skeleton.
- `template/.claude/settings.json` minimal permissions scaffold.
- Format-guide READMEs for commands, agents, and skills.
- `install.sh` copy-in installer (non-destructive unless `FORCE=1`).
- `scripts/validate.py` dependency-free validator.
- Project docs: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.
- GitHub issue/PR templates and a CI workflow.

[Unreleased]: https://github.com/EinsZweiDrei-ai/einszweidrei-claude-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/EinsZweiDrei-ai/einszweidrei-claude-kit/releases/tag/v0.1.0
