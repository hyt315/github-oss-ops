# 版本发布与运营报告指南

> 适用任务：确定 SemVer 版本号、生成 Changelog 与 Release Notes、创建 GitHub Release、出周报/月报。改版本文件、打 Tag、发 Release 与对外宣传各自独立确认。

## 1. 版本号与 Changelog 规范

- **SemVer 规则**：破坏性变更升 `MAJOR`；向后兼容新功能升 `MINOR`；向后兼容修复升 `PATCH`；`0.y.z` 阶段不承诺 API 兼容；仅文档/重构/内部整理是否发版由项目自定。
- **提取真实改动（避免漏掉 Squash / Rebase PR）**：不要只用 `git log --merges`，优先用以下任一命令：
  ```bash
  R=owner/repo
  # 方式 1：拉取上次发版后合并的 PR
  gh pr list -R $R --state merged --base main --search "merged:>=YYYY-MM-DD" --limit 100 --json number,title,labels,author
  # 方式 2：调用 GitHub 自动生成 Release Notes 草稿
  gh api repos/$R/releases/generate-notes -f tag_name="vX.Y.Z" -f previous_tag_name="vA.B.C" --jq .body
  ```
- **Changelog 格式**：遵循 Keep a Changelog（Added / Changed / Deprecated / Removed / Fixed / Security），安全修复必须单列在 Security 下。
- **版本文件同步**：更新项目实际存在的版本清单（如 `package.json`、`pyproject.toml`、`Cargo.toml`、`manifest.json`、`SKILL.md` 的 `metadata.version`）；Go 项目 v2+ 需注意模块路径 `/vN` 后缀。

## 2. 创建 Tag 与 Release（必须回读）

1. 确认目标分支 CI 全绿且本地无未提交改动。
2. 推送带注释 tag 并创建正式 Release（只推 tag 不算发版）：
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   gh release create vX.Y.Z -R $R --title "vX.Y.Z" --notes-file RELEASE_NOTES.md
   ```
3. 回读确认：`gh release view vX.Y.Z -R $R --json tagName,name,url,assets`。
4. **可选对外宣传**：仅在用户明确要求时，基于同一份 Release Notes 针对 2–3 个真实活跃渠道（如 X、V2EX、Reddit、Discussions）分别改写简短版本，突出「解决什么问题 + 真实变化 + 升级命令」，不发千篇一律的硬广。

## 3. 运营报告（避免 30 条截断失真）

- **精准计数（不要用默认只返回 30 条的 `gh issue list` 计数）**：
  ```bash
  R=owner/repo
  # 本周期新建 / 关闭的 Issue 与 PR 精确总数
  gh api -X GET search/issues -f q="repo:$R is:issue created:YYYY-MM-DD..YYYY-MM-DD" --jq .total_count
  gh api -X GET search/issues -f q="repo:$R is:issue is:closed closed:YYYY-MM-DD..YYYY-MM-DD" --jq .total_count
  gh api -X GET search/issues -f q="repo:$R is:pr is:merged merged:YYYY-MM-DD..YYYY-MM-DD" --jq .total_count
  ```
- **核心健康指标（用中位数并注明样本数）**：
  - **首次响应时长**：外部 Issue 创建到维护者首次有效回复的中位数；
  - **MTTR（解决时长）**：Bug Issue 创建到关闭的中位数；
  - **MTTM（合并时长）**：PR 创建到合并的中位数（需要逐条算时长时用 `--limit 1000` 并核对是否触及上限）。
- **报告结构**：严格区分「客观数据（附取数范围与样本数）」「主要进展（合并 PR / 发版）」「待处理风险（积压、CI 失败、安全事项）」「下周期建议行动」。查不到的数据直接写「未查」，绝不估算。
