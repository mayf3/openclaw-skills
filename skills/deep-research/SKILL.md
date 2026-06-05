---
name: deep-research
description: |
  深度研究，支持三种后端：ChatGPT Deep Research（浏览器）、Gemini Deep Research（浏览器）、DDG 纯搜索（无需浏览器）。

  Use when:
  (1) 需要深度调研、综合分析、多源对比
  (2) 用户提到 "deep research"、"深度研究"、"调研报告"
  (3) 简单搜索搞不定、需要 30+ 分钟深挖的主题
  (4) "compare X vs Y"、"analyze trends"、"state of the art"

  NOT for: 简单查询、debugging、1-2 次搜索能回答的问题。

  Backends:
  - chatgpt: Brave CDP + ChatGPT (需 Plus/Team 订阅)
  - gemini: Brave CDP + Gemini (需 Advanced 订阅或免费快速模式)
  - ddgs: 纯 DuckDuckGo 搜索 (无需付费，5-10 分钟出结果)

  Requires (browser backends): Brave Browser on --remote-debugging-port=9222, Python 3, websockets.
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      tools: ["python3.12"]
---

# Deep Research 🔬

统一深度研究框架，根据场景自动选择后端。

## 后端选择决策树

```
用户请求深度研究
├── Brave 浏览器可用 (9222 端口)?
│   ├── 用户指定了后端?
│   │   ├── "用 ChatGPT" → references/chatgpt.md
│   │   ├── "用 Gemini" → references/gemini.md
│   │   └── 自动选择:
│   │       ├── 学术/技术主题 → gemini（文档生成更结构化）
│   │       ├── 商业/市场分析 → chatgpt（综合分析更强）
│   │       └── 都可以 → gemini（免费快速模式更省配额）
│   └── 浏览器不可用 → references/ddgs.md（降级）
└── 无浏览器 → references/ddgs.md
```

## 研究模式

| 模式 | 后端 | 时长 | 适用 |
|------|------|------|------|
| **快速** | ddgs | 5-10 min | 初步探索、不需要 AI 辅助 |
| **标准** | chatgpt/gemini | 30-60 min | 大多数研究任务 |
| **深度** | chatgpt/gemini | 60-90 min | 关键决策、需要极高可信度 |

**默认假设**：技术问题 = 技术受众。对比 = 平衡视角。趋势 = 近 1-2 年。

## 公共流程（所有后端共享）

### Phase 1: SCOPE（确定范围）

- 理解用户真正想知道什么
- 确定研究边界（时间、领域、深度）
- 选择模式和后端

### Phase 2: PLAN（规划）

- 将主题拆分为 3-5 个研究子问题
- 确定关键词策略
- 确定目标来源类型（学术/官方/媒体/社区）

### Phase 3-5: RETRIEVE → TRIANGULATE → SYNTHESIZE

**具体操作按后端 reference 执行：**
- 浏览器后端（ChatGPT/Gemini）：加载 [chatgpt.md](./references/chatgpt.md) 或 [gemini.md](./references/gemini.md)
- DDG 后端：加载 [ddgs.md](./references/ddgs.md)

**通用原则：**
- 每个主要声明至少 3 个来源支撑
- 优先 Tier 1-2 来源（论文/政府/权威媒体）
- 交叉验证是底线

### Phase 6: PACKAGE（输出）

**输出文件结构（长报告）**：
```
reports/YYYY-MMDD-[topic]/
├── README.md              # 元信息
├── 00-executive-summary.md # 300字摘要
├── 01-top-picks.md        # Top 3 方案（如适用）
├── 02-deep-dive.md        # 完整分析
└── raw/                   # 原始数据
```

**报告质量标准：**
- Executive Summary（200-400 字）
- 每个主要发现 600-2000 字，附引用
- 所有声明标注来源 [N]
- 无占位符、无捏造引用

**交付方式：**
- 短报告：直接在聊天中输出
- 长报告：输出摘要 + 关键结论，提供完整报告路径

## 后端 Reference 文件

| 文件 | 内容 |
|------|------|
| [chatgpt.md](./references/chatgpt.md) | ChatGPT Deep Research CDP 操作流程 |
| [gemini.md](./references/gemini.md) | Gemini Deep Research CDP 操作流程 |
| [ddgs.md](./references/ddgs.md) | DDG 纯搜索流程（含 ddgs_search.py 命令） |
| [methodology.md](./references/methodology/methodology.md) | 研究方法论（6 阶段流水线） |
| [quality-gates.md](./references/methodology/quality-gates.md) | 质量检查标准 |
| [report-assembly.md](./references/methodology/report-assembly.md) | 报告组装指南 |

## 活跃脚本

```bash
# CDP 浏览器控制（共享自 brave-browser-agent）
python3 {{SKILL_DIR}}/scripts/cdp_exec.py [open|eval|screenshot|list|navigate] ...

# CDP 状态诊断（共享自 brave-browser-agent）
python3 {{SKILL_DIR}}/scripts/check_cdp.py
python3 {{SKILL_DIR}}/scripts/check_cdp.py --quick    # 快速检查
python3 {{SKILL_DIR}}/scripts/check_cdp.py --json     # JSON 输出

# 来源可信度评估
python3 {{SKILL_DIR}}/scripts/source_evaluator.py --url "https://..."

# 报告验证
python3 {{SKILL_DIR}}/scripts/validate_report.py --report [path]
python3 {{SKILL_DIR}}/scripts/validate_report.py --report [path] --quiet  # 只显示摘要
python3 {{SKILL_DIR}}/scripts/verify_citations.py --report [path]
python3 {{SKILL_DIR}}/scripts/verify_citations.py --report [path] --quiet  # 只显示摘要
python3 {{SKILL_DIR}}/scripts/verify_citations.py --report [path] --strict  # 严格模式：任何可疑即失败

# Markdown → HTML
python3 {{SKILL_DIR}}/scripts/md_to_html.py [markdown_path] [-o output.html] [--full]

# 测试（对 test fixtures 运行 validate_report.py）
python3 {{SKILL_DIR}}/tests/run_tests.py
python3 {{SKILL_DIR}}/tests/run_tests.py -v   # 详细输出
python3 {{SKILL_DIR}}/tests/run_tests.py --ci # CI 模式（失败退出 1）
```

> **脚本说明**：
> - `cdp_exec.py` 和 `check_cdp.py` 是共享自 brave-browser-agent 的符号链接，保持单一维护点
> - `check_brave.py` 已移除（被 `check_cdp.py` 替代，功能更全面）
> - 未使用的旧脚本已移至 `scripts/legacy/`（research_engine.py、citation_manager.py、verify_html.py、shell 脚本）

## 模板

- 报告结构：[report_template.md](./templates/report_template.md)
- HTML 样式：[mckinsey_report_template.html](./templates/mckinsey_report_template.html)

## When to Use / NOT Use

**Use:** 深度分析、技术对比、前沿综述、多视角调查、市场分析、需要 30+ 分钟的研究。

**Do NOT use:** 简单查询、debugging、1-2 次搜索能回答的问题、实时性要求极高的查询。

## 限制

1. 浏览器后端需要 Brave 运行在 9222 端口 + 对应平台已登录
2. ChatGPT 需要 Plus/Team 订阅，Gemini 需要 Advanced 或免费快速模式
3. 研究时间较长（浏览器后端 30-90 分钟，DDG 5-10 分钟）
4. 浏览器后端需要稳定网络访问对应平台

## 更新日志

详见 [changelog.md](./changelog.md)
