# 社区治理、冲突处置与贡献者运营指南

> 遵循 GitHub Open Source Guides、All Contributors 规范与 GitHub Sponsors 运营实践。

---

## 目录

- [一、社区冲突 4 级降温与处置阶梯](#一社区冲突-4-级降温与处置阶梯)
- [二、去情绪化沟通与维护者应对文案](#二去情绪化沟通与维护者应对文案)
- [三、All Contributors 24 种全景致谢规范](#三all-contributors-24-种全景致谢规范)
- [四、贡献者成长与维护者晋升阶梯](#四贡献者成长与维护者晋升阶梯)
- [五、GitHub Sponsors 赞助与商业可持续运营](#五github-sponsors-赞助与商业可持续运营)

---

## 一、社区冲突 4 级降温与处置阶梯

当遇到离题争论、恶意攻击或违反 Code of Conduct 的行为时，遵循标准阶梯式处理：

```
Level 1: 善意提醒与规则指引 ──> 针对轻微离题、粗鲁语气
    ↓
Level 2: 隐藏非建设性评论 ────> 标记为 off-topic / spam / abuse / disruptive
    ↓
Level 3: 锁定讨论 (Lock) ─────> 针对无休止情绪化争论或已解决但被刷屏的 Issue
    ↓
Level 4: 封禁与举报 (Block) ──> 针对持续人身攻击、恶意骚扰、垃圾广告账号
```

### 1. 隐藏评论（Hide Comment）
在评论右上角菜单选择 `Hide`，并选择官方原因：
- `Off-topic`（偏离主题）；
- `Spam`（垃圾广告）；
- `Abuse`（滥用违规）；
- `Duplicate`（重复内容）。

### 2. 锁定讨论（Lock Conversation）
在 Issue / PR 右侧边栏点击 `Lock conversation`，选择锁定原因：
- `Resolved`（问题已解决）；
- `Off-topic`（讨论已跑题）；
- `Too heated`（讨论情绪过激）；
- `Spam`（垃圾评论泛滥）。

### 3. 封禁用户（Block User）
- 组织维护者可将恶意用户从 Organization 屏蔽（支持 1天/3天/7天/30天/永久）；
- 严重违反平台规则的可直接通过 `Report content` 向 GitHub Trust & Safety 官方举报。

---

## 二、去情绪化沟通与维护者应对文案

维护者始终保持专业、冷静与中立。

### 模板 1：提醒遵守 Code of Conduct
> 感谢参与讨论。为了保持社区健康与建设性的交流氛围，请大家遵守我们的 Code of Conduct (CODE_OF_CONDUCT.md)，避免情绪化言论，聚焦于技术问题本身。

### 模板 2：锁定过热讨论
> 本讨论已偏离技术主题且存在情绪化交流。为了维护健康的社区环境，我们已暂时锁定本 Issue。如果对具体技术实现有新的构想，欢迎在 [Discussions](https://github.com/hyt315/github-oss-ops/discussions) 中开启建设性探讨。

---

## 三、All Contributors 24 种全景致谢规范

不仅致谢写代码的人，凡是对项目有贡献的人都应被记录：

| 贡献类型 | 标识 Emoji | 适用场景 |
|---|:---:|---|
| **代码 (Code)** | 💻 | 提交了功能或修复代码 |
| **文档 (Documentation)** | 📖 | 编写或改进了 README、Wiki、教程 |
| **设计 (Design)** | 🎨 | 设计了 Logo、UI、插图、配色 |
| **Bug 反馈 (Bug reports)** | 🐛 | 提交了详尽、高质量的 Bug 复现报告 |
| **分流与问答 (Triage / Q&A)** | 🔍 / 💬 | 在 Issue / Discussions 帮助解答他人问题 |
| **翻译与本地化 (Translation)** | 🌍 | 翻译了多语言文档与界面 |
| **测试与 CI (Tests / Infra)** | ⚠️ / 🚇 | 编写单元测试、优化 GitHub Actions CI |
| **赞助与资助 (Financial)** | 💵 | 通过 GitHub Sponsors 等渠道提供财务支持 |

---

## 四、贡献者成长与维护者晋升阶梯

设计透明的晋升阶梯，帮助贡献者成为共同维护者：

1. **First-time Contributor（首次贡献者）**：
   - 及时合并符合标准的简单 PR，发送热情致谢；
   - 推荐标有 `good first issue` 或 `help wanted` 的后续任务。
2. **Regular Contributor（活跃贡献者）**：
   - 贡献 3+ 个高质量 PR 的开发者；
   - 邀请加入项目的 GitHub Team 或 Discord / 微信维护者群。
3. **Triage Member（分流协作员）**：
   - 赋予仓库 `Triage` 权限（可打标签、分流 Issue、管理 Discussions，不可直接 Push）。
4. **Core Collaborator（核心维护者）**：
   - 赋予仓库 `Write` 权限；
   - 参与版本决策、PR 审查与技术路线图规划。

---

## 五、GitHub Sponsors 赞助与商业可持续运营

### 1. 配置 `.github/FUNDING.yml`
```yaml
github: [hyt315]
patreon: your_patreon
open_collective: your_project
custom: ['https://afdian.com/a/your_name', 'https://buymeacoffee.com/your_name']
```

### 2. 设计合理的赞助层级 (Sponsor Tiers)
- **$5/月 (Coffee Supporter)**：README 赞助者名单展示 + 专属 Sponsor 徽章；
- **$25/月 (Backer)**：个人头像与链接在 README 首页滚动展示；
- **$100/月 (Bronze Sponsor)**：企业 Logo 挂载在 README 与文档首页；
- **$500/月 (Silver/Gold Sponsor)**：商业企业优先 Issue 响应与咨询支持通道。
