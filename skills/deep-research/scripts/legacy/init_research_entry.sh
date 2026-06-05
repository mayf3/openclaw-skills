#!/bin/bash

# init_research_entry.sh
# 在RESEARCH-CHECKLIST.md中初始化新的研究条目

set -e

WORKSPACE="$WORKSPACE"
CHECKLIST="$WORKSPACE/RESEARCH-CHECKLIST.md"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --topic)
            TOPIC="$2"
            shift 2
            ;;
        --date)
            DATE="$2"
            shift 2
            ;;
        --method)
            METHOD="$2"
            shift 2
            ;;
        --description)
            DESCRIPTION="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 验证必需参数
if [ -z "$TOPIC" ] || [ -z "$DATE" ]; then
    echo "❌ 错误: 缺少必需参数"
    echo "用法: $0 --topic \"主题\" --date YYYY-MM-DD [--method \"方法\"] [--description \"描述\"]"
    exit 1
fi

# 设置默认值
METHOD=${METHOD:-"Gemini Deep Research"}
CURRENT_TIME=$(date +%H:%M)
TIMESTAMP="$DATE $CURRENT_TIME"

# 生成研究ID（查找当前最大的ID）
last_id=$(grep "^### #" "$CHECKLIST" | tail -1 | awk '{print $2}' | tr -d '#')
if [ -z "$last_id" ]; then
    new_id=1
else
    new_id=$((last_id + 1))
fi

# 生成目录名（简化的topic名称）
topic_slug=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
topic_slug=$(echo "$topic_slug" | cut -c1-50)  # 限制长度
research_dir="reports/$DATE-$topic_slug"

# 生成启动截图文件名
timestamp=$(date +%s)
start_screenshot="gemini-research-$timestamp-start.jpg"

# 创建研究目录
mkdir -p "$WORKSPACE/$research_dir/raw/screenshots"
echo "✅ 创建研究目录: $research_dir"

# 在CHECKLIST中添加新条目
cat >> "$CHECKLIST" << EOF

### #$new_id - $TOPIC
- **状态**: 🔄 进行中
- **发起日期**: $TIMESTAMP
- **研究方法**: $METHOD
- **研究主题**: ${DESCRIPTION:-"$TOPIC - 2024-2025年最新研究进展"}
- **结果目录**: \`$research_dir/\`（待创建）
- **截图**:
  - ✅ $start_screenshot → \`temp/\`
- **下一步**: 等待研究完成，提取结果，生成7个文档

EOF

echo "✅ 添加研究条目到CHECKLIST (#$new_id)"

# 更新统计
total=$(grep -c "^### #" "$CHECKLIST")
completed=$(grep -c "状态.*✅.*已完成" "$CHECKLIST" || echo "0")
ongoing=$(grep -c "状态.*🔄.*进行中" "$CHECKLIST" || echo "0")
unclear=$(grep -c "状态.*⏸️.*状态不明" "$CHECKLIST" || echo "0")

# 更新头部统计
sed -i.bak "s/- \*\*总研究数\*\*: [0-9]*/- **总研究数**: $total/" "$CHECKLIST"
sed -i.bak "s/- \*\*已完成\*\*: [0-9]* ✅/- **已完成**: $completed ✅/" "$CHECKLIST"
sed -i.bak "s/- \*\*进行中\*\*: [0-9]* 🔄/- **进行中**: $ongoing 🔄/" "$CHECKLIST"
sed -i.bak "s/- \*\*状态不明\*\*: [0-9]* ⏸️/- **状态不明**: $unclear ⏸️/" "$CHECKLIST"

# 清理备份文件
rm -f "$CHECKLIST.bak"

echo "✅ 更新统计: 总数=$total, 已完成=$completed, 进行中=$ongoing"
echo ""
echo "📋 新研究已初始化:"
echo "  ID: #$new_id"
echo "  主题: $TOPIC"
echo "  时间: $TIMESTAMP"
echo "  目录: $research_dir"

exit 0
