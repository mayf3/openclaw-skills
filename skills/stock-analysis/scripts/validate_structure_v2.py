#!/usr/bin/env python3
"""
股票分析目录结构严格验证脚本 v2.0

功能：
1. 白名单机制：只允许特定文件名和格式
2. 内容完整性检查：检查 MD/JSON 文件的必需字段/章节
3. 财报命名规范检查
4. 目录结构完整性检查
5. 禁止额外文件（不符合规范的文件）
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

# 允许的根目录文件
ALLOWED_ROOT_FILES = ["metadata.json", "README.md"]

# 允许的 data/ 目录文件
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

# 允许的 reports/ 目录文件
ALLOWED_REPORT_FILES = {
    "价值投资分析.md": {
        "required": True,
        "required_sections": [
            "公司概况",
            "财务质量分析",
            "估值分析",
            "护城河分析",
            "管理层分析",
            "投资建议"
        ]
    },
    "财报深度解读.md": {
        "required": False,
        "required_sections": []
    },
    "估值建模.md": {
        "required": False,
        "required_sections": []
    },
    "投资决策.md": {
        "required": False,
        "required_sections": []
    }
}

# 允许的 financial-reports/ 目录文件模式
ALLOWED_FINANCIAL_REPORT_PATTERNS = [
    r"^\d{4}-annual-report\.pdf$",          # 2024-annual-report.pdf（全年报）
    r"^\d{4}-Q[1-4]-report\.pdf$",           # 2024-Q1-report.pdf（季报）
    r"^\d{4}-semiannual-report\.pdf$",      # 2024-semiannual-report.pdf（半年报）
    r"^\d{4}-annual-report\.md$",           # 2024-annual-report.md（全年报MD）
    r"^index\.md$"                           # index.md（财报索引）
]

# ==================== 验证函数 ====================

def validate_root_directory(base_path):
    """验证根目录文件"""
    print_info("验证根目录文件...")

    all_valid = True

    # 检查必需文件
    if not (base_path / "metadata.json").exists():
        print_error("缺少必需文件: metadata.json")
        all_valid = False
    else:
        print_success("metadata.json 存在")

    # 检查是否有不允许的文件
    for item in base_path.iterdir():
        if item.is_file():
            if item.name not in ALLOWED_ROOT_FILES:
                print_warning(f"不允许的根目录文件: {item.name}")
                all_valid = False

    return all_valid

def validate_data_directory(base_path):
    """验证 data/ 目录"""
    print_info("验证 data/ 目录...")

    data_dir = base_path / "data"
    if not data_dir.exists():
        print_error("data/ 目录不存在")
        return False

    all_valid = True

    # 检查每个允许的文件
    for filename, config in ALLOWED_DATA_FILES.items():
        file_path = data_dir / filename

        if not file_path.exists():
            if config["required"]:
                print_error(f"缺少必需文件: data/{filename}")
                all_valid = False
            else:
                print_info(f"可选文件不存在: data/{filename}")
            continue

        # 文件存在，检查格式
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 检查必需字段
            if config["required_fields"]:
                missing_fields = [field for field in config["required_fields"] if field not in data]
                if missing_fields:
                    print_error(f"data/{filename} 缺少必需字段: {', '.join(missing_fields)}")
                    all_valid = False
                else:
                    print_success(f"data/{filename} 格式正确")

        except json.JSONDecodeError as e:
            print_error(f"data/{filename} JSON 格式错误: {e}")
            all_valid = False

    # 检查是否有不允许的文件
    for item in data_dir.iterdir():
        if item.is_file() and item.name not in ALLOWED_DATA_FILES:
            print_warning(f"data/{item.name} 不在白名单中")
            all_valid = False

    return all_valid

def validate_reports_directory(base_path):
    """验证 reports/ 目录"""
    print_info("验证 reports/ 目录...")

    reports_dir = base_path / "reports"
    if not reports_dir.exists():
        print_error("reports/ 目录不存在")
        return False

    all_valid = True

    # 检查每个允许的文件
    for filename, config in ALLOWED_REPORT_FILES.items():
        file_path = reports_dir / filename

        if not file_path.exists():
            if config["required"]:
                print_error(f"缺少必需文件: reports/{filename}")
                all_valid = False
            else:
                print_info(f"可选文件不存在: reports/{filename}")
            continue

        # 文件存在，检查内容
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 检查文件是否为空
            if not content.strip():
                print_error(f"reports/{filename} 文件为空")
                all_valid = False
                continue

            # 检查必需章节
            if config["required_sections"]:
                missing_sections = []
                for section in config["required_sections"]:
                    # 检查章节标题（支持 # ## ### 等格式，允许前面的 emoji）
                    pattern = rf"^#+\s*[^\n]*{re.escape(section)}"
                    if not re.search(pattern, content, re.MULTILINE):
                        missing_sections.append(section)

                if missing_sections:
                    print_error(f"reports/{filename} 缺少必需章节: {', '.join(missing_sections)}")
                    all_valid = False
                else:
                    print_success(f"reports/{filename} 包含所有必需章节")

        except Exception as e:
            print_error(f"reports/{filename} 读取失败: {e}")
            all_valid = False

    # 检查是否有不允许的文件
    for item in reports_dir.iterdir():
        if item.is_file() and item.name not in ALLOWED_REPORT_FILES:
            print_warning(f"reports/{item.name} 不在白名单中")
            all_valid = False

    return all_valid

def validate_financial_reports_directory(base_path):
    """验证 financial-reports/ 目录"""
    print_info("验证 financial-reports/ 目录...")

    fr_dir = base_path / "financial-reports"
    if not fr_dir.exists():
        print_warning("financial-reports/ 目录不存在")
        return False

    all_valid = True
    has_files = False

    # 检查每个文件
    for item in fr_dir.iterdir():
        if item.is_file():
            has_files = True
            # 检查文件名是否符合规范
            filename_valid = False
            for pattern in ALLOWED_FINANCIAL_REPORT_PATTERNS:
                if re.match(pattern, item.name):
                    filename_valid = True
                    break

            if filename_valid:
                print_success(f"financial-reports/{item.name} 命名符合规范")
            else:
                print_warning(f"financial-reports/{item.name} 命名不符合规范")
                all_valid = False

    if not has_files:
        print_warning("financial-reports/ 目录为空")

    # 检查是否有财报（根据分析层级决定是否必需）
    metadata_file = base_path / "metadata.json"
    if metadata_file.exists():
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            # 检查分析层级
            if "analysis_levels" in metadata:
                level2_completed = metadata["analysis_levels"].get("level_2", {}).get("completed", False)

                # Level 2+ 完成时，财报应该是必需的
                if level2_completed and not has_files:
                    print_error("Level 2 分析已完成，但缺少财报文件")
                    all_valid = False

        except Exception as e:
            pass  # 如果读取失败，忽略这个检查

    return all_valid

def validate_metadata(base_path):
    """验证 metadata.json 内容"""
    print_info("验证 metadata.json 内容...")

    metadata_file = base_path / "metadata.json"
    if not metadata_file.exists():
        print_error("metadata.json 不存在")
        return False

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except json.JSONDecodeError as e:
        print_error(f"metadata.json 格式错误: {e}")
        return False

    all_valid = True

    # 检查必需字段
    required_fields = ["stock_code", "stock_name", "analysis_levels"]
    for field in required_fields:
        if field not in metadata:
            print_error(f"metadata.json 缺少必需字段: {field}")
            all_valid = False
        else:
            print_success(f"metadata.json 包含字段: {field}")

    # 检查分析层级
    if "analysis_levels" in metadata:
        required_levels = ["level_1", "level_2", "level_3", "level_4"]
        for level in required_levels:
            if level not in metadata["analysis_levels"]:
                print_warning(f"metadata.json 缺少分析层级: {level}")

    return all_valid

def validate_extra_directories(base_path):
    """检查是否有额外的目录（不允许的）"""
    print_info("检查额外目录...")

    allowed_dirs = {"data", "financial-reports", "reports", "archive"}
    extra_dirs = []

    for item in base_path.iterdir():
        if item.is_dir() and item.name not in allowed_dirs:
            extra_dirs.append(item.name)

    if extra_dirs:
        print_warning(f"发现额外目录: {', '.join(extra_dirs)}")
        return False
    else:
        print_success("没有额外目录")
        return True

def main():
    if len(sys.argv) < 2:
        print("用法: python3 validate_structure_v2.py <股票目录路径>")
        print("示例: python3 validate_structure_v2.py ~/workspace/blog/knowledge-base/docs/投资分析/stocks/600519-贵州茅台")
        sys.exit(1)

    base_path = Path(sys.argv[1]).expanduser()

    if not base_path.exists():
        print_error(f"路径不存在: {base_path}")
        sys.exit(1)

    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}股票分析目录结构严格验证 v2.0{RESET}")
    print(f"{BLUE}路径: {base_path}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    all_valid = True

    # 1. 验证根目录
    if not validate_root_directory(base_path):
        all_valid = False

    print()

    # 2. 验证 data/ 目录
    if not validate_data_directory(base_path):
        all_valid = False

    print()

    # 3. 验证 reports/ 目录
    if not validate_reports_directory(base_path):
        all_valid = False

    print()

    # 4. 验证 financial-reports/ 目录
    if not validate_financial_reports_directory(base_path):
        all_valid = False

    print()

    # 5. 验证 metadata.json
    if not validate_metadata(base_path):
        all_valid = False

    print()

    # 6. 检查额外目录
    if not validate_extra_directories(base_path):
        all_valid = False

    print()
    print(f"{BLUE}{'='*60}{RESET}")
    if all_valid:
        print(f"{GREEN}验证通过！目录结构和内容完全符合规范。{RESET}")
    else:
        print(f"{RED}验证失败！请修复上述问题。{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    main()
