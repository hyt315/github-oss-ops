# ⚙️ GitHub OSS Ops / github-oss-ops

<div align="center">

**Approval-gated GitHub repository operations skill for maintainers — intelligent issue triage, PR review assistance, and release management.**

**给独立维护者和小团队用的 GitHub 运营 Agent Skill：智能分流 Issue、辅助 PR 审查、自动化版本发布，所有外部写操作均留在明确批准之后。**

[![Validate](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml/badge.svg)](https://github.com/hyt315/github-oss-ops/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/hyt315/github-oss-ops?sort=semver)](https://github.com/hyt315/github-oss-ops/releases/latest)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/hyt315/github-oss-ops?style=social)](https://github.com/hyt315/github-oss-ops/stargazers)

[English](./README.en.md) | [中文](./README.md)

</div>

![GitHub OSS Ops workflow: scan, triage, draft, approve, act and report](assets/social-preview.png)

---

## 📖 What is this?

Launching an open-source project is only the first step; maintaining it is an endurance run:
- Sorting through incoming issues to check for duplicates, assign priority, and draft replies;
- Reviewing community PRs for diff scope, CI status, test coverage, and breaking risks;
- Organizing release notes and version updates following SemVer rules;
- Managing stale issues gently without abrupt automatic closures.

**`github-oss-ops`** structures these demanding tasks into **reproducible, automated workflows** while **strictly keeping the human in the loop** — all external write operations (commenting, labeling, closing, PR reviews, tags, and releases) require explicit approval.

---

## ✨ Key Features

| Core Workflow | Capabilities & Actions | Value Delivered & Boundaries |
|---|---|---|
| 📋 **Issue Triage** | Aggregates new issues, checks duplicates, classifies severity, drafts replies | Read operations automatic; labeling/closing requires approval |
| 🔍 **PR Review Assist** | Summarizes diff scope, CI results, breaking risks, and release impact | Never masquerades as a human; reviews require explicit approval |
| 🚀 **Release Management** | Recommends SemVer bumps from merged PRs, generates changelogs, checks consistency | Tags, Releases, and asset uploads confirmed separately |
| 🧹 **Stale Governance** | Identifies inactive issues/PRs and recommends phased, courteous reminders | Never closes issues automatically |
| 📊 **Ops Insights Report** | Tracks response times, backlog trends, merge rhythm, and health metrics | Strictly distinguishes facts from AI inferences |

---

## 📊 5-Workflow Complete Architecture

```
[Input: User asks to scan repo / triage issues / review PR / release]
                                 │
         [Workflow 1: Issue Triage & Duplication Check] ─> Draft classifications
                                 │
         [Workflow 2: PR Risk & CI Assisted Review] ─────> Test & risk audits
                                 │
         [Workflow 3: SemVer Bump & Release Notes] ──────> Changelog & tag draft
                                 │
         [Workflow 4: Stale Item Governance] ────────────> Polite batch reminders
                                 │
         [Workflow 5: Community Health & Ops Report] ────> Response metrics & report
```

---

## 📚 Real-World Walkthroughs

Three end-to-end verified examples, detailed in [examples/README.md](examples/README.md):
1. [New Issue Triage & Duplication Check](examples/README.md#示例一新-issue-分流)
2. [PR Risk Review & CI Diagnostics](examples/README.md#示例二pr-风险审查)
3. [Weekly Report & Release Drafts](examples/README.md#示例三周报与-release-草稿)

---

## 🚀 Quick Start

This is an AI Agent Skill — install it into your AI assistant and you're ready.

### Option A: Paste one sentence into any Agent (recommended, most universal)

Send this to your AI assistant and it will detect the platform and clone to the right skills directory:

> Please install the github-oss-ops skill: clone `https://github.com/hyt315/github-oss-ops` into your skills directory (e.g. `~/.claude/skills/github-oss-ops`, `~/.agents/skills/github-oss-ops`, or `~/.cursor/skills/github-oss-ops`) and confirm it works. When I want to triage issues, review PRs, release versions, or generate ops reports, guide me with explicit write-action approvals.

### Option B: GitHub CLI 2.90+ (one command)

```bash
gh skill install hyt315/github-oss-ops github-oss-ops --agent claude-code --scope user
```

### Option C: Manual per-platform install

| Platform | User-level Path | Project-level Path |
|---|---|---|
| **Claude Code** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.claude/skills/github-oss-ops` | `.claude/skills/github-oss-ops` |
| **Codex** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.agents/skills/github-oss-ops` | `.agents/skills/github-oss-ops` |
| **Cursor** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.cursor/skills/github-oss-ops` | `.cursor/skills/github-oss-ops` |
| **General Agents** | `git clone https://github.com/hyt315/github-oss-ops.git ~/.agents/skills/github-oss-ops` | `.agents/skills/github-oss-ops` |

### Option D: Run local regression selftest

```powershell
python scripts/selftest.py
```

---

## 🔒 Permission Boundaries & Safety Principles

- **Read-Only First**: Repository scanning, issue triage analysis, and PR risk reviews run locally read-only;
- **Strict Approval Gates**: Adding labels, posting comments, closing issues, submitting reviews, tagging, and creating Releases require user approval;
- **Fact vs. Inference**: Reports strictly distinguish empirical repository data from AI recommendations.

---

## 📥 Download

| Method | Command / Link |
|---|---|
| **HTTPS** | `git clone https://github.com/hyt315/github-oss-ops.git` |
| **SSH** | `git clone git@github.com:hyt315/github-oss-ops.git` |
| **GitHub CLI** | `gh repo clone hyt315/github-oss-ops` |
| **ZIP** | [Download ZIP](https://github.com/hyt315/github-oss-ops/archive/refs/heads/main.zip) |
| **Tarball** | [Download Tar](https://github.com/hyt315/github-oss-ops/archive/refs/heads/main.tar.gz) |
| **Single file (SKILL.md)** | `curl -O https://raw.githubusercontent.com/hyt315/github-oss-ops/main/SKILL.md` |

---

## 📁 File Structure

```
github-oss-ops/
├── SKILL.md                          # Core skill definition and ops workflows
├── README.md                         # Chinese documentation
├── README.en.md                      # English documentation
├── CHANGELOG.md                      # Version history
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── CONTRIBUTING.md                   # Contribution guide
├── CODE_OF_CONDUCT.md                # Code of conduct
├── SECURITY.md                       # Security policy
├── SUPPORT.md                        # Support channels
├── manifest.json                     # Skill manifest
├── agents/                           # Multi-agent metadata
├── examples/README.md                # 3 Verified end-to-end case studies
├── scripts/
│   ├── validate-skill.mjs            # Validator
│   ├── validate_repo.py              # Structure validator
│   └── selftest.py                   # Automated regression test runner
└── references/                       # Ops guidelines & release playbooks
```

---

## ❓ FAQ

- **Q: Does the skill post comments or apply labels automatically?**  
  A: No. It generates drafts and classifications first; write operations execute only after your explicit approval.
- **Q: How does it recommend SemVer version numbers?**  
  A: It analyzes merged PRs since the last release: breaking changes -> Major, new features -> Minor, bugfixes -> Patch.
- **Q: What token permissions are required?**  
  A: Read-only audits require standard read permissions; write operations use Fine-grained PATs with scoped access.

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). If this skill helped you, please give it a [Star ⭐](https://github.com/hyt315/github-oss-ops/stargazers)!

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

> 🌏 **中文版: [README.md](./README.md)**
