#!/usr/bin/env python3
"""validate.py - github-oss-ops 技能包自检（唯一校验入口）

只读、零依赖（Python 3.10+ 标准库）。检查的是本技能包自身，不访问网络、不读取目标仓库。

检查项：
  1. 必需文件在盘
  2. SKILL.md frontmatter（name / version / description）
  3. 版本号与日期一致：SKILL.md、manifest.json（version 与 updated_at）、CHANGELOG.md 最新条目、
     .github/repository-metadata.yml（release.tag 与 release.title）
  4. CHANGELOG 每个二级标题形如 `## [x.y.z] - YYYY-MM-DD`
  5. references/ 下每份手册都被 SKILL.md 引用（无孤儿）
  6. 所有 Markdown 本地链接可达，指向 .md 的 `#锚点` 必须对应真实标题
  7. references/ 不得写死 "SKILL.md Step N"（编号一改就失效）
  8. 中英文 README 安装路径齐全，“最新版本”标题的版本号和日期与 CHANGELOG 最新条目一致
  9. 文本文件中无凭据样式字符串、无危险凭据指引
 10. 全部 Python 文件可被 ast 解析

用法：
  python scripts/validate.py          # 人读输出，退出码 0=通过 1=失败
  python scripts/validate.py --json   # 机读输出
"""

from __future__ import annotations

import argparse
import ast
import json
import pathlib
import re
import sys
from urllib.parse import unquote

SKILL_NAME = "github-oss-ops"
ROOT = pathlib.Path(__file__).resolve().parent.parent

REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "README.en.md",
    "CHANGELOG.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CONTRIBUTORS.md",
    "manifest.json",
    "agents/openai.yaml",
    "examples/README.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/repository-metadata.yml",
)

README_FRAGMENTS = (
    f"~/.agents/skills/{SKILL_NAME}",
    f"~/.claude/skills/{SKILL_NAME}",
    f"~/.cursor/skills/{SKILL_NAME}",
    f"https://github.com/hyt315/{SKILL_NAME}/releases/latest",
    "examples/README.md",
)

TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".py", ".mjs", ".js", ".txt", ".svg"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

# 拼接写法，避免本文件自身命中规则
SECRET_PATTERNS = (
    re.compile("gh" + r"p_[A-Za-z0-9]{20,}"),
    re.compile("github" + r"_pat_[A-Za-z0-9_]{20,}"),
    re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile("AK" + r"IA[0-9A-Z]{16}"),
)
UNSAFE_PATTERNS = (
    re.compile(r"Get-ChildItem\s+-Path\s+\$HOME\s+-Recurse", re.I),
    re.compile(r"print\s*\(\s*token\s*\)", re.I),
    re.compile(r"echo\s+\$GITHUB_(?:TOKEN|PERSONAL_ACCESS_TOKEN)"),
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CHANGELOG_HEADING_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.M)
FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
# “最新版本”标题：{version} 与 {date} 由 CHANGELOG 最新条目填入
README_LATEST = {
    "README.md": "## 🆕 最新版本：v{version}（{date}）",
    "README.en.md": "## 🆕 Latest release: v{version} ({date})",
}
STEP_REF_RE = re.compile(r"SKILL\.md\s*Step\s*\d", re.I)


def _iter_files(root: pathlib.Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            yield path


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _anchors(text: str) -> set[str]:
    """按 GitHub 规则把 Markdown 标题转成锚点（小写、去标点、空格变连字符、重名加 -N）。"""
    found: set[str] = set()
    seen: dict[str, int] = {}
    for raw in HEADING_RE.findall(FENCE_RE.sub("", text)):
        title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
        title = re.sub(r"<[^>]+>", "", title).replace("`", "")
        slug = re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        found.add(slug if count == 0 else f"{slug}-{count}")
    return found


def _frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return fields


def validate(root: pathlib.Path = ROOT) -> dict:
    errors: list[str] = []
    checks = 0

    def check(ok: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not ok:
            errors.append(message)

    # 1. 必需文件
    for rel in REQUIRED_FILES:
        check((root / rel).is_file(), f"缺少必需文件: {rel}")
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return {"status": "FAIL", "checks": checks, "errors": errors}
    skill = _read(skill_path)

    # 2. frontmatter
    fm = _frontmatter(skill)
    check(bool(fm), "SKILL.md 缺少 YAML frontmatter")
    check(fm.get("name") == SKILL_NAME, f"SKILL.md name 应为 {SKILL_NAME}，实际为 {fm.get('name')!r}")
    check(bool(fm.get("description")), "SKILL.md 缺少 description")
    version = fm.get("version", "")
    check(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), f"SKILL.md version 不是 x.y.z: {version!r}")

    # 3. 版本一致
    manifest: dict = {}
    try:
        manifest = json.loads(_read(root / "manifest.json"))
        check(manifest.get("version") == version,
              f"manifest.json 版本 {manifest.get('version')!r} 与 SKILL.md {version!r} 不一致")
        check(manifest.get("name") == SKILL_NAME, "manifest.json name 不一致")
    except (OSError, json.JSONDecodeError) as exc:
        check(False, f"manifest.json 无法解析: {exc}")

    release_date = ""
    changelog_path = root / "CHANGELOG.md"
    if changelog_path.is_file():
        headings = [line for line in _read(changelog_path).splitlines() if line.startswith("## ")]
        # 4. 标题格式
        for line in headings:
            check(bool(CHANGELOG_HEADING_RE.match(line)), f"CHANGELOG 标题格式不对: {line!r}")
        newest = CHANGELOG_HEADING_RE.match(headings[0]) if headings else None
        check(bool(newest) and newest.group(1) == version,
              f"CHANGELOG 最新条目应为 [{version}]")
        if newest:
            release_date = newest.group(2)
            check(manifest.get("updated_at") == release_date,
                  f"manifest.json updated_at {manifest.get('updated_at')!r} 与 CHANGELOG 最新条目日期 {release_date} 不一致")

    metadata_path = root / ".github/repository-metadata.yml"
    if metadata_path.is_file():
        metadata = _read(metadata_path)
        ver = re.escape(version)
        check(bool(re.search(rf"^\s*tag:\s*v{ver}\s*$", metadata, re.M)),
              f"repository-metadata.yml 的 release tag 应为 v{version}")
        check(bool(re.search(rf"^\s*title:.*\bv{ver}\s*$", metadata, re.M)),
              f"repository-metadata.yml 的 release title 应以 v{version} 结尾")

    # 5. 无孤儿手册
    cited = set(re.findall(r"references/([\w\-]+\.md)", skill))
    for ref in sorted((root / "references").glob("*.md")):
        check(ref.name in cited, f"SKILL.md 未引用 references/{ref.name}")

    for path in _iter_files(root):
        rel = path.relative_to(root).as_posix()
        if path.suffix not in TEXT_SUFFIXES:
            continue
        text = _read(path)

        # 6. 本地链接
        if path.suffix == ".md":
            for target in LINK_RE.findall(text):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                local, _, fragment = target.partition("#")
                dest = path.parent / unquote(local) if local else path
                if local:
                    check(dest.exists(), f"{rel}: 本地链接失效 {target}")
                if fragment and dest.suffix == ".md" and dest.is_file():
                    check(unquote(fragment).lower() in _anchors(_read(dest)),
                          f"{rel}: 锚点不存在 {target}")

        # 7. 写死步骤编号
        if rel.startswith("references/"):
            check(not STEP_REF_RE.search(text), f"{rel}: 不要写死 'SKILL.md Step N'，改写为适用任务")

        # 9. 凭据与危险指引
        for pattern in SECRET_PATTERNS:
            check(not pattern.search(text), f"{rel}: 疑似凭据字符串")
        for pattern in UNSAFE_PATTERNS:
            check(not pattern.search(text), f"{rel}: 不安全的凭据指引")

        # 10. Python 语法
        if path.suffix == ".py":
            try:
                ast.parse(text, filename=rel)
                check(True, "")
            except SyntaxError as exc:
                check(False, f"{rel}: 第 {exc.lineno} 行语法错误 {exc.msg}")

    # 8. README 安装路径与“最新版本”标题
    for name, latest in README_LATEST.items():
        path = root / name
        if not path.is_file():
            continue
        readme = _read(path)
        for fragment in README_FRAGMENTS:
            check(fragment in readme, f"{name} 缺少 {fragment}")
        if version:
            expected = latest.format(version=version, date=release_date)
            check(expected in readme.splitlines(), f"{name} 未写明当前版本，应有标题行：{expected}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "skill": SKILL_NAME,
        "version": version,
        "checks": checks,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="github-oss-ops 技能包自检（只读）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--root", type=pathlib.Path, default=ROOT, help="技能包根目录")
    args = parser.parse_args(argv)

    report = validate(args.root.resolve())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{SKILL_NAME} v{report.get('version', '?')}: {report['status']}（{report['checks']} 项检查）")
        for err in report["errors"]:
            print(f"  - {err}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
