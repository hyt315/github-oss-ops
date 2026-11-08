# Changelog

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [SemVer](https://semver.org/lang/zh-CN/)。

## [2.2.0] - 2026-11-08

### Changed

- `SKILL.md` 由串行的 Step 1–9 改为“任务路由表”：每类请求只读对应的 1–2 份手册，并写明产出和需要批准的写操作。新增只读的仓库快照命令，事实卡标明“格式示例”，数值必须来自命令。
- 校验脚本合并为一个：`scripts/validate.py` 取代 `validate_ops.py`、`selftest.py`、`validate-skill.mjs`；`tests/test_validate.py` 取代 `tests/test_skill.py`，补上版本漂移、孤儿手册、失效链接、凭据样式、写死步骤编号等负向测试。CI 改为 Python，不再依赖 Node。
- 手册不再写死 “SKILL.md Step N”，改为“适用任务”说明，避免编号变动后失效。
- `github-oss-ops-pitfalls.md` 删去与其他手册重复的段落，改为指向对应手册。
- `reporting.md` 补上 MTTM 定义与取数命令，时长指标改用中位数并注明样本数。
- Stale 模板只处理 `status:needs-info`，PR 只提醒不自动关闭，与避坑指南保持一致。
- Issue Labeler 配置改名为 `.github/issue-labeler.yml`，避免与 `actions/labeler` 冲突；`sync-labels` 改为 0。

### Fixed（对照 2026-11-08 的 GitHub Docs 与 Changelog 核对）

- Interaction limits 三种选项与时长写错（应为 existing users／prior contributors／repository collaborators；时长含 6 个月）。
- 删除不存在的“把 Issue 转成安全公告”和“Issue 改为私密”的说法；GitHub 没有私信功能。
- Issue 转 Discussion：REST 与 GraphQL 都不支持，只能在网页操作。
- Fork PR 工作流审批的设置名与选项名更新为当前名称。
- Rulesets 的 Evaluate 模式仅 Enterprise 提供；组织级规则集需要 Team 或 Enterprise。
- Artifact attestations 单独使用为 SLSA Build Level 2，不是 Level 3。
- 默认 `GITHUB_TOKEN` 权限：新建个人仓库默认只读，组织仓库继承组织设置。
- 私有漏洞报告：设置路径、`Security & quality` 标签页改名（2026-04-02）、`Start a temporary private fork` 按钮名、临时私有 Fork 无法运行 CI、`Request CVE` 是 72 小时内审核而非分配、发布公告后 Dependabot 告警需 GitHub 审核且非全覆盖。
- 隐藏评论的原因选项补全，删除不存在的 `disruptive`；敏感内容需删除编辑历史修订。
- All Contributors 类型数（官方现为 33 种）与 key 对应关系；删除写死的作者账号。
- Dependabot：`reviewers` 选项已于 2025-08-08 移除；安全更新需手动开启，并非默认启用。
- `actions/stale` v11 已于 2026-07-28 正式发布，模板升级到 v11.0.0；`github/issue-labeler` 升到 v3.5（Node 24）；`pozil/auto-assign-issue` 升到 v4.1.0；`actions/first-interaction` 版本说明更正。
- 健康检查脚本过滤掉 PR 并分页读取全部 Issue。
- 欢迎机器人与自动分配对 Fork PR 只有只读 Token 的限制已注明。
- Conventional Commits：只有 `feat`／`fix`／破坏性变更有规定的版本段，`docs`／`refactor`／`perf` 不再默认算 PATCH。
- Changelog 生成改用 `gh pr list` 与 `releases/generate-notes`（`git log --merges` 会漏掉 Squash／Rebase 合并）；Changelog 草稿统一为 Keep a Changelog 格式。
- Go 模块 v2+ 需要 `/vN` 路径后缀；X 字数、Hacker News、V2EX 发帖规则补充说明。
- PR 审查补上 Rulesets 与 Merge Queue 一节（入口文件此前声称有，手册里没有）；`mergeable_state` 取值补全。
- CI 的 `actions/checkout` 升到 v7.0.1；Node 20 已停止维护，改用 Python 3.12。
- CHANGELOG 中 1.2.0 条目标题损坏，已修复并补上 1.2.1。
- README（中英文）新增“最新版本”一节；`validate.py` 检查 README 写明当前版本，避免版本信息滞后。

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

## [1.2.1] - 2026-08-22

- 在 SKILL.md 中补充参考手册的阅读时长说明（LK005），使 Release 下载内容与 main 一致。

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
