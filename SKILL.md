---
name: github-oss-ops
version: 2.2.0
description: Use when maintaining an open-source GitHub repository after launch - Issue triage, spotting AI-generated or spam Issues/PRs, drafting replies, PR review, CI diagnosis, private vulnerability reports (PVR, security advisories, CVE), version bumps and release notes, release announcements, community moderation, contributor recognition, sponsorship, stale-item cleanup, repository automation and health reports. All GitHub writes are approval-gated. Triggers include Issue 分流、triage、回复 Issue、PR 审查、发版、Release、changelog、漏洞响应、社区治理、致谢贡献者、stale、运营周报、开源项目运营、oss ops.
---

# GitHub 开源项目运营

开源项目上线后的日常维护：分流 Issue、审查 PR、处理漏洞报告、准备发版、治理社区、出运营报告。默认只读和起草，写入 GitHub 前必须经用户批准。

## 铁律

1. **默认只读**：读取、分析、起草草稿不需要批准。评论、打标签、关闭、合并、推送、改设置、打 Tag、发 Release、对外发帖都是写操作，执行前逐项展示“目标 + 具体内容 + 能否撤销”，得到用户明确确认后才做。一次确认只覆盖展示过的那一项。
2. **不碰凭据**：不让用户在聊天里贴 Token，不翻用户目录或配置文件找凭据，不打印、记录或写入凭据。
3. **按需读手册**：先用下面的路由表找到任务，只读对应的那一两份手册。
4. **事实与推断分开**：数据来自命令或 API 就写明来源；查不到就写“未查”或“无法确认”，不估数。
5. **GitHub 界面会改名**：手册里的菜单路径以 2026-11-08 核对为准，和实际页面不一致时以页面为准，并告诉用户。

## 任务路由

| 用户想做的事 | 先读 | 产出 | 需批准的写操作 |
|---|---|---|---|
| 确认仓库、配置访问权限 | [github-access-guide.md](references/github-access-guide.md) | 可用的访问方式 | 无 |
| 看仓库整体健康、排查 CI／权限风险 | [github-oss-ops-pitfalls.md](references/github-oss-ops-pitfalls.md) | 事实卡 + 风险清单 | 改设置、改工作流 |
| 分流新 Issue、识别重复和垃圾 | [triage-workflow.md](references/triage-workflow.md) | 每条的类型／优先级／标签建议 | 打标签、关闭、转 Discussion |
| 回复 Issue 或 PR | [response-templates.md](references/response-templates.md) | 中英文回复草稿 | 发送评论 |
| 审查 PR | [pr-review-guide.md](references/pr-review-guide.md) | 审查摘要 + Review 草稿 | 提交 Review、合并 |
| 有人报告安全漏洞 | [security-vulnerability-sop.md](references/security-vulnerability-sop.md) | 处置步骤 + 私有渠道引导回复 | 编辑／删除内容、建公告、申请 CVE、发布公告 |
| 定版本号、写 Changelog、发版、宣传 | [release-workflow.md](references/release-workflow.md) | 版本建议、Release Notes、宣传文案草稿 | 改版本文件、打 Tag、发 Release、对外发帖（分别确认） |
| 处理争吵、致谢贡献者、赞助 | [community-and-contributors.md](references/community-and-contributors.md) | 处置建议与文案 | 隐藏、锁定、屏蔽、改权限 |
| 配置 Stale、自动打标等自动化 | [automation-templates.md](references/automation-templates.md) | 写进目标仓库的 YAML 草稿 | 提交工作流文件 |
| 出周报／月报 | [reporting.md](references/reporting.md) | 运营报告 | 无 |

一个请求涉及多项时（例如“扫一遍再起草回复”），按表从上到下依次做，每一项的写操作单独确认。

## 通用流程

1. **确认目标**：从用户输入或 `git remote -v` 得到 `owner/repo`；公开仓库的只读扫描不需要认证。需要私有数据或写操作时，按访问指南选通道：平台 GitHub 连接器或官方 MCP（OAuth）→ 已登录的 `gh` → 用户明确选择的 Fine-grained PAT → 公开 REST／网页只读。
2. **只读收集**：只拉当前任务需要的数据。仓库健康扫描用下面的快照命令。
3. **产出**：按对应手册给出分析和草稿。涉及仓库状态时附事实卡。
4. **待批准清单**：最后单列“待批准写操作”，每项写清目标和内容；用户确认哪项就只执行哪项，执行后回读结果确认。

### 仓库快照命令（只读）

```bash
R=owner/repo
gh repo view $R --json defaultBranchRef,visibility,hasDiscussionsEnabled,stargazerCount
gh issue list -R $R --state open --limit 200 --json number,title,labels,createdAt,updatedAt,comments
gh pr list -R $R --state open --limit 100 --json number,title,isDraft,mergeable,reviewDecision,createdAt
gh run list -R $R --limit 10 --json workflowName,conclusion,headBranch,createdAt
gh api repos/$R/rulesets                                  # 规则集（含标签保护）
gh api repos/$R/private-vulnerability-reporting           # {"enabled": true|false}
gh api repos/$R/actions/permissions/workflow              # 默认 GITHUB_TOKEN 权限
gh release list -R $R --limit 3
```

没有 `gh` 时用同名 REST 接口；某项因权限查不到就在事实卡里写“未查（需 X 权限）”。

## 事实卡格式

仓库扫描、分流和发版检查的结果都用这张表开头。下面只是**格式示例**，每个值必须来自上面的命令，不能沿用示例数字。

| 维度 | 检查项 | 实测值 | 基线 | 判定 |
|---|---|---|---|:---:|
| 基础 | 默认分支与规则集 | `main`，规则集 1 条 | 默认分支有规则集保护 | 🟢 |
| 基础 | 工作流默认 Token 权限 | `read` | 只读 | 🟢 |
| Issue | 未关闭／无标签／超 7 天未回复 | 12／2／1 | 首次响应 < 2 天 | 🟡 |
| PR | 未关闭／待审查／CI 失败 | 4／2／0 | CI 绿、无长期积压 | 🟢 |
| 安全 | 私有漏洞报告 | 已开启 | 开启 | 🟢 |
| 发版 | 最新 Release 与标签保护 | `v2.1.0`，标签规则集：无 | 标签受保护 | 🔴 |

判定：🟢 达标，🟡 需关注，🔴 有风险，⚪ 未查。

## 本技能包自检

```bash
python scripts/validate.py          # 结构、版本一致、链接、凭据扫描
python -m unittest discover tests   # 校验器的正向与负向测试
```

只依赖 Python 3.10+ 标准库，只读，不联网。
