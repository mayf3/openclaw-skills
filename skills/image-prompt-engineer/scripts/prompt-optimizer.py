#!/usr/bin/env python3
"""Image Prompt Optimizer — 中文需求 → 英文 Prompt 转换"""

import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Image Prompt Optimizer")
    parser.add_argument("--chinese", "-c", help="中文需求描述")
    parser.add_argument("--platform", "-p", choices=["midjourney", "sd", "sd", "dalle3", "flux"],
                       default="midjourney", help="目标平台")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text",
                       help="输出格式")
    parser.add_argument("--optimize", "-o", help="优化已有英文 prompt")

    args = parser.parse_args()

    if not args.chinese and not args.optimize:
        # Interactive mode
        print("🖼️  Image Prompt Optimizer")
        print("=" * 50)
        cn = input("📝 输入中文需求: ").strip()
        plat = input(f"🎯 目标平台 (midjourney/sd/dalle3/flux) [midjourney]: ").strip() or "midjourney"
        args.chinese = cn
        args.platform = plat

    result = {
        "platform": args.platform,
        "chinese_input": args.chinese or "",
        "recommended_params": get_params(args.platform)
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n🎯 目标平台: {args.platform}")
        print(f"📝 中文需求: {args.chinese or '(待输入)'}")
        print(f"\n📋 推荐参数:")
        for k, v in result["recommended_params"].items():
            print(f"   {k}: {v}")
        print(f"\n💡 提示: 将中文需求翻译成结构化英文 prompt 后，")
        print(f"   参考 references/ 下的对应平台指南调整格式。")


def get_params(platform):
    params = {
        "midjourney": {
            "version": "6",
            "style": "raw (写实) 或 默认 (艺术)",
            "stylize": "50-100 (写实), 200-600 (艺术)",
            "aspect_ratio": "按需 16:9, 9:16, 4:3, 1:1",
            "notes": "用自然英语句子，逗号分隔"
        },
        "sd": {
            "cfg_scale": "7-9",
            "steps": "25-30",
            "sampler": "DPM++ 2M Karras",
            "size": "1024x1024 (SDXL)",
            "notes": "用关键词堆叠，逗号分隔，支持权重()"
        },
        "dalle3": {
            "notes": "用自然语言段落，不支持权重和负面词",
            "aspect_ratio": "在描述中指定"
        },
        "flux": {
            "notes": "类似 MJ 的自然语言，但能吃更多关键词",
            "aspect_ratio": "在描述中指定"
        }
    }
    return params.get(platform, {})


if __name__ == "__main__":
    main()
