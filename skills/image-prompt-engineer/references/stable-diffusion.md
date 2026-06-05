# Stable Diffusion Prompt 特化指南

## 基础语法

SD 使用关键词堆叠方式，逗号分隔，支持权重语法。

### 权重控制

| 语法 | 含义 | 示例 |
|------|------|------|
| `(word)` | 权重 ×1.1 | `(masterpiece)` |
| `(word:1.3)` | 权重 ×1.3 | `(intricate details:1.3)` |
| `(word:0.7)` | 权重 ×0.7（降低） | `(background:0.7)` |
| `[word]` | 权重 ×0.9 | `[blurry]` |
| `word++` | A1111 风格 | `masterpiece++` |
| `word + word` | 概念混合 | `cat + dragon` |

### 特定平台的语法差异

| 平台 | 权重语法 | 负面提示词 |
|------|---------|-----------|
| **A1111** | `(word:1.2)` `[word]` | 独立文本框 |
| **ComfyUI** | 同上 | 独立的 CLIP Text Encode |
| **Fooocus** | 同上 | 独立文本框 |
| **Forge** | 同上 | 独立文本框 |

---

## 关键词构成

### 质量标签（前置，权重高）
```
(masterpiece, best quality, ultra-detailed, 8K:1.2)
```

### 主体（中置，权重适中）
```
subject, clothing, action, expression
```

### 环境与风格（后置，权重低）

**场景：**
```
background, environment, lighting, atmosphere
```

**风格：**
```
anime style, photorealistic, oil painting, 3D render, pixel art
```

**艺术家模仿：**
```
style of [artist name], by [artist]
```

### 技术参数

在负面提示词之外，SD 有一些可调整参数：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| CFG Scale | 7-11 | 越低越自由，越高越遵循（>14 容易过饱和） |
| Steps | 20-40 | SDXL 建议 25-35，SD1.5 建议 20-30 |
| Sampler | DPM++ 2M Karras | 出图稳定，通用 |
| | DPM++ SDE Karras | 细节更多，稍慢 |
| | Euler a | 渲染最快，细节稍差 |
| Size | 根据模型 | SDXL → 1024×1024，SD1.5 → 512×512 |

---

## Checkpoint 与 LoRA

### 常用 Checkpoint

| Checkpoint | 擅长 | 推荐场景 |
|-----------|------|----------|
| **Realistic Vision V5.1** | 写实人像 | 真人照片风格 |
| **Juggernaut XL** | 综合写实 | SDXL 全场景 |
| **DreamShaper** | 介于写实与艺术 | 概念艺术 |
| **Counterfeit** | 动漫 | 二次元 |
| **revAnimated** | 2.5D | 半写实半动漫 |

### LoRA 使用

LoRA 格式：`<lora:filename:weight>`

示例：`<lora:add_detail:0.8> <lora:film_grain:0.5>`

常见 LoRA 类型：
- 风格 LoRA（水墨风、赛博朋克）
- 角色 LoRA（特定人物）
- 概念 LoRA（特定材质、构图）
- 增强 LoRA（画质提升、细节增强）

---

## 负面提示词

### 通用负面词
```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit,
fewer digits, cropped, worst quality, low quality, normal quality,
jpeg artifacts, signature, watermark, username, blurry, artist name,
ugly, deformed, extra limbs, fused fingers, too many fingers,
long neck, mutated hands, mutated, poorly drawn hands, poor hands,
extra arms, extra legs, malformed limbs, mutated, bad proportions,
cloned face, disfigured, gross, out of frame
```

### 去 AI 感专用
```
plastic skin, smooth skin, airbrushed, oversmoothed, wax skin,
unnatural skin texture, porcelain skin, doll-like, mannequin,
CGI, render, 3D render, software, photoshopped, edited
```

---

## 推荐的 prompt 模板

### 写实人像
```
(masterpiece, best quality, photorealistic:1.2), 1girl, (detailed face:1.1),
(realistic skin texture:1.1), intricate skin pores, natural makeup,
(soft lighting:1.1), (depth of field:1.1), bokeh background,
professional portrait photography, (golden hour:1.1), sharp focus, 8K
Negative prompt: (worst quality, low quality:1.4), bad anatomy, extra fingers,
plastic skin, smooth skin, airbrushed, cgi, oversaturated
Steps: 30, CFG: 7, Sampler: DPM++ 2M Karras
```

### 建筑/室内
```
(masterpiece:1.2), modern minimalist living room, floor-to-ceiling windows,
natural lighting, warm wooden floors, mid-century furniture, indoor plants,
architectural photography, ultra wide angle, realistic textures, 8K
Negative prompt: low quality, blurry, deformed, bad perspective, oversaturated
Steps: 25, CFG: 9, Sampler: DPM++ 2M Karras
```

### 概念/幻想
```
(masterpiece, best quality:1.2), fantasy landscape, floating islands in the sky,
ancient ruins, giant waterfalls, glowing crystals, dramatic lighting,
epic clouds, volumetric fog, intricate details, concept art,
trending on ArtStation, 8K
Negative prompt: lowres, bad anatomy, blurry, deformed, ugly, watermark
Steps: 35, CFG: 10, Sampler: DPM++ 2M Karras
```
