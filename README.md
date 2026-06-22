# 🛠️ GitHub 开源项目运营 / GitHub OSS Ops

<div align="center">

**开源发布后的"AI 客服"：Issue 智能分流、PR 辅助审查、版本管理、运营报告，一站式搞定**

**AI-powered operations for open-source repos: smart Issue triage, PR review assistance, release management, and ops reporting**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.1-green.svg)]()
[![SKILL.md](https://img.shields.io/badge/Agent%20Skill-SKILL.md-green)](SKILL.md)

[English](#english) | [中文](#中文)

</div>

---

## 中文

## 📖 这是什么？

**GitHub 开源项目运营** 是一个 AI Agent Skill，专为已发布的开源项目日常维护设计。它能自动扫描 Issue/PR、智能分类打标签、起草回复、审查代码、管理 Release 版本、处理过期 Issue，甚至生成运营报告。

> 💡 与 [github-oss-prep](https://github.com/hyt315/github-oss-prep) 配合使用：oss-prep 负责项目发布准备，本技能负责发布后的日常运营。

### ✨ 核心功能

| 功能模块 | 说明 |
|----------|------|
| 🔍 **Issue 扫描** | 扫描未读 Issue，按类型智能分类（Bug/Feature/Question/文档） |
| ✍️ **智能回复** | 基于模板自动起草回复，支持流转状态、打标签 |
| 📋 **PR 审查** | 按规则审查 PR 标题格式、改动影响、敏感信息、工作流对齐 |
| 📦 **版本管理** | 自动生成 Release Notes，基于 Conventional Commits 计算版本号 |
| 🧹 **过期清理** | 扫描过期 Issue/PR，起草关闭或提醒回复 |
| 📊 **运营报告** | 生成统计报告：新建/关闭趋势、响应时间、活跃贡献者排行 |
| ⚙️ **自动化配置** | 生成 GitHub Actions 工作流，配置 Issue 自动管理 |

---

## 🚀 快速开始

这是一个 AI Agent Skill，安装到任意 AI 编程助手后即可使用。

### 怎么用

安装后直接告诉 AI 助手你的需求：

- "看看这个仓库有什么新 Issue？"
- "帮我审查这个 PR"
- "这个 Issue 该怎么回复？"
- "生成这周的运营报告"
- "帮我管理过期 Issue"

每个操作都会先生成草稿展示给你确认，明确同意后才执行。

---

## 📥 安装 / Installation

| 平台 | 安装命令 |
|------|----------|
| **Claude Code** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.claude/skills/github-oss-ops` |
| **Codex** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.codex/skills/github-oss-ops` |
| **Cursor** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.cursor/skills/github-oss-ops` |

> 安装后 Skill 自动生效，无需额外配置。需要 GitHub 访问权限（PAT 或 MCP），首次使用时 Skill 会自动引导配置。

---

## 📥 下载 / Download

| 方式 | 命令 / 链接 |
|------|------------|
| **HTTPS** | `git clone https://github.com/hyt315/github-oss-ops.git` |
| **SSH** | `git clone git@github.com:hyt315/github-oss-ops.git` |
| **GitHub CLI** | `gh repo clone hyt315/github-oss-ops` |
| **ZIP 源码** | [下载 ZIP](https://github.com/hyt315/github-oss-ops/archive/refs/heads/main.zip) |
| **Tar 源码** | [下载 Tar](https://github.com/hyt315/github-oss-ops/archive/refs/heads/main.tar.gz) |

---

## 💡 核心理念

- **只起草，不发送**：所有操作都先生成草稿展示给你，确认后才执行
- **渐进式运营**：不需要一次配置全部，按需使用各功能模块
- **维护者视角**：帮助个人维护者或小型团队降低维护负担

---

## 📁 文件结构

```
github-oss-ops/
├── SKILL.md                          # Skill 核心定义
├── README.md                         # 本文件
├── LICENSE                           # MIT 协议
├── .gitignore                        # Git 忽略规则
├── CONTRIBUTING.md                   # 贡献指南
├── CODE_OF_CONDUCT.md                # 行为准则
├── SECURITY.md                       # 安全策略
├── .github/
│   ├── pull_request_template.md      # PR 模板
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.yml            # Bug 报告表单
│       ├── feature_request.yml       # 功能建议表单
│       └── doc_improvement.yml       # 文档改进表单
└── references/                       # 参考文件
    ├── automation-templates.md       # 自动化配置模板
    ├── github-access-guide.md        # GitHub 访问指南
    ├── triage-workflow.md            # Issue 分流工作流
    ├── response-templates.md         # 回复模板库
    ├── pr-review-guide.md            # PR 审查指南
    └── release-workflow.md           # 发版工作流
```

---

## 🤝 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可

[MIT](LICENSE)

---

## English

## 📖 What is this?

**GitHub OSS Ops** is an AI Agent Skill for day-to-day open-source repository maintenance. It automates Issue triage, drafts replies, assists with PR reviews, manages releases, handles stale items, and generates operations reports.

> 💡 Works alongside [github-oss-prep](https://github.com/hyt315/github-oss-prep): oss-prep handles project launch prep, this skill handles post-launch operations.

### ✨ Core Features

| Module | Description |
|--------|-------------|
| 🔍 **Issue Scanning** | Scan unread Issues, auto-classify by type (Bug/Feature/Question/Docs) |
| ✍️ **Smart Replies** | Draft context-aware replies based on templates with status/label suggestions |
| 📋 **PR Review** | Rule-based PR review: title format, impact, sensitive info, workflow alignment |
| 📦 **Release Management** | Auto-generate release notes, calculate Semantic Version from Conventional Commits |
| 🧹 **Stale Cleanup** | Scan stale Issues/PRs, draft close or reminder replies |
| 📊 **Ops Reports** | Generate stats: open/close trends, response times, active contributors |
| ⚙️ **Automation Setup** | Generate GitHub Actions workflows for automated Issue management |

---

## 🚀 Quick Start

This is an AI Agent Skill — install it in any AI coding assistant and it's ready to use.

### How to use

Once installed, simply tell your AI assistant what you need:

- "Check for new Issues in this repo"
- "Review this PR for me"
- "How should I reply to this Issue?"
- "Generate this week's operations report"
- "Help me clean up stale Issues"

Every action drafts first, shows you for review, then executes only after your approval.

---

## 📁 File Structure

```
github-oss-ops/
├── SKILL.md                          # Core skill definition
├── README.md                         # This file
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── CONTRIBUTING.md                   # Contribution guide
├── CODE_OF_CONDUCT.md                # Code of conduct
├── SECURITY.md                       # Security policy
├── .github/
│   ├── pull_request_template.md      # PR template
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.yml            # Bug report form
│       ├── feature_request.yml       # Feature request form
│       └── doc_improvement.yml       # Docs improvement form
└── references/                       # Reference documents (6 files)
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

[MIT](LICENSE)
