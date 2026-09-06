#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_ops.py - GitHub OSS Ops 运维就绪度与规范校验器

提供快速采样 (--quick)、机读结构化导出 (--json) 与只读保障 (--read-only)。
纯 Python 3.10+ 标准库实现，零第三方依赖。
遵循 Zero-Mutation 铁律，纯只读校验，不修改任何文件。

Usage:
    python scripts/validate_ops.py [--quick] [--json] [--read-only]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent


def validate_repository(quick: bool = False, read_only: bool = True) -> Dict[str, Any]:
    """执行仓库运维规范全景校验。"""
    report: Dict[str, Any] = {
        "status": "PASS",
        "skill": "github-oss-ops",
        "quick_mode": quick,
        "read_only": read_only,
        "checks": [],
        "errors": [],
        "warnings": [],
        "metrics": {},
    }

    # 1. 核心文件在盘检查
    required_files = [
        "SKILL.md",
        "manifest.json",
        "CHANGELOG.md",
        "README.md",
        "README.en.md",
        "scripts/selftest.py",
        "scripts/validate-skill.mjs",
        ".github/repository-metadata.yml",
    ]
    for rel in required_files:
        p = ROOT / rel
        if p.is_file():
            report["checks"].append({"check": f"file_exists:{rel}", "passed": True})
        else:
            report["status"] = "FAIL"
            report["errors"].append(f"Missing required file: {rel}")
            report["checks"].append({"check": f"file_exists:{rel}", "passed": False})

    # 2. 检查 references 目录与避坑指南
    ref_dir = ROOT / "references"
    expected_refs = [
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
    for ref_name in expected_refs:
        ref_file = ref_dir / ref_name
        if ref_file.is_file():
            report["checks"].append({"check": f"ref_exists:{ref_name}", "passed": True})
        else:
            report["status"] = "FAIL"
            report["errors"].append(f"Missing reference file: {ref_name}")
            report["checks"].append({"check": f"ref_exists:{ref_name}", "passed": False})

    # 3. 快速模式直接返回基础检查
    if quick:
        report["metrics"]["quick_check_count"] = len(report["checks"])
        return report

    # 4. SKILL.md 深度合规校验
    skill_file = ROOT / "SKILL.md"
    if skill_file.is_file():
        skill_text = skill_file.read_text(encoding="utf-8")
        
        # 版本号核验
        manifest_file = ROOT / "manifest.json"
        manifest_version = ""
        if manifest_file.is_file():
            try:
                m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
                manifest_version = m_data.get("version", "")
            except Exception as e:
                report["errors"].append(f"Failed to parse manifest.json: {e}")

        if manifest_version and f"version: {manifest_version}" in skill_text:
            report["checks"].append({"check": "skill_version_matches_manifest", "passed": True})
        else:
            report["status"] = "FAIL"
            report["errors"].append(f"SKILL.md version does not match manifest.json ({manifest_version})")
            report["checks"].append({"check": "skill_version_matches_manifest", "passed": False})

        # 核心 Steps 存在性
        for i in range(1, 10):
            step_header = f"## Step {i}"
            if step_header in skill_text:
                report["checks"].append({"check": f"has_step_{i}", "passed": True})
            else:
                report["status"] = "FAIL"
                report["errors"].append(f"SKILL.md missing {step_header}")
                report["checks"].append({"check": f"has_step_{i}", "passed": False})

        # 安全与授权声明检查
        safety_keywords = [
            "用户明确确认",
            "零依赖",
            "只读",
            "Zero-Mutation",
        ]
        for kw in safety_keywords:
            if kw in skill_text:
                report["checks"].append({"check": f"safety_keyword:{kw}", "passed": True})
            else:
                report["status"] = "FAIL"
                report["errors"].append(f"SKILL.md missing safety keyword: {kw}")
                report["checks"].append({"check": f"safety_keyword:{kw}", "passed": False})

        # 事实卡片 (Fact Card) 声明检查
        if "Fact Card" in skill_text or "事实卡" in skill_text:
            report["checks"].append({"check": "fact_card_declared", "passed": True})
        else:
            report["status"] = "FAIL"
            report["errors"].append("SKILL.md missing Fact Card specification")
            report["checks"].append({"check": "fact_card_declared", "passed": False})

        # 引用就近动作引导 (👉 动作：先读)
        action_directives = re.findall(r"👉\s*动作[：:]\s*先读", skill_text)
        if len(action_directives) >= 8:
            report["checks"].append({"check": "inline_action_directives", "passed": True, "count": len(action_directives)})
        else:
            report["warnings"].append(f"SKILL.md has fewer than 8 inline action directives ({len(action_directives)})")
            report["checks"].append({"check": "inline_action_directives", "passed": False, "count": len(action_directives)})

    report["metrics"]["total_checks"] = len(report["checks"])
    report["metrics"]["error_count"] = len(report["errors"])
    report["metrics"]["warning_count"] = len(report["warnings"])
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GitHub OSS Ops 运维就绪度与规范校验器",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--json", action="store_true", help="机读结构化 JSON 格式输出")
    parser.add_argument("--quick", action="store_true", help="快速采样模式（仅核心基础盘查）")
    parser.add_argument("--read-only", action="store_true", default=True, help="强制只读运行保障")
    args = parser.parse_args()

    result = validate_repository(quick=args.quick, read_only=args.read_only)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print(" GitHub OSS Ops 运维就绪度与规范校验")
        print("=" * 60)
        print(f"模式: {'[QUICK 快速采样]' if args.quick else '[FULL 深度全检]'} | 只读安全: 开启")
        print(f"结果: {result['status']}")
        print(f"检查项: {len(result['checks'])} 项 | 错误: {len(result['errors'])} | 告警: {len(result['warnings'])}")
        if result["errors"]:
            print("\n❌ 发现错误:")
            for err in result["errors"]:
                print(f"  - {err}")
        if result["warnings"]:
            print("\n⚠️ 告警项:")
            for w in result["warnings"]:
                print(f"  - {w}")
        if result["status"] == "PASS":
            print("\n✨ 仓库运维规范 100% 达标！")
        print("=" * 60)

    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
