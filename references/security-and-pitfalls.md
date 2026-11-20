# 私有漏洞响应 SOP 与运维避坑指南

> 适用任务：处理安全漏洞报告（PVR / GHSA / CVE）、排查仓库 CI/权限/Rulesets 安全基线与应对突发刷屏。

## 1. 私有漏洞响应 SOP（PVR / GHSA）

### 1.1 漏洞被误发到公开 Issue 时（止损优先）
- GitHub **没有**「把公开 Issue 转成安全公告」的按钮，公开仓库的 Issue 也无法改为私密。
- **正确顺序**：
  1. 有写权限者立刻编辑隐藏利用细节，并**删除包含敏感细节的编辑历史修订**（情况极严重时由管理员直接删除 Issue）；
  2. **修复前不要打 `type:security` 或 `priority:P0` 标签**，避免把未修复漏洞标红指给所有人；
  3. 在公开评论里仅礼貌引导报告者通过私有渠道提交（绝不复述细节）；
  4. 维护者在 `Security & quality → Advisories`（原 Security 标签页）手动新建草稿安全公告继续跟进。

### 1.2 开启与使用 Private Vulnerability Reporting (PVR)
- 核查状态：`gh api repos/<owner>/<repo>/private-vulnerability-reporting`（返回 `{"enabled": true|false}`）。
- 开启路径：`Settings → Advanced Security → Private vulnerability reporting`。
- 收到报告后评估真实性与严重级别（防范 AI 生成的虚假漏洞报告：先对照源码核实函数与攻击路径是否真实存在）。
- 在公告页点击 **Start a temporary private fork** 协同开发补丁（注意：临时私有 Fork **无法运行 GitHub Actions CI**，需本地完整测试）。
- 确认需要编号时在公告页点击 **Request CVE**（GitHub 作为 CNA 通常在 72 小时内审核，并非自动秒批）。
- 与报告者约定协调披露日期（行业常见上限 90 天）；先发布修复版本，再发布安全公告（发布后经 GitHub 审核可触发下游 Dependabot 告警，但并非所有生态全覆盖）。

## 2. 权限与 CI/CD 供应链避坑

- **`GITHUB_TOKEN` 权限**：新建个人仓库默认只读，但老仓库或组织仓库可能仍为读写。核对 `gh api repos/<owner>/<repo>/actions/permissions/workflow`，并在每个 workflow 顶层显式声明 `permissions: { contents: read }`，仅在发版等必要 job 局部放宽。
- **`pull_request_target` 防 Pwn-Request**：该触发器拥有基础仓库 Secrets 与可写 Token。只做元数据操作（如打标签）时不检出 PR 代码；只要需要构建或跑测试，必须用 `pull_request`；确需带凭据测外部代码时放入带 **Environment protection rules** 人工审批的环境。
- **锁定外部 Action 40 位 SHA**：所有第三方及官方 `uses:` 均锁定完整 commit SHA 并附版本注释，用 Dependabot（`github-actions`）自动滚版本。
- **Fork PR 工作流审批**：在 `Settings → Actions → General → Approval for running fork pull request workflows from contributors` 至少设为 `Require approval for first-time contributors`。

## 3. 分支与发版标签保护（Rulesets）

- 核查命令：`gh api repos/<owner>/<repo>/rulesets`。
- **套餐差异**：Free/Pro/Team 只有 `Active` 与 `Disabled`；`Evaluate` 观察模式仅 Enterprise 提供；组织级规则集需 Team 或 Enterprise。
- **保护发版标签**：为 `v*` 建标签规则集，勾选 `Restrict updates` 与 `Restrict deletions`，防止已发布 tag 被覆盖或删除；不要把 `Repository admin` 放进默认 Bypass。
- **构建溯源（可选）**：使用 `actions/attest-build-provenance` 为发布产物生成出处证明，下游可用 `gh attestation verify` 校验（单独使用可达 SLSA Build Level 2）。

## 4. 社区防刷与 API 限流

- **Interaction limits**：路径 `Settings → Moderation options → Interaction limits`，支持 `Limit to existing users`（限注册 <24 小时无贡献账号）、`Limit to prior contributors`、`Limit to repository collaborators`，时长可选 24 小时 / 3 天 / 1 周 / 1 个月 / 6 个月。也可在此处限制无写权限用户的并发 PR 数量。
- **API 限流退避**：未认证 60 次/小时，认证用户 5,000 次/小时；遇到 `403`/`429` 次级限流时读取 `retry-after` 或 `x-ratelimit-reset` 退避重试，避免并发批量写操作。
- **跨平台换行符**：在根目录 `.gitattributes` 声明 `* text=auto eol=lf`（及 `*.sh`/`*.py` 强制 LF），避免 Windows CRLF 导致 Linux Runner 报错。
