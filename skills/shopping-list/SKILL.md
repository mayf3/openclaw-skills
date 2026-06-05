---
name: shopping-list
description: Persistent shopping list management for AI agents. Supports add/edit/delete items,
  budget tracking, category/store organization, and history. Use when tracking shopping needs,
  managing grocery lists, or organizing purchases by store/priority.
---

# 购物清单管理技能

## 技能说明

这是一个完整的购物清单管理技能，提供增删查改的核心功能。

## 功能特性

### 📝 基础操作
- ➕ **添加物品**: 快速记录购物需求
- 📋 **查看清单**: 按分类/优先级/商店展示
- ✏️ **编辑物品**: 修改数量、优先级等
- ❌ **删除物品**: 移除已购或不需要的物品
- ✅ **标记完成**: 标记物品为已购买

### 💰 预算管理
- 📊 **预算设定**: 设定总预算和分类预算
- 💵 **花费跟踪**: 实时记录购物花费
- 📉 **预算预警**: 超预算提醒
- 📈 **统计分析**: 月度消费报告

### 🔔 智能提醒
- ⏰ **定期提醒**: 每周购物提醒
- 📅 **临期提醒**: 易腐食品提前提醒
- 🔄 **智能补充**: 根据使用频率预测需求

## 命令接口

### 添加物品
```
/sl add <物品名> [数量] [单位]
  [--category <分类>]
  [--priority <优先级>]
  [--store <商店>]
  [--notes <备注>]
  [--price <预估价格>]

示例：
/sl add 牛奶 2盒 --category 食品生鲜 --priority high
/sl add 抽纸 1包 --category 日用品 --priority medium --notes 清风
```

### 查看清单
```
/sl list
  [--category <分类>]
  [--priority <优先级>]
  [--store <商店>]
  [--status <状态>]

示例：
/sl list --category 食品生鲜
/sl list --priority high
/sl list --status pending
```

### 更新物品
```
/sl update <物品ID>
  [--quantity <数量>]
  [--priority <优先级>]
  [--price <价格>]
  [--notes <备注>]

示例：
/sl update item_001 --quantity 3
/sl update item_002 --priority high
```

### 删除物品
```
/sl delete <物品ID>

示例：
/sl delete item_001
```

### 结账
```
/sl checkout [--spent <实际花费>]

示例：
/sl checkout --spent 185.5
```

### 统计报告
```
/sl stats
  [--period <周期>]
  [--category <分类>]

示例：
/sl stats
/sl stats --period month
/sl stats --category 食品生鲜
```

## 数据结构

### 物品对象
```json
{
  "id": "item_001",
  "name": "牛奶",
  "quantity": 2,
  "unit": "盒",
  "category": "食品生鲜",
  "subcategory": "肉禽蛋奶",
  "priority": "high",
  "status": "pending",
  "estimated_price": 20,
  "actual_price": null,
  "store": "超市A",
  "tags": ["日常", "急用"],
  "notes": "特仑苏",
  "created_at": "2026-03-14T20:00:00+08:00"
}
```

### 状态值
- `pending`: 待购买
- `purchased`: 已购买
- `cancelled`: 已取消

### 优先级
- `high`: 高优先级（紧急）
- `medium`: 中优先级（重要）
- `low`: 低优先级（普通）

## 目录结构

```
<your-workspace-path>/
├── shopping-lists/
│   ├── active.json              # 当前待购清单
│   ├── config.json              # 配置文件
│   ├── history/                 # 历史记录
│   └── stats/                   # 统计数据
└── skills/
    └── shopping-list/
        └── SKILL.md             # 技能文档
```

## 使用示例

### 场景1: 日常购物
```bash
# 1. 添加物品
/sl add 牛奶 2盒 --category 食品 --priority high
/sl add 鸡蛋 1盒 --category 食品 --priority high
/sl add 抽纸 1包 --category 日用 --priority medium

# 2. 查看清单
/sl list

# 3. 购物后结账
/sl checkout --spent 55
```

### 场景2: 预算管理
```bash
# 1. 查看预算
/sl stats

# 2. 按分类查看
/sl stats --category 食品生鲜

# 3. 月度报告
/sl stats --period month
```

### 场景3: 智能提醒
```bash
# 查看即将到期的物品
/sl list --status expiring

# 查看常购物品
/sl stats --frequent
```

## 注意事项

1. **数据备份**: 历史记录会自动归档，不会丢失
2. **预算控制**: 建议设定合理的预算上限
3. **定期整理**: 及时清理已购物品，保持清单整洁
4. **智能预测**: 系统会学习你的购物习惯，提供智能建议

## 扩展功能

未来可以考虑：
- 📱 与飞书文档集成
- 🛒 与电商平台对接
- 📍 基于位置的提醒
- 👨‍👩‍👧‍👦 多用户协作
- 📸 图片识别添加物品
