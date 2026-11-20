# ⚙️ GitHub OSS Ops / 开源项目运营

<div align="center">

**轻量化、审批门禁驱动的 GitHub 开源维护技能：Issue 智能分流、AI 垃圾与提示词注入防御、PR 辅助审查、PVR/GHSA 私有漏洞响应、SemVer 发版与精准运营报告。**

**Lightweight, approval-gated GitHub maintainer ops skill: Issue triage, AI slop & prompt-injection defense, PR review, PVR/GHSA vulnerability SOP, SemVer releases, and accurate health reporting.**

[![Validate](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml/badge.svg)](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/hyt315/github-oss-ops?sort=semver)](https://github.com/hyt315/github-oss-ops/releases/latest)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](./README.en.md) | [中文](./README.md)

</div>

![GitHub OSS Ops workflow: scan, triage, draft, approve, act and report](assets/social-preview.png)

## 这是什么？

开源项目上线后，维护者每天面对的是 Issue 分流、AI 幻觉与低质 PR 噪音、安全漏洞私有协同、发版与周报。`github-oss-ops` 用一套精简的按需路由手册把这些事交给 AI 协助分析与起草，同时守住三条硬边界：

- **默认只读，写操作逐项审批**：评论、打标、关闭、合并、打 Tag、发 Release 必须先展示目标与内容，经维护者确认后再执行并回读。
- **外部内容一律不可信**：把 Issue/PR 文本与注释严格当作数据，防止恶意 Prompt Injection 诱导 AI 自动批准或执行越权命令。
- **拒绝过度模板化**：不硬塞几百行客套话模板，只保留经过核对的 GitHub 官方边界、精确 `gh`/API 命令与避坑清单。

## 快速开始

### 方式 A：把这句话发给你的 AI 助手（最省事）

> 请帮我安装 `github-oss-ops` 技能：将 `https://github.com/hyt315/github-oss-ops` 安装到你的 skills 目录，并确认安装成功。

安装后直接说「帮我分流一下新 Issue」「审查一下这个 PR」「准备发个新版本」或「出份本月运营报告」即可触发。

### 方式 B：使用 `npx skills` 一键安装（支持 90+ Agent）

```bash
# 安装到当前项目
npx skills add hyt315/github-oss-ops

# 全局安装（推荐）
npx skills add hyt315/github-oss-ops -g
```

### 方式 C：手动克隆

```bash
# Claude Code
git clone https://github.com/hyt315/github-oss-ops.git ~/.claude/skills/github-oss-ops

# Cursor
git clone https://github.com/hyt315/github-oss-ops.git ~/.cursor/skills/github-oss-ops

# Codex / 通用 Agents 目录
git clone https://github.com/hyt315/github-oss-ops.git ~/.agents/skills/github-oss-ops
```

### 本地自检

```bash
python3 scripts/validate.py
python3 -m unittest discover tests -v
```

## 工作方式

```text
[用户请求：体检 / 分流 Issue / 审查 PR / 处理漏洞 / 发版 / 出周报]
                              │
  [SKILL.md 4 路任务路由] ──> 只读当前任务对应的 1 份精简手册
                              │
  [只读收集] ──────────────> gh / REST / MCP 拉取真实数据（防 30 条截断）
                              │
  [产出草稿] ──────────────> 事实卡 + 风险分析 + 自然语言回复/Review/Release 草稿
                              │
  [待批准清单] ────────────> 逐项确认后执行并回读核对
```

## 文件结构

```text
github-oss-ops/
├── SKILL.md                             # 主入口：铁律、任务路由、只读快照与事实卡
├── scripts/validate.py                  # 零依赖技能包自检脚本
├── tests/test_validate.py               # 正向与负向单元测试
├── references/
│   ├── triage-and-pr.md                 # Issue 分流、AI Slop 与 Prompt Injection 防御、PR 审查与回复底线
│   ├── security-and-pitfalls.md         # PVR/GHSA 私有漏洞 SOP、CI 供应链与 Rulesets 避坑
│   ├── release-and-reporting.md         # SemVer 发版、Release Notes 与无截断运营报告
│   └── automation-and-access.md         # 最小权限访问、按需自动化（Stale/Dependabot）与社区治理
└── .github/workflows/validate.yml       # Python 3.10 / 3.12 矩阵 CI
```

## 开源生命周期协作套件

- **[`github-oss-prep`](https://github.com/hyt315/github-oss-prep)**：开源前准备——确定性隐私与安全审计、必要/可选门面整理、现代安装范式与授权发布。
- **[`github-oss-ops`](https://github.com/hyt315/github-oss-ops)**：开源后运营——Issue 分流、AI 垃圾与注入防御、PR 审查、PVR/GHSA 安全协同与发版运营。
- **[`github-oss-contribute`](https://github.com/hyt315/github-oss-contribute)**：贡献者导航——Fork 同步、Rebase 冲突处理、DCO 签名与高质量 PR 自查。

## 开源协议

本项目采用 [MIT 许可证](LICENSE) 开源，完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。
