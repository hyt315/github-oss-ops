---
name: github-oss-ops
version: 2.1.0
description: Use when maintaining an open-source GitHub repository after launch, including Issue triage, AI hallucination defense, reply drafting, PR review assistance, CI diagnosis, private security vulnerability handling (GHSA/PVR), release preparation, multi-channel release broadcasting, community moderation, contributor recognition (All Contributors), sponsorship ops, stale-item review, and approval-gated GitHub writes. Triggers include Issue 管理、分流、triage、PR 审查、回复 Issue、版本号、发版、Release、changelog、漏洞响应、社区治理、致谢贡献者、赞助运营、过期 Issue、stale、运营报告、开源项目运营、oss ops, and project operations.
---

# GitHub 开源项目运营

开源发布后的项目“AI 维护中枢”：智能分流 Issue、防范 AI 垃圾、辅助 PR 审查、GHSA 私有漏洞协同、自动化版本发布、全渠道广播宣发与社区健康治理。

## 核心理念与铁律

- **Zero-Mutation 铁律**：默认所有操作均为只读分析、状态诊断与草稿生成。评论、打标签、关闭、合并、推送、修改设置和正式发版等所有破坏性或变更性写操作，必须明确展示目标与 Diff 内容，并在执行前获得用户明确确认，严正标明须用户明确授权后方可执行，并提供可逆回滚对策与治理建议；
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

十本深度参考手册承载本技能的核心运营资产。以下时机必须读取对应文件：

- Step 1 确认仓库与权限时，👉 动作：先读 [references/github-access-guide.md](references/github-access-guide.md)：授权路径优先级与最小权限示例；
- Step 2 排查深水区故障与隐患时，👉 动作：先读 [references/github-oss-ops-pitfalls.md](references/github-oss-ops-pitfalls.md)：GITHUB_TOKEN 提权风险、`pull_request_target` Pwn-Request 防御、Rulesets Tag 保护、Stale Bot 反噬与 API 次级限流对策；
- Step 3 分流 Issue 时，👉 动作：先读 [references/triage-workflow.md](references/triage-workflow.md)：分类决策树、AI 幻觉识别、转 Discussion 与优先级矩阵；
- Step 4 起草回复时，👉 动作：先读 [references/response-templates.md](references/response-templates.md)：各场景中英文礼貌回复模板、首次贡献致谢与拒审说明；
- Step 5 审查 PR 时，👉 动作：先读 [references/pr-review-guide.md](references/pr-review-guide.md)：审查清单、刷 KPI 式低质 PR 防御、Rulesets 与合并策略；
- Step 6 处置漏洞时，👉 动作：先读 [references/security-vulnerability-sop.md](references/security-vulnerability-sop.md)：官方 Private Vulnerability Reporting 私有协同、临时私有 Fork、申请 CVE 与 GHSA 公开披露；
- Step 7 发版广播时，👉 动作：先读 [references/release-workflow.md](references/release-workflow.md)：SemVer 规则、Release Notes 模板与 X/Reddit/微信全渠道广播文案；
- Step 8 治理与运营时，👉 动作：先读 [references/community-and-contributors.md](references/community-and-contributors.md)：社区冲突 4 级降温、All Contributors 致谢与 GitHub Sponsors 运营；
- Step 9 自动化配置时，👉 动作：先读 [references/automation-templates.md](references/automation-templates.md)：Stale Bot/Labeler 模板与自动化规则；
- Step 9 洞察周报输出时，👉 动作：先读 [references/reporting.md](references/reporting.md)：MTTR / MTTM 运营健康指标体系。

---

## 运营工作流

```
Step 1: 确认目标仓库与权限 ─────> 👉 动作：先读 references/github-access-guide.md
    ↓
Step 2: 扫描项目状态概览 ───────> 👉 动作：先读 references/github-oss-ops-pitfalls.md 聚合 open Issue/PR
    ↓
Step 3: Issue 智能分流与防伪 ───> 👉 动作：先读 references/triage-workflow.md (决策树 + AI 幻觉识别)
    ↓
Step 4: 结构化回复生成 ─────────> 👉 动作：先读 references/response-templates.md (生成草稿 → 用户批准 → 发送)
    ↓
Step 5: PR 辅助审查与防刷 ──────> 👉 动作：先读 references/pr-review-guide.md (Diff 范围 + Breaking Change + 质量核查)
    ↓
Step 6: 私有安全漏洞协同 ───────> 👉 动作：先读 references/security-vulnerability-sop.md (PVR + 临时私有 Fork + 申请 CVE)
    ↓
Step 7: 版本管理与全渠道广播 ───> 👉 动作：先读 references/release-workflow.md (SemVer + Release Notes + 社交广播)
    ↓
Step 8: 社区治理与贡献者运营 ───> 👉 动作：先读 references/community-and-contributors.md (冲突降温 + All Contributors + 赞助)
    ↓
Step 9: 自动化与洞察周报 ───────> 👉 动作：先读 references/automation-templates.md 与 reporting.md (Stale 治理 + 运营周报)
```

---

## Step 1: 确认目标仓库与权限
检查当前目录 `git remote -v` 获取 `owner/repo`。👉 动作：先读 [references/github-access-guide.md](references/github-access-guide.md) 核实 5 级授权通道。

## Step 2: 扫描项目状态概览与避坑排查
获取 open Issue / PR 列表、近期 Stale 项及 CI 运行状态。👉 动作：先读 [references/github-oss-ops-pitfalls.md](references/github-oss-ops-pitfalls.md) 识别潜在供应链隐患与权限过度暴露风险，运行 `python scripts/validate_ops.py --quick` 输出事实卡快照。

## Step 3: Issue 智能分流与防伪
👉 动作：先读 [references/triage-workflow.md](references/triage-workflow.md)，识别 Bug / Feature / Question，排查 2026 AI 幻觉 Issue 并引导开放咨询转入 Discussions。

## Step 4: 结构化回复生成
👉 动作：先读 [references/response-templates.md](references/response-templates.md)，根据情景生成专业礼貌草稿。所有评论发送、打标签与关闭等写操作**须经用户显式授权**后执行。

## Step 5: PR 辅助审查与防刷
👉 动作：先读 [references/pr-review-guide.md](references/pr-review-guide.md)，核验 Diff 范围、CI 状态、Breaking Changes、Merge Queue 与 Rulesets 分支保护，拦截刷绿点低质 PR。

## Step 6: 私有安全漏洞协同
👉 动作：先读 [references/security-vulnerability-sop.md](references/security-vulnerability-sop.md)，引导使用 Private Vulnerability Reporting (PVR)，创建 Temporary Private Fork 协同修复并申请 CVE。

## Step 7: 版本管理与全渠道广播
👉 动作：先读 [references/release-workflow.md](references/release-workflow.md)，基于已合并 PR 建议 SemVer 版本号，生成 Release Notes 及 Twitter/Reddit/微信广播推文。发版推送须经用户显式授权。

## Step 8: 社区治理与贡献者运营
👉 动作：先读 [references/community-and-contributors.md](references/community-and-contributors.md)，执行社区冲突 4 级降温处置，按 All Contributors 规范致谢并运营 GitHub Sponsors。

## Step 9: 自动化与洞察周报
👉 动作：先读 [references/automation-templates.md](references/automation-templates.md) 与 [references/reporting.md](references/reporting.md)，按需配置 Stale Bot/Labeler，输出 MTTR / MTTM 运营洞察周报。

---

## 输出规范：Ops 事实卡片 (Fact Card)

在完成项目状态扫描、分流或发版审查时，必须以标准 Markdown 表格输出统一事实卡片：

| 层级 | 检查项 (Metric/Item) | 测量实值 (Value) | 正常基线 (Baseline) | 状态判定 (Status) |
|---|---|---|---|:---:|
| L1 基础层 | 仓库基线与分支保护 | `owner/repo` (`main`) | 规则集 Rulesets 就绪 | 🟢 正常 |
| L1 基础层 | GITHUB_TOKEN 权限 / PAT 类型 | `contents: read` | 最小权限原则 | 🟢 合规 |
| L2 核心层 | Issue 分流响应与健康度 | Open: 12 (待分流: 2, Stale: 1) | Triage 响应 < 48h | 🟡 需关注 |
| L2 核心层 | PR 审查与 AI 垃圾防御 | Open: 4 (无冲突: 4, CI: 通过) | 严格拦截 AI Slop / 刷绿点 PR | 🟢 健康 |
| L3 深水层 | 漏洞私有协同 (PVR / GHSA) | PVR 开启 / 待审 GHSA: 0 | 私有协同，零公开披露 | 🟢 安全 |
| L3 深水层 | 发版就绪与 Tag 不可变性 | 待发版标签 `v2.1.0` (SemVer) | Tag Rulesets 开启更新/删除保护 | 🟢 就绪 |

> **⚠️ 授权声明**：本技能默认遵循 **Zero-Mutation** 原则与纯只读排查纪律。任何外部写操作（打标签、关闭、合并、发版）或破坏性治理建议，须用户明确授权后方可手动执行或由助手代为执行，并提供明确的安全恢复与回退对策。

---

## 质量门禁与自测

- **本地规范全检**：运行 `python scripts/validate_ops.py --quick` 进行快速采样，或运行 `python scripts/validate_ops.py --json` 导出完整机读报告；
- **静态结构校验**：运行 `node scripts/validate-skill.mjs` 做结构与外部链接校验；
- **全套回归测试**：运行 `python scripts/selftest.py` 验证 AST 语法、工作流 Step 与负向用例；
- **单元测试**：运行 `python -m unittest discover tests` 执行全套单元测试套件；
- **全维度静态审计**：运行 `python <skill-doctor>/scripts/audit.py . --dynamic` 确保 39 项规则 100% 全绿通过。
