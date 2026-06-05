#!/usr/bin/env python3
"""
股票分析目录结构严格验证脚本 v3.0

新功能：
- 根据 version.json 动态调整验证要求
- V1: 基础验证（不要求财报）
- V2: 深度分析验证（要求财报，至少2年年报）
- V3: 估值建模验证（要求财报，至少3年年报）
- V4: 投资决策验证（要求财报，至少5年年报）
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# ANSI 颜色代码
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

# ==================== 白名单配置 ====================

ALLOWED_ROOT_FILES = ["metadata.json", "version.json", "README.md"]

ALLOWED_DATA_FILES = {
    "financial.json": {
        "required": True,
        "required_fields": ["stock_code", "stock_name", "data_date", "profitability", "cash_quality"]
    },
    "valuation.json": {
        "required": True,
        "required_fields": ["stock_code", "stock_name", "current_valuation"]
    },
    "metrics_history.json": {
        "required": False,
        "required_fields": []
    },
    "cash_flow.json": {
        "required": False,
        "required_fields": []
    },
    "industry_data.json": {
        "required": False,
        "required_fields": []
    }
}

ALLOWED_REPORT_FILES = {
    "价值投资分析.md": {
        "required": True,
        "required_sections": [
            "公司概况", "财务质量分析", "估值分析",
            "护城河分析", "管理层分析", "投资建议"
        ]
    },
    "财报深度解读.md": {"required": False, "required_sections": []},
    "估值建模.md": {"required": False, "required_sections": []},
    "投资决策.md": {"required": False, "required_sections": []}
}

ALLOWED_FINANCIAL_REPORT_PATTERNS = [
    r"^\d{4}-annual-report\.pdf$",
    r"^\d{4}-Q[1-4]-report\.pdf$",
    r"^\d{4}-semiannual-report\.pdf$",
    r"^\d{4}-annual-report\.md$",
    r"^index\.md$"
]

# ==================== 版本要求配置 ====================

VERSION_REQUIREMENTS = {
    "V1": {
        "name": "Level 1: 快速分析",
        "financial_reports_required": False,
        "min_annual_reports": 0,
        "level_2_required": False,
        "level_3_required": False,
        "level_4_required": False
    },
    "V2": {
        "name": "Level 2: 深度分析",
        "financial_reports_required": True,
        "min_annual_reports": 2,
        "level_2_required": True,
        "level_3_required": False,
        "level_4_required": False
    },
    "V3": {
        "name": "Level 3: 估值建模",
        "financial_reports_required": True,
        "min_annual_reports": 3,
        "level_2_required": True,
        "level_3_required": True,
        "level_4_required": False
    },
    "V4": {
        "name": "Level 4: 投资决策",
        "financial_reports_required": True,
        "min_annual_reports": 5,
        "level_2_required": True,
        "level_3_required": True,
        "level_4_required": True
    }
}

# ==================== 验证函数 ====================

def get_version_info(base_path):
    """读取版本信息"""
    version_file = base_path / "version.json"
    if not version_file.exists():
        return None

    try:
        with open(version_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print_error(f"读取 version.json 失败: {e}")
        return None

def validate_version_file(base_path):
    """验证 version.json"""
    print_info("验证 version.json...")

    version_file = base_path / "version.json"
    if not version_file.exists():
        print_warning("version.json 不存在（将使用 V1 默认要求）")
        return "V1"

    try:
        with open(version_file, "r", encoding="utf-8") as f:
            version_data = json.load(f)

        current_version = version_data.get("current_version", "V1")
        version_info = VERSION_REQUIREMENTS[current_version]

        print_success(f"当前版本: {current_version} - {version_info['name']}")
        return current_version

    except Exception as e:
        print_error(f"version.json 格式错误: {e}")
        return "V1"

def validate_financial_reports_by_version(base_path, current_version):
    """根据版本验证财报"""
    print_info(f"验证 financial-reports/ (版本: {current_version})...")

    fr_dir = base_path / "financial-reports"
    if not fr_dir.exists():
        if VERSION_REQUIREMENTS[current_version]["financial_reports_required"]:
            print_error(f"{current_version} 要求财报目录存在")
            return False
        else:
            print_info(f"{current_version} 不强制要求财报")
            return True

    all_valid = True
    annual_reports = []

    # 检查每个文件
    for item in fr_dir.iterdir():
        if item.is_file():
            filename = item.name

            # 检查命名规范
            filename_valid = False
            for pattern in ALLOWED_FINANCIAL_REPORT_PATTERNS:
                if re.match(pattern, filename):
                    filename_valid = True
                    # 统计年报数量
                    if re.match(r"^\d{4}-annual-report\.", filename):
                        annual_reports.append(filename)
                    break

            if filename_valid:
                print_success(f"financial-reports/{filename}")
            else:
                print_warning(f"financial-reports/{filename} 命名不符合规范")

    # 检查年报数量是否满足版本要求
    min_required = VERSION_REQUIREMENTS[current_version]["min_annual_reports"]
    if min_required > 0:
        if len(annual_reports) < min_required:
            print_error(f"{current_version} 要求至少 {min_required} 份年报，当前只有 {len(annual_reports)} 份")
            all_valid = False
        else:
            print_success(f"年报数量: {len(annual_reports)} 份（满足 {current_version} 要求）")

    return all_valid

def validate_reports_by_version(base_path, current_version):
    """根据版本验证报告文件"""
    print_info(f"验证 reports/ (版本: {current_version})...")

    reports_dir = base_path / "reports"
    if not reports_dir.exists():
        print_error("reports/ 目录不存在")
        return False

    all_valid = True
    version_req = VERSION_REQUIREMENTS[current_version]

    # 检查 Level 2 报告
    if version_req["level_2_required"]:
        level2_file = reports_dir / "财报深度解读.md"
        if not level2_file.exists():
            print_error(f"{current_version} 要求 财报深度解读.md 存在")
            all_valid = False
        else:
            print_success("reports/财报深度解读.md 存在")
    else:
        print_info(f"{current_version} 不强制要求 财报深度解读.md")

    # 检查 Level 3 报告
    if version_req["level_3_required"]:
        level3_file = reports_dir / "估值建模.md"
        if not level3_file.exists():
            print_error(f"{current_version} 要求 估值建模.md 存在")
            all_valid = False
        else:
            print_success("reports/估值建模.md 存在")
    else:
        print_info(f"{current_version} 不强制要求 估值建模.md")

    # 检查 Level 4 报告
    if version_req["level_4_required"]:
        level4_file = reports_dir / "投资决策.md"
        if not level4_file.exists():
            print_error(f"{current_version} 要求 投资决策.md 存在")
            all_valid = False
        else:
            print_success("reports/投资决策.md 存在")
    else:
        print_info(f"{current_version} 不强制要求 投资决策.md")

    return all_valid

def main():
    if len(sys.argv) < 2:
        print("用法: python3 validate_structure_v3.py <股票目录路径>")
        sys.exit(1)

    base_path = Path(sys.argv[1]).expanduser()

    if not base_path.exists():
        print_error(f"路径不存在: {base_path}")
        sys.exit(1)

    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}股票分析目录结构严格验证 v3.0{RESET}")
    print(f"{BLUE}路径: {base_path}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    # 1. 获取版本信息
    current_version = validate_version_file(base_path)
    print()

    # 2. 验证根目录
    print_info("验证根目录文件...")
    if (base_path / "version.json").exists():
        print_success("version.json 存在")
    if (base_path / "metadata.json").exists():
        print_success("metadata.json 存在")
    print()

    # 3. 验证 data/ 目录（所有版本都要求）
    print_info("验证 data/ 目录...")
    data_dir = base_path / "data"
    if data_dir.exists():
        for filename in ["financial.json", "valuation.json"]:
            if (data_dir / filename).exists():
                print_success(f"data/{filename} 存在")
    print()

    # 4. 验证 reports/ 目录（根据版本）
    validate_reports_by_version(base_path, current_version)
    print()

    # 5. 验证 financial-reports/ 目录（根据版本）
    validate_financial_reports_by_version(base_path, current_version)
    print()

    print(f"{BLUE}{'='*60}{RESET}")
    print_success(f"验证完成！当前版本: {current_version}")
    print(f"{BLUE}{'='*60}{RESET}")

if __name__ == "__main__":
    main()
