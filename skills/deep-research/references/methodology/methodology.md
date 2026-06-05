# Deep Research Methodology（OpenClaw 版）

6 阶段流水线：SCOPE → PLAN → RETRIEVE → TRIANGULATE → SYNTHESIZE → PACKAGE

---

## Phase 1: SCOPE（确定范围）

- 理解用户真正想知道什么
- 拆分为 3-5 个研究子问题
- 确定边界（时间范围、领域、深度等级）
- 选择后端（chatgpt/gemini/ddgs）和模式（快速/标准/深度）

## Phase 2: PLAN（规划）

- 为每个子问题设计 2-3 个搜索关键词变体
- 确定目标来源类型（学术/官方/媒体/社区）
- 规划工具链：DDGS 搜索 → 全文提取 → 交叉验证

## Phase 3: RETRIEVE（检索）

**按后端执行，通用工具链如下：**

### DDGS 搜索（smart-search skill）

```bash
# 多后端搜索
python3 <smart-search-dir>/scripts/ddgs_search.py "query" --backend brave --fallback yandex,yahoo,bing

# 新闻搜索
python3 <smart-search-dir>/scripts/ddgs_search.py "query" --type news --backend bing

# 全文提取
python3 <smart-search-dir>/scripts/ddgs_search.py --extract-url "https://example.com/article"

# 多类型并行
python3 <smart-search-dir>/scripts/ddgs_search.py "query" --type all

# 批量搜索
python3 <smart-search-dir>/scripts/ddgs_search.py --batch-file queries.txt --fallback yandex,yahoo,bing
```

### 网页内容提取

```bash
# web_fetch（静态页面，50KB 限制）
web_fetch({"url": "https://...", "maxChars": 5000})

# DDGS extract()（更快，一站式，推荐优先用）
python3 <smart-search-dir>/scripts/ddgs_search.py --extract-url "https://..."
```

### 浏览器后端（ChatGPT/Gemini）

按照 `references/chatgpt.md` 或 `references/gemini.md` 执行 CDP 操作流程。

### 子问题分工

复杂研究可用 `sessions_spawn` 启动子 agent 并行处理不同子问题：
- 子 agent A：技术实现分析
- 子 agent B：市场/行业数据
- 子 agent C：学术前沿综述

**来源目标**：
- 快速模式：10+ 来源
- 标准模式：15-20 来源
- 深度模式：25+ 来源

## Phase 4: TRIANGULATE（交叉验证）

- 每个核心声明至少 2 个独立来源确认
- 矛盾来源如实报告，不选择性采信
- 来源可信度分级：Tier 1（论文/政府/权威媒体）→ Tier 5（匿名论坛）
- 仅一个来源的说法标注为"未验证"

**SIFT 四步法**：Stop → Investigate source → Find better coverage → Trace to original

## Phase 5: SYNTHESIZE（综合）

- 事实卡片法：每条关键声明 = 内容 + 来源 + 层级 + 时间
- 推导链透明："事实 A → 事实 B → 对比 → 结论"
- 承认信息空白，不强凑
- 区分事实与观点

## Phase 6: PACKAGE（输出）

短报告直接在聊天中输出。长报告按 SKILL.md 定义的目录结构输出。

**质量标准**：
- 每个主要声明有来源支撑 [N]
- 无占位符、无捏造引用
- 散文优先（≥80%），列表少用
- 时效性标注日期

---

## 搜索策略备忘

| 搜索目标 | 首选 | 备选 |
|---------|------|------|
| 英文技术 | DDGS brave | 360 |
| 学术论文 | Google Scholar | Semantic Scholar |
| 中文深度 | 搜狗微信 | 百度 |
| 最新新闻 | DDGS news | web_fetch reuters.com |
| 用户评价 | site:reddit.com | Hacker News |
| 代码实现 | grep.app | GitHub |

**已知问题**：
- Bing CN 英文搜索有关键词碰撞，英文用 DDGS brave 或 360
- brave 后端连续 4-5 次后可能空返回，批量用 yandex 更稳
- `after:YYYY-MM-DD` 在 Bing/360 已验证有效

## 来源评估

用 `scripts/source_evaluator.py` 对来源打分（0-100）：
```bash
python3 {{SKILL_DIR}}/scripts/source_evaluator.py --url "https://..."
```

关键维度：权威性、时效性、可验证性、偏见倾向。

---

*旧版方法论（含 Claude Code Task tool / WebSearch / Exa MCP 内容）已归档至 `legacy/` 目录。*
