# GitHub Actions 自动化模板

> 开源项目运营常用的 GitHub Actions 工作流模板。SKILL.md Step 9 引用本文件。

---

## 目录

- [Stale Bot（过期管理）](#stale-bot过期管理)
- [Issue Labeler（自动标签）](#issue-labeler自动标签)
- [Welcome Bot（欢迎首次贡献者）](#welcome-bot欢迎首次贡献者)
- [Auto-assign（自动分配）](#auto-assign自动分配)
- [Issue 健康检查](#issue-健康检查)
- [Dependabot（依赖安全）](#dependabot依赖安全)
- [CODEOWNERS（代码所有者）](#codeowners代码所有者)
- [配置说明](#配置说明)

---

## Stale Bot（过期管理）

自动标记和关闭长期无活动的 Issue 和 PR。

```yaml
# .github/workflows/stale.yml
name: Stale Issues

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0:00 运行

permissions:
  actions: write          # 用于工作流状态缓存（有状态运行需要）
  issues: write
  pull-requests: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v10
        with:
          # Issue 配置
          days-before-issue-stale: 30       # 30 天无活动标记 stale
          days-before-issue-close: 14       # 标记后 14 天无活动关闭
          stale-issue-label: 'status:stale'
          stale-issue-message: |
            This issue has been automatically marked as stale because it has had no activity for 30 days.
            If this is still relevant, please provide an update. Otherwise, it will be closed in 14 days.
          close-issue-message: |
            This issue was closed due to inactivity. Feel free to reopen if the issue persists.
          exempt-issue-labels: 'priority:P0,priority:P1,status:in-progress,status:blocked'
          # 仅处理特定类型的 Issue（v10.1+ 支持，可选）
          # only-issue-types: 'Bug,Enhancement'  # 需仓库已启用 Issue 类型功能

          # PR 配置
          days-before-pr-stale: 30
          days-before-pr-close: 14
          stale-pr-label: 'status:stale'
          stale-pr-message: |
            This PR has been marked as stale. Please update if you're still working on it.
          close-pr-message: |
            This PR was closed due to inactivity. Feel free to reopen.
          exempt-pr-labels: 'status:in-progress,status:blocked'

          # 通用配置
          operations-per-run: 30            # 每次最多处理 30 个，避免速率限制
          remove-stale-when-updated: true   # 有新活动时移除 stale 标签
          # sort-by: 'updated'              # 排序方式（v10+ 支持）：updated | created
```

> **版本说明**：`actions/stale@v10` 需要 runner v2.327.1+（Node.js 24）。v9+ 引入了有状态运行——如果因 `operations-per-run` 中断，下次会从中断处继续，全部处理完毕后重置状态。因此调度间隔不宜过短。

### 参数调整建议

| 场景 | days-before-stale | days-before-close | 说明 |
|------|-------------------|-------------------|------|
| 活跃项目 | 14 | 7 | 快速清理，保持 Issue 列表干净 |
| 一般项目（推荐） | 30 | 14 | 平衡，给用户足够时间 |
| 低频项目 | 60 | 30 | 宽松，避免误关 |
| 问题类 Issue | 7 | 7 | 快速关闭已解答的问题 |

---

## Issue Labeler（自动标签）

根据 Issue 内容自动添加标签。使用 `github/issue-labeler` 或 `actions/labeler`。

### 配置文件

```yaml
# .github/labeler.yml（Issue Labeler 配置）
# 根据 Issue 正文中的关键词自动添加标签

# Bug 相关
type:bug:
  - '(bug|crash|error|错误|崩溃|不工作|无法|失败|异常|卡死)'

# 功能请求
type:enhancement:
  - '(feature|request|suggestion|建议|希望|能不能|新增|支持|功能请求)'

# 使用问题
type:question:
  - '(question|how to|怎么|如何|请问|求助|为什么)'

# 文档
type:documentation:
  - '(docs|documentation|readme|文档|typo|错别字|说明不清)'
```

### GitHub Actions 工作流

```yaml
# .github/workflows/labeler.yml
name: Issue Labeler

on:
  issues:
    types: [opened, edited]

permissions:
  issues: write

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: github/issue-labeler@v3.4
        with:
          configuration-path: .github/labeler.yml
          enable-versioned-regex: 0
          sync-labels: 1               # v3.0+ 默认不移除不匹配的标签，设为 1 启用同步
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

> **注意**：`github/issue-labeler@v3.0` 引入了破坏性变更——默认不再移除不匹配正则的已有标签。如需自动同步（移除不匹配的标签），必须设置 `sync-labels: 1`。`on` 触发器建议同时包含 `opened` 和 `edited`，这样 Issue 编辑后也会重新匹配。

---

## Welcome Bot（欢迎首次贡献者）

自动欢迎首次提交 Issue 或 PR 的贡献者。

```yaml
# .github/workflows/welcome.yml
name: Welcome Contributors

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

permissions:
  issues: write
  pull-requests: write

jobs:
  welcome:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/first-interaction@v3
        with:
          issue_message: |
            ## Welcome! 👋

            Thanks for opening your first issue in this project!

            A few tips:
            - Please make sure you've searched existing issues to avoid duplicates
            - Check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
            - Be patient — maintainers will review your issue as soon as possible

            We appreciate your contribution!
          pr_message: |
            ## Welcome! 👋

            Thanks for your first pull request!

            A few things to check:
            - [ ] Tests pass locally
            - [ ] Code follows the project's style guide
            - [ ] Documentation is updated (if applicable)
            - [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)

            A maintainer will review your PR soon. Thanks for contributing!
```

> **版本说明**：`actions/first-interaction@v3` 相比 v1 有以下破坏性变更：
> - 参数名从 `issue-message`/`pr-message` 改为 `issue_message`/`pr_message`（下划线替代连字符）
> - PR 触发器从 `pull_request_target` 改为 `pull_request`（更安全，避免 token 权限泄露风险）
> - 不再需要 `repo-token` 参数，默认使用 `GITHUB_TOKEN`
> - 需要 runner v2.327.1+（Node.js 24）

### 自定义欢迎信息要点

- 感谢贡献者的时间和努力
- 提供有用的链接（CONTRIBUTING.md、文档、Code of Conduct）
- 说明接下来会发生什么（审查流程、预期时间）
- 语气友好，不要居高临下

---

## Auto-assign（自动分配）

自动将新 Issue 或 PR 分配给维护者。

```yaml
# .github/workflows/auto-assign.yml
name: Auto Assign

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

permissions:
  issues: write
  pull-requests: write

jobs:
  assign:
    runs-on: ubuntu-latest
    steps:
      - uses: pozil/auto-assign-issue@v4
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          assignees: your-github-username   # 替换为你的 GitHub 用户名
          numOfAssignee: 1
```

### 多人轮询分配

如果有多个维护者，可以用轮询（round-robin）方式分配：

```yaml
      - uses: pozil/auto-assign-issue@v4
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          assignees: user1, user2, user3
          numOfAssignee: 1
          allowSelfAssign: true
```

> **版本说明**：`pozil/auto-assign-issue@v4` 需要 runner v2.327.1+（Node.js 24）。v3+ 切换至 ES Module，v4 增加 Node 24 支持。PR 触发器建议使用 `pull_request` 而非 `pull_request_target`（安全考虑）。

---

## Issue 健康检查

定期检查 Issue 列表健康度，生成报告。

```yaml
# .github/workflows/issue-health.yml
name: Issue Health Check

on:
  schedule:
    - cron: '0 9 * * 1'  # 每周一 9:00 UTC
  workflow_dispatch:        # 支持手动触发

permissions:
  issues: read

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check issue health
        uses: actions/github-script@v9
        with:
          script: |
            const { data: issues } = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              per_page: 100
            });

            const now = new Date();
            const needsTriage = issues.filter(i =>
              !i.labels.length || i.labels.some(l => l.name === 'status:needs-triage')
            );
            const stale = issues.filter(i =>
              (now - new Date(i.updated_at)) / (1000 * 60 * 60 * 24) > 30
            );
            const needsInfo = issues.filter(i =>
              i.labels.some(l => l.name === 'status:needs-info')
            );

            console.log(`## Issue Health Report`);
            console.log(`- Open issues: ${issues.length}`);
            console.log(`- Needs triage: ${needsTriage.length}`);
            console.log(`- Stale (>30 days): ${stale.length}`);
            console.log(`- Needs info: ${needsInfo.length}`);

            if (needsTriage.length > 0) {
              console.log(`\n### Needs Triage:`);
              needsTriage.forEach(i => console.log(`- #${i.number}: ${i.title}`));
            }
```

---

## Dependabot（依赖安全）

自动检测依赖中的安全漏洞并创建 PR 修复。开源项目强烈建议启用。

```yaml
# .github/dependabot.yml
version: 2

updates:
  # npm 依赖（根据项目实际包管理器调整 ecosystem）
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"          # 每周检查一次
      day: "monday"
    open-pull-requests-limit: 10  # 同时最多 10 个 PR
    labels:
      - "type:security"
      - "dependencies"
    commit-message:
      prefix: "deps"              # 提交信息前缀
    reviewers:
      - "your-github-username"    # 审查者

  # GitHub Actions 版本更新
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "type:security"
      - "dependencies"
```

### 支持的包生态系统

| ecosystem | 对应文件 |
|-----------|----------|
| `npm` | `package.json` / `package-lock.json` |
| `pip` | `requirements.txt` / `pyproject.toml` |
| `cargo` | `Cargo.toml` / `Cargo.lock` |
| `go` | `go.mod` / `go.sum` |
| `maven` | `pom.xml` |
| `gradle` | `build.gradle` |
| `composer` | `composer.json` |
| `docker` | `Dockerfile` |
| `github-actions` | `.github/workflows/*.yml` |

> **安全更新 vs 版本更新**：Dependabot 安全更新默认对所有公开仓库免费启用，无需配置。上方 YAML 配置的是版本更新（主动保持依赖最新）。安全更新会在检测到漏洞时自动创建 PR。

---

## CODEOWNERS（代码所有者）

自动根据文件路径请求特定维护者审查 PR。与分支保护规则配合使用效果最佳。

```bash
# .github/CODEOWNERS
# 格式：文件路径模式  @用户名 或 @组织/团队名

# 默认所有者（兜底）
*                           @your-github-username

# 按目录分配
/src/core/                  @your-github-username @core-maintainer
/src/ui/                    @ui-maintainer
/docs/                      @docs-maintainer

# 按文件类型分配
*.md                        @docs-maintainer
package.json                @your-github-username
Cargo.toml                  @your-github-username

# GitHub 相关配置
.github/                    @your-github-username
```

### 配合分支保护使用

在仓库 Settings → Branches → Branch protection rules 中：
1. 选择需要保护的分支（如 `main`）
2. 勾选 **Require pull request reviews before merging**
3. 勾选 **Require review from Code Owners**

这样，当 PR 修改了 CODEOWNERS 中匹配的文件时，会自动请求对应维护者审查。

> CODEOWNERS 文件也可放在仓库根目录，但 `.github/CODEOWNERS` 优先级更高。

---

## 配置说明

### 如何选择自动化

| 项目规模 | 建议配置 |
|----------|----------|
| 个人项目（< 10 Issue/月） | Stale Bot + Dependabot |
| 小型项目（10-50 Issue/月） | Stale Bot + Issue Labeler + Welcome Bot + Dependabot + CODEOWNERS |
| 中型项目（> 50 Issue/月） | 全部配置 + 自定义规则 |

### 文件放置位置

所有工作流文件放在 `.github/workflows/` 目录下：

```
.github/
├── workflows/
│   ├── stale.yml          # Stale Bot
│   ├── labeler.yml        # Issue Labeler
│   ├── welcome.yml        # Welcome Bot
│   ├── auto-assign.yml    # Auto-assign
│   └── issue-health.yml   # 健康检查
├── labeler.yml            # Labeler 规则配置
├── dependabot.yml         # Dependabot 配置
├── CODEOWNERS             # 代码所有者配置
└── ISSUE_TEMPLATE/        # Issue 模板（oss-prep 已处理）
```

### GitHub Token 权限

这些工作流只需要 `GITHUB_TOKEN`（GitHub Actions 自动提供的 Token），不需要额外的 PAT。权限设置已在每个 YAML 中通过 `permissions` 字段声明。
