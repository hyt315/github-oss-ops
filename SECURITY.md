# Security Policy

## Reporting a vulnerability

Report vulnerabilities through [GitHub Private Vulnerability Reporting](https://github.com/hyt315/github-oss-ops/security/advisories/new).

Do not open a public Issue containing exploit details, credentials, private repository data or personal information. If Private Vulnerability Reporting is unavailable, open a public Issue that only asks the maintainer to enable a private channel; do not include sensitive details.

## Credential safety

GitHub OSS Ops must never:

- ask a user to paste a PAT, API key or password into chat;
- search a home directory, editor configuration, MCP configuration or shell history for credentials;
- print, log, commit or persist credentials in the skill directory;
- place credentials in a Git remote URL;
- request broader GitHub permissions than the approved operation requires.

If a credential appears in chat, logs or a commit, stop the affected write operation, advise immediate revocation/rotation and verify the repository history before release.

## Supported versions

Only the latest published release is actively supported.
