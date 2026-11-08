# GitHub 开源项目运维避坑指南

> 适用任务：仓库健康扫描、CI／工作流安全审查、权限与保护规则排查、突发刷屏处置。
> 本文只收“容易踩、后果重”的坑；日常流程见各专题手册，重复内容不在此展开。
> 事实核对日期：2026-11-08（GitHub Docs 与 GitHub Changelog）。GitHub 界面名称变化较快，以实际页面为准。

---

## 目录
1. [权限与凭据](#1-权限与凭据)
2. [CI／CD 供应链与 Pwn Request](#2-cicd-供应链与-pwn-request)
3. [分支与标签保护：Rulesets](#3-分支与标签保护rulesets)
4. [分流治理的两个坑](#4-分流治理的两个坑)
5. [漏洞误报到公开 Issue](#5-漏洞误报到公开-issue)
6. [社区防刷与危机处置：互动限制、评论隐藏与治理降温](#6-社区防刷与危机处置互动限制评论隐藏与治理降温)
7. [API 限流、换行符与代理](#7-api-限流换行符与代理)
8. [运维基线核对清单](#8-运维基线核对清单)

---

## 1. 权限与凭据

### 1.1 `GITHUB_TOKEN` 权限别靠默认值
- **现状**：新建个人仓库默认只给 `contents`／`packages` 读权限；但组织仓库继承组织设置，老仓库可能还是 `Read and write permissions`。不同仓库默认值不同，不能假设。
- **做法**：
  - 核对 `Settings → Actions → General → Workflow permissions`，设为 `Read repository contents and packages permissions`；
  - 每个工作流顶部显式声明最小权限，只在需要的 Job 里局部加写权限：
    ```yaml
    permissions:
      contents: read

    jobs:
      release:
        runs-on: ubuntu-latest
        permissions:
          contents: write
    ```

### 1.2 Classic PAT 范围过大
- **坑**：给自动化用一个全局 `repo` 范围、永不过期的 Classic PAT，一旦泄露，名下所有仓库都暴露。
- **做法**：优先 GitHub App；必须用 PAT 时用 **Fine-grained PAT**，只选目标仓库、设置到期时间、只给需要的权限（如 `Issues: Read and write`），不给 `Administration`。
- 授权通道的优先级见 [github-access-guide.md](github-access-guide.md)。

---

## 2. CI／CD 供应链与 Pwn Request

### 2.1 `pull_request_target` + 检出 PR 代码
- **机理**：`pull_request_target` 在基础仓库的上下文中运行，能拿到 Secrets 和可写 `GITHUB_TOKEN`。若再检出 Fork 分支并执行其中的代码（`npm install` 的 `postinstall`、测试脚本、`make`），攻击者提交一个 PR 就能窃取 Secrets。
- **铁律**：
  1. `pull_request_target` 只做元数据操作（读标题、打标签），**不检出、不执行 PR 代码**；
  2. 需要构建 PR 代码就用 `pull_request`（Fork PR 拿到的是只读 Token、没有 Secrets）；
  3. 确需用敏感凭据测试外部代码时，放进带 **Environment protection rules** 的环境，人工批准后再运行。
- **副作用要知道**：因为 Fork PR 只有只读 Token，基于 `pull_request` 的欢迎评论、自动分配等对 Fork PR 会失败。见 [automation-templates.md](automation-templates.md) 中的说明。

### 2.2 第三方 Action 用可变标签
- **坑**：`uses: some/action@v1` 或 `@main`，上游被黑或标签被改后，CI 静默执行恶意代码。
- **做法**：固定到完整 40 位 commit SHA，并注明版本；配 Dependabot（`package-ecosystem: github-actions`）跟进更新：
  ```yaml
  uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  ```

### 2.3 Fork PR 的工作流审批
- **坑**：自动化账号批量开空 PR，消耗公共仓库的 Actions 资源。
- **做法**：`Settings → Actions → General → Approval for running fork pull request workflows from contributors`，选项：
  - `Require approval for first-time contributors who are new to GitHub`
  - `Require approval for first-time contributors`（默认）
  - `Require approval for all external contributors`（最严）

---

## 3. 分支与标签保护：Rulesets

### 3.1 Rulesets 与经典分支保护
- Rulesets 可同时保护分支和**标签**、支持 Bypass 列表、多条规则叠加，是官方推荐方向；经典分支保护仍可用。
- **套餐差异**：Free／Pro／Team 的规则集只有 `Active` 和 `Disabled`；`Evaluate`（只观察不拦截）仅 GitHub Enterprise 提供。组织级规则集需要 Team 或 Enterprise。
- 核查命令：`gh api repos/<owner>/<repo>/rulesets`。

### 3.2 发版标签被删除或覆盖
- **坑**：删掉 `v2.0.0` 后推送同名篡改标签；或重新构建时覆盖用户已下载的资产。
- **做法**：
  - 建标签规则集，Target 选 `v*` 一类模式，勾选 `Restrict updates` 与 `Restrict deletions`，只把发版机器人放进 Bypass；
  - 构建产物用 Artifact attestations（`actions/attest-build-provenance`，v4 起是 `actions/attest` 的封装）生成出处证明，下游用 `gh attestation verify` 校验。单独使用可达 **SLSA v1.0 Build Level 2**；要到 Level 3 需在受审查的可复用工作流中构建。

### 3.3 管理员绕过
- **坑**：管理员可绕过规则直接 `git push origin main`，跳过 CI 与审查。
- **做法**：Rulesets 中不把 `Repository admin` 放进 Bypass；确需绕过的机器人单列，并定期看审计日志。

---

## 4. 分流治理的两个坑

### 4.1 Stale 机器人误伤
- 自动关闭不等于解决。只对 `status:needs-info` 且超期未回复的 Issue 走 Stale；给 `type:bug`、`status:confirmed`、`security` 等加豁免标签。配置模板见 [automation-templates.md](automation-templates.md)。

### 4.2 AI 生成的低质 Issue／PR
- 识别特征与处理流程见 [triage-workflow.md](triage-workflow.md)（Issue）与 [pr-review-guide.md](pr-review-guide.md)（PR）。
- 大量刷 PR 时：`Interaction limits` 页面可设置**无写权限用户的并发 PR 上限**（2026 年新增，仅限 PR，不限 Issue），可按账号年龄或已合并 PR 数豁免。

---

## 5. 漏洞误报到公开 Issue
- **没有**“把 Issue 转成安全公告”的按钮，公开仓库的 Issue 也不能改为私密。
- **做法**：
  1. 有写权限者先隐藏或编辑掉利用细节，并**删除含细节的编辑历史修订**；情况严重时由管理员删除 Issue；
  2. 在公开评论里请报告者改用私有报告（不复述细节）；
  3. 维护者在 `Security & quality → Advisories` 新建草稿安全公告继续处理。
- 完整流程见 [security-vulnerability-sop.md](security-vulnerability-sop.md)。

---

## 6. 社区防刷与危机处置：互动限制、评论隐藏与治理降温

### 6.1 Interaction limits（临时互动限制）
- 路径：`Settings → Moderation options → Interaction limits`（仓库管理员或组织 Moderator）。
- 三种限制：
  - `Limit to existing users`：限制注册不满 24 小时、无历史贡献且非协作者的账号；
  - `Limit to prior contributors`：限制未向默认分支贡献过且非协作者的用户；
  - `Limit to repository collaborators`：只有有写权限的人能互动。
- 时长：24 小时、3 天、1 周、1 个月、6 个月。到期自动解除。
- 个人账号或组织已开启全局限制时，单个仓库不能再单独设置。

### 6.2 隐藏、锁定、屏蔽
分级处置与原因选项见 [community-and-contributors.md](community-and-contributors.md)。

---

## 7. API 限流、换行符与代理

### 7.1 REST API 限流
- 未认证：每小时 60 次；认证用户：每小时 5,000 次（GitHub App 安装和企业账号可更高）。GraphQL 按点数单独计算主限额。
- 并发或短时突发会触发**次级限流**，返回 `403` 或 `429`。
- 对策：读 `x-ratelimit-remaining`／`x-ratelimit-reset`；有 `retry-after` 就按它等待，否则等到 reset 时间，再指数退避；避免并发请求。

### 7.2 换行符
- Windows 下 `core.autocrlf=true` 可能让脚本以 CRLF 推送，Linux Runner 上报 `: command not found`。仓库根目录用 `.gitattributes` 固定：
  ```gitattributes
  * text=auto eol=lf
  *.sh text eol=lf
  *.py text eol=lf
  ```

### 7.3 代理与证书
- 走本地代理或企业网关时，脚本应支持 `HTTP_PROXY`／`HTTPS_PROXY`；证书报错时导入代理 CA（如设置 `SSL_CERT_FILE`），不要关闭证书校验。

---

## 8. 运维基线核对清单

| 维度 | 检查项 | 合格基线 | 风险 |
|---|---|---|---|
| 凭据 | 工作流默认 Token 权限 | 仓库设置为只读，工作流显式声明 `permissions` | 高 |
| CI 供应链 | `pull_request_target` | 不检出、不执行 PR 代码 | 高 |
| 第三方 Action | 版本锁定 | 完整 commit SHA + 版本注释，Dependabot 跟进 | 中高 |
| Fork PR | 工作流审批 | 至少 `Require approval for first-time contributors` | 中 |
| 发版 | 标签保护 | 标签规则集开启 `Restrict updates` 与 `Restrict deletions` | 高 |
| 溯源 | Artifact attestations | 发布产物生成出处证明 | 中 |
| 分流 | Stale 配置 | 只处理 `needs-info`，豁免 bug／confirmed／security | 中高 |
| 漏洞 | Private vulnerability reporting | 已开启，`SECURITY.md` 指向私有渠道 | 高 |
| 社区 | 突发刷屏 | 熟悉 Interaction limits 与 PR 上限 | 中 |
| 脚本 | 限流 | 读限流头，尊重 `retry-after`，退避重试 | 中 |
