# ⚙️ GitHub OSS Ops / Repository Operations

<div align="center">

**Industrial-grade GitHub repository operations skill for maintainers — intelligent issue triage, AI slop defense, PR review, GHSA vulnerability SOP, release management, and multi-channel broadcasting.**

**给独立维护者与开源团队打造的 AI 运营中枢：智能分流 Issue、AI 垃圾防御、PR 辅助审查、GHSA 私有漏洞协同、自动化版本发布与全渠道广播宣发。**

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

## 📖 What is this?

Launching an open-source project is only the first step — daily maintenance is a long-distance marathon:
- Facing influxes of new issues, identifying whether reports are AI-generated hallucinations, and routing general inquiries to Discussions;
- Reviewing external PRs for diff scope, CI health, breaking changes, and contribution-farming whitespace edits;
- Handling security reports via official Private Vulnerability Reporting (PVR) and GHSA without leaking 0-days in public threads;
- Calculating SemVer release notes from merged PRs and preparing multi-channel release broadcast copy for Twitter/Reddit/Discord;
- Applying 4-step de-escalation moderation SOPs for heated community conflicts.

**`github-oss-ops`** organizes these complex tasks into **reproducible, structured, approval-gated workflows**, while **firmly keeping human maintainers in full control** — all external write actions (commenting, labeling, closing, merging, tagging, creating releases) require explicit user approval before execution.

---

## ✨ Key Features

| Workflow | Capabilities & Actions | Value & Guardrails |
|---|---|---|
| 📋 **Issue Triage & AI Defense** | Aggregates issues, classifies priority, **detects 2026 AI hallucination issues**, routes Q&A to Discussions | Automated reading; comments and closures require approval |
| 🔍 **PR Review & Slop Defense** | Analyzes diff scope, CI status, **filters low-effort PRs**, audits Rulesets and Merge Queue | Never impersonates human review; no unapproved review comments |
| 🛡️ **GHSA Private Security SOP** | Receives PVR reports, creates Temporary Private Forks, requests official CVE IDs | Strictly forbids public vulnerability discussions |
| 🚀 **SemVer Release & Broadcast** | Suggests SemVer numbers, generates grouped changelogs, **drafts multi-channel social posts (X/Reddit/Discord)** | Tags, releases, and binary assets require independent approval |
| 🤝 **Community Moderation & Ladder** | 4-step de-escalation ladder (Hide/Lock/Block), **All Contributors 24-type acknowledgment** | Maintains a welcoming community and prevents burnout |
| 💰 **Sponsorship & Sustainable Ops** | `.github/FUNDING.yml` config, sponsor tier design, and commercial enterprise support channels | Helps projects build financial and community sustainability |
| 📊 **Repository Health & Metrics** | Calculates MTTR, MTTM, manages Stale Bot, and generates weekly operational digests | Distinguishes objective facts from recommendations |

---

## 📊 Complete Operational Workflow Pipeline

```
[Input: User asks to scan repository / triage issues / review PRs / release]
                                 │
   [Step 1: Target Repo & Auth Probing] ─> Read references/github-access-guide.md
                                 │
   [Step 2: Repository Status Scan] ────> Aggregates open issues/PRs & recent activity
                                 │
   [Step 3: Issue Triage & Defense] ────> Read references/triage-workflow.md (AI Hallucinations + Discussions)
                                 │
   [Step 4: Structured Reply Drafting] ──> Read references/response-templates.md (Drafts -> Approval -> Send)
                                 │
   [Step 5: PR Review & Slop Filter] ───> Read references/pr-review-guide.md (Diff scope + Breaking changes)
                                 │
   [Step 6: Private Security Handling] ──> Read references/security-vulnerability-sop.md (PVR + Fork + CVE)
                                 │
   [Step 7: Release & Broadcasting] ────> Read references/release-workflow.md (SemVer + Social broadcast)
                                 │
   [Step 8: Community Moderation] ──────> Read references/community-and-contributors.md (De-escalation + All Contributors)
                                 │
   [Step 9: Automation & Reporting] ────> Read references/automation-templates.md & reporting.md
```

---

## 🛡️ 2026 AI Slop Defense & GHSA Vulnerability SOP

### 1. 2026 AI Slop & Contribution Farming Defense Matrix

```
[New Inbound Contribution]
           │
           ├──> [Issue Audit] ──> Contains hallucinated APIs / fake config / unaligned stack traces?
           │         │
           │         ├── Yes ──> Label resolution:invalid, politely reject and close
           │         └── No ───> Normal triage (Bug/Feature/Docs), route discussions to GitHub Discussions
           │
           └──> [PR Review] ────> Whitespace-only / useless comments / mechanical renames (Contribution farming)?
                     │
                     ├── Yes ──> Politely reject per Contributing guidelines, keeping master clean
                     └── No ───> Audit diff scope, CI status, breaking changes & test coverage
```

### 2. GHSA 90-Day Coordinated Vulnerability Disclosure Flow

```
[Researcher Reports Vulnerability] ──> Via GitHub Private Vulnerability Reporting (PVR)
                                                   │
                  [Create Temporary Private Fork for Collaboration]
                                                   │
                  [Request Official CVE ID via GitHub as CNA]
                                                   │
                  [90-Day Coordinated Vulnerability Disclosure Window]
                                                   │
                  [Publish Security Advisory + Release Patch ➔ Dependabot Alerts]
```

---

## 📚 Real-World Examples

Three end-to-end verified examples in [examples/README.md](examples/README.md):
1. [Issue Triage and Duplicate Detection](examples/README.md#示例一新-issue-分流)
2. [PR Risk Review and CI Diagnosis](examples/README.md#示例二pr-风险审查)
3. [Weekly Report and Release Drafting](examples/README.md#示例三周报与-release-草稿)

---

## 🚀 Quick Start

This is an AI Agent Skill — install it to your AI assistant to use it immediately.

### Option A: Paste one sentence into any Agent (recommended, universal)

Send this to your AI assistant and it will clone to the right skills directory:

> Please install the github-oss-ops skill: clone `https://github.com/hyt315/github-oss-ops` into your skills directory (e.g. `~/.claude/skills/github-oss-ops`, `~/.agents/skills/github-oss-ops`, or `~/.cursor/skills/github-oss-ops`) and confirm it works. When I ask to manage my open-source repository, triage issues, review PRs, handle security advisories, or draft releases, guide me through the SKILL.md workflow with approval-gated writes.

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

### Option D: Run regression tests locally

```powershell
# Run structure validation
node scripts/validate-skill.mjs

# Run regression selftest
python scripts/selftest.py

# Run skill-doctor audit
python path/to/skill-doctor/scripts/audit.py . --dynamic
```

---

## 🔒 Permissions & Safety Principles

- **Strict Read-Only by Default**: Reading public repositories requires no tokens and only analyzes public data;
- **Approval-Gated Writes**: Commenting, labeling, closing, merging, tagging, and creating releases require explicit user confirmation;
- **Zero Credential Harvesting**: Never asks for tokens in chat and never scans local private configuration files;
- **Least-Privilege Model**: Only requests permissions strictly necessary for the active task.

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

## 📖 In-Depth Technical References

| Reference Guide | Core Focus | When to Read | Estimated Time |
|---|---|---|---|
| 📋 [**Issue Triage Workflow (`triage-workflow.md`)**](references/triage-workflow.md) | Decision trees, AI hallucination defense, Discussions routing | When triaging incoming issues | 4 mins |
| 💬 [**Response Templates (`response-templates.md`)**](references/response-templates.md) | Standard response templates and first-timer acknowledgments | When drafting replies | 3 mins |
| 🔍 [**PR Review Guide (`pr-review-guide.md`)**](references/pr-review-guide.md) | PR checklist, low-effort PR defense, Rulesets, merge strategies | When reviewing pull requests | 4 mins |
| 🛡️ [**Security Vulnerability SOP (`security-vulnerability-sop.md`)**](references/security-vulnerability-sop.md) | PVR, Temporary Private Forks, CVE requests, GHSA publication | When handling security advisories | 4 mins |
| 🚀 [**Release Workflow (`release-workflow.md`)**](references/release-workflow.md) | SemVer rules, release notes templates, multi-channel social copy | When cutting new releases | 4 mins |
| 🤝 [**Community & Contributors (`community-and-contributors.md`)**](references/community-and-contributors.md) | 4-step de-escalation, All Contributors recognition, Sponsors ops | When moderating or growing community | 4 mins |
| ⚙️ [**Automation Templates (`automation-templates.md`)**](references/automation-templates.md) | Stale Bot, Release Drafter, Issue Labeler configurations | When setting up repository automation | 4 mins |
| 📊 [**Reporting Guide (`reporting.md`)**](references/reporting.md) | MTTR/MTTM metrics definitions and weekly report templates | When reviewing project health | 3 mins |
| 🔑 [**GitHub Access Guide (`github-access-guide.md`)**](references/github-access-guide.md) | 5-level auth hierarchy and least-privilege configuration | When configuring access | 3 mins |

---

## 📁 File Structure

```
github-oss-ops/
├── SKILL.md                          # Core skill definition, progressive dispatch & 9 operational steps
├── README.md                         # Chinese documentation
├── README.en.md                      # English documentation
├── CHANGELOG.md                      # Version history
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── CONTRIBUTING.md                   # Contribution guide
├── CODE_OF_CONDUCT.md                # Code of conduct
├── SECURITY.md                       # Security policy
├── CONTRIBUTORS.md                   # Contributors list
├── manifest.json                     # Skill manifest
├── agents/                           # Multi-agent metadata
├── assets/                           # Media assets and social previews
├── examples/                         # Real-world examples
├── scripts/
│   ├── validate-skill.mjs            # Validation script
│   └── selftest.py                   # Automated regression test runner
└── references/                       # 8 In-depth operational guides
    ├── triage-workflow.md            # Triage decision tree & AI hallucination defense
    ├── response-templates.md         # Reply templates & first-timer acknowledgments
    ├── pr-review-guide.md            # PR review checklist & low-effort PR defense
    ├── security-vulnerability-sop.md # PVR, Temporary Private Forks & CVE requests
    ├── release-workflow.md           # SemVer releases & multi-channel social broadcasting
    ├── community-and-contributors.md # 4-step de-escalation & All Contributors recognition
    ├── automation-templates.md       # Stale / Release Drafter / Labeler configs
    ├── reporting.md                  # MTTR/MTTM metrics & weekly reporting
    └── github-access-guide.md        # 5-level auth hierarchy & least-privilege guide
```

---

## ❓ FAQ

- **Q: Why are all write operations approval-gated?**  
  A: Maintainer credibility is essential. Approval-gated design ensures AI only prepares analysis and drafts in the background, preventing automated mistakes or accidental closures.
- **Q: How does this defend against 2026 AI-generated hallucination bug reports?**  
  A: `triage-workflow.md` includes an AI hallucination checklist (fake APIs, unaligned stack traces) paired with polite deflection templates and concurrency limit guidelines.
- **Q: Why must security vulnerabilities never be discussed in public issues?**  
  A: Public disclosures expose unpatched users to zero-day risks. The skill guides maintainers through official Private Vulnerability Reporting (PVR) and Temporary Private Forks to safely patch vulnerabilities and assign CVEs.

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). If this skill helped you, please give it a [Star ⭐](https://github.com/hyt315/github-oss-ops/stargazers)!

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

> 🌏 **中文版: [README.md](./README.md)**
