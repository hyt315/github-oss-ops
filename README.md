# ⚙️ GitHub OSS Ops / 开源项目运营

<div align="center">

**给独立维护者与开源团队打造的 AI 运营中枢：智能分流 Issue、AI 垃圾防御、PR 辅助审查、GHSA 私有漏洞协同、自动化版本发布与全渠道广播宣发。**

**Industrial-grade GitHub repository operations skill for maintainers — intelligent issue triage, AI slop defense, PR review, GHSA vulnerability SOP, release management, and multi-channel broadcasting.**

[![Validate](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml/badge.svg)](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/hyt315/github-oss-ops?sort=semver)](https://github.com/hyt315/github-oss-ops/releases/latest)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/hyt315/github-oss-ops?style=social)](https://github.com/hyt315/github-oss-ops/stargazers)

[English](./README.en.md) | [中文](./README.md)

</div>

![GitHub OSS Ops workflow: scan, triage, draft, approve, act and report](assets/social-preview.png)

---

## 📖 这是什么？

项目开源发布只是开始，维护者的日常运营才是长跑：
- 每天面对大量新 Issue，需要识别是否为大模型虚构的“AI 幻觉 Bug”，并将开放式咨询转入 Discussions；
- 收到外部 PR 时，需要核验 Diff 范围、CI 状态、破坏性风险，防范纯改空格刷贡献的“低质 PR”；
- 收到安全报告时，需要遵循官方 Private Vulnerability Reporting (PVR) 与 GHSA 协同流程，严防在公开 Issue 泄露 0-day；
- 准备发版时，需要按 SemVer 规范从已合并改动中自动生成 Release 说明，并向 Twitter/Reddit/微信等全渠道同步广播推文；
- 面对社区冲突与负面言论，需要去情绪化的 4 级降温处置 SOP。

**`github-oss-ops`** 将这些繁重步骤组织成 **可复核、结构化、自动化的高效工作流**，同时 **严格保留人的最终决定权** —— 所有外部写操作（发布评论、打标签、合并 PR、打 Tag、创建 Release）均在用户明确批准后才执行。

---

## ✨ 核心特性

| 核心工作流 | 覆盖功能与操作 | 带来价值与默认边界 |
|---|---|---|
| 📋 **Issue 智能分流与防伪** | 聚合新 Issue、判断类型/优先级、**识别 AI 幻觉与垃圾 Issue**、引导转入 Discussions | 读取全自动；评论、标签、关闭操作必须获得人工授权 |
| 🔍 **PR 辅助审查与防刷** | 汇总 Diff 范围、CI 状态、**防范刷 KPI 式低质 PR**、核验 Rulesets 与 Merge Queue | 绝不伪装成人类审查，未经确认不向 PR 提交 Review |
| 🛡️ **GHSA 私有安全协同** | 官方 PVR 私有漏洞接收、创建 Temporary Private Fork 协同修复、申请正式 CVE ID | 严禁在公开 Issue 讨论漏洞，闭环安全通报 |
| 🚀 **SemVer 发版与社交广播** | 依据已合并 PR 建议 SemVer 版本号、生成分类变更日志、**全渠道社交广播推文 (X/Reddit/微信)** | Tag、Release 与资产推送分别独立确认 |
| 🤝 **社区治理与贡献者阶梯** | 社区冲突 4 级降温处置（隐藏评论/锁定讨论/封禁）、**All Contributors 贡献致谢** | 规范化社区氛围，保障维护者心理健康 |
| 💰 **Sponsors 赞助与商业支持** | `.github/FUNDING.yml` 平台配置、赞助层级设计 (Sponsor Tiers) 与商业支持引导 | 助力开源项目实现财务与生态可持续发展 |
| 📊 **运营洞察与自动化** | 统计首次响应、解决时长 (MTTR)、合并时长 (MTTM)、配置 Stale Bot 与自动打标 CI | 区分客观事实、推断与运营建议 |

---

## 📊 开源运营全流程架构

```
[用户请求：扫描仓库 / 分流 Issue / 审查 PR / 处理漏洞 / 发版 / 出周报]
                               │
   [SKILL.md 任务路由表] ──> 只读与任务对应的 1–2 份手册
                               │
   [只读收集] ──────────────> gh / REST / MCP 拉取当前任务所需数据
                               │
   [产出] ──────────────────> 事实卡 + 分析 + 草稿（回复、Review、Release Notes）
                               │
   [待批准写操作清单] ───────> 用户逐项确认后执行，执行后回读核对
```

---

## 🛡️ AI 垃圾防御与私有漏洞响应

### 1. AI 幻觉与刷贡献防御

```
[收到外部新提交]
       │
       ├──> [Issue 检测] ──> 是否包含虚构 API / 不存在配置 / 虚假报错堆栈？
       │         │
       │         ├── 是 ──> 标记 resolution:invalid，礼貌回复模板劝退并关闭
       │         └── 否 ──> 正常打标分流 (Bug/Feature/Docs)，开放探讨转入 Discussions
       │
       └──> [PR 审查] ────> 是否仅改空格/无义注释/机械重命名 (Contribution Farming)？
                 │
                 ├── 是 ──> 依据贡献指南礼貌拒绝，维护主干纯洁度
                 └── 否 ──> 辅助审查 Diff 范围、CI 状态、Breaking Changes 与测试覆盖
```

### 2. 私有漏洞协同流程

```
[白帽研究员提交漏洞] ──> 触发 GitHub Private Vulnerability Reporting (PVR)
                                      │
               [创建 Temporary Private Fork 私有分叉协同修复]
                                      │
               [在公告页 Request CVE，GitHub 作为 CNA 审核]
                                      │
               [与报告者约定公开日期（常见上限 90 天）]
                                      │
               [发布补丁与安全公告 ➔ GitHub 审核后可触发 Dependabot 告警]
```

---

## 📚 实战案例演示

三个端到端可复核实战案例，详见 [examples/README.md](examples/README.md)：
1. [新 Issue 分流与重复检测](examples/README.md#示例一新-issue-分流)
2. [PR 风险审查与 CI 诊断](examples/README.md#示例二pr-风险审查)
3. [周报与 Release 草稿](examples/README.md#示例三周报与-release-草稿)

---

## 🚀 快速开始

这是一个标准的 AI Agent Skill —— 安装到你的 AI 助手后即可直接使用。

### 方式 A：把一句话发给任意 Agent（最推荐、最通用）

把下面这段话直接复制发送给你的 AI 助手，它会自动完成安装：

> 请安装 github-oss-ops 技能：克隆 `https://github.com/hyt315/github-oss-ops` 到你的 skills 目录（如 `~/.claude/skills/github-oss-ops`、`~/.agents/skills/github-oss-ops` 或 `~/.cursor/skills/github-oss-ops`），并确认安装成功。以后我要「管理我的开源项目 / 分流 Issue / 审查 PR / 漏洞协同 / 发版广播 / 出周报」时，按 SKILL.md 的流程引导我完成，所有写操作都在我确认后执行。

### 方式 B：GitHub CLI 2.90+（一行命令）

```bash
gh skill install hyt315/github-oss-ops github-oss-ops --agent claude-code --scope user
```

### 方式 C：多平台手动安装

| 平台 | 用户级安装路径 | 项目级安装路径 |
|---|---|---|
| **Claude Code** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.claude/skills/github-oss-ops` | `.claude/skills/github-oss-ops` |
| **Codex** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.agents/skills/github-oss-ops` | `.agents/skills/github-oss-ops` |
| **Cursor** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.cursor/skills/github-oss-ops` | `.cursor/skills/github-oss-ops` |
| **通用 Agents** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.agents/skills/github-oss-ops` | `.agents/skills/github-oss-ops` |

### 方式 D：本地运行回归自测

```bash
# 技能包自检：结构、版本一致、链接、凭据扫描（只读，零依赖）
python scripts/validate.py
python scripts/validate.py --json

# 校验器的正向与负向测试
python -m unittest discover tests
```

---

## 🔒 权限与安全原则

- **严格只读默认**：扫描公开仓库无需任何 Token，仅分析公开数据并生成草稿；
- **读写分离与确认门禁**：所有评论发送、打标签、关闭 Issue、合并 PR、打 Tag、创建 Release，必须明确展示目标和内容，并在执行前获得用户明确确认；
- **凭据零采集**：绝不在聊天中索取 Token，绝不主动搜索用户本地私有配置文件；
- **最小权限策略**：仅申请当前操作所需的最小权限（如 Issue 只读仅需 `issues:read`）。

---

## 📥 下载与获取

| 方式 | 命令 / 链接 |
|---|---|
| **HTTPS** | `git clone https://github.com/hyt315/github-oss-ops.git` |
| **SSH** | `git clone git@github.com:hyt315/github-oss-ops.git` |
| **GitHub CLI** | `gh repo clone hyt315/github-oss-ops` |
| **ZIP 压缩包** | [下载 ZIP](https://github.com/hyt315/github-oss-ops/archive/refs/heads/main.zip) |
| **Tar 归档** | [下载 Tar](https://github.com/hyt315/github-oss-ops/archive/refs/heads/main.tar.gz) |
| **单文件 (SKILL.md)** | `curl -O https://raw.githubusercontent.com/hyt315/github-oss-ops/main/SKILL.md` |

---

## 📖 深度参考手册导读

| 参考文档 | 核心内容 | 推荐阅读时机 | 预估耗时 |
|---|---|---|---|
| ⚠️ [**深水区避坑指南 (`github-oss-ops-pitfalls.md`)**](references/github-oss-ops-pitfalls.md) | GITHUB_TOKEN 提权、Pwn-Request 防御、Rulesets Tag 保护与 API 次级限流 | 排查供应链风险与复杂运维故障时 | 5 分钟 |
| 📋 [**Issue 分流工作流 (`triage-workflow.md`)**](references/triage-workflow.md) | 分类决策树、AI 幻觉识别、转 Discussions 与优先级矩阵 | 分流新 Issue 与过滤垃圾提报时 | 4 分钟 |
| 💬 [**回复模板库 (`response-templates.md`)**](references/response-templates.md) | 各种日常场景的中英文回复模板与首次贡献致谢 | 起草回复草稿时 | 3 分钟 |
| 🔍 [**PR 审查指南 (`pr-review-guide.md`)**](references/pr-review-guide.md) | 审查清单、刷 KPI 贡献防御、Rulesets 与合并策略 | 审查外部 PR 时 | 4 分钟 |
| 🛡️ [**私有安全协同 SOP (`security-vulnerability-sop.md`)**](references/security-vulnerability-sop.md) | 官方 PVR、临时私有 Fork 修复、申请 CVE 与 GHSA 公开披露 | 接收并处置安全漏洞时 | 4 分钟 |
| 🚀 [**版本发布工作流 (`release-workflow.md`)**](references/release-workflow.md) | SemVer 语义化规则、Release 说明模板与社交广播推文 | 准备打 Tag 和发布新版本时 | 4 分钟 |
| 🤝 [**社区治理与贡献者 (`community-and-contributors.md`)**](references/community-and-contributors.md) | 社区冲突 4 级降温处置、All Contributors 致谢与 Sponsors 运营 | 处置冲突或运营贡献者生态时 | 4 分钟 |
| ⚙️ [**自动化模板 (`automation-templates.md`)**](references/automation-templates.md) | Stale、Issue Labeler、欢迎机器人、Dependabot 与 CODEOWNERS 配置 | 搭建仓库自动化 CI 时 | 4 分钟 |
| 📊 [**运营报告指南 (`reporting.md`)**](references/reporting.md) | 核心指标定义（MTTR/MTTM）与运营周报模板 | 周期性复盘项目健康度时 | 3 分钟 |
| 🔑 [**GitHub 授权指南 (`github-access-guide.md`)**](references/github-access-guide.md) | 5 级授权优先级、最小权限配置与回退路径 | 需要写操作或配置访问时 | 3 分钟 |

---

## 📁 文件结构

```
github-oss-ops/
├── SKILL.md                          # 核心技能定义：铁律、任务路由表、通用流程与事实卡
├── README.md                         # 中文说明文档
├── README.en.md                      # 英文说明文档
├── CHANGELOG.md                      # 版本发布记录
├── LICENSE                           # MIT 开源许可证
├── .gitignore                        # Git 忽略规则
├── CONTRIBUTING.md                   # 社区贡献指南
├── CODE_OF_CONDUCT.md                # 行为准则
├── SECURITY.md                       # 安全策略
├── CONTRIBUTORS.md                   # 贡献者名单
├── manifest.json                     # 技能元数据清单
├── agents/                           # 多 Agent 平台元数据
├── assets/                           # 门面配图与预览图
├── examples/                         # 三大实战案例
├── tests/
│   └── test_validate.py              # 校验器的正向与负向测试
├── scripts/
│   └── validate.py                   # 技能包自检（唯一校验入口，零依赖）
└── references/                       # 10 本深度运营手册
    ├── github-oss-ops-pitfalls.md    # 核心避坑指南与深水区脆弱点防御
    ├── triage-workflow.md            # Issue 分流决策树与 AI 幻觉识别
    ├── response-templates.md         # 多场景回复模板与首次贡献致谢
    ├── pr-review-guide.md            # PR 审查清单与刷 KPI 贡献防御
    ├── security-vulnerability-sop.md # 官方 PVR、临时私有 Fork 与 CVE 协同
    ├── release-workflow.md           # SemVer 发版与全渠道社交广播推文
    ├── community-and-contributors.md # 社区冲突 4 级降温与 All Contributors
    ├── automation-templates.md       # Stale / Issue Labeler / 欢迎 / Dependabot 配置
    ├── reporting.md                  # MTTR/MTTM 指标与运营周报
    └── github-access-guide.md        # 5 级授权路径与最小权限指南
```

---

---

## 🌐 GitHub 开源全生命周期协作矩阵 (Open Source Lifecycle Suite)

面向独立开发者与开源团队的完整工具链闭环：

| 阶段 / 角色 | 推荐技能 | 核心使命与能力 | GitHub 仓库 |
|---|---|---|---|
| 📦 **开源前准备** | [**`github-oss-prep`**](https://github.com/hyt315/github-oss-prep) | 自动化生成规范门面、中英双语 README、CI 工作流、社区资产与合规审计 | [hyt315/github-oss-prep](https://github.com/hyt315/github-oss-prep) |
| 🩺 **质量体检** | [**`skill-doctor`**](https://github.com/hyt315/skill-doctor) | 50+ 项工业级静态规则 + 动态实跑自测，确保 Agent Skill 100% 满分无死角 | [hyt315/skill-doctor](https://github.com/hyt315/skill-doctor) |
| ⚙️ **开源后运营** | [**`github-oss-ops`**](https://github.com/hyt315/github-oss-ops) | 智能分流 Issue、AI 垃圾防御、PR 辅助审查、GHSA 私有漏洞协同与发版全渠道广播 | [hyt315/github-oss-ops](https://github.com/hyt315/github-oss-ops) |
| 🚀 **贡献者导航** | [**`github-oss-contribute`**](https://github.com/hyt315/github-oss-contribute) | 面向贡献者的全程向导：Fork 同步、Rebase 冲突消解、DCO 签名、反 AI Slop 质量门禁 | [hyt315/github-oss-contribute](https://github.com/hyt315/github-oss-contribute) |

---

## ❓ 常见问题 (FAQ)

- **Q: 为什么所有的写操作都需要人工确认？**  
  A: 开源项目维护者的一言一行直接代表项目公信力。读写分离确保 AI 只能在后台准备好分析和草稿，绝不会发生“AI 自动回复愚蠢内容”或“自动误关关键 Issue”的事故。
- **Q: 如何防御大模型批量生成的“假 Bug 报告”？**  
  A: `triage-workflow.md` 提供了 AI 幻觉 Issue 识别特征库（虚构 API、无法对齐的报错堆栈），并配有礼貌劝退模板与 Interaction limits（临时互动限制）指引。
- **Q: 收到疑似安全漏洞为什么绝不能在公开 Issue 回复？**  
  A: 公开披露漏洞细节会导致未打补丁的用户暴露在 0-day 攻击风险下。技能指导维护者使用 GitHub 官方 Private Vulnerability Reporting (PVR)，在临时私有分叉中协同开发补丁并申请 CVE。

---

## 🤝 参与贡献

欢迎提交 Issue 与 Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。如果这个技能对你有帮助，欢迎在 GitHub 上点个 [Star ⭐](https://github.com/hyt315/github-oss-ops/stargazers)！

---

## 📄 开源协议

本项目采用 [MIT 许可证](LICENSE) 开源。

---

> 🌏 **English: [README.en.md](./README.en.md)**
