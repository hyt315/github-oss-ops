# 版本管理与发布流程

> PR 合并后的版本更新、GitHub Release 创建和 Changelog 生成指南。SKILL.md Step 6 引用本文件。

---

## 目录

- [Semver 语义化版本](#semver-语义化版本)
- [版本文件模板](#版本文件模板)
- [Changelog 规范](#changelog-规范)
- [GitHub Release 创建流程](#github-release-创建流程)
- [Conventional Commits 集成](#conventional-commits-集成)
- [版本号同步检查](#版本号同步检查)
- [常见问题](#常见问题)

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
| **Removed** | 删除功能（breaking change） |
| **Security** | 安全修复（`type:security`） |

### 生成 Changelog 的数据来源

1. 获取上一个 tag 到当前 HEAD 之间的所有已合并 PR
2. 按 PR 标签分类到对应类别
3. 提取 PR 标题作为 changelog 条目
4. 附上 PR 编号和贡献者用户名

```bash
# 获取两个 tag 之间合并的 PR
git log v1.2.3..HEAD --merges --oneline
```

或通过 GitHub API：

```
GET /repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc
# 过滤 merged_at 在上一个 release 之后的 PR
```

---

## GitHub Release 创建流程

### 方式一：通过 GitHub API

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
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

目前 GitHub MCP Server 没有直接的 `create_release` 工具。使用 curl 回退方案或通过 `create_or_update_file` 先推送版本文件变更，再用 `gh` CLI 创建 Release：

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

| 提交前缀 | semver 版本段 | 示例 |
|----------|--------------|------|
| `feat:` | MINOR | `feat: add export feature` |
| `fix:` | PATCH | `fix: login timeout` |
| `docs:` | PATCH | `docs: update API reference` |
| `refactor:` | PATCH | `refactor: simplify auth flow` |
| `perf:` | PATCH | `perf: optimize query` |
| `feat!:` 或 `BREAKING CHANGE:` | MAJOR | `feat!: redesign config format` |

### 自动推导流程

1. 获取上一个 tag 之后的所有 commit
2. 解析 commit message 前缀
3. 如果存在 `BREAKING CHANGE` 或 `!:` → MAJOR
4. 否则如果存在 `feat:` → MINOR
5. 否则 → PATCH

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
