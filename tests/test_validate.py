"""scripts/validate.py 的正向与负向测试。

运行：python -m unittest discover tests
"""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate  # noqa: E402


class ValidateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name) / "github-oss-ops"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def edit(self, rel: str, old: str, new: str) -> None:
        path = self.root / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"fixture text not found in {rel}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def append(self, rel: str, extra: str) -> None:
        path = self.root / rel
        path.write_text(path.read_text(encoding="utf-8") + extra, encoding="utf-8")

    def assertFailsWith(self, fragment: str) -> None:
        report = validate.validate(self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(fragment in e for e in report["errors"]), report["errors"])

    # 正向
    def test_repository_passes(self) -> None:
        report = validate.validate(ROOT)
        self.assertEqual(report["status"], "PASS", report["errors"])
        self.assertGreater(report["checks"], 50)

    def test_cli_json(self) -> None:
        self.assertEqual(validate.main(["--json", "--root", str(self.root)]), 0)

    # 负向
    def test_missing_required_file(self) -> None:
        (self.root / "SECURITY.md").unlink()
        self.assertFailsWith("SECURITY.md")

    def test_manifest_version_drift(self) -> None:
        manifest = json.loads((self.root / "manifest.json").read_text(encoding="utf-8"))
        manifest["version"] = "0.0.1"
        (self.root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertFailsWith("manifest.json")

    def test_bad_changelog_heading(self) -> None:
        self.append("CHANGELOG.md", "\n## 6-08-21\n")
        self.assertFailsWith("CHANGELOG 标题格式")

    def test_orphan_reference(self) -> None:
        (self.root / "references/orphan.md").write_text("# orphan\n", encoding="utf-8")
        self.assertFailsWith("orphan.md")

    def test_broken_local_link(self) -> None:
        self.append("README.md", "\n[x](references/missing.md)\n")
        self.assertFailsWith("本地链接失效")

    def test_hardcoded_step_number(self) -> None:
        self.append("references/reporting.md", "\n> SKILL.md Step 8 引用本文件。\n")
        self.assertFailsWith("Step N")

    def test_secret_like_string(self) -> None:
        self.append("examples/README.md", "\n" + "gh" + "p_" + "A" * 36 + "\n")
        self.assertFailsWith("疑似凭据")

    def test_readme_version_stale(self) -> None:
        # 从当前版本推导旧版本号，避免每次发版都要改测试
        version = validate.validate(ROOT)["version"]
        major, minor, patch = (int(x) for x in version.split("."))
        stale = f"{major}.{minor}.{patch + 1}"
        for name in ("README.md", "README.en.md"):
            path = self.root / name
            path.write_text(path.read_text(encoding="utf-8").replace(f"v{version}", f"v{stale}"), encoding="utf-8")
        self.assertFailsWith("未写明当前版本")

    def test_readme_latest_date_drift(self) -> None:
        path = self.root / "README.en.md"
        text = re.sub(r"^(## 🆕 Latest release: v\S+) \(\d{4}-\d{2}-\d{2}\)", r"\1 (1999-01-01)",
                      path.read_text(encoding="utf-8"), count=1, flags=re.M)
        path.write_text(text, encoding="utf-8")
        self.assertFailsWith("README.en.md 未写明当前版本")

    def test_readme_en_missing_install_path(self) -> None:
        path = self.root / "README.en.md"
        path.write_text(path.read_text(encoding="utf-8").replace("~/.cursor/skills/", "~/.cursor/skill/"), encoding="utf-8")
        self.assertFailsWith("README.en.md 缺少")

    def test_manifest_updated_at_drift(self) -> None:
        manifest = json.loads((self.root / "manifest.json").read_text(encoding="utf-8"))
        manifest["updated_at"] = "1999-01-01"
        (self.root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertFailsWith("updated_at")

    def test_metadata_title_drift(self) -> None:
        path = self.root / ".github/repository-metadata.yml"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("title: GitHub OSS Ops v", "title: GitHub OSS Ops v0."), encoding="utf-8")
        self.assertFailsWith("release title")

    def test_broken_anchor(self) -> None:
        self.append("README.md", "\n[x](references/reporting.md#不存在的章节)\n")
        self.assertFailsWith("锚点不存在")

    def test_broken_same_file_anchor(self) -> None:
        self.append("references/reporting.md", "\n[x](#no-such-heading)\n")
        self.assertFailsWith("锚点不存在")

    def test_anchor_slug_rules(self) -> None:
        anchors = validate._anchors("## 2.1 `pull_request_target` + 检出 PR 代码\n## FAQ\n## FAQ\n```\n# 代码块里的不算\n```\n")
        self.assertIn("21-pull_request_target--检出-pr-代码", anchors)
        self.assertIn("faq-1", anchors)
        self.assertNotIn("代码块里的不算", anchors)

    def test_python_syntax_error(self) -> None:
        (self.root / "scripts/broken.py").write_text("def f(:\n    pass\n", encoding="utf-8")
        self.assertFailsWith("语法错误")


if __name__ == "__main__":
    unittest.main()
