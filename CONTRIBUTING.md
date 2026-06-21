# Contributing to GitHub OSS Ops

感谢你的关注！本项目是一个 AI Agent Skill，贡献方式略有不同。

## 如何贡献

### 报告问题

1. 在 [Issues](https://github.com/hyt315/github-oss-ops/issues) 中提交，选择合适的模板
2. 描述期望行为、实际行为、复现步骤
3. 如果是功能建议，说明使用场景

### 贡献代码 / 文档

1. **Fork** 本仓库
2. **创建分支**：`git checkout -b feature/你的功能名`
3. **提交改动**：使用 Conventional Commits 格式（`feat:` / `fix:` / `docs:` 等）
4. **推送分支**：`git push origin feature/你的功能名`
5. **提交 Pull Request**：填写 PR 模板，说明改动内容和原因

### 贡献 Skill 逻辑

Skill 的核心逻辑在 `SKILL.md` 中。修改时请注意：

- 用中文撰写主体内容，保持清晰简洁
- 新增触发词添加到 frontmatter 的 `description` 中
- 修改后不引入敏感信息（API Key、真实路径等）

### 行为准则

请遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
