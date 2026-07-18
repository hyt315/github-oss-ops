# GitHub access guide

This guide defines how GitHub OSS Ops selects an access path without collecting credentials.

## Decision order

### 1. Public read-only work

Public repository metadata, files, Issues, PRs, releases and Actions status can usually be read without authentication. Complete all useful read-only analysis first. Authentication failure must not block an offline draft or manual handoff.

### 2. Official GitHub connection or remote MCP

Prefer a platform-provided GitHub connector or the [official GitHub MCP Server](https://github.com/github/github-mcp-server). The hosted remote server supports OAuth in compatible hosts and avoids manually handling a PAT.

Do not assume fixed tool names. Inspect the capabilities exposed by the current host, then map the operation by purpose:

| Purpose | Typical capability |
| --- | --- |
| Repository files and metadata | repository/file read |
| Issue list, details and comments | issue read/list |
| Issue labels, state and comments | issue write/comment |
| PR diff, checks, reviews and merge | pull-request read/write/review |
| Workflow runs and logs | Actions list/get |
| Tags and releases | release/tag API, GitHub CLI or REST fallback |

The official MCP Server supports toolsets and individual-tool allow-lists. Enable only the groups needed for the task; read-only mode is appropriate for audits.

### 3. GitHub CLI

Check authentication without exposing credentials:

```bash
gh auth status
```

If authentication is missing, the user should complete the browser flow in a trusted terminal:

```bash
gh auth login --web
```

Useful commands:

```bash
gh issue list --repo OWNER/REPO --state open
gh pr checks 42 --repo OWNER/REPO
gh pr view 42 --repo OWNER/REPO --json files,reviews,statusCheckRollup
gh release list --repo OWNER/REPO
```

### 4. Fine-grained PAT

Use a PAT only when the user explicitly chooses it and no safer authorized connection is available.

- Prefer a fine-grained PAT over a classic PAT.
- Limit repository access to the target repository.
- Grant read-only permissions for audits.
- Add write permissions only for the approved operation.
- Set an expiration date and rotate on suspected exposure.
- Let a trusted password prompt, credential manager or environment manager receive it.

Never ask the user to paste it into chat. Never inspect configuration files to extract it. Never print it to confirm that it exists.

## Minimum-permission examples

| Operation | Repository permission |
| --- | --- |
| Read public Issues and PRs | none for public data; otherwise Issues/PR read |
| Comment or label an Issue | Issues read/write |
| Review or merge a PR | Pull requests read/write; Contents write may also be required |
| Read workflow results | Actions read |
| Create a Release | Contents write |
| Change repository settings | Administration write |

Permission names and availability can vary by token type and repository ownership. Verify against GitHub's current authorization screen rather than copying a broad scope list.

## REST fallback

Use the current `Bearer` authorization form when an already-provisioned environment variable is available through a trusted runtime:

```bash
curl --fail-with-body \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO
```

Do not run commands that echo the variable. Do not embed credentials in the URL. Redact request headers from debugging logs.

## Approval boundary

Read-only calls can proceed when they are within the repository the user placed in scope. Before a write, show:

1. repository and exact target;
2. proposed content or state change;
3. whether it is reversible;
4. expected follow-up, such as CI or notification effects.

Approval for one comment does not authorize closing an Issue, merging a PR, publishing a Release or changing repository settings.

## Failure handling

| Failure | Response |
| --- | --- |
| Public API rate limit | Continue with cloned files/local Git data; report freshness limits |
| Authentication missing | Finish read-only/offline work; request trusted authorization only for the blocked write |
| 401 | Do not retry repeatedly; verify auth state and rotate only if the credential is invalid |
| 403 | Check repository selection and minimum permission for the exact operation |
| 404 on a private repository | Treat as possible permission failure without revealing repository existence |
| Connector or MCP unavailable | Use `gh`, public API or manual handoff; do not install an unofficial abandoned server |
| Credential exposed | Stop, revoke/rotate, scan Git history and remove the value before continuing |

## Authoritative references

- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [Managing personal access tokens](https://docs.github.com/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Permissions required for fine-grained PATs](https://docs.github.com/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens)
- [GitHub CLI authentication](https://cli.github.com/manual/gh_auth_login)
