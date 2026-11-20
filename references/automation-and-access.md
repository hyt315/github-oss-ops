# 访问权限、按需自动化与社区治理

> 适用任务：选择 GitHub 访问方式、按需配置仓库自动化（Stale / Dependabot / CODEOWNERS）、处理社区冲突或贡献者致谢。

## 1. GitHub 访问与最小权限原则

公开仓库的只读扫描与草稿起草**不需要任何 Token**。需要私有数据或写操作时按顺序选路：

1. **官方 GitHub 连接器 / GitHub MCP（OAuth）**：首选，无需人工管理 PAT。
2. **已登录的 GitHub CLI（`gh`）**：先跑 `gh auth status --active`（只查状态，禁止 `--show-token`）。
3. **Fine-grained PAT（仅当无上述通道且用户主动选择）**：仅选目标仓库、设置过期时间、按需赋最小权限（如分流只给 `Issues: Read and write`，不给 `Administration`）；绝不让用户在聊天中粘贴 Token，也不扫描用户主目录或配置文件。
4. **公开 REST 只读兜底**：无认证时用 `curl` 或只读 API 拉取公开信息，写操作改为输出精确命令交给用户执行。

## 2. 按需自动化（只装真正有用的）

中小项目不要盲目堆满机器人（关键词正则自动打标误判高，Welcome Bot 对 Fork PR 会因只读 Token 失败）。最稳妥的按需组合只有两样：

### 2.1 安全的 Stale Bot（只清理 `status:needs-info`，绝不误关已确认 Bug）
```yaml
# 目标仓库 .github/workflows/stale.yml
name: Stale Issues
on:
  schedule:
    - cron: '0 0 * * *'
permissions:
  actions: write
  issues: write
  pull-requests: write
jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@4391f3da665fdf50b6810c1a66712fb9ba21aa93 # v11.0.0
        with:
          any-of-issue-labels: 'status:needs-info'
          days-before-issue-stale: 14
          days-before-issue-close: 14
          stale-issue-label: 'status:stale'
          close-issue-reason: 'not_planned'
          exempt-issue-labels: 'type:security,status:confirmed,priority:P0,priority:P1'
          days-before-pr-stale: 30
          days-before-pr-close: -1
          operations-per-run: 30
          remove-stale-when-updated: true
```

### 2.2 Dependabot（只声明项目里真实存在的生态）
注意：GitHub 已移除 `reviewers` 选项；安全更新需在仓库 Settings 手动开启。给不存在 `package.json`/`pyproject.toml` 的仓库配置 `npm`/`pip` 会导致任务失败。

```yaml
# 目标仓库 .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions-dependencies:
        patterns: ["*"]
```

### 2.3 CODEOWNERS（多人维护时按需添加）
放在 `.github/CODEOWNERS`，按路径指定审查者（如 `* @owner`、`.github/workflows/ @owner`），配合 Rulesets 强制关键路径审查。

## 3. 社区治理与贡献者致谢

- **4 级冲突降温**（每步均需维护者批准）：① 客观说明事实与行为准则 → ② 隐藏违规评论（GitHub 官方原因：`spam` / `abuse` / `off-topic` / `outdated` / `duplicate` / `resolved`；含敏感信息时另删编辑历史）→ ③ 锁定讨论串（Lock conversation）→ ④ 临时屏蔽账号或开启 Interaction limits。
- **贡献者致谢**：Release Notes 中 `@` 致谢所有代码与文档贡献者；需要多类型致谢（文档、设计、复现、翻译等）时可用 All Contributors（官方支持 33 种类型）。
- **赞助配置（可选）**：在 `.github/FUNDING.yml` 配置 GitHub Sponsors 或外部赞助链接，仅在项目有稳定用户群时启用。
