# Changelog

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/) 格式记录变更。

## [2.1.0] - 2026-09-06

### 🌟 Minor Upgrade: 运维避坑指南落地、就绪度验证工具与 AST 语法安全防线

- **深水区避坑指南全景沉淀**：新增 [references/github-oss-ops-pitfalls.md](references/github-oss-ops-pitfalls.md)，覆盖 GITHUB_TOKEN 提权风险、`pull_request_target` Pwn-Request 防御、新一代 Rulesets Tag 保护、Stale Bot 反噬与 AI 垃圾拦截、PVR 私有安全协同及 API 次级限流退避；
- **全景运维就绪度校验器**：新增 `scripts/validate_ops.py`，支持 `--json`（结构化机读报告）、`--quick`（快速采样）与 `--read-only`（零变更保障）；
- **动态版本感知 CI 守护**：重构 `scripts/validate-skill.mjs`，动态读取 `manifest.json` 版本号，彻底消除发版 CI 硬编码脱节隐患；
- **AST 语法解析与多维回归**：升级 `scripts/selftest.py`，引入 `ast.parse` 静态语法解析门禁，新增 `tests/test_skill.py` 自动化测试集；
- **统一事实卡片与安全授权宣告**：在 `SKILL.md` 中规范化定义标准 Markdown 格式的 Ops 事实卡片 (Fact Card)，固化 Zero-Mutation 铁律与破坏性写操作显式授权防线。

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
