# Issue 分流工作流

> 详细的 Issue 分类决策树、标签体系设计和优先级矩阵。SKILL.md Step 3 引用本文件。

---

## 目录

- [分流决策树](#分流决策树)
- [标准标签体系](#标准标签体系)
- [优先级矩阵](#优先级矩阵)
- [重复检测策略](#重复检测策略)
- [边界情况处理](#边界情况处理)
- [安全漏洞处理](#安全漏洞处理)
- [垃圾 Issue 和滥用处理](#垃圾-issue-和滥用处理)
- [从 Issue 转 Discussion 的场景](#从-issue-转-discussion-的场景)
- [Issue 模板优化](#issue-模板优化)
- [批量分流操作](#批量分流操作)

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
# 批量创建标签
for label in '{"name":"type:bug","color":"d73a4a","description":"Confirmed bug"}' \
             '{"name":"type:enhancement","color":"a2eeef","description":"Feature request"}' \
             '{"name":"type:question","color":"d876e3","description":"Usage question"}' \
             '{"name":"type:documentation","color":"0075ca","description":"Documentation improvement"}' \
             '{"name":"type:refactor","color":"e4e669","description":"Code refactoring"}' \
             '{"name":"type:performance","color":"fbca04","description":"Performance related"}' \
             '{"name":"type:security","color":"b60205","description":"Security issue"}' \
             '{"name":"priority:P0","color":"b60205","description":"Critical issue"}' \
             '{"name":"priority:P1","color":"d93f0b","description":"Important issue"}' \
             '{"name":"priority:P2","color":"0e8a16","description":"Normal priority"}' \
             '{"name":"priority:P3","color":"c5def5","description":"Low priority"}' \
             '{"name":"status:needs-triage","color":"fbca04","description":"Needs triage"}' \
             '{"name":"status:needs-info","color":"e4e669","description":"Needs more info"}' \
             '{"name":"status:confirmed","color":"0e8a16","description":"Bug confirmed, reproducible"}' \
             '{"name":"status:in-progress","color":"0052cc","description":"Work in progress"}' \
             '{"name":"status:blocked","color":"d93f0b","description":"Blocked by another issue"}' \
             '{"name":"status:stale","color":"cfd3d7","description":"Stale, no recent activity"}' \
             '{"name":"resolution:duplicate","color":"cfd3d7","description":"Duplicate issue"}' \
             '{"name":"resolution:wontfix","color":"cfd3d7","description":"Will not fix"}' \
             '{"name":"resolution:no-response","color":"cfd3d7","description":"Closed due to no response"}' \
             '{"name":"resolution:invalid","color":"cfd3d7","description":"Invalid issue"}' \
             '{"name":"good first issue","color":"7057ff","description":"Good for newcomers"}' \
             '{"name":"help wanted","color":"008672","description":"Contributions welcome"}'; do
  curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/<owner>/<repo>/labels" \
    -d "$label"
done
```

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
| Issue 包含敏感信息（token/密码） | 提醒提交者立即删除并轮换凭据，删除评论中的敏感内容 |
| Issue 是重复提交（同一用户多次） | 引用原始 Issue，关闭重复项，标记 `resolution:duplicate` |
| Issue 已在旧版本修复但用户未升级 | 说明已修复的版本号，引导升级 |

---

## 安全漏洞处理

安全漏洞需要特殊处理流程，不能在公开 Issue 中讨论细节。

### 处理流程

```
收到安全相关 Issue
    ↓
立即标记 type:security + priority:P0
    ↓
删除 Issue 中可能包含的漏洞利用细节（如有）
    ↓
私信提交者，引导使用 Private Vulnerability Reporting
    ↓
关闭公开 Issue（或转为私密）
    ↓
在 Security Advisory 中记录和跟踪
    ↓
修复后发布安全公告 + CVE（如适用）
```

### Private Vulnerability Reporting

GitHub 提供私密的漏洞报告通道，维护者应在仓库设置中启用：

1. 进入仓库 Settings → Security → Code security
2. 开启 **Private vulnerability reporting**
3. 此后用户可通过仓库页面的 **Security** 标签页私密报告漏洞

### 安全 Issue 回复要点

- 不要在公开评论中确认或否认漏洞的存在
- 引导提交者使用私密渠道
- 感谢报告者的负责任披露
- 说明预计的响应时间

> 详细的回复模板见 `references/response-templates.md` 中的"安全漏洞回复"部分。

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

## 从 Issue 转 Discussion 的场景

以下情况建议将 Issue 转为 Discussion：

| 场景 | 原因 |
|------|------|
| 开放性讨论（无明确行动项） | Issue 应聚焦于可执行的任务 |
| 使用教程/经验分享 | 适合 Discussion 的 Show and Tell |
| 投票/调查类 | 适合 Discussion 的 Polls |
| 问答（已被解答） | 标记为已解答的 Q&A 更有价值 |

转 Discussion 的操作：GitHub UI 上可以直接 Convert to Discussion，或通过 API（目前 REST API 不直接支持，需要 GraphQL）。

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

> **提示**：`oss-prep` 技能已处理基础模板创建。本节提供的是优化建议，可根据项目实际情况调整。

---

## 批量分流操作

当积压的 Issue 较多时，可以批量处理：

1. 按类型分组：先处理所有明显的 Bug，再处理功能请求，最后处理问题
2. 每批 10-15 个，展示给用户确认
3. 确认后再执行标签和回复操作
4. 避免一次性操作过多导致 API 速率限制
