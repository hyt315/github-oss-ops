# Issue 分流工作流

> 适用任务：Issue 分流。包含分类决策树、标签体系、优先级矩阵与 AI 幻觉 Issue 识别。

---

## 目录

- [分流决策树](#分流决策树)
- [标准标签体系](#标准标签体系)
- [优先级矩阵](#优先级矩阵)
- [重复检测策略](#重复检测策略)
- [边界情况处理](#边界情况处理)
- [安全漏洞处理](#安全漏洞处理)
- [垃圾 Issue 和滥用处理](#垃圾-issue-和滥用处理)
- [AI 幻觉与垃圾 Issue 识别](#ai-幻觉与垃圾-issue-识别)
- [从 Issue 转 Discussion](#从-issue-转-discussion)
- [Issue 模板优化](#issue-模板优化)
- [批量分流操作](#批量分流操作)
- [分流结果展示模板](#分流结果展示模板)
- [仓库状态摘要模板](#仓库状态摘要模板)

---

## 分流决策树

```
新 Issue 进来
├── 标题/内容包含关键词 → 判断类型
│   ├── bug/crash/error/错误/崩溃/不工作/无法/失败 → type:bug
│   ├── feature/request/suggest/建议/希望/能不能/新增 → type:enhancement
│   ├── how/怎么/如何/请问/求助/question → type:question
│   ├── docs/readme/文档/说明/typo → type:documentation
│   └── security/vulnerability/CVE → 标记为安全相关，不公开讨论
│
├── 信息不足以判断 → status:needs-info
│   └── 回复请求补充信息（OS、版本、复现步骤、日志）
│
└── 搜索已有 Issue 检查重复
    ├── 找到高度相似 → resolution:duplicate，引用原始 Issue
    └── 无重复 → 正常分流
```

### 关键词匹配表

| 分类 | 中文关键词 | 英文关键词 |
|------|-----------|-----------|
| Bug | 报错、错误、崩溃、闪退、不工作、无法、失败、异常、卡死、白屏 | bug, crash, error, broken, not working, fail, exception, frozen |
| 功能请求 | 建议、希望、能不能、新增、支持、功能、想法 | feature, request, suggestion, enhancement, support, idea, proposal |
| 使用问题 | 怎么、如何、请问、求助、不懂、不会、为什么 | how to, question, help, why, can't figure out, stuck |
| 文档 | 文档、README、说明、typo、错别字、描述不清 | docs, documentation, readme, typo, unclear, wording |

---

## 标准标签体系

### 类型标签（type:*）

| 标签 | 颜色 | 说明 |
|------|------|------|
| `type:bug` | `#d73a4a`（红） | 确认的代码缺陷 |
| `type:enhancement` | `#a2eeef`（蓝） | 新功能或改进 |
| `type:question` | `#d876e3`（紫） | 使用问题，非 Bug |
| `type:documentation` | `#0075ca`（深蓝） | 文档相关 |
| `type:refactor` | `#e4e669`（黄） | 代码重构 |
| `type:performance` | `#fbca04`（金） | 性能相关 |
| `type:security` | `#b60205`（深红） | 安全问题 |

### 优先级标签（priority:*）

| 标签 | 颜色 | 说明 |
|------|------|------|
| `priority:P0` | `#b60205`（深红） | 紧急：核心功能不可用、安全漏洞 |
| `priority:P1` | `#d93f0b`（橙红） | 重要：影响较多用户，有明确修复方案 |
| `priority:P2` | `#0e8a16`（绿） | 一般：小问题、体验优化 |
| `priority:P3` | `#c5def5`（浅蓝） | 低：锦上添花、小众需求 |

### 状态标签（status:*）

| 标签 | 颜色 | 说明 |
|------|------|------|
| `status:needs-triage` | `#fbca04`（黄） | 待分流（新 Issue 默认） |
| `status:needs-info` | `#e4e669`（浅黄） | 需要提交者补充信息 |
| `status:confirmed` | `#0e8a16`（绿） | Bug 已确认，可复现 |
| `status:in-progress` | `#0052cc`（蓝） | 正在处理中 |
| `status:blocked` | `#d93f0b`（橙） | 被其他问题阻塞 |
| `status:stale` | `#cfd3d7`（灰） | 长期无活动，由 Stale Bot 自动标记 |

### 决议标签（resolution:*）

| 标签 | 颜色 | 说明 |
|------|------|------|
| `resolution:duplicate` | `#cfd3d7`（灰） | 重复 Issue |
| `resolution:wontfix` | `#cfd3d7`（灰） | 不修复（不在项目范围） |
| `resolution:no-response` | `#cfd3d7`（灰） | 提交者无回复，自动关闭 |
| `resolution:invalid` | `#cfd3d7`（灰） | 无效 Issue |

### 社区标签

| 标签 | 颜色 | 说明 |
|------|------|------|
| `good first issue` | `#7057ff`（靛蓝） | 适合首次贡献者 |
| `help wanted` | `#008672`（青绿） | 欢迎社区贡献 |

### 创建标签的 API

```bash
# 批量创建或更新标签。可重复执行：--force 会更新已存在的同名标签，
# 新仓库自带的 good first issue / help wanted 不会因“已存在”而报错
R=owner/repo
while IFS='|' read -r name color desc; do
  gh label create "$name" -R "$R" --color "$color" --description "$desc" --force
done <<'LABELS'
type:bug|d73a4a|Confirmed bug
type:enhancement|a2eeef|Feature request
type:question|d876e3|Usage question
type:documentation|0075ca|Documentation improvement
type:refactor|e4e669|Code refactoring
type:performance|fbca04|Performance related
type:security|b60205|Security issue
priority:P0|b60205|Critical issue
priority:P1|d93f0b|Important issue
priority:P2|0e8a16|Normal priority
priority:P3|c5def5|Low priority
status:needs-triage|fbca04|Needs triage
status:needs-info|e4e669|Needs more info
status:confirmed|0e8a16|Bug confirmed, reproducible
status:in-progress|0052cc|Work in progress
status:blocked|d93f0b|Blocked by another issue
status:stale|cfd3d7|Stale, no recent activity
resolution:duplicate|cfd3d7|Duplicate issue
resolution:wontfix|cfd3d7|Will not fix
resolution:no-response|cfd3d7|Closed due to no response
resolution:invalid|cfd3d7|Invalid issue
good first issue|7057ff|Good for newcomers
help wanted|008672|Contributions welcome
LABELS
```

> 没有 `gh` 时用 `POST /repos/{owner}/{repo}/labels`；同名标签已存在会返回 422，要改用 `PATCH /repos/{owner}/{repo}/labels/{name}` 更新。

---

## 优先级矩阵

基于**影响范围**和**严重程度**两个维度：

| | 影响少数用户 | 影响多数用户 | 影响所有用户 |
|---|---|---|---|
| **致命**（数据丢失/安全） | P1 | P0 | P0 |
| **严重**（核心功能不可用） | P1 | P1 | P0 |
| **一般**（功能异常但有 workaround） | P2 | P1 | P1 |
| **轻微**（体验问题/UI 瑕疵） | P3 | P2 | P2 |

---

## 重复检测策略

### 搜索方法

1. **标题关键词提取**：从 Issue 标题中提取 2-3 个核心关键词
2. **在已有 Issue 中搜索**：`search_issues` 工具，用关键词搜索
3. **相似度判断**：
   - 标题关键词重合 ≥ 2 个 + 描述场景相似 → 高度疑似重复
   - 仅标题部分重合 → 可能相关，在评论中引用但不关闭

### 处理重复

```
这是一个重复的 Issue。原始 Issue 为 #{original_number}，
那里已有相关讨论和进展。建议在该 Issue 中继续跟进。

如有不同情况，请补充说明，我会重新评估。
```

---

## 边界情况处理

| 情况 | 处理方式 |
|------|----------|
| Issue 同时是 Bug 和功能请求 | 拆分为两个 Issue，或标记为主类型 + 补充说明 |
| Issue 描述模糊，无法判断 | 标记 `status:needs-info`，请求具体信息 |
| Issue 是安全漏洞报告 | 不公开讨论，引导使用 Private Vulnerability Reporting（见下方安全漏洞处理） |
| Issue 包含不当内容 | 按 CODE_OF_CONDUCT 处理，提醒维护者 |
| Issue 属于另一个项目 | 告知提交者正确的仓库地址，关闭 |
| Issue 是求助但不是 Bug | 引导到 GitHub Discussions（如果开启了） |
| 首次贡献者的低质量 Issue | 温和引导，提供模板链接，不直接关闭 |
| Issue 是垃圾内容/广告 | 直接关闭并标记 `resolution:invalid`，必要时举报用户 |
| Issue 包含敏感信息（token/密码） | 提醒提交者立即吊销并轮换凭据；编辑删除敏感内容，并删除含敏感内容的编辑历史修订 |
| Issue 是重复提交（同一用户多次） | 引用原始 Issue，关闭重复项，标记 `resolution:duplicate` |
| Issue 已在旧版本修复但用户未升级 | 说明已修复的版本号，引导升级 |

---

## 安全漏洞处理

安全报告不能在公开 Issue 里讨论细节。分流时按 [security-vulnerability-sop.md §一](security-vulnerability-sop.md#一漏洞被发到公开-issue-时) 的顺序处理（每步写操作先经用户批准）：

1. **先去掉细节**：Issue 里已有利用细节或凭据时，编辑删除并删掉含细节的编辑历史修订，必要时由管理员删除 Issue；
2. 起草一条**不复述细节**的公开回复，请报告者改用 Private vulnerability reporting（GitHub 没有私信；公开仓库的 Issue 也不能改为私密）；
3. 优先级在私有安全公告里跟踪。修复发布前不要给这条公开 Issue 打 `type:security`／`priority:P0`，标签会把未修复的漏洞指给所有人看；`type:security` 留给不含利用细节的安全加固类 Issue。

之后的评估、修复、CVE 与公告流程见 [security-vulnerability-sop.md](security-vulnerability-sop.md)，回复模板见 [response-templates.md](response-templates.md) 的“安全漏洞回复”。

---

## 垃圾 Issue 和滥用处理

### 识别垃圾 Issue

| 信号 | 说明 |
|------|------|
| 内容与项目完全无关 | 广告、推广、无关链接 |
| 重复提交相同内容 | 同一用户多次提交完全相同的 Issue |
| 包含钓鱼链接 | 可疑 URL、仿冒网站 |
| 纯垃圾文本 | 无意义的字符组合 |
| 职业广告 | 代写、代做、刷量等服务推广 |

### 处理策略

| 情况 | 操作 |
|------|------|
| 明显垃圾内容 | 直接关闭，标记 `resolution:invalid`，不回复 |
| 可疑但不确定 | 标记 `status:needs-triage`，询问提交者意图 |
| 钓鱼链接 | 关闭 Issue，删除含链接的评论，通过 GitHub 举报 |
| 反复提交垃圾 | 在 GitHub 用户主页点击 **Report abuse** 举报用户 |
| 包含恶意代码 | 关闭 Issue，不执行任何代码，提醒维护者 |

> **注意**：不要点击垃圾 Issue 中的任何链接。处理垃圾 Issue 时不需要回复，直接关闭即可，避免给垃圾信息制造者任何互动信号。

---

## AI 幻觉与垃圾 Issue 识别

随着 AI 编码助手普及，社区中出现了由 LLM 自动生成的大量低质或幻觉 Issue。维护者应按以下标准识别并快速处置：

### 1. AI 幻觉 Issue 典型特征
- **虚构的 API 或参数**：提报的问题基于项目中根本不存在的函数名、配置项或 CLI 标志；
- **无法对齐的报错堆栈**：堆栈信息包含不存在的源码文件名或明显由大模型凭空构造的 Traceback；
- **空泛无实义的建议**：“建议重构项目以提升架构弹性和高可用”，却无法给出具体的业务场景或痛点。

### 2. 处置策略
- **核实代码库**：用搜索工具快速检索提报的 API/文件是否存在；
- **判定为 AI 幻觉/垃圾后**：使用礼貌模板快速关闭并打上 `resolution:invalid` 标签，避免展开长篇辩论；
- **高频滥用防御**：若特定账号持续批量提交，可开启 Interaction limits 临时限制新账号或非贡献者互动，必要时屏蔽该账号（见 [community-and-contributors.md](community-and-contributors.md)）。

---

## 从 Issue 转 Discussion

保持 Issue 队列为纯粹的“待开发/待修复工单”，将开放式探讨转移到 Discussions：

| 提报内容 | 推荐转入的 Discussion 分类 | 处置动作 |
|---|---|---|
| **“如何实现某个效果？”/ 使用求助** | `Q&A` | 点击右侧 `Convert to discussion` → 选择 `Q&A` 分类 |
| **“未来是否可以支持某种架构？”/ 头脑风暴** | `Ideas` | 转入 `Ideas` 分类，交由社区投票点赞 |
| **“我用这个项目做了一个很酷的作品”/ 案例展示** | `Show and tell` | 转入 `Show and tell`，鼓励社区交流 |
| **项目重大里程碑 / 路线图公告** | `Announcements` | 维护者专属发布渠道 |


以下情况建议将 Issue 转为 Discussion：

| 场景 | 原因 |
|------|------|
| 开放性讨论（无明确行动项） | Issue 应聚焦于可执行的任务 |
| 使用教程/经验分享 | 适合 Discussion 的 Show and Tell |
| 投票/调查类 | 适合 Discussion 的 Polls |
| 问答（已被解答） | 标记为已解答的 Q&A 更有价值 |

转 Discussion 只能在网页上操作：Issue 右侧栏 `Convert to discussion`（需 Triage 及以上权限）。REST 和 GraphQL 都没有转换接口，按标签批量转换的功能已于 2025-05 下线；GraphQL 的 `createDiscussion` 只能新建副本，不会保留原 Issue 的评论。

---

## Issue 模板优化

良好的 Issue 模板能大幅降低分流成本，让提交者在创建时就提供足够信息。

### 模板设计原则

| 原则 | 说明 |
|------|------|
| 分类型提供模板 | Bug 报告、功能请求、使用问题分别使用不同模板 |
| 必填项明确 | 用 `**必填**` 或 placeholder 提示关键信息 |
| 提供示例 | 在模板中给出填写示例，降低理解成本 |
| 避免过长 | 模板过长会导致提交者跳过填写 |
| 包含环境信息 | Bug 模板应包含 OS、版本、复现步骤等字段 |

### 推荐的 Bug 报告模板结构

```markdown
---
name: Bug 报告
about: 报告一个 Bug
title: "[Bug] "
labels: ["type:bug", "status:needs-triage"]
---

## 问题描述
<!-- 简要描述遇到的问题 -->

## 复现步骤
1. 
2. 
3. 

## 期望行为
<!-- 你期望发生什么 -->

## 实际行为
<!-- 实际发生了什么 -->

## 环境信息
- 操作系统：
- 项目版本：
- 运行环境（Node/Python/浏览器等）：

## 附加信息
<!-- 截图、日志、错误堆栈等 -->
```

### 模板文件位置

```
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.md          # Bug 报告模板
    ├── feature_request.md     # 功能请求模板
    ├── question.md            # 使用问题模板
    └── config.yml             # 模板配置（可选择禁用空白 Issue）
```

### config.yml 示例

```yaml
# .github/ISSUE_TEMPLATE/config.yml
blank_issues_enabled: false    # 禁止不使用模板的空白 Issue
contact_links:
  - name: 使用问题
    url: https://github.com/owner/repo/discussions
    about: 使用问题请在 Discussions 中提问
```

> **提示**：`github-oss-prep` 技能已处理基础模板创建。本节提供的是优化建议，可根据项目实际情况调整。

---

## 批量分流操作

当积压的 Issue 较多时，可以批量处理：

1. 按类型分组：先处理所有明显的 Bug，再处理功能请求，最后处理问题
2. 每批 10-15 个，展示给用户确认
3. 确认后再执行标签和回复操作
4. 避免一次性操作过多导致 API 速率限制

---

## 分流结果展示模板

```text
### Issue #{number}: {title}
- 提交者：@{user}（首次贡献 / 活跃贡献者）
- 分类：Bug / 功能请求 / 使用问题 / 文档 / 需要更多信息
- 建议优先级：P1
- 建议标签：type:bug, priority:P1
- 疑似重复：无 / 可能是 #{other_number} 的重复
- 建议操作：标记标签 + 回复 / 关闭 / 转 Discussion
```

---

## 仓库状态摘要模板

```text
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
