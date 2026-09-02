---
name: github-oss-ops
version: 2.0.0
description: Use when maintaining an open-source GitHub repository after launch, including Issue triage, AI hallucination defense, reply drafting, PR review assistance, CI diagnosis, private security vulnerability handling (GHSA/PVR), release preparation, multi-channel release broadcasting, community moderation, contributor recognition (All Contributors), sponsorship ops, stale-item review, and approval-gated GitHub writes. Triggers include Issue 管理、分流、triage、PR 审查、回复 Issue、版本号、发版、Release、changelog、漏洞响应、社区治理、致谢贡献者、赞助运营、过期 Issue、stale、运营报告、开源项目运营、oss ops, and project operations.
---

# GitHub 开源项目运营

开源发布后的项目“AI 维护中枢”：智能分流 Issue、防范 AI 垃圾、辅助 PR 审查、GHSA 私有漏洞协同、自动化版本发布、全渠道广播宣发与社区健康治理。

## 核心理念与铁律

- **读写分离铁律**：公开信息读取、分析和草稿生成直接执行；评论、打标签、关闭、合并、推送、修改设置和正式发版等所有外部写操作，必须明确目标与 Diff 内容，并在执行前获得用户明确确认；
- **渐进式披露原则（Progressive Disclosure）**：本入口仅作为总控调度器，具体各阶段详细决策树、回复模板、审查规范与广播文案，严格按需调阅对应的深度参考手册；
- **维护者视角**：帮助独立维护者或小型团队高效管理项目，大幅降低日常重复沟通与维护负担；
- **凭据零采集**：不要求用户在聊天中发送 Token，不扫描个人私有目录，不打印、记录或写入凭据；
- **能力发现优先**：根据当前平台实际提供的 GitHub 连接、MCP、CLI 或 API 动态选择能力路径；
- **纯 Python 标准库零依赖**：辅助验证脚本严格基于 Python 3.10+ 标准库开发，100% 零第三方依赖、纯只读。

---

## 运行模式与授权优先级

公开仓库的只读扫描不要求认证。只有读取私有数据或执行写操作时才需要 GitHub 授权。按以下优先级使用：

1. **平台官方 GitHub 连接器或 GitHub 官方远程 MCP（OAuth）**：由受信任界面完成授权；
2. **已认证的 GitHub CLI**：先运行 `gh auth status`，未登录时引导用户运行 `gh auth login --web`；
3. **GitHub 官方本地 MCP Server**：适合需要本地宿主或受控 toolsets 的环境；
4. **Fine-grained PAT**：仅在用户明确选择时使用，限定最小权限仓库与有效期，安全读取；
5. **公开 REST API / 网页**：作为只读或人工交接回退。

---

## Reference Files

八本深度参考手册承载本技能的核心运营资产。以下时机必须读取对应文件：

- Step 1 确认仓库与权限时，先读 [references/github-access-guide.md](references/github-access-guide.md)：授权路径优先级与最小权限示例；
- Step 3 分流 Issue 时，先读 [references/triage-workflow.md](references/triage-workflow.md)：分类决策树、AI 幻觉识别、转 Discussion 与优先级矩阵；
- Step 4 起草回复时，先读 [references/response-templates.md](references/response-templates.md)：各场景中英文礼貌回复模板、首次贡献致谢与拒审说明；
- Step 5 审查 PR 时，先读 [references/pr-review-guide.md](references/pr-review-guide.md)：审查清单、刷 KPI 式低质 PR 防御、Rulesets 与合并策略；
- Step 6 处置漏洞时，先读 [references/security-vulnerability-sop.md](references/security-vulnerability-sop.md)：官方 Private Vulnerability Reporting 私有协同、临时私有 Fork、申请 CVE 与 GHSA 公开披露；
- Step 7 发版广播时，先读 [references/release-workflow.md](references/release-workflow.md)：SemVer 规则、Release Notes 模板与 X/Reddit/微信全渠道广播文案；
- Step 8 治理与运营时，先读 [references/community-and-contributors.md](references/community-and-contributors.md)：社区冲突 4 级降温、All Contributors 致谢与 GitHub Sponsors 运营；
- Step 9 自动化与周报时，先读 [references/automation-templates.md](references/automation-templates.md) 与 [references/reporting.md](references/reporting.md)：Stale Bot/Labeler 模板与 MTTR 运营健康指标。

---

## 运营工作流

```
Step 1: 确认目标仓库与权限 ─────> 读 references/github-access-guide.md
    ↓
Step 2: 扫描项目状态概览 ───────> 聚合 open Issue/PR 数量与近期动态
    ↓
Step 3: Issue 智能分流与防伪 ───> 读 references/triage-workflow.md (决策树 + AI 幻觉识别)
    ↓
Step 4: 结构化回复生成 ─────────> 读 references/response-templates.md (生成草稿 → 用户批准 → 发送)
    ↓
Step 5: PR 辅助审查与防刷 ──────> 读 references/pr-review-guide.md (Diff 范围 + Breaking Change + 质量核查)
    ↓
Step 6: 私有安全漏洞协同 ───────> 读 references/security-vulnerability-sop.md (PVR + 临时私有 Fork + 申请 CVE)
    ↓
Step 7: 版本管理与全渠道广播 ───> 读 references/release-workflow.md (SemVer + Release Notes + 社交广播)
    ↓
Step 8: 社区治理与贡献者运营 ───> 读 references/community-and-contributors.md (冲突降温 + All Contributors + 赞助)
    ↓
Step 9: 自动化与洞察周报 ───────> 读 references/automation-templates.md 与 reporting.md (Stale 治理 + 运营周报)
```

---

## Step 1: 确认目标仓库与权限
检查当前目录 `git remote -v` 获取 `owner/repo`。先读 [references/github-access-guide.md](references/github-access-guide.md) 核实 5 级授权通道。

## Step 2: 扫描项目状态概览
获取 open Issue / PR 列表、近期 Stale 项及 CI 运行状态，输出项目健康快照。

## Step 3: Issue 智能分流与防伪
先读 [references/triage-workflow.md](references/triage-workflow.md)，识别 Bug / Feature / Question，排查 2026 AI 幻觉 Issue 并引导开放咨询转入 Discussions。

## Step 4: 结构化回复生成
先读 [references/response-templates.md](references/response-templates.md)，根据情景生成专业礼貌草稿。所有评论发送须经用户批准。

## Step 5: PR 辅助审查与防刷
先读 [references/pr-review-guide.md](references/pr-review-guide.md)，核验 Diff 范围、CI 状态、Breaking Changes、Merge Queue 与 Rulesets 分支保护，拦截刷绿点低质 PR。

## Step 6: 私有安全漏洞协同
先读 [references/security-vulnerability-sop.md](references/security-vulnerability-sop.md)，引导使用 Private Vulnerability Reporting (PVR)，创建 Temporary Private Fork 协同修复并申请 CVE。

## Step 7: 版本管理与全渠道广播
先读 [references/release-workflow.md](references/release-workflow.md)，基于已合并 PR 建议 SemVer 版本号，生成 Release Notes 及 Twitter/Reddit/微信广播推文。

## Step 8: 社区治理与贡献者运营
先读 [references/community-and-contributors.md](references/community-and-contributors.md)，执行社区冲突 4 级降温处置，按 All Contributors 规范致谢并运营 GitHub Sponsors。

## Step 9: 自动化与洞察周报
先读 [references/automation-templates.md](references/automation-templates.md) 与 [references/reporting.md](references/reporting.md)，按需配置 Stale Bot/Labeler，输出 MTTR / MTTM 运营洞察周报。

---

## 质量门禁与自测

- **改动本技能后**：运行 `node scripts/validate-skill.mjs` 做结构校验，运行 `python scripts/selftest.py` 做回归测试；
- **全维度静态审计**：运行 `python <skill-doctor>/scripts/audit.py . --dynamic` 确保 39 项规则 100% 全绿通过。
