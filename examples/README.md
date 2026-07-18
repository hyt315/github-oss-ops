# GitHub OSS Ops examples

These examples make the skill's output and approval boundaries inspectable before installation. Repository names and issue text are illustrative; the workflow and fields are the enforced contract.

## 示例一：新 Issue 分流

**Prompt**

```text
扫描 owner/repo 最近 7 天的新 Issue。识别重复项、类型、优先级和需要补充的信息。先给草稿，不要写入 GitHub。
```

**Expected read-only output**

```text
时间窗口：2026-07-11 至 2026-07-18
Issue #42 — Windows 渲染失败
分类：type:bug / priority:high
证据：包含可复现命令；CI 中 Windows job 同类失败
可能重复：#37（相同错误码，仍需维护者确认）
建议：请求系统版本和最小复现仓库
草稿：感谢反馈。为了确认是否与 #37 相同，请补充……

待批准写操作：添加 type:bug、priority:high；发送上述评论。
```

只有用户确认具体 Issue、标签和评论内容后，才执行写操作。

## 示例二：PR 风险审查

**Prompt**

```text
审查 PR #57。检查改动范围、测试、敏感信息、CI、兼容性和发布影响，不要提交 Review 或合并。
```

**Expected output**

```text
结论：Request changes（草稿）
高风险：工作流从 pull_request 改为 pull_request_target，并读取 PR 分支脚本
中风险：新增依赖未更新锁文件
已通过：单元测试、格式检查
缺失：威胁说明、最小权限 permissions
建议 Review：请恢复 pull_request，或说明为何必须使用 pull_request_target……

待批准写操作：提交 Request changes Review。
```

## 示例三：周报与 Release 草稿

**Prompt**

```text
生成本周运营报告，并根据 v1.2.0 之后已合并 PR 起草下一版 Release。不要创建 Tag 或 Release。
```

**Expected output**

```text
统计窗口：2026-07-11 00:00Z 至 2026-07-18 00:00Z
新 Issue 8 / 关闭 6 / 净增加 2
新 PR 5 / 合并 4 / 关闭未合并 1
首次响应中位数：9.4 小时（样本 7）
建议版本：v1.3.0
依据：2 个向后兼容功能、3 个修复、1 个文档更新
Release 草稿：Added … / Fixed … / Documentation …

待批准写操作：版本文件 PR、Tag、GitHub Release（分别确认）。
```
