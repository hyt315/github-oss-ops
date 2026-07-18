import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const expectedName = 'github-oss-ops';
const expectedVersion = '1.1.0';
const required = [
  'SKILL.md', 'README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md',
  'CODE_OF_CONDUCT.md', 'SECURITY.md', 'CONTRIBUTORS.md',
  '.github/pull_request_template.md', '.github/ISSUE_TEMPLATE/config.yml',
  '.github/repository-metadata.yml', 'agents/openai.yaml', 'examples/README.md',
];

const fail = (message) => {
  console.error(`Validation failed: ${message}`);
  process.exitCode = 1;
};

for (const relative of required) {
  if (!fs.existsSync(path.join(root, relative))) fail(`missing ${relative}`);
}

const skill = fs.readFileSync(path.join(root, 'SKILL.md'), 'utf8');
const readme = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
const changelog = fs.readFileSync(path.join(root, 'CHANGELOG.md'), 'utf8');
const metadata = fs.readFileSync(path.join(root, '.github/repository-metadata.yml'), 'utf8');

if (!skill.startsWith('---\n')) fail('SKILL.md must start with YAML frontmatter');
if (!skill.includes(`name: ${expectedName}`)) fail('SKILL.md name mismatch');
if (!skill.includes(`version: ${expectedVersion}`)) fail('SKILL.md version mismatch');
if (!/^description:\s*.+/m.test(skill)) fail('SKILL.md description is missing');
if (!changelog.includes(`## [${expectedVersion}]`)) fail('CHANGELOG version mismatch');
if (!metadata.includes(`tag: v${expectedVersion}`)) fail('repository release metadata mismatch');

for (const fragment of [
  `~/.agents/skills/${expectedName}`,
  `~/.claude/skills/${expectedName}`,
  `~/.cursor/skills/${expectedName}`,
  'https://github.com/hyt315/github-oss-ops/releases/latest',
  'examples/README.md',
]) {
  if (!readme.includes(fragment)) fail(`README missing ${fragment}`);
}

const ignored = new Set(['.git']);
const files = [];
const walk = (directory) => {
  for (const entry of fs.readdirSync(directory, {withFileTypes: true})) {
    if (ignored.has(entry.name)) continue;
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(absolute);
    else files.push(absolute);
  }
};
walk(root);

const textExtensions = new Set(['.md', '.yml', '.yaml', '.json', '.mjs', '.js', '.txt']);
const secretPatterns = [
  /ghp_[A-Za-z0-9]{20,}/,
  /github_pat_[A-Za-z0-9_]{20,}/,
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /AKIA[0-9A-Z]{16}/,
];
const bannedSafetyPatterns = [
  /~\/\.codex\/skills\/github-oss-ops/,
  /Get-ChildItem\s+-Path\s+\$HOME\s+-Recurse/i,
  /print\s*\(\s*token\s*\)/i,
  /echo\s+\$GITHUB_(?:TOKEN|PERSONAL_ACCESS_TOKEN)/,
];

for (const file of files) {
  if (!textExtensions.has(path.extname(file))) continue;
  const text = fs.readFileSync(file, 'utf8');
  for (const pattern of secretPatterns) {
    if (pattern.test(text)) fail(`credential-like value in ${path.relative(root, file)}`);
  }
  for (const pattern of bannedSafetyPatterns) {
    if (pattern.test(text)) fail(`unsafe credential or install guidance in ${path.relative(root, file)}`);
  }

  if (path.extname(file) === '.md') {
    for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
      const target = match[1].trim().split(/\s+/)[0];
      if (/^(?:https?:|mailto:|#)/.test(target)) continue;
      const local = decodeURIComponent(target.split('#')[0]);
      if (!local) continue;
      if (!fs.existsSync(path.resolve(path.dirname(file), local))) {
        fail(`broken local link ${target} in ${path.relative(root, file)}`);
      }
    }
  }
}

if (!process.exitCode) console.log(`${expectedName} v${expectedVersion} validation passed`);
