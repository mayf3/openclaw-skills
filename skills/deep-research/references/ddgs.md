# DDG 纯搜索后端（无需浏览器）

使用 DuckDuckGo 搜索进行多源深度研究，不需要浏览器或付费订阅。

## 适用场景

- 没有 Brave 浏览器可用时
- 不需要 AI 辅助分析，只需要多源搜索+人工综合
- 快速研究（5-10 分钟出结果）
- 作为浏览器后端的降级方案

## 前置条件

- `smart-search` skill 已安装（提供 `ddgs_search.py`）
- 无需 API Key、无需浏览器

> **关于路径 `<smart-search-dir>`**：这是 smart-search skill 目录的绝对路径。
> 实际使用时可用 `{{smart_search_skill_dir}}` 或在当前 agent 的 workspace 中搜索 `ddgs_search.py`。
> 典型路径：`smart-search/scripts/ddgs_search.py`

## 流程

### 1. 规划研究（拆分子问题）

将主题拆分为 3-5 个研究子问题：

```
主题: "AI 对医疗的影响"
子问题:
  1. AI 在医疗中的主要应用有哪些？
  2. 有哪些临床效果数据？
  3. 监管挑战是什么？
  4. 领先公司有哪些？
  5. 市场规模和增长？
```

### 2. 多源搜索

**搜索脚本**（smart-search skill 提供）：

```bash
# 基础搜索（brave 后端，英文首选）
python3 <smart-search-dir>/scripts/ddgs_search.py "AI healthcare clinical outcomes 2025" --backend brave

# 中文搜索（bing 后端）
python3 <smart-search-dir>/scripts/ddgs_search.py "AI 医疗临床效果数据 2025" --backend bing

# 新闻搜索
python3 <smart-search-dir>/scripts/ddgs_search.py "AI healthcare breakthrough" --type news --backend brave

# 多类型并行搜索（text + news + videos）
python3 <smart-search-dir>/scripts/ddgs_search.py "AI healthcare market size" --type all

# 降级链（brave 失败时自动尝试 yandex → yahoo → bing）
python3 <smart-search-dir>/scripts/ddgs_search.py "query" --backend brave --fallback yandex,yahoo,bing

# 批量搜索（从文件读取查询）
python3 <smart-search-dir>/scripts/ddgs_search.py --batch-file queries.txt --fallback yandex,yahoo,bing
```

**搜索策略**：
- 目标 15-30 个独立来源
- 优先级：学术/官方/权威媒体 > 博客 > 论坛
- 混合 text + news 搜索
- 英文用 brave，中文用 bing

**垂直搜索**：

```bash
# 学术论文
python3 <smart-search-dir>/scripts/ddgs_search.py "AI radiology diagnosis accuracy site:arxiv.org" --backend brave

# 权威媒体
python3 <smart-search-dir>/scripts/ddgs_search.py "AI healthcare regulation 2025 site:reuters.com OR site:nature.com" --backend brave

# 用户讨论
python3 <smart-search-dir>/scripts/ddgs_search.py "AI doctor experience site:reddit.com" --backend brave

# 时间过滤（Bing/360 有效）
python3 <smart-search-dir>/scripts/ddgs_search.py "AI healthcare after:2025-01-01" --backend bing
```

### 3. 深度阅读关键来源

```bash
# DDGS extract()（推荐，快且稳定）
python3 <smart-search-dir>/scripts/ddgs_search.py --extract-url "https://example.com/article"

# web_fetch（备选，50KB 限制）
web_fetch({"url": "https://example.com/article", "maxChars": 10000})

# 输出格式选择
python3 <smart-search-dir>/scripts/ddgs_search.py --extract-url "https://..." --extract-format text_markdown
```

选 3-5 个关键来源全文阅读，不要只看搜索摘要。

### 4. 综合报告

```markdown
# [主题]: Deep Research Report
*Generated: [date] | Sources: [N] | Confidence: [High/Medium/Low]*

## Executive Summary
[3-5 句核心发现]

## 1. [第一个主题]
- 关键点 ([来源](url)) [T2]
- 支撑数据 ([来源](url)) [T1]

## Key Takeaways
- [洞察 1]
- [洞察 2]

## Sources
1. [标题](url) — [一句话摘要] [T1-T5]
```

## 质量规则

1. **每个声明必须有来源**，无来源的不写入
2. **交叉验证**：仅一个来源的说法标注为"未验证"
3. **时效性**：优先 12 个月内的来源，标注日期
4. **承认空白**：找不到好信息就说"数据不足"
5. **禁止幻觉**：不知道就说不知道
6. **来源层级标注**：[T1] 论文/政府 → [T5] 匿名论坛

## 作为降级方案

当浏览器后端不可用（Brave 未启动、ChatGPT/Gemini 未登录）时，自动切换到此模式：
- 覆盖范围更广但深度较浅
- 不需要任何付费订阅
- 速度更快（5-10 分钟 vs 30-60 分钟）

## 速率控制

- brave 后端连续 4-5 次搜索后可能空返回，批量搜索用 yandex 更稳定
- 间隔 1-2.5 秒随机延迟
- 指数退避：`wait = (2 ** attempt) + random.uniform(0, 1)`
