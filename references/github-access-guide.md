# GitHub 访问配置指南

> 本技能需要 GitHub 访问凭据才能操作 Issue 和 PR。本文件说明如何获取和配置。

---

## 目录

- [什么是 PAT](#什么是-pat)
- [第一步：生成 PAT](#第一步生成-pat)
- [第二步：配置到 MCP Server](#第二步配置到-mcp-server)
- [第三步：验证](#第三步验证)
- [GitHub CLI（gh）方式](#github-cligh-方式)
- [Token 自动发现策略](#token-自动发现策略)
- [MCP 工具清单](#mcp-工具清单)
- [curl + REST API 回退方案](#curl--rest-api-回退方案)
- [常见问题](#常见问题)

---

## 什么是 PAT

PAT（Personal Access Token）是 GitHub 的个人访问令牌，用于 API 认证。GitHub 提供两种：

- **Classic PAT**（`ghp_` 前缀）：传统令牌，通过 scope 授权，权限范围较宽
- **Fine-grained PAT**（`github_pat_` 前缀）：细粒度令牌，可限定到特定仓库，更安全但配置更复杂

### 如何选择

| 特性 | Classic PAT | Fine-grained PAT |
|------|-------------|------------------|
| 权限粒度 | 按 scope（如 `repo`） | 按仓库 + 按权限（如 `Issues: Write`） |
| 仓库范围 | 所有可访问仓库 | 可限定到特定仓库 |
| 安全性 | 较低（泄露即全仓库） | 较高（泄露仅限授权仓库） |
| 过期时间 | 可设 No expiration | 必须设过期时间（最长 1 年） |
| 配置难度 | 简单（勾选 `repo`） | 稍复杂（逐项选择权限） |
| GitHub 推荐 | 兼容性最好 | **推荐用于生产环境** |

**本技能推荐**：个人项目用 Classic PAT（配置最简单），正式维护的开源项目用 Fine-grained PAT（更安全）。

---

## 第一步：生成 PAT

### 方式 A：生成 Classic PAT（简单）

1. 打开 https://github.com/settings/tokens/new

2. 点击 **Generate new token (classic)**

3. 填写：
   - **Note**：`github-oss-ops`（备注名称，随意）
   - **Expiration**：选择过期时间（建议 90 天，不建议 No expiration）
   - **Select scopes**：勾选 `repo`（完整仓库访问权限）

4. 点击 **Generate token**

5. **立即复制 token**（`ghp_` 开头的字符串），页面刷新后无法再次查看

### 方式 B：生成 Fine-grained PAT（更安全）

1. 打开 https://github.com/settings/personal-access-tokens/new

2. 填写：
   - **Token name**：`github-oss-ops`
   - **Expiration**：建议 90 天（最长 1 年，到期需重新生成）
   - **Repository access**：选择 **Only select repositories**，勾选要管理的仓库

3. 在 **Repository permissions** 中，按需勾选以下权限：

   | 权限 | 级别 | 用途 |
   |------|------|------|
   | Issues | Read and write | Issue 管理（读取、更新、评论） |
   | Pull requests | Read and write | PR 管理（读取、审查、合并） |
   | Metadata | Read-only | 仓库基本信息（必选） |
   | Labels | Read and write | 标签管理 |
   | Contents | Read-only | 读取文件（PR 改动分析） |
   | Commit statuses | Read-only | CI/CD 状态检查 |
   | Members | Read-only | 贡献者信息 |

4. 点击 **Generate token**

5. **立即复制 token**（`github_pat_` 开头的字符串）

---

## 第二步：配置到 MCP Server

GitHub 官方 MCP Server（`github/github-mcp-server`）提供两种部署方式：

- **远程服务器**（推荐）：GitHub 托管，通过 OAuth 认证，无需 Docker
- **本地服务器**：通过 Docker 运行，使用 PAT 认证

> **重要**：旧的 `@modelcontextprotocol/server-github`（npx 方式）已不再维护，请迁移至官方 `github/github-mcp-server`。下方配置均使用官方版本。

### 前置条件（本地服务器方式）

- 安装 [Docker](https://www.docker.com/) 并确保 Docker 正在运行
- Docker 镜像：`ghcr.io/github/github-mcp-server`（公开镜像，无需登录）

### Cursor

编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_你的token"
      }
    }
  }
}
```

### Claude Desktop

编辑配置文件：
- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_你的token"
      }
    }
  }
}
```

### Windsurf

编辑 `~/.codeium/mcp_config.json`：

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_你的token"
      }
    }
  }
}
```

> 注意：Windsurf 可能不支持环境变量引用，需要直接在 `env` 中硬编码 token。

### VS Code / GitHub Copilot

在项目根目录创建或编辑 `.vscode/mcp.json`：

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github_token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}"
      }
    }
  }
}
```

> 注意：VS Code 使用 `servers` 而非 `mcpServers` 作为顶层键名。`${input:github_token}` 方式会在首次使用时弹窗输入 token，避免硬编码。

### 远程服务器方式（无需 Docker）

如果你的 MCP 客户端支持远程 MCP 服务器（VS Code 1.101+、Claude Desktop、Cursor 等），可以直接使用 GitHub 托管的远程服务器，通过 OAuth 认证，无需 PAT 和 Docker：

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

首次使用时会弹出浏览器窗口完成 OAuth 授权。详见 [GitHub MCP Server 文档](https://github.com/github/github-mcp-server)。

### 通用方式（环境变量）

如果不想使用 MCP，也可以直接设置环境变量，配合 GitHub CLI 或 curl 使用：

```powershell
# Windows PowerShell
$env:GITHUB_TOKEN = "ghp_你的token"
```

```bash
# Linux / macOS
export GITHUB_TOKEN="ghp_你的token"
```

---

## 第三步：验证

### 验证 PAT

```bash
# Linux / macOS
curl -sI -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

```powershell
# Windows PowerShell
curl -sI -H "Authorization: token $env:GITHUB_TOKEN" `
  https://api.github.com/user
```

响应头中 `x-oauth-scopes` 应包含 `repo`（Classic PAT），如：
```
x-oauth-scopes: repo, workflow
```

> Fine-grained PAT 的响应头中 `x-oauth-scopes` 为空，需检查 `x-accepted-github-permissions` 确认权限。

### 验证 MCP Server

启动 MCP 客户端后，尝试调用一个简单工具（如 `list_issues`），如果返回数据说明配置成功。如果报错，检查 Docker 是否运行、token 是否正确。

---

## GitHub CLI（gh）方式

除了 MCP 和 curl，GitHub 官方 CLI 工具 `gh` 是更便捷的替代方案，语法简洁且支持认证管理。

### 安装

| 平台 | 安装命令 |
|------|----------|
| Windows (winget) | `winget install GitHub.cli` |
| Windows (scoop) | `scoop install gh` |
| macOS (Homebrew) | `brew install gh` |
| Linux (apt) | `sudo apt install gh` |

详见 https://cli.github.com/

### 认证

```bash
# 交互式登录（推荐，支持浏览器 OAuth）
gh auth login

# 使用 PAT 登录
gh auth login --with-token < token.txt

# 检查认证状态
gh auth status

# 刷新权限（如需额外 scope）
gh auth refresh -s read:project
```

### 常用 Issue 管理命令

```bash
# 列出未关闭的 Issue
gh issue list --repo owner/repo --state open

# 查看某个 Issue 详情
gh issue view 123 --repo owner/repo

# 创建 Issue
gh issue create --repo owner/repo --title "Bug: xxx" --body "描述"

# 添加标签
gh issue edit 123 --repo owner/repo --add-label "type:bug,priority:P1"

# 添加评论
gh issue comment 123 --repo owner/repo --body "回复内容"

# 关闭 Issue
gh issue close 123 --repo owner/repo --comment "已修复"
```

### 常用 PR 管理命令

```bash
# 列出未关闭的 PR
gh pr list --repo owner/repo --state open

# 查看 PR 详情（含改动文件）
gh pr view 456 --repo owner/repo
gh pr diff 456 --repo owner/repo

# 审查 PR
gh pr review 456 --repo owner/repo --approve --body "LGTM"
gh pr review 456 --repo owner/repo --request-changes --body "需要修改"

# 合并 PR
gh pr merge 456 --repo owner/repo --squash --delete-branch
```

> `gh` CLI 适合交互式操作和简单脚本。批量操作和复杂逻辑建议使用 MCP 工具或 REST API。

---

## Token 自动发现策略

技能运行时按以下优先级自动查找 Token：

1. **环境变量**：读取 `GITHUB_TOKEN` 或 `GITHUB_PERSONAL_ACCESS_TOKEN`
   - bash：`echo $GITHUB_TOKEN`
   - PowerShell：`$env:GITHUB_TOKEN`

2. **MCP 配置文件**：在用户主目录下搜索包含 GitHub MCP 配置的 JSON 文件（深度 3 层）
   - Windows：`Get-ChildItem -Path $HOME -Recurse -Depth 3 -Filter *.json`
   - 匹配内容包含 `GITHUB_PERSONAL_ACCESS_TOKEN` 或 `mcpServers.*github` 的文件

3. **兜底路径**（自动发现失败时参考）：

   | 路径 | 工具 |
   |------|------|
   | `~/.cursor/mcp.json` | Cursor |
   | `%APPDATA%\Claude\claude_desktop_config.json` | Claude Desktop (Windows) |
   | `~/.codeium/mcp_config.json` | Windsurf |
   | `.vscode/mcp.json` | VS Code |

找到配置文件后，解析 JSON 提取 Token：

```python
import json
d = json.load(open("<配置文件路径>"))
for key in ('mcpServers', 'servers', 'mcp'):
    servers = d.get(key, {})
    if 'github' in servers:
        token = servers['github'].get('env', {}).get('GITHUB_PERSONAL_ACCESS_TOKEN', '')
        if token:
            print(token)
            break
```

如所有方式都找不到，引导用户按上方步骤配置 PAT。

---

## MCP 工具清单

本技能使用的 GitHub MCP 工具：

### Issue 操作

| 工具 | 功能 | 底层 API |
|------|------|----------|
| `list_issues` | 列出仓库的 Issue（支持过滤状态、标签） | `GET /repos/{owner}/{repo}/issues` |
| `get_issue` | 获取单个 Issue 详情 | `GET /repos/{owner}/{repo}/issues/{number}` |
| `create_issue` | 创建新 Issue | `POST /repos/{owner}/{repo}/issues` |
| `update_issue` | 更新 Issue（标签、状态、指派人） | `PATCH /repos/{owner}/{repo}/issues/{number}` |
| `add_issue_comment` | 添加 Issue 评论 | `POST /repos/{owner}/{repo}/issues/{number}/comments` |
| `search_issues` | 搜索 Issue | `GET /search/issues` |

### PR 操作

| 工具 | 功能 | 底层 API |
|------|------|----------|
| `list_pull_requests` | 列出 PR | `GET /repos/{owner}/{repo}/pulls` |
| `get_pull_request` | 获取 PR 详情 | `GET /repos/{owner}/{repo}/pulls/{number}` |
| `get_pull_request_files` | 获取 PR 改动文件 | `GET /repos/{owner}/{repo}/pulls/{number}/files` |
| `get_pull_request_status` | 获取 PR 检查状态 | `GET /repos/{owner}/{repo}/pulls/{number}` |
| `get_pull_request_comments` | 获取 PR 评论 | `GET /repos/{owner}/{repo}/pulls/{number}/comments` |
| `get_pull_request_reviews` | 获取 PR 审查 | `GET /repos/{owner}/{repo}/pulls/{number}/reviews` |
| `create_pull_request_review` | 提交 PR 审查意见 | `POST /repos/{owner}/{repo}/pulls/{number}/reviews` |
| `merge_pull_request` | 合并 PR | `PUT /repos/{owner}/{repo}/pulls/{number}/merge` |

### 其他

| 工具 | 功能 |
|------|------|
| `search_repositories` | 搜索仓库 |
| `get_file_contents` | 读取仓库文件 |
| `list_commits` | 列出提交历史 |
| `search_code` | 搜索代码 |
| `search_users` | 搜索用户 |

---

## curl + REST API 回退方案

当 MCP 工具不可用时，通过 curl 直接调用 GitHub REST API：

> **Windows PowerShell 用户注意**：
> - 环境变量引用：将 `$GITHUB_TOKEN` 替换为 `$env:GITHUB_TOKEN`
> - 行续接符：将 `\` 替换为 `` ` ``（反引号）
> - JSON 字符串：PowerShell 中单引号内的 JSON 不需要转义，但双引号内的需要
> - 推荐使用 `gh` CLI 替代 curl，语法更简洁且跨平台

### 列出 Issue

```bash
# Linux / macOS
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/issues?state=open&per_page=100"
```

```powershell
# Windows PowerShell
curl -s -H "Authorization: token $env:GITHUB_TOKEN" `
  -H "Accept: application/vnd.github+json" `
  "https://api.github.com/repos/<owner>/<repo>/issues?state=open&per_page=100"
```

### 获取 Issue 详情

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/<owner>/<repo>/issues/<number>"
```

### 添加 Issue 评论

```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/issues/<number>/comments" \
  -d '{"body":"评论内容"}'
```

### 更新 Issue（添加标签）

```bash
curl -s -X PATCH -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/issues/<number>" \
  -d '{"labels":["type:bug","priority:P1"]}'
```

### 列出 PR

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/<owner>/<repo>/pulls?state=open"
```

### 获取 PR 改动文件

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/<owner>/<repo>/pulls/<number>/files"
```

### 提交 PR 审查

```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/pulls/<number>/reviews" \
  -d '{"body":"审查意见","event":"COMMENT"}'
```

> `event` 可选值：`APPROVE`（批准）、`REQUEST_CHANGES`（需要修改）、`COMMENT`（仅评论）

### 列出标签

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/<owner>/<repo>/labels"
```

### 创建标签

```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/labels" \
  -d '{"name":"type:bug","color":"d73a4a","description":"Confirmed bug"}'
```

### 搜索 Issue

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/issues?q=repo:<owner>/<repo>+is:issue+is:open+关键词"
```

### API 速率限制

- 已认证请求：5000 次/小时
- 未认证请求：60 次/小时
- 如遇到 `403 rate limit exceeded`，等待重置或减少操作频率
- `actions/stale` 的 `operations-per-run` 参数可限制每次运行处理数量
- 可通过 `GET /rate_limit` 接口查看当前剩余配额

---

## 常见问题

| 问题 | 解决 |
|------|------|
| token 生成后找不到 | 确保在 "Tokens (classic)" 页面生成 Classic PAT，在 "Fine-grained tokens" 页面生成 Fine-grained PAT |
| 403 Forbidden | Classic PAT 的 scope 不够（重新勾选 `repo`）；Fine-grained PAT 权限不足（检查 Issues/PR 权限是否为 Read and write） |
| 401 Bad credentials | token 过期或被撤销，重新生成 |
| Docker 拉取镜像失败 | 执行 `docker logout ghcr.io` 后重试，或检查 Docker 是否运行 |
| MCP 工具列表为空 | MCP Server 未启动，检查 Docker 是否运行、配置文件 JSON 是否正确 |
| MCP Server 启动后立即退出 | 检查 token 是否有效，Docker 日志中通常有错误信息 |
| API 返回空结果 | 确认仓库是公开仓库，或 token 有访问私有仓库的权限 |
| PAT 被自动删除了 | GitHub 会清理一年未使用的 Classic PAT；Fine-grained PAT 到期后自动失效 |
| Fine-grained PAT 无法操作 | 确认 Repository access 中已勾选目标仓库，且权限级别足够 |

### 安全提醒

- PAT 等同密码，不要分享给任何人
- 不要提交到公开仓库（建议在 `.gitignore` 中添加 `.env`）
- 建议设置过期时间，定期轮换（Fine-grained PAT 强制设过期时间）
- GitHub 会自动删除一年未使用的 Classic PAT
- 优先使用 Fine-grained PAT，将权限限制在特定仓库
- 如怀疑 token 泄露，立即在 GitHub Settings → Tokens 中撤销
