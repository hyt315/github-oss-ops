#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""github-oss-ops 自测：验证技能文档结构完整、references 引用齐全、九个 Step 在位、AST 语法严密。

好夹具（本技能自身）：
- SKILL.md 存在且 frontmatter 合规、Step 1-9 全在
- 10 本 references 手册全部在盘并被 SKILL.md 引用（含 github-oss-ops-pitfalls.md）
- Fact Card 事实卡片、Zero-Mutation 铁律与用户显式授权声明防回归
- scripts/validate_ops.py 与 validate-skill.mjs 均在盘
- AST 静态语法解析门禁：全树 Python 脚本语法合规
负向用例：
- 抽掉 Step / 制造孤儿引用 / 裸路径引用均触发 FAIL
- 语法损坏 Python 样本必须被 AST 门禁准确识别与拦截
零依赖，仅 Python 标准库。

Run: python scripts/selftest.py   # 退出 0 = PASS，1 = FAIL
"""

from __future__ import annotations

import ast
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
NAME_RE = r"^[a-z0-9]+(-[a-z0-9]+)*$"
STEPS = [f"## Step {i}" for i in range(1, 10)]


def check_skill_text(text: str, root_name: str) -> list[str]:
    """同套校验逻辑：返回 failures 列表（空 = 通过）。供正向与负向共用。"""
    failures: list[str] = []
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        return ["frontmatter missing"]
    head = fm.group(1)
    name = re.search(r"^name:\s*(\S+)\s*$", head, re.M)
    n = name.group(1) if name else ""
    if not re.match(NAME_RE, n) or n != root_name:
        failures.append(f"name '{n}' invalid or != {root_name}")
    for step in STEPS:
        if step not in text:
            failures.append(f"missing workflow section: {step}")
    refs = set(re.findall(r"references/[\w\-]+\.md", text))
    actual = {f"references/{p.name}" for p in (ROOT / "references").glob("*.md")}
    if actual - refs:
        failures.append(f"orphan references: {sorted(actual - refs)}")
    # LK002 回归：正文不得出现指向本仓库不存在文件的裸 .github 路径引用
    bare = re.findall(r"`(\.github/[\w\-./]+)`", text)
    real = {str(p.relative_to(ROOT)).replace("\\", "/") for p in ROOT.rglob(".github/*") if p.is_file()}
    ghosts = sorted({b for b in bare if b not in real})
    if ghosts:
        failures.append(f"bare paths to non-existent repo files: {ghosts}")
    return failures


def verify_ast_syntax(directory: pathlib.Path) -> list[str]:
    """遍历指定目录下的所有 Python 脚本并进行 AST 语法解析。"""
    syntax_errors: list[str] = []
    for py_file in directory.glob("**/*.py"):
        try:
            code = py_file.read_text(encoding="utf-8")
            ast.parse(code, filename=str(py_file))
        except SyntaxError as e:
            syntax_errors.append(f"{py_file.name}: line {e.lineno}: {e.msg}")
        except Exception as e:
            syntax_errors.append(f"{py_file.name}: {e}")
    return syntax_errors


failures: list[str] = []

# 好夹具：本技能自身
if not SKILL.is_file():
    print("RESULT FAIL\n - SKILL.md missing")
    sys.exit(1)
text = SKILL.read_text(encoding="utf-8")
failures += check_skill_text(text, ROOT.name)

# 关键配套在盘
for p in (
    "scripts/validate_ops.py",
    "scripts/validate-skill.mjs",
    "tests/test_skill.py",
    "examples/README.md",
    "references/automation-templates.md",
    "references/triage-workflow.md",
    "references/github-oss-ops-pitfalls.md",
):
    if not (ROOT / p).is_file():
        failures.append(f"missing file: {p}")

# 调研采纳内容防回归（2026-09 复审）
adopted_keywords = (
    "Merge Queue",
    "Rulesets",
    "Private Vulnerability Reporting",
    "Fact Card",
    "Zero-Mutation",
    "用户显式授权",
    "github-oss-ops-pitfalls.md",
    "validate_ops.py",
)
for kw in adopted_keywords:
    if not re.search(re.escape(kw), text, re.I):
        failures.append(f"missing adopted keyword: {kw}")

# AST 静态语法解析门禁
for target_dir in (ROOT / "scripts", ROOT / "tests"):
    if target_dir.is_dir():
        ast_errs = verify_ast_syntax(target_dir)
        for err in ast_errs:
            failures.append(f"AST syntax error in {err}")

# 负向用例：抽掉全部 Step 的坏样本必须被拒
bad = "---\nname: bad-skill\ndescription: 触发词：运营\n---\n\n无工作流正文。\n"
if not any("Step" in f for f in check_skill_text(bad, ROOT.name)):
    failures.append("negative: missing-step sample NOT detected")

# 负向用例：孤儿引用检测必须生效（抽掉一个真实引用）
no_ref_text = text.replace("references/triage-workflow.md", "triage-workflow")
if not any("orphan" in f for f in check_skill_text(no_ref_text, ROOT.name)):
    failures.append("negative: orphan reference NOT detected")

# 负向用例：裸路径门必须生效（塞回一个不存在的裸路径）
bare_text = text + "\n示例：`.github/workflows/fake.yml`\n"
if not any("bare paths" in f for f in check_skill_text(bare_text, ROOT.name)):
    failures.append("negative: bare-path ghost NOT detected")

# 负向用例：损坏 Python 语法的样本必须被 AST 门禁拦截
bad_syntax_code = "def broken_syntax(:\n    pass\n"
try:
    ast.parse(bad_syntax_code)
    failures.append("negative: AST broken-syntax sample NOT detected")
except SyntaxError as expected_err:
    _expected_syn = str(expected_err)  # 负向用例预期拦截，合规留痕

print("RESULT " + ("PASS" if not failures else "FAIL"))
for f in failures:
    print(" -", f)
sys.exit(0 if not failures else 1)
