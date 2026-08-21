# Changelog

All notable changes to GitHub OSS Ops are documented here.

## [1.2.0] - 2026-08-21

### Added

- Rulesets guidance (maintainer side): prefer Rulesets over classic branch protection; push rules apply to the entire fork network; `gh api repos/<owner>/<repo>/rulesets` to verify (GitHub Docs, verified 2026-08).
- Merge Queue note in Step 5: approved ≠ merged — PR re-runs required checks in queue; `gh pr merge --auto` to enqueue (GitHub Docs, verified 2026-08).
- Private vulnerability reporting verification command in Step 3.2: `gh api repos/<owner>/<repo>/private-vulnerability-reporting` (GitHub Docs, verified 2026-08).
- actions/stale version note in automation-templates: V11 is latest (ESM migration), official README still shows v10 — pin v10 until V11 is formally released.
- `scripts/selftest.py`: zero-dep regression (good fixture = this skill passes; negative fixtures: missing steps, orphan references, bare `.github` paths to non-existent repo files must be detected). Fixes the missing regression entry (DY001) found by skill-doctor audit.

### Changed

- Step 9.1 automation table: template paths now read "automation-templates § X → target repo .github/..." so they are not mistaken for files of this repo (fixes LK002 false-positive / agent hallucination risk).
- Linked `scripts/validate-skill.mjs` and `scripts/selftest.py` from the prerequisites section (fixes LK003).
- Added a table of contents to `references/github-access-guide.md` (fixes SK003).

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
