#!/bin/bash

# update_checklist.sh
# 更新RESEARCH-CHECKLIST.md中的研究状态

set -e

WORKSPACE="$WORKSPACE"
CHECKLIST="$WORKSPACE/RESEARCH-CHECKLIST.md"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --id)
            RESEARCH_ID="$2"
            shift 2
            ;;
        --status)
            STATUS="$2"
            shift 2
            ;;
        --field)
            FIELD="$2"
            shift 2
            ;;
        --value)
            VALUE="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 验证必需参数
if [ -z "$RESEARCH_ID" ]; then
    echo "❌ 错误: 缺少研究ID"
    echo "用法: $0 --id \"#5\" --status \"已完成\" [--field \"完成日期\" --value \"2026-03-12 06:30\"]"
    exit 1
fi

# 检查研究ID是否存在
if ! grep -q "^### $RESEARCH_ID" "$CHECKLIST"; then
    echo "❌ 错误: 研究ID $RESEARCH_ID 不存在"
    exit 1
fi

# 更新状态
if [ -n "$STATUS" ]; then
    # 提取状态图标
    case "$STATUS" in
        "已完成"|"完成"|"✅")
            status_icon="✅ 已完成"
            status_text="已完成"
            ;;
        "进行中"|"🔄")
            status_icon="🔄 进行中"
            status_text="进行中"
            ;;
        "状态不明"|"⏸️")
            status_icon="⏸️ 状态不明"
            status_text="状态不明"
            ;;
        "失败"|"❌")
            status_icon="❌ 失败"
            status_text="失败"
            ;;
        *)
            echo "⚠️  未知状态: $STATUS，使用默认格式"
            status_icon="$STATUS"
            status_text="$STATUS"
            ;;
    esac

    # 更新状态行
    sed -i.bak "/^### $RESEARCH_ID/,/^### #/ s/- \*\*状态\*\*:.*/- **状态**: $status_icon/" "$CHECKLIST"
    echo "✅ 更新状态: $RESEARCH_ID → $status_text"
fi

# 更新指定字段
if [ -n "$FIELD" ] && [ -n "$VALUE" ]; then
    sed -i.bak "/^### $RESEARCH_ID/,/^### #/ s/- \*\*$FIELD\*\*:.*/- **$FIELD**: $VALUE/" "$CHECKLIST"
    echo "✅ 更新字段: $FIELD = $VALUE"
fi

# 清理备份文件
rm -f "$CHECKLIST.bak"

# 重新计算统计
total=$(grep -c "^### #" "$CHECKLIST")
completed=$(grep -c "状态.*✅.*已完成" "$CHECKLIST" || echo "0")
ongoing=$(grep -c "状态.*🔄.*进行中" "$CHECKLIST" || echo "0")
unclear=$(grep -c "状态.*⏸️.*状态不明" "$CHECKLIST" || echo "0")
failed=$(grep -c "状态.*❌.*失败" "$CHECKLIST" || echo "0")

# 更新头部统计
sed -i.bak "s/- \*\*总研究数\*\*: [0-9]*/- **总研究数**: $total/" "$CHECKLIST"
sed -i.bak "s/- \*\*已完成\*\*: [0-9]* ✅/- **已完成**: $completed ✅/" "$CHECKLIST"
sed -i.bak "s/- \*\*进行中\*\*: [0-9]* 🔄/- **进行中**: $ongoing 🔄/" "$CHECKLIST"
sed -i.bak "s/- \*\*状态不明\*\*: [0-9]* ⏸️/- **状态不明**: $unclear ⏸️/" "$CHECKLIST"
sed -i.bak "s/- \*\*失败\/中断\*\*: [0-9]* ❌/- **失败/中断**: $failed ❌/" "$CHECKLIST"

# 清理备份文件
rm -f "$CHECKLIST.bak"

echo "✅ 更新统计: 总数=$total, 已完成=$completed, 进行中=$ongoing, 状态不明=$unclear, 失败=$failed"

exit 0
