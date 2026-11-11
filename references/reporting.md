# 运营报告模板

> 适用任务：运营周报／月报。默认统计最近 7 天，用户可指定起止日期。所有时间用 UTC，报告里写明统计窗口。

## 指标定义

| 指标 | 定义 | 取数 |
|------|------|------|
| 新 Issue / 关闭 Issue | 窗口内创建／关闭的 Issue 数（不含 PR） | `gh api -X GET search/issues -f q="repo:OWNER/REPO is:issue created:START..END" --jq .total_count`，关闭同理用 `closed:` |
| 首次响应时间 | Issue 创建 → 第一条**维护者**评论（排除作者本人和机器人） | 逐条读评论；样本少于 5 条时注明 |
| MTTR（解决时长） | Issue 创建 → 关闭 | `gh issue list --state closed --search "closed:START..END" --limit 1000 --json createdAt,closedAt`，两者相减 |
| MTTM（合并时长） | PR 创建 → 合并 | `gh pr list --state merged --search "merged:START..END" --limit 1000 --json createdAt,mergedAt` |
| Issue 净变化 | 新增 − 关闭（正数表示积压在涨） | 由上两项计算 |
| 新 PR / 合并 PR / 关闭未合并 | 窗口内数量 | 同上用 `search/issues` 的 `total_count`：`is:pr created:START..END`／`is:pr is:merged merged:START..END`／`is:pr is:unmerged closed:START..END` |
| 未关闭 Issue / PR 总数 | 报告时刻的积压 | `search/issues` 的 `total_count`：`is:issue is:open`／`is:pr is:open`（`open_issues_count` 含 PR，不能直接用） |
| 贡献者 / 首次贡献者 | 窗口内有合并 PR 的人；其中第一次被合并的人 | 合并 PR 的作者去重；首次需查其历史 PR |
| Star / Fork 变化 | 与上期快照相比 | API 只给当前总数，上期没有快照就写“无基线” |

**计数别用列表长度**：`gh issue list`／`gh pr list` 默认只返回 30 条，`--limit` 之外的会被静默截掉，数量一律取 `search/issues` 的 `total_count`；需要逐条计算时长时才拉列表，并核对列表条数等于 `total_count`，不等就注明“样本被截断”。搜索 API 单次查询最多返回 1000 条。

**统计口径**：时长类指标用**中位数**并给出样本数，不用平均数（少数陈年 Issue 会把平均值拉得很高）。MTTR、MTTM 是本技能的约定口径，不是 GitHub 官方指标。

## 报告模板

```text
## 运营报告 — {owner}/{repo}
统计窗口：{start} ~ {end}（UTC）

### 数据概览
| 指标 | 本期 | 上期 | 变化 |
|------|------|------|------|
| 新 Issue | N | N | +N |
| 关闭 Issue | N | N | +N |
| Issue 净变化 | +N | +N | — |
| 首次响应中位数 | Xh（样本 N） | Xh | 改善/变差 |
| MTTR 中位数 | Xd（样本 N） | Xd | 改善/变差 |
| 新 PR / 合并 PR | N / N | N / N | — |
| MTTM 中位数 | Xd（样本 N） | Xd | 改善/变差 |
| 首次贡献者 | N | N | +N |
| Star | +N | +N | — |

### 健康评估（参考阈值，按项目规模调整）
- 首次响应：< 2 天良好；2–7 天一般；> 7 天需改进
- Issue 净变化：连续两期为正，说明积压在涨
- PR 等待审查：超过 7 天未回应的 PR 数

### 需要关注
- [具体 Issue／PR 编号与原因]

### 建议
- [基于上面数据的 1–3 条行动建议，区分“事实”与“推断”]
```

> 上期数据没有时写“无基线”，不要编造。阈值是经验值，不是行业标准。
