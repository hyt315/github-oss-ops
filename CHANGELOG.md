# Changelog

All notable changes to GitHub OSS Ops are documented here.

## [1.1.0] - 2026-07-18

### Added

- Three end-to-end examples with explicit read/write approval boundaries.
- Cross-platform static validator and GitHub Actions validation workflow.
- Agent metadata, repository metadata, contributor attribution and a social-preview asset.

### Changed

- Corrected Codex installation to the current `~/.agents/skills` location and clarified ChatGPT/Codex naming.
- Reworked authentication around public read-only access, official GitHub OAuth/MCP, authenticated GitHub CLI and least-privilege fine-grained PATs.
- Rewrote the project landing page around outcomes, examples, downloads and a five-minute first run.

### Security

- Removed credential discovery that searched user directories or printed extracted tokens.
- Prohibited asking users to paste credentials into chat or persisting credentials in the skill directory.
- Replaced public vulnerability reporting with GitHub Private Vulnerability Reporting.

## [1.0.2] - 2026-07-18

- Aligned MCP tool names with the then-current consolidated GitHub MCP tools.

## [1.0.1] - 2026-07-18

- Replaced non-functional HTML anchors with Markdown headings.

## [1.0.0] - 2026-07-18

- Initial public release.
