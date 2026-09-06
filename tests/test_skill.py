#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_skill.py - GitHub OSS Ops 技能核心功能与规范自动化测试套件

涵盖：
1. SKILL.md 结构、frontmatter 与工作流 Step 完整性
2. references 目录 10 本参考手册引用与在盘一致性
3. scripts 目录全量 Python 脚本 AST 静态语法解析门禁
4. validate_ops 验证工具在 full / quick / json 模式下的合规断言
5. 零凭据采集与 Zero-Mutation 只读安全铁律防线
"""

from __future__ import annotations

import ast
import json
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_ops


class TestGitHubOssOpsSkill(unittest.TestCase):
    """GitHub OSS Ops 核心规范与自测套件。"""

    def setUp(self) -> None:
        self.root = ROOT
        self.skill_file = self.root / "SKILL.md"
        self.manifest_file = self.root / "manifest.json"
        self.ref_dir = self.root / "references"
        self.scripts_dir = self.root / "scripts"

    def test_skill_frontmatter_and_steps(self) -> None:
        """验证 SKILL.md 存在且 frontmatter、版本、Step 1-9 齐全。"""
        self.assertTrue(self.skill_file.is_file(), "SKILL.md must exist")
        text = self.skill_file.read_text(encoding="utf-8")

        # Frontmatter
        self.assertTrue(text.startswith("---\n") or text.startswith("---\r\n"))
        fm_match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(fm_match)
        fm_text = fm_match.group(1)
        self.assertIn("name: github-oss-ops", fm_text)

        # Manifest 版本一致性
        manifest = json.loads(self.manifest_file.read_text(encoding="utf-8"))
        self.assertIn(f"version: {manifest['version']}", fm_text)

        # Steps 1 to 9
        for i in range(1, 10):
            self.assertIn(f"## Step {i}", text, f"Missing Step {i} in SKILL.md")

    def test_references_and_pitfalls_complete(self) -> None:
        """验证 10 本 reference 手册完整且被 SKILL.md 引用。"""
        expected = [
            "automation-templates.md",
            "community-and-contributors.md",
            "github-access-guide.md",
            "github-oss-ops-pitfalls.md",
            "pr-review-guide.md",
            "release-workflow.md",
            "reporting.md",
            "response-templates.md",
            "security-vulnerability-sop.md",
            "triage-workflow.md",
        ]
        text = self.skill_file.read_text(encoding="utf-8")
        for ref in expected:
            ref_path = self.ref_dir / ref
            self.assertTrue(ref_path.is_file(), f"Reference file missing on disk: {ref}")
            self.assertIn(f"references/{ref}", text, f"Reference not cited in SKILL.md: {ref}")

    def test_ast_syntax_integrity(self) -> None:
        """通过 AST 静态语法解析门禁校验所有 Python 脚本无语法错误。"""
        py_files = list(self.scripts_dir.glob("*.py")) + list((self.root / "tests").glob("*.py"))
        self.assertGreaterEqual(len(py_files), 3, "Should have at least 3 python files")
        for py_file in py_files:
            code = py_file.read_text(encoding="utf-8")
            try:
                tree = ast.parse(code, filename=str(py_file))
                self.assertIsNotNone(tree, f"AST parse returned None for {py_file.name}")
            except SyntaxError as e:
                self.fail(f"AST syntax parsing error in {py_file.name}: {e}")

    def test_validate_ops_execution(self) -> None:
        """验证 validate_ops 模块功能及快速/全检模式。"""
        # Full validation
        full_res = validate_ops.validate_repository(quick=False, read_only=True)
        self.assertEqual(full_res["status"], "PASS", f"validate_ops failed: {full_res.get('errors')}")
        self.assertGreater(full_res["metrics"]["total_checks"], 25)

        # Quick validation
        quick_res = validate_ops.validate_repository(quick=True, read_only=True)
        self.assertEqual(quick_res["status"], "PASS")
        self.assertTrue(quick_res["quick_mode"])

    def test_safety_and_fact_card(self) -> None:
        """验证 Fact Card 规范、Zero-Mutation 铁律与授权声明。"""
        text = self.skill_file.read_text(encoding="utf-8")
        self.assertIn("Fact Card", text)
        self.assertIn("Zero-Mutation", text)
        self.assertIn("用户显式授权", text)

        # 凭据安全：绝无真实 Token 硬编码
        secret_patterns = [
            r"ghp_[A-Za-z0-9]{20,}",
            r"github_pat_[A-Za-z0-9_]{20,}",
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        ]
        for pattern in secret_patterns:
            self.assertIsNone(re.search(pattern, text))


if __name__ == "__main__":
    unittest.main()
