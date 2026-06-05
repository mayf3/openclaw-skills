#!/usr/bin/env python3
"""
metadata.json 迁移脚本

将旧格式迁移到新格式（支持多层分析）
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def migrate_metadata(metadata_file):
    """迁移 metadata.json 到新格式"""

    with open(metadata_file, "r", encoding="utf-8") as f:
        old_metadata = json.load(f)

    # 检查是否已经是新格式
    if "analysis_levels" in old_metadata:
        print("metadata.json 已经是新格式，无需迁移")
        return True

    # 创建新格式
    new_metadata = {
        "stock_code": old_metadata.get("stock_code"),
        "stock_name": old_metadata.get("stock_name"),
        "industry": old_metadata.get("industry"),
        "market_cap": old_metadata.get("market_cap"),
        "created_at": old_metadata.get("created_at", datetime.now().strftime("%Y-%m-%d")),
        "updated_at": datetime.now().strftime("%Y-%m-%d"),

        "analysis_levels": {
            "level_1": {
                "name": "四维度快速分析",
                "file": "reports/价值投资分析.md",
                "completed": False,
                "last_update": None,
                "score": None,
                "rating": None
            },
            "level_2": {
                "name": "财报深度解读",
                "file": "reports/财报深度解读.md",
                "completed": False,
                "last_update": None
            },
            "level_3": {
                "name": "估值建模",
                "file": "reports/估值建模.md",
                "completed": False,
                "last_update": None
            },
            "level_4": {
                "name": "投资决策",
                "file": "reports/投资决策.md",
                "completed": False,
                "last_update": None
            }
        },

        "data_sources": old_metadata.get("data_sources", []),

        "quality_checks": old_metadata.get("quality_checks", {}),

        "changelog": old_metadata.get("changelog", [])
    }

    # 从旧格式迁移 Level 1 数据
    if "analysis" in old_metadata:
        old_analysis = old_metadata["analysis"]
        new_metadata["analysis_levels"]["level_1"]["completed"] = True
        new_metadata["analysis_levels"]["level_1"]["last_update"] = old_analysis.get("last_update")
        new_metadata["analysis_levels"]["level_1"]["score"] = old_analysis.get("score")
        new_metadata["analysis_levels"]["level_1"]["rating"] = old_analysis.get("rating")

    # 添加迁移记录
    new_metadata["changelog"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "action": "迁移",
        "details": "metadata.json 从 v1.0 迁移到 v2.0（支持多层分析）"
    })

    # 备份旧文件
    backup_file = metadata_file.with_suffix(".json.backup")
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(old_metadata, f, ensure_ascii=False, indent=2)
    print(f"已备份旧文件到: {backup_file}")

    # 写入新文件
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(new_metadata, f, ensure_ascii=False, indent=2)

    print(f"✓ 已迁移: {metadata_file}")
    return True

def main():
    if len(sys.argv) < 2:
        print("用法: python3 migrate_metadata.py <metadata.json路径>")
        print("示例: python3 migrate_metadata.py ~/workspace/blog/knowledge-base/docs/投资分析/stocks/600519-贵州茅台/metadata.json")
        sys.exit(1)

    metadata_file = Path(sys.argv[1]).expanduser()

    if not metadata_file.exists():
        print(f"✗ 文件不存在: {metadata_file}")
        sys.exit(1)

    if migrate_metadata(metadata_file):
        print("✓ 迁移完成")
        sys.exit(0)
    else:
        print("✗ 迁移失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
