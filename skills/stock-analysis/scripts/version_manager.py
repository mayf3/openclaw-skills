#!/usr/bin/env python3
"""
股票分析版本管理脚本

创建和管理 version.json，标识当前股票分析所处的版本/阶段
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 分析版本定义
ANALYSIS_VERSIONS = {
    "V1": {
        "name": "Level 1: 快速分析",
        "description": "四维度快速分析，使用API数据",
        "requirements": {
            "financial_reports_required": False,
            "level_2_required": False,
            "level_3_required": False,
            "level_4_required": False
        }
    },
    "V2": {
        "name": "Level 2: 深度分析",
        "description": "财报深度解读，需要财报文件",
        "requirements": {
            "financial_reports_required": True,
            "min_annual_reports": 2,
            "level_2_required": True,
            "level_3_required": False,
            "level_4_required": False
        }
    },
    "V3": {
        "name": "Level 3: 估值建模",
        "description": "DCF模型和估值分析，需要完整历史数据",
        "requirements": {
            "financial_reports_required": True,
            "min_annual_reports": 3,
            "level_2_required": True,
            "level_3_required": True,
            "level_4_required": False
        }
    },
    "V4": {
        "name": "Level 4: 投资决策",
        "description": "完整投资决策分析，所有数据齐全",
        "requirements": {
            "financial_reports_required": True,
            "min_annual_reports": 5,
            "level_2_required": True,
            "level_3_required": True,
            "level_4_required": True
        }
    }
}

def create_version_file(stock_dir, version="V1"):
    """创建 version.json 文件"""
    stock_path = Path(stock_dir).expanduser()

    if not stock_path.exists():
        print(f"✗ 股票目录不存在: {stock_path}")
        return False

    if version not in ANALYSIS_VERSIONS:
        print(f"✗ 无效的版本: {version}")
        print(f"可用版本: {', '.join(ANALYSIS_VERSIONS.keys())}")
        return False

    version_info = ANALYSIS_VERSIONS[version]

    version_data = {
        "current_version": version,
        "version_name": version_info["name"],
        "description": version_info["description"],
        "requirements": version_info["requirements"],
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
        "changelog": [
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "version": version,
                "action": "init",
                "description": f"初始化{version_info['name']}"
            }
        ]
    }

    version_file = stock_path / "version.json"
    with open(version_file, "w", encoding="utf-8") as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    print(f"✓ 已创建 version.json (版本: {version})")
    print(f"  描述: {version_info['description']}")
    return True

def upgrade_version(stock_dir, target_version):
    """升级到更高版本"""
    stock_path = Path(stock_dir).expanduser()
    version_file = stock_path / "version.json"

    if not version_file.exists():
        print(f"✗ version.json 不存在，请先使用 init 创建")
        return False

    # 读取当前版本
    with open(version_file, "r", encoding="utf-8") as f:
        version_data = json.load(f)

    current_version = version_data["current_version"]
    version_order = ["V1", "V2", "V3", "V4"]

    if version_order.index(target_version) <= version_order.index(current_version):
        print(f"✗ 目标版本 {target_version} 不高于当前版本 {current_version}")
        return False

    # 升级
    version_info = ANALYSIS_VERSIONS[target_version]

    # 添加 changelog
    version_data["changelog"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "version": target_version,
        "action": "upgrade",
        "from_version": current_version,
        "description": f"从 {current_version} 升级到 {target_version}"
    })

    # 更新版本信息
    version_data["current_version"] = target_version
    version_data["version_name"] = version_info["name"]
    version_data["description"] = version_info["description"]
    version_data["requirements"] = version_info["requirements"]
    version_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")

    # 写入文件
    with open(version_file, "w", encoding="utf-8") as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    print(f"✓ 已从 {current_version} 升级到 {target_version}")
    print(f"  描述: {version_info['description']}")
    print(f"  新要求: {version_info['requirements']}")
    return True

def get_version(stock_dir):
    """获取当前版本信息"""
    stock_path = Path(stock_dir).expanduser()
    version_file = stock_path / "version.json"

    if not version_file.exists():
        return None

    with open(version_file, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  创建版本文件: python3 version_manager.py <股票目录> init [V1|V2|V3|V4]")
        print("  升级版本:   python3 version_manager.py <股票目录> upgrade <V2|V3|V4>")
        print("  查看版本:   python3 version_manager.py <股票目录> status")
        print()
        print("示例:")
        print("  python3 version_manager.py ~/workspace/blog/knowledge-base/docs/投资分析/stocks/600519-贵州茅台 init V1")
        print("  python3 version_manager.py ~/workspace/blog/knowledge-base/docs/投资分析/stocks/600519-贵州茅台 upgrade V2")
        print("  python3 version_manager.py ~/workspace/blog/knowledge-base/docs/投资分析/stocks/600519-贵州茅台 status")
        sys.exit(1)

    stock_dir = sys.argv[1]
    action = sys.argv[2]

    if action == "init":
        version = sys.argv[3] if len(sys.argv) > 3 else "V1"
        create_version_file(stock_dir, version)

    elif action == "upgrade":
        target_version = sys.argv[3]
        upgrade_version(stock_dir, target_version)

    elif action == "status":
        version_info = get_version(stock_dir)
        if version_info:
            print(f"当前版本: {version_info['current_version']}")
            print(f"版本名称: {version_info['version_name']}")
            print(f"描述: {version_info['description']}")
            print(f"要求: {json.dumps(version_info['requirements'], ensure_ascii=False, indent=2)}")
            print(f"创建时间: {version_info['created_at']}")
            print(f"更新时间: {version_info['updated_at']}")
        else:
            print("未找到版本信息")

if __name__ == "__main__":
    main()
