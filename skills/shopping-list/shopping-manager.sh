#!/bin/bash

# 购物清单管理脚本
# Shopping List Manager Script

set -euo pipefail

# 配置
WORKSPACE_DIR="${WORKSPACE_DIR:-$WORKSPACE_DIR}"
SHOPPING_DIR="$WORKSPACE_DIR/shopping-lists"
ACTIVE_LIST="$SHOPPING_DIR/active.json"
CONFIG_FILE="$SHOPPING_DIR/config.json"
HISTORY_DIR="$SHOPPING_DIR/history"
STATS_DIR="$SHOPPING_DIR/stats"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 初始化目录结构
init_shopping_list() {
    log_info "初始化购物清单目录..."
    mkdir -p "$SHOPPING_DIR"/{history,stats}
    mkdir -p "$WORKSPACE_DIR/skills/shopping-list/templates"

    # 如果不存在 active.json，创建默认文件
    if [[ ! -f "$ACTIVE_LIST" ]]; then
        create_default_active_list
    fi

    # 如果不存在 config.json，创建默认配置
    if [[ ! -f "$CONFIG_FILE" ]]; then
        create_default_config
    fi

    log_success "初始化完成！"
}

# 创建默认清单
create_default_active_list() {
    cat > "$ACTIVE_LIST" << 'EOF'
{
  "version": "1.0",
  "created_at": "#{DATE}",
  "updated_at": "#{DATE}",
  "status": "active",
  "shopping_trip": {
    "planned_date": null,
    "store": null,
    "budget": null
  },
  "budget": {
    "total": 0,
    "spent": 0,
    "remaining": 0
  },
  "items": [],
  "summary": {
    "total_items": 0,
    "pending": 0,
    "purchased": 0,
    "high_priority": 0,
    "estimated_total": 0
  }
}
EOF
    # 替换日期占位符
    local current_date=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")
    sed -i '' "s/#{DATE}/$current_date/g" "$ACTIVE_LIST"
    log_success "已创建默认购物清单"
}

# 创建默认配置
create_default_config() {
    cat > "$CONFIG_FILE" << 'EOF'
{
  "version": "1.0",
  "preferences": {
    "currency": "CNY",
    "date_format": "YYYY-MM-DD",
    "default_store": "超市A",
    "auto_archive_days": 7
  },
  "budget": {
    "monthly_total": 5000,
    "categories": {
      "食品生鲜": 2000,
      "日用品": 1000,
      "电子产品": 1000,
      "服装鞋帽": 1000,
      "其他": 1000
    }
  }
}
EOF
    log_success "已创建默认配置文件"
}

# 添加物品
add_item() {
    local name="$1"
    local quantity="${2:-1}"
    local unit="${3:-件}"
    local category="${4:-其他}"
    local priority="${5:-medium}"
    local store="${6:-默认}"
    local notes="${7:-}"
    local price="${8:-0}"

    log_info "添加物品: $name ($quantity $unit)"

    # 生成唯一ID
    local item_id="item_$(date +%s%N)"

    # 读取当前清单
    local json_content=$(cat "$ACTIVE_LIST")

    # 添加物品（这里需要使用 jq 工具）
    if command -v jq &> /dev/null; then
        # 使用 jq 添加物品
        local current_date=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")
        local new_item=$(cat <<EOF
{
  "id": "$item_id",
  "name": "$name",
  "quantity": $quantity,
  "unit": "$unit",
  "category": "$category",
  "subcategory": "",
  "priority": "$priority",
  "status": "pending",
  "estimated_price": $price,
  "actual_price": null,
  "store": "$store",
  "tags": [],
  "notes": "$notes",
  "created_at": "$current_date"
}
EOF
)
        # 使用 jq 添加到数组
        jq --argjson new_item "$new_item" \
           '.items += [$new_item] |
            .summary.total_items += 1 |
            .summary.pending += 1 |
            if ($new_item.priority == "high") then .summary.high_priority += 1 else . end |
            .updated_at = "'$current_date'"' \
           "$ACTIVE_LIST" > "$ACTIVE_LIST.tmp" && \
        mv "$ACTIVE_LIST.tmp" "$ACTIVE_LIST"

        log_success "物品已添加: $name (ID: $item_id)"
    else
        log_warning "未安装 jq 工具，使用基础文本处理..."
        # 这里可以添加不使用 jq 的处理逻辑
        log_error "请安装 jq: brew install jq"
        return 1
    fi
}

# 查看清单
list_items() {
    local filter_category="${1:-}"
    local filter_priority="${2:-}"
    local filter_status="${3:-}"

    log_info "购物清单:"

    if [[ ! -f "$ACTIVE_LIST" ]]; then
        log_warning "清单文件不存在"
        return 1
    fi

    if command -v jq &> /dev/null; then
        # 使用 jq 格式化输出
        jq -r '
            .items[] |
            select((.category == "'"$filter_category"'" or "'"$filter_category"'" == "") and
                   (.priority == "'"$filter_priority"'" or "'"$filter_priority"'" == "") and
                   (.status == "'"$filter_status"'" or "'"$filter_status"'" == "")) |
            "\(.name)\t\(.quantity) \(.unit)\t\(.category)\t\(.priority)\t\(.status)"
        ' "$ACTIVE_LIST" | column -t -s $'\t'
    else
        log_warning "未安装 jq 工具"
        cat "$ACTIVE_LIST"
    fi
}

# 更新物品
update_item() {
    local item_id="$1"
    local field="$2"
    local value="$3"

    log_info "更新物品 $item_id 的 $field 为 $value"

    if command -v jq &> /dev/null; then
        local current_date=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")
        jq --arg id "$item_id" \
           --arg field "$field" \
           --arg value "$value" \
           '(.items[] | select(.id == $id) | .[$field]) = $value |
            .updated_at = "'$current_date'"' \
           "$ACTIVE_LIST" > "$ACTIVE_LIST.tmp" && \
        mv "$ACTIVE_LIST.tmp" "$ACTIVE_LIST"

        log_success "物品已更新"
    else
        log_error "请安装 jq: brew install jq"
        return 1
    fi
}

# 删除物品
delete_item() {
    local item_id="$1"

    log_info "删除物品: $item_id"

    if command -v jq &> /dev/null; then
        local current_date=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")
        jq --arg id "$item_id" \
           'del(.items[] | select(.id == $id)) |
            .updated_at = "'$current_date'"' \
           "$ACTIVE_LIST" > "$ACTIVE_LIST.tmp" && \
        mv "$ACTIVE_LIST.tmp" "$ACTIVE_LIST"

        log_success "物品已删除"
    else
        log_error "请安装 jq: brew install jq"
        return 1
    fi
}

# 结账归档
checkout() {
    local actual_spent="${1:-0}"

    log_info "结账归档: ¥$actual_spent"

    if command -v jq &> /dev/null; then
        # 读取当前清单
        local current_date=$(date +"%Y-%m-%d")
        local history_file="$HISTORY_DIR/$current_date.json"

        # 创建历史记录
        jq --argjson spent "$actual_spent" \
           '.shopping_trip.date = "'$current_date'" |
            .shopping_trip.completed = true |
            .budget.actual = $spent |
            .budget.saved = (.budget.total - $spent)' \
           "$ACTIVE_LIST" > "$history_file"

        # 清空当前清单
        jq '.items = [] |
            .summary.total_items = 0 |
            .summary.pending = 0 |
            .summary.purchased = 0 |
            .summary.high_priority = 0 |
            .budget.spent = 0 |
            .budget.remaining = .budget.total |
            .summary.estimated_total = 0 |
            .updated_at = "'$(date -u +"%Y-%m-%dT%H:%M:%S+08:00")'"' \
           "$ACTIVE_LIST" > "$ACTIVE_LIST.tmp" && \
        mv "$ACTIVE_LIST.tmp" "$ACTIVE_LIST"

        log_success "结账完成，已归档到: $history_file"
    else
        log_error "请安装 jq: brew install jq"
        return 1
    fi
}

# 统计报告
show_stats() {
    log_info "购物统计:"

    if [[ ! -f "$ACTIVE_LIST" ]]; then
        log_warning "清单文件不存在"
        return 1
    fi

    if command -v jq &> /dev/null; then
        echo ""
        echo "=== 当前清单概览 ==="
        jq -r '
            "总物品数: \(.summary.total_items)
待购买: \(.summary.pending)
已购买: \(.summary.purchased)
高优先级: \(.summary.high_priority)
预估总价: ¥\(.summary.estimated_total)"
        ' "$ACTIVE_LIST"

        echo ""
        echo "=== 预算状态 ==="
        jq -r '
            "总预算: ¥\(.budget.total)
已花费: ¥\(.budget.spent)
剩余: ¥\(.budget.remaining)"
        ' "$ACTIVE_LIST"

        echo ""
        echo "=== 分类统计 ==="
        jq -r '
            .items |
            group_by(.category) |
            .[] |
            "类别: \(.[0].category) | 数量: \(length)"
        ' "$ACTIVE_LIST"
    else
        log_warning "未安装 jq 工具"
        cat "$ACTIVE_LIST"
    fi
}

# 帮助信息
show_help() {
    cat << EOF
购物清单管理工具

用法:
  $0 <command> [arguments]

命令:
  init                          初始化购物清单系统
  add <name> [qty] [unit]       添加物品
  list [category] [priority]    查看清单
  update <id> <field> <value>   更新物品
  delete <id>                   删除物品
  checkout [amount]             结账归档
  stats                         统计报告
  help                          显示帮助

示例:
  $0 init
  $0 add "牛奶" 2 "盒" "食品生鲜" "high" "超市A" "特仑苏" 20
  $0 list
  $0 update item_001 quantity 3
  $0 delete item_001
  $0 checkout 185.5
  $0 stats

注意: 需要安装 jq 工具
  brew install jq
EOF
}

# 主程序
main() {
    local command="${1:-help}"

    case "$command" in
        init)
            init_shopping_list
            ;;
        add)
            shift
            add_item "$@"
            ;;
        list)
            shift
            list_items "$@"
            ;;
        update)
            shift
            update_item "$@"
            ;;
        delete)
            shift
            delete_item "$@"
            ;;
        checkout)
            shift
            checkout "${1:-0}"
            ;;
        stats)
            show_stats
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 执行主程序
main "$@"
