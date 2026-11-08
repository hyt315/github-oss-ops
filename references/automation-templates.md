# GitHub Actions 自动化模板

> 适用任务：为目标仓库配置 Stale、自动打标、欢迎、自动分配与 Dependabot。以下 YAML 是写进**目标仓库**的模板，落盘前须经用户批准。

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

只清理“等用户补充信息却一直没回”的 Issue，不碰已确认的 Bug。原因见 [避坑指南 §4.1](github-oss-ops-pitfalls.md#41-stale-机器人误伤)。

> **版本（2026-11-08 核对）**：`actions/stale` 最新为 v11.0.0（2026-07-28 发布，内部改为 ESM，输入不变），需要 runner v2.327.1+。

```yaml
# 目标仓库 .github/workflows/stale.yml
name: Stale Issues

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0:00

permissions:
  actions: write          # 保存跨次运行状态
  issues: write
  pull-requests: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@4391f3da665fdf50b6810c1a66712fb9ba21aa93 # v11.0.0
        with:
          # Issue：只处理等待补充信息的
          any-of-issue-labels: 'status:needs-info'
          days-before-issue-stale: 14
          days-before-issue-close: 14
          stale-issue-label: 'status:stale'
          stale-issue-message: |
            This issue is waiting for more information and has had no activity for 14 days.
            Please add the requested details. It will be closed in 14 days otherwise, and you can reopen it at any time.
          close-issue-message: |
            Closing for now because the requested information was not provided. Reply or reopen whenever you can share it.
          close-issue-reason: 'not_planned'
          exempt-issue-labels: 'type:security,status:confirmed,status:in-progress,priority:P0,priority:P1'

          # PR：只提醒，不自动关闭
          days-before-pr-stale: 30
          days-before-pr-close: -1
          stale-pr-label: 'status:stale'
          stale-pr-message: |
            This PR has had no activity for 30 days. Please update it if you are still working on it.
          exempt-pr-labels: 'status:in-progress,status:blocked'

          operations-per-run: 30            # 每次最多处理 30 个，避免限流
          remove-stale-when-updated: true
          # sort-by: 'created'              # 可选 created（默认）| updated | comments
```

> **说明**：v9 起支持跨次运行续跑：被 `operations-per-run` 截断后，下次从中断处继续，全部处理完再重置。所以调度不宜过密。`days-before-*-close: -1` 表示永不自动关闭。

### 参数调整建议

针对 `status:needs-info` 的 Issue：

| 场景 | days-before-issue-stale | days-before-issue-close | 说明 |
|------|-------------------|-------------------|------|
| 活跃项目 | 7 | 7 | 维护者响应快，用户也该快 |
| 一般项目（推荐） | 14 | 14 | 给用户足够时间 |
| 低频项目 | 30 | 30 | 宽松，避免误关 |

不建议对全部 Issue 开启自动关闭；确需清理老旧积压时，先人工过一遍。

---

## Issue Labeler（自动标签）

按 Issue 标题和正文里的关键词自动打类型标签，用 `github/issue-labeler`。

> `actions/labeler` 是给 **PR 按改动文件路径**打标签的，不能按关键词给 Issue 打标签；两者默认都读 `.github/labeler.yml` 但格式不同，所以这里把配置放在 `.github/issue-labeler.yml`，避免冲突。

### 配置文件

```yaml
# 目标仓库 .github/issue-labeler.yml
# 正则匹配 Issue 标题与正文

type:bug:
  - '(bug|crash|error|错误|崩溃|不工作|无法|失败|异常|卡死)'

type:enhancement:
  - '(feature|request|suggestion|建议|希望|能不能|新增|支持|功能请求)'

type:question:
  - '(question|how to|怎么|如何|请问|求助|为什么)'

type:documentation:
  - '(docs|documentation|readme|文档|typo|错别字|说明不清)'
```

### GitHub Actions 工作流

```yaml
# 目标仓库 .github/workflows/issue-labeler.yml
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
      - uses: github/issue-labeler@ccca1e16fcb66762200e616fc29b57b940c1cb67 # v3.5
        with:
          configuration-path: .github/issue-labeler.yml
          include-title: 1
          enable-versioned-regex: 0
          sync-labels: 0               # 不移除人工打的标签
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

> **注意**：v3.0 起默认不移除不匹配的已有标签。`sync-labels: 1` 会删掉人工分流时加的类型标签，除非完全交给机器人，否则保持 `0`。关键词匹配误判较多，结果仍需人工复核。

---

## Welcome Bot（欢迎首次贡献者）

自动欢迎首次提交 Issue 或 PR 的贡献者。

```yaml
# 目标仓库 .github/workflows/welcome.yml
name: Welcome Contributors

on:
  issues:
    types: [opened]
  pull_request:              # 注意：来自 Fork 的 PR 只有只读 Token，欢迎评论会失败
    types: [opened]

permissions:
  issues: write
  pull-requests: write

jobs:
  welcome:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/first-interaction@1c4688942c71f71d4f5502a26ea67c331730fa4d # v3.1.0
        with:
          issue_message: |
            ## Welcome! 👋

            Thanks for opening your first issue in this project!

            A few tips:
            - Please make sure you've searched existing issues to avoid duplicates
            - Check [CONTRIBUTING.md](https://github.com/${{ github.repository }}/blob/${{ github.event.repository.default_branch }}/CONTRIBUTING.md) for guidelines
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

> **版本说明（2026-11-08 核对）**：
> - 参数名在 **v2.0.0** 起改为下划线：`issue_message`／`pr_message`／`repo_token`；
> - `repo_token` 默认取 `github.token`，一般不用填；
> - v3 的破坏性变更只有一条：需要 runner v2.327.1+（Node.js 24）。
>
> **Fork PR 的限制**：`pull_request` 触发时，Fork 来的 PR 拿到的是只读 `GITHUB_TOKEN`，无法评论，所以首次贡献者的 Fork PR 收不到欢迎语。不要为此改用 `pull_request_target` 并检出代码（见 [避坑指南 §2.1](github-oss-ops-pitfalls.md#21-pull_request_target--检出-pr-代码)）。只发评论、不检出代码的话，`pull_request_target` 是安全的，可以单独给 PR 欢迎建一个这样的工作流。

### 自定义欢迎信息要点

- 感谢贡献者的时间和努力
- 提供有用的链接（CONTRIBUTING.md、文档、Code of Conduct）
- 说明接下来会发生什么（审查流程、预期时间）
- 语气友好，不要居高临下

---

## Auto-assign（自动分配）

自动将新 Issue 或 PR 分配给维护者。

```yaml
# 目标仓库 .github/workflows/auto-assign.yml
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
      - uses: pozil/auto-assign-issue@d6e511896e5f1d2408e74db74416647d8ff80c8c # v4.1.0
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          assignees: your-github-username   # 替换为你的 GitHub 用户名
          numOfAssignee: 1
```

### 多人轮询分配

如果有多个维护者，可以用轮询（round-robin）方式分配：

```yaml
      - uses: pozil/auto-assign-issue@d6e511896e5f1d2408e74db74416647d8ff80c8c # v4.1.0
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          assignees: user1, user2, user3
          numOfAssignee: 1
          allowSelfAssign: true
```

> **版本说明**：`pozil/auto-assign-issue` v4 运行在 Node.js 24，需要 runner v2.327.1+。与欢迎机器人一样，Fork PR 在 `pull_request` 下只有只读 Token，自动分配会失败；可只对 Issue 启用，PR 交给 CODEOWNERS 自动请求审查。

---

## Issue 健康检查

定期检查 Issue 列表健康度，生成报告。

```yaml
# 目标仓库 .github/workflows/issue-health.yml
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
        uses: actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3 # v9.0.0
        with:
          script: |
            // listForRepo 会把 PR 一起返回，需要过滤；paginate 取全部页
            const all = await github.paginate(github.rest.issues.listForRepo, {
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              per_page: 100
            });
            const issues = all.filter(i => !i.pull_request);

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
# 目标仓库 .github/dependabot.yml
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
      - "dependencies"
    commit-message:
      prefix: "deps"              # 提交信息前缀
    # 审查者改由 CODEOWNERS 决定：`reviewers` 选项已于 2025-08-08 移除

  # GitHub Actions 版本更新
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
```

> 版本更新 PR 不一定是安全修复，所以不默认打 `type:security`。

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

> **安全更新 vs 版本更新**：上方 YAML 配置的是**版本更新**。**安全更新**不靠这个文件，需要在 `Settings` 的安全设置中依次开启依赖图（Dependency graph）、Dependabot alerts 和 Dependabot security updates，之后检测到漏洞时会自动开修复 PR。

---

## CODEOWNERS（代码所有者）

自动根据文件路径请求特定维护者审查 PR。与分支保护规则配合使用效果最佳。

```bash
# 目标仓库 .github/CODEOWNERS
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

### 配合分支规则使用

推荐用 Rulesets（`Settings → Rules → Rulesets`）给 `main` 建分支规则集，开启 **Require a pull request before merging**，再勾选 **Require review from Code Owners**。经典分支保护（`Settings → Branches`）里的同名选项效果相同。

这样，当 PR 修改了 CODEOWNERS 中匹配的文件时，会自动请求对应维护者审查。

> CODEOWNERS 可放在 `.github/`、仓库根目录或 `docs/`，GitHub 按这个顺序查找，用第一个找到的。

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
│   ├── issue-labeler.yml  # Issue Labeler
│   ├── welcome.yml        # Welcome Bot
│   ├── auto-assign.yml    # Auto-assign
│   └── issue-health.yml   # 健康检查
├── issue-labeler.yml      # Issue Labeler 关键词规则
├── dependabot.yml         # Dependabot 配置
├── CODEOWNERS             # 代码所有者配置
└── ISSUE_TEMPLATE/        # Issue 模板（github-oss-prep 已处理）
```

### GitHub Token 权限

这些工作流只需要 `GITHUB_TOKEN`（GitHub Actions 自动提供的 Token），不需要额外的 PAT。权限设置已在每个 YAML 中通过 `permissions` 字段声明。
