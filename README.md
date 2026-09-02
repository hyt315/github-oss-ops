<div align="center">

# ⚙️ GitHub OSS Ops / 开源项目运营

**给独立维护者和小团队用的 GitHub 运营 Agent Skill：扫描 Issue/PR、生成可审查草稿、辅助版本发布，所有外部写操作都留在明确批准之后。**

**简体中文 · [English](./README.en.md)**

[![Validate](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml/badge.svg)](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/hyt315/github-oss-ops?sort=semver)](https://github.com/hyt315/github-oss-ops/releases)
[![Downloads](https://img.shields.io/github/downloads/hyt315/github-oss-ops/total)](https://github.com/hyt315/github-oss-ops/releases)
[![Contributors](https://img.shields.io/github/contributors/hyt315/github-oss-ops)](CONTRIBUTORS.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/hyt315/github-oss-ops?style=social)](https://github.com/hyt315/github-oss-ops/stargazers)

</div>

![GitHub OSS Ops workflow: scan, triage, draft, approve, act and report](assets/social-preview.png)

---

## 📖 这是什么？

项目发布只是开始。维护者还要反复查看 Issue、确认重复、审查 PR、跟踪 CI、整理版本说明、处理长期无响应内容。**GitHub OSS Ops** 把这些步骤组织成**可复核的工作流**，同时**保留人的最终决定权**——所有外部写操作（评论、标签、关闭、Review、Tag、Release、推送）都在明确批准之后执行。

### ✨ 核心特性

| 工作流 | Skill 会做什么 | 默认边界 |
| --- | --- | --- |
| Issue 分流 | 聚合新 Issue、判断类型/优先级/重复项、起草回复 | 读取可直接进行；评论、标签、关闭需批准 |
| PR 辅助审查 | 汇总 diff、CI、风险、测试和发布影响 | 不伪装成人工审查，未批准不提交 Review |
| Release 管理 | 按已合并改动建议 SemVer、生成说明、核对版本一致性 | Tag、Release、推送分别确认 |
| Stale 管理 | 识别长期无响应内容并提出分批处理建议 | 不自动批量关闭 |
| 运营报告 | 输出响应时间、积压、合并和版本节奏 | 区分事实、推断与建议 |

---

## 📚 示例：三个可复核的完整工作流

1. [新 Issue 分流与重复检测](examples/README.md#示例一新-issue-分流)
2. [PR 风险审查与 CI 诊断](examples/README.md#示例二pr-风险审查)
3. [周报与 Release 草稿](examples/README.md#示例三周报与-release-草稿)

---

## 🚀 快速开始

> ✨ **一句话装进 AI Agent**：把下面这段话直接发给你的 AI 助手，它会自动完成安装——
>
> ```text
> 请安装 github-oss-ops Skill：把 https://github.com/hyt315/github-oss-ops 克隆到你的 skills 目录（Claude Code：~/.claude/skills/github-oss-ops/；Codex：~/.agents/skills/github-oss-ops/；Cursor：~/.cursor/skills/github-oss-ops/），并确认 SKILL.md、references/、scripts/ 都在。以后我要「管理我的开源项目 / 分流 Issue / 审查 PR / 发版 / 出周报」时，按 SKILL.md 的九步工作流引导我完成，所有写操作都在我确认后执行。
> ```

| 平台 | 用户级安装 |
| --- | --- |
| **Claude Code** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.claude/skills/github-oss-ops` |
| **Codex / ChatGPT** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.agents/skills/github-oss-ops` |
| **Cursor** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.cursor/skills/github-oss-ops` |

> 项目级安装把路径换成 `.claude/skills/`、`.agents/skills/`、`.cursor/skills/`（项目根目录）。新安装未发现时重启对应 Agent。**注意：必须安装完整仓库**（SKILL.md 会引用 references/），单文件不是完整安装。

---

## 💬 触发方式

对 AI 说以下任意一类话，即会触发本技能：

- 「帮我看下我的开源项目」「有哪些新 Issue 要处理」
- 「这个 Issue 怎么分类/回」「PR 有风险吗」
- 「帮我发个版 / 出周报 / 清理 stale Issue」

## ⚙️ 前置条件

- **Git** 已安装；目标仓库为 GitHub 上的开源项目
- 公开仓库的只读扫描**无需认证**；只有读取私有数据或执行写操作时才需要 GitHub 授权（官方连接、`gh`、MCP OAuth、fine-grained PAT 或网页，按此优先级）
- 不要求把 Token 发到聊天；**所有写操作在执行前给你看草稿并获得确认**

## 📦 输出交付物

```text
📋 Issue 分流结果 —— 类型/优先级/重复检测/回复草稿（标签与评论待批准）
🧾 PR 审查摘要   —— diff+CI+风险+测试，三段式意见（Review 待批准）
📦 版本方案       —— SemVer 建议 + Changelog 草稿 + 版本号同步清单（Tag/Release 待批准）
🩺 Stale 建议     —— 分批处理提议（不自动关闭）
📊 运营报告       —— 响应时间/积压/合并节奏 + 健康评估与建议
```

---

## 📥 下载 / 安装

```bash
# HTTPS
git clone https://github.com/hyt315/github-oss-ops.git

# SSH
git clone git@github.com:hyt315/github-oss-ops.git

# GitHub CLI
gh repo clone hyt315/github-oss-ops

# ZIP
# https://github.com/hyt315/github-oss-ops/archive/refs/heads/main.zip

# 单文件（仅 SKILL.md，注意不是完整安装）
curl -O https://raw.githubusercontent.com/hyt315/github-oss-ops/main/SKILL.md
```

---

## 📁 文件结构

```
github-oss-ops/
├── SKILL.md                      # 技能入口（九步工作流）
├── references/
│   ├── automation-templates.md   # Actions 自动化模板（stale/labeler/welcome/auto-assign/dependabot）
│   ├── github-access-guide.md    # 授权路径与最小权限
│   ├── pr-review-guide.md        # PR 审查清单与模板
│   ├── release-workflow.md       # 版本管理与 release 流程
│   ├── reporting.md              # 运营报告模板与指标
│   ├── response-templates.md     # 回复模板
│   └── triage-workflow.md        # Issue 分流决策树与模板
├── scripts/
│   ├── validate-skill.mjs        # 结构校验（CI 用）
│   └── selftest.py               # 回归测试（好夹具绿 + 负向被抓）
├── examples/README.md            # 三个端到端工作流示例
├── agents/openai.yaml
├── LICENSE / CHANGELOG.md
├── README.md  /  README.en.md   # 双语说明（本文件为中文）
└── .github/                      # Issue/PR 模板 + CI(validate)
```

---

## ▶️ 快速使用

九步工作流各自独立可用——你可能只卡在某个环节：

1. **确认目标仓库** → 2. **扫描项目状态**（输出状态摘要） → 3. **Issue 分流**（分类/优先级/重复检测） → 4. **智能回复**（按场景生成草稿） → 5. **PR 审查辅助**（diff+CI 汇总） → 6. **版本管理**（PR 合并后 SemVer+Changelog） → 7. **过期管理**（Stale 分批建议） → 8. **运营报告** → 9. **自动化配置**（生成 Actions 模板，含 Rulesets 建议）

> 每个外部动作（评论、标签、关闭、Review、Tag、Release、推送）都要先给你看草稿、获得确认后执行；安全漏洞 Issue 走私密通道（Private vulnerability reporting），不在公开评论确认。

---

## 🤝 贡献 / 反馈

- 报 Bug / 提建议：用仓库的 Issue 模板
- 贡献：见 [CONTRIBUTING.md](CONTRIBUTING.md)，改动前跑 `python scripts/selftest.py` 与 `node scripts/validate-skill.mjs`
- 漏洞报告：见 [SECURITY.md](SECURITY.md)（私有漏洞报告，勿走公开 Issue）

---

## 📜 License

[MIT](LICENSE) © 2026 hyt315

> 🌏 **English version: [README.en.md](./README.en.md)**