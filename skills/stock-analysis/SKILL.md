---
name: stock-analysis
description: 四维度价值投资分析系统（财务质量30%、估值30%、护城河25%、管理层15%）。当需要分析单只股票、生成价值投资报告、计算四维度评分、给出投资建议时使用。激活条件：用户提及股票分析、价值投资、投资建议、股票评分、ROE筛选、财报分析。提供100分制量化评分和明确投资建议（≥90强烈买入、80-89买入、70-79观望、60-69谨慎、低于60回避）。
metadata:
  openclaw:
    emoji: 📊
---

# Stock Analysis

四维度价值投资分析系统，100分制量化评分 + 明确投资建议。

## 评分体系

| 维度 | 权重 | 核心指标 |
|------|------|----------|
| 财务质量 | 30% | ROE≥15%、毛利率≥30%、现金流/净利润≥1.0、ROA≥8% |
| 估值 | 30% | PE-TTM≤30、PB≤5、PEG≤1.5 |
| 护城河 | 25% | 品牌、成本优势、网络效应、转换成本、专利壁垒 |
| 管理层 | 15% | 分红率≥30%、透明度、战略执行 |

### 投资建议

| 评分 | 建议 | 标识 |
|------|------|------|
| ≥90 | 强烈买入 | 🔴 |
| 80-89 | 买入 | 🟠 |
| 70-79 | 观望 | 🟡 |
| 60-69 | 谨慎 | 🟢 |
| <60 | 回避 | ⚪ |

## 工作流程

### 1. 前置检查

- 确认股票在 PROGRESS.md 中为⏳待分析状态
- 检查 `stocks/{代码}-{名称}/reports/价值投资分析.md` 是否已存在

### 2. 获取财务数据

数据源优先级：东方财富API > 腾讯API > 新浪API（已失效）

必需字段：ROE、毛利率、PE-TTM、PB、现金流/净利润、分红率

存储到 `data/metadata.json`

### 3. 四维度评分

详细评分标准见 [references/scoring-criteria.md](references/scoring-criteria.md)。

### 4. 生成报告

使用模板 [references/report-template.md](references/report-template.md)：

```bash
# 验证报告结构
python3 scripts/validate_structure.py ~/workspace/blog/knowledge-base/docs/投资分析/stocks/{代码}-{名称}
```

### 5. 更新进度

更新 PROGRESS.md 对应行：状态→✅已完成、评分、报告日期。

## 报告目录结构

```
~/workspace/blog/knowledge-base/docs/投资分析/stocks/
├── 600519-贵州茅台/
│   ├── data/metadata.json
│   └── reports/价值投资分析.md
└── ...
```

## 关键脚本

| 脚本 | 用途 |
|------|------|
| `scripts/validate_structure.py` | 报告结构验证 |
| `scripts/validate_structure_v2.py` | 增强验证 |
| `scripts/validate_structure_v3.py` | 完整验证（推荐） |
| `scripts/filter_stocks_by_roe_v3.py` | ROE筛选 |
| `scripts/migrate_metadata.py` | 元数据迁移 |
| `scripts/version_manager.py` | 版本管理 |

## 注意事项

- 分析基于价值投资理念，不适用短线投机
- 安全边际优先：价格高于价值时观望
- 护城河是核心竞争力
- 分红率反映管理层诚信
- 生成报告后必须运行验证脚本
