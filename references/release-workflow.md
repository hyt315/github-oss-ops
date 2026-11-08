# 版本管理与发布流程

> 适用任务：判断版本号、写 Changelog 与 Release Notes、起草发版宣传文案。Tag、Release 与对外发布各自单独确认。

---

## 目录

- [Semver 语义化版本](#semver-语义化版本)
- [版本文件模板](#版本文件模板)
- [Changelog 规范](#changelog-规范)
- [GitHub Release 创建流程](#github-release-创建流程)
- [Conventional Commits 集成](#conventional-commits-集成)
- [版本号同步检查](#版本号同步检查)
- [常见问题](#常见问题)
- [版本更新方案示例](#版本更新方案示例)
- [发版宣传文案模板](#发版宣传文案模板)

---

## Semver 语义化版本

格式：`MAJOR.MINOR.PATCH`（如 `1.2.3`）

| 版本段 | 何时递增 | 含义 |
|--------|---------|------|
| MAJOR | 不兼容的 API 变更 | 用户需要修改代码才能升级 |
| MINOR | 向后兼容的功能新增 | 用户可直接升级使用新功能 |
| PATCH | 向后兼容的 Bug 修复 | 用户应尽快升级修复问题 |

### 判断规则

```
PR 合并后，检查改动类型：

是否有破坏性变更？
├── 是 → MAJOR（x.0.0）
│       如：删除公开 API、修改函数签名、更改数据格式
│
└── 否 → 是否有新功能？
         ├── 是 → MINOR（x.y.0）
         │       如：新增函数、新增配置选项、新增命令
         │
         └── 否 → PATCH（x.y.z）
                  如：修复 Bug、优化性能、更新文档
```

### 特殊情况

| 场景 | 版本段 | 说明 |
|------|--------|------|
| v0.x.x（初始开发阶段） | 任意段都可变 | v0 阶段 API 不稳定，MINOR 递增也可能有破坏性变更 |
| 同时合并多个 PR | 取最高段 | 一个 patch + 一个 minor → minor |
| 仅文档更新 | patch | 不改代码但用户需要知道有更新 |
| 安全修复 | patch 或 minor | 取决于是否新增 API |
| 依赖升级（Dependabot） | patch（通常） | 除非依赖有 breaking change |

---

## 版本文件模板

### Node.js / npm

文件：`package.json`

```json
{
  "name": "my-package",
  "version": "1.2.3",
  ...
}
```

更新方式：修改 `version` 字段值。

如有 `package-lock.json`，同步更新其 `version` 和 `packages[""].version`。

### Python

方式一：`pyproject.toml`

```toml
[project]
name = "my-package"
version = "1.2.3"
```

方式二：`__init__.py`

```python
__version__ = "1.2.3"
```

方式三：`setup.py`（旧项目）

```python
setup(
    name="my-package",
    version="1.2.3",
    ...
)
```

> 优先检查 `pyproject.toml`，如不存在再检查 `setup.py` 或 `__init__.py`。

### Rust

文件：`Cargo.toml`

```toml
[package]
name = "my-crate"
version = "1.2.3"
```

更新后 `Cargo.lock` 会在下次 `cargo build` 时自动更新。

### Java / Maven

文件：`pom.xml`

```xml
<project>
  <groupId>com.example</groupId>
  <artifactId>my-app</artifactId>
  <version>1.2.3</version>
</project>
```

### Java / Gradle

文件：`build.gradle` 或 `build.gradle.kts`

```groovy
version = '1.2.3'
```

### Go

Go 项目不使用版本文件，通过 git tag 管理版本：

```bash
git tag v1.2.3
git push origin v1.2.3
```

> **v2 及以上的大版本**：模块路径必须带 `/vN` 后缀（如 `module github.com/owner/repo/v2`，并同步改所有导入路径），否则 `v2.0.0` 标签不会被 Go 工具链当作该模块的版本。

### 通用（无版本文件）

如果项目没有版本文件，仅通过 git tag 管理：

1. 创建带注释的 tag：`git tag -a v1.2.3 -m "Release v1.2.3"`
2. 推送 tag：`git push origin v1.2.3`
3. 基于 tag 创建 GitHub Release

---

## Changelog 规范

### 格式（Keep a Changelog）

```markdown
# Changelog

## [1.3.0] - 2026-06-20

### Added
- 新增数据导出功能 (#45) by @contributor
- 支持自定义主题颜色 (#48) by @another-user

### Fixed
- 修复登录超时问题 (#42) by @bug-reporter
- 修复移动端布局错位 (#43)

### Changed
- 升级依赖 react 18 → 19 (#50)

### Removed
- 移除已弃用的 `legacyExport` API (#51)
```

### 分类规则

| 类别 | 对应内容 |
|------|---------|
| **Added** | 新增功能（`type:enhancement`） |
| **Fixed** | Bug 修复（`type:bug`） |
| **Changed** | 行为变更（不一定是 breaking） |
| **Deprecated** | 标记弃用（尚未删除） |
| **Removed** | 删除功能（按 SemVer，删除公开 API 属于破坏性变更，需升 MAJOR） |
| **Security** | 安全修复（`type:security`） |

### 生成 Changelog 的数据来源

1. 获取上一个 tag 到当前 HEAD 之间的所有已合并 PR
2. 按 PR 标签分类到对应类别
3. 提取 PR 标题作为 changelog 条目
4. 附上 PR 编号和贡献者用户名

优先用 GitHub 查已合并 PR（`git log --merges` 会漏掉 Squash 和 Rebase 合并）：

```bash
# 上一个 tag 的日期之后合并到默认分支的 PR
gh pr list --state merged --base main --search "merged:>=2026-06-01" \
  --json number,title,labels,author,mergedAt --limit 200
```

或让 GitHub 直接生成分类草稿（只读，不创建 Release）：

```bash
gh api repos/{owner}/{repo}/releases/generate-notes \
  -f tag_name=v1.3.0 -f previous_tag_name=v1.2.3
```

---

## GitHub Release 创建流程

### 方式一：通过 GitHub API

```bash
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{owner}/{repo}/releases \
  -d '{
    "tag_name": "v1.3.0",
    "target_commitish": "main",
    "name": "v1.3.0",
    "body": "### Added\n- 新增导出功能 (#45)\n\n### Fixed\n- 修复登录超时 (#42)",
    "draft": false,
    "prerelease": false
  }'
```

### 方式二：通过 MCP 工具

先检查当前 GitHub 连接或 MCP 是否暴露 Release/Tag 写入能力。工具能力会更新，不要把某个工具名或缺失状态写死；没有相应能力时，使用已认证的 `gh` CLI 或 REST API：

```bash
gh release create v1.3.0 --title "v1.3.0" --notes "### Added..." --target main
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `tag_name` | 版本号标签（如 `v1.3.0`） |
| `target_commitish` | 打 tag 的分支（通常是 `main`） |
| `name` | Release 标题（通常与 tag 相同） |
| `body` | Release 正文（即 changelog） |
| `draft` | `true` = 草稿（用户可手动发布），`false` = 立即发布 |
| `prerelease` | `true` = 预发布版本（如 alpha/beta/rc） |

### 预发布版本

| 阶段 | 标签格式 | 示例 |
|------|---------|------|
| Alpha | `v1.3.0-alpha.1` | 内部测试，功能不完整 |
| Beta | `v1.3.0-beta.1` | 功能完整，可能有 Bug |
| RC | `v1.3.0-rc.1` | 候选发布，无已知问题即转正 |

预发布版本的 Release 应设置 `prerelease: true`。

---

## Conventional Commits 集成

如果项目使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范，可以自动从提交信息推导版本段：

| 提交 | semver 版本段 | 示例 |
|----------|--------------|------|
| `feat:` | MINOR | `feat: add export feature` |
| `fix:` | PATCH | `fix: login timeout` |
| 类型后加 `!`，或正文末尾有 `BREAKING CHANGE:` 脚注 | MAJOR | `feat!: redesign config format` |
| 其他类型（`docs:`、`refactor:`、`perf:`、`chore:` 等） | 规范未规定，由项目自定 | 常见做法：单独出现时不发版，或并入下一个 PATCH |

### 自动推导流程

1. 获取上一个 tag 之后的所有 commit
2. 解析 commit message 前缀
3. 如果有 `!` 或 `BREAKING CHANGE:` 脚注 → MAJOR（`0.x` 阶段按项目约定，通常升 MINOR）
4. 否则如果有 `feat:` → MINOR
5. 否则如果有 `fix:` → PATCH
6. 只有其他类型 → 按项目约定，并向用户说明

---

## 版本号同步检查

版本号必须在所有位置保持一致。发版前逐项检查：

| # | 位置 | 检查内容 | 易漏点 |
|---|------|----------|--------|
| 1 | 版本文件 | `package.json` / `pyproject.toml` / `Cargo.toml` 等 | 有些项目在多处声明版本（如 `package.json` + `package-lock.json`） |
| 2 | README 徽章 | shields.io 版本徽章 URL 中的版本号 | 徽章是静态 URL，不会自动更新 |
| 3 | 其他元数据文件 | `SKILL.md` frontmatter、`setup.py` 等 | Skill 项目的 `version` 字段 |
| 4 | Git tag | `git tag -a v1.x.x` | tag 只是指针，不等于 Release |
| 5 | GitHub Release | 基于 tag 创建带 changelog 的发布页 | 必须手动创建，tag 不会自动生成 Release |

### 发版前 Checklist

```
- [ ] 版本文件已更新
- [ ] README 徽章已更新
- [ ] 其他元数据文件已更新
- [ ] Git tag 已创建并推送
- [ ] GitHub Release 已创建（附 changelog）
- [ ] 各处版本号一致（交叉检查）
```

> **常见坑**：README 里的 shields.io 徽章是最容易忘记更新的。建议把徽章 URL 的版本号写为动态参数（如读取 `package.json`），或者在发版 checklist 里明确列出。

---

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 找不到版本文件 | 项目用纯 git tag 管理 | 跳过版本文件更新，直接打 tag + 创建 Release |
| 版本号冲突 | tag 已存在 | 检查现有 tag（`git tag -l`），递增版本号 |
| 不知道当前版本 | 没有 tag 也没有版本文件 | 从 `v0.1.0` 或 `v1.0.0` 开始 |
| 多个版本文件 | 项目同时在多处声明版本 | 全部更新，保持一致 |
| PR 没有标签 | 无法自动判断改动类型 | 读取 PR 的改动文件，分析是否涉及公开 API 变更 |
| Release 创建失败 | Token 缺少 `contents: write` 权限 | 检查 PAT 权限或 Fine-grained PAT 的仓库权限设置 |

---

## 版本更新方案示例

```text
### 版本更新建议

- 当前版本：v1.2.3
- 合并的 PR：
  - #42 fix: 修复登录超时问题（patch）
  - #45 feat: 新增导出功能（minor）
- 建议新版本：v1.3.0（取最高版本段）
- 版本文件：`package.json`

### Changelog 草稿（Keep a Changelog 格式）

## [Unreleased]

## [1.3.0] - 2026-06-20

### Added
- 新增导出功能 (#45) by @contributor

### Fixed
- 修复登录超时问题 (#42) by @contributor
```

## 发版宣传文案模板

发版完成后可起草以下文案。**对外发布属于公开写操作，必须由用户确认后由用户本人或经授权发出。**

### 1. X（Twitter）短帖模板

> 普通账号单帖上限 280 字符，链接按 23 字符计；Premium 账号可更长。
```text
🚀 {project_name} {version} is officially released!

Key Highlights:
✨ {feature_1}
🐛 {fix_1}
⚡ {perf_1}

Special thanks to all our amazing contributors! 🙌
📦 Full Release Notes & Download: {release_url}

#OpenSource #GitHub #{tag}
```

### 2. Reddit 发布帖模板

> 发到 Hacker News 时标题用 `Show HN: {project_name} – {one_sentence_pitch}`，正文去掉称呼，简短说明做了什么、为什么做。各子版块对自我推广有不同规定，先看版规。
```text
Title: {project_name} {version} released - {one_sentence_pitch}

Hey r/opensource,

We just shipped {version} of {project_name}! In this release, we focused heavily on {main_theme}.

What's New:
- {feature_1_details}
- {feature_2_details}
- {breaking_change_or_perf_details}

Try it out:
`{install_command}`

GitHub Repo: {repo_url}
Full Changelog: {release_url}

Feedback and contributions are warmly welcome!
```

### 3. V2EX／掘金／微信公众号文案模板

> V2EX 的项目推广只能发在“分享创造”节点。
```text
标题：【开源发布】{project_name} {version} 正式发布：{核心卖点一句话}

大家好，{project_name} 迎来了全新的 {version} 版本！本次更新带来了以下重点特性：

🌟 核心亮点：
1. 【新增】{feature_1}：{详细说明}；
2. 【优化】{feature_2}：{详细说明}；
3. 【修复】{fix_1}：{详细说明}。

🚀 快速开始：
{install_code_block}

🔗 链接直达：
- GitHub 仓库：{repo_url}
- 完整发版日志：{release_url}

欢迎各位开发者 Star ⭐ 体验与提出建议！
```
