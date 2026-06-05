# 图像生成 Prompt Skill — 研究报告

**日期**: 2026-05-21
**执行者**: skill-engineer-agent
**任务**: #66 (研究图像生成prompt的skill并上架技能商城) + #73 (研究图像生成描述词prompt技能，发布到技能商场)

---

## 一、研究结论

### 现有技能调研

在开始研发前，先检查了 workspace 中已有的图像相关技能：

| 技能 | 来源 | 说明 |
|------|------|------|
| **ai-image-prompt** | ClawHub (loveaoui, v1.0.2) | 已安装在 candidate-skills，面向电商场景（模特换装/产品图/海报），含 9500+ 字 SKILL.md + 6 个 ref 文件 |
| gemini-image-gen | ClawHub | Gemini 图像生成工具 |
| gpt-image-gen | ClawHub | GPT 图像生成工具 |
| images-search | ClawHub | 图像搜索 |
| siliconflow-image-gen | ClawHub | SiliconFlow 图像生成 |
| print-image | ClawHub | 打印图像 |

**结论**：存在一个电商场景专用的 prompt skill（ai-image-prompt），但缺少覆盖 Midjourney / Stable Diffusion / DALL-E 3 / Flux 全平台的通用 prompt 技能。

### Prompt Engineering 核心发现

1. **平台差异巨大** — MJ 用自然语言 + 参数，SD 用关键词堆叠 + 权重语法，DALL-E 3 用段落描述，Flux 介于 MJ 和 DALL-E 之间
2. **结构化是王道** — 好的 prompt = 主体 + 动作 + 环境 + 光线 + 构图 + 风格 + 画质
3. **去 AI 感技巧** — 加皮肤纹理/自然瑕疵/真实环境光，删除 perfect/flawless 等空洞词
4. **负面词重要性** — SD/Flux 的负面提示词直接影响出图质量
5. **中文→英文翻译** — 拆要素 → 加修饰 → 按平台调整格式

---

## 二、交付物

### 1. 新技能：image-prompt-engineer（通用图像 prompt 技能）

**位置**: `candidate-skills/skills/image-prompt-engineer/`

**结构**:
```
image-prompt-engineer/
├── SKILL.md                    # 主技能文件（通用工作流）
├── scripts/
│   └── prompt-optimizer.py     # 中文→英文 prompt 转换工具
└── references/
    ├── prompt-structure.md     # 通用 prompt 架构指南
    ├── midjourney.md           # MJ 特化指南（参数/风格/预设）
    ├── stable-diffusion.md     # SD 特化指南（权重/Checkpoint/LoRA）
    ├── dalle-flux.md           # DALL-E 3 & Flux 特化指南
    ├── style-library.md        # 风格词汇库（7大类，80+ 风格词）
    ├── negative-prompts.md     # 负面提示词库（7个分类）
    └── case-studies.md         # 实战案例（5个完整案例）
```

### 2. 激活现有技能：ai-image-prompt

将 ClawHub 安装的 ai-image-prompt（v1.0.2）从 candidate-skills 链接到 active skills/ 目录，使其可被 agent 加载使用。

### 3. 完整覆盖范围

| 平台 | 新技能覆盖 | 旧技能覆盖 |
|------|-----------|-----------|
| Midjourney | ✅ 语法/参数/风格/预设 | ❌ |
| Stable Diffusion | ✅ 权重/Checkpoint/LoRA/负面词 | ❌ |
| DALL-E 3 | ✅ 自然语言/去限制技巧 | ❌ |
| Flux | ✅ MJ-like 语法 | ❌ |
| 电商产品图 | ❌ | ✅ 7种模式 |
| 模特换装 | ❌ | ✅ 完整流程 |
| 去 AI 感 | ✅ 通用技巧 | ✅ 专用指南 |
| 风格迁移 | ✅ 跨平台 | ✅ 7种子类型 |

两个技能互补，不重复。

---

## 三、使用方式

Agent 触发后，根据意图选择：

**新生成图片** → 读 SKILL.md Step 2 → 参考 `references/prompt-structure.md` 写结构 → 参考对应平台指南调整格式

**优化已有 prompt** → 读 SKILL.md Step 3 → 根据评估表逐项改进

**中文→英文** → 读 SKILL.md Step 4 → 三步法翻译

**跨平台转换** → 读 SKILL.md Step 5 → 参考 `references/` 下的转换表

---

## 四、后续建议

1. ✅ 已将 ai-image-prompt 链接到 active skills/（ClawHub 版电商 prompt 技能）
2. ✅ 新 skill image-prompt-engineer 已发布到 candidate-skills（通用 prompt 技能）
3. ✅ 已通过 skill-creator 的 quick_validate 验证
4. ⏳ 建议通知小老师（小花）验收（任务 #74）
5. ⏳ 如需上架 ClawHub，可分配给 open-source-agent 处理
