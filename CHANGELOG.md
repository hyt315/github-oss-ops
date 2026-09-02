# Changelog

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/) 格式记录变更。

## [2.0.0] - 2026-09-02

### 🌟 Major Upgrade: 全景运营中枢、AI 垃圾防御、GHSA 私有漏洞协同与全渠道发版广播

- **渐进式调度架构重构**：`SKILL.md` 瘦身为轻量高信号调度中枢（105 行，~2143 tokens），严格按需索引 8 本参考手册；
- **AI 幻觉与垃圾 Issue/PR 防御**：新增虚假报错堆栈、虚构 API 识别与刷 KPI 贡献防御机制；
- **GitHub 官方 PVR 与 GHSA 私有安全协同**：新增 `references/security-vulnerability-sop.md`，提供 Temporary Private Fork、CVE 申请与协同披露 SOP；
- **全渠道发版广播中枢**：在 `references/release-workflow.md` 中新增 Twitter/X、Reddit、Discord、V2EX、微信全渠道广播推文模板；
- **社区治理与 All Contributors 致谢**：新增 `references/community-and-contributors.md`，覆盖冲突 4 级降温处置、24 种贡献类型致谢与 GitHub Sponsors 运营；
- **门面与文档全面升级**：中英双语 README 达到 PREP 黄金规范标准。

6-08-21

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
