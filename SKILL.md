---
name: github-oss-ops
version: 1.0.0
description: Use when managing open source GitHub repositories — covers Issue triage, smart replies, PR review assistance, version/release management, stale management, and operations reporting. Triggers: Issue 管理、分流、triage、看看有没有新 Issue、PR 审查、回复 Issue、版本号、发版、Release、changelog、过期 Issue、stale、运营报告、开源项目运营、oss ops、project operations.
---

# GitHub 开源项目运营

开源发布后的项目"AI 客服"：自动扫描 Issue/PR，智能分类、生成回复草稿、辅助审查、管理过期项、输出运营报告。

## 核心理念

- **只起草，不发送**：所有回复和标签操作都先展示给用户确认，明确同意才执行
- **维护者视角**：帮助个人维护者或小型团队高效管理项目，降低维护负担
- **渐进式运营**：不需要一次配置全部，按需使用各功能模块
- **与 github-oss-prep 配合**：oss-prep 负责发布，本技能负责发布后的日常运营

---

## 前置条件

需要 GitHub 访问凭据（三选一）：

1. **GitHub PAT**（推荐 Fine-grained PAT，Classic PAT 亦可）
   - Fine-grained PAT（`github_pat_` 前缀）：可限定仓库和权限，更安全
   - Classic PAT（`ghp_` 前缀）：需 `repo` 权限，配置最简单
2. **GitHub MCP 工具**（推荐）：官方 `github/github-mcp-server`，通过 Docker 运行
   - 可用工具：`list_issues`、`get_issue`、`update_issue`、`add_issue_comment` 等
3. **GitHub CLI（`gh`）**：安装 `gh` 并执行 `gh auth login`，适合交互式操作
4. **curl + REST API**：以上均不可用时的回退方案

配置方式（PAT）：
- 环境变量：设置 `GITHUB_TOKEN` 或 `GITHUB_PERSONAL_ACCESS_TOKEN`
- MCP Server 配置文件：将 PAT 填入对应工具的 `env` 中

详细的 PAT 生成步骤（含 Fine-grained PAT）、各工具 MCP 配置模板、GitHub CLI 用法、MCP 工具清单和 curl + REST API 回退方案，参见 [references/github-access-guide.md](references/github-access-guide.md)。

---

## 工作流程

```
Step 1: 确认目标仓库
    ↓
Step 2: 扫描（Issue/PR 状态概览）
    ↓
Step 3: Issue 分流（分类 + 标记 + 优先级评估）
    ↓
Step 4: 智能回复（生成回复草稿 → 用户确认 → 发送）
    ↓
Step 5: PR 审查辅助（读改动 + 生成审查意见）
    ↓
Step 6: 版本管理（PR 合并后 → semver 版本更新 → Release）
    ↓
Step 7: 过期管理（Stale Issue/PR 处理）
    ↓
Step 8: 运营报告（统计 + 健康评估 + 建议）
    ↓
Step 9: 自动化配置（按需生成 GitHub Actions 模板）
```

> 每一步都是独立可用的。用户可能只需要"帮我看看有没有新 Issue"（Step 2-3），不需要走完全流程。

---

## Step 1: 确认目标仓库

如果用户没有指定仓库名，通过以下方式确认：

1. 检查当前工作目录是否是 git 仓库（`git remote -v`）
2. 如果是，提取 `owner/repo` 信息
3. 如果不是，询问用户要管理哪个仓库

确认仓库后，检查仓库是否为公开仓库（本技能面向开源项目）。

---

## Step 2: 扫描项目状态

### 2.1 获取 Issue/PR 概览

通过 MCP 工具或 API 获取以下数据：

| 数据 | 获取方式 |
|------|----------|
| 未关闭的 Issue 列表 | `list_issues`（state: open）或 `GET /repos/{owner}/{repo}/issues` |
| 未关闭的 PR 列表 | `list_pull_requests`（state: open）或 `GET /repos/{owner}/{repo}/pulls` |
| 最近 7 天的新 Issue | 按 `created_at` 过滤 |
| 最近 7 天的新 PR | 按 `created_at` 过滤 |
| 需要回复的 Issue | 无维护者评论的 open Issue |

### 2.2 输出状态摘要

```
## 仓库状态概览 — {owner}/{repo}

### 数据总览
- 未关闭 Issue：N 个（其中 N 个待分流）
- 未关闭 PR：N 个（其中 N 个待审查）
- 最近 7 天新增：N 个 Issue，N 个 PR

### 需要关注
- [ ] N 个 Issue 没有任何标签（待分流）
- [ ] N 个 Issue 超过 7 天未回复
- [ ] N 个 PR 等待审查
```

### 2.3 检查已有标签体系

读取仓库现有标签（`GET /repos/{owner}/{repo}/labels`），判断是否需要建立或优化标签体系。如果标签混乱或缺失，建议进入 Step 8 先配置标签体系。

---

## Step 3: Issue 分流

> **核心操作**：读取每个未分流的 Issue → 分类 → 建议标签和优先级 → 展示给用户确认 → 执行标记。

### 3.1 分类规则

读取 Issue 的标题和正文，根据以下信号判断类型：

| 信号 | 分类 | 建议标签 |
|------|------|----------|
| 提到"bug""错误""crash""不工作""无法" | Bug | `type:bug` |
| 提到"建议""希望""能不能""feature" | 功能请求 | `type:enhancement` |
| 提到"怎么""如何""请问""求助" | 使用问题 | `type:question` |
| 提到"文档""README""说明" | 文档改进 | `type:documentation` |
| 提到"漏洞""安全""security""vulnerability""XSS""SQL注入" | 安全漏洞 | `type:security` + `priority:P0` |
| 提到"重构""refactor""优化代码结构" | 重构 | `type:refactor` |
| 提到"性能""慢""卡顿""performance""优化速度" | 性能问题 | `type:performance` |
| 信息不足，无法判断 | 需要更多信息 | `status:needs-info` |

### 3.2 安全漏洞特殊处理

**安全漏洞 Issue 不走常规分流流程**，需要特殊处理：

1. 标记 `type:security` + `priority:P0`
2. 不在公开评论中确认或讨论漏洞细节
3. 引导提交者使用 GitHub Private Vulnerability Reporting
4. 关闭公开 Issue（或转为私密）
5. 在 Security Advisory 中跟踪

> 详细的安全漏洞处理流程和垃圾 Issue 处理见 `references/triage-workflow.md`。

### 3.3 优先级评估

| 优先级 | 判断标准 | 建议标签 |
|--------|----------|----------|
| **P0 紧急** | 影响核心功能、安全漏洞、数据丢失 | `priority:P0` |
| **P1 重要** | 影响较多用户、有明确的修复方案 | `priority:P1` |
| **P2 一般** | 小问题、体验优化、不紧急 | `priority:P2` |
| **P3 低** | 锦上添花、小众需求 | `priority:P3` |

### 3.4 重复检测

对每个新 Issue，在已有 Issue 中搜索相似标题和关键词。如果发现疑似重复：
- 标出疑似重复的 Issue 编号
- 建议关闭并引用原始 Issue

### 3.5 分流结果展示

逐个 Issue 展示分析结果：

```
### Issue #{number}: {title}
- 提交者：@{user}（首次贡献 / 活跃贡献者）
- 分类：Bug / 功能请求 / 使用问题 / 文档 / 需要更多信息
- 建议优先级：P1
- 建议标签：type:bug, priority:P1
- 疑似重复：无 / 可能是 #{other_number} 的重复
- 建议操作：标记标签 + 回复 / 关闭 / 转 Discussion
```

**用户确认后**，调用 `update_issue` 添加标签，或调用 `add_issue_comment` 添加回复。

> 详细的标签体系、分流决策树和边界情况处理见 `references/triage-workflow.md`。

---

## Step 4: 智能回复

> **核心原则**：生成回复草稿 → 展示给用户 → 用户确认或修改 → 才调用 `add_issue_comment` 发送。

### 4.1 回复场景判断

| Issue 类型 | 回复策略 |
|------------|----------|
| Bug（可复现） | 确认问题 + 说明下一步（已在修复 / 需要更多信息） |
| Bug（不可复现） | 请求环境信息（OS、版本、复现步骤） |
| 功能请求（合理） | 感谢建议 + 评估可行性 + 标记 `help wanted` 或加入计划 |
| 功能请求（不合适） | 礼貌拒绝 + 说明原因（不在项目范围内） |
| 使用问题 | 给出解答 + 引导到文档或 Discussion |
| 重复 Issue | 引用原始 Issue + 关闭 |
| 安全漏洞 | 引导使用 Private Vulnerability Reporting + 关闭公开 Issue |
| 首次贡献者 | 额外感谢 + 引导到 CONTRIBUTING.md |

### 4.2 回复语言

- Issue 是中文 → 用中文回复
- Issue 是英文 → 用英文回复
- Issue 混合语言 → 用主要语言回复

### 4.3 回复质量要求

- 语气友好、专业，不居高临下
- 给出具体的下一步（不是"我们看看"）
- 引用具体的文档或 Issue 编号
- 首次贡献者要额外表示欢迎

> 各场景的完整回复模板见 `references/response-templates.md`。

---

## Step 5: PR 审查辅助

### 5.1 PR 改动分析

对每个待审查的 PR：

1. 读取 PR 描述和关联的 Issue
2. 通过 `get_pull_request_files` 获取改动文件列表
3. 检查 CI/CD 状态（通过 `get_pull_request_status` 或 API 获取检查结果）
4. 检查可合并状态（`mergeable` / `mergeable_state`）
5. 分析改动类型（bug fix / feature / docs / refactor）
6. 检查常见质量问题（硬编码、缺少测试、破坏性变更）

### 5.2 生成审查意见

输出审查摘要供维护者参考：

```
### PR #{number}: {title}
- 提交者：@{user}（首次贡献 / 活跃贡献者）
- 关联 Issue：#{number} / 无
- 改动范围：N 个文件，+X / -Y 行
- 改动类型：Bug Fix / Feature / Docs / Refactor
- CI/CD 状态：✅ 全部通过 / ❌ 有失败 / ⏳ 进行中
- 可合并状态：✅ 无冲突 / ⚠️ 有冲突 / 🔒 被阻塞

#### 自动检查
- [ ] CI/CD 检查是否全部通过
- [ ] 是否包含测试（如适用）
- [ ] 是否有破坏性变更
- [ ] 是否更新了文档（如适用）
- [ ] 代码风格是否一致
- [ ] CODEOWNERS 审查是否完成（如配置了 CODEOWNERS）

#### 建议
- [列出具体建议]

#### 建议操作
- 批准并合并 / 需要修改 / 拒绝（说明原因）
```

**用户确认后**，调用 `create_pull_request_review` 提交审查，或 `merge_pull_request` 合并。

> PR 审查的详细检查清单和常见问题见 `references/pr-review-guide.md`。

---

## Step 6: 版本管理（PR 合并后）

> **触发时机**：PR 合并后，或用户主动要求发版时执行。此步骤为可选步骤。

### 6.1 判断版本变更类型

根据合并的 PR 类型，按 semver 规则建议版本段：

| PR 改动类型 | semver 版本段 | 示例 |
|------------|--------------|------|
| Bug Fix（`type:bug`） | patch（x.x.+1） | 1.2.3 → 1.2.4 |
| 功能新增（`type:enhancement`） | minor（x.+1.0） | 1.2.3 → 1.3.0 |
| 破坏性变更（breaking change） | major（+1.0.0） | 1.2.3 → 2.0.0 |
| 文档/重构/性能（无 API 变更） | patch（x.x.+1） | 1.2.3 → 1.2.4 |
| 安全修复（`type:security`） | patch 或 minor | 视影响范围决定 |

### 6.2 读取当前版本

自动检测项目的版本文件和当前版本号：

| 项目类型 | 版本文件 |
|----------|----------|
| Node.js / npm | `package.json` → `version` 字段 |
| Python | `pyproject.toml` → `version` 或 `__init__.py` → `__version__` |
| Rust | `Cargo.toml` → `version` 字段 |
| Go | `go.mod` 无版本，通过 git tag 管理 |
| Java | `pom.xml` → `<version>` 或 `build.gradle` → `version` |
| 通用 | git tag（`v*.*.*`） |

### 6.3 生成版本更新方案

```
### 版本更新建议

- 当前版本：v1.2.3
- 合并的 PR：
  - #42 fix: 修复登录超时问题（patch）
  - #45 feat: 新增导出功能（minor）
- 建议新版本：v1.3.0（取最高版本段）
- 版本文件：`package.json`

### Changelog 草稿

## v1.3.0 (2026-06-20)

### Features
- 新增导出功能 (#45) by @contributor

### Bug Fixes
- 修复登录超时问题 (#42) by @contributor
```

### 6.4 执行版本更新

**用户确认后**，按顺序执行：

1. 更新版本文件（通过 `create_or_update_file` 推送）
2. 更新所有版本号声明位置（见下方同步清单）
3. 创建 git tag（通过 API 或本地 `git tag`）
4. 创建 GitHub Release（通过 API，附上 changelog）

### 6.5 版本号同步清单

版本号必须在以下所有位置保持一致，漏一个就会让用户看到不一致的版本号：

| # | 位置 | 具体内容 | 作用 |
|---|------|----------|------|
| 1 | 版本文件 | `package.json` / `pyproject.toml` / `Cargo.toml` 等 | 包管理器识别 |
| 2 | README 徽章 | shields.io 版本徽章（如 `version-1.1.0-green`） | 项目首页展示 |
| 3 | SKILL.md frontmatter | `version: 1.1.0`（如果是 Skill 项目） | Agent 识别用 |
| 4 | Git tag | `git tag -a v1.1.0` | GitHub Tags 页面 |
| 5 | GitHub Release | 基于 tag 创建 | Releases 正式发布页 |

> tag 和 Release 是两回事：tag 只是指针，Release 是带说明的发布页面。两者都需要创建。

> 详细的 semver 规则、多语言版本文件模板、GitHub Release 创建流程和 changelog 规范见 `references/release-workflow.md`。

---

## Step 7: 过期管理

### 7.1 识别过期 Issue/PR

筛选条件（可调整）：

| 类型 | 判定标准 | 对应自动化参数 |
|------|----------|----------------|
| 过期 Issue | open 状态 + 30 天无活动 | `days-before-issue-stale: 30` |
| 等待反馈的 Issue | 标记 `status:needs-info` + 14 天无回复 | 需单独配置（见下方说明） |
| 过期 PR | open 状态 + 30 天无活动 | `days-before-pr-stale: 30` |
| 使用问题 | 标记 `type:question` + 7 天无回复 | 需单独配置（见下方说明） |

> **手动 vs 自动化的差异**：`actions/stale` 默认对所有 Issue 使用统一的时间参数。如需按类型差异化处理（如使用问题 7 天、等待反馈 14 天），有两种方案：
> 1. **多工作流方案**：为不同类型配置独立的 stale 工作流，通过 `only-issue-types` 或标签过滤
> 2. **简化方案**：统一使用 30+14 天，手动处理特殊类型（本技能默认推荐）

### 7.2 处理策略

| 类型 | 建议操作 |
|------|----------|
| 过期 Bug | 提醒维护者关注，不自动关闭 |
| 过期功能请求 | 提醒 + 询问是否仍需要 |
| 过期使用问题 | 提醒一次，再过 7 天关闭，标记 `resolution:no-response` |
| 等待反馈无回复 | 提醒一次，再过 14 天关闭，标记 `resolution:no-response` |
| 过期 PR | 提醒提交者更新，或建议维护者接管 |

**所有操作都先展示给用户确认，不自动关闭任何 Issue。**

### 6.3 关闭时的规范

关闭 Issue 时，评论中说明关闭原因，并附上：
- 如问题已解决：引用修复的 commit 或 PR
- 如无法复现：说明已尝试的环境
- 如无回复：说明曾多次提醒

---

## Step 8: 运营报告

### 8.1 报告数据

通过 API 统计以下指标：

| 指标 | 说明 |
|------|------|
| 新 Issue 数 | 报告周期内新增 |
| 关闭 Issue 数 | 报告周期内关闭 |
| 平均响应时间 | 从 Issue 创建到首次维护者回复的时间 |
| 平均解决时间 | 从 Issue 创建到关闭的时间（MTTR） |
| Issue 关闭率 | 关闭数 / 新增数（衡量积压趋势） |
| 新 PR 数 | 报告周期内新增 |
| 合并 PR 数 | 报告周期内合并 |
| PR 合并率 | 合并数 / 新增数 |
| 未关闭 Issue 总数 | 当前积压 |
| 贡献者数 | 报告周期内有贡献的人数 |
| 首次贡献者数 | 报告周期内首次贡献的人数 |
| Star/Fork 变化 | 报告周期内的增长 |

### 8.2 报告模板

```
## 运营报告 — {owner}/{repo}
报告周期：{start_date} ~ {end_date}

### 数据概览
| 指标 | 本期 | 上期 | 变化 |
|------|------|------|------|
| 新 Issue | N | N | +X% |
| 关闭 Issue | N | N | -X% |
| Issue 关闭率 | X% | X% | +X% |
| 平均响应时间 | Xh | Xh | 改善/恶化 |
| 平均解决时间 | Xd | Xd | 改善/恶化 |
| 新 PR | N | N | +X% |
| 合并 PR | N | N | -X% |
| PR 合并率 | X% | X% | +X% |
| 首次贡献者 | N | N | +X% |
| Star | +N | +N | +X% |

### 健康评估
- Issue 响应时间：良好（<24h）/ 一般（1-3天）/ 需改进（>3天）
- Issue 积压：健康（<10）/ 一般（10-30）/ 过多（>30）
- PR 积压：健康（<5）/ 一般（5-15）/ 过多（>15）
- Issue 关闭率：健康（>80%）/ 一般（50-80%）/ 需改进（<50%）

### 建议
- [根据数据给出具体建议]
```

### 8.3 报告周期

默认生成最近 7 天的周报，用户可指定：
- `周报`：最近 7 天
- `月报`：最近 30 天
- `自定义`：指定起止日期

---

## Step 9: 自动化配置

> 按需为用户的项目生成 GitHub Actions 工作流文件，减少手动重复操作。

### 9.1 可配置的自动化

| 自动化 | 功能 | 生成文件 |
|--------|------|----------|
| Stale Bot | 自动标记/关闭过期 Issue | `.github/workflows/stale.yml` |
| Issue Labeler | 根据 Issue 内容自动添加标签 | `.github/workflows/labeler.yml` + `.github/labeler.yml` |
| Welcome Bot | 欢迎首次贡献者 | `.github/workflows/welcome.yml` |
| Auto-assign | 自动分配 Issue/PR 给维护者 | `.github/workflows/auto-assign.yml` |
| Dependabot | 依赖安全更新和版本更新 | `.github/dependabot.yml` |
| CODEOWNERS | 按文件路径自动请求审查 | `.github/CODEOWNERS` |

### 9.2 配置流程

1. 询问用户需要哪些自动化
2. 根据项目类型和现有配置生成适合的参数
3. 展示生成的 YAML 文件内容
4. 用户确认后，写入项目目录或推送到仓库

> 完整的 GitHub Actions YAML 模板和参数说明见 `references/automation-templates.md`。

### 9.3 标签体系初始化

如果项目缺少标准标签体系，建议先创建以下基础标签：

| 标签 | 颜色 | 用途 |
|------|------|------|
| `type:bug` | 红色 | Bug 报告 |
| `type:enhancement` | 蓝色 | 功能请求 |
| `type:question` | 紫色 | 使用问题 |
| `type:documentation` | 浅蓝 | 文档改进 |
| `type:refactor` | 浅黄 | 代码重构 |
| `type:performance` | 黄色 | 性能问题 |
| `type:security` | 深红 | 安全漏洞 |
| `priority:P0` ~ `P3` | 橙→灰 | 优先级 |
| `status:needs-triage` | 深黄 | 待分流 |
| `status:needs-info` | 黄色 | 需要更多信息 |
| `status:confirmed` | 绿色 | Bug 已确认 |
| `status:in-progress` | 蓝色 | 正在处理 |
| `status:blocked` | 橙色 | 被阻塞 |
| `status:stale` | 灰色 | 过期（Stale Bot 标记） |
| `good first issue` | 绿色 | 适合新手 |
| `help wanted` | 绿色 | 欢迎贡献 |
| `resolution:duplicate` | 灰色 | 重复 Issue |
| `resolution:wontfix` | 灰色 | 不修复 |
| `resolution:no-response` | 灰色 | 无回复关闭 |
| `resolution:invalid` | 灰色 | 无效 Issue |

通过 API 批量创建标签：`POST /repos/{owner}/{repo}/labels`。

> 完整的标签体系说明（含颜色色值）和批量创建脚本见 `references/triage-workflow.md`。

---

## 异常处理

| 情况 | 处理 |
|------|------|
| 仓库不存在或无权限 | 提示用户确认仓库名和 Token 权限 |
| 没有未关闭的 Issue | 输出"一切正常"，不生成多余报告 |
| Issue 数量超过 100 | 分批处理，优先处理最近的 |
| API 速率限制 | 等待或提示用户稍后重试（已认证 5000 次/小时，未认证 60 次/小时） |
| MCP 工具不可用 | 回退到 GitHub CLI（`gh`）或 curl + REST API |
| Docker 未运行 | MCP Server 无法启动，提示用户启动 Docker 或使用 `gh` CLI / curl 回退方案 |
| Windows PowerShell 环境 | curl 示例中 `$GITHUB_TOKEN` 需改为 `$env:GITHUB_TOKEN`，行续接符 `\` 改为 `` ` `` |
| Fine-grained PAT 权限不足 | 提示用户检查 PAT 的仓库范围和权限级别（Issues/PR 需 Read and write） |
| 用户取消操作 | 不执行任何已准备好的操作 |
