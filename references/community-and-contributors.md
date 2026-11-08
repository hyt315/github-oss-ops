# 社区治理、冲突处置与贡献者运营指南

> 遵循 GitHub Open Source Guides、All Contributors 规范与 GitHub Sponsors 运营实践。

---

## 目录

- [一、社区冲突 4 级降温与处置阶梯](#一社区冲突-4-级降温与处置阶梯)
- [二、去情绪化沟通与维护者应对文案](#二去情绪化沟通与维护者应对文案)
- [三、All Contributors 致谢规范](#三all-contributors-致谢规范)
- [四、贡献者成长与维护者晋升阶梯](#四贡献者成长与维护者晋升阶梯)
- [五、GitHub Sponsors 赞助与商业可持续运营](#五github-sponsors-赞助与商业可持续运营)

---

## 一、社区冲突 4 级降温与处置阶梯

当遇到离题争论、恶意攻击或违反 Code of Conduct 的行为时，遵循标准阶梯式处理：

```
Level 1: 善意提醒与规则指引 ──> 针对轻微离题、粗鲁语气
    ↓
Level 2: 隐藏非建设性评论 ────> Hide 并选原因（Off-topic / Spam / Abuse 等）
    ↓
Level 3: 锁定讨论 (Lock) ─────> 针对无休止情绪化争论或已解决但被刷屏的 Issue
    ↓
Level 4: 封禁与举报 (Block) ──> 针对持续人身攻击、恶意骚扰、垃圾广告账号
```

### 1. 隐藏评论（Hide Comment）
在评论右上角 `...` 菜单选择 `Hide`，再选原因。GitHub 提供的原因：`Spam`、`Abuse`、`Off-topic`、`Outdated`、`Duplicate`、`Resolved`、`Low quality`（以页面实际选项为准）。

- 隐藏 Issue／PR 评论需要仓库 **Write** 权限；Triage 只能隐藏 Discussions 里的评论。
- 评论里含敏感信息（凭据、漏洞细节）时，仅编辑删掉不够：编辑历史对有读权限的人可见，还要在 `edited` 下拉里**删除那一版修订**。

### 2. 锁定讨论（Lock Conversation）
在 Issue / PR 右侧边栏点击 `Lock conversation`，选择锁定原因：
- `Resolved`（问题已解决）；
- `Off-topic`（讨论已跑题）；
- `Too heated`（讨论情绪过激）；
- `Spam`（垃圾评论泛滥）。

### 3. 封禁用户（Block User）
- 个人仓库：在个人设置里屏蔽该用户；组织仓库：由组织 **Owner 或 Moderator** 在组织设置中屏蔽，可选永久或一段时间；
- 突发刷屏先用 **Interaction limits**（仓库 Settings → Moderation options → Interaction limits）临时降温，详见 [避坑指南 §6](github-oss-ops-pitfalls.md#6-社区防刷与危机处置互动限制评论隐藏与治理降温)；
- 严重违规用评论或主页上的 `Report content`／`Report abuse` 向 GitHub 举报。

---

## 二、去情绪化沟通与维护者应对文案

维护者始终保持专业、冷静与中立。

### 模板 1：提醒遵守 Code of Conduct
> 感谢参与讨论。为了保持社区健康与建设性的交流氛围，请大家遵守我们的 Code of Conduct (CODE_OF_CONDUCT.md)，避免情绪化言论，聚焦于技术问题本身。

### 模板 2：锁定过热讨论
> 本讨论已偏离技术主题且存在情绪化交流。为了维护健康的社区环境，我们已暂时锁定本 Issue。如果对具体技术实现有新的构想，欢迎在 Discussions（`https://github.com/<owner>/<repo>/discussions`） 中开启建设性探讨。

---

## 三、All Contributors 致谢规范

不只致谢写代码的人。下表是常用类型，完整列表与 key 以官方 [Emoji Key](https://allcontributors.org/emoji-key/) 为准（2026-11 核对时为 33 种）：

| 贡献类型（key） | Emoji | 适用场景 |
|---|:---:|---|
| 代码 `code` | 💻 | 提交了功能或修复代码 |
| 文档 `doc` | 📖 | 编写或改进了 README、Wiki、教程 |
| 设计 `design` | 🎨 | 设计了 Logo、UI、插图、配色 |
| Bug 反馈 `bug` | 🐛 | 提交了详尽、高质量的 Bug 复现报告 |
| 答疑 `question` | 💬 | 在 Issue／Discussions 帮助解答他人问题 |
| 审查 PR `review` | 👀 | 审查他人的 PR |
| 翻译 `translation` | 🌍 | 翻译了多语言文档与界面 |
| 测试 `test` | ⚠️ | 编写测试 |
| 基础设施 `infra` | 🚇 | 维护 CI、构建与托管 |
| 资助 `financial` | 💵 | 通过 GitHub Sponsors 等渠道提供财务支持 |

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
   - 赋予仓库 `Triage` 权限：可打标签、指派、关闭／重开 Issue 与 PR，可移动、锁定 Discussions；不能 Push、不能批准或合并 PR，不能管理 Discussions 分类。
4. **Core Collaborator（核心维护者）**：
   - 赋予仓库 `Write` 权限；
   - 参与版本决策、PR 审查与技术路线图规划。

---

## 五、GitHub Sponsors 赞助与商业可持续运营

### 1. 配置 `.github/FUNDING.yml`
```yaml
github: [your_github_username]
patreon: your_patreon
open_collective: your_project
custom: ['https://afdian.com/a/your_name', 'https://buymeacoffee.com/your_name']
```

### 2. 设计合理的赞助层级 (Sponsor Tiers)
- **$5/月 (Coffee Supporter)**：README 赞助者名单展示 + 专属 Sponsor 徽章；
- **$25/月 (Backer)**：个人头像与链接在 README 首页滚动展示；
- **$100/月 (Bronze Sponsor)**：企业 Logo 挂载在 README 与文档首页；
- **$500/月 (Silver/Gold Sponsor)**：商业企业优先 Issue 响应与咨询支持通道。
