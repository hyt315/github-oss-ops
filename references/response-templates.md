# 回复模板库

> 各场景的 Issue/PR 回复草稿模板。SKILL.md Step 4 引用本文件。
> 所有模板均为草稿，维护者确认或修改后才发送。

---

## 目录

- [Bug 回复](#bug-回复)
- [功能请求回复](#功能请求回复)
- [使用问题回复](#使用问题回复)
- [重复 Issue 回复](#重复-issue-回复)
- [安全漏洞回复](#安全漏洞回复)
- [首次贡献者欢迎](#首次贡献者欢迎)
- [过期提醒](#过期提醒)
- [关闭说明](#关闭说明)
- [PR 审查回复](#pr-审查回复)
- [Dependabot PR 回复](#dependabot-pr-回复)

---

## Bug 回复

### 确认可复现

**中文**：
```
感谢反馈！我已确认这是一个 Bug，标记为 `type:bug`。

**复现信息**：
- 环境：{os} / {version}
- 复现步骤：{steps}

正在排查中，修复后会在本 Issue 中更新进展。
```

**英文**：
```
Thanks for reporting this! I've confirmed this is a bug and labeled it as `type:bug`.

**Reproduction info**:
- Environment: {os} / {version}
- Steps: {steps}

I'm looking into it and will update this issue with progress.
```

### 不可复现，需要更多信息

**中文**：
```
感谢反馈！我尝试复现了这个问题，但在我的环境中没有出现。

能否提供以下信息帮助排查？
- 操作系统和版本
- 项目版本号
- 完整的错误日志或截图
- 最小复现步骤

提供后我会重新检查。
```

**英文**：
```
Thanks for the report! I tried to reproduce this but couldn't on my end.

Could you provide the following to help debug?
- OS and version
- Project version
- Full error log or screenshot
- Minimal reproduction steps

I'll take another look once you provide this info.
```

---

## 功能请求回复

### 合理的建议

**中文**：
```
感谢你的建议！这个想法不错，我已标记为 `type:enhancement`。

**评估**：
- 可行性：{评估}
- 优先级：{P1/P2/P3}

我会将其加入后续版本的计划中。如果社区有更多人需要这个功能（点赞本 Issue），会优先处理。
```

**英文**：
```
Thanks for the suggestion! This is a great idea — labeled as `type:enhancement`.

**Assessment**:
- Feasibility: {assessment}
- Priority: {P1/P2/P3}

I'll add this to the roadmap. If more community members need this feature (thumbs up on this issue), it'll be prioritized higher.
```

### 不在项目范围内

**中文**：
```
感谢你的建议。经过考虑，这个功能目前不在项目的核心范围内。

**原因**：{具体原因，如"会增加过多依赖"/"与项目定位不符"/"维护成本过高"}

如果有其他想法，欢迎继续提 Issue。
```

**英文**：
```
Thanks for the suggestion. After consideration, this feature is currently outside the project's core scope.

**Reason**: {specific reason, e.g., "would add too many dependencies" / "doesn't align with project goals" / "maintenance cost too high"}

Feel free to open another issue if you have other ideas.
```

---

## 使用问题回复

### 给出解答

**中文**：
```
这个问题可以这样解决：

{具体的解决方案/步骤}

如果需要更多帮助，建议：
- 查阅文档：{文档链接}
- 在 [Discussions](../../discussions) 中提问（问答类讨论更方便检索）
```

**英文**：
```
Here's how to solve this:

{specific solution/steps}

If you need more help:
- Check the docs: {docs link}
- Ask in [Discussions](../../discussions) (Q&A discussions are easier to search)
```

### 信息不足

**中文**：
```
需要了解更多信息才能帮你排查：

1. 你使用的是什么版本？
2. 你的操作步骤是什么？
3. 期望的结果是什么？实际结果是什么？
4. 有没有错误信息？

提供这些信息后我来看下。
```

---

## 重复 Issue 回复

**中文**：
```
这个问题已在 #{original_number} 中讨论过了，那边有更详细的进展。

如果情况有所不同，请补充说明，我会重新评估。
```

**英文**：
```
This has already been discussed in #{original_number}, where there's more detailed progress.

If your situation is different, please add details and I'll re-evaluate.
```

---

## 安全漏洞回复

> **重要**：安全漏洞不应在公开 Issue 中讨论。以下模板用于引导提交者使用私密渠道。

### 引导使用私密渠道

**中文**：
```
感谢你的报告。出于安全考虑，漏洞细节不应在公开 Issue 中讨论。

请通过 GitHub 的 Private Vulnerability Reporting 重新提交：
1. 前往本仓库的 **Security** 标签页
2. 点击 **Report a vulnerability**
3. 填写漏洞详情

我会在收到私密报告后尽快处理。感谢你的负责任披露！

本 Issue 将被关闭。
```

**英文**：
```
Thank you for your report. For security reasons, vulnerability details should not be discussed in public issues.

Please resubmit via GitHub's Private Vulnerability Reporting:
1. Go to the **Security** tab of this repository
2. Click **Report a vulnerability**
3. Fill in the vulnerability details

I'll review the private report as soon as possible. Thank you for responsible disclosure!

This issue will be closed.
```

### 确认收到私密报告

**中文**：
```
已收到你的安全报告，感谢！

**处理计划**：
- 预计在 {N} 天内完成评估
- 确认漏洞后会尽快修复
- 修复发布后会致谢（如果你同意）

在此期间请不要公开讨论此漏洞。
```

**英文**：
```
Security report received. Thank you!

**Plan**:
- Evaluation within {N} days
- Fix will be prioritized once confirmed
- Credit will be given in the release notes (with your permission)

Please do not discuss this vulnerability publicly until a fix is released.
```

---

## 首次贡献者欢迎

**中文**：
```
感谢你的首次贡献！欢迎加入项目。

几个小提示：
- 提交 Issue 时可以使用模板，这样信息更完整
- 如果想贡献代码，可以先看看 [CONTRIBUTING.md](../../blob/main/CONTRIBUTING.md)
- 有任何问题随时在这里问

期待你的参与！
```

**英文**：
```
Thanks for your first contribution! Welcome to the project.

A few tips:
- Using issue templates helps provide complete information
- If you'd like to contribute code, check out [CONTRIBUTING.md](../../blob/main/CONTRIBUTING.md) first
- Feel free to ask any questions here

Looking forward to your contributions!
```

---

## 过期提醒

### 第一次提醒（Bug/功能请求）

**中文**：
```
这个 Issue 已经 30 天没有活动了。想确认一下：

- 这个问题还在吗？
- 有没有新的信息可以补充？

如果已经解决或不再需要，我会关闭它。如果还需要处理，回复一下我会继续跟进。
```

**英文**：
```
This issue hasn't had activity for 30 days. Just checking in:

- Is this still an issue?
- Any new information to add?

I'll close it if it's resolved or no longer needed. If you still need help, just reply and I'll follow up.
```

### 第二次提醒（等待反馈无回复）

**中文**：
```
这是第二次提醒。之前请求了一些补充信息，目前还没有收到回复。

如果 7 天内没有回复，这个 Issue 会自动关闭。需要帮助的话随时回复。
```

---

## 关闭说明

### Bug 已修复

```
这个问题已在 {commit_hash} / #{pr_number} 中修复。感谢反馈！

如果修复后仍有问题，请重新打开这个 Issue。
```

### 无法复现

```
经过多次尝试，我们无法复现这个问题。可能是环境特定的问题。

如果其他人也遇到了，请提供更多信息，我会重新调查。
```

### 无回复关闭

```
由于超过 {N} 天没有收到回复，暂时关闭这个 Issue。

如果需要继续讨论，随时回复，我会重新打开。
```

---

## PR 审查回复

### 批准合并

```
LGTM! 改动看起来不错。

- 改动范围合理
- 代码风格一致
- {其他具体评价}

感谢贡献！
```

### 需要修改

```
感谢提交！整体方向没问题，有几个地方需要调整：

1. {具体建议 1}
2. {具体建议 2}

修改后我再 review 一次。
```

### 拒绝（礼貌）

```
感谢你的 PR！不过这个改动目前不适合合并，原因是：

{具体原因，如"与项目方向不符"/"已有替代方案"/"需要先讨论设计"}

建议先在 Issue 中讨论方案，确认后再提交代码，避免白做工。
```

---

## Dependabot PR 回复

### 安全更新（优先处理）

```
感谢 Dependabot 的安全更新。

**检查结果**：
- 变更类型：安全修复
- 影响范围：{依赖名称} {旧版本} → {新版本}
- CI 状态：✅ 通过
- 破坏性变更：无

确认无破坏性变更，合并。
```

### 版本更新（需验证）

```
Dependabot 版本更新 PR。

**检查结果**：
- 变更类型：{major/minor/patch} 版本更新
- 影响范围：{依赖名称} {旧版本} → {新版本}
- CI 状态：{✅ 通过 / ❌ 失败}
- 破坏性变更：{有/无，如有则说明}

{如 CI 失败}：CI 检查未通过，需要排查兼容性问题。暂时不合并。
{如 major 更新}：major 版本更新，需要检查 CHANGELOG 和迁移指南。
{如无问题}：确认无破坏性变更，合并。
```

### 暂不合并（major 版本有破坏性变更）

```
这个 Dependabot PR 是 major 版本更新，可能有破坏性变更。

**需要确认**：
- {依赖名称} 的 CHANGELOG 中标记了哪些破坏性变更
- 项目是否使用了受影响的 API
- 是否需要修改代码以适配新版本

建议先在单独的分支上测试，确认无问题后再合并。
```
