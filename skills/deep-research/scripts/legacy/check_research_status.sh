#!/bin/bash

# check_research_status.sh
# 检查RESEARCH-CHECKLIST.md中的研究状态

WORKSPACE="$WORKSPACE"
CHECKLIST="$WORKSPACE/RESEARCH-CHECKLIST.md"

echo "📋 检查RESEARCH-CHECKLIST.md..."
echo ""

# 提取统计信息
total=$(grep -c "^### #" "$CHECKLIST" 2>/dev/null || echo "0")
completed=$(grep -c "状态.*✅.*已完成" "$CHECKLIST" 2>/dev/null || echo "0")
ongoing=$(grep -c "状态.*🔄" "$CHECKLIST" 2>/dev/null || echo "0")
unclear=$(grep -c "状态.*⏸️" "$CHECKLIST" 2>/dev/null || echo "0")

echo "📊 当前研究统计:"
echo "- 总研究数: $total"
echo "- 已完成: $completed ✅"
echo "- 进行中: $ongoing 🔄"
echo "- 状态不明: $unclear ⏸️"
echo ""

# 查找进行中和状态不明的研究
if [ "$ongoing" -gt 0 ] || [ "$unclear" -gt 0 ]; then
    echo "⚠️  发现未完成的研究:"
    echo ""

    # 提取进行中的研究
    if [ "$ongoing" -gt 0 ]; then
        echo "🔄 进行中的研究:"
        awk '/^### #/ {id=$0} /状态.*🔄.*进行中/ {print id " " $0}' "$CHECKLIST" | \
            sed 's/状态.*🔄.*进行中/🔄 进行中/' | \
            while read line; do
                echo "  $line"
                # 提取发起日期
                id=$(echo "$line" | awk '{print $2}')
                grep -A 10 "$id" "$CHECKLIST" | grep "发起日期" | sed 's/^/    /'
            done
        echo ""
    fi

    # 提取状态不明的研究
    if [ "$unclear" -gt 0 ]; then
        echo "⏸️  状态不明的研究:"
        awk '/^### #/ {id=$0} /状态.*⏸️.*状态不明/ {print id " " $0}' "$CHECKLIST" | \
            sed 's/状态.*⏸️.*状态不明/⏸️ 状态不明/' | \
            while read line; do
                echo "  $line"
                # 提取发起日期
                id=$(echo "$line" | awk '{print $2}')
                grep -A 10 "$id" "$CHECKLIST" | grep "发起日期" | sed 's/^/    /'
            done
        echo ""
    fi

    # 检查超时的研究（超过24小时）
    echo "⏰ 检查超时的研究（>24小时未更新）:"
    # 简化版本：列出所有研究及其发起日期
    awk '/^### #/ {id=$0} /- \*\*发起日期\*\*: / {
        print id
        print $0
    }' "$CHECKLIST" | head -20
    echo ""

else
    echo "✅ 没有未完成的研究"
fi

exit 0
