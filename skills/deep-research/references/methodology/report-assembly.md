# Report Assembly: Progressive File Generation

## Length Requirements by Mode

| Mode | Target Words | Description |
|------|--------------|-------------|
| Quick | 2,000-4,000 | Baseline quality threshold |
| Standard | 4,000-8,000 | Comprehensive analysis |
| Deep | 8,000-15,000 | Thorough investigation |
| UltraDeep | 15,000-20,000+ | Maximum rigor |

---

## Progressive Section Generation

**Core Strategy:** Generate and write each section individually using Write/Edit tools. This allows unlimited report length while keeping each generation manageable.

### Setup

Create output directory and initialize markdown file:

```bash
# Create folder: reports/YYYY-MMDD-[topic]/
mkdir -p reports/YYYY-MMDD-[topic]
```

### Section Generation Loop

**Pattern:** Generate section → Write/Edit to file → Move to next section.
Each Write/Edit call contains ONE section (≤2,000 words per call).

**Track citations across sections** — maintain a running list of all [N] citations used.

**Section sequence:**

1. **Executive Summary** (200-400 words)
2. **Introduction** (400-800 words)
3. **Finding 1-N** (600-2,000 words each)
4. **Synthesis & Insights** (500-1,000 words)
5. **Limitations & Caveats** (300-600 words)
6. **Recommendations** (300-600 words)
7. **Bibliography** (CRITICAL — every [N] must have complete entry)
8. **Methodology Appendix** (optional, 200-400 words)

### Citation Tracking

Update citation state after each section. Track as:

```
[N] Author/Org (Year). "Title". Publication. URL
```

**Zero tolerance for:**
- Ranges (`[3-50]`)
- Placeholders (`Additional citations`, `...continue...`)
- Truncation (stopping at 10 when 30 cited)

---

## File Organization

**Directory structure:**
```
reports/YYYY-MMDD-[topic]/
├── README.md              # 元信息
├── 00-executive-summary.md
├── 01-top-picks.md        # Top 3 方案（如适用）
├── 02-deep-dive.md
└── raw/                   # 原始数据
```

**File naming:** All files use same base name with date prefix.

---

## Word Count Per Section

**No single Edit call should exceed 2,000 words.**

Example: 10 findings × 1,500 words = 15,000 words total
- Each Edit call: 1,500 words (under limit)
- File grows to 15,000 words progressively

---

*旧版含 Claude Code 专用路径和 token 限制的内容已在 2026-05-28 清理。*
