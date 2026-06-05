---
name: image-prompt-engineer
description: >
  图像生成提示词（Prompt）工程师技能。为 Midjourney、Stable Diffusion、DALL-E 3、Flux 等主流 AI 图像生成平台
  编写、优化、翻译高质量的提示词。使用场景包括：(1) 用户需要生成图片但不知道怎么写 prompt；
  (2) 需要优化/润色现有提示词；(3) 需要将中文需求翻译成英文 prompt；
  (4) 需要转换 prompt 在不同平台之间（MJ ↔ SD ↔ DALL-E）；
  (5) 需要针对特定风格（写实/动漫/3D/像素/水墨等）生成 prompt。
  Not for: 实际调用图像生成 API（那是 image-gen skill 的职责）、图片分析/反推提示词（那是 ai-image-prompt skill 的职责）。
---

# Image Prompt Engineer

图像生成提示词工程师。帮助你编写面向 Midjourney / Stable Diffusion / DALL-E 3 / Flux 等平台的高质量提示词。

## 快速导航

- **通用提示词架构** → 见 `references/prompt-structure.md`
- **Midjourney 特化** → 见 `references/midjourney.md`（参数、风格化、垫图）
- **Stable Diffusion 特化** → 见 `references/stable-diffusion.md`（Checkpoint、LoRA、负面提示词）
- **DALL-E 3 / Flux 特化** → 见 `references/dalle-flux.md`
- **负面提示词库** → 见 `references/negative-prompts.md`
- **风格词汇库** → 见 `references/style-library.md`

## 使用流程

### Step 1: 确定用户意图

| 意图 | 用户表述 | 处理方式 |
|------|----------|----------|
| **新生成** | "帮我写一个...prompt" / "我想生成..." | 进入 Step 2 |
| **优化** | "帮我优化这个prompt" / "让它更真实" | 进入 Step 3 |
| **翻译** | "翻译成英文prompt" / "中译英" | 进入 Step 4 |
| **跨平台转换** | "帮我转成Midjourney格式" / "这个SD prompt怎么用在MJ" | 进入 Step 5 |

### Step 2: 编写新 Prompt

按以下结构组织（可省略不适用部分）：

```
[主体(subject)] + [动作/状态(action/state)] + [环境(environment)] +
[光照(lighting)] + [构图(composition)] + [风格(style)] + [画质(quality)]
```

**中文需求 → 英文 Prompt 三步法：**

1. **拆要素**：主体 → 动作 → 环境 → 光照 → 构图 → 风格 → 画质
2. **加修饰**：每要素加 1-2 个修饰词（颜色/材质/情绪/氛围）
3. **按平台调整**：MJ 用自然语言逗号分隔，SD 用关键词堆叠

### Step 3: 优化现有 Prompt

评估维度及改进方向：

| 维度 | 问题 | 改进方法 |
|------|------|----------|
| **清晰度** | 主体模糊 | 加具体描述（年龄/发型/服装/表情） |
| **真实感** | AI 感强 | 加皮肤纹理/自然瑕疵/柔光; 删 perfect/flawless |
| **构图** | 主体位置不佳 | 加视角（低角/航拍/微距/广角）和景别（特写/中景/全景） |
| **光线** | 光影平淡 | 加光源类型（黄金时刻/柔光箱/侧逆光/霓虹） |
| **风格一致性** | 风格混杂 | 限 1-2 种风格关键词 |
| **负面提示词** | 出现伪影 | 加对应负面词 |

### Step 4: 中译英 Prompt

翻译原则：
- **MJ/DALL-E**: 自然英语句子，逗号分隔关键要素
- **SD/Flux**: 关键词堆叠，逗号分隔，权重用 `(word:1.2)` 或 `word++`
- **保留数字/参数**：宽高比 `--ar 16:9`、风格化 `--s 250` 等不要翻译

### Step 5: 跨平台转换

| 平台 | 特点 | 转换要点 |
|------|------|----------|
| **MJ→SD** | 长句→堆叠词 | 拆成关键词，加负面词，加 CFG 推荐值 |
| **SD→MJ** | 堆叠词→自然句 | 合并成通顺句子，去权重符号，调低风格化值 |
| **MJ→DALL-E** | 去参数 | 去掉 `--ar` `--s` `--v` 等参数，DALL-E 自动处理 |
| **MJ→Flux** | 类似 MJ | 可保留大部分格式，Flux 更吃关键词密度 |

## 安全边界

- 不生成 NSFW/暴力/政治敏感内容
- 不冒充特定真人形象
- 不生成仿冒品牌/版权内容
- 涉及人物肖像时注明"是 AI 生成的艺术作品"

---

*查看 references/ 下的专文件获取各平台深度指南。*
