# DALL-E 3 & Flux Prompt 特化指南

## DALL-E 3

### 特点

- **自然语言优先** — 最好写完整的英语段落，不需要关键词堆叠
- **不支持负面提示词** — 用正面引导替代："请确保不出现文字和水印"
- **不支持权重语法** — 没有 `--` 参数，没有 `::` 分隔
- **自动处理比例** — 指定即可，如 "a 16:9 image of..."
- **最长 prompt** — 可以写很长（400+ 词），是三大平台中最能吃 prompt 的
- **理解中文** — 可以直接写中文，但英文效果更好

### 最佳实践

**简洁版**（推荐）：
```
Create a photorealistic image of a young woman in a traditional Chinese hanfu
playing a guzheng under a cherry blossom tree. Soft golden hour light filtering
through petals. Cinematic composition with warm tones. 16:9 aspect ratio.
```

**详细版**（DALL-E 3 能处理）：
```
A professional fashion photograph of a young East Asian woman with long black hair
wearing a flowing silk red dress, standing confidently on a misty city rooftop at
golden hour. Warm sunlight catches her hair and creates a soft rim light on her
silhouette. The background shows a modern cityscape with skyscrapers fading into
fog. Shot on medium format film, natural skin texture visible, slightly candid
pose with a subtle smile. The atmosphere is elegant and contemplative. Rich warm
colors with cool blue tones in the shadows. 4:3 aspect ratio.
```

### 注意事项

| 不要 | 要 |
|------|-----|
| `--ar 16:9` | "a 16:9 image" |
| `(masterpiece:1.2)` | "award-winning composition" |
| `--no text` | "without any text or watermark" |
| "perfect flawless skin" | "realistic skin with natural texture" |

### 写实类（去 OpenAI 安全限制）

DALL-E 3 有比较严格的安全限制。绕过技巧：
- 用 "photograph" 替代 "naked"/"scantily clad"
- 用 "fashion photography" 替代 "seductive"
- 明确写 "21 years old" 表明是成年人
- 用艺术风格包装：`a classical painting of...`

---

## Flux (Black Forest Labs)

### 特点

- **MJ-like 语法** — 类似 Midjourney 的自然语言风格
- **高关键词密度** — 比 MJ 更能吃关键词，可以写更多细节
- **无参数** — 没有 `--ar` `--s` 等参数（类似 DALL-E）
- **强写实能力** — Flux.1 Pro/Dev 的写实能力是当前最强的
- **弱文字生成** — 文字依然不可靠

### Prompt 结构建议

**Flux 推荐风格**：
```
[详细的主体描述]，[详细的环境描述]，[光线和色彩]，[构图视角]，[画质和要求]
```

**示例 - 写实人像**：
```
Cinematic portrait of a middle-aged Japanese chef with salt-and-pepper beard,
wearing a traditional white chef coat, standing in a warm-lit professional kitchen
at night. Steam rising from a pot. Rembrandt lighting, shallow depth of field,
intense focus on eyes, subtle smile lines. Shot on Leica M11, natural skin
texture, film-like grain. Photorealistic, 8K.
```

**示例 - 产品摄影**：
```
Professional studio product photograph of a matte black espresso machine,
elegant minimalist design, brushed metal accents, placed on a rustic wooden
countertop. Golden hour light streaming through window creating long shadows.
A small ceramic cup with foam art nearby. Shallow depth of field, commercial
photography style, warm tone, ultra-detailed surface texture. 8K.
```

### 与 MJ 的对比

| 维度 | Flux | Midjourney |
|------|------|-----------|
| 写实能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 风格多样性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| prompt 理解 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 参数控制 | ❌ | ✅ (`--ar`, `--s`, `--no`) |
| 文字生成 | ⭐⭐ | ⭐⭐⭐ |
| 输入图像（垫图） | ❌ | ✅ |
| 负面提示词 | ❌ | ✅ (`--no`) |
