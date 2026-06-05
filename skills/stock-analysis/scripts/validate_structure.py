#!/usr/bin/env python3
"""
股票分析目录结构验证脚本

功能：
1. 验证目录结构是否符合规范
2. 检查文件名格式
3. 验证数据格式
4. 检查报告完整性
5. 验证 metadata.json 同步状态
"""

import os
import sys
import json
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

def validate_directory_structure(base_path):
    """验证目录结构"""
    print_info("验证目录结构...")

    required_dirs = ["data", "financial-reports", "reports"]
    optional_dirs = ["analysis", "archive"]
    all_valid = True

    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if not dir_path.exists():
            print_error(f"缺少必需目录: {dir_name}/")
            all_valid = False
        else:
            print_success(f"目录存在: {dir_name}/")

    # 检查可选目录
    for dir_name in optional_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print_success(f"可选目录存在: {dir_name}/")

    return all_valid

def validate_metadata(base_path):
    """验证 metadata.json"""
    print_info("验证 metadata.json...")

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

    # 检查必需字段
    required_fields = ["stock_code", "stock_name", "analysis_levels"]
    all_valid = True

    for field in required_fields:
        if field not in metadata:
            print_error(f"缺少必需字段: {field}")
            all_valid = False
        else:
            print_success(f"字段存在: {field}")

    # 检查分析层级
    if "analysis_levels" in metadata:
        for level_key, level_data in metadata["analysis_levels"].items():
            if "file" in level_data:
                file_path = base_path / level_data["file"]
                if level_data.get("completed", False):
                    if not file_path.exists():
                        print_error(f"{level_key} 标记为完成但文件不存在: {level_data['file']}")
                        all_valid = False
                    else:
                        print_success(f"{level_key} 文件存在: {level_data['file']}")

    return all_valid

def validate_data_files(base_path):
    """验证 data/ 目录下的数据文件"""
    print_info("验证数据文件...")

    data_dir = base_path / "data"
    if not data_dir.exists():
        print_error("data/ 目录不存在")
        return False

    required_files = ["financial.json", "valuation.json"]
    optional_files = ["metrics_history.json", "cash_flow.json", "industry_data.json"]
    all_valid = True

    # 检查必需文件
    for filename in required_files:
        file_path = data_dir / filename
        if not file_path.exists():
            print_warning(f"缺少推荐文件: {filename}")
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print_success(f"文件存在且格式正确: {filename}")
            except json.JSONDecodeError:
                print_error(f"文件格式错误: {filename}")
                all_valid = False

    # 检查可选文件
    for filename in optional_files:
        file_path = data_dir / filename
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json.load(f)
                    print_success(f"可选文件存在: {filename}")
            except json.JSONDecodeError:
                print_error(f"可选文件格式错误: {filename}")

    return all_valid

def validate_report_files(base_path):
    """验证 reports/ 目录下的报告文件"""
    print_info("验证报告文件...")

    reports_dir = base_path / "reports"
    if not reports_dir.exists():
        print_error("reports/ 目录不存在")
        return False

    # 检查标准报告文件
    standard_reports = {
        "价值投资分析.md": "Level 1: 四维度快速分析",
        "财报深度解读.md": "Level 2: 财报详细解读",
        "估值建模.md": "Level 3: 估值模型",
        "投资决策.md": "Level 4: 投资建议"
    }

    all_valid = True
    for filename, description in standard_reports.items():
        file_path = reports_dir / filename
        if file_path.exists():
            # 检查文件是否为空
            if file_path.stat().st_size == 0:
                print_error(f"报告文件为空: {filename}")
                all_valid = False
            else:
                print_success(f"报告存在: {filename} ({description})")
        else:
            print_info(f"报告不存在: {filename} ({description})")

    # 检查是否有非标准命名的文件
    for file_path in reports_dir.glob("*.md"):
        if file_path.name not in standard_reports:
            print_warning(f"非标准报告文件: {file_path.name}")

    return all_valid

def validate_filename_format(base_path):
    """验证文件名格式"""
    print_info("验证文件名格式...")

    # 检查是否有带日期的文件（错误）
    reports_dir = base_path / "reports"
    if reports_dir.exists():
        for file_path in reports_dir.glob("*.md"):
            if "-" in file_path.name and file_path.name != "价值投资分析.md":
                # 检查是否包含日期格式（如 -2025, -2025-12-26）
                if any(pattern in file_path.name for pattern in ["-202", "-2025", "-2026"]):
                    print_warning(f"文件名可能包含日期（建议避免）: {file_path.name}")
                else:
                    print_success(f"文件名格式正确: {file_path.name}")

    return True

def sync_metadata_with_reports(base_path):
    """同步 metadata.json 与实际报告状态"""
    print_info("同步 metadata.json...")

    metadata_file = base_path / "metadata.json"
    if not metadata_file.exists():
        print_error("metadata.json 不存在，无法同步")
        return False

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    updated = False
    reports_dir = base_path / "reports"

    # 同步 Level 1 状态
    level1_report = reports_dir / "价值投资分析.md"
    if "analysis_levels" in metadata and "level_1" in metadata["analysis_levels"]:
        level1_data = metadata["analysis_levels"]["level_1"]
        completed = level1_report.exists() and level1_report.stat().st_size > 0

        if level1_data.get("completed") != completed:
            level1_data["completed"] = completed
            level1_data["last_update"] = datetime.now().strftime("%Y-%m-%d")
            updated = True
            print_success(f"同步 Level 1 状态: completed={completed}")

    # 更新总更新时间
    if updated:
        metadata["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print_success("metadata.json 已更新")
    else:
        print_info("metadata.json 无需更新")

    return True

def main():
    if len(sys.argv) < 2:
        print("用法: python3 validate_structure.py <股票目录路径>")
        print("示例: python3 validate_structure.py ~/workspace/blog/knowledge-base/docs/投资分析/stocks/600519-贵州茅台")
        sys.exit(1)

    base_path = Path(sys.argv[1]).expanduser()

    if not base_path.exists():
        print_error(f"路径不存在: {base_path}")
        sys.exit(1)

    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}股票分析目录结构验证{RESET}")
    print(f"{BLUE}路径: {base_path}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    all_valid = True

    # 1. 验证目录结构
    if not validate_directory_structure(base_path):
        all_valid = False

    print()

    # 2. 验证 metadata.json
    if not validate_metadata(base_path):
        all_valid = False

    print()

    # 3. 验证数据文件
    if not validate_data_files(base_path):
        all_valid = False

    print()

    # 4. 验证报告文件
    if not validate_report_files(base_path):
        all_valid = False

    print()

    # 5. 验证文件名格式
    if not validate_filename_format(base_path):
        all_valid = False

    print()

    # 6. 同步 metadata.json
    sync_metadata_with_reports(base_path)

    print()
    print(f"{BLUE}{'='*60}{RESET}")
    if all_valid:
        print(f"{GREEN}验证通过！目录结构符合规范。{RESET}")
    else:
        print(f"{RED}验证失败！请修复上述问题。{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    main()
