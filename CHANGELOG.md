# Changelog

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [SemVer](https://semver.org/lang/zh-CN/)。

## [2.3.0] - 2026-11-20

Major simplification & security hardening release. Cut template bloat by >70%, aligned with the `agentskills.io` open specification, and added Prompt Injection defense for AI-assisted repository operations.

### Added

- **Prompt Injection iron rule in `SKILL.md`**: Explicitly treats all external Issue/PR descriptions, comments, and code comments as untrusted data so embedded instructions cannot hijack review or triage actions.
- **Expanded secret scanning in `scripts/validate.py`**: Added detection for OpenAI/Anthropic `sk-` keys, Google `AIza`, Hugging Face `hf_`, npm `npm_`, PyPI `pypi-`, and URL-embedded credentials.
- **Modern Agent Skill installation**: Added `npx skills add hyt315/github-oss-ops` alongside copy-to-AI one-liner installation and manual clone.

### Changed

- **Consolidated `references/` (10 files, 2,479 lines → 4 files)**: Replaced verbose canned reply templates (`response-templates.md`), version-file textbooks, and bloated workflow YAMLs with 4 high-signal manuals (`triage-and-pr.md`, `security-and-pitfalls.md`, `release-and-reporting.md`, `automation-and-access.md`).
- **Aligned `SKILL.md` frontmatter with `agentskills.io`**: Moved `version` under `metadata.version`, added `license: MIT`, and updated `scripts/validate.py` to reject non-standard top-level keys.
- **Decoupled brittle release-ceremony checks**: Removed rigid date/heading/path bindings on `README.md`, `README.en.md`, and `.github/repository-metadata.yml` from `scripts/validate.py`.
- **Streamlined bilingual READMEs**: Removed dead `skill-doctor` link, duplicate dividers, and inline changelog duplication.

### Removed

- `references/response-templates.md` (replaced by 5 concise reply principles in `triage-and-pr.md`).
- `.github/repository-metadata.yml`, `CONTRIBUTORS.md`, and `examples/README.md` (redundant static files).

## [2.2.1] - 2026-11-12

- Switched reporting counts to `search/issues` `total_count` to avoid 30-item truncation; aligned public-issue vulnerability handling with SOP; switched label bootstrap to `gh label create --force`; added Python 3.10 + 3.12 CI matrix.

## [2.2.0] - 2026-11-08

- Converted `SKILL.md` to a task routing table with read-only snapshot commands; unified validation into `scripts/validate.py`; fact-checked GitHub Docs & Changelog updates (PVR, Rulesets, Interaction limits, Dependabot, Actions v11/v7).

## [2.1.0] - 2026-09-06

- Added `github-oss-ops-pitfalls.md`, readiness validator, and AST syntax checks.

## [2.0.0] - 2026-09-02

- Introduced AI slop defense, GHSA private vulnerability SOP, release workflow, and community moderation guides.

## [1.2.1] - 2026-08-22

- Added reading-time notes to `SKILL.md`.

## [1.2.0] - 2026-08-21

- Added Rulesets, Merge Queue, and PVR verification commands.

## [1.1.0] - 2026-07-18

- Reworked authentication around public read-only access, official OAuth/MCP, `gh`, and least-privilege Fine-grained PATs.

## [1.0.2] - 2026-07-17

- Aligned MCP tool names with consolidated GitHub MCP tools.

## [1.0.1] - 2026-06-22

- Replaced non-functional HTML anchors with Markdown headings.

## [1.0.0] - 2026-06-21

- Initial public release.
